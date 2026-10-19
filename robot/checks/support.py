"""Support under gravity in any orientation (`support.*`).

WHY: a combat robot is flipped, inverted and shaken every match. A part that only *rests* in its pocket (gravity holds it
on the -Z face) falls out or hammers around the moment the robot is upside down. So every part that nothing holds by a
declared method (screw, press fit, clamp, glue, ...) must be geometrically captured: translating it along any of the six
axis directions must hit another part within `MAX_PLAY_MM`. This is the gravity test with the robot in all six
orientations; it extends `retention.loose` (which covers only some kinds, at 0.5 mm) to every part, at 0.2 mm.
"""

from __future__ import annotations

import numpy as np

from .. import measure
from ..finding import BLOCKER, fail, ok
from .interference import DIRS, allowed_depth

G = "support"
MAX_PLAY_MM = 0.2  # more free travel than this in any direction = loose when inverted or shaken
LADDER = (MAX_PLAY_MM, 0.5, 1.0, 2.0, 5.0, 10.0)  # travel probes (mm); first blocked rung bounds the free travel
SKIP_KINDS = {"structure", "belt"}  # the chassis is the frame parts are held against; belts are held by tension (`tension.*`)
# Declared holds that resist pull-out in every direction. Tape/kapton/velcro, `pocket` and `interlock` are only as good as
# the geometry around them (tape peels when the part hammers), so those are measured.
HOLD_METHODS = {"screw", "screws", "shaft", "pin", "press_fit", "glue", "adhesive", "snap", "clamp", "strap", "fused"}


def hold_groups(r):
    """Union-find over declared holds (screws through/into parts, holding connections, fused; a joint locates but does not hold): part id -> root."""
    up = {p.id: p.id for p in r.spec.parts}

    def find(x):
        while up[x] != x:
            up[x] = up[up[x]]
            x = up[x]
        return x

    def join(a, b):
        if a in up and b in up:
            up[find(a)] = find(b)

    for f in r.spec.fasteners:
        ids = list(f.through or []) + ([f.threads_into] if f.threads_into else [])
        for o in ids[1:]:
            join(ids[0], o)
    for c in r.spec.connections:
        if c.method in HOLD_METHODS:
            join(c.a, c.b)
    for p in r.spec.parts:
        if p.fused_with:
            join(p.id, p.fused_with)
    return find


def held(r, p, find, anchored) -> bool:
    """True when a declared hold ties `p` (through any chain of holds) to the chassis, or a part-level hold covers it."""
    if p.joint is not None or (p.retained is not None and str(p.retained) in HOLD_METHODS):
        return True
    return find(p.id) in anchored


def free_travel(near, d) -> float:
    """Largest probed travel (mm) along unit `d` before any moving body hits its obstacle (`near`: [(body, obstacle, depth)])."""
    d = np.asarray(d, float)
    free = 0.0
    for t in LADDER:
        for b, o, ad in near:
            # overlap depth = half the slab thickness (see interference.captive): pad the shift by twice the threshold
            if measure.overlap_exceeds(b, o, ad + 0.02, d * (t + 2 * (ad + 0.02))):
                return free
        free = t
    return free


def run(ctx):
    """Each group of parts tied together by declared holds but not to the chassis is slid as one rigid body."""
    r, w = ctx.r, ctx.world
    out = []
    find = hold_groups(r)
    anchored = {find(p.id) for p in r.spec.parts if p.kind == "structure"}
    fgroup = {}  # fastener id -> hold group of the parts it passes through (it rides with them)
    for f in r.spec.fasteners:
        roots = {find(x) for x in list(f.through or []) + [f.threads_into] if x and x in {q.id for q in r.spec.parts}}
        if len(roots) == 1:
            fgroup[f.id] = roots.pop()

    def gid(o):
        if o.part_idx is not None:
            return find(r.parts[o.part_idx].part.id)
        return fgroup.get(o.id) if o.fastener else None

    groups = {}  # root -> (member bodies, ids that need a hold)
    for b in w.bodies:
        if b.part_idx is None or b.fastener or b.is_wire:
            continue
        p = r.parts[b.part_idx].part
        g = find(p.id)
        if g in anchored or p.kind in SKIP_KINDS:
            continue
        mem, need = groups.setdefault(g, ([], []))
        mem.append(b)
        if not held(r, p, find, anchored):
            need.append(p.id)
    reach = LADDER[-1] + 1.0
    checked = 0
    for g, (mem, need) in groups.items():
        if not need:
            continue
        checked += 1
        near = []  # (member, obstacle, allowed depth); parts held to the group move with it and cannot stop it
        for b in mem:
            grown = np.array([b.aabb[0] - reach, b.aabb[1] + reach])
            for o in w.bodies:
                if o.is_wire or gid(o) == g or not measure.aabb_overlap(o.aabb, grown):
                    continue
                ad = allowed_depth(r, b, o)
                if ad < 1.0e3:
                    near.append((b, o, ad))
        loose = []
        for name, d in DIRS:
            t = free_travel(near, d)
            if t > MAX_PLAY_MM:
                loose.append((name, t))
        if not loose:
            continue
        txt = ", ".join(f"{n} {'>=' if t >= LADDER[-1] else '~'}{t:g} mm" for n, t in loose)
        ids = need + [b.id for b in mem if b.id not in need]
        with_ = f" (moving as one with {', '.join(f'`{x}`' for x in ids[1:])})" if len(ids) > 1 else ""
        out.append(fail("support.loose", G, BLOCKER, "Part falls out when the robot is inverted or shaken",
                        f"`{ids[0]}`{with_} is not fastened, press-fit, clamped or captured to the chassis: it slides freely "
                        f"{txt} (limit {MAX_PLAY_MM:g} mm). Upside down or in a hit it drops out or rattles.")
                   .on(*ids).here(np.mean([b.aabb.mean(axis=0) for b in mem], axis=0))
                   .fix("Screw or clamp it to the chassis, close the open side with a lid/rib to <= 0.2 mm, or declare a real "
                        "hold (`retained`: press_fit, clamp, strap; or a `connections` entry with that method)."))
    if checked and not out:
        out.append(ok("support.loose", G, "Every unfastened part is captured",
                      f"{checked} unfastened part group(s) move at most {MAX_PLAY_MM:g} mm in all six directions."))
    return out
