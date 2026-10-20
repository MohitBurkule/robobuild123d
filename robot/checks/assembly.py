"""Assembly by disassembly: take the robot apart one part at a time, each sliding straight out along a clear path.
If every part can leave, the reverse order assembles it without anything passing through anything else (port of assembly.rs)."""

from __future__ import annotations

import math

import numpy as np

from .. import measure
from ..finding import BLOCKER, AssemblyStep, fail, ok
from .interference import _corners, allowed_depth

G = "assembly"
STEP = 0.7
MAX_TRAVEL = 140.0
AXES = [np.array(v, float) for v in ((0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0))]


def group(ctx, pid, present=None):
    """Members that move with part `pid` (tyres on their wheel, children on a joint)."""
    ids = [pid]
    while True:
        n = len(ids)
        for p in ctx.r.spec.parts:
            if (p.tyre_of in ids or p.parent in ids) and p.id not in ids:
                ids.append(p.id)
        if len(ids) == n:
            break
    # A screw whose every clamped part (through + threads_into) is in the group was driven on the bench: it leaves with
    # the sub-assembly instead of pinning it in place (drisk bolts, weapon-module standoff screws). Parts that have
    # already been taken off (`present` False) no longer hold it: a screw backed out of a standoff that has gone stays
    # captive in its plate and leaves with it.
    multi = len(ids) > 1
    if multi or present is not None:
        S = set(ids)
        gone = set()
        if present is not None:
            gone = {b.id for k, b in enumerate(ctx.world.bodies) if not present[k]}
        for f in ctx.r.spec.fasteners:
            cl = (set(f.through or []) | ({f.threads_into} if f.threads_into else set())) - gone
            k = ctx.world.index(f.id)
            captive = bool(f.threads_into) and f.threads_into in gone
            if cl and cl <= S and (multi or captive) and (present is None or k is None or present[k]):
                ids.append(f.id)
                if f.threads_into in gone and k is not None:
                    backoff(ctx, k, f, present)
    return [k for k in (ctx.world.index(i) for i in ids) if k is not None]


def backoff(ctx, k, f, present):
    """A screw left captive in its plate (its standoff / nut has gone) is backed out along its axis until its head
    meets whatever is behind it (at most its length) before the plate moves; record that offset for `slide`."""
    offs = getattr(ctx, "asm_offsets", None)
    if offs is None:
        offs = ctx.asm_offsets = {}
    if k in offs:
        return
    v = -np.asarray(f.dir, float) / np.linalg.norm(f.dir)
    offs[k] = np.zeros(3)
    res = slide(ctx, [k], present, v)
    ln = float(measure_len(f))
    t = ln if res[0] == "ok" else max(0.0, min(ln, res[2] - STEP))
    offs[k] = v * t


def measure_len(f):
    import re
    m = re.search(r"x\s*([0-9.]+)", f.designation or "")
    return float(m.group(1)) if m else 0.0


def slide(ctx, members, present, d, base=None):
    """Slide `members` along `d` (starting from offset `base`): ('ok', travel) when clear of every present body,
    ('hit', j, t, at) for the first body hit."""
    w, r = ctx.world, ctx.r
    base = np.zeros(3) if base is None else np.asarray(base, float)
    offs = getattr(ctx, "asm_offsets", None) or {}
    others = [j for j, o in enumerate(w.bodies) if present[j] and j not in members and not o.is_wire]
    if others:
        others_max = max(float((_corners(w.bodies[j].aabb) @ d).max()) for j in others)
    else:
        others_max = -math.inf
    mine_min = min(float((_corners(w.bodies[m].aabb + base + offs.get(m, 0.0)) @ d).min()) for m in members)
    last = 0.0
    for k in range(int(MAX_TRAVEL / STEP) + 1):
        t = k * STEP
        if mine_min + t > others_max + 0.1:
            break
        shift = base + d * t
        for j in others:
            o = w.bodies[j]
            for m in members:
                b = w.bodies[m]
                sh = shift + offs.get(m, 0.0)
                if not measure.aabb_overlap(b.aabb + sh, o.aabb):
                    continue
                last = t
                allow = allowed_depth(r, b, o)
                if math.isinf(allow) or allow >= 1.0e3:
                    continue
                if measure.overlap_exceeds(b, o, max(allow, 0.05), sh):
                    return ("hit", j, t, b.aabb.mean(axis=0) + sh)
    return ("ok", last + 3.0)


