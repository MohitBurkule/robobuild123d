"""Collisions: static overlaps, joint sweeps, spinning-weapon sweeps, and "what holds this part" (port of interference.rs)."""

from __future__ import annotations

import math

import numpy as np
from scipy import ndimage

from .. import catalog, geom, measure
from .. import world as world_mod
from ..finding import BLOCKER, WARNING, fail, note, ok
from .power import spin_axis  # one shared helper (also used by spinner)

G = "interference"
INF = math.inf


def allowed_depth(r, a, b) -> float:
    """Maximum overlap depth allowed between two bodies, from the spec and from how parts are meant to fit together."""
    allow = r.profile.contact_tol_mm
    for ao in r.spec.allow_overlap:
        if (ao.a == a.id and ao.b == b.id) or (ao.a == b.id and ao.b == a.id):
            allow = max(allow, ao.max_depth_mm if ao.max_depth_mm is not None else 0.5)

    def part(x):
        return r.parts[x.part_idx].part if x.part_idx is not None and x.part_idx < len(r.parts) else None

    pa, pb = part(a), part(b)
    if pa is not None and pb is not None:
        if pa.fused_with == pb.id or pb.fused_with == pa.id:
            return INF
        if pa.tyre_of == pb.id or pb.tyre_of == pa.id:
            allow = max(allow, 1.0)
        for x, y in ((pa, pb), (pb, pa)):
            if x.belt is not None and y.id in (x.belt.pulleys or []):
                allow = max(allow, 0.8)
            if x.weapon is not None and (x.weapon.motor == y.id or x.weapon.locking_bar == y.id):
                allow = max(allow, 1.0e3)
    for x, y in ((a, b), (b, a)):
        if x.fastener:
            f = next((f for f in r.spec.fasteners if f.id == x.id), None)
            if f is not None and f.threads_into == y.id:
                return INF
    return allow


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    bad = checked = 0
    n = len(w.bodies)
    for i in range(n):
        a = w.bodies[i]
        for j in range(i + 1, n):
            b = w.bodies[j]
            if not measure.aabb_overlap(a.aabb, b.aabb):
                continue
            allow = allowed_depth(r, a, b)
            if math.isinf(allow):
                continue
            checked += 1
            o = measure.overlap(a, b, cap=allow)
            if o is not None and o.depth > allow:
                bad += 1
                out.append(fail("interference.overlap", G, BLOCKER, "Parts collide",
                                f"`{a.id}` and `{b.id}` overlap by {o.depth:.2f} mm (about {o.volume:.1f} mm3).")
                           .on(a.id, b.id).here(o.at)
                           .expect(f"overlap <= {allow:.2f} mm (touching is fine)", f"{o.depth:.2f} mm")
                           .fix("Move or resize one of them, cut a pocket in the housing, or list a deliberate press fit in `allow_overlap`."))
    if bad == 0:
        out.append(ok("interference.overlap", G, "No parts collide",
                      f"{checked} touching or overlapping pairs checked; touching is allowed, overlap deeper than "
                      f"{r.profile.contact_tol_mm:.2f} mm is not."))
    if ctx.opts.deep:
        out.extend(joint_sweeps(ctx))
        out.extend(spin_sweeps(ctx))
    else:
        ctx.not_checked.append("Joint range sweeps and spinning-weapon sweep (fast mode skipped them)")
    out.extend(wheel_clearance(ctx))
    out.extend(captive(ctx))
    return out


WHEEL_CLEARANCE_MM = 1.0  # running clearance between a wheel or tyre and anything that does not turn with it
HUB_METHODS = {"press_fit", "shaft", "pin", "screw", "glue", "interlock", "snap", "tape", "velcro"}


