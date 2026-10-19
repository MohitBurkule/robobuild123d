"""Measurements for the combat failure-mode checks (not a check group itself; used by `threat`).

`facts(ctx)` samples the robot once (surface points with normals and owners), runs the attack-model visibility passes
(`attack.visible`) and fills a flat dict of facts. Each block is independent and guarded: a block that raises leaves
its keys missing (the rule then reports "not measured") and records the error in `T["_errors"]`.

The ground-game facts of `combat_ground.facts` (perimeter edge gaps, skirts, wheels, centre of mass...) are reused as
`T["cg"]` and copied to the top level where a rule needs them.
"""

from __future__ import annotations

import math

import numpy as np

from .. import _physics as ph
from .. import combat_ground as cg
from . import attack as A

HEAVY_MIN_G = 10.0
STATIC_SKIP = ("insert", "nut", "pin", "shaft", "bearing", "belt", "pulley")


class S:  # shared sample state
    pass


def _sample(ctx, h):
    w = ctx.world
    s = S()
    s.floor = ph.floor_z(ctx)
    s.bodies = [b for b in w.bodies if not b.is_wire]
    rotor = {b.id for b in s.bodies if b.kind == "weapon"}
    changed = True
    while changed:  # parts riding on a weapon (hub, bell, spacer) spin with it
        changed = False
        for b in s.bodies:
            p = ph.part(ctx, b)
            if b.id not in rotor and p is not None and (p.parent in rotor or p.rotates_with in rotor):
                rotor.add(b.id)
                changed = True
    s.rotor = rotor
    pts, nrm, own, face = [], [], [], []
    for i, b in enumerate(s.bodies):
        p, n = b.surface(h)
        nf = len(p) - len(b.mesh.vertices)
        pts.append(p)
        nrm.append(n)
        own.append(np.full(len(p), i))
        f = np.zeros(len(p), bool)
        f[:max(nf, 0)] = True
        face.append(f)
    s.P, s.N, s.O, s.face = np.vstack(pts), np.vstack(nrm), np.concatenate(own), np.concatenate(face)
    s.kind = np.array([b.kind for b in s.bodies], dtype=object)[s.O]
    s.is_rotor = np.array([b.id in rotor for b in s.bodies])[s.O]
    s.is_wheel = np.isin(s.kind, A.WHEELISH)
    s.is_fast = np.array([b.fastener for b in s.bodies])[s.O]
    s.z = s.P[:, 2] - s.floor
    lo, hi = s.P.min(axis=0), s.P.max(axis=0)
    s.centre = (lo + hi) / 2
    s.views = {}
    s.h = h
    s.cell = max(A.CELL_MM, 2.0 * h)  # z-buffer cell: coarser than the sampling so plates do not look porous
    return s


def view(s, bearing, elev=0.0):
    key = (int(round(bearing)) % 360, float(elev))
    if key not in s.views:
        s.views[key] = A.visible(s.P - s.centre, A.travel_dir(*key), cell=s.cell)
    return s.views[key]


def skin(s):
    """Points any attacker (horizontal all round, 30 deg from above, straight down) meets first."""
    if not hasattr(s, "_skin"):
        m = np.zeros(len(s.P), bool)
        for b in A.ALL_AROUND:
            m |= view(s, b, 0.0) | view(s, b, 30.0)
        m |= view(s, 0, 90.0)
        s._skin = m
    return s._skin


def _mat(ctx, b):
    return ph.material_of(ctx, b)


def _longest_run(z, step):
    if not len(z):
        return 0.0
    k = np.unique(np.floor(z / step).astype(int))
    best = cur = 1
    for a, c in zip(k[:-1], k[1:]):
        cur = cur + 1 if c - a == 1 else 1
        best = max(best, cur)
    return best * step


def _crit(b):
    return b.kind in A.CRITICAL or (b.kind == "esc" and "rx" in b.id)


def _receivers(bodies):
    rx = [b for b in bodies if b.kind == "receiver"]
    return rx or [b for b in bodies if b.kind == "esc" and ("rx" in b.id or "receiver" in b.id)]


# ---------------------------------------------------------------------------------------------------- blocks

def m_bite(ctx, s, T):
    """VS01 / VS05 / HS01 / HS02: what the incoming spinner meets."""
    d = A.bite_depth()
    T["bite_mm"] = d
    cos35 = math.cos(math.radians(35))
    best, where = 0.0, None
    for brg in A.FRONT_SIDE:
        for el in A.ATTACKS["vertical"]["elev"]:
            dv = A.travel_dir(brg, el)
            m = view(s, brg, el) & ~s.is_rotor & ~s.is_wheel & (s.z >= 0) & (s.z <= 40) & s.face
            m &= (s.N @ -dv) > cos35
            if not m.any():
                continue
            u = np.cross(dv, [0, 0, 1.0])
            u = u / (np.linalg.norm(u) or 1.0)
            col = np.floor(s.P[m] @ u / s.cell).astype(int)
            zz = s.z[m]
            idx = np.nonzero(m)[0]
            for c in np.unique(col):
                sel = col == c
                h = _longest_run(zz[sel], s.h)
                if h > best:
                    best = h
                    j = idx[sel][0]
                    where = (s.bodies[s.O[j]].id, brg, el, s.P[j])
    T["vs01.step_mm"] = best
    T["vs01.where"] = where
    # VS05: drum band, front.
    tot = blunt = 0
    for brg in range(60, 121, 10):
        dv = A.travel_dir(brg)
        m = view(s, brg) & ~s.is_rotor & ~s.is_wheel & (s.z >= 15) & (s.z <= 45) & s.face
        tot += int(m.sum())
        blunt += int((m & ((s.N @ -dv) > math.cos(math.radians(30)))).sum())
    T["vs05.blunt_frac"] = blunt / tot if tot >= 10 else 0.0
    # HS01: vertical exposed faces in the horizontal-spinner band, all round.
    vert = 0
    n_b = 0
    sin15 = math.sin(math.radians(15))
    for brg in A.ALL_AROUND:
        dv = A.travel_dir(brg)
        m = view(s, brg) & ~s.is_rotor & ~s.is_wheel & (s.z >= 2) & (s.z <= 15) & s.face
        if m.sum() < 3:
            continue
        n_b += 1
        skirt = np.isin(s.kind[m], ("wedge", "fork", "skirt", "wedgelet"))
        v = (np.abs(s.N[m, 2]) < sin15) & ((s.N[m] @ -dv) > 0.5) & ~skirt
        if v.mean() >= 0.5:
            vert += 1
    T["hs01.vert_frac"] = vert / n_b if n_b else None
    # HS02: wheels first-hit at wheel-centre height.
    wh = [b for b in s.bodies if b.kind in A.WHEELISH]
    if wh:
        zc = float(np.mean([b.center[2] for b in wh])) - s.floor
        exposed = []
        for brg in range(0, 360, 5):
            if 250 <= brg <= 290:  # rear +/- 20 deg
                continue
            m = view(s, brg) & (np.abs(s.z - zc) <= 3.0) & ~s.is_rotor
            if m.any() and s.is_wheel[m].any():
                exposed.append(brg)
        T["hs02.exposed"] = exposed
    else:
        T["hs02.exposed"] = []