def shank_clears(ctx, i, present):
    """A screw backed out along a free path until its shank has left the part it threads into and every part it passes
    through is out: the rest of its way is open, so it counts as removed even if the straight slide to infinity hits
    something further on (the other mount). Once clear it must also leave along a collision-free sideways path (a screw boxed in on all sides still fails). Returns (direction, travel)."""
    w, r = ctx.world, ctx.r
    b = w.bodies[i]
    f = next((f for f in r.spec.fasteners if f.id == b.id), None)
    if f is None or not f.threads_into:
        return None
    host = [w.index(t) for t in [f.threads_into] + list(f.through or [])]
    host = [j for j in host if j is not None and present[j]]
    for d in candidate_dirs(ctx, i):
        res = slide(ctx, [i], present, d)
        if res[0] != "hit":
            continue
        t = 0.0
        while t < res[2] - 1e-9:
            sh = d * t
            if not any(measure.aabb_overlap(b.aabb + sh, w.bodies[j].aabb) and
                       measure.overlap_exceeds(b, w.bodies[j], 0.05, sh) for j in host):
                for e in AXES:   # out of its threads, it must leave along a free path (lifted out of the gap), not just sit clear
                    if abs(float(e @ d)) > 0.99:
                        continue
                    r2 = slide(ctx, [i], present, e, base=sh)
                    if r2[0] == "ok":
                        return e, t + r2[1]
            t += STEP
    return None


def loose_exit(ctx, i, present):
    """A screw whose nut / threaded part has already left is loose: it backs out along its axis only until its shank
    clears the parts it passes through, then drops out sideways (a captive screw between an upright and a disc).
    Returns (direction, travel) of the second leg, or None."""
    w, r = ctx.world, ctx.r
    b = w.bodies[i]
    f = next((f for f in r.spec.fasteners if f.id == b.id), None)
    if f is None or not f.threads_into:
        return None
    k = w.index(f.threads_into)
    if k is None or present[k]:
        return None
    v = -np.asarray(f.dir, float) / np.linalg.norm(f.dir)
    first = slide(ctx, [i], present, v)
    reach = MAX_TRAVEL if first[0] == "ok" else first[2]
    thr = [w.index(t) for t in (f.through or [])]
    thr = [j for j in thr if j is not None and present[j]]
    t = 0.0
    while t <= reach:
        sh = v * t
        if not any(measure.aabb_overlap(b.aabb + sh, w.bodies[j].aabb) and
                   measure.overlap_exceeds(b, w.bodies[j], 0.05, sh) for j in thr):
            for d in AXES:
                if abs(float(d @ v)) > 0.99:
                    continue
                res = slide(ctx, [i], present, d, base=sh)
                if res[0] == "ok":
                    return d, t + res[1]
            return None
        t += STEP
    return None


TWO_LEG_MAX_SIZE = 15.0   # mm: only small loose parts (nuts, spacers) are tried
TWO_LEG_REACH = 12.0      # mm: the first leg stops at most this far in


def two_leg_exit(ctx, i, present):
    """A small part with no straight way out may slide a few mm out of its seat (leg 1, along an axis) and then
    leave sideways (leg 2) once it is clear of what held it. Returns (direction of leg 2, total travel) or None."""
    w = ctx.world
    b = w.bodies[i]
    if b.fastener or float((b.aabb[1] - b.aabb[0]).max()) > TWO_LEG_MAX_SIZE:
        return None
    members = [i]
    for d1 in AXES:
        first = slide(ctx, members, present, d1)
        reach = TWO_LEG_REACH if first[0] == "ok" else min(first[2], TWO_LEG_REACH)
        t = 1.4
        while t <= reach:
            base = d1 * t
            for d2 in AXES:
                if abs(float(d2 @ d1)) > 0.99:
                    continue
                res = slide(ctx, members, present, d2, base=base)
                if res[0] == "ok":
                    return d2, t + res[1]
            t += 1.4
    return None


