"""2D geometry for layout: outlines as shapely polygons, rectangles, clearances."""

from __future__ import annotations

from functools import lru_cache

from shapely.geometry import Polygon, box


def polygon(points) -> Polygon:
    p = Polygon([tuple(map(float, q)) for q in points])
    return p if p.is_valid else p.buffer(0)


@lru_cache(maxsize=64)
def _inset_cached(key, d):
    return polygon(key).buffer(-d, join_style=2)


def inset(points, d: float) -> Polygon:
    """The outline shrunk by `d` (mitred corners)."""
    return _inset_cached(tuple(tuple(map(float, q)) for q in points), float(d))


def rect_poly(r) -> Polygon:
    x0, x1, y0, y1 = r
    return box(x0, y0, x1, y1)


def rect_inside(r, poly: Polygon) -> bool:
    return poly.covers(rect_poly(r))


def rect_gap(a, b) -> float:
    """Clear distance between two rectangles (negative = overlap depth along the shallower axis)."""
    dx = max(a[0] - b[1], b[0] - a[1])
    dy = max(a[2] - b[3], b[2] - a[3])
    if dx < 0 and dy < 0:
        return max(dx, dy)
    return max(dx, dy) if (dx < 0 or dy < 0) else (dx * dx + dy * dy) ** 0.5


def bounds(points) -> tuple:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    return min(xs), max(xs), min(ys), max(ys)


def wall_distance(r, points) -> float:
    """Distance from the rectangle to the nearest point of the outline boundary."""
    return polygon(points).exterior.distance(rect_poly(r))


def manhattan(a, b) -> float:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
