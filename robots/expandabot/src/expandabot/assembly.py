"""Expandabot assembly: the tub is the datum; moving parts are placed in world coordinates at rest and carry their
motion in the spec joints (flipper revolute at the hinge, horn revolute at the servo output, wheels free on the axles).

`build(part=...)` is the geometry entry point the spec's model shapes call; `cots()` returns the catalogue parts with
their world poses for the spec.
"""
import os

import build123d as bd

from . import parts as P
from .params import *  # noqa: F401,F403

PARTS = {
    "tub": P.tub,
    "lid_r": P.lid_right,
    "lid_l": P.lid_left,
    "side_r": P.side_plate_right,
    "side_l": P.side_plate_left,
    "clamp_r": P.clamp_right,
    "clamp_l": P.clamp_left,
    "flipper": P.flipper,
    "hinge_block": P.hinge_block,
    "horn": P.horn,
    "drive_pin": P.drive_pin,
    "hinge_pin": P.hinge_pin,
    "wheel_l": P.wheel_left,
    "wheel_r": P.wheel_right,
}


def build(part="tub", **_kw):
    if part not in PARTS:
        raise KeyError(f"unknown Expandabot part `{part}`; one of {sorted(PARTS)}")
    return PARTS[part]()


def cots():
    """Catalogue parts as {name: (catalog_id, build123d Location)} in world coordinates."""
    out = {
        "motor_l": (DRIVE_MOTOR_ID, P.motor_pose(True)),
        "motor_r": (DRIVE_MOTOR_ID, P.motor_pose(False)),
        "servo": (SERVO_ID, P.servo_pose()),
        "battery": (BATTERY_ID, bd.Pos(0, BAT_Y, TUB_Z0 + WALL + BAT_H / 2) * bd.Rot(0, 0, 90)),
        "esc": (ESC_ID, bd.Pos(SIDE_ZONE_X, ESC_Y, TUB_Z0 + WALL + ESC_H / 2) * bd.Rot(0, 0, 90)),
        "switch": (SWITCH_ID, P.switch_pose()),
    }
    return out


def made_parts():
    """{name: (solid, kind)} for every fabricated part."""
    made = {
        name: (fn(), "print" if name in ("tub", "hinge_block", "horn") else
               ("tyre" if name.startswith("wheel_") else "sheet"))
        for name, fn in PARTS.items()
    }
    made["hinge_pin"] = (P.hinge_pin(), "print")
    return made


def mass_report(made):
    fab = {k: v for k, v in made.items() if v[1] != "cots"}
    return P.mass_g(fab)


def export(out_dir):
    """STEP of the assembly + one STL per fabricated part."""
    os.makedirs(out_dir, exist_ok=True)
    made = made_parts()
    for name, (cid, loc) in cots().items():
        made[name] = (P.catalog_solid(cid).moved(loc), "cots")
    bd.export_step(bd.Compound(children=[s for s, _ in made.values()]), os.path.join(out_dir, "expandabot.step"))
    for name, (solid, kind) in made.items():
        if kind != "cots":
            bd.export_stl(solid, os.path.join(out_dir, f"{name}.stl"))
    return made
