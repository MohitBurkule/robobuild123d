"""Side_Panel_alt_sm (TPU): a plate screwed to the chassis side boss, a battered skin outside the rear wheel, a rear
crossbar whose finger sits beside the outer chassis tab on the cross bolt, and a fork prong running forward past the
weapon to the floor. Right-hand part in the STEP frame; the left panel is its mirror."""
import math

from shapely.geometry import Polygon, box as sbox

from robocad.geom import _box, _cyl, _U, _S, _ext, _mirror_x, _solid
from .params_chassis import AXLE_Z, BOSS_PITCH, HOLE_D, TAB_HOLE_Z, TAB_HOLE_DY, HY, HX, TAB_X_OUT, HEX, HEX_PHASE, M3 as NUT_D
from .params_side import *  # noqa: F401,F403


def _yz_prism(pts, x0, x1):
    """Polygon in (y, z) extruded along X from x0 to x1."""
    return _ext(Polygon(pts), "yz", x0, x1)


def _xz_prism(pts, y0, y1):
    """Polygon in (x, z) extruded along Y from y0 to y1."""
    s = _ext(Polygon(pts), "xz", 0, y1 - y0)
    return s.moved(__import__("build123d").Location((0, y0, 0)))


def plate():
    return _box(*PLATE_X, -PLATE_Y, PLATE_Y, *PLATE_Z)


def skin_x(z, outer=False):
    """X of the skin's inner (or outer) face at height z: it leans out SKIN_BATTER from SKIN_TOP."""
    x = SKIN_TOP[0] + (SKIN_TOP[1] - z) * math.tan(math.radians(SKIN_BATTER))
    return x + (SP_T / math.cos(math.radians(SKIN_BATTER)) if outer else 0)


def skin():
    """Battered outer wall outside the rear wheel, SP_T thick."""
    z0, z1 = SKIN_BOT_Z, SKIN_TOP[1]
    return _xz_prism([(skin_x(z1), z1), (skin_x(z1, True), z1), (skin_x(z0, True), z0), (skin_x(z0), z0)], *SKIN_Y)


def front_wall():
    """Strut from the plate out to the skin just ahead of the tyre."""
    return _box(PLATE_X[0], skin_x(SKIN_TOP[1], True), *STRUT_Y, PLATE_Z[0], SKIN_TOP[1])


def crossbar():
    """Rear crossbar from the outer chassis tab's face out to the skin's outer face, behind the rear tyre."""
    return _box(TAB_X_OUT, skin_x(CROSS_Z[0], True), *CROSS_Y, *CROSS_Z)


def fork():
    """Fork prong: from the crossbar top, falling to its floor run at FORK_KNEE_Y, out to the tip."""
    y0 = CROSS_Y[1] - SP_T
    bot = FLOOR_Z + FLOOR_CLR
    return _yz_prism([(y0, 0), (y0, CROSS_TOP), (FORK_TIP_Y, bot + FORK_TIP_T), (FORK_TIP_Y, bot), (FORK_KNEE_Y, bot)], *FORK_X)


def cuts():
    """Head-side holes of the right pod (fasteners table): the two countersunk boss screws and the cross bolt."""
    from .fasteners import cutters
    from robot.cad import fastener_catalog as fc
    y, z = HY + TAB_HOLE_DY, TAB_HOLE_Z
    m = fc.nut(NUT_D, "thin")[1]
    pts = [(y + NUT_R * math.cos(math.radians(a)), z + NUT_R * math.sin(math.radians(a))) for a in range(HEX_PHASE, 360, 360 // HEX)]
    entry = sbox(CROSS_Y[0] - 1, z - NUT_R * math.sqrt(3) / 2, y, z + NUT_R * math.sqrt(3) / 2)   # nut slides in from the front (the tyre gap)
    hexa = _ext(Polygon(pts).union(entry), "yz", TAB_X_OUT - 1, TAB_X_OUT + m)
    bolt = _cyl(HOLE_D / 2, TAB_X_OUT - 1, TAB_X_OUT + CROSS_LAND + 1, (y, z), "x")
    return _U(cutters("side_r"), hexa, bolt)   # cross-bolt nut captive in the land, against the outer tab


def side_panel(side=1):
    s = _solid(_S(_U(plate(), skin(), front_wall(), crossbar(), fork()), cuts()))
    return s if side > 0 else _solid(_mirror_x(s))


def side_panel_r():
    return side_panel(1)
