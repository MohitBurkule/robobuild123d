"""Scythe assembly with build123d joints (rigid / revolute), mirroring Revron's rig idea (joints.py). UNTESTED.

Stack on the weapon axis, bottom up: foot -> bar -> hub -> GR1507 bell (shaft down) -> stator -> tub boss -> top panel.
Rotating: foot, bar, hub, bell + shaft (one revolute joint on the axis). Fixed: everything else.
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


def weapon_motor_solid():
    """GR1507 catalogue solid, shaft down: catalogue +X = bell top -> world -Z; bell cap on the hub top face.
    rot (0, 90, 0) turns +X to -Z (right-hand about +Y). describe()['cap_x'] is the bell cap in the catalogue frame."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    cap_z = P.bar_top_z() + P.HUB_H
    return hw.placed(m["id"], (0.0, P.WPN_AXIS_Y, cap_z + m["cap_x"]), (0.0, 90.0, 0.0))


def build(angle_deg=0.0):
    t, h, b = weapon_stack(angle_deg)
    parts = dict(tub=t, weapon_hub=h, bar=b, weapon_motor=weapon_motor_solid(), top_panel=panels.top_panel())
    parts.update(drive.parts())
    parts.update(skids.parts())
    return parts


def compound(angle_deg=0.0):
    return bd.Compound(label="scythe", children=list(build(angle_deg).values()))
