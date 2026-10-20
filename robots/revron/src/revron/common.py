"""[fix-S] Shared geometry helpers: polygons, extrusions, booleans, lofts, Chaikin/PCHIP smoothing, catalog hardware."""
import json, math, os, sys
from .params import *  # noqa: F401,F403


def _polar(r, n=N_STACK, phase=0.0):
    """Points of a polar pattern (build123d PolarLocations in the 2D shapely profiles): n points on radius r."""
    return [(r * math.cos(math.radians(phase + 360.0 * k / n)), r * math.sin(math.radians(phase + 360.0 * k / n))) for k in range(n)]


def _m2():
    """ISO 273 / ISO 2306 M2 hole radii from the fastener catalog: (tap drill r, close clearance r, normal clearance r)."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad import fastener_catalog as fc
    return fc.tap_drill(2.0) / 2, fc.clearance(2.0, "close") / 2, fc.clearance(2.0, "normal") / 2


# ---------------------------------------------------------------------------------------------------------------- 2D
def _arc(c, r, a0, a1, n=24):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def _poly(pts):
    from shapely.geometry import Polygon
    return Polygon(pts).buffer(0)


def _round(p, r_out=0.0, r_in=0.0):
    """Shapely polygon with convex corners rounded r_out and concave corners r_in (2D fillets)."""
    if r_in:
        p = p.buffer(r_in, join_style=1).buffer(-r_in, join_style=1)
    if r_out:
        p = p.buffer(-r_out, join_style=1).buffer(r_out, join_style=1)
    return p


def _tangent_line_circle(p, c, r, upper=True):
    """Tangent point on circle (c, r) of a line from point p (upper / lower side seen from p)."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    d = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    b = math.asin(r / d)
    t = a + (b if upper else -b)
    L = math.sqrt(d * d - r * r)
    return (p[0] + L * math.cos(t), p[1] + L * math.sin(t))


# ---------------------------------------------------------------------------------------------------------------- 3D
def _b():
    import build123d as b
    return b


def _face(poly, plane):
    """build123d face of a shapely polygon (with holes) drawn on `plane` ('xy', 'yz', 'xz') at offset 0."""
    b = _b()
    def to3(u, v):
        return {"xy": (u, v, 0.0), "yz": (0.0, u, v), "xz": (u, 0.0, v)}[plane]
    def wire(ring):
        pts = [b.Vector(*to3(u, v)) for u, v in list(ring.coords)[:-1]]
        return b.Wire.make_polygon(pts, close=True)
    polys = getattr(poly, "geoms", [poly])
    faces = []
    for p in polys:
        if p.area < 1e-6:
            continue
        f = b.Face(wire(p.exterior), [wire(i) for i in p.interiors])
        faces.append(f)
    return faces


def _ext(poly, plane, a0, a1):
    """Prism of a shapely polygon on `plane`, extruded along its normal from a0 to a1."""
    b = _b()
    n = {"xy": (0, 0, 1), "yz": (1, 0, 0), "xz": (0, 1, 0)}[plane]
    a0, a1 = min(a0, a1), max(a0, a1)
    out = None
    for f in _face(poly, plane):
        s = b.Solid.extrude(f, b.Vector(*[c * (a1 - a0) for c in n])).moved(b.Location(tuple(c * a0 for c in n)))
        out = s if out is None else out.fuse(s)
    return out


def _cyl(r, a0, a1, c, axis="x"):
    b = _b()
    a0, a1 = min(a0, a1), max(a0, a1)
    d = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
    o = {"x": (a0, c[0], c[1]), "y": (c[0], a0, c[1]), "z": (c[0], c[1], a0)}[axis]
    return b.Solid.make_cylinder(r, a1 - a0, b.Plane(origin=o, z_dir=d))


def _box(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Solid.make_box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)).moved(b.Location((min(x0, x1), min(y0, y1), min(z0, z1))))


