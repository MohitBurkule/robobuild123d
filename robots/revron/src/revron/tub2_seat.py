"""[tub2] Base-panel seat: rabbet in the RV26 outline (rect, ears round the screws near the edge, R blends), N10 preload pad recess,
squared rear corner behind the gearbox plates, and the stop wall's lower inner edge round."""
from build123d import Align, Axis, BuildSketch, Circle, Locations, Mode, Plane, Rectangle, extrude, fillet
from .tub2_params import (PRELOAD_PAD, PAD_MARGIN, SEAT_Z, CH_Z0, CH_WALL,
                          CH_IN_X, WALL_IN_REAR, DECK, OVER, SA_X0, STOP_BACK_Y, STOP_FRONT_Y, STOP_ROUND_R, SKIN, PANEL_CLEARANCE)
from . import panel_base
from .tub2_util import box_xy, concave_filler, mirrored, prism


def rabbet():
    """The seat is the RV26 outline (panel_base.outline, the panel's own sketch) grown by the print clearance."""
    return panel_base.rabbet(PANEL_CLEARANCE, CH_Z0 - CH_WALL, SEAT_Z)


def pad_recess_and_corner():
    """+X: recess for the N10 preload pad (pad + margin each side) and the squared rear corner (wall thick, from the seat to the deck)."""
    (px, py), h = PRELOAD_PAD["c"], PRELOAD_PAD["s"] / 2 + PAD_MARGIN
    pad = box_xy(px - h, px + h, py - h, py + h, SEAT_Z - OVER, SEAT_Z + PAD_MARGIN)
    corner = box_xy(CH_IN_X - CH_WALL, CH_IN_X + OVER, WALL_IN_REAR, WALL_IN_REAR + CH_WALL, SEAT_Z, DECK)
    return [pad, corner]


def stop_wall_round():
    """+X: the lower inner edge of the stop wall is rounded R: a quarter-round cutter (square minus circle) run along the wall's Y span."""
    z1 = SEAT_Z + STOP_ROUND_R
    with BuildSketch(Plane.XZ.offset(-(STOP_BACK_Y + STOP_ROUND_R))) as sk:
        with Locations((SA_X0, SEAT_Z - OVER)):
            Rectangle(STOP_ROUND_R, z1 - SEAT_Z + OVER, align=(Align.MIN, Align.MIN))
        with Locations((SA_X0 + STOP_ROUND_R, z1)):
            Circle(STOP_ROUND_R, mode=Mode.SUBTRACT)
    return extrude(sk.sketch, STOP_ROUND_R + OVER)   # runs R along Y from the stop wall back face


def seat_cuts():
    return [rabbet()] + [mirrored(c) for c in pad_recess_and_corner() + [stop_wall_round()]]
