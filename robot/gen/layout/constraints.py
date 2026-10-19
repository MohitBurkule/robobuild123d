"""Hard constraints of the layout CSP. Each is a small named predicate: unary ones judge one placement against the
problem, binary ones judge a new placement against those already made. Return None if satisfied, else a reason."""

from __future__ import annotations

from . import geom


def inside_shell(inp, comp, pl):
    """The cavity (component + gap) lies inside the outline shrunk by the wall."""
    if comp.on_wall:
        return None
    if not geom.rect_inside(pl.rect(inp.gap), geom.inset(inp.outline, inp.wall)):
        return "outside the shell"
    return None


def clear_of_keepouts(inp, comp, pl):
    r = pl.rect(inp.gap)
    for k in inp.keepouts:
        if geom.rect_gap(r, (k.x0, k.x1, k.y0, k.y1)) < inp.pocket_wall:
            return f"hits {k.id}"
    return None


def clear_of_holes(inp, comp, pl):
    r = pl.rect(inp.gap)
    for x, y, rad in inp.holes:
        if geom.rect_gap(r, (x - rad, x + rad, y - rad, y + rad)) < 0.6:
            return "hits a screw boss"
    return None


def edge_margins(inp, comp, pl):
    """Battery rule: >= min_front_mm from the front edge and >= min_side_mm from each side (combat R120/R121)."""
    if not (comp.min_front_mm or comp.min_side_mm):
        return None
    x0, x1, y0, y1 = geom.bounds(inp.outline)
    fx, fy = pl.footprint
    r = (pl.x - fx / 2, pl.x + fx / 2, pl.y - fy / 2, pl.y + fy / 2)
    if y1 - r[3] < comp.min_front_mm:
        return "too close to the front"
    if r[0] - x0 < comp.min_side_mm or x1 - r[1] < comp.min_side_mm:
        return "too close to a side"
    return None


def wall_reachable(inp, comp, pl):
    """Wall components (power switch) sit against the outer wall so a finger reaches them from outside."""
    if not comp.on_wall:
        return None
    r = pl.rect(inp.gap)
    if not geom.rect_inside(r, geom.inset(inp.outline, inp.wall)):
        return "switch pocket leaves the shell"
    if geom.wall_distance(r, inp.outline) > inp.wall + 4.0:
        return "switch not at the outer wall"
    x0, x1, y0, y1 = geom.bounds(inp.outline)
    gaps = {"front": y1 - r[3], "rear": r[2] - y0, "left": x1 - r[1], "right": r[0] - x0}
    if min(gaps, key=gaps.get) not in comp.wall_faces:
        return "switch on a wall it may not use"
    return None


def fixed_position(inp, comp, pl):
    if comp.fixed_at is None:
        return None
    fx, fy = comp.fixed_at[0], comp.fixed_at[1]
    return None if abs(pl.x - fx) < 1e-6 and abs(pl.y - fy) < 1e-6 else "not at its fixed position"


def no_overlap(inp, pl, placed):
    """Cavities keep a printable wall between them."""
    r = pl.rect(inp.gap)
    for other in placed:
        if geom.rect_gap(r, other.rect(inp.gap)) < inp.pocket_wall:
            return f"overlaps {other.id}"
    return None


def not_avoided(inp, comp, pl):
    """Placements a later stage (wiring) rejected: stay at least 4 mm away from them or turn."""
    for cid, x, y, rz in inp.avoid:
        if cid == comp.id and rz == pl.rot_z and abs(pl.x - x) + abs(pl.y - y) < 4.0:
            return "rejected by a later stage"
    return None


UNARY = (inside_shell, clear_of_keepouts, clear_of_holes, edge_margins, wall_reachable, fixed_position, not_avoided)
BINARY = (no_overlap,)


def unary_ok(inp, comp, pl) -> bool:
    return all(c(inp, comp, pl) is None for c in UNARY)


def binary_ok(inp, pl, placed) -> bool:
    return all(c(inp, pl, placed) is None for c in BINARY)