def candidate_dirs(ctx, i):
    b, r = ctx.world.bodies[i], ctx.r
    if b.fastener:
        f = next((f for f in r.spec.fasteners if f.id == b.id), None)
        if f is None:
            return []
        v = np.asarray(f.dir, float)
        return [-v / np.linalg.norm(v)]
    d = list(AXES)
    for c in range(3):
        a = b.M[:3, c] / np.linalg.norm(b.M[:3, c])
        if all(abs(float(x @ a)) < 0.99 for x in AXES):
            d += [a, -a]
    return d


def _sweep(ctx, present, root, teardown, steps):
    """Repeatedly take off whatever can leave; `teardown` entries ({parts, dir}) are declared one-direction moves."""
    r, w = ctx.r, ctx.world
    n = len(w.bodies)
    while True:
        progress = False
        order = [i for i in range(n) if present[i] and i != root]
        order.sort(key=lambda i: 0 if w.bodies[i].fastener else 1)  # screws first
        for i in order:
            if not present[i]:
                continue
            b = w.bodies[i]
            members = [i] if b.fastener else [m for m in group(ctx, b.id, present) if present[m]]
            if root in members:
                continue
            for d in candidate_dirs(ctx, i):
                res = slide(ctx, members, present, d)
                if res[0] == "ok":
                    for m in members:
                        present[m] = False
                        steps.append(AssemblyStep(len(steps) + 1, w.bodies[m].id, [float(x) for x in d], float(res[1])))
                    progress = True
                    break
            else:
                le = shank_clears(ctx, i, present) if b.fastener else None
                if le is None:
                    le = loose_exit(ctx, i, present) if b.fastener else None
                if le is not None:
                    present[i] = False
                    steps.append(AssemblyStep(len(steps) + 1, b.id, [float(x) for x in le[0]], float(le[1])))
                    progress = True
        for t in teardown:
            ks = [w.index(pid) for pid in t.get("parts") or []]
            if not ks or any(k is None for k in ks) or not all(present[k] for k in ks):
                continue
            members = sorted({m for k in ks for m in group(ctx, w.bodies[k].id, present) if present[m]})
            if root in members:
                continue
            d = np.asarray(t.get("dir") or [0, 0, 1], float)
            d = d / np.linalg.norm(d)
            res = slide(ctx, members, present, d)
            if res[0] == "ok":
                for m in members:
                    present[m] = False
                    steps.append(AssemblyStep(len(steps) + 1, w.bodies[m].id, [float(x) for x in d], float(res[1])))
                progress = True
        left = sum(1 for i in range(n) if present[i] and i != root)
        if left == 0:
            break
        if not progress:
            # last resort: a small part that only has a sliding path of two legs (a nut pushed in from the cavity,
            # then dropped out through the open floor) leaves as it was put in
            for i in [i for i in range(n) if present[i] and i != root]:
                le = two_leg_exit(ctx, i, present)
                if le is not None:
                    present[i] = False
                    steps.append(AssemblyStep(len(steps) + 1, w.bodies[i].id, [float(x) for x in le[0]], float(le[1])))
                    progress = True
            if not progress:
                break


