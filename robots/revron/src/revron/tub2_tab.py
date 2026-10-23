"""[tub2] Weapon-mount tab on the front wall (Boss-Extrude4/5, Fillet21 R2, Cut-Extrude key hole): the tab wall (profile under the lug's top
line, clear of the weapon rotor circle), the key tab keyed into the mount's notch, the R2 blend into the front wall, the rabbet under the
tab and the square key hole. Built for +X and mirrored."""
from build123d import Align, BuildSketch, Locations, Mode, Plane, Polygon, Rectangle, chamfer, extrude, fillet
from .params_chassis import SA_X0, SB_X0
from .tub2_iface import TAB, HAS_TAB, MOUNT_IN as MNT_IN, SPIDER_OUT, SPIDER_GAP
from .tub2_params import CH_Y1, CH_Z0, CH_Z1, CH_WALL, SKIN, OVER, WALL_IN_FRONT, DECK, SEAT_Z
from .tub2_lug import top_line_slope
from .tub2_util import box_xy, concave_filler, fit_radius, prism

TAB_FRONT = TAB['y1'] if HAS_TAB else None                             # tab front face (Y); also the slot's reach
TAB_WALL_NOM = 3 * SKIN                           # nominal tab wall thickness
TAB_GAP = SKIN / 10                               # tab wall stops this short of the mount's inner face
# the wall's inner face follows the spider seat: nominal thickness, or (a spider nearer the mount, e.g. a longer-bell motor) as thin as keeps SPIDER_GAP to its outer face
WALL_X1 = MNT_IN - TAB_GAP
WALL_X0 = round(max(WALL_X1 - TAB_WALL_NOM, SPIDER_OUT + SPIDER_GAP) if SPIDER_OUT is not None else WALL_X1 - TAB_WALL_NOM, 6)
WALL_X = (WALL_X0, round(WALL_X1, 6))           # tab wall X span (inboard of the mount)
TAB_WALL_T = WALL_X[1] - WALL_X[0]                # actual thickness
if HAS_TAB and TAB_WALL_T < SKIN:
    raise ValueError(f"tub tab wall {TAB_WALL_T:.2f} mm thick: the spider seat (outer face |X| {SPIDER_OUT:g}) leaves no room for a wall inboard of the mount (|X| {MNT_IN:g})")
KEY_CLR = 0.05                                   # key tab to the mount notch
KEY_LEN = 8.0                                     # key tab octagon: this long back from TAB_FRONT (STEP 18.5 to 26.5), chamfer SKIN
KEY_Y0 = TAB_FRONT - KEY_LEN if HAS_TAB else None                      # so the key rides the tab front when the tab follows the axle standoff
KEY_Z0, KEY_Z1 = (TAB['z0'] + KEY_CLR, TAB['z0'] + TAB['h'] - KEY_CLR) if HAS_TAB else (None, None)   # between the mount notch's floor and roof (Z)
KEY_X = (MNT_IN - 2 * TAB_GAP, SA_X0 + OVER)      # key tab runs from the mount's notch into the lug
# The STEP's tab wall is not symmetric: its front-top corner is bevelled one way on -X (45 deg) and another on +X (steeper plane, one tab chamfer lower
# on the front face). One shared base (the -X front point, the bevel meets the top line) plus the +X delta; the rotor circle is not drawn in the STEP.
BEVEL_Z = 13.35                                   # organic (STEP): height on the front face where the -X 45 deg bevel starts
BEVEL_DELTA = {'-x': (0.0, None), '+x': (TAB['cham'], 25.6)} if HAS_TAB else {}   # per side: (drop of the front point below BEVEL_Z, Y where the bevel meets the top line; None = 45 deg)
KEY_WALL, KEY_R = 3 * SKIN / 2, SKIN                # wall left round the key hole; its corner R (Fillet4)


def _bevel_pts(side):
    """Cutter polygon of the front-top bevel of the tab wall on `side` (sketch x = world Y, y = world Z)."""
    s = top_line_slope()
    drop, y_top = BEVEL_DELTA[side]
    zf = BEVEL_Z - drop
    yt = y_top if y_top is not None else (zf + TAB_FRONT - CH_Z1 + s * CH_Y1) / (1 + s)   # 45 deg bevel: z = zf + (TAB_FRONT - y) meets the top line
    return (yt, CH_Z1 + s * (yt - CH_Y1)), (TAB_FRONT, zf), (TAB_FRONT, CH_Z1 + 1), (yt, CH_Z1 + 1)


