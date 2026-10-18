"""Joint design: does each screwed joint follow the defaults a mechanical engineer would use?

A joint is the pair of parts one or more fasteners hold together: the head-side part (`through[0]`) and the base part (the
next distinct part in `through`, or the part the insert/nut sits in). For each joint we measure, on the meshes:

* the contact patch (faces within ~0.1 mm: what the screws actually clamp) and
* the mating interface (faces within 1 mm: how the two parts meet; its dominant plane says which way they go together).

Defaults checked (each its own id): screw axis normal to the mating plane, screw passes through clamped faces, clearance
hole on the head side, insert/nut/thread on the far side, locating feature, >= 2 spread and balanced screws, screws along
the assembly direction and reachable without removing other parts, few screw sizes and standard lengths, counterbore for
the head, insert boss wall, edge distance, no proud heads on the outside/ground, captive nuts, heat-set inserts (not
self-tapping) for removable joints, no self-tapping along print layers, head bearing pressure on plastic.

A fastener can carry `reason` (e.g. "shear pin", "radial set screw on a flat") to accept an off-axis direction.
"""

from __future__ import annotations

import math
from collections import defaultdict

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, note, ok

G = "joints"
CONTACT_TOL = 0.15  # 0.1 mm contact + tessellation slack
MATE_TOL = 3.0  # mating interface: faces of the two parts facing each other within 3 mm
SAMPLE_H = 0.7
AXIS_LIMIT_DEG = 30.0
STANDARD_LENGTHS = [2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50, 55, 60, 65, 70, 80, 90]
# Clamp preload (N) a printed joint is typically tightened to, by thread diameter (torque-limited for plastic).
PRELOAD_N = ((1.65, 80.0), (2.05, 150.0), (2.55, 250.0), (3.05, 400.0), (4.05, 700.0), (99.0, 1100.0))
HARDWARE = {"insert", "nut"}
LOCATOR_WORDS = ("dowel", "pin", "key", "lip", "step", "spigot", "register", "tongue", "slot", "boss", "locat")


def _unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 0 else v


def _perp(d):
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    u = _unit(np.cross(d, a))
    return u, _unit(np.cross(d, u))


def _ring(c, d, r, n=12):
    u, v = _perp(d)
    a = np.arange(n) * 2 * np.pi / n
    return c + np.outer(np.cos(a), u) * r + np.outer(np.sin(a), v) * r


def _angle(a, b):
    """Angle (deg) between two lines (sign ignored)."""
    return math.degrees(math.acos(min(1.0, abs(float(np.dot(_unit(a), _unit(b)))))))


