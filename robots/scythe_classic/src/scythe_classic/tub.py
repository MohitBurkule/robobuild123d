"""Printed nylon tub: a sloped-side cone over the bar, with a vertical-walled rear pod that carries the N10s.

Made as: FDM nylon, printed floor-down (+Z build). The cone (round, tapering up) is the old Scythe look; its walls
slope TUB_SLOPE_DEG inward going up so a vertical hit glances off. The rear pod is a rectangular arm behind the disc
that carries the two N10 drive motors, battery, ESC, receiver and switch. Its walls are vertical: a motor body at
the wheel height sits inside the walls, and a sloped wall there would cut through it.
Weapon boss: a ring from the floor to the top panel round the bell, with the stator's base screw holes (catalogue
base_holes, weapon_motor.describe). The screws take the stator into the top panel, so a bar hit's torque goes
stator -> boss -> top panel and walls (the top panel is the tension skin).
"""
import math

import build123d as bd

from . import params as P
from ._reuse import hw, weapon_motor


def _slope_inset(h):
    return h * math.tan(math.radians(P.TUB_SLOPE_DEG))


def z0():
    return P.tub_floor_z()


def height():
    return P.TUB_TOP_Z - P.TOP_PANEL_T - z0()


def pod_front_y():
    """Y where the pod's front edge meets the cone: its outer corners sit on the disc's circle."""
    return P.WPN_AXIS_Y - math.sqrt(P.TUB_R ** 2 - (P.POD_W / 2) ** 2)


def pod_rear_y():
    """Rear edge: POD_L behind the wheel axle line."""
    return P.wheel_y() - P.POD_L / 2


def pod_len():
    return pod_front_y() - pod_rear_y()


def pod_cy():
    return (pod_front_y() + pod_rear_y()) / 2


def disc_face(grow=0.0):
    """Cone plan outline (circle) at the floor, grown or shrunk by `grow`, on the weapon axis."""
    return bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R + grow)


def pod_box(grow=0.0, z_lo=0.0, h=None):
    """Vertical rear pod prism, grown or shrunk on all four sides by `grow`."""
    h = height() if h is None else h
    return bd.Pos(0, pod_cy(), z_lo) * bd.Box(P.POD_W + 2 * grow, pod_len() + 2 * grow, h,
                                              align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def top_outline(inset):
    """Plan outline of the top panel: the cone shrunk by the slope inset, joined to the pod's full-width top."""
    disc = bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R - inset)
    pod = bd.Pos(0, pod_cy()) * bd.Rectangle(P.POD_W, pod_len())
    return (disc + pod).clean()


def cone_loft(grow_lo, grow_hi, z_lo, z_hi):
    """Sloped cone solid: the circle grown by grow_lo at z_lo, grown by grow_hi at z_hi (the slope sets grow_hi)."""
    lo = bd.Plane.XY.offset(z_lo)
    hi = bd.Plane.XY.offset(z_hi)
    return bd.loft([lo * disc_face(grow_lo).faces()[0], hi * disc_face(grow_hi).faces()[0]])


def outer_body():
    """The solid tub outside: sloped cone plus the vertical rear pod."""
    h = height()
    cone = cone_loft(0.0, -_slope_inset(h), z0(), z0() + h)
    return cone + pod_box(z_lo=z0(), h=h)


def cavity():
    """What is hollowed out: the cone inside its walls above the floor, and the pod inside its walls."""
    h = height()
    # the outer cone is already inset by the slope at the floor top: the wall is measured from that radius, so the base
    # keeps TUB_WALL (a plain -TUB_WALL at the floor top left a zero-thickness wall at the cone base)
    base_inset = P.TUB_FLOOR_T * math.tan(math.radians(P.TUB_SLOPE_DEG))
    cone = cone_loft(-P.TUB_WALL - base_inset, -_slope_inset(h) - P.TUB_WALL, z0() + P.TUB_FLOOR_T, z0() + h + 0.01)
    pod = pod_box(-P.TUB_WALL, z0() + P.TUB_FLOOR_T, h + 0.01 - P.TUB_FLOOR_T)
    return cone + pod


def shell():
    return outer_body() - cavity()


def weapon_boss():
    """Printed ring from the floor to the top panel: the stator's base screws go down through it. Its inner wall is
    the bell clearance, and the motor solid is cut out so the cross base and stator sit clear of it."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    z_lo = z0() + P.TUB_FLOOR_T
    r_out = max(r for r, _, _ in m["base_holes"]) + 2 * P.TUB_WALL
    r_in = m["bell_r"] + P.MOTOR_BELL_CLR
    ring = bd.Pos(0, P.WPN_AXIS_Y, z_lo) * (bd.Cylinder(r_out, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
                                           - bd.Cylinder(r_in, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    for r, deg, d in m["base_holes"]:
        ring -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg)), z_lo) * bd.Cylinder(
            d / 2, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return ring - weapon_motor_placed()


def weapon_motor_placed():
    """The weapon motor solid at its assembly pose (shaft down), as the assembly places it."""
    return hw.placed(P.WEAPON_MOTOR, (0.0, P.WPN_AXIS_Y, P.wpn_motor_z()), (0.0, 90.0, 0.0))


def bell_bore():
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(m["bell_r"] + P.MOTOR_BELL_CLR, P.TUB_FLOOR_T + 2,
                                                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def axle_holes():
    """N10 output shaft exits through the pod walls; one side built, mirrored. 2.3 mm hole: the N10's 2 mm shaft collar and the 3 mm shaft pass it."""
    one = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(2.3, 2 * P.TUB_WALL + 2)
    return one + bd.mirror(one, bd.Plane.YZ)


RIB_T = 1.2        # mm cradle rib thickness (nozzle multiple)
RIB_GAP = 0.2      # mm print clearance between the N10 flats and the ribs


def motor_cradles():
    """Two ribs per N10 along its length (y = axle line +-(6 + gap)), from the pod floor up to the motor top, from the pod
    wall inward over the body length. The motor drops in from the top (panel off) and is held in y by the ribs and in x by
    the pod wall on its shaft side; the N10's flats are 12 mm wide (catalogue box 9 x 12 x 10)."""
    out = None
    z_lo = z0() + P.TUB_FLOOR_T
    z_hi = P.WHEEL_CZ + 5.0
    x_in = P.POD_W / 2 - P.TUB_WALL                   # inner face of the pod wall
    x_rear = x_in - (P.DRIVE_MOTOR_FACE_X - P.DRIVE_MOTOR_REAR_X) - 0.2
    for side in (1, -1):
        for sy in (1, -1):
            yc = P.wheel_y() + sy * (6.0 + RIB_GAP + RIB_T / 2)
            rib = bd.Pos(side * (x_in + x_rear) / 2, yc, z_lo) * bd.Box(
                x_in - x_rear + 0.2, RIB_T, z_hi - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            out = rib if out is None else out + rib
    return out


def tub():
    return shell() + weapon_boss() + motor_cradles() - bell_bore() - axle_holes()
