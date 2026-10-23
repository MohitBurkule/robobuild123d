"""[tub2] Insert columns: the rear-centre boss with its R-skin fillet, and the heat-set bores."""
from build123d import Align, BuildSketch, Circle, Cone, Cylinder, Locations, Plane, Pos
from .tub2_params import (INS, INS_AXIS, TOP_XY, TOP_SCREW_WEB, TOP_NECK, TOP_PILOT_R, COL_R, SKIN, BORE_R, BORE_CH, CH_Z0, CH_Z1, DECK, OVER,
                          WALL_IN_REAR, SEAT_Z, BOSS_AT_REAR, FLANK_X, STOP_X)
from .tub2_util import box_xy, concave_filler, prism


def rear_boss():
    """Rear-centre boss: a column round whose flanks run straight (|x| = COL_R) back to the rear wall; the +X flank meets the wall in an R-skin fillet."""
    (bx, by), = INS_AXIS
    with BuildSketch() as sk:
        with Locations((bx, by)):
            Circle(COL_R)
    boss = prism(sk, CH_Z0, DECK + OVER)
    if not BOSS_AT_REAR:                       # moved out in front of the gearmotor (params_chassis.BOSS_Y): a free-standing column, no flanks back to the wall
        if STOP_X > OVER:                      # the motors' inner ends stand off the axis: a block as wide as the gap they leave (the round column no longer reaches them) keeps them from sliding in
            boss += box_xy(bx - STOP_X, bx + STOP_X, WALL_IN_REAR - OVER, by, CH_Z0, DECK + OVER)
        return boss
    flank = box_xy(bx - COL_R, bx + COL_R, WALL_IN_REAR - OVER, by, CH_Z0, DECK + OVER)
    if FLANK_X > COL_R:                        # a wider chassis moves the gearmotor out of the round column's reach: a stop block as wide as the motor has moved stands in for it
        flank += box_xy(bx - FLANK_X, bx + FLANK_X, WALL_IN_REAR - OVER, by + COL_R, CH_Z0, DECK + OVER)
    fil = prism(concave_filler((bx + COL_R, WALL_IN_REAR), (1, 1), SKIN), CH_Z0, DECK + OVER)
    return boss + flank + fil + fil.mirror(Plane.YZ)


def bores():
    """Heat-set bores through the column with a 45 deg chamfer at the base-panel seat and at the rim. The four corner columns the Ti top
    panel screws into keep a TOP_NECK web under the rim instead (tap-drill pilot through it): the panel's d2.8 holes sit over these columns in the STEP."""
    cutters = []
    for x, y in INS:
        top_screw = TOP_SCREW_WEB and (x, y) in TOP_XY
        z_end = CH_Z1 - TOP_NECK if top_screw else CH_Z1
        cutters.append(Pos(x, y, CH_Z0 - OVER) * Cylinder(BORE_R, z_end - CH_Z0 + OVER, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        cutters.append(Pos(x, y, SEAT_Z) * Cone(BORE_R + BORE_CH, BORE_R, BORE_CH, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        if top_screw:
            cutters.append(Pos(x, y, z_end - OVER) * Cylinder(TOP_PILOT_R, TOP_NECK + 2 * OVER, align=(Align.CENTER, Align.CENTER, Align.MIN)))
        else:
            cutters.append(Pos(x, y, CH_Z1) * Cone(BORE_R, BORE_R + BORE_CH, BORE_CH, align=(Align.CENTER, Align.CENTER, Align.MAX)))
    return sum(cutters[1:], cutters[0])
