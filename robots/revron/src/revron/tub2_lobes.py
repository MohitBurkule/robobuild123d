"""[tub2] Side nut lobe (Boss-Extrude6 + Fillet3/Fillet8 root R2) and what mates with it: the captive M3 nut bore and hex pocket, the
N10 keyhole (hull of two circles, opened into a U-slot to the floor so the gearbox boss drops in from below), the snap slit. Built for +X, mirrored."""
from build123d import Box, BuildSketch, Circle, Cylinder, Locations, Mode, Plane, Pos, Align, RegularPolygon, Polygon, Rectangle, Rotation, extrude, fillet, make_hull
from .tub2_params import CH_HALF_W, CH_IN_X, CH_Z0, CH_WALL, OVER, SKIN
from math import atan2, degrees, hypot
from .params_chassis import NUT, RY, RZ, variant
from .tub2_arcs import inset_line, line_meet, outer_tangents
from .params_hardware import PRESS

LOBE_R = 4.5                         # D10: lobe round about the nut (diameter 9)
CAP_R, CAP_REACH = 2.0, (12.0, -1.58)  # R of the hull's end cap towards the middle and its centre's (Y, Z) offset from the nut
LOBE_PROUD = 3.0                     # Boss-Extrude6 depth
HEX_CLR = 0.05                       # drawn pocket: clearance each side of the nut's flats
NUT_AF = 5.5                         # M3 thin nut across flats; pocket circumradius = AF / sqrt(3)
BORE_R = 1.6                         # D7: 3.2 clearance bore
SEAT_R, NECK_R, NECK_DZ = 2.5, SKIN, 5.0   # keyhole: boss seat round at the shaft, neck round centred NECK_DZ below it
BOSS_R, BOSS_CLR = 2.0, 0.05        # 4 dia gearbox boss and its slot clearance each side: U-slot half width = sum
SLIT_R, SLIT_INSET = 0.5, 2.413   # slit corner R; slit walls sit this far inside the lobe's tangent lines (leaves the snap-in wall)
LOBE_OUT = CH_HALF_W + LOBE_PROUD
CAP_AT = (NUT[0] + CAP_REACH[0], NUT[1] + CAP_REACH[1])


def _yz(x0):
    """YZ sketch plane (sketch x = world Y, y = world Z) at world X = x0, normal +X."""
    return Plane.YZ.offset(x0)


def lobe():
    """Hull of the nut round and the end cap, standing LOBE_PROUD proud of the wall's outer face."""
    with BuildSketch(_yz(CH_HALF_W - OVER)) as sk:
        with Locations(NUT):
            Circle(LOBE_R)
        with Locations(CAP_AT):
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
        if variant("open_keyhole"):   # variant: U-slot from the seat down through the floor
            with Locations((RY, (RZ + CH_Z0 - 2 * OVER) / 2)):
                Rectangle(2 * (BOSS_R + BOSS_CLR), RZ - CH_Z0 + 2 * OVER)
    return extrude(sk.sketch, CH_WALL + 2 * OVER)


def nut_bore():
    """Clearance bore through wall and lobe (a cylinder along X at the nut)."""
    return Pos(CH_IN_X - OVER, *NUT) * Rotation(0, 90, 0) * Cylinder(BORE_R, LOBE_OUT - CH_IN_X + 2 * OVER, align=(Align.CENTER, Align.CENTER, Align.MIN))


def hex_pocket():
    """Hex pocket for the thin nut through the wall (Cut-Extrude6): nut AF plus clearance each side, flats parallel to the lobe's upper
    tangent line. Variant nut_press: a hair under the nut instead, so it is pressed in and cannot shift."""
    af = NUT_AF + (-PRESS["nut"] if variant("nut_press") else 2 * HEX_CLR)
    upper = max(outer_tangents(NUT, LOBE_R, CAP_AT, CAP_R), key=lambda t: t[0][1])
    tilt = degrees(atan2(upper[1][1] - upper[0][1], upper[1][0] - upper[0][0]))
    with BuildSketch(_yz(CH_IN_X - OVER)) as sk:
        with Locations(NUT):
            RegularPolygon(af / 3 ** 0.5, 6, rotation=tilt)
    return extrude(sk.sketch, CH_WALL + OVER)


def slit():
    """Snap-in relief (Fillet7 R0.5): the wedge between the lobe's two tangent lines moved SLIT_INSET inward, outside the nut round; its
    corners are rounded."""
    lines = [inset_line(t, NUT, SLIT_INSET) for t in outer_tangents(NUT, LOBE_R, CAP_AT, CAP_R)]
    apex = line_meet(*lines)
    reach = hypot(NUT[0] - apex[0], NUT[1] - apex[1])                  # the wedge opens toward the nut and runs out past it
    ends = [(apex[0] - reach * d[0], apex[1] - reach * d[1]) for _, d in lines]
    with BuildSketch(_yz(CH_HALF_W)) as sk:
        Polygon(apex, *ends, align=None)
        with Locations(NUT):
            Circle(LOBE_R, mode=Mode.SUBTRACT)
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
