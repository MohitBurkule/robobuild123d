"""[fix-C] Revron fork group (split out of side.py; geometry unchanged)."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _blade(s):
    from shapely.geometry import Point, Polygon
    seg = FORK_SEG
    body = Point(*FORK_EYE).buffer(FORK_EYE_R, seg["eye"]).union(Polygon(FORK_BLADE))
    body = _round(body, r_out=FORK_R_OUT, r_in=FORK_R_IN).union(Polygon(FORK_TIP_WEDGE))
    return body.buffer(FORK_R_TIP, seg["tip"]).buffer(-FORK_R_TIP, seg["tip"])


def _drill(p):
    from shapely.geometry import Point, Polygon
    seg = FORK_SEG
    p = p.difference(Point(SB[0], SB[1]).buffer(FORK_BORE_R, seg["eye"])).difference(Point(*FORK_EYE).buffer(FORK_PIN_R, seg["pin"]))
    return p.difference(_round(Polygon(FORK_WINDOW), r_out=FORK_R_WINDOW))


def _fork_outline(s):
    """Ti fork on the nose standoff: eye + blade tapering to a 0.45 mm kerf-safe land, pin hole, lightening window."""
    from shapely.geometry import Polygon
    from shapely import affinity
    p = _drill(_blade(s)).union(_round(Polygon(FORK_TIP_LAND), r_out=FORK_R_TIP)).buffer(0)
    if s < 0:
        p = affinity.rotate(p, FORK_TILT, origin=SB)
    return p, *FORK_X[1 if s > 0 else -1]


def fork(s):
    p, x0, x1 = _fork_outline(s)
    return _ext(p, "yz", x0, x1)


def _fork_slot(s):
    """Seat for the tine in the wedgelet nose: the filled outline swept up out of the ramp so the slit is open on top."""
    from shapely.geometry import Polygon, box
    from shapely import affinity
    p, x0, x1 = _fork_outline(s)
    solid = Polygon(p.exterior)
    up = solid
    for k in range(1, FORK_SWEEP["steps"] + 1):
        up = up.union(affinity.translate(solid, 0, FORK_SWEEP["dy"] * k))
    up = up.intersection(box(*FORK_SWEEP["clip"])).union(solid)
    return _ext(up.buffer(0), "yz", x0, x1)