def tab_wall_sketch(plane, side='+x'):
    """Tab wall profile: block under the lug's top line, chamfered at the front floor corner, clear of the rotor circle."""
    s = top_line_slope()
    z_at = lambda y: CH_Z1 + s * (y - CH_Y1)
    with BuildSketch(plane) as sk:
        with Locations((WALL_IN_FRONT, CH_Z0)):
            Rectangle(TAB_FRONT - WALL_IN_FRONT, CH_Z1 - CH_Z0, align=(Align.MIN, Align.MIN))
        Polygon((CH_Y1, CH_Z1), (TAB_FRONT, z_at(TAB_FRONT)), (TAB_FRONT, CH_Z1 + 1), (CH_Y1, CH_Z1 + 1), mode=Mode.SUBTRACT, align=None)
        Polygon(*_bevel_pts(side), mode=Mode.SUBTRACT, align=None)
        chamfer([v for v in sk.vertices() if abs(v.X - TAB_FRONT) < OVER and abs(v.Y - CH_Z0) < OVER], SKIN)
    return sk


def tab_wall(side='+x'):
    if not HAS_TAB:
        return None
    return extrude(tab_wall_sketch(Plane.YZ.offset(WALL_X[0]), side).sketch, TAB_WALL_T)


def key_sketch(plane, inset=0.0, side=None):
    with BuildSketch(plane) as sk:
        with Locations((KEY_Y0 + inset, KEY_Z0 + inset)):
            Rectangle(TAB_FRONT - KEY_Y0 - 2 * inset, KEY_Z1 - KEY_Z0 - 2 * inset, align=(Align.MIN, Align.MIN))
        if inset:
            w, h = TAB_FRONT - KEY_Y0 - 2 * inset, KEY_Z1 - KEY_Z0 - 2 * inset
            fillet(sk.vertices(), fit_radius([(0, 0), (w, 0), (w, h), (0, h)], 0, KEY_R, rounded=(1, 2, 3)))   # R wall, or what the key hole's span allows
        else:
            chamfer(sk.vertices(), SKIN)
            if side == '+x':                                   # the STEP's key shares the +X wall's steeper front-top bevel plane (one face across wall and key)
                Polygon(*_bevel_pts(side), mode=Mode.SUBTRACT, align=None)
    return sk


def key_tab(side='+x'):
    if not HAS_TAB:
        return None
    return extrude(key_sketch(Plane.YZ.offset(KEY_X[0]), side=side).sketch, KEY_X[1] - KEY_X[0])


def key_hole():
    """Square hole (the key inset by the wall) through tab wall, key tab and lug."""
    if not HAS_TAB:
        return None
    x0 = WALL_X[0] - SKIN / 3
    return extrude(key_sketch(Plane.YZ.offset(x0), KEY_WALL).sketch, SB_X0 + SKIN / 2 - x0)


def wall_blend():
    """Concave R = wall blend between the tab wall's inner face and the front wall's outer face."""
    if not HAS_TAB:
        return None
    y1 = CH_Y1 + CH_WALL                                                   # the blend reaches one R in front of the front face
    cham_z = lambda y: CH_Z1 - (y - WALL_IN_FRONT)                         # the front wall's top-edge chamfer (CH_WALL, 45 deg, starts at the inner face) runs on under the blend
    with BuildSketch(Plane.YZ.offset(WALL_X[0] - CH_WALL - 1)) as under:
        Polygon((CH_Y1 - 1, CH_Z0), (y1, CH_Z0), (y1, cham_z(y1)), (CH_Y1 - 1, cham_z(CH_Y1 - 1)), align=None)
    return prism(concave_filler((WALL_X[0], CH_Y1), (-1, 1), CH_WALL), CH_Z0, DECK) & extrude(under.sketch, CH_WALL + 2)


def rabbet():
    """The front wall stops at the base-panel rabbet under the key tab (from the tab wall to the lug)."""
    if not HAS_TAB:
        return None
    return box_xy(WALL_X[1], SA_X0, WALL_IN_FRONT - SKIN, CH_Y1 + OVER, CH_Z0 - OVER, SEAT_Z)


def rub_point():
    """Where the spider sweeps closest to the -X tab wall: its inner face (x = -WALL_X[0]) at the point the 45 deg bevel leaves the top line. None without a tab."""
    if not HAS_TAB:
        return None
    s = top_line_slope()
    zf = BEVEL_Z - BEVEL_DELTA['-x'][0]
    y = (zf + TAB_FRONT - CH_Z1 + s * CH_Y1) / (1 + s)
    return (-WALL_X[0], y, CH_Z1 + s * (y - CH_Y1))