def m_top(ctx, s, T):
    """HS03 / HA01 / HA02 / HA03 / WL04 / DB04: the top surface, its thickness and what sits under it."""
    top = view(s, 0, 90.0)
    ztop = float(s.z[top].max())
    near = top & (s.z >= ztop - 5.0) & ~s.is_rotor
    crit_top = sorted({s.bodies[i].id for i in np.unique(s.O[near]) if s.bodies[i].kind in ("switch", "receiver", "belt", "pulley", "esc", "battery") or _receivers([s.bodies[i]])})
    T["hs03.top_parts"] = crit_top
    T["db04.open"] = sorted({s.bodies[i].id for i in np.unique(s.O[top & s.face]) if _crit(s.bodies[i]) and s.bodies[i].kind not in ("motor", "switch")})
    # Grid of top cells (5 mm): topmost visible point and its plate.
    cell = 5.0
    m = top & s.face & ~s.is_rotor & ~s.is_wheel & ~s.is_fast
    idx = np.nonzero(m)[0]
    if not len(idx):
        return
    key = np.floor(s.P[idx, :2] / cell).astype(int)
    order = np.lexsort((-s.P[idx, 2], key[:, 1], key[:, 0]))
    idx, key = idx[order], key[order]
    firsts = np.ones(len(idx), bool)
    firsts[1:] = np.any(key[1:] != key[:-1], axis=1)
    cells = idx[firsts]
    crit = [b for b in s.bodies if _crit(b)]
    rows = []
    by_body = {}
    for j in cells:
        by_body.setdefault(s.O[j], []).append(j)
    thick = {}
    for bi, js in by_body.items():
        js = np.array(js)
        t = A.thickness(s.bodies[bi], s.P[js], s.N[js], max_mm=12.0, step=0.5)
        thick.update(dict(zip(js.tolist(), t.tolist())))
    for j in cells:
        b = s.bodies[s.O[j]]
        p = s.P[j]
        t = thick[int(j)]
        lo, hi = b.aabb
        span = float(np.clip(min(p[0] - lo[0], hi[0] - p[0], p[1] - lo[1], hi[1] - p[1]), 5.0, 30.0))
        cap = A.energy_capacity_j(_mat(ctx, b), t * math.pi * span * span)
        under = []
        for c in crit:
            if c.id == b.id:
                continue
            clo, chi = c.aabb
            if clo[0] <= p[0] <= chi[0] and clo[1] <= p[1] <= chi[1] and chi[2] < p[2]:
                under.append((c, float(p[2] - t - chi[2])))
        rows.append({"plate": b.id, "p": p, "t": t, "span": span, "cap": cap, "under": [(c.id, c.kind, g) for c, g in under]})
    T["top_cells"] = rows
    over = [r for r in rows if r["under"]]
    known = [r for r in over if r["cap"] is not None]
    T["ha01.min_cap_j"] = min((r["cap"] for r in known), default=None) if over else 99.0
    T["ha01.where"] = min(known, key=lambda r: r["cap"])["plate"] if known else None
    if over and not known:
        T["ha01.min_cap_j"] = None
    bad = []
    for r in over:
        for cid, ck, g in r["under"]:
            if (ck in ("battery", "esc", "receiver")) and g <= 10.0 and r["cap"] is not None and r["cap"] < A.E_HAMMER_J:
                bad.append((cid, r["plate"], round(g, 1), round(r["cap"], 2)))
    T["ha02.bad"] = sorted(set(bad))
    # WL04: crusher on the shell over the battery.
    bat = [b for b in s.bodies if b.kind == "battery"]
    if bat:
        b = bat[0]
        c = b.center
        cand = [r for r in over if any(cid == b.id for cid, _, _ in r["under"])]
        if cand:
            r = min(cand, key=lambda r: np.hypot(*(r["p"][:2] - c[:2])))
            pb = next(x for x in s.bodies if x.id == r["plate"])
            mm = A.mech(_mat(ctx, pb))
            gap = next(g for cid, _, g in r["under"] if cid == b.id)
            L = float(min(pb.aabb[1][0] - pb.aabb[0][0], pb.aabb[1][1] - pb.aabb[0][1]))
            bw = float(min(b.aabb[1][0] - b.aabb[0][0], b.aabb[1][1] - b.aabb[0][1]))
            if mm:
                I = bw * r["t"] ** 3 / 12.0
                T["wl04.defl_mm"] = 200.0 * L ** 3 / (48.0 * mm[1] * I)
            T["wl04.gap_mm"] = max(gap, 0.0)
            T["wl04.plate"] = r["plate"]


