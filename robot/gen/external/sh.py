"""Tiny builders for the spec's shape JSON (see GUIDE.md `shape`). Everything returns plain dicts."""

from __future__ import annotations

import math


def r(v, n=3):
    return round(float(v), n)


def place(s, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": s, "at": [r(a) for a in at], "rot": [r(a) for a in rot]}


def box(sx, sy, sz, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "box", "size": [r(sx), r(sy), r(sz)]}, at, rot)


def boxr(x0, x1, y0, y1, z0, z1):
    """Box from its extents."""
    return box(x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))


def cyl(radius, height, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "cylinder", "radius": r(radius), "height": r(height)}, at, rot)


def cyl_axis(radius, a0, a1, axis, c0, c1):
    """Cylinder along `axis` ('x'|'y'|'z') from a0 to a1; (c0, c1) are the other two coordinates in xyz order."""
    mid, h = (a0 + a1) / 2, abs(a1 - a0)
    if axis == "x":
        return cyl(radius, h, (mid, c0, c1), (0, 90, 0))
    if axis == "y":
        return cyl(radius, h, (c0, mid, c1), (-90, 0, 0))
    return cyl(radius, h, (c0, c1, mid))


def prism(points, height, at=(0, 0, 0), rot=(0, 0, 0), spline=False):
    s = {"type": "spline_prism" if spline else "prism", "points": [[r(x), r(y)] for x, y in points], "height": r(height)}
    return place(s, at, rot)


def side_prism(points_yz, x0, x1):
    """Extrude a Y-Z profile along X from x0 to x1 (profile points are (y, z))."""
    s = {"type": "prism", "points": [[r(y), r(z)] for y, z in points_yz], "height": r(x1 - x0)}
    return place(place(s, (0, 0, 0), (90, 0, 90)), ((x0 + x1) / 2, 0, 0))


def front_prism(points_xz, y0, y1):
    """Extrude an X-Z profile along Y from y0 to y1 (profile points are (x, z))."""
    s = {"type": "prism", "points": [[r(x), r(z)] for x, z in points_xz], "height": r(y1 - y0)}
    return place(place(s, (0, 0, 0), (90, 0, 0)), (0, (y0 + y1) / 2, 0))


def revolve(profile_rz, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "revolve", "profile": [[r(a), r(b)] for a, b in profile_rz]}, at, rot)


def loft(sections, ruled=False):
    return {"type": "loft", "sections": sections, "ruled": ruled}


def U(*items):
    items = [i for i in items if i is not None]
    return items[0] if len(items) == 1 else {"type": "union", "items": list(items)}


def S(base, *cuts):
    cuts = [c for c in cuts if c is not None]
    return base if not cuts else {"type": "subtract", "base": base, "cut": list(cuts)}


def fillet(s, radius):
    return {"type": "fillet", "shape": s, "radius": r(radius)}


def mirror(s, axis="x"):
    return {"type": "mirror", "shape": s, "axis": axis}


def circle_pts(cx, cy, rad, n=24, a0=0.0):
    return [(cx + rad * math.cos(a0 + 2 * math.pi * i / n), cy + rad * math.sin(a0 + 2 * math.pi * i / n)) for i in range(n)]


def rounded_rect_pts(x0, x1, y0, y1, rad, n=4):
    """Rounded rectangle outline (counter-clockwise), `n` points per corner arc."""
    out = []
    for cx, cy, a in ((x1 - rad, y1 - rad, 0), (x0 + rad, y1 - rad, 90), (x0 + rad, y0 + rad, 180), (x1 - rad, y0 + rad, 270)):
        for i in range(n + 1):
            t = math.radians(a + 90 * i / n)
            out.append((cx + rad * math.cos(t), cy + rad * math.sin(t)))
    return out
