"""Ripsaw weapon rails: two printed prongs of the tub, double shear on the 2004's through shaft. UNTESTED.

Load path: tooth -> disc -> 3x M3 into the bell face -> bell/shaft -> (a) stator base -> 3x M3 through the LEFT rail,
(b) shaft end -> outboard bearing in the RIGHT rail -> both rails -> tub floor ring. Rotating: disc, bell, shaft,
bearing inner race. Fixed: stator, rails, bearing outer race.
Returns tool solids in world frame; tub.py unions/cuts them so the rails print as one piece with the tub."""
import build123d as bd

from . import params as P


def _rail_profile():
    """Side (YZ) profile of a rail prong: from the tub body front back into the body, up to the boss round the axle."""
    y0, y_nose = P.TUB_Y1 - P.RAIL_L, P.Y_AX + P.BOSS_R + P.RAIL_NOSE   # rail roots RAIL_L back inside the body
    return bd.Polygon((y0, P.TUB_FLOOR_Z), (y_nose, P.TUB_FLOOR_Z), (y_nose, P.RAIL_TOP), (y0, P.TUB_TOP_Z), align=None)


def _rail(x0, x1):
    return bd.extrude(bd.Plane.YZ.offset(x0) * _rail_profile(), x1 - x0)


def rails():
    """Left (stator) rail and right (bearing) rail plus the right bearing boss."""
    left = _rail(*P.RAIL_L_X)
    right = _rail(P.RAIL_R_X[0], P.RAIL_R_X[0] + P.RAIL_T)
    boss = bd.Pos(0, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Pos(0, 0, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2) * \
        bd.Cylinder(P.BOSS_R, P.RAIL_R_X[1] - P.RAIL_R_X[0])
    return left + right + boss


def cuts():
    """Stator screw holes (catalogue base pattern, through the left rail, csk outside), shaft clearance, bearing seat."""
    axis_at = lambda x: bd.Pos(x, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0)   # local Z along robot +X
    out = []
    for r, a, d in P.WM["base_holes"]:
        hole = bd.Rot(0, 0, a) * bd.Pos(r, 0, 0) * bd.Cylinder(d / 2 + P.MOVING_CLR / 2, P.RAIL_T * 3)
        out.append(axis_at(P.RAIL_L_X[0] + P.RAIL_T / 2) * hole)
    out.append(axis_at(P.WM_X_BACK) * bd.Cylinder(P.WM["base_hub_r"] + P.MOVING_CLR, P.RAIL_T * 3))   # rear hub / stub relief
    out.append(axis_at((P.RAIL_R_X[0] + P.BEAR_X[0]) / 2) * bd.Cylinder(P.WM["shaft_r"] + P.MOVING_CLR, P.BEAR_X[0] - P.RAIL_R_X[0] + 0.2))
    out.append(axis_at((P.BEAR_X[0] + P.BEAR_X[1]) / 2) * bd.Cylinder(P.BEAR_OD / 2, P.BEAR_W))   # press seat, blind outside
    out.append(bd.Pos(0, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) *
               bd.Cylinder(P.DISC_R + P.MOVING_CLR * 4, P.DISC_T + 2 * P.MOVING_CLR))   # disc slot through the tub body
    out.append(axis_at((P.WM_X_BACK + P.WM_X_CAP) / 2) * bd.Cylinder(P.WM["bell_r"] + 2 * P.MOVING_CLR, P.WM_BODY_L))
    return out


def motor_frame():
    """Location of the catalogue motor frame (+X = bell face) in the robot: bell face at WM_X_CAP on the axle."""
    return bd.Location((P.WM_X_CAP - P.WM["cap_x"], P.Y_AX, P.Z_AX))


def disc_frame():
    """Disc own frame (+Z spin axis) onto the robot +X axle, sheet from -DISC_T/2."""
    return bd.Location((-P.DISC_T / 2, P.Y_AX, P.Z_AX), (0, 90, 0))