def m_routes(ctx, s, T):
    """HA03 / GD02 / GD07 / GD08: routed wires against the top skin, the outer skin and the weapon sweep."""
    routes = list(ctx.routes or [])
    T["n_routes"] = len(routes)
    T["n_wires"] = len(ctx.r.spec.wires)
    if not routes:
        return
    from scipy.spatial import cKDTree
    top = view(s, 0, 90.0)
    tk = cKDTree(s.P[top])
    sk = cKDTree(s.P[skin(s) & ~s.is_rotor])
    ha, gd2 = [], []
    wires = {w.id: w for w in ctx.r.spec.wires}
    ids = {p.id for p in ctx.r.spec.parts}
    for rt in routes:
        Q = np.asarray(rt.points, float)
        if len(Q) < 2:
            continue
        Qd = _densify(Q, 1.0)
        rr = rt.od_mm / 2
        d, _ = tk.query(Qd)
        ha.append((float(d.min() - rr), rt.id))
        w = wires.get(rt.id)
        if w is not None and (w.kind == "power" or (w.awg is not None and w.awg <= 20)):
            ends = {A.part_of(getattr(w, "from"), ids), A.part_of(w.to, ids)}
            if ends & {p.id for p in ctx.r.spec.parts if p.kind in ("battery", "switch")}:
                core = Qd[(np.linalg.norm(Qd - Q[0], axis=1) > 5) & (np.linalg.norm(Qd - Q[-1], axis=1) > 5)]
                if len(core):
                    dd, _ = sk.query(core)
                    gd2.append((float(dd.min() - rr), rt.id))
    T["ha03.min_mm"] = min(ha) if ha else None
    T["gd02.min_mm"] = min(gd2) if gd2 else 99.0
    # GD07: slack.
    short = []
    for rt in routes:
        w = wires.get(rt.id)
        Q = np.asarray(rt.points, float)
        slack = w.slack_mm if w is not None else None
        if slack is None and len(Q) >= 2:
            slack = rt.length_mm - float(np.linalg.norm(Q[-1] - Q[0]))
        if slack is not None and slack < 5.0:
            short.append(rt.id)
    T["gd07.short"] = short
    # GD08: weapon swept volume.
    sw = _weapon_sweeps(ctx, s)
    gaps = []
    for rt in routes:
        Qd = _densify(np.asarray(rt.points, float), 0.5)
        for wid, o, a, R, t0, t1 in sw:
            g = A.cyl_gap(Qd, o, a, R, t0, t1) - rt.od_mm / 2
            k = int(np.argmin(g))
            gaps.append((float(g[k]), rt.id, wid, Qd[k]))
    T["gd08.min"] = min(gaps, key=lambda x: x[0]) if gaps else None


def _densify(Q, step):
    out = [Q[0]]
    for a, b in zip(Q[:-1], Q[1:]):
        n = max(int(np.linalg.norm(b - a) / step), 1)
        out.extend(a + (b - a) * (k / n) for k in range(1, n + 1))
    return np.asarray(out)


def _weapon_sweeps(ctx, s):
    if hasattr(s, "_sweeps"):
        return s._sweeps
    out = []
    for p, wb, o, a in ph.weapons(ctx):
        riders = [b for b in s.bodies if b.id in s.rotor and b.kind == "weapon" or b.id == wb.id]
        V = np.vstack([b.mesh.vertices for b in riders])
        q = V - o
        t = q @ a
        R = float(ph.perp_radius(V, o, a).max())
        tw = wb.mesh.vertices - o
        tt = tw @ a
        out.append((wb.id, o, a, R, float(tt.min()), float(tt.max())))
    s._sweeps = out
    return out


def m_ground(ctx, s, T, F):
    """WL01/02/06/07, AR01/02, VS04, HS04: from the ground-game facts."""
    gap, S = F.get("gap"), F.get("sectors")
    if gap is not None:
        g = gap[S["front"]]
        g = np.nan_to_num(g, nan=99.0)
        ref = float(np.median(A.REF_WEDGE_LIPS_MM))
        T["wl01.win_front"] = float(np.mean(g <= ref)) if len(g) else None
        T["wl01.ref_mm"] = ref
    for k in ("gap_med.front", "gap_med.left", "gap_med.right", "gap_p20.front", "cog_h", "mass_g", "mu", "driven_share",
              "stall_torque_gcm", "wheel_dia", "motor_rpm", "body_front_y", "body_rear_y", "body_max_x", "body_min_x",
              "wheel_max_x", "wheel_min_x", "wheel_front_y", "half_x", "half_y", "track", "wheel_y", "wheelbase_wheels",
              "fork_open_mm", "family"):
        T[k] = F.get(k)
    com = F.get("com")
    T["com"] = com
    wh = [b for b in s.bodies if b.kind == "wheel"]
    T["wheel_rear_y"] = float(min(b.aabb[0][1] for b in wh)) if wh else None
    if com is not None and T["body_front_y"] is not None and T["body_rear_y"] is not None:
        L = T["body_front_y"] - T["body_rear_y"]
        T["wl02.com_rear_frac"] = float((T["body_front_y"] - com[1]) / L) if L > 1 else None
        dy, dz = float(com[1] - T["body_rear_y"]), float(T["cog_h"] or 0.0)
        a = math.radians(45)
        rise = dy * math.sin(a) + dz * math.cos(a) - dz
        T["wl02.lift_j"] = (T["mass_g"] or 0) * 1e-3 * ph.G0 * rise * 1e-3


def m_rest(ctx, s, T, F):
    """AR03: rest poses on the sides / top from the convex hull and the centre of mass."""
    com = F.get("com")
    if com is None:
        return
    from scipy.spatial import ConvexHull, Delaunay
    selfright = bool(ctx.r.spec.raw.get("self_right") or ctx.r.spec.raw.get("srimech")) or any(
        p.weapon is not None and p.weapon.kind in ("flipper", "lifter", "self_right") for p in ctx.r.spec.parts)
    trapped = []
    for name, d in (("left side", (1, 0, 0)), ("right side", (-1, 0, 0)), ("nose", (0, 1, 0)), ("tail", (0, -1, 0)), ("top", (0, 0, 1))):
        d = np.array(d, float)
        h = s.P @ d
        c = h >= h.max() - 1.0
        a = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0, 0])
        u = np.cross(d, a)
        u /= np.linalg.norm(u)
        v = np.cross(d, u)
        Q = np.c_[s.P[c] @ u, s.P[c] @ v]
        cp = np.array([com @ u, com @ v])
        stable = False
        try:
            if len(Q) >= 3:
                hull = ConvexHull(Q)
                if hull.volume > 1.0:
                    stable = bool(Delaunay(Q[hull.vertices]).find_simplex(cp) >= 0)
        except Exception:  # noqa: BLE001 - degenerate contact patch (line/point): not a rest pose
            stable = False
        wheel = bool(s.is_wheel[c].any())
        if name == "top" and (ctx.r.spec.can_run_inverted or wheel):
            continue
        if stable and not wheel and not selfright:
            trapped.append(name)
    T["ar03.trapped"] = trapped


