"""[tub2] Boss-Extrude1 + Chamfer + Fillet3: the outer box (plan R = wall, top edge chamfer = wall) and the cavity up to the deck."""
from build123d import Align, Axis, BuildPart, BuildSketch, Locations, Plane, Rectangle, chamfer, extrude, fillet
from .tub2_params import CH_HALF_W, CH_Y0, CH_Y1, CH_Z0, CH_Z1, CH_IN_X, WALL_IN_REAR, WALL_IN_FRONT, DECK, CH_WALL, CAVITY_R

APEX_SHY = 0.005   # chamfer a hair under the plan R: equal sizes collapse the corner cone to a point (open sliver in the mesh)


def _plan(x_half, y0, y1, r):
    """Rounded rectangle symmetric about X = 0 spanning y0..y1 (sketch on the XY plane)."""
    with BuildSketch() as sk:
        with Locations((0, y0)):
            Rectangle(2 * x_half, y1 - y0, align=(Align.CENTER, Align.MIN))
        fillet(sk.vertices(), r)
    return sk


def shell():
    """Closed-top box printed deck-down: Boss-Extrude1 outline, top chamfer, cavity open underneath."""
    with BuildPart() as p:
        with BuildSketch(Plane.XY.offset(CH_Z0)) as sk:
            with Locations((0, CH_Y0)):
                Rectangle(2 * CH_HALF_W, CH_Y1 - CH_Y0, align=(Align.CENTER, Align.MIN))
            fillet(sk.vertices(), CH_WALL)  # plan R = wall
        extrude(amount=CH_Z1 - CH_Z0)
        chamfer(p.faces().sort_by(Axis.Z)[-1].edges(), CH_WALL - APEX_SHY)   # chamfer = wall thickness
    outer = p.part
    cav = _plan(CH_IN_X, WALL_IN_REAR, WALL_IN_FRONT, CAVITY_R)
    return outer - (Plane.XY.offset(CH_Z0 - CH_WALL) * extrude(cav.sketch, DECK - CH_Z0 + CH_WALL))
