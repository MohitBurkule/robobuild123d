"""[fix-S] Revron geometry helpers that read Revron parameters (stack count, window segments, Chaikin ratio, the M2 hole
radii); the parameter-free helpers live in the shared robocad.geom and are re-exported here."""
import json, math, os, sys
from collections import namedtuple
from robocad.geom import *  # noqa: F401,F403
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


def _ring_windows(p, c, r_in, r_out, half_deg, phase, rnd, seg_in=WSEG_FN):
    """p minus a ring sector window in each quadrant (N_STACK, `phase` deg from the first), corners rounded `rnd`."""
    from shapely.geometry import Point
    for k in range(N_STACK):
        q = Point(c).buffer(r_out, WSEG_MAX).difference(Point(c).buffer(r_in, seg_in)).intersection(_wedge(c, phase + 360.0 * k / N_STACK, half_deg, 2 * r_out))
        p = p.difference(_round(q, r_out=rnd))
    return p


def _offset_var(line, ds):
    """Offset of an open (x, y) polyline to its left by a per-point distance (averaged tangent normals, smoothed)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 2, 0)], line[min(i + 2, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty)
        out.append((x - ds[i] * ty / L, y + ds[i] * tx / L))
    return _chaikin_open(out, 0)


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


__all__ = [n for n in dir() if not n.startswith('__')]
