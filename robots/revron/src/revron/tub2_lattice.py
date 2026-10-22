"""[tub2] Rear-wall lightening: one X-braced window per side, four pockets (two side triangles, two caps) between the brace ribs.
Window = the rear wall between the rear boss collar and the side wall, skin above the floor and below the deck; ribs are two wall-thick
diagonals crossing at the window centre; the cap pockets stop at the corner posts. Cut from the inside, plan corners and floor R1 = the pocket depth (Fillet19), so the corners are spheres."""
from math import atan2, degrees, hypot
from build123d import Align, Axis, BuildSketch, Locations, Mode, Plane, Pos, Rectangle, Box, extrude, fillet
from .tub2_util import round_floor_pocket
from .tub2_params import CH_Y0, CH_Z0, CH_Z1, CH_WALL, CH_IN_X, COL_R, SKIN, WALL_IN_REAR, OVER

X0, X1 = COL_R + CH_WALL, CH_IN_X - SKIN              # window sides: rear boss collar .. side wall less skin
Z0, Z1 = CH_Z0 + CH_WALL + SKIN, CH_Z1 - CH_WALL - SKIN  # window floor / roof: wall + skin in from the chassis faces
XC, ZC = (X0 + X1) / 2, (Z0 + Z1) / 2                  # crossing point of the braces
RIB_W = CH_WALL                                        # brace thickness = wall
RIB_END = CH_Z0 + 5 * SKIN / 2                         # a brace's centreline meets the window side this high (Z)
CAP_HALF = 5 * CH_WALL / 2                             # cap pockets stop this far either side of the crossing (corner posts beyond)
FLOOR_R = SKIN                                         # floor round = plan corner round = pocket depth (corner spheres)
FLOOR_Y = CH_Y0 + SKIN                                 # pocket floor leaves one skin on the outside
TOP_Y = WALL_IN_REAR + SKIN                            # cutter runs a skin past the inner face


def _pockets_2d():
    """Window less the two braces: 4 faces, in sketch (X, Z) on the default plane."""
    angle = degrees(atan2(ZC - RIB_END, XC - X0))
    with BuildSketch() as sk:
        with Locations((XC, ZC)):
            Rectangle(X1 - X0, Z1 - Z0)
        for a in (angle, -angle):
            with Locations((XC, ZC)):
                Rectangle(2 * hypot(X1 - X0, Z1 - Z0), RIB_W, rotation=a, mode=Mode.SUBTRACT)
    return sk.sketch


def pockets():
    """+X cutters. Faces centred on the crossing in X are the caps and are clipped to the corner posts."""
    out = []
    post = Pos(XC, ZC) * Rectangle(2 * CAP_HALF, Z1 - Z0 + 2 * OVER)       # between the corner posts
    for f in _pockets_2d().faces():
        if abs(f.center().X - XC) < SKIN:                  # caps: stopped at the corner posts in plan, before the round, so the stop wall meets the ribs in the pocket's own R
            f = (f & post).faces()[0]
        out.append(round_floor_pocket(f, FLOOR_Y, TOP_Y, FLOOR_R))
    return out