def m_corners(ctx, s, T):
    """LD01: landing on each corner of the outline."""
    sm = skin(s) & s.face & ~s.is_rotor & ~s.is_wheel & ~s.is_fast
    idx = np.nonzero(sm)[0]
    if not len(idx):
        return
    lo, hi = s.P[idx].min(axis=0), s.P[idx].max(axis=0)
    rows = []
    for cx in (lo[0], hi[0]):
        for cy in (lo[1], hi[1]):
            for cz in (lo[2], hi[2]):
                c = np.array([cx, cy, cz])
                j = idx[np.argmin(np.linalg.norm(s.P[idx] - c, axis=1))]
                b = s.bodies[s.O[j]]
                own = idx[(s.O[idx] == s.O[j]) & (np.linalg.norm(s.P[idx] - s.P[j], axis=1) <= 8.0)][:24]
                t = float(np.median(A.thickness(b, s.P[own], s.N[own], max_mm=10.0, step=0.5)))
                cap = A.energy_capacity_j(_mat(ctx, b), t * 30.0 * 30.0)
                rows.append((cap, b.id, t))
    known = [r for r in rows if r[0] is not None]
    T["ld01.min"] = min(known) if known else None


def _axis_of(b):
    ext = b.aabb[1] - b.aabb[0]
    a = np.zeros(3)
    a[int(np.argmin(ext))] = 1.0
    return a, float(max(ext) / 2)


