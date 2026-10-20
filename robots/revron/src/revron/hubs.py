"""[fix-C] Revron hubs group: rear / front hubs, tyres and standoffs (split out of side.py; geometry unchanged)."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _mirrored(prof, s):
    return [(s * x, r) for x, r in prof]


def _d_outline(cy, cz, d=RH_D):
    from shapely.geometry import Polygon
    fa = math.asin(d["flat"] / d["r"])
    hx = d["r"] * math.cos(fa)
    a0, span = math.pi - fa, math.pi + 2 * fa
    arc = [(cy + d["r"] * math.cos(a0 + span * k / (d["arc_n"] - 1)), cz + d["r"] * math.sin(a0 + span * k / (d["arc_n"] - 1)))
           for k in range(d["arc_n"])]
    n = d["flat_n"]
    flat = [(cy + hx - 2 * hx * k / n, cz + d["flat"] - d["crown"] * math.sin(math.pi * k / n)) for k in range(1, n)]
    return Polygon(arc + flat)


def _grub(s):
    from robot.cad.holes import hole_tool
    top = RH_SEAT_R
    return hole_tool((s * RH_GRUB_X, RY, RZ + top), (0, 0, -1), "M2x5", head="cap", into="tapped", side="thread",
                     engage=top - RH_D["flat"])[0]


def _nut_slot(s):
    z0, z1 = RH_NUT_Z
    return _box(s * RH_BORE_X, s * RH_NUT_X, RY - RH_NUT_HALF, RY + RH_NUT_HALF, RZ + z0, RZ + z1)


def rear_hub(s):
    body = _revolve_x(_mirrored(REAR_HUB_PROFILE, s), s * RH_ORIGIN_X, (RY, RZ))
    return _S(body, _ext(_d_outline(RY, RZ), "yz", s * RH_BORE_X, s * RH_NUT_X), _nut_slot(s), _grub(s))


def front_hub(s):
    return _revolve_x(_mirrored(FRONT_HUB_PROFILE, s), s * FH_ORIGIN_X, SA)


def _tyre_arc(cx, cr, rs, angles):
    return [(cx + rs * math.cos(math.radians(a)) * k, cr + rs * math.sin(math.radians(a))) for a, k in angles]


def tyre(od, idd, x0, x1, c, shoulder=0.0):
    if shoulder <= 0:
        return _S(_cyl(od / 2, x0, x1, c), _cyl(idd / 2, x0 - 1, x1 + 1, c))
    R, rs, w, st = od / 2, shoulder, x1 - x0, TYRE_SECTION_STEP
    up = [(a, -1) for a in range(0, QUARTER_TURN + 1, st)]
    down = [(a, 1) for a in range(QUARTER_TURN, -1, -st)]
    prof = [(0.0, idd / 2)] + _tyre_arc(rs, R - rs, rs, up) + _tyre_arc(w - rs, R - rs, rs, down) + [(w, idd / 2)]
    return _revolve_x(prof, x0, c)


def standoff_end(L_x, c):
    """The standoff's outboard end: (point, outward axis). The side panel's SA boss seats on it."""
    x = max(L_x, key=abs)
    return (x, *c), (x / abs(x), 0.0, 0.0)


def standoff(L_x, c):
    b = _b()
    s = _S(_cyl(SO_R, *L_x, c), _cyl(STANDOFF_BORE_R, L_x[0] - 1, L_x[1] + 1, c))
    p, z = standoff_end(L_x, c)
    b.RigidJoint("end", s, b.Location(b.Plane(origin=p, z_dir=z)))   # [fix-C-j1] the panel's `sa` joint connects here
    return s