def _clusters(N, cos_lim=math.cos(math.radians(20))):
    """Greedy normal clusters (opposite normals = same plane). Returns [(unit normal, member mask)] largest first."""
    left = np.ones(len(N), bool)
    out = []
    while left.any():
        idx = np.nonzero(left)[0]
        # seed with the normal that has the most neighbours among the remaining ones
        sub = N[idx]
        seeds = idx[:: max(1, len(idx) // 40)]
        best, best_m = None, None
        for s in seeds:
            m = left & (np.abs(N @ N[s]) >= cos_lim)
            if best_m is None or m.sum() > best_m.sum():
                best, best_m = s, m
        n = N[best_m] * np.sign(N[best_m] @ N[best])[:, None]
        out.append((_unit(n.mean(axis=0)), best_m))
        left &= ~best_m
        if len(sub) == 0:
            break
    out.sort(key=lambda c: -int(c[1].sum()))
    return out


class Joint:
    def __init__(self, head, base):
        self.head, self.base = head, base
        self.fasteners = []
        self.contact = None  # (P, N) faces within CONTACT_TOL
        self.mate = None  # (P, N) faces within MATE_TOL
        self.gap = None


def _part(r, pid):
    return r.spec.part(pid) if pid else None


def _is_hw(r, pid):
    p = _part(r, pid)
    return bool(p and (p.kind in HARDWARE))


def _host_of(ctx, hw_id, dr):
    """The structural body an insert or nut sits in: most of a ring just outside it lies inside that body."""
    w = ctx.world
    hb = w.body(hw_id)
    if hb is None:
        return None
    lo, hi = hb.aabb
    c = (lo + hi) / 2
    ext = hi - lo
    rad = float(np.max(ext - np.abs(ext @ dr) * np.abs(dr))) / 2  # half the size across the axis
    P = np.vstack([_ring(c + dr * s, dr, rad + 0.4, 12) for s in (-0.3, 0.0, 0.3)])
    best, bn = None, 0
    for b in w.bodies:
        if b.fastener or b.is_wire or b.id == hw_id or _is_hw(ctx.r, b.id):
            continue
        n = int(b.inside(P).sum())
        if n > bn:
            best, bn = b.id, n
    return best


def _plate_normal(B):
    """Normal of a plate/panel-like body: one face orientation (both sides) holds >= 45% of its surface area. Else None."""
    m = B.mesh
    N, A = m.face_normals, m.area_faces
    if not len(A) or A.sum() <= 0:
        return None
    best, ba = None, 0.0
    for ax in np.eye(3).tolist() + [list(n) for n in N[np.argsort(-A)[:20]]]:
        ax = _unit(ax)
        sel = np.abs(N @ ax) > math.cos(math.radians(25))
        if A[sel].sum() > ba:
            ba, best = float(A[sel].sum()), _unit((N[sel] * np.sign(N[sel] @ ax)[:, None] * A[sel][:, None]).sum(axis=0))
    return best if ba >= 0.45 * A.sum() else None


_SAMPLES = {}


def _face_samples(A):
    """Face-interior surface samples (spacing ~SAMPLE_H) with face normals; no vertices (their normals are averaged)."""
    import trimesh
    key = (id(A.geom), A.M.tobytes())
    if key not in _SAMPLES:
        m = A.mesh
        n = int(min(max(m.area / SAMPLE_H ** 2, 50), 60000))
        P, fi = trimesh.sample.sample_surface_even(m, n, seed=7) if hasattr(trimesh.sample, "sample_surface_even") else trimesh.sample.sample_surface(m, n, seed=7)
        _SAMPLES[key] = (P, m.face_normals[fi])
        if len(_SAMPLES) > 256:
            _SAMPLES.pop(next(iter(_SAMPLES)))
    return _SAMPLES[key]


def _surface_patch(A, B, tol):
    P, N = _face_samples(A)
    lo, hi = B.aabb
    m = np.all((P > lo - tol) & (P < hi + tol), axis=1)
    P, N = P[m], N[m]
    if not len(P):
        return P, N, np.zeros(0)
    import trimesh
    from scipy.spatial import cKDTree
    Q, _ = B.surface(0.6)
    dq, _ = cKDTree(Q).query(P, distance_upper_bound=tol + 0.6)
    pre = np.isfinite(dq)
    P, N = P[pre], N[pre]
    if not len(P):
        return P, N, np.zeros(0)
    cp, d, tri = trimesh.proximity.closest_point(B.mesh, P)
    facing = np.einsum("ij,ij->i", N, B.mesh.face_normals[tri]) < -0.7
    k = (d < tol) & facing
    return P[k], N[k], d[k]


def _resolve_joints(ctx, out):
    r, w = ctx.r, ctx.world
    joints, info = {}, {}
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            ctx.not_checked.append(f"Joint checks for `{f.id}`: designation `{f.designation}` not understood")
            continue
        dr = _unit(f.dir)
        through = [t for t in f.through if w.body(t) is not None]
        missing = [t for t in list(f.through) + ([f.threads_into] if f.threads_into else []) if w.body(t) is None]
        if missing:
            ctx.not_checked.append(f"Joint checks for `{f.id}`: `{', '.join(missing)}` not bodies")
        host = None
        if f.threads_into and w.body(f.threads_into) is not None:
            host = _host_of(ctx, f.threads_into, dr) if _is_hw(r, f.threads_into) else f.threads_into
            if host is None:
                ctx.not_checked.append(f"Joint `{f.id}`: no part found around `{f.threads_into}` (insert/nut host unknown)")
        chain = through + ([host] if host else [])
        dedup = []
        for c in chain:
            if c not in dedup:
                dedup.append(c)
        info[f.id] = (f, dl, dr, through, host)
        if len(dedup) < 2:
            if not through:
                ctx.not_checked.append(f"Joint checks for `{f.id}`: no `through` part, so the clamped joint is unknown")
            continue  # a set screw or a screw into its own part: no joint between two parts
        key = (dedup[0], dedup[1])
        j = joints.setdefault(key, Joint(*key))
        j.fasteners.append(f.id)
    for j in joints.values():
        A, B = w.body(j.head), w.body(j.base)
        P, N, d = _surface_patch(A, B, MATE_TOL)
        j.mate = (P, N)
        j.gap = float(d.min()) if len(d) else None
        k = d < CONTACT_TOL
        j.contact = (P[k], N[k])
    return joints, info


_SLIDE_CACHE = {}


def _slides_along(ctx, pid, d):
    """True when part `pid` (with its children) can be lifted off along `d` once the parts removed before it are gone."""
    from . import assembly
    key = (id(ctx), pid, tuple(np.round(d, 3)))
    if key in _SLIDE_CACHE:
        return _SLIDE_CACHE[key]
    w = ctx.world
    order = {s.id: s.order for s in ctx.assembly}
    mine = order.get(pid, 0)
    present = [not (b.fastener or b.is_wire or order.get(b.id, 1e9) < mine) for b in w.bodies]
    members = assembly.group(ctx, pid)
    res = assembly.slide(ctx, members, present, np.asarray(d, float))[0] == "ok"
    _SLIDE_CACHE[key] = res
    return res


def _fid(ids):
    return ", ".join(f"`{i}`" for i in ids)


def _reason(f):
    return (f._extra.get("reason") or f._extra.get("axis_reason") or "").strip()


def _conn(r, a, b):
    for c in r.spec.connections:
        if {c.a, c.b} == {a, b}:
            return c
    return None


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    if not r.spec.fasteners:
        return [note("joint.none", G, "No screwed joints", "The spec has no fasteners; joint design checks had nothing to judge.")]
    joints, info = _resolve_joints(ctx, out)
    area = SAMPLE_H * SAMPLE_H
    plan = {s.id: _unit(s.dir) for s in (ctx.assembly or [])}
    if not plan:
        ctx.not_checked.append("Joint screw direction vs assembly direction: no assembly plan (run deep mode)")
    bodies_solid = [b for b in w.bodies if not b.fastener and not b.is_wire]
    floor = r.spec.ground_z
    if floor is None:
        floor = ctx.metrics.get("ground_z")
    if floor is None and bodies_solid:
        floor = min(float(b.aabb[0][2]) for b in bodies_solid)

    # ---- per joint ----
    for (a, b), j in joints.items():
        fs = [info[i] for i in j.fasteners]
        Pm, Nm = j.mate
        Pc, Nc = j.contact
        if len(Pm) == 0:
            out.append(fail("joint.no_contact", G, WARNING, "Screwed parts do not touch",
                            f"{_fid(j.fasteners)} join `{a}` to `{b}`, but no face of `{a}` is within {MATE_TOL} mm of `{b}`; the screws bridge a gap and will pull the parts until something bends.")
                       .on(a, b, *j.fasteners).fix(f"Give `{a}` a seat face that sits on `{b}` where the screws clamp."))
            ctx.not_checked.append(f"Joint `{a}`-`{b}`: no mating faces found, interface checks skipped")
            continue
        cl = _clusters(Nm)
        mate_n, mate_m = cl[0]
        pn = _plate_normal(w.body(a))
        if pn is not None:  # a plate is joined through its face: prefer a mating face along its normal when it is a real one
            for n_, m_ in cl[1:]:
                if m_.sum() >= 0.5 * mate_m.sum() and _angle(n_, pn) < 20 and _angle(mate_n, pn) > 30:
                    mate_n, mate_m = n_, m_
                    break
        mate_area = float(mate_m.sum()) * area
        # 1. screw axis vs how the parts meet
        bad = []
        for f, dl, dr, _, _ in fs:
            ang = _angle(dr, mate_n)
            if ang > AXIS_LIMIT_DEG:
                if _reason(f):
                    out.append(note("joint.axis_reason", G, "Off-axis screw accepted by reason",
                                    f"`{f.id}` is {ang:.0f} deg off the `{a}`-`{b}` mating plane normal; accepted: {_reason(f)}").on(f.id, a, b))
                else:
                    bad.append((f, ang))
        if bad:
            f0 = bad[0][0]
            nm = np.round(mate_n, 2).tolist()
            out.append(fail("joint.axis_vs_interface", G, BLOCKER, "Screws do not point the way the parts meet",
                            f"`{a}` meets `{b}` on a {mate_area:.0f} mm2 face with normal {nm}, but {_fid(f.id for f, _ in bad)} run "
                            f"{max(x for _, x in bad):.0f} deg off it (limit {AXIS_LIMIT_DEG:.0f}). They clamp only small tabs while the main interface is loaded in shear/peel by the screws.")
                       .on(a, b, *[f.id for f, _ in bad]).here(Pm[mate_m].mean(axis=0))
                       .expect(f"<= {AXIS_LIMIT_DEG:.0f} deg from {nm}", f"{max(x for _, x in bad):.0f} deg")
                       .fix(f"Turn the screws to run along {nm} through the {mate_area:.0f} mm2 face where `{a}` meets `{b}` (head on the `{a}` side, insert in `{b}`), "
                            f"or add `reason` on each fastener if the off-axis direction is deliberate (e.g. shear pin)."))
        # 2. fastener passes through the clamped contact faces
        for f, dl, dr, through, host in fs:
            d = dl[0]
            dk = catalog.screw_dims(d)[0]
            at = np.asarray(f.at, float)
            if len(Pc):
                rel = Pc - at
                t = rel @ dr
                radial = np.linalg.norm(rel - np.outer(t, dr), axis=1)
                near = (radial < dk * 0.75 + 1.0) & (t > -0.5) & (t < dl[1] + 0.5)
            else:
                near = np.zeros(0, bool)
            if not near.any():
                out.append(fail("joint.through_contact", G, BLOCKER, "Screw does not clamp the mating faces",
                                f"`{f.id}` joins `{a}` to `{b}` but no face where they touch (within 0.1 mm) lies under its head footprint along the shank"
                                + (f" (closest faces are {j.gap:.2f} mm apart)" if j.gap is not None and j.gap >= CONTACT_TOL else "")
                                + "; tightening it bends the parts instead of clamping a seat.")
                           .on(f.id, a, b).here(at)
                           .fix(f"Put the screw through the face where `{a}` sits on `{b}` (contact patch), so the head clamps `{a}` onto `{b}`."))
                continue
            angs = [_angle(dr, n) for n in Nc[near]]
            if min(angs) > 60.0 and not _reason(f):
                out.append(fail("joint.parallel_interface", G, BLOCKER, "Screw runs along the joint instead of across it",
                                f"`{f.id}` passes {min(angs):.0f} deg or more off every face where `{a}` touches `{b}`; a screw parallel to the interface clamps nothing and only works in shear.")
                           .on(f.id, a, b).here(at)
                           .fix("Turn the screw normal to the contact faces, or add `reason` (e.g. \"shear pin\") if it is meant to work in shear."))
        # 3. locating feature
        conn = _conn(r, a, b)
        located = bool(conn and (conn.mechanical_key or any(w_ in (conn.reason or "").lower() for w_ in LOCATOR_WORDS)))
        if not located and len(Pc):
            ccl = _clusters(Nc)
            main = ccl[0][0]
            side = [c for c in ccl[1:] if _angle(c[0], main) > 45 and c[1].sum() * area >= 3.0]
            located = bool(side)
        if not located:
            out.append(fail("joint.no_locator", G, WARNING, "Joint has no locating feature",
                            f"`{a}` on `{b}` is held in place only by friction and the screws' shear ({_fid(j.fasteners)}); no lip, step, pin or spigot locates it.")
                       .on(a, b).fix("Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate."))
        # 4. bolt pattern
        keyed = bool(conn and conn.mechanical_key)
        if len(fs) < 2 and not keyed:
            out.append(fail("joint.single_fastener", G, WARNING, "Joint held by a single screw",
                            f"`{a}`-`{b}` is held by only {_fid(j.fasteners)}; one screw lets the part pivot and loosen.")
                       .on(a, b, *j.fasteners).fix("Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection."))
        if len(fs) >= 2:
            ax = mate_n
            pts = np.array([np.asarray(f.at, float) for f, *_ in fs])
            proj = pts - np.outer(pts @ ax, ax)
            span = max(np.linalg.norm(p - q) for p in proj for q in proj)
            d = max(dl[0] for _, dl, *_ in fs)
            if span < 3 * d:
                out.append(fail("joint.bolt_spread", G, WARNING, "Screws bunched together",
                                f"The {len(fs)} screws of `{a}`-`{b}` span only {span:.1f} mm (needs >= {3 * d:.1f} mm = 3d) and cannot resist a twisting load.")
                           .on(a, b, *j.fasteners).expect(f">= {3 * d:.1f} mm", f"{span:.1f} mm").fix("Spread the screws to opposite ends of the joint."))
            mc = Pm[mate_m].mean(axis=0)
            mproj = mc - (mc @ ax) * ax
            pc = proj.mean(axis=0)
            extent = float(np.linalg.norm(np.ptp(Pm[mate_m] - np.outer(Pm[mate_m] @ ax, ax), axis=0))) / 2
            off = float(np.linalg.norm(pc - mproj))
            if extent > 0 and off > 0.5 * extent:
                out.append(fail("joint.bolt_symmetry", G, WARNING, "Screw pattern is off-centre on the joint",
                                f"The screws of `{a}`-`{b}` sit {off:.1f} mm from the middle of the {extent * 2:.0f} mm interface; impacts on the far end lever the joint open.")
                           .on(a, b, *j.fasteners).here(pc).fix("Place the screws symmetrically about the interface (or the load path)."))

    # ---- per fastener ----
    sizes, desigs = defaultdict(list), defaultdict(list)
    for fid, (f, dl, dr, through, host) in info.items():
        d, ln = dl
        dk, k, _ = catalog.screw_dims(d)
        at = np.asarray(f.at, float)
        sizes[d].append(fid)
        desigs[f"M{d:g}x{ln:g}"].append(fid)
        if not any(abs(ln - s) < 0.01 for s in STANDARD_LENGTHS):
            out.append(fail("joint.standard_length", G, WARNING, "Non-standard screw length",
                            f"`{fid}` is {f.designation}; {ln:g} mm is not a stock ISO length.").on(fid)
                       .fix(f"Use {min(STANDARD_LENGTHS, key=lambda s: abs(s - ln))} mm, or adjust the stack."))
        head = through[0] if through else None
        threaded = f.threads_into
        hw = _is_hw(r, threaded)
        clamp_side = [t for t in through if t != host and t != threaded]
        # clearance hole in head-side parts
        for t in clamp_side:
            B = w.body(t)
            P = np.vstack([_ring(at + dr * s, dr, (d + 0.2) / 2 - 0.05, 12) for s in np.arange(0.2, ln, 0.3)])
            ins = B.inside(P)
            if ins.any():
                out.append(fail("joint.clearance_hole", G, BLOCKER, "No clearance hole for the screw",
                                f"`{fid}` passes through `{t}`, which has material within {(d + 0.2) / 2:.2f} mm of the screw axis; the head-side part needs a clearance hole >= {d + 0.2:.1f} mm so the screw clamps instead of threading into it.")
                           .on(fid, t).here(P[np.argmax(ins)]).expect(f">= {d + 0.2:.1f} mm hole", "smaller")
                           .fix(f"Cut a {d + 0.2:.1f}-{d + 0.4:.1f} mm through hole in `{t}` on the screw axis."))
        # counterbore wide/deep enough for the head
        for t in through[:1] if (f.head or "socket") != "none" else []:
            B = w.body(t)
            P = np.vstack([_ring(at - dr * s, dr, dk / 2 + 0.1, 12) for s in (0.2, k / 2, k - 0.2)])
            ins = B.inside(P)
            if ins.any():
                out.append(fail("joint.counterbore", G, WARNING, "Counterbore too small for the screw head",
                                f"The {dk:.1f} mm head of `{fid}` is cut into `{t}`; a counterbore needs >= {dk + 0.4:.1f} mm dia and >= {k:.1f} mm depth.")
                           .on(fid, t).here(at).fix(f"Open the counterbore in `{t}` to {dk + 0.5:.1f} mm and {k + 0.2:.1f} mm deep, or move `at` to its floor."))
                break
        # threaded side
        tp = _part(r, threaded)
        if threaded and tp is not None and not hw and w.body(threaded) is not None:
            if catalog.part_is_printed(tp.process, tp.material):
                if f.removable:
                    out.append(fail("joint.selftap_removable", G, WARNING, "Removable screw self-taps into plastic",
                                    f"`{fid}` threads straight into printed `{threaded}` but is removable; printed threads wear out after a few cycles.")
                               .on(fid, threaded).fix(f"Add a heat-set insert (`heatset_m{d:g}`) in `{threaded}` and thread into that."))
                orient = str(tp._extra.get("print_orientation") or "+z")
                bz = {"+x": [1, 0, 0], "-x": [1, 0, 0], "+y": [0, 1, 0], "-y": [0, 1, 0]}.get(orient, [0, 0, 1])
                if _angle(dr, bz) < 30:
                    out.append(fail("joint.layer_tension", G, WARNING, "Screw pulls printed layers apart",
                                    f"`{fid}` self-taps into `{threaded}` along its print direction ({orient}); the pull-out load is across layer lines (about half strength).")
                               .on(fid, threaded).fix("Use a heat-set insert, a captive nut, or turn the screw (or the print) so the thread runs along the layers."))
                Tb = w.body(threaded)
                lo, hi = float(at @ dr), float((at + dr * ln) @ dr)
                cs = np.array([[x, y, z] for x in Tb.aabb[:, 0] for y in Tb.aabb[:, 1] for z in Tb.aabb[:, 2]]) @ dr
                eng = max(min(hi, cs.max()) - max(lo, cs.min()), 0.0)
                if eng < 2.0 * d:
                    out.append(fail("joint.plastic_engagement", G, WARNING, "Too little thread in plastic",
                                    f"`{fid}` has {eng:.1f} mm of thread in printed `{threaded}`; plastic needs >= {2 * d:.1f} mm (2d).")
                               .on(fid, threaded).expect(f">= {2 * d:.1f} mm", f"{eng:.1f} mm").fix("Use a longer screw or an insert."))
                ring = _ring(at + dr * min(ln * 0.7, ln - 0.5), dr, 1.5 * d, 12)
                frac = float(Tb.inside(ring).mean())
                if frac < 0.75:
                    out.append(fail("joint.thin_wall", G, WARNING, "Screw taps into a thin wall",
                                    f"Only {frac * 100:.0f}% of a {3 * d:.1f} mm boss around `{fid}` is material in `{threaded}`; the wall will split.")
                               .on(fid, threaded).fix(f"Give the hole a boss >= {3 * d:.1f} mm OD (wall >= d)."))
        if hw and tp is not None and w.body(threaded) is not None and (host or tp.kind == "nut"):
            Hb, Hw = (w.body(host) if host else None), w.body(threaded)
            lo, hi = Hw.aabb
            c = (lo + hi) / 2
            ext = hi - lo
            length = float(abs(ext @ dr))
            od = float(np.max(ext - np.abs(dr) * length))
            if tp.kind == "insert" and Hb is not None:
                ring = np.vstack([_ring(c + dr * s, dr, od - 0.1, 16) for s in (-length * 0.3, 0, length * 0.3)])
                frac = float(Hb.inside(ring).mean())
                if frac < 0.75:
                    out.append(fail("joint.insert_boss", G, WARNING, "Insert boss too thin",
                                    f"Insert `{threaded}` ({od:.1f} mm OD) sits in `{host}` with only {frac * 100:.0f}% of a {2 * od:.1f} mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.")
                               .on(threaded, host).here(c).fix(f"Thicken `{host}` around the insert to a {2 * od:.1f} mm boss."))
                if length + 0.01 < 1.5 * d:
                    out.append(fail("joint.insert_length", G, WARNING, "Insert shorter than 1.5d",
                                    f"Insert `{threaded}` is {length:.1f} mm long; use >= {1.5 * d:.1f} mm for full thread strength.").on(threaded))
            elif tp.kind == "nut":
                ring = _ring(c, dr, od / 2 + 0.4, 16)
                frac = 0.0
                for o in bodies_solid:
                    if o.id in (threaded,) or _is_hw(r, o.id):
                        continue
                    frac = max(frac, float(o.inside(ring).mean()))
                if frac < 0.5:
                    out.append(fail("joint.loose_nut", G, WARNING, "Nut is not captive",
                                    f"Nut `{threaded}` on `{fid}` has material on only {frac * 100:.0f}% of its flats; it will spin and must be held with a spanner (impossible once assembled).")
                               .on(threaded, fid).here(c).fix("Sink the nut into a hex nut trap in the part (or replace it with a heat-set insert)."))
        # head bearing pressure on plastic
        hp = _part(r, head)
        if hp is not None and catalog.part_is_printed(hp.process, hp.material) and (f.head or "socket") not in ("flange", "washer"):
            if not f._extra.get("washer"):
                F = next(v for lim, v in PRELOAD_N if d <= lim)
                a_mm2 = math.pi / 4 * (dk ** 2 - (d + 0.2) ** 2)
                s = F / a_mm2
                m = catalog.mech(hp.material)
                lim = (m[0] if m else 40.0) * catalog.PRINTED_Z_FACTOR
                if s > lim:
                    out.append(fail("joint.head_bearing", G, WARNING, "Screw head crushes the plastic",
                                    f"`{fid}` head bears {s:.0f} MPa on printed `{head}` at ~{F:.0f} N clamp; creep limit ~{lim:.0f} MPa.")
                               .on(fid, head).fix("Add a washer (`\"washer\": true`), use a flange/button head, or a larger head."))
        # proud heads on the outside or the floor
        if (f.head or "socket") not in ("countersunk", "flat", "none"):
            top = at - dr * (k + 0.3)
            ray = np.array([top - dr * s for s in np.arange(0.0, 60.0, 0.7)])
            exposed = not any(o.inside(ray).any() for o in bodies_solid if o.id not in through)
            rec = np.vstack([_ring(at - dr * (k * 0.5), dr, dk / 2 + 0.5, 12)])
            recessed = max((float(o.inside(rec).mean()) for o in bodies_solid), default=0.0) >= 0.5
            if exposed and not recessed:
                hb = w.body(fid)
                low = float(hb.aabb[0][2]) if hb is not None else float(top[2])
                if floor is not None and low < floor + 1.0:
                    out.append(fail("joint.head_ground", G, BLOCKER, "Screw head touches the ground",
                                    f"The head of `{fid}` sits {low - floor:.1f} mm above the floor plane and sticks out of `{head}`; it scrapes the arena and holds the robot up.")
                               .on(fid, head).here(at).fix("Recess it in a counterbore or use a countersunk screw flush with the skid surface."))
                else:
                    out.append(fail("joint.head_proud", G, WARNING, "Screw head proud on an outer surface",
                                    f"The head of `{fid}` stands {k:.1f} mm proud of `{head}` on the outside; hits shear heads and opponents catch on them.")
                               .on(fid, head).here(at).fix("Counterbore the head flush or use a countersunk (`head: countersunk`) screw."))
        # direction vs assembly direction, and serviceability
        if head and head in plan:
            dout = plan[head]
            if _angle(dr, dout) > 30 and not _reason(f) and not _slides_along(ctx, head, -dr):
                out.append(fail("joint.assembly_dir", G, WARNING, "Screw not inserted along the part's assembly direction",
                                f"`{head}` can only go on along {np.round(-dout, 2).tolist()} but `{fid}` is driven along {np.round(dr, 2).tolist()} ({_angle(dr, dout):.0f} deg off); the screw cannot pull the part home onto its seat.")
                           .on(fid, head).fix("Drive the screws along the direction the part slides on, through its seat face."))
        elif head and plan:
            ctx.not_checked.append(f"Joint `{fid}`: `{head}` has no assembly step, screw vs assembly direction not checked")
        if f.tool:
            top = at - dr * (k + 0.2)
            ray = np.array([top - dr * s for s in np.arange(0.0, 60.0, 0.5)])
            first, ft = None, 1e9
            for o in bodies_solid:
                if o.id in through or o.id == threaded:
                    continue
                ins = np.nonzero(o.inside(ray))[0]
                if len(ins) and ins[0] < ft:
                    first, ft = o, ins[0]
            if first is not None:
                op = _part(r, first.id)
                is_cover = op is not None and (op.kind in ("armour", "plate", "lid", "cover") or any(p.cover == first.id for p in r.spec.parts))
                if not is_cover:
                    out.append(fail("joint.service_access", G, WARNING, "Screw only reachable after removing another part",
                                    f"The driver line out of `{fid}` hits `{first.id}` {ft * 0.5:.1f} mm from the head; `{first.id}` must come off before this joint can be serviced.")
                               .on(fid, first.id).here(top - dr * ft * 0.5)
                               .fix(f"Turn the screw so its driver path exits through an open face or a removable cover, not through `{first.id}`."))
    if len(sizes) > 3:
        out.append(fail("joint.screw_sizes", G, WARNING, "Too many screw diameters",
                        f"{len(sizes)} thread sizes ({', '.join(f'M{d:g}' for d in sorted(sizes))}); keep <= 3 so one driver set and one insert stock do.")
                   .fix("Standardise on one or two sizes (e.g. M2 and M3)."))
    if len(desigs) > 5:
        out.append(fail("joint.screw_variety", G, WARNING, "Too many different screws",
                        f"{len(desigs)} different screws ({', '.join(sorted(desigs))}); a pit kit should need <= 5.")
                   .fix("Adjust stacks so neighbouring joints share one length."))
    if not any(not x.passed and x.severity in (BLOCKER, WARNING) for x in out):
        out.append(ok("joint.ok", G, "Screwed joints follow engineering defaults",
                      f"{len(joints)} joints: screws normal to the mating faces, through the contact patch, located, patterned and serviceable."))
    return out
