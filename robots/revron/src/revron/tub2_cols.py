"""[tub2] Insert columns: flared feet under the bolt pattern, the rear-centre boss with its R-skin fillet, and the heat-set bores."""
from build123d import Align, BuildPart, BuildSketch, Circle, Cone, Cylinder, Locations, Mode, Plane, Pos, Rectangle, extrude
from .tub2_params import (INS, INS_RIGHT, INS_AXIS, INS_Z, COL_R, FOOT_R, SKIN, BORE_R, BORE_CH, CH_Z0, CH_Z1, DECK, OVER,
                          WALL_IN_REAR, SEAT_Z)
from .tub2_util import box_xy, concave_filler, prism


def feet():
    """A foot cylinder under every column (+X pattern and the axis one), flaring 45 deg into the column radius."""
    foot_top, flare = INS_Z[0], FOOT_R - COL_R
    parts = []
    for x, y in INS_AXIS:   # only the rear-centre column stands free of a block; the corner columns sit inside theirs
        parts.append(Pos(x, y, CH_Z0) * Cylinder(FOOT_R, foot_top - CH_Z0, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        parts.append(Pos(x, y, foot_top - OVER) * Cone(FOOT_R, COL_R, flare + OVER, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return sum(parts[1:], parts[0])


def rear_boss():
    """Rear-centre boss: a column round whose flanks run straight (|x| = COL_R) back to the rear wall; the +X flank meets the wall in an R-skin fillet."""
    (bx, by), = INS_AXIS
    with BuildSketch() as sk:
        with Locations((bx, by)):
            Circle(COL_R)
    boss = prism(sk, CH_Z0, DECK + OVER)
    flank = box_xy(bx - COL_R, bx + COL_R, WALL_IN_REAR - OVER, by, CH_Z0, DECK + OVER)
    fil = prism(concave_filler((bx + COL_R, WALL_IN_REAR), (1, 1), SKIN), CH_Z0, DECK + OVER)
    return boss + flank + fil + fil.mirror(Plane.YZ)


def bores():
    """Heat-set bores through the whole column with a 45 deg chamfer at the base-panel seat and at the rim."""
    cutters = []
    for x, y in INS:
        cutters.append(Pos(x, y, CH_Z0 - OVER) * Cylinder(BORE_R, CH_Z1 - CH_Z0 + 2 * OVER, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        cutters.append(Pos(x, y, SEAT_Z) * Cone(BORE_R + BORE_CH, BORE_R, BORE_CH, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        cutters.append(Pos(x, y, CH_Z1) * Cone(BORE_R, BORE_R + BORE_CH, BORE_CH, align=(Align.CENTER, Align.CENTER, Align.MAX)))
    return sum(cutters[1:], cutters[0])
