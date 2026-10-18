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


def group(ctx, pid):
    """Members that move with part `pid` (tyres on their wheel, children on a joint)."""
    ids = [pid]
    while True:
        n = len(ids)
        for p in ctx.r.spec.parts:
            if (p.tyre_of in ids or p.parent in ids) and p.id not in ids:
                ids.append(p.id)
        if len(ids) == n:
            break
    return [k for k in (ctx.world.index(i) for i in ids) if k is not None]


def slide(ctx, members, present, d):
    """Slide `members` along `d`: ('ok', travel) when clear of every present body, ('hit', j, t, at) for the first body hit."""
    w, r = ctx.world, ctx.r
    others = [j for j, o in enumerate(w.bodies) if present[j] and j not in members and not o.is_wire]
    if others:
        others_max = max(float((_corners(w.bodies[j].aabb) @ d).max()) for j in others)
    else:
        others_max = -math.inf
    mine_min = min(float((_corners(w.bodies[m].aabb) @ d).min()) for m in members)
    last = 0.0
    for k in range(int(MAX_TRAVEL / STEP) + 1):
        t = k * STEP
        if mine_min + t > others_max + 0.1:
            break
        shift = d * t
        for j in others:
            o = w.bodies[j]
            for m in members:
                b = w.bodies[m]
                if not measure.aabb_overlap(b.aabb + shift, o.aabb):
                    continue
                last = t
                allow = allowed_depth(r, b, o)
                if math.isinf(allow) or allow >= 1.0e3:
                    continue
                if measure.overlap_exceeds(b, o, max(allow, 0.05), shift):
                    return ("hit", j, t, b.aabb.mean(axis=0) + shift)
    return ("ok", last + 3.0)


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


def run(ctx):
    r, w = ctx.r, ctx.world
    n = len(w.bodies)
    present = [not b.is_wire for b in w.bodies]
    rootp = next((p for p in r.spec.parts if p.kind == "structure"), None)
    root = w.index(rootp.id) if rootp else None
    steps, out = [], []
    while True:
        progress = False
        order = [i for i in range(n) if present[i] and i != root]
        order.sort(key=lambda i: 0 if w.bodies[i].fastener else 1)  # screws first
        for i in order:
            if not present[i]:
                continue
            b = w.bodies[i]
            members = [i] if b.fastener else group(ctx, b.id)
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
        left = sum(1 for i in range(n) if present[i] and i != root)
        if left == 0 or not progress:
            break
    stuck = [i for i in range(n) if present[i] and i != root]
    for i in stuck:
        b = w.bodies[i]
        members = [i] if b.fastener else group(ctx, b.id)
        worst = None
        for d in candidate_dirs(ctx, i):
            res = slide(ctx, members, present, d)
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
    if not stuck:
        text = ", ".join(s.id for s in reversed(steps))
        out.append(ok("assembly.order", G, "Everything can be assembled",
                      f"Every part slides in along a clear straight path. Assembly order: {text}."))
    ctx.assembly = steps
    return out
