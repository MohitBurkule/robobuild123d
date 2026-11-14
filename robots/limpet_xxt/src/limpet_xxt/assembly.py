"""Limpet XXT assembly: the tub is the datum; moving parts hang on build123d joints. UNTESTED: written without running.

Joints
  tub.hinge      RevoluteJoint, axis +Y through the front top edge  -> flipper + hinge block (rest = FLIP_REST_DEG down)
  tub.axle_*     RevoluteJoint on each motor shaft axis              -> wheel (free spin)
  tub.servo_out  RevoluteJoint on the servo output axis              -> horn
Static parts (side plates, lids, catalogue parts) are built in robot coordinates; the side plates and lids carry a
RigidJoint on their first screw so a check can mate them to the matching tub insert.
"""
import math

import build123d as bd

from .params import *  # noqa: F401,F403
from . import parts as P


def _hinge_frame(flip_deg):
    """World location of the flipper hinge frame for a flip angle (0 = rest, FLIP_OPEN_DEG = fully up)."""
    return bd.Pos(HINGE_X, 0, HINGE_Z) * bd.Rot(0, FLIP_REST_DEG - flip_deg, 0)


def horn_angle(flip_deg):
    """Horn angle (deg about +Y, from +X) that points the drive pin at the tail slot centre for a flip angle."""
    slot = _hinge_frame(flip_deg) * bd.Pos(-(TAIL_L - HORN_R), 0, 0)
    p = slot.position
    return math.degrees(math.atan2(-(p.Z - SERVO_OUT_Z), p.X - SERVO_OUT_X))


def build(flip_deg=START_FLIP_DEG):
    """Return {name: (solid, kind)} with kind in print / sheet / tyre / cots, placed in robot coordinates."""
    tub = P.tub()
    tub.label = "tub"
    bd.RevoluteJoint("hinge", tub, axis=bd.Axis((HINGE_X, 0, HINGE_Z), (0, 1, 0)), angular_range=(0, FLIP_OPEN_DEG))
    bd.RevoluteJoint("servo_out", tub, axis=bd.Axis((SERVO_OUT_X, 0, SERVO_OUT_Z), (0, 1, 0)))

    flip = bd.Compound(children=[P.flipper(), P.hinge_block()], label="flipper")
    bd.RigidJoint("hinge", flip, bd.Location())
    flip.location = _hinge_frame(flip_deg)          # = tub.joints["hinge"].connect_to(flip.joints["hinge"], angle)

    horn = P.horn()
    horn.label = "horn"
    horn.location = bd.Pos(SERVO_OUT_X, 0, SERVO_OUT_Z) * bd.Rot(0, horn_angle(flip_deg), 0)

    made = {
        "tub": (tub, "print"),
        "lid_r": (P.lid_right(), "sheet"),
        "lid_l": (P.lid_left(), "sheet"),
        "side_r": (P.side_plate_right(), "sheet"),
        "side_l": (P.side_plate_left(), "sheet"),
        "flipper": (P.flipper().moved(_hinge_frame(flip_deg)), "sheet"),
        "hinge_block": (P.hinge_block().moved(_hinge_frame(flip_deg)), "print"),
        "horn": (horn, "print"),
    }

    # four wheels: one built, patterned by mirror about XZ (left/right) and by the two axle stations (front/rear)
    w = P.wheel()
    for front in (True, False):
        x = AXLES_X[0] if front else AXLES_X[1]
        for left in (True, False):
            s = 1 if left else -1
            name = f"wheel_{'f' if front else 'r'}{'l' if left else 'r'}"
            bd.RevoluteJoint(f"axle_{name}", tub, axis=bd.Axis((x, s * WHEEL_Y, AXLE_Z), (0, s, 0)))
            made[name] = (bd.Pos(x, s * WHEEL_Y, AXLE_Z) * bd.Rot(0, 0, 90) * w, "tyre")

    cots = {f"motor_{'f' if f else 'r'}{'l' if l else 'r'}": (DRIVE_MOTOR_ID, P.motor_pose(f, l))
            for f in (True, False) for l in (True, False)}
    bat_bay, esc_bay = P._bays()
    sw_h = P.hw.size(SWITCH_ID)[2]
    cots.update({
        "servo": (SERVO_ID, P.servo_pose()),
        "battery": (BATTERY_ID, bat_bay.placement),
        "esc": (ESC_ID, esc_bay.placement),
        "switch": (SWITCH_ID, bd.Pos(ESC_X, -SIDE_ZONE_Y, TUB_Z1 - sw_h / 2)),
    })
    for name, (cid, loc) in cots.items():
        made[name] = (P.catalog_solid(cid).moved(loc), "cots")
    return made


def mass_report(made):
    fab = {k: v for k, v in made.items() if v[1] != "cots"}
    return P.mass_g(fab)


def export(out_dir, flip_deg=START_FLIP_DEG):
    """STEP of the assembly + one STL per fabricated part (not run here)."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    made = build(flip_deg)
    bd.export_step(bd.Compound(children=[s for s, _ in made.values()]), os.path.join(out_dir, "limpet_xxt.step"))
    for name, (solid, kind) in made.items():
        if kind != "cots" and not name.startswith("wheel_") or name == "wheel_fl":
            bd.export_stl(solid, os.path.join(out_dir, f"{name}.stl"))
    return made
