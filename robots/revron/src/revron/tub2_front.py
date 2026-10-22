"""[tub2] Front wall: the weapon-wire slot (Cut-Extrude7 + Fillet10) and the two lightening pockets either side of its rib frame
(Cut-Extrude + Fillet22 R0.8 on every pocket edge but the open one). Wall thickness, axle height and ribs are shared masters."""
from build123d import Axis, BuildSketch, Box, Locations, Plane, Pos, Rectangle, extrude, fillet
from .tub2_util import round_floor_pocket
from .tub2_params import CH_WALL, SKIN, OVER, WALL_IN_FRONT
from .params_chassis import RZ

WIRE_X, WIRE_W, WIRE_H = 8.75, 3.0, 12.0       # Sketch16: slot width 3 and height 12 about the axle height; centre X
WIRE_RIB = CH_WALL + SKIN                      # rib frame round the slot (3)
POCKET_HALF_X = 18.25                          # pockets stop here either side of the axis (just inside the lug faces)
POCKET_H = 9.0                                 # pocket height about the axle height
POCKET_R = 0.8                                 # Fillet22: corner round = floor round ...
POCKET_DEPTH = POCKET_R                        # ... = depth sunk into the wall from its inner face, so the floor corners are spheres
TAB_FRONT = 26.5                               # the slot runs on through the weapon tab


def wire_slot():
    """Obround slot through the front wall and the tab (R = half the width)."""
    with BuildSketch(_xz()) as sk:
        with Locations((WIRE_X, RZ)):
            Rectangle(WIRE_W, WIRE_H)
        fillet(sk.vertices(), WIRE_W / 2)
    return extrude(sk.sketch, -(TAB_FRONT - WALL_IN_FRONT + SKIN))   # XZ plane normal is -Y: negative amount runs toward the front


def _xz():
    return Plane.XZ.offset(-(WALL_IN_FRONT - SKIN))


def _pocket(x0, x1):
    """Pocket cutter (X x Z rectangle): plan corners, floor edges and depth all R (corner spheres)."""
    with BuildSketch() as sk:
        with Locations(((x0 + x1) / 2, RZ)):
            Rectangle(x1 - x0, POCKET_H)
    return round_floor_pocket(sk.sketch.faces()[0], WALL_IN_FRONT + POCKET_DEPTH, WALL_IN_FRONT - SKIN, POCKET_R)


def wall_pockets():
    """One pocket from the -X end to the rib frame, one from the frame to +X end; the frame is the slot plus a rib each side."""
    f0, f1 = WIRE_X - WIRE_W / 2 - WIRE_RIB, WIRE_X + WIRE_W / 2 + WIRE_RIB
    return [_pocket(-POCKET_HALF_X, f0), _pocket(f1, POCKET_HALF_X)]
