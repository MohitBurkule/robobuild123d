"""[tub2] Side nut lobe (Boss-Extrude6 + Fillet3/Fillet8 root R2) and what mates with it: the captive M3 nut bore and hex pocket, the
N10 keyhole (hull of two circles, opened into a U-slot to the floor so the gearbox boss drops in from below), the snap slit. Built for +X, mirrored."""
from build123d import Box, BuildSketch, Circle, Cylinder, Locations, Mode, Plane, Pos, Align, RegularPolygon, Polygon, Rectangle, Rotation, extrude, fillet, make_hull
from .tub2_params import CH_HALF_W, CH_IN_X, CH_Z0, CH_WALL, OVER, SKIN
from .params_chassis import NUT, RY, RZ
from .params_hardware import PRESS

LOBE_R = 4.5                         # D10: lobe round about the nut (diameter 9)
LOBE_CAP, CAP_R = (0.5, 6.9), 2.0    # (Y, Z) and R of the hull's end cap towards the middle
LOBE_PROUD = 3.0                     # Boss-Extrude6 depth
NUT_AF = 5.5                         # M3 thin nut across flats; pocket circumradius = AF / sqrt(3)
BORE_R = 1.6                         # D7: 3.2 clearance bore
SEAT_R, NECK_R, NECK_DZ = 2.5, SKIN, 5.0   # keyhole: boss seat round at the shaft, neck round centred NECK_DZ below it
BOSS_R, BOSS_CLR = 2.0, 0.05        # 4 dia gearbox boss and its slot clearance each side: U-slot half width = sum
SLIT = ((-7.14, 6.85), (-3.45, 7.05), (-3.45, 7.95), (-6.9, 8.9))   # snap-in relief wedge in the lobe (Y, Z), R0.5 corners
SLIT_R = 0.5
LOBE_OUT = CH_HALF_W + LOBE_PROUD


def _yz(x0):
    """YZ sketch plane (sketch x = world Y, y = world Z) at world X = x0, normal +X."""
    return Plane.YZ.offset(x0)


def lobe():
    """Hull of the nut round and the end cap, standing LOBE_PROUD proud of the wall's outer face."""
    with BuildSketch(_yz(CH_HALF_W - OVER)) as sk:
        with Locations(NUT):
            Circle(LOBE_R)
        with Locations(LOBE_CAP):
            Circle(CAP_R)
        make_hull()
    return extrude(sk.sketch, LOBE_PROUD + OVER)


def bounds():
    bb = lobe().bounding_box()
    return bb.min.Y, bb.min.Z, bb.max.Y, bb.max.Z


def keyhole():
    """Tapered seat for the gearbox shaft boss through the wall: hull of the seat round and the neck round."""
    with BuildSketch(_yz(CH_IN_X - OVER)) as sk:
        with Locations((RY, RZ)):
            Circle(SEAT_R)
        with Locations((RY, RZ - NECK_DZ)):
            Circle(NECK_R)
        make_hull()
        with Locations((RY, (RZ + CH_Z0 - 2 * OVER) / 2)):
            Rectangle(2 * (BOSS_R + BOSS_CLR), RZ - CH_Z0 + 2 * OVER)   # U-slot from the seat down through the floor
    return extrude(sk.sketch, CH_WALL + 2 * OVER)


def nut_bore():
    """Clearance bore through wall and lobe (a cylinder along X at the nut)."""
    return Pos(CH_IN_X - OVER, *NUT) * Rotation(0, 90, 0) * Cylinder(BORE_R, LOBE_OUT - CH_IN_X + 2 * OVER, align=(Align.CENTER, Align.CENTER, Align.MIN))


def hex_pocket():
    """Hex pocket for the thin nut through the wall thickness; corners point up and down (flats parallel to Z)."""
    with BuildSketch(_yz(CH_IN_X - OVER)) as sk:
        with Locations(NUT):
            RegularPolygon(NUT_AF / 3 ** 0.5 - PRESS["nut"], 6, rotation=30)   # pocket corners under the nut's: it is pressed in, so it cannot shift or turn
    return extrude(sk.sketch, CH_WALL + OVER)


def slit():
    with BuildSketch(_yz(CH_HALF_W)) as sk:
        Polygon(*SLIT, align=None)
        fillet(sk.vertices(), SLIT_R)
    return extrude(sk.sketch, LOBE_PROUD + OVER)


def floor_relief():
    """The root fillet must not hang below the floor: cut a slab under the chassis floor along the lobe."""
    y0, _, y1, _ = bounds()
    m = CH_WALL + OVER
    return Pos((CH_HALF_W + LOBE_OUT) / 2 - OVER, (y0 + y1) / 2, CH_Z0 - 3 * SKIN / 2) * \
        Box(LOBE_OUT - CH_HALF_W + SKIN, y1 - y0 + 2 * m, 3 * SKIN)


def additions():
    return [lobe(), lobe().mirror(Plane.YZ)]


def cuts():
    half = [keyhole(), nut_bore(), hex_pocket(), slit(), floor_relief()]
    return half + [h.mirror(Plane.YZ) for h in half]