def wheel_axis(r, w, i):
    """(origin, unit axis) a wheel turns about: its revolute joint, else its catalog axle, else its thinnest local axis."""
    b = w.bodies[i]
    rp = r.parts[b.part_idx]
    j = rp.part.joint
    if j is not None and j.kind == "revolute":
        pb = w.body(rp.part.parent) if rp.part.parent else None
        PM = pb.M if pb is not None else np.eye(4)
        ax = PM[:3, :3] @ np.asarray(j.axis, float)
        if np.linalg.norm(ax) > 1e-9:
            return (PM @ np.append(np.asarray(j.pivot, float), 1.0))[:3], ax / np.linalg.norm(ax)
    if rp.cat is not None and rp.cat.shaft is not None:
        sh = rp.cat.shaft
        ax = b.M[:3, :3] @ np.asarray(sh.get("dir", [1, 0, 0]), float)
        return (b.M @ np.append(np.asarray(sh.get("at", [0, 0, 0]), float), 1.0))[:3], ax / np.linalg.norm(ax)
    lo, hi = b.geom.bounds
    k = int(np.argmin(hi - lo))
    ax = b.M[:3, :3] @ np.eye(3)[k]
    return (b.M @ np.append((lo + hi) / 2, 1.0))[:3], ax / np.linalg.norm(ax)


def wheel_clearance(ctx):
    """Running clearance of wheels and tyres: the wheel revolved about its axle must keep WHEEL_CLEARANCE_MM from every
    part that does not turn with it (pocket walls, wedge, armour). Distances are measured in the (radius, axial) plane, so
    a surface of revolution is handled exactly up to the 0.5 mm surface sampling."""
    from scipy.spatial import cKDTree

    r, w = ctx.r, ctx.world
    out = []
    clr = WHEEL_CLEARANCE_MM
    turning = {}
    for i, b in enumerate(w.bodies):
        if b.part_idx is None:
            continue
        p = r.parts[b.part_idx].part
        if p.kind == "wheel" or p.tyre_of:
            turning[b.id] = i
    if not turning:
        return out
    hub = {}
    for c in r.spec.connections:
        if c.method in HUB_METHODS:
            hub.setdefault(c.a, set()).add(c.b)
            hub.setdefault(c.b, set()).add(c.a)
    for f in r.spec.fasteners:
        ids = set(f.through or []) | ({f.threads_into} if f.threads_into else set())
        for x in ids:
            hub.setdefault(x, set()).update(ids - {x})
    bad = 0
    for wid, i in sorted(turning.items()):
        b = w.bodies[i]
        p = r.parts[b.part_idx].part
        origin, axis = wheel_axis(r, w, i)
        skip = set(hub.get(wid, ())) | descendants(r, wid) | set(turning)
        if p.tyre_of:
            skip.add(p.tyre_of)
        skip |= {q.id for q in r.spec.parts if q.tyre_of == wid}

        def ra(P):
            q = np.atleast_2d(P) - origin
            a = q @ axis
            return np.linalg.norm(q - np.outer(a, axis), axis=1), a

        pts, _ = b.surface(0.5)
        wr, wa = ra(pts)
        tree = cKDTree(np.c_[wr, wa])
        rmax, amin, amax = float(wr.max()), float(wa.min()), float(wa.max())
        nb = max(int(math.ceil((amax - amin) / 0.5)), 1)
        rbin = np.zeros(nb)
        np.maximum.at(rbin, np.clip(((wa - amin) / 0.5).astype(int), 0, nb - 1), wr)
        worst = {}
        for o in w.bodies:
            if o is b or o.is_wire or o.fastener or o.id in skip:
                continue
            ad = allowed_depth(r, b, o)
            if math.isinf(ad) or ad >= 1.0e3:
                continue
            cr, ca = ra(_corners(o.aabb))
            if ca.max() < amin - clr or ca.min() > amax + clr:
                continue
            if not measure.aabb_overlap(b.aabb, o.aabb, rmax + clr):
                continue
            P, _ = o.surface(0.5)
            pr, pa = ra(P)
            m = (pr <= rmax + clr) & (pa >= amin - clr) & (pa <= amax + clr)
            if not m.any():
                continue
            P, pr, pa = P[m], pr[m], pa[m]
            d, _ = tree.query(np.c_[pr, pa])
            inside = (pa >= amin) & (pa <= amax) & (pr < rbin[np.clip(((pa - amin) / 0.5).astype(int), 0, nb - 1)])
            d = np.where(inside, 0.0, d)
            k = int(np.argmin(d))
            if d[k] < clr:
                worst[o.id] = (float(d[k]), P[k])
        for oid, (g, at) in sorted(worst.items()):
            bad += 1
            out.append(fail("interference.wheel_clearance", G, WARNING, "Wheel has no running clearance",
                            f"`{wid}` turning about its axle comes within {g:.2f} mm of `{oid}`; it needs {clr:.1f} mm so tyre "
                            f"squash, flex and debris do not make it rub.")
                       .on(wid, oid).here(at).expect(f">= {clr:.1f} mm", f"{g:.2f} mm")
                       .fix("Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces)."))
    if bad == 0:
        out.append(ok("interference.wheel_clearance", G, "Wheels run clear",
                      f"{len(turning)} wheels and tyres keep at least {clr:.1f} mm from every part that does not turn with them."))
    return out