def m_wheels(ctx, s, T, F):
    """LD02 (wheel shaft at landing), DB01 (wheel debris gap), DB06 (tyre grooves)."""
    wh = [b for b in s.bodies if b.kind == "wheel"]
    if not wh:
        return
    mass = (F.get("mass_g") or ph.robot_mass_g(ctx)) * 1e-3
    worst, db, grooves = None, [], []
    for b in wh:
        a, R = _axis_of(b)
        o = b.center
        t = (b.mesh.vertices - o) @ a
        t0, t1 = float(t.min()), float(t.max())
        p = ph.part(ctx, b)
        ride = {b.id} | {x.id for x in s.bodies if (ph.part(ctx, x) is not None and (ph.part(ctx, x).parent == b.id or ph.part(ctx, x).tyre_of == b.id))}
        # LD02: overhang from the wheel centre to the first support along the axis toward the robot centre.
        sign = 1.0 if (s.centre - o) @ a > 0 else -1.0
        line = o + np.outer(np.arange(0.0, 60.0, 0.5) * sign, a)
        L = None
        for x in s.bodies:
            if x.id in ride or x.kind in A.WHEELISH or x.fastener or x.kind in ("pulley", "shaft", "belt") or "hub" in x.id:
                continue
            hit = x.inside(line)
            if hit.any():
                k = int(np.argmax(hit)) * 0.5
                L = k if L is None else min(L, k)
        shaft = next((x for x in s.bodies if x.kind == "shaft" and not x.fastener and x.inside(o[None])[0]), None)
        d = 2.0 * float(np.percentile(ph.perp_radius(shaft.mesh.vertices, o, a), 99)) if shaft is not None else 3.0
        smat = _mat(ctx, shaft) if shaft is not None else "steel"
        sy = (A.mech(smat) or (350.0,))[0]
        if L is not None:
            Fw = mass * ph.G0 * A.DROP_G / len(wh)
            sig = 32.0 * Fw * max(L, 1.0) / (math.pi * d ** 3)
            sf = sy / sig
            if worst is None or sf < worst[0]:
                worst = (sf, b.id, L, d)
        # DB01: static parts around the swept wheel.
        m = ~np.isin(np.array([x.id for x in s.bodies], dtype=object)[s.O], list(ride)) & ~s.is_wheel & ~s.is_rotor
        m &= ~np.isin(s.kind, ("pulley", "belt", "shaft", "tyre")) & ~s.is_fast
        Q = s.P[m]
        g = A.cyl_gap(Q, o, a, R, t0, t1)
        near = (g > 0.3) & (g < 20.0) & (s.z[m] > 0.5)
        if near.any():
            q = Q[near] - o
            u = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0, 0])
            u /= np.linalg.norm(u)
            v = np.cross(a, u)
            ang = (np.degrees(np.arctan2(q @ v, q @ u)) % 360 // 30).astype(int)
            for sec in np.unique(ang):
                gm = float(g[near][ang == sec].min())
                if A.DEBRIS_WHEEL_MM[0] <= gm < A.DEBRIS_WHEEL_MM[1]:
                    db.append((round(gm, 1), b.id, int(sec) * 30))
        # DB06: grooves on the tread.
        tyre = next((x for x in s.bodies if x.id in ride and x.kind == "tyre"), b)
        P2 = tyre.mesh.vertices
        if len(P2) > 20:
            q = P2 - o
            r = ph.perp_radius(P2, o, a)
            tm = np.abs(q @ a - (t0 + t1) / 2) <= (t1 - t0) / 4
            u = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0, 0])
            u /= np.linalg.norm(u)
            v = np.cross(a, u)
            ang = (np.degrees(np.arctan2(q @ v, q @ u)) % 360 // 5).astype(int)
            mx = [r[tm & (ang == k)].max() for k in np.unique(ang[tm])]
            if len(mx) >= 12 and max(mx) - min(mx) > 1.0:
                grooves.append(tyre.id)
    T["ld02.worst"] = worst
    T["db01.bad"] = sorted(db)
    T["db06.grooved"] = grooves


def m_weapon(ctx, s, T, F):
    """DB02 (weapon debris gap), OW01 (floor strike at 5 deg pitch), OW02, OW04, VS06."""
    sw = _weapon_sweeps(ctx, s)
    T["n_weapons"] = len(sw)
    T["weapon_vertical"] = any(abs(a[2]) < 0.5 for _, _, a, _, _, _ in sw)
    if not sw:
        return
    db = []
    ws = []
    for wid, o, a, R, t0, t1 in sw:
        m = ~s.is_rotor & ~s.is_wheel & ~s.is_fast & ~np.isin(s.kind, ("shaft", "bearing", "pulley", "belt", "weapon_motor"))
        Q = s.P[m]
        g = A.cyl_gap(Q, o, a, R, t0, t1)
        below = (Q[:, 2] < o[2]) & (g > 0.3) & (g < 20.0)
        if below.any():
            q = Q[below] - o
            u = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.9 else np.array([1.0, 0, 0])
            u /= np.linalg.norm(u)
            v = np.cross(a, u)
            ang = (np.degrees(np.arctan2(q @ v, q @ u)) % 360 // 30).astype(int)
            for sec in np.unique(ang):
                gm = float(g[below][ang == sec].min())
                if A.DEBRIS_WEAPON_MM[0] <= gm < A.DEBRIS_WEAPON_MM[1]:
                    db.append((round(gm, 1), wid, int(sec) * 30))
        ws.append((wid, o, a, R, t0, t1))
    T["db02.bad"] = sorted(db)
    # OW01: nose-down pitch about the front wheel contact, limited by whatever touches the floor first.
    wy = F.get("wheel_y")
    if wy:
        yw = float(max(wy))
        ahead = (~s.is_rotor) & (~s.is_wheel) & (s.P[:, 1] > yw + 1.0)
        lim = math.radians(5.0)
        if ahead.any():
            ang = np.arctan2(np.maximum(s.z[ahead], 0.0), s.P[ahead, 1] - yw)
            lim = min(lim, float(ang.min()))
        res = []
        for wid, o, a, R, t0, t1 in ws:
            u = np.cross(a, [1.0, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1.0, 0])
            u /= np.linalg.norm(u)
            v = np.cross(a, u)
            ph_ = np.linspace(0, 2 * math.pi, 181)
            ring = o + R * (np.outer(np.cos(ph_), u) + np.outer(np.sin(ph_), v))
            ring = np.vstack([ring + a * t0, ring + a * t1])
            z = (ring[:, 2] - s.floor) * math.cos(lim) - (ring[:, 1] - yw) * math.sin(lim)
            res.append((float(z.min()), wid, math.degrees(lim)))
        T["ow01.min"] = min(res)
    # OW02: vertical-spinner gyro vs track.
    T["ow02.ratio"] = None
    if F.get("track"):
        vs = [R for _, _, a, R, _, _ in ws if abs(a[2]) < 0.5]
        if vs:
            T["ow02.ratio"] = float(F["track"] / (2 * max(vs)))
    # OW04 / VS06: supports and uprights.
    sup = []
    for p, wb, o, a in ph.weapons(ctx):
        lay = ph.shaft_layout(ctx, wb, o, a)
        sup.append((wb.id, 0 if lay is None else len(lay["sides"])))
    T["ow04.supports"] = sup
    ups = []
    for k, v in ctx.metrics.items():
        if k.startswith("upright_stress_mpa."):
            hid = k.split(".", 1)[1]
            hb = next((b for b in s.bodies if b.id == hid), None)
            mm = A.mech(_mat(ctx, hb)) if hb is not None else None
            if mm and v:
                ups.append((mm[0] / (2.0 * float(v)), hid))
    T["vs06.sf"] = min(ups) if ups else None
    bolts = []
    hosts = [h for _, h in ups]
    for h in hosts:
        n = 0
        for f in ctx.r.spec.fasteners:
            if h in (f.through or []) or f.threads_into == h:
                try:
                    dd = float(str(f.designation).upper().lstrip("M").split("X")[0])
                except ValueError:
                    dd = 0.0
                if dd >= 2.0:
                    n += 1
        bolts.append((n, h))
    T["vs06.bolts"] = min(bolts) if bolts else None


def m_exposure(ctx, s, T):
    """ST01/ST02/ST05, DB03, DB05: what the outer skin is made of and how thick it is."""
    fs = np.zeros(len(s.P), bool)
    for brg in A.FRONT_SIDE:
        fs |= view(s, brg)
    fs &= s.face & ~s.is_rotor & ~s.is_wheel & ~s.is_fast
    sk = skin(s)
    T["db03.visible"] = sorted({s.bodies[i].id for i in np.unique(s.O[sk]) if s.bodies[i].kind in ("belt", "pulley")})
    T["db05.visible"] = sorted({s.bodies[i].id for i in np.unique(s.O[sk]) if s.bodies[i].kind in ("motor", "weapon_motor")})
    brittle, thin, st1 = [], [], []
    F_imp = ph.impact_n(ctx) * 0.25
    for bi in np.unique(s.O[fs | (sk & view(s, 0, 90.0) & s.face & ~s.is_rotor & ~s.is_wheel & ~s.is_fast)]):
        b = s.bodies[bi]
        if b.kind in STATIC_SKIP or b.kind in A.CRITICAL or b.kind in ("connector", "spring", "other") and not ph.printed(ctx, b):
            continue
        mat = _mat(ctx, b)
        m = (s.O == bi) & (fs | (sk & s.face))
        if mat in A.BRITTLE and (s.O[fs] == bi).any():
            brittle.append(b.id)
        js = np.nonzero(m)[0]
        if not len(js):
            continue
        js = js[:: max(len(js) // 60, 1)]
        t = A.thickness(b, s.P[js], s.N[js], max_mm=4.0, step=0.25)
        t10 = float(np.percentile(t, 10))
        pr = ph.printed(ctx, b)
        lim = 2.5 if pr else (0.8 if A.is_metal(mat) else None)
        if lim is not None and t10 < lim:
            thin.append((round(t10, 2), b.id, lim))
        # ST01: layer direction at front/side hit points.
        if pr and mat in A.DUCTILITY and not str(mat).startswith("tpu") and (s.O[fs] == bi).any():
            p = ph.part(ctx, b)
            bd = np.asarray((p._extra.get("print_dir") or p._extra.get("build_dir") or [0, 0, 1]) if p else [0, 0, 1], float)
            bd = bd / (np.linalg.norm(bd) or 1.0)
            jf = np.nonzero((s.O == bi) & fs)[0]
            across = float(np.mean(np.abs(s.N[jf] @ bd) < 0.5))
            k = 0.4 if across >= 0.5 else 1.0
            mm = A.mech(mat)
            if mm:
                tm = float(np.median(t))
                sf = mm[0] * k * 20.0 * tm * tm / 6.0 / (F_imp * 10.0)
                st1.append((round(sf, 2), b.id, k))
    T["st05.brittle"] = sorted(brittle)
    T["st02.thin"] = sorted(thin)
    T["st01.min"] = min(st1) if st1 else None


def m_frame(ctx, s, T):
    """ST03 (sharp concave corners), ST06 (frame section), ST04 (bolt pull-out at dynamic factor 3)."""
    shells = [b for b in s.bodies if b.kind in ("structure", "armor", "plate") and not b.fastener]
    sharp = []
    for b in shells:
        m = b.mesh
        if not len(m.face_adjacency):
            continue
        conc = ~m.face_adjacency_convex & (m.face_adjacency_angles > math.radians(60))
        if conc.any():
            e = m.vertices[m.face_adjacency_edges[conc]]
            L = float(np.linalg.norm(e[:, 0] - e[:, 1], axis=1).sum())
            if L > 5.0:
                sharp.append((round(L), b.id))
    T["st03.sharp"] = sorted(sharp, reverse=True)
    pm = [(float(v) / A.DYN_FACTOR, k.split(".", 1)[1]) for k, v in ctx.metrics.items() if k.startswith("bolt_pullout_margin.")]
    T["st04.min"] = min(pm) if pm else None
    # ST06: section modulus of the main structural body along its length and width.
    st = [b for b in s.bodies if b.kind == "structure" and not b.fastener]
    if not st:
        return
    ch = max(st, key=lambda b: abs(b.mesh.volume))
    mm = A.mech(_mat(ctx, ch))
    if not mm:
        return
    h = 3.0 if ctx.opts.fast else 2.0
    lo, hi = ch.aabb
    ax = [np.arange(lo[i] + h / 2, hi[i], h) for i in range(3)]
    G = np.stack(np.meshgrid(*ax, indexing="ij"), -1).reshape(-1, 3)
    if len(G) > 250000:
        return
    occ = ch.inside(G).reshape(len(ax[0]), len(ax[1]), len(ax[2]))
    F_imp = ph.impact_n(ctx)
    worst = None
    for along, name in ((1, "front-rear"), (0, "side-side")):
        n = occ.shape[along]
        Lm = n * h
        for k in range(n):
            sl = np.take(occ, k, axis=along)
            zz = np.nonzero(sl)
            if not len(zz[0]):
                continue
            z = ax[2][zz[1]]
            zc = z.mean()
            I = float(((z - zc) ** 2).sum() * h * h + len(z) * h ** 4 / 12.0)
            c = float(np.abs(z - zc).max() + h / 2)
            pos = (k + 0.5) * h
            M = F_imp / 2.0 * min(pos, Lm - pos)
            if M <= 0:
                continue
            sf = mm[0] * (I / c) / M
            if worst is None or sf < worst[0]:
                worst = (round(sf, 2), ch.id, name, round(float(ax[along][k]), 1))
    T["st06.min"] = worst


def m_retention(ctx, s, T):
    """LD03 (heavy parts held in all 6 directions), OW05 (battery after inversion), GD09 (ESC on foam)."""
    spec = ctx.r.spec
    held_by = {}
    for f in spec.fasteners:
        for pid in list(f.through or []) + [f.threads_into]:
            if pid:
                held_by[pid] = True
    for c in spec.connections:
        if any(k in str(c.method).lower() for k in ("screw", "bolt", "strap", "zip", "glue", "clip", "press", "tape", "velcro", "snap", "heat")):
            held_by[c.a] = held_by[c.b] = True
    heavy = []
    for b in s.bodies:
        if b.fastener or b.id in s.rotor or b.kind in A.WHEELISH or b.kind in ("structure", "armor", "plate", "insert", "nut", "belt"):
            continue
        g = ph.mass_g(ctx, b)
        if b.kind in A.CRITICAL or (g is not None and g >= HEAVY_MIN_G):
            heavy.append(b)
    loose = []
    bat_up = None
    others = [x for x in s.bodies if not x.is_wire]
    for b in heavy:
        if held_by.get(b.id):
            if b.kind == "battery":
                bat_up = True
            continue
        p, n = b.surface(2.0)
        free = []
        for name, d in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)), ("-y", (0, -1, 0)), ("+z", (0, 0, 1)), ("-z", (0, 0, -1))):
            d = np.array(d, float)
            sel = (n @ d) > 0.5
            Q = (p[sel] + d * 1.5)[:: max(int(sel.sum()) // 150, 1)]
            blocked = False
            if len(Q):
                for x in others:
                    if x.id == b.id:
                        continue
                    lo, hi = x.aabb
                    if np.any(np.all((Q >= lo) & (Q <= hi), axis=1)) and x.inside(Q).any():
                        blocked = True
                        break
            if not blocked:
                free.append(name)
        if free:
            loose.append((b.id, free))
        if b.kind == "battery":
            bat_up = "+z" not in free
    T["ld03.loose"] = loose
    T["ow05.battery_held"] = bat_up
    # GD09
    esc = [b for b in s.bodies if b.kind == "esc"]
    foam = any(("foam" in (p.material or "") or "foam" in p.id or "tape" in p.id) for p in spec.parts) or any(
        any(k in str(c.method).lower() for k in ("foam", "tape", "velcro")) for c in spec.connections)
    hard = []
    for e in esc:
        p, _ = e.surface(2.0)
        p = p[:: max(len(p) // 200, 1)]
        for x in s.bodies:
            if x.id == e.id or x.kind not in ("structure", "plate", "armor") or ph.material_of(ctx, x) in ("tpu", "tpu_95a", "tpu_85a"):
                continue
            lo, hi = x.aabb
            near = np.all((p >= lo - 0.5) & (p <= hi + 0.5), axis=1)
            if near.any() and float(x.distance(p[near]).min()) <= 0.3:
                hard.append(e.id)
                break
    T["gd09.hard"] = [] if foam else hard


def m_guts(ctx, s, T):
    """GD01 (chunk removal), GD03 (battery depth), GD04 (receiver), GD05 (drive per side), GD06 (switch)."""
    from scipy.spatial import cKDTree
    spec = ctx.r.spec
    sk = skin(s) & ~s.is_rotor
    ids = {p.id for p in spec.parts}

    def depth(b):
        own = s.O == s.bodies.index(b)
        if (sk & own).any():
            return 0.0
        tree = cKDTree(s.P[sk & ~own & ~s.is_wheel])
        p, _ = b.surface(2.0)
        return float(tree.query(p)[0].min())
    bat = [b for b in s.bodies if b.kind == "battery"]
    T["gd03.depth"] = min(((depth(b), b.id) for b in bat), default=None)
    rx = _receivers(s.bodies)
    T["gd04.depth"] = min(((depth(b), b.id) for b in rx), default=None)
    caged = []
    for b in rx:
        c = b.center
        enc = [x for x in s.bodies if x.id != b.id and x.kind in ("structure", "armor", "plate") and np.all(x.aabb[0] <= c) and np.all(c <= x.aabb[1])]
        if enc and all(A.is_metal(_mat(ctx, x)) for x in enc):
            caged.append(b.id)
    T["gd04.caged"] = caged
    mot = [b for b in s.bodies if b.kind == "motor"]
    T["gd05.per_side"] = (sum(1 for b in mot if b.center[0] > s.centre[0]), sum(1 for b in mot if b.center[0] <= s.centre[0])) if mot else None
    # GD06: switch.
    sw = [b for b in s.bodies if b.kind == "switch"]
    if sw and T.get("body_front_y") is not None and T.get("body_rear_y") is not None:
        b = sw[0]
        own = s.O == s.bodies.index(b)
        L = T["body_front_y"] - T["body_rear_y"]
        front = b.center[1] > T["body_front_y"] - 0.3 * L
        rec = None
        for name, d in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)), ("-y", (0, -1, 0)), ("+z", (0, 0, 1))):
            d = np.array(d, float)
            brg = math.degrees(math.atan2(d[1], d[0])) if d[2] == 0 else 0
            vm = view(s, brg, 90.0 if d[2] else 0.0)
            if not (vm & own).any():
                continue
            js = np.nonzero(vm & own)[0]
            ext = float((s.P[js] @ d).max())
            j0 = js[np.argmax(s.P[js] @ d)]
            perp = s.P - s.P[j0]
            perp = perp - np.outer(perp @ d, d)
            nb = (np.linalg.norm(perp, axis=1) <= 10.0) & ~own & sk
            r_ = float((s.P[nb] @ d).max() - ext) if nb.any() else 0.0
            rec = r_ if rec is None else min(rec, r_)
        T["gd06"] = (b.id, rec, bool(front))
    # GD01: chunk removal at front/side hit points.
    elec = [b for b in s.bodies if b.kind in A.CRITICAL or b.kind in ("esc", "receiver")]
    if not elec or not bat:
        return
    hits = np.zeros(len(s.P), bool)
    for brg in range(0, 181, 15):
        hits |= view(s, brg)
    hits &= (s.z >= 2) & (s.z <= 40) & s.face & ~s.is_rotor
    hp = np.nonzero(hits)[0]
    if not len(hp):
        return
    hp = hp[:: max(len(hp) // 80, 1)]
    centres = s.P[hp] - s.N[hp] * 4.0
    surf = {b.id: b.surface(2.0)[0] for b in elec}
    routes = {rt.id: _densify(np.asarray(rt.points, float), 2.0) for rt in (ctx.routes or []) if len(rt.points) >= 2}
    edges = []
    for w in spec.wires:
        a_, b_ = A.part_of(getattr(w, "from"), ids), A.part_of(w.to, ids)
        if a_ and b_:
            edges.append((w.id, a_, b_))
    kinds = {b.id: b.kind for b in s.bodies}
    motors = [b.id for b in elec if b.kind == "motor"]
    rx_ids = [b.id for b in rx]
    alive_n = 0
    for c in centres:
        dead = {bid for bid, P in surf.items() if (np.linalg.norm(P - c, axis=1) <= 12.0).any()}
        cut = {wid for wid, Q in routes.items() if (np.linalg.norm(Q - c, axis=1) <= 12.0).any()}
        if any(b.id in dead for b in bat):
            continue
        if edges:
            adj = {}
            for wid, a_, b_ in edges:
                if wid in cut or a_ in dead or b_ in dead:
                    continue
                adj.setdefault(a_, set()).add(b_)
                adj.setdefault(b_, set()).add(a_)
            seen, todo = set(), [b.id for b in bat]
            while todo:
                x = todo.pop()
                if x in seen:
                    continue
                seen.add(x)
                todo.extend(adj.get(x, ()))
            drive = any(m in seen for m in motors)
            radio = (not rx_ids) or any(r_ in seen for r_ in rx_ids)
        else:
            drive = any(m not in dead for m in motors)
            radio = (not rx_ids) or any(r_ not in dead for r_ in rx_ids)
        if drive and radio:
            alive_n += 1
    T["gd01.alive_frac"] = alive_n / len(centres)
    T["gd01.n_hits"] = len(centres)
    _ = kinds


def m_lips(ctx, s, T, F):
    """VS02/VS03, HS05, AS01-AS08, WL06 inputs: the front lips and forks."""
    lips = []
    w = ctx.world
    floor = s.floor
    metal_bodies = [b for b in s.bodies if A.is_metal(_mat(ctx, b)) and not b.fastener and b.id not in s.rotor]
    for d in F.get("skirts") or []:
        b = w.body(d["id"])
        if b is None:
            continue
        mat = d["material"]
        sp, sn = b.surface(0.5)
        ymax = d["ymax"]
        x = dict(d)
        x["metal"] = A.is_metal(mat)
        x["printed"] = ph.printed(ctx, b)
        x["U_j"] = A.energy_capacity_j(mat, abs(float(b.mesh.volume))) if mat else None
        lo, hi = b.aabb
        x["backed"] = any(np.all(mb.aabb[0] <= hi + 1.0) and np.all(lo - 1.0 <= mb.aabb[1]) for mb in metal_bodies if mb.id != b.id)
        tip = sp[:, 1] >= ymax - 3.0
        under = tip & (sn[:, 2] < -0.2)
        x["alpha_deg"] = float(np.degrees(np.median(np.arctan2(np.maximum(sn[under, 1], 0.0), -sn[under, 2])))) if under.any() else 90.0
        tt = cg._slice_thickness(sp, ymax - 0.3, None)
        x["tip_r"] = (tt / 2.0) if tt is not None else 0.0
        ch = tip & (sn[:, 1] > 0.2) & (sn[:, 2] < -0.2)
        x["chamfer_mm"] = float(np.ptp(sp[ch, 2])) if ch.sum() >= 2 else 0.0
        # Tip width at the floor (z within 2 mm of the lip bottom).
        low = tip & (sp[:, 2] <= float(sp[:, 2].min()) + 2.0)
        x["tip_w"] = float(np.ptp(sp[low, 0])) if low.sum() >= 2 else d["width"]
        # Side skirt bottom-edge chamfer (outward-down faces between 30 and 75 deg from horizontal).
        bot = sp[:, 2] <= float(sp[:, 2].min()) + 2.0
        lat = np.abs(sn[:, 0])
        cham = bot & (lat > 0.26) & (sn[:, 2] < -0.26)
        x["side_chamfer"] = bool(cham.any())
        p = ph.part(ctx, b)
        x["replaceable"] = bool(p is not None and (p._extra.get("replaceable") or any(
            b.id in (f.through or []) and f.removable for f in ctx.r.spec.fasteners)))
        x["preload_n"] = float((p._extra.get("preload_n") or 0.0)) if p is not None else 0.0
        x["gap_floor"] = float(lo[2] - floor)
        lips.append(x)
    T["lips"] = lips
    T["front_lips"] = [x for x in lips if x["front"]]
    T["side_lips"] = [x for x in lips if not x["front"]]
    T["forks"] = [x for x in T["front_lips"] if x["kind"] == "fork" or any(k in x["id"] for k in ("fork", "tine", "blade", "wedglet", "wedgelet"))]


def m_pockets(ctx, s, T):
    """WL03: concave pockets in the side outline (per 4 mm Y column, x(z)) and the top outline (per 4 mm X column, z(y))."""
    m = ~s.is_fast
    P = s.P[m]
    best = (0.0, "side")
    def concav(col, along, val, sign):
        nonlocal best
        for c in np.unique(col):
            sel = col == c
            a = np.floor(along[sel] / s.cell).astype(int)
            v = val[sel] * sign
            if len(np.unique(a)) < 3:
                continue
            ks = np.arange(a.min(), a.max() + 1)
            prof = np.full(len(ks), np.nan)
            np.fmax.at(prof, a - a.min(), v)
            ok_ = ~np.isnan(prof)
            prof = np.interp(np.arange(len(prof)), np.nonzero(ok_)[0], prof[ok_])  # sampling holes are not pockets
            up = np.maximum.accumulate(prof)
            dn = np.maximum.accumulate(prof[::-1])[::-1]
            dep = np.minimum(up, dn) - prof
            k = float(dep.max())
            if k > best[0]:
                best = (k, name)
    yc = np.floor(P[:, 1] / 4.0).astype(int)
    for name, sign in (("left side", 1.0), ("right side", -1.0)):
        concav(yc, P[:, 2], P[:, 0], sign)
    name = "top"
    xc = np.floor(P[:, 0] / 4.0).astype(int)
    concav(xc, P[:, 1], P[:, 2], 1.0)
    T["wl03.pocket"] = best


def m_pulleys(ctx, s, T):
    """OW03: pulleys that carry a belt have flanges or a groove (rim proud at both axial ends)."""
    belts = [b for b in s.bodies if b.kind == "belt"]
    if not belts:
        return
    bad = []
    for b in s.bodies:
        if b.kind != "pulley":
            continue
        if not any(np.all(b.aabb[0] <= x.aabb[1] + 0.5) and np.all(x.aabb[0] <= b.aabb[1] + 0.5) for x in belts):
            continue
        a, _ = _axis_of(b)
        o = b.center
        V = b.mesh.vertices
        t = (V - o) @ a
        r = ph.perp_radius(V, o, a)
        k = np.clip(((t - t.min()) / max(np.ptp(t), 1e-6) * 5).astype(int), 0, 4)
        mx = [float(r[k == i].max()) if (k == i).any() else 0.0 for i in range(5)]
        if not (mx[0] > max(mx[1:4]) - 0.0 + 0.4 and mx[4] > max(mx[1:4]) + 0.4):
            bad.append(b.id)
    T["ow03.unflanged"] = bad


BLOCKS = (
    ("bite", lambda c, s, T, F: m_bite(c, s, T)),
    ("top", lambda c, s, T, F: m_top(c, s, T)),
    ("ground", m_ground),
    ("routes", lambda c, s, T, F: m_routes(c, s, T)),
    ("rest", m_rest),
    ("corners", lambda c, s, T, F: m_corners(c, s, T)),
    ("wheels", m_wheels),
    ("weapon", m_weapon),
    ("exposure", lambda c, s, T, F: m_exposure(c, s, T)),
    ("frame", lambda c, s, T, F: m_frame(c, s, T)),
    ("retention", lambda c, s, T, F: m_retention(c, s, T)),
    ("guts", lambda c, s, T, F: m_guts(c, s, T)),
    ("lips", m_lips),
    ("pockets", lambda c, s, T, F: m_pockets(c, s, T)),
    ("pulleys", lambda c, s, T, F: m_pulleys(c, s, T)),
)


def facts(ctx):
    T = {"_errors": {}, "_timings": {}}
    import time
    F = cg.facts(ctx)
    T["cg"] = F
    if "floor" not in F:
        return T
    T["family"] = F.get("family")
    s = _sample(ctx, 2.0 if ctx.opts.fast else 1.0)
    T["self_right"] = bool(ctx.r.spec.can_run_inverted or ctx.r.spec.raw.get("self_right") or ctx.r.spec.raw.get("srimech")) or any(
        p.weapon is not None and p.weapon.kind in ("flipper", "lifter", "self_right") for p in ctx.r.spec.parts)
    for name, fn in BLOCKS:
        t0 = time.time()
        try:
            fn(ctx, s, T, F)
        except Exception as e:  # noqa: BLE001 - one bad measurement must not hide the others
            T["_errors"][name] = f"{type(e).__name__}: {e}"
        T["_timings"][name] = round(time.time() - t0, 2)
    return T
