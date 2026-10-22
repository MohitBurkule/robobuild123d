"""[tub2] Weapon-mount tab on the front wall (Boss-Extrude4/5, Fillet21 R2, Cut-Extrude key hole): the tab wall (profile under the lug's top
line, clear of the weapon rotor circle), the key tab keyed into the mount's notch, the R2 blend into the front wall, the rabbet under the
tab and the square key hole. Built for +X and mirrored."""
from build123d import Align, BuildSketch, Circle, Locations, Mode, Plane, Polygon, Rectangle, chamfer, extrude, fillet
from .params_chassis import MNT_IN, SA_X0, SB_X0, WY, WZ
from .params_weapon import WEAPON_CLEAR_R
from .tub2_params import CH_Y1, CH_Z0, CH_Z1, CH_WALL, SKIN, OVER, WALL_IN_FRONT, DECK, SEAT_Z
from .tub2_lug import top_line_slope
from .tub2_util import box_xy, concave_filler, prism

TAB_FRONT = 26.5                                  # tab front face (Y); also the slot's reach
TAB_WALL_T = 3 * SKIN                             # tab wall thickness
TAB_GAP = SKIN / 10                               # tab wall stops this short of the mount's inner face
WALL_X = (MNT_IN - TAB_GAP - TAB_WALL_T, MNT_IN - TAB_GAP)   # tab wall X span (inboard of the mount)
KEY_Y0, KEY_Z0, KEY_Z1 = 18.5, 5.4, 13.5          # key tab octagon (Y0 .. TAB_FRONT, Z0 .. Z1), chamfer SKIN
KEY_X = (MNT_IN - 2 * TAB_GAP, SA_X0 + OVER)      # key tab runs from the mount's notch into the lug
KEY_WALL, KEY_R = 3 * SKIN / 2, SKIN                # wall left round the key hole; its corner R (Fillet4)


def tab_wall_sketch(plane):
    """Tab wall profile: block under the lug's top line, chamfered at the front floor corner, clear of the rotor circle."""
    s = top_line_slope()
    z_at = lambda y: CH_Z1 + s * (y - CH_Y1)
    with BuildSketch(plane) as sk:
        with Locations((WALL_IN_FRONT, CH_Z0)):
            Rectangle(TAB_FRONT - WALL_IN_FRONT, CH_Z1 - CH_Z0, align=(Align.MIN, Align.MIN))
        Polygon((CH_Y1, CH_Z1), (TAB_FRONT, z_at(TAB_FRONT)), (TAB_FRONT, CH_Z1 + 1), (CH_Y1, CH_Z1 + 1), mode=Mode.SUBTRACT, align=None)
        with Locations((WY, WZ)):
            Circle(WEAPON_CLEAR_R, mode=Mode.SUBTRACT)
        chamfer([v for v in sk.vertices() if abs(v.X - TAB_FRONT) < OVER and abs(v.Y - CH_Z0) < OVER], SKIN)
    return sk


def tab_wall():
    return extrude(tab_wall_sketch(Plane.YZ.offset(WALL_X[0])).sketch, TAB_WALL_T)


def key_sketch(plane, inset=0.0):
    with BuildSketch(plane) as sk:
        with Locations((KEY_Y0 + inset, KEY_Z0 + inset)):
            Rectangle(TAB_FRONT - KEY_Y0 - 2 * inset, KEY_Z1 - KEY_Z0 - 2 * inset, align=(Align.MIN, Align.MIN))
        if inset:
            fillet(sk.vertices(), KEY_R)
        else:
            chamfer(sk.vertices(), SKIN)
    return sk


def key_tab():
    return extrude(key_sketch(Plane.YZ.offset(KEY_X[0])).sketch, KEY_X[1] - KEY_X[0])


def key_hole():
    """Square hole (the key inset by the wall) through tab wall, key tab and lug."""
    x0 = WALL_X[0] - SKIN / 3
    return extrude(key_sketch(Plane.YZ.offset(x0), KEY_WALL).sketch, SB_X0 + SKIN / 2 - x0)


def wall_blend():
    """Concave R = wall blend between the tab wall's inner face and the front wall's outer face."""
    return prism(concave_filler((WALL_X[0], CH_Y1), (-1, 1), CH_WALL), CH_Z0, DECK)


def rabbet():
    """The front wall stops at the base-panel rabbet under the key tab (from the tab wall to the lug)."""
    return box_xy(WALL_X[1], SA_X0, WALL_IN_FRONT - SKIN, CH_Y1 + OVER, CH_Z0 - OVER, SEAT_Z)