def descendants(r, root):
    s = {root}
    while True:
        before = len(s)
        for p in r.spec.parts:
            if p.parent and p.parent in s:
                s.add(p.id)
        if len(s) == before:
            return s


def joint_sweeps(ctx):
    r, w0 = ctx.r, ctx.world
    out, anyj = [], False
    for rp in r.parts:
        j = rp.part.joint
        if j is None:
            continue
        anyj = True
        moved = descendants(r, rp.part.id)
        lo, hi = min(j.min, j.max), max(j.min, j.max)
        step = 0.8 if j.kind == "prismatic" else 3.0
        n = int(min(max(math.ceil((hi - lo) / step), 1), 80))
        worst = {}
        for k in range(n + 1):
            v = lo + (hi - lo) * k / n
            w = world_mod.World.build(r, {rp.part.id: v})
            # Bodies that do not move are identical to the start world; reuse them (cached meshes / manifolds).
            for idx, b in enumerate(w.bodies):
                if b.id not in moved and idx < len(w0.bodies) and w0.bodies[idx].id == b.id:
                    w.bodies[idx] = w0.bodies[idx]
            for a in w.bodies:
                if a.id not in moved:
                    continue
                for b in w.bodies:
                    if b.id in moved or not measure.aabb_overlap(a.aabb, b.aabb):
                        continue
                    allow = allowed_depth(r, a, b)
                    if math.isinf(allow):
                        continue
                    o = measure.overlap(a, b, cap=allow)
                    if o is not None and o.depth > allow:
                        key = (a.id, b.id)
                        if key not in worst or o.depth > worst[key][0]:
                            worst[key] = (o.depth, v, o.at)
        unit = "mm" if j.kind == "prismatic" else "deg"
        for (a, b), (depth, v, at) in sorted(worst.items()):
            out.append(fail("interference.sweep", G, BLOCKER, "Moving part hits another part",
                            f"`{a}` moving on joint `{rp.part.id}` runs into `{b}` (depth {depth:.2f} mm) at {v:.1f} {unit}.")
                       .on(a, b).here(at)
                       .expect(f"no contact anywhere in {lo:.0f}..{hi:.0f} {unit}", f"contact at {v:.1f} {unit}")
                       .fix("Limit the joint range (`min`/`max`), move the pivot, or cut clearance into the part it hits."))
        if not worst:
            out.append(ok("interference.sweep", G, "Joint sweep is clear",
                          f"`{rp.part.id}` swept {lo:.0f}..{hi:.0f} {unit} in {n} steps without hitting anything."))
    if not anyj:
        out.append(note("interference.sweep", G, "No joints to sweep", "No part has a joint."))
    return out


def _corners(bb):
    lo, hi = bb
    return np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])


