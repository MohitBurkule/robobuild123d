"""[tub2] Deck lightening pockets (cut from below, SKIN left): the diagonal ribs from the centre through the column centres bound the two
X pockets and two side pockets (R = wall at every rib corner); rear boxes sit between the stop walls. Right-hand pockets are mirrored."""
from build123d import Align, BuildSketch, Locations, Polygon, Rectangle, fillet
from .tub2_params import (POCKET_X, SIDE_X, CENTRE_Y, DIAG_K, RIB_OFF, FRONT_RIB, STOP_GAP, POCKET_SKIN, CENTRE_Y0, REAR_R, SKIN,
                          CH_WALL, CH_IN_X, COL_R, DECK, WALL_IN_FRONT, WALL_IN_REAR, STOP_BACK_Y, STOP_FRONT_Y, SA_X0)
from .tub2_util import prism, mirrored


def _cut(sk):
    return prism(sk, DECK - SKIN, DECK + SKIN)


def _rounded(pts, tips):
    """Polygon through pts with R = wall at the vertices listed in `tips`, sharp elsewhere."""
    with BuildSketch() as sk:
        Polygon(*pts, align=None)
        fillet([v for v in sk.vertices() if any(abs(v.X - x) + abs(v.Y - y) < SKIN / 10 for x, y in tips)], CH_WALL)
    return sk


def x_pockets():
    """Front pocket above the front rib, rear pocket below the rear rib; both pointed on the axis."""
    x, k, top = POCKET_X, DIAG_K, WALL_IN_FRONT - FRONT_RIB
    a_up, a_lo = CENTRE_Y + RIB_OFF, CENTRE_Y - RIB_OFF
    up = [(0, a_up), (x, a_up + k * x), (x, top), (-x, top), (-x, a_up + k * x)]
    face = STOP_FRONT_Y
    lo = [(0, a_lo), (x, a_lo - k * x), (x, face), (SA_X0, face), (SA_X0, face - STOP_GAP), (-SA_X0, face - STOP_GAP), (-SA_X0, face), (-x, face), (-x, a_lo - k * x)]
    tips = lambda p: [p[0], p[1], p[-1]]
    return [_cut(_rounded(up, tips(up))), _cut(_rounded(lo, tips(lo)))]


def side_pocket():
    """Triangle between the two rib edges (front rib's lower edge, rear rib's upper edge) out to SIDE_X; tip where they cross."""
    k, x = DIAG_K, SIDE_X
    up_y = lambda u: CENTRE_Y - RIB_OFF + k * u
    lo_y = lambda u: CENTRE_Y + RIB_OFF - k * u
    tip = RIB_OFF / k
    pts = [(tip, up_y(tip)), (x, up_y(x)), (x, lo_y(x))]
    return _cut(_rounded(pts, pts))


def rear_pockets():
    """Right-hand rear boxes: two share the width between the centre box and the side wall, split by one wall; the centre box is as wide as the boss."""
    x0, x1 = COL_R + SKIN, CH_IN_X - SKIN
    w = (x1 - x0 - CH_WALL) / 2
    y0, y1 = WALL_IN_REAR + POCKET_SKIN, STOP_BACK_Y - POCKET_SKIN
    with BuildSketch() as sk:
        for x in (x0, x0 + w + CH_WALL):
            with Locations((x, y0)):
                Rectangle(w, y1 - y0, align=(Align.MIN, Align.MIN))
        fillet(sk.vertices(), REAR_R)
    with BuildSketch() as ck:
        with Locations((0, CENTRE_Y0)):
            Rectangle(2 * COL_R, y1 - CENTRE_Y0, align=(Align.CENTER, Align.MIN))
        fillet(ck.vertices(), REAR_R)
    return _cut(sk), _cut(ck)


def deck_pockets():
    rear, centre = rear_pockets()
    return x_pockets() + [centre] + [mirrored(h) for h in (side_pocket(), rear)]
