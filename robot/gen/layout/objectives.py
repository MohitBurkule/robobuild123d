"""Soft objectives of the layout CSP (lower is better). Each term is a small function of the full placement set."""

from __future__ import annotations

import math

from . import geom

WEIGHTS = {"wire_mm": 0.05, "cog_mm": 1.0, "compact": 0.004, "spread": 0.0}


def port_point(inp, placements, ref: str):
    """World XY of `comp` (centre) or `comp.port`, or an anchor name."""
    if ref in inp.anchors:
        return inp.anchors[ref]
    cid, _, port = ref.partition(".")
    pl = placements.get(cid)
    if pl is None:
        return inp.anchors.get(cid)
    comp = next((c for c in inp.components if c.id == cid), None)
    if comp is None or not port or port not in comp.ports:
        return (pl.x, pl.y)
    lx, ly = comp.ports[port][0], comp.ports[port][1]
    a = math.radians(pl.rot_z)
    return (pl.x + lx * math.cos(a) - ly * math.sin(a), pl.y + lx * math.sin(a) + ly * math.cos(a))


def wire_mm(inp, placements) -> float:
    total = 0.0
    for l in inp.links:
        a, b = port_point(inp, placements, l.a), port_point(inp, placements, l.b)
        if a is not None and b is not None:
            total += l.weight * geom.manhattan(a, b)
    return total


def cog(inp, placements) -> tuple:
    m = sum(f[0] for f in inp.fixed_mass)
    sx = sum(f[0] * f[1] for f in inp.fixed_mass)
    sy = sum(f[0] * f[2] for f in inp.fixed_mass)
    for c in inp.components:
        pl = placements.get(c.id)
        if pl is not None:
            m += c.mass_g
            sx += c.mass_g * pl.x
            sy += c.mass_g * pl.y
    return (sx / m, sy / m) if m else (0.0, 0.0)


def cog_mm(inp, placements) -> float:
    cx, cy = cog(inp, placements)
    return math.hypot(cx - inp.cog_target[0], cy - inp.cog_target[1])


def compact(inp, placements) -> float:
    rs = [p.rect() for p in placements.values()]
    if not rs:
        return 0.0
    return (max(r[1] for r in rs) - min(r[0] for r in rs)) * (max(r[3] for r in rs) - min(r[2] for r in rs))


TERMS = {"wire_mm": wire_mm, "cog_mm": cog_mm, "compact": compact}


def evaluate(inp, placements, weights=None) -> tuple:
    w = dict(WEIGHTS, **(weights or {}))
    terms = {k: f(inp, placements) for k, f in TERMS.items()}
    return sum(w.get(k, 0.0) * v for k, v in terms.items()), terms
