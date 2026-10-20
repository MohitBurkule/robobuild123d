"""[W1] Small helpers of the split tub modules: half-model mirroring, rectangles, symmetric outlines, cones."""
from shapely.geometry import Polygon
from .common import _b, _mirror_x


def both(*solids):
    """The +X solids and their -X mirror images."""
    return list(solids) + [_mirror_x(s) for s in solids]


def rect(x0, x1, y0, y1):
    return Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def inset_rect(c, d):
    """The chassis plan rectangle shrunk by d on every side."""
    return rect(-c["x"] + d, c["x"] - d, c["y0"] + d, c["y1"] - d)


def inner(c):
    """Inner wall faces (xi, yi0, yi1)."""
    return c["x"] - c["wall"], c["y0"] + c["wall"], c["y1"] - c["wall"]


def sym(half):
    """Outline symmetric about X = 0 from its +X half (points listed from the axis round the +X side back to the axis)."""
    return Polygon([(-u, v) for u, v in reversed(half)] + list(half)).buffer(0)


def cone(r_base, r_top, h, at, up=True):
    """Cone of height h standing on `at` (x, y, z), narrowing from r_base to r_top upwards (up) or downwards."""
    b = _b()
    return b.Solid.make_cone(r_base, r_top, h, b.Plane(origin=at, z_dir=(0, 0, 1 if up else -1)))