def _csk(d_hole, d_head, at, axis, sign, depth=8.0, head=3.0):
    """Countersink + clearance for a flat head screw whose head is flush at `at` (face point), shank going `sign`
    along `axis`: a 90 deg cone from d_head at the face down to d_hole, the clearance hole, and a head bore outward."""
    b = _b()
    d = [0.0, 0.0, 0.0]
    d[{"x": 0, "y": 1, "z": 2}[axis]] = float(sign)
    h = (d_head - d_hole) / 2
    cone = b.Solid.make_cone(d_head / 2, d_hole / 2, h, b.Plane(origin=at, z_dir=d))
    hole = b.Solid.make_cylinder(d_hole / 2, depth, b.Plane(origin=at, z_dir=d))
    head = b.Solid.make_cylinder(d_head / 2, head, b.Plane(origin=at, z_dir=[-c for c in d]))
    return cone.fuse(hole, head)


def _one(x):
    """Normalise a boolean result (Solid / Compound / ShapeList) to a single shape."""
    b = _b()
    if isinstance(x, (list, tuple)) or type(x).__name__ == "ShapeList":
        x = list(x)
        return x[0] if len(x) == 1 else b.Compound(x)
    return x


def _U(*s):
    s = [_one(x) for x in s if x is not None]
    return _one(s[0].fuse(*s[1:]).clean()) if len(s) > 1 else s[0]


def _S(base, *c):
    c = [_one(x) for x in c if x is not None]
    base = _one(base)
    return _one(base.cut(*c).clean()) if c else base


def _I(a, b_):
    return _one(_one(a).intersect(_one(b_)))


def _mirror_x(s):
    return s.mirror(_b().Plane.YZ)


def _solid(x):
    b = _b()
    if isinstance(x, b.Solid):
        return x
    sols = x.solids()
    if len(sols) == 1:
        return sols[0]
    return b.Compound(list(sols))


def Polygon_(pts):
    from shapely.geometry import Polygon
    return Polygon(pts)


def _wedge(c, a0, half_deg, reach, n=36):
    """Sector polygon from c, `half_deg` either side of the direction a0 (deg), out to `reach`."""
    from shapely.geometry import Polygon
    return Polygon([c] + [(c[0] + reach * math.cos(math.radians(a0 + d)), c[1] + reach * math.sin(math.radians(a0 + d)))
                         for d in [-half_deg + 2 * half_deg * i / n for i in range(n + 1)]])


def _ring_windows(p, c, r_in, r_out, half_deg, phase, rnd, seg_in=WSEG_FN):
    """p minus a ring sector window in each quadrant (N_STACK, `phase` deg from the first), corners rounded `rnd`."""
    from shapely.geometry import Point
    for k in range(N_STACK):
        q = Point(c).buffer(r_out, WSEG_MAX).difference(Point(c).buffer(r_in, seg_in)).intersection(_wedge(c, phase + 360.0 * k / N_STACK, half_deg, 2 * r_out))
        p = p.difference(_round(q, r_out=rnd))
    return p


# ------------------------------------------------------------------------------------------------------------ wheels
def _revolve_x(profile, x_at, c):
    """Solid of revolution about the X axis through c = (Y, Z): profile [(x, r)] in local x from x_at."""
    b = _b()
    pts = [b.Vector(x_at + x, c[0], c[1] + r) for x, r in profile]
    f = b.Face(b.Wire.make_polygon(pts, close=True))
    return b.Solid.revolve(f, 360, b.Axis((0, c[0], c[1]), (1, 0, 0)))


