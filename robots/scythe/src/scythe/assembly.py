"""Scythe assembly with build123d joints (rigid / revolute), mirroring Revron's rig idea (joints.py).

Stack on the weapon axis, bottom up: foot (on the shaft thread) -> bar -> hub -> GR1507 bell (cap down) -> stator
(flange up against the tub boss) -> boss -> top panel.
Rotating: foot, bar, hub, bell (one revolute joint on the axis). Fixed: everything else.

The GR1507 is split like Revron: weapon_motor_stator (catalogue gr1507, fixed, flange bolted up into the boss) and
weapon_motor_bell (gr1507_can, spins with the bar). The catalogue motor has no output shaft, so the rotor shaft is
modelled separately (wshaft) like Revron's: it runs from the foot thread (z 0.5) up into the bell cap.
"""
import build123d as bd

from . import params as P
from . import bar, weapon_hub, tub, drive, skids, panels
from ._reuse import hw, weapon_motor


def _axis_loc(z):
    return bd.Location((0, P.WPN_AXIS_Y, z))


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
    """GR1507 shaft-down: bell cap on the hub top face. rot (0, 90, 0) turns +X to -Z (right-hand about +Y)."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return (0.0, P.WPN_AXIS_Y, tub.motor_z()), (0.0, 90.0, 0.0)


def weapon_motor_stator():
    at, rot = motor_pose()
    return hw.placed(weapon_motor.describe(P.WEAPON_MOTOR)["id"], at, rot)


def weapon_motor_bell():
    at, rot = motor_pose()
    return hw.placed("gr1507_can", at, rot)


def wshaft():
    """Rotor shaft extension: from the foot thread up into the bell cap (the catalogue motor has no shaft)."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    top = tub.motor_z() - m["cap_x"] + 1.7
    return bd.Pos(0, P.WPN_AXIS_Y, 0.5) * bd.Cylinder(m["shaft_r"], top - 0.5,
                                                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def build(angle_deg=0.0):
    t, h, b = weapon_stack(angle_deg)
    parts = dict(tub=t, weapon_hub=h, bar=b, weapon_motor_stator=weapon_motor_stator(),
                 weapon_motor_bell=weapon_motor_bell(), wshaft=wshaft(), top_panel=panels.top_panel())
    parts.update(drive.parts())
    parts.update(skids.parts())
    return parts


def compound(angle_deg=0.0):
    return bd.Compound(label="scythe", children=list(build(angle_deg).values()))
