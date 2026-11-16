"""Printed nylon tub: sloped-side disc over the bar + rear drive pod.

Made as: FDM PA12 / PA-CF, printed floor-down (+Z build), no supports except the N10 keyhole roofs (bridged).
Plan: disc of TUB_R on the weapon axis, unioned with the rear pod (POD_W wide) that carries the N10s, battery,
ESCs, receiver and switch. Sides slope TUB_SLOPE_DEG inward going up: a vertical disc or drum hitting the side
glances up and off; nothing square to bite. Fragile parts (wires, pack, switch) are all inside the walls; the switch
is reached through a top-panel hole only.
Weapon boss: a ring on the stator flange top face up to the top panel; the stator's base screws (catalogue
mount_holes from revron weapon_motor.describe) go down through the panel and the boss into the flange, so a
bar hit's torque and the gyro/impact shove go stator -> boss -> top panel + walls (the top panel is the tension skin).
Drive cradles: printed pads and side ribs under and beside each N10; the gearbox face bears on the pod wall and
the wheel boss on the shaft clamps the wall between them, so the motors cannot walk inboard.
"""
import math

import build123d as bd

from . import params as P
from ._reuse import weapon_motor


def _slope_inset(h):
    return h * math.tan(math.radians(P.TUB_SLOPE_DEG))


def z0():
    return P.tub_floor_z()


def height():
    return P.TUB_TOP_Z - P.TOP_PANEL_T - z0()


def pod_rear_y():
    """Rear face of the pod at the floor."""
    return P.wheel_y() - P.POD_REAR


def outline(grow=0.0):
    """Plan outline at the floor (widest section), the disc + pod, in world XY."""
    disc = bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R + grow)
    pod = bd.Pos(0, (pod_rear_y() + P.WPN_AXIS_Y) / 2) * bd.Rectangle(P.POD_W + 2 * grow, P.WPN_AXIS_Y - pod_rear_y())
    return (disc + pod).clean()


def shell():
    """Lofted sloped outer body minus the same loft offset by the wall."""
    h = height()
    inset = _slope_inset(h)
    lo = bd.Plane.XY.offset(z0())
    hi = bd.Plane.XY.offset(z0() + h)
    outer = bd.loft([lo * outline().faces()[0], hi * outline(-inset).faces()[0]])
    inner = bd.loft([lo.offset(P.TUB_FLOOR_T) * outline(-P.TUB_WALL).faces()[0],
                     hi.offset(0.01) * outline(-inset - P.TUB_WALL).faces()[0]])
    return outer - inner


def motor_z():
    """Weapon motor origin z: bell cap on the hub top face (assembly.weapon_motor_solid)."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return P.bar_top_z() + P.HUB_H + m["cap_x"]


def flange_top_z():
    """Top face of the stator mounting flange in world z (catalogue +X = bell cap -> world -Z)."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return motor_z() - m["back_x"]


def weapon_boss():
    """Ring on the stator flange top face up to the top panel; the panel screws pass through it into the flange."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    thick = top - flange_top_z()
    ring_r = max(r for r, _, _ in m["base_holes"]) + 2 * P.TUB_WALL
    boss = bd.Pos(0, P.WPN_AXIS_Y, flange_top_z()) * bd.Cylinder(ring_r, thick, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for r, deg, d in m["base_holes"]:
        boss -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg)), flange_top_z()) * bd.Cylinder(
            d / 2 + 0.1, thick, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return boss


def bell_bore():
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(m["bell_r"] + P.MOTOR_BELL_CLR, P.TUB_FLOOR_T + 2,
                                                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def axle_holes():
    """N10 output shaft exits through the pod walls; one side built, mirrored."""
    one = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(2.0, 2 * P.TUB_WALL + 2)
    return one + bd.mirror(one, bd.Plane.YZ)


def _cradle(side):
    """Pad + front/rear ribs locating one N10 body against the pod wall (side +1 right, -1 left)."""
    x_in = abs(P.POD_W / 2 - P.TUB_WALL + P.N10_BODY_IN)
    x_out = P.POD_W / 2 - P.TUB_WALL
    lo, hi = sorted((side * x_in, side * x_out))
    floor = z0() + P.TUB_FLOOR_T
    pad = bd.Pos((lo + hi) / 2, P.wheel_y(), floor) * bd.Box(hi - lo, 11.5, P.WHEEL_CZ - 5 - floor,
                                                            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    rib_t = 1.5
    for sgn in (-1, 1):
        pad += bd.Pos((lo + hi) / 2, P.wheel_y() + sgn * (6.1 + rib_t / 2), floor) * bd.Box(
            hi - lo, rib_t, P.WHEEL_CZ + 5 - floor, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return pad


def tub():
    return shell() + weapon_boss() + _cradle(1) + _cradle(-1) - bell_bore() - axle_holes()