class Revolved:
    """Occupancy of a part revolved about an axis, on a grid of (radius, axial position)."""

    def __init__(self, origin, axis, cell, nr, na, amin, occ):
        self.origin, self.axis, self.cell, self.nr, self.na, self.amin, self.occ = origin, axis, cell, nr, na, amin, occ

    def _ra(self, P):
        q = np.atleast_2d(P) - self.origin
        a = q @ self.axis
        r = np.linalg.norm(q - np.outer(a, self.axis), axis=1)
        return r, a

    @staticmethod
    def build(body, origin, axis, cell):
        q = _corners(body.aabb) - origin
        a = q @ axis
        rmax = float(np.linalg.norm(q - np.outer(a, axis), axis=1).max())
        amin, amax = float(a.min()), float(a.max())
        nr = int(math.ceil(rmax / cell)) + 2
        na = int(math.ceil((amax - amin) / cell)) + 2
        if nr * na > 4_000_000:
            return None
        lo, hi = body.aabb[0] - 0.2, body.aabb[1] + 0.2
        if np.prod(np.ceil((hi - lo) / cell)) > 40_000_000:
            return None
        occ3, glo, h = geom.voxelize(body.mesh, cell, lo, hi)
        rv = Revolved(origin, axis, cell, nr, na, amin, np.zeros((na, nr), bool))
        idx = np.argwhere(occ3)
        if len(idx):
            P = glo + (idx + 0.5) * h
            r, aa = rv._ra(P)
            ir = (r / cell).astype(np.int64)
            ia = np.floor((aa - amin) / cell).astype(np.int64)
            m = (ir >= 0) & (ia >= 0) & (ir < nr) & (ia < na)
            rv.occ[ia[m], ir[m]] = True
        return rv

    def near(self, P, pad: int):
        """Occupied within `pad` cells, for each point."""
        occ = self.occ if pad <= 0 else ndimage.binary_dilation(self.occ, np.ones((2 * pad + 1, 2 * pad + 1), bool))
        r, a = self._ra(P)
        ir = (r / self.cell).astype(np.int64)
        ia = np.floor((a - self.amin) / self.cell).astype(np.int64)
        m = (ir >= 0) & (ia >= 0) & (ir < self.nr) & (ia < self.na)
        out = np.zeros(len(ir), bool)
        out[m] = occ[ia[m], ir[m]]
        return out


def spin_sweeps(ctx):
    r, w = ctx.r, ctx.world
    out = []
    pad_close = max(int(math.ceil(r.profile.min_clearance_moving_mm / 0.5)), 1)
    for i, b in enumerate(w.bodies):
        if b.part_idx is None:
            continue
        wd = r.parts[b.part_idx].part.weapon
        if wd is None or wd.kind not in ("spinner", "drum", "disc", "bar"):
            continue
        sa = spin_axis(w, r, i)
        if sa is None:
            continue
        origin, axis = sa
        rev = Revolved.build(b, origin, axis, 0.5)
        if rev is None:
            out.append(fail("interference.spin", G, WARNING, "Weapon sweep not checked", "The weapon is too large to rasterise.").on(b.id))
            ctx.not_checked.append(f"Spinning sweep of `{b.id}`: weapon too large to rasterise")
            continue
        rmax = rev.nr * rev.cell
        reach = rmax + 1.0
        hits = {}
        for j, o in enumerate(w.bodies):
            if j == i or o.is_wire:
                continue
            ad = allowed_depth(r, b, o)
            if math.isinf(ad) or ad >= 1.0e3:
                continue
            q = _corners(o.aabb) - origin
            rad = np.linalg.norm(q - np.outer(q @ axis, axis), axis=1)
            size = float(np.linalg.norm(o.aabb[1] - o.aabb[0]))
            if not np.any(rad < reach + size):
                continue
            occ, glo, h = geom.voxelize(o.mesh, 0.5, o.aabb[0], o.aabb[1])
            idx = np.argwhere(occ)
            if not len(idx):
                continue
            P = glo + (idx + 0.5) * h
            pr, _ = rev._ra(P)
            P = P[pr <= reach]
            if not len(P):
                continue
            hit = rev.near(P, 0)
            close = ~hit & rev.near(P, pad_close)
            if hit.any():
                hits[o.id] = (True, P[np.argmax(hit)])
            elif close.any():
                hits[o.id] = (False, P[np.argmax(close)])
        for oid, (hit, at) in sorted(hits.items()):
            if hit:
                out.append(fail("interference.spin", G, BLOCKER, "Spinning weapon hits the robot",
                                f"`{b.id}` spinning sweeps through `{oid}`.").on(b.id, oid).here(at)
                           .fix("Move the part out of the swept disc, shrink the weapon, or add an explicit gap of at least 1 mm."))
            else:
                out.append(fail("interference.spin_clearance", G, WARNING, "Spinning weapon has almost no clearance",
                                f"`{oid}` is within {r.profile.min_clearance_moving_mm:.1f} mm of the sweep of `{b.id}`; bearings, flex and hits will make them touch.")
                           .on(b.id, oid).here(at)
                           .fix("Leave at least 1 mm between a spinning weapon and anything fixed."))
        if not hits:
            out.append(ok("interference.spin", G, "Weapon sweep is clear", f"`{b.id}` swept a full turn without touching another part."))
    return out