def apply_service_pose(ctx):
    """Spec `service_pose` [{parts, axis_at, axis_dir, deg, reason}]: rotate those bodies about an axis for the whole
    full-robot teardown (a weapon disc turned by hand so its rim clears the screws that hold the module). Returns undo()."""
    import trimesh.transformations as tf

    w = ctx.world
    undo = []
    for e in (ctx.r.spec.raw or {}).get("service_pose") or []:
        R = tf.rotation_matrix(np.radians(float(e.get("deg", 0.0))), e.get("axis_dir") or [1, 0, 0], e.get("axis_at") or [0, 0, 0])
        for pid in e.get("parts") or []:
            k = w.index(pid)
            if k is None:
                continue
            bd = w.bodies[k]
            undo.append((bd, bd.M.copy()))
            bd.M = R @ bd.M
            bd._mesh = bd._man = None
            bd._surf = {}
    def restore():
        for bd, M in undo:
            bd.M = M
            bd._mesh = bd._man = None
            bd._surf = {}
    return restore


def run(ctx):
    return _run(ctx)


def _run(ctx):
    r, w = ctx.r, ctx.world
    n = len(w.bodies)
    present = [not b.is_wire for b in w.bodies]
    rootp = next((p for p in r.spec.parts if p.kind == "structure"), None)
    root = w.index(rootp.id) if rootp else None
    steps, out = [], []
    # O-rings / elastic belts that can be stretched over their flanges (disasm.elastic_stretch) come off first by
    # stretching, not by a straight slide.
    from . import disasm

    nc = list(ctx.not_checked)
    for bid in sorted(disasm.elastic(ctx, [])):
        k = w.index(bid)
        if k is not None and present[k]:
            present[k] = False
            steps.append(AssemblyStep(len(steps) + 1, bid, [0.0, 0.0, 0.0], 0.0))
    ctx.not_checked[:] = nc
    restore = apply_service_pose(ctx)   # the declared service pose holds for the full-robot teardown only (not the bench pass)
    try:
        _sweep(ctx, present, root, getattr(r.spec, "teardown", None) or [], steps)
    finally:
        restore()
    # A declared swap module (spec `modules`) leaves as one unit; its bench teardown (`module_teardown`) is judged on the
    # module alone, its root plate staying put, so a quick-change weapon is checked both ways.
    stuck_bench = []
    for m in (r.spec.raw or {}).get("modules") or []:
        rk = w.index(m.get("root"))
        if rk is None or present[rk]:
            continue
        ids = {rk} | {k for k in (w.index(x) for x in m.get("parts") or []) if k is not None}
        ids |= set(group(ctx, m["root"], [True] * n))
        p2 = [k in ids and not w.bodies[k].is_wire for k in range(n)]
        _sweep(ctx, p2, rk, (r.spec.raw or {}).get("module_teardown") or [], steps)
        stuck_bench += [(k, p2) for k in range(n) if p2[k] and k != rk]
    stuck = [i for i in range(n) if present[i] and i != root]
    for i, pres in [(i, present) for i in stuck] + stuck_bench:
        b = w.bodies[i]
        members = [i] if b.fastener else group(ctx, b.id, pres)
        worst = None
        for d in candidate_dirs(ctx, i):
            res = slide(ctx, members, pres, d)
            if res[0] == "hit" and (worst is None or res[2] > worst[0]):
                worst = (res[2], res[1], d, res[3])
        if worst is not None:
            t, j, d, _ = worst
            msg = (f"`{b.id}` is trapped: its best way out is along ({d[0]:.0f}, {d[1]:.0f}, {d[2]:.0f}), which gets "
                   f"{t:.1f} mm before it hits `{w.bodies[j].id}`.")
        else:
            msg = f"`{b.id}` has no way out."
        out.append(fail("assembly.blocked", G, BLOCKER, "Part cannot be assembled", msg).on(b.id)
                   .here(worst[3] if worst else b.aabb.mean(axis=0))
                   .fix("Open the pocket on the side it enters from (a U-slot instead of a hole for a shaft, a bore open to the mating face for an insert, an open wall for a wheel), or split the housing so the part can drop in."))
    if not stuck and not stuck_bench:
        text = ", ".join(s.id for s in reversed(steps))
        out.append(ok("assembly.order", G, "Everything can be assembled",
                      f"Every part slides in along a clear straight path. Assembly order: {text}."))
    ctx.assembly = steps
    return out