def _interp(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return ys[-1]


def _end_cap(p, q, prev, n=5):
    """Points of a half-round cap from p to q (open ends of a band), bulging away from `prev`."""
    cx, cy = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    r = math.dist(p, q) / 2
    a0 = math.atan2(p[1] - cy, p[0] - cx)
    tx, ty = p[0] - prev[0], p[1] - prev[1]
    sgn = 1 if math.cos(a0 + math.pi / 2) * tx + math.sin(a0 + math.pi / 2) * ty > 0 else -1
    return [(cx + r * math.cos(a0 + sgn * math.pi * k / (n + 1)), cy + r * math.sin(a0 + sgn * math.pi * k / (n + 1))) for k in range(1, n + 1)]


def _offset_var(line, ds):
    """Offset of an open (x, y) polyline to its left by a per-point distance (averaged tangent normals, smoothed)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 2, 0)], line[min(i + 2, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty)
        out.append((x - ds[i] * ty / L, y + ds[i] * tx / L))
    return _chaikin_open(out, 0)


def _offset_open(line, d):
    """Offset of an open (x, y) polyline by d to its left (mitre at the vertices, same point count)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 1, 0)], line[min(i + 1, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty)
        out.append((x - d * ty / L, y + d * tx / L))
    return out


def _pchip_open(p, n):
    """Open path through the points p (monotone cubic in chord length: passes through every measured point, no
    overshoot); Chaikin corner cutting pulled the front swing 0.8 mm off the STEP inner face."""
    import numpy as np
    from scipy.interpolate import PchipInterpolator
    P = np.asarray(p, float)
    t = np.r_[0.0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    u = np.linspace(0.0, t[-1], n)
    return [(float(x), float(y)) for x, y in zip(PchipInterpolator(t, P[:, 0])(u), PchipInterpolator(t, P[:, 1])(u))]


def _chaikin_open(p, n):
    k = CHAIKIN_Q
    c = 1 - k
    for _ in range(n):
        q = [p[0]]
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            q += [(c * x0 + k * x1, c * y0 + k * y1), (k * x0 + c * x1, k * y0 + c * y1)]
        q.append(p[-1])
        p = q
    return p


def _band(path, w):
    """Shapely polygon between an open path and its offset by w to the left (round joins)."""
    from shapely.geometry import LineString, Polygon
    off = LineString(path).offset_curve(w, join_style=1)
    oc = list(off.coords)
    if math.dist(oc[0], path[0]) > math.dist(oc[-1], path[0]):
        oc = oc[::-1]
    return Polygon(list(path) + oc[::-1]).buffer(0)


def _loft_yz(pa, xa, pb, xb, n=160):
    """Ruled loft between two shapely outlines in YZ planes at X xa and xb (both resampled to n points from the point
    nearest +Y, so the rulings do not twist)."""
    return _loft_yz_n([(pa, xa), (pb, xb)], n)


def _loft_yz_n(sections, n=160):
    """One ruled loft through several (shapely outline, X) sections: the same faces as a chain of two-section _loft_yz
    slices, but one solid, so the chain is not handed to a fuse slice by slice (24 touching slices in one fuse ran OCC
    out of memory on a cold build)."""
    b = _b()
    def wire(p, x):
        ring = list(p.exterior.coords)[:-1]
        if Polygon(ring).exterior.is_ccw is False:
            ring = ring[::-1]
        k = max(range(len(ring)), key=lambda i: (ring[i][0], -abs(ring[i][1])))
        ring = ring[k:] + ring[:k] + [ring[k]]
        pts = _resample(ring, n + 1)[:-1]
        return b.Wire.make_polygon([b.Vector(x, u, v) for u, v in pts], close=True)
    from shapely.geometry import Polygon
    return b.Solid.make_loft([wire(p, x) for p, x in sections], ruled=True)


def _resample(line, n):
    from shapely.geometry import LineString
    ln = LineString(line)
    return [tuple(ln.interpolate(i / (n - 1), normalized=True).coords[0]) for i in range(n)]


def _band_wire(path, w, z, n=160):
    """Closed wire of a wall band: the inner face path and its offset by w to the left (shapely, round joins), both
    resampled to n points so bands of different width loft cleanly."""
    from shapely.geometry import LineString
    b = _b()
    off = LineString(path).offset_curve(w, join_style=1)
    oc = list(off.coords)
    if math.dist(oc[0], path[0]) > math.dist(oc[-1], path[0]):
        oc = oc[::-1]
    pts = _resample(path, n) + _resample(oc, n)[::-1]
    return b.Wire.make_polygon([b.Vector(x, y, z) for x, y in pts], close=True)


__all__ = [n for n in dir() if not n.startswith('__')]
