"""[tub2] Deck lightening pockets (cut from below, SKIN left): the diagonal ribs from the centre through the column centres bound the two
X pockets and two side pockets (R = wall at every rib corner); rear boxes sit between the stop walls. Right-hand pockets are mirrored."""
from build123d import Align, BuildSketch, Circle, Locations, Mode, Polygon, Rectangle, fillet
from .tub2_params import (INS_AXIS, POCKET_X, SIDE_X, CENTRE_Y, DIAG_K, RIB_OFF, FRONT_RIB, STOP_GAP, POCKET_SKIN, CENTRE_Y0, REAR_R, SKIN,
                          CH_WALL, CH_IN_X, COL_R, DECK, OVER, WALL_IN_FRONT, WALL_IN_REAR, STOP_BACK_Y, STOP_FRONT_Y, SA_X0)
from .tub2_util import box_xy, concave_filler, fit_radius, prism, mirrored


def _cut(sk, below=SKIN):
    return prism(sk, DECK - below, DECK + SKIN)


def _rounded(pts, tips):
    """Polygon through pts with R = wall at the vertices listed in `tips`, sharp elsewhere. A corner whose rib or wall edges are too
    short for the full wall radius (a thicker wall squeezes the pocket) takes the largest round that fits."""
    tips = [min(range(len(pts)), key=lambda i: abs(pts[i][0] - x) + abs(pts[i][1] - y)) for x, y in tips]
    with BuildSketch() as sk:
        Polygon(*pts, align=None)
        for i in tips:
            r = fit_radius(pts, i, CH_WALL, [j for j in tips if j != i])
            fillet([v for v in sk.vertices() if abs(v.X - pts[i][0]) + abs(v.Y - pts[i][1]) < SKIN / 10], r)
    return sk


def x_pockets():
    """Front pocket above the front rib, rear pocket below the rear rib; both pointed on the axis."""
    x, k, top = POCKET_X, DIAG_K, WALL_IN_FRONT - FRONT_RIB
    a_up, a_lo = CENTRE_Y + RIB_OFF, CENTRE_Y - RIB_OFF
    up = [(0, a_up), (x, a_up + k * x), (x, top), (-x, top), (-x, a_up + k * x)]
    face = STOP_FRONT_Y
    lo = [(0, a_lo), (x, a_lo - k * x), (x, face), (SA_X0, face), (SA_X0, face - STOP_GAP), (-SA_X0, face - STOP_GAP), (-SA_X0, face), (-x, face), (-x, a_lo - k * x)]
    tips = lambda p: [p[0], p[1], p[-1]]
    return [_cut(_rounded(up, tips(up)), 0), _cut(_rounded(lo, tips(lo)), 0)]


def side_pocket():
    """Triangle between the two rib edges (front rib's lower edge, rear rib's upper edge) out to SIDE_X; tip where they cross."""
    k, x = DIAG_K, SIDE_X
    up_y = lambda u: CENTRE_Y - RIB_OFF + k * u
    lo_y = lambda u: CENTRE_Y + RIB_OFF - k * u
    tip = RIB_OFF / k
    pts = [(tip, up_y(tip)), (x, up_y(x)), (x, lo_y(x))]
    return _cut(_rounded(pts, pts))


def _rear_layout():
    """Right-hand rear boxes: x0 (first box start), w (box width), y0 / y1 (rear / front edge). The two boxes share the width between the
    centre box and the side wall, split by one wall thickness."""
    x0, x1 = COL_R + SKIN, CH_IN_X - SKIN
    return x0, (x1 - x0 - CH_WALL) / 2, WALL_IN_REAR + POCKET_SKIN, STOP_BACK_Y - POCKET_SKIN


def rear_pad():
    """Boss-Extrude10 + Fillet20: the deck is half a skin thicker behind the stop wall, from the web's outer skin out to the side wall. R = skin on
    the pad's free front corner (convex) and in the concave corner where its web side meets the rear wall."""
    x0, w, _, _ = _rear_layout()
    xp, z0, z1 = x0 + w + SKIN, DECK - SKIN / 2, DECK + OVER
    with BuildSketch() as sk:
        with Locations((xp, WALL_IN_REAR - OVER)):
            Rectangle(CH_IN_X + OVER - xp, STOP_BACK_Y - WALL_IN_REAR + OVER, align=(Align.MIN, Align.MIN))
        fillet([v for v in sk.vertices() if abs(v.X - xp) < OVER and abs(v.Y - STOP_BACK_Y) < OVER], SKIN)
    return [prism(g, z0, z1) for g in (sk, concave_filler((xp, WALL_IN_REAR), (-1, 1), SKIN))]


def rear_pockets():
    """Rear boxes cut through the deck and its pad (one skin deep below the pad, so they start at the pad underside); the centre box is as wide as the boss."""
    x0, w, y0, y1 = _rear_layout()
    with BuildSketch() as sk:
        for x in (x0, x0 + w + CH_WALL):
            with Locations((x, y0)):
                Rectangle(w, y1 - y0, align=(Align.MIN, Align.MIN))
        fillet(sk.vertices(), REAR_R)
    with BuildSketch() as ck:
        with Locations((0, CENTRE_Y0)):
            Rectangle(2 * COL_R, y1 - CENTRE_Y0, align=(Align.CENTER, Align.MIN))
        fillet(ck.vertices(), REAR_R)
        for bx, by in INS_AXIS:                        # the boss collar (column + one skin) stands in the deck: the pocket wraps round it
            with Locations((bx, by)):
                Circle(COL_R + SKIN, mode=Mode.SUBTRACT)
    return _cut(sk), _cut(ck)


def deck_pockets():
    rear, centre = rear_pockets()
    return x_pockets() + [centre] + [mirrored(h) for h in (side_pocket(), rear)]
