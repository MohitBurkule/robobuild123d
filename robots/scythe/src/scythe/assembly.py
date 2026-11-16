"""Scythe assembly with build123d joints (rigid / revolute), mirroring Revron's rig idea (joints.py).

Motor-as-hub weapon stack on the axis, bottom up: M3 nut (on the shaft's lower thread) -> bar -> hub (both on the
motor's own 3 mm shaft) -> bl_1806 bell (cap down on the hub's top face; the shaft is a press fit in the bell's bored
core) -> stator (flange up, screwed through the top panel and the printed boss).
Rotating: bar, hub, nut, shaft, bell (one revolute joint on the axis). Fixed: everything else, including the stator
(the motor's own bearings carry the rotor from above; the bar is a cantilevered undercutter, like the reference
hspin_bar, whose open side stays a warning under the 20 J stored-energy cap).

The bl_1806 is split like Revron's GR1507: weapon_motor_stator (catalogue bl_1806_stator, fixed) and
weapon_motor_bell (bl_1806_can, spins with the bar). The motor's own shaft is drawn as its own part (wshaft,
`shaft_of` the bell): it runs from the nut thread at the bottom, through bar and hub, up into the bell core bore.
"""
import build123d as bd

from . import params as P
from . import bar, weapon_hub, tub, drive, panels
from ._reuse import hw


def weapon_stack(angle_deg=0.0):
    """Bar and hub placed by joints: tub-fixed axis joint (revolute) -> hub bar-face joint -> bar top joint."""
    t = tub.tub()
    h = weapon_hub.hub()
    b = bar.bar()
    bd.RevoluteJoint("weapon_axis", t, axis=bd.Axis((0, P.WPN_AXIS_Y, P.bar_top_z()), (0, 0, 1)), angle_reference=(1, 0, 0))
    bd.RigidJoint("bar_face", h, bd.Location((0, 0, 0)))
    bd.RigidJoint("hub_face", b, bd.Location((0, 0, P.BAR_T)))
    t.joints["weapon_axis"].connect_to(h.joints["bar_face"], angle=angle_deg)
    h.joints["bar_face"].connect_to(b.joints["hub_face"])
    return t, h, b


def motor_pose():
    """bl_1806 shaft-down: bell cap on the hub top face. rot (0, 90, 0) turns +X to -Z (right-hand about +Y)."""
    return (0.0, P.WPN_AXIS_Y, P.motor_z()), (0.0, 90.0, 0.0)


def weapon_motor_stator():
    at, rot = motor_pose()
    return hw.placed(P.WEAPON_MOTOR_STATOR, at, rot)


def weapon_motor_bell():
    at, rot = motor_pose()
    return hw.placed(P.WEAPON_MOTOR_CAN, at, rot)


def wshaft():
    """The motor's own shaft, extended: from the M3 nut thread at the bottom through bar and hub into the bell core."""
    return bd.Pos(0, P.WPN_AXIS_Y, P.WSHAFT_TIP_Z) * bd.Cylinder(P.SHAFT_D / 2, P.wshaft_len(),
                                                                 align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def shaft_nut():
    """M3 aluminium nut on the shaft's lower thread: clamps bar + hub up against the bell cap face."""
    return bd.Pos(0, P.WPN_AXIS_Y, P.nut_z0()) * bd.Cylinder(2.75, P.NUT_T,
                                                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def build(angle_deg=0.0):
    t, h, b = weapon_stack(angle_deg)
    parts = dict(tub=t, weapon_hub=h, bar=b, weapon_motor_stator=weapon_motor_stator(),
                 weapon_motor_bell=weapon_motor_bell(), wshaft=wshaft(), shaft_nut=shaft_nut(),
                 top_panel=panels.top_panel())
    parts.update(drive.parts())
    return parts


def compound(angle_deg=0.0):
    return bd.Compound(label="scythe", children=list(build(angle_deg).values()))
