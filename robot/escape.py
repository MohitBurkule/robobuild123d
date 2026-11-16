"""Smallest move that clears a collision, measured on the meshes so nobody hand-computes geometry.

For an overlapping pair (a, b) try sliding each body along +-X, +-Y, +-Z and find (by bisection) the least travel
that brings the overlap depth down to the allowed depth. Each option also reports which OTHER parts the moved body
would then hit, so the caller can pick a move that does not just shift the problem. Used by the interference check
(exact numbers in the blocker message and in the repair hints) and by the jiggle solver (robot/solve/jiggle.py).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from . import measure

AXES = [(n, np.array(v, float)) for n, v in (("+x", (1, 0, 0)), ("-x", (-1, 0, 0)), ("+y", (0, 1, 0)),
                                              ("-y", (0, -1, 0)), ("+z", (0, 0, 1)), ("-z", (0, 0, -1)))]
MAX_TRAVEL_MM = 8.0   # moves longer than this are redesigns, not nudges
TOL_MM = 0.02         # bisection resolution
MARGIN_MM = 0.05      # added to the cleared travel so the result is not exactly on the limit


@dataclass
class Move:
    part: str
    axis: str
    vec: list            # world-frame shift, mm
    mm: float
    new_hits: list = field(default_factory=list)   # [(other part id, depth mm)] collisions the move creates
    note: str = ""       # e.g. "or shorten the screw by 0.9 mm" when moving a fastener along its own axis
    vol: float = 0.0     # mover volume: smaller parts are cheaper to move

    def text(self) -> str:
        s = f"move `{self.part}` {self.axis} {self.mm:.2f} mm"
        if self.new_hits:
            s += " (then hits " + ", ".join(f"`{o}` {d:.2f} mm" for o, d in self.new_hits) + ")"
        return s + (f" {self.note}" if self.note else "")

    def to_dict(self):
        return {"part": self.part, "axis": self.axis, "vec": self.vec, "mm": round(self.mm, 3),
                "new_hits": [[o, round(d, 3)] for o, d in self.new_hits]}


def _depth(a, b, shift, allow):
    o = measure.overlap(a, b, shift, cap=allow)
    return 0.0 if o is None else float(o.depth)


def clear_travel(a, b, d, allow, max_travel=MAX_TRAVEL_MM):
    """Least travel of `a` along unit vector d so overlap(a, b) <= allow; None if not within max_travel."""
    lo, hi = 0.0, None
    steps, s = [], 0.25
    while s < max_travel:
        steps.append(s)
        s *= 2
    for s in steps + [max_travel]:   # grow until clear (nudges are short, so the first clear step brackets it)
        if _depth(a, b, d * s, allow) <= allow:
            hi = s
            break
        lo = s
    if hi is None:
        return None
    while hi - lo > TOL_MM:
        m = (lo + hi) / 2
        if _depth(a, b, d * m, allow) <= allow:
            hi = m
        else:
            lo = m
    return hi + MARGIN_MM


def new_hits(world, body, shift, skip, allow_fn):
    """Bodies the shifted `body` would overlap (beyond their allowance), except ids in `skip`."""
    box = body.aabb + shift
    out = []
    for o in world.bodies:
        if o.id in skip or o.id == body.id or o.is_wire or not measure.aabb_overlap(box, o.aabb):
            continue
        allow = allow_fn(body, o)
        if not np.isfinite(allow):
            continue
        dpt = _depth(body, o, shift, allow)
        if dpt > allow:
            out.append((o.id, dpt))
    return out


def options(world, a, b, allow, allow_fn, movers=None, max_travel=MAX_TRAVEL_MM, carry=None):
    """All single-axis moves that clear (a, b), best first: fewest new collisions, then shortest travel.
    `movers`: ids allowed to move (default both). `carry(id)`: ids that move with it (children), skipped in new_hits."""
    res = []
    for mover, other in ((a, b), (b, a)):
        if movers is not None and mover.id not in movers:
            continue
        group = carry(mover.id) if carry else {mover.id}
        for name, d in AXES:
            t = clear_travel(mover, other, d, allow, max_travel)
            if t is None:
                continue
            hits = new_hits(world, mover, d * t, group | {other.id}, allow_fn)
            note = ""
            if getattr(mover, "fastener", False):
                ax = np.asarray(mover.M, float)[:3, 2]
                if abs(float(ax @ d)) > 0.99:
                    note = f"(or a screw {t:.1f} mm shorter: next stock length down)"
            vol = float(getattr(mover.geom, "volume", 0.0) or 0.0)
            res.append(Move(mover.id, name, [float(x) for x in d * t], t, hits, note, vol))
    res.sort(key=lambda m: (len(m.new_hits), round(m.mm, 1), m.vol))
    return res


def summary(opts, n=3) -> str:
    """One line for a finding message: the best clean moves."""
    if not opts:
        return f"No single-axis move under {MAX_TRAVEL_MM:.0f} mm clears it: resize a part or cut a pocket."
    clean = [m for m in opts if not m.new_hits]
    pick = (clean or opts)[:n]
    head = "Smallest fixes (measured): " if clean else "No clean move; least bad: "
    return head + "; or ".join(m.text() for m in pick) + "."