CAPTIVE_MAX_PLAY_MM = 0.5  # a part is captive only if it cannot move more than this in any of the 6 axis directions
SKIP_KINDS = {"structure", "wedge", "armor", "plate", "fork"}
MUST = {"battery", "motor", "weapon_motor", "servo"}
SHOULD = {"esc", "receiver", "switch", "insert", "nut", "bearing", "shaft", "pin"}
DIRS = [("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)), ("-y", (0, -1, 0)), ("+z", (0, 0, 1)), ("-z", (0, 0, -1))]


def captive(ctx):
    r, w = ctx.r, ctx.world
    out = []
    slop = min(r.profile.capture_slop_mm, CAPTIVE_MAX_PLAY_MM)
    checked = loose_ok = 0
    cmap = {}
    for i, b in enumerate(w.bodies):
        if b.part_idx is None:
            continue
        p = r.parts[b.part_idx].part
        if p.kind in SKIP_KINDS:
            continue
        grown = np.array([b.aabb[0] - slop, b.aabb[1] + slop])
        near = []
        for j, o in enumerate(w.bodies):
            if j == i or o.is_wire or not measure.aabb_overlap(o.aabb, grown):
                continue
            ad = allowed_depth(r, b, o)
            if ad >= 1.0e3:
                continue
            near.append((o, ad))
        free, blockers = [], []
        for name, d in DIRS:
            blocked = False
            shift = np.asarray(d, float) * slop
            for o, ad in near:
                if measure.overlap_exceeds(b, o, ad + 0.02, shift):
                    blocked = True
                    if not o.fastener and o.id not in blockers:
                        blockers.append(o.id)
            if not blocked:
                free.append(name)
        if not free:
            cmap[p.id] = blockers
        must, should = p.kind in MUST, p.kind in SHOULD
        if not (must or should) or p.fused_with is not None:
            continue
        if any(f.threads_into == p.id or p.id in (f.through or []) for f in r.spec.fasteners):
            continue
        checked += 1
        if p.kind == "battery" and p.retained is None:
            out.append(fail("retention.battery_undeclared", G, BLOCKER, "Battery retention is not declared",
                            f"`{p.id}` has no screw through it and no `retained`; the battery is the heaviest loose part and "
                            f"must say how it is held (`retained: pocket` if the pocket alone holds it, which is then measured).")
                       .on(p.id).here(b.aabb.mean(axis=0))
                       .fix("Set `retained` (pocket, velcro, strap, press_fit, tape) or screw a retaining plate over it."))
            continue
        if p.retained is not None and p.retained != "pocket":  # `pocket` claims captive: the geometry must prove it
            loose_ok += 1
            out.append(note("retention.declared", G, "Held by declared method", f"`{p.id}` is held by {p.retained}.").on(p.id))
            continue
        if not free:
            continue
        out.append(fail("retention.loose", G, BLOCKER if must else WARNING, "Nothing holds this part in place",
                        f"`{p.id}` can move more than {slop:.1f} mm toward {', '.join(free)} without touching anything (captive means at most "
                        f"{CAPTIVE_MAX_PLAY_MM:.1f} mm of play in every direction); in a hit it will fall out or rattle.")
                   .on(p.id).here(b.aabb.mean(axis=0))
                   .fix("Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit)."))
    ctx.captive = cmap
    if checked > 0 and all(f.passed or f.id == "retention.declared" for f in out):
        out.append(ok("retention.captive", G, "Every loose part is held",
                      f"{checked} parts checked, {loose_ok} held by a declared method, the rest captive in their pockets."))
    return out


def is_printed_part(r, pid) -> bool:
    p = r.spec.part(pid)
    return p is not None and catalog.part_is_printed(p.process, p.material)
