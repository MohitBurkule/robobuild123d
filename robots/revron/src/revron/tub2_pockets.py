"""[tub2] Deck lightening pockets (cut from below, SKIN left): two X pockets on the axis, two side pockets between their diagonals,
the centre rear box and two side rear boxes between the stop walls. Side and rear pockets are built on +X and mirrored."""
from build123d import Align, BuildSketch, Locations, Polygon, Rectangle, fillet
from .tub2_params import (POCKET_X, UP_APEX, LO_APEX, DIAG_K, RIB_V, CENTRE_Y0, SKIN, CH_WALL, CH_IN_X, COL_R, DECK,
                          WALL_IN_FRONT, WALL_IN_REAR, STOP_BACK_Y, STOP_FRONT_Y)
from .tub2_util import prism, mirrored

APEX_R = CH_WALL                          # round at the pocket tips on the axis and at the side-pocket tip
REAR_FRONT_Y = STOP_BACK_Y - SKIN         # rear boxes stop a skin short of the stop wall


def _cut(sk):
    return prism(sk, DECK - SKIN, DECK + SKIN)


def _round(sk, tips=()):
    """Corner rounds: SKIN everywhere, APEX_R at the vertices listed in `tips` (x, y)."""
    near = lambda v: any(abs(v.X - x) + abs(v.Y - y) < SKIN / 10 for x, y in tips)
    fillet([v for v in sk.vertices() if not near(v)], SKIN / 2)   # short front edge: half-skin rounds
    fillet([v for v in sk.vertices() if near(v)], APEX_R)
    return sk


def x_pockets():
    """Two triangles-with-box on the axis: front pocket opens toward the front wall, rear toward the stop wall front face; shared diagonal slope."""
    x, k = POCKET_X, DIAG_K
    front_y = WALL_IN_FRONT - SKIN
    with BuildSketch() as up:
        Polygon((0, UP_APEX), (x, UP_APEX + k * x), (x, front_y), (-x, front_y), (-x, UP_APEX + k * x), align=None)
    with BuildSketch() as lo:
        Polygon((0, LO_APEX), (x, LO_APEX - k * x), (x, STOP_FRONT_Y), (-x, STOP_FRONT_Y), (-x, LO_APEX - k * x), align=None)
    return [_cut(_round(up, [(0, UP_APEX)])), _cut(_round(lo, [(0, LO_APEX)]))]


def side_pockets():
    """+X triangle between the two X-pocket diagonals (each RIB_V below/above them); the tip is where the two diagonals meet."""
    k, x = DIAG_K, POCKET_X
    up_y = lambda u: UP_APEX - RIB_V + k * u
    lo_y = lambda u: LO_APEX + RIB_V - k * u
    tip = (LO_APEX - UP_APEX + 2 * RIB_V) / (2 * k)
    with BuildSketch() as sk:
        Polygon((tip, up_y(tip)), (x, up_y(x)), (x, lo_y(x)), align=None)
    fillet(sk.vertices(), APEX_R)
    return [_cut(sk)]


def rear_pockets():
    """+X rear boxes: the centre box is as wide as the rear boss; two side boxes share the remaining width, separated by one wall thickness."""
    x0, x1 = COL_R + SKIN, CH_IN_X - SKIN
    w = (x1 - x0 - CH_WALL) / 2
    y0 = WALL_IN_REAR + SKIN
    out = []
    with BuildSketch() as sk:
        for x in (x0, x0 + w + CH_WALL):
            with Locations((x, y0)):
                Rectangle(w, REAR_FRONT_Y - y0, align=(Align.MIN, Align.MIN))
    fillet(sk.vertices(), SKIN)
    out.append(_cut(sk))
    with BuildSketch() as ck:
        with Locations((0, CENTRE_Y0)):
            Rectangle(2 * COL_R, REAR_FRONT_Y - CENTRE_Y0, align=(Align.CENTER, Align.MIN))
    fillet(ck.vertices(), SKIN)
    return out, _cut(ck)


def deck_pockets():
    sides = side_pockets()
    rear, centre = rear_pockets()
    half = sides + rear
    return x_pockets() + [centre] + [mirrored(h) for h in half]
