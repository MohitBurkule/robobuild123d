"""Printed nylon tub: sloped-side disc over the bar + rear drive pod. UNTESTED.

Made as: FDM PA12 / PA-CF, printed floor-down (+Z build), no supports except the N10 keyhole roofs (bridged).
Plan: disc of TUB_R on the weapon axis, unioned with the rear pod (POD_W x POD_L) that carries the N10s, battery,
ESCs, receiver and switch. Sides slope TUB_SLOPE_DEG inward going up: a vertical disc or drum hitting the side
glances up and off; nothing square to bite. Fragile parts (wires, pack, switch) are all inside the walls; the switch
is reached through a top-panel hole only.
Weapon boss: a ring round the bell bore, BOSS_T thick under the top panel; the stator's base screws (catalogue
mount_holes from revron weapon_motor.describe) go up through the boss into the top panel line (heat-set M2), so a
bar hit's torque and the gyro/impact shove go stator -> boss -> top panel + walls (the top panel is the tension skin).
Bay pockets: robot/cad/bay.py fits catalogue part envelopes into the pod (see pockets()); APIs there are used only
through part_envelope(), which is read but not confirmed for these ids.
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


def outline(grow=0.0):
    """Plan outline at the floor (widest section), the disc + pod, in world XY."""
    disc = bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R + grow)
    pod_y = (P.wheel_y() + P.POD_L / 2 + P.WPN_AXIS_Y) / 2
    pod = bd.Pos(0, pod_y) * bd.Rectangle(P.POD_W + 2 * grow, P.WPN_AXIS_Y - P.wheel_y() + P.POD_L / 2)
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


def weapon_boss():
    """Ring under the top panel the stator screws into; bell bore through the floor."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    ring_r = max(r for r, _, _ in m["base_holes"]) + 2 * P.TUB_WALL
    boss = bd.Pos(0, P.WPN_AXIS_Y, top - P.BOSS_T) * bd.Cylinder(ring_r, P.BOSS_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for r, deg, d in m["base_holes"]:
        boss -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg)), top - P.BOSS_T) * bd.Cylinder(
            d / 2, P.BOSS_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return boss


def bell_bore():
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(m["bell_r"] + P.MOTOR_BELL_CLR, P.TUB_FLOOR_T + 2,
                                                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def axle_holes():
    """N10 output shaft exits through the pod walls; one side built, mirrored."""
    one = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(2.0, 2 * P.TUB_WALL + 2)
    return one + bd.mirror(one, bd.Plane.YZ)


def tub():
    return shell() + weapon_boss() - bell_bore() - axle_holes()
