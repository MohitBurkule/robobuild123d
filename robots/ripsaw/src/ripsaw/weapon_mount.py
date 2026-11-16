"""Ripsaw weapon plates: two printed nylon plates bolted to the tub's front-wall pads. UNTESTED.

Load path: tooth -> disc -> 3x M3 into the bell face (driven with the right plate off) -> bell/shaft ->
(a) stator -> 3x M2.5 -> mount plate (left), (b) shaft end -> MR63 press fit in the post plate (right) ->
both plates -> 3x M2 each from INSIDE the tub, threading into tapped holes in the plate heels.
Rotating: disc, bell, shaft, bearing inner race. Fixed: stator, plates, bearing outer race, tub.

Service: the M2 plate screws come out from inside the tub (tool straight along Y, open interior); with both
plates off, the weapon (disc + bell + shaft) slides forward out of the disc slot, and the stator then lifts off its
screws. Nothing is trapped by the unibody.
"""
import build123d as bd

from . import params as P


def _tap_holes(x0, x1):
    """M2 tap holes along Y through the plate heel, on the plate's x centreline: the plate screws thread straight
    into the nylon (1.0 mm walls round the bore in the 4 mm plate)."""
    out = []
    for z in P.PLATE_SCREW_Z:
        out.append(bd.Pos((x0 + x1) / 2, P.TUB_Y1 + P.PLATE_HEEL_L / 2, z) * bd.Rot(90, 0, 0)
                   * bd.Cylinder(1.0, P.PLATE_HEEL_L + 2))
    return out


def _plate(x0, x1):
    """A plate: heel box bearing on the front wall face, prong rising past the axle to RAIL_TOP, fork-pin pad."""
    y0, y_heel1 = P.PLATE_Y0, P.PLATE_Y0 + P.PLATE_HEEL_L
    heel = bd.Pos((x0 + x1) / 2, (y0 + y_heel1) / 2, (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2) \
        * bd.Box(x1 - x0, y_heel1 - y0, P.TUB_TOP_Z - P.TUB_FLOOR_Z)
    prong = bd.extrude(bd.Plane.YZ.offset(x0) * bd.Polygon(
        (y_heel1, P.TUB_FLOOR_Z), (P.PLATE_NOSE_Y, P.TUB_FLOOR_Z),
        (P.PLATE_NOSE_Y, P.RAIL_TOP), (y_heel1, P.TUB_TOP_Z), align=None), x1 - x0)
    from . import forks as F
    pad = bd.Pos((x0 + x1) / 2, F.pin_point(1)[1], F.pin_point(1)[2]) * bd.Rot(0, 90, 0) * bd.Cylinder(P.PIN_PAD_R, x1 - x0)
    return heel + prong + pad


def mount_l():
    """Left plate: stator screws (catalogue base pattern through the plate), rear hub relief, plate screws, fork pin."""
    import math
    x0, x1 = P.RAIL_L_X
    s = _plate(x0, x1)
    for r, a, _d in P.WM["base_holes"]:
        s = s - bd.Pos((x0 + x1) / 2, P.Y_AX + r * math.cos(math.radians(a)), P.Z_AX + r * math.sin(math.radians(a))) \
            * bd.Rot(0, 90, 0) * bd.Cylinder(P.STATOR_SCREW_CLR / 2, P.PLATE_T * 3)
    s = s - bd.Pos((x0 + x1) / 2, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(3.1, P.PLATE_T * 3)  # rear hub relief
    for c in _tap_holes(x0, x1):
        s = s - c
    s = s - fork_pin_hole(x0, x1)
    s = s - lock_pin_hole(x0, x1)
    s.label = "mount_l"
    return s


def post_r():
    """Right plate: MR63 press seat (flush with the outer face), shaft clearance behind it, plate screws, fork pin."""
    x0, x1 = P.RAIL_R_X
    s = _plate(x0, x1)
    s = s - bd.Pos((P.BEAR_X[0] + P.BEAR_X[1]) / 2, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(P.BEAR_OD / 2, P.BEAR_W)
    s = s - bd.Pos((x0 + P.BEAR_X[0]) / 2, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(P.WM["shaft_r"] + 1.3,
                                                                                           P.BEAR_X[0] - x0 + 0.2)
    for c in _tap_holes(x0, x1):
        s = s - c
    s = s - fork_pin_hole(x0, x1)
    s = s - lock_pin_hole(x0, x1)
    s.label = "post_r"
    return s


def fork_pin_hole(x0=None, x1=None):
    """M3 fork hinge pin clearance hole through a plate at the fork pin point (part of both plates)."""
    from . import forks as F
    y, z = F.pin_point(1)[1], F.pin_point(1)[2]
    x0 = x0 if x0 is not None else min(P.RAIL_L_X[0], P.RAIL_R_X[0]) - 1.0
    x1 = x1 if x1 is not None else max(P.RAIL_L_X[1], P.RAIL_R_X[1]) + 1.0
    return bd.Pos((x0 + x1) / 2, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(P.FORK_PIN / 2 + 0.1, x1 - x0 + 2)


def lock_pin_hole(x0=None, x1=None):
    """3 mm weapon lock pin hole through a plate, on the balance-window radius (weapon_lock)."""
    import math
    a = math.radians(P.LOCK_ANGLE)
    y = P.Y_AX + P.LOCK_R * math.sin(a)
    z = P.Z_AX - P.LOCK_R * math.cos(a)
    x0 = x0 if x0 is not None else min(P.RAIL_L_X[0], P.RAIL_R_X[0]) - 1.0
    x1 = x1 if x1 is not None else max(P.RAIL_L_X[1], P.RAIL_R_X[1]) + 1.0
    return bd.Pos((x0 + x1) / 2, y, z) * bd.Rot(0, 90, 0) * bd.Cylinder(1.6, x1 - x0 + 2)


def motor_frame():
    """Location of the catalogue motor frame (+X = bell face) in the robot: bell face at WM_X_CAP on the axle."""
    return bd.Location((P.WM_X_CAP - P.WM["cap_x"], P.Y_AX, P.Z_AX))


def disc_frame():
    """Disc own frame (+Z spin axis) onto the robot +X axle, sheet from -DISC_T/2."""
    return bd.Location((-P.DISC_T / 2, P.Y_AX, P.Z_AX), (0, 90, 0))
