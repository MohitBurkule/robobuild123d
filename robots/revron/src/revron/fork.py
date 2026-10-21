"""[fix-C] Revron fork group (split out of side.py; geometry unchanged)."""
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _fork_outline(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = FK_X[1 if s > 0 else -1]
    outline = Point(*FK_EYE).buffer(FK_EYE_R, FK_RES).union(Polygon(FK_BLADE))
    outline = _round(outline, r_out=FK_ROUND[0], r_in=FK_ROUND[1]).union(Polygon(FK_TIP)).buffer(FK_TIP_R, FK_RES_BUF).buffer(-FK_TIP_R, FK_RES_BUF)   # sharp tip, r0.15 (> kerf) where it joins
    p = outline.difference(Point(SB[0], SB[1]).buffer(FK_SB_R, FK_RES)).difference(Point(*FK_EYE).buffer(FK_PIN_R, FK_RES_PIN))
    p = p.difference(_round(Polygon(FK_WIN), r_out=FK_WIN_R))   # lightening window
    # laser kerf / min web: the knife tip cannot be cut sharp; keep the full length but end it in a 0.45 mm land
    p = p.union(_round(Polygon(FK_LAND), r_out=FK_LAND_R)).buffer(FK_LAND_R, FK_RES).buffer(-FK_LAND_R, FK_RES)   # closing: the land's junctions with the blade edges get r >= kerf
    if s < 0:   # the STEP hangs the left fork 1.1 deg nose-down about its standoff (pin-hole play in the cheek)
        from shapely import affinity
        p = affinity.rotate(p, FK_TILT, origin=SB)
    return p, x0, x1


def fork(s):
    p, x0, x1 = _fork_outline(s)
    return _ext(p, "yz", x0, x1)


def _fork_slot(s):
    """Seat for the fork tine in the wedgelet nose: exactly the 1.5 mm tine outline (window and tilt included), so the
    cut volume is the volume the fork fills and nothing else is taken from the TPU."""
    return fork(s)
