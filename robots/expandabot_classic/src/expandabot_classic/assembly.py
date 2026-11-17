"""Expandabot Classic assembly entry point."""
import os

import build123d as bd

from . import parts as P
from .params import *  # noqa: F401,F403

PARTS = {
    "tub": P.tub,
    "top_panel": P.top_panel,
    "side_l": P.side_left,
    "side_r": P.side_right,
    "wedge": P.wedge,
    "crossbar": P.crossbar,
    "bracket_l": P.bracket_left,
    "bracket_r": P.bracket_right,
    "wing_l": P.wing_left,
    "wing_r": P.wing_right,
    "hinge_pin_l": P.hinge_pin,
    "hinge_pin_r": P.hinge_pin,
    "horn": P.horn,
    "nose_pin": P.nose_pin,
    "wheel_l": P.wheel_left,
    "wheel_r": P.wheel_right,
}


def build(part="tub", **_kw):
    if part not in PARTS:
        raise KeyError(f"unknown Expandabot Classic part `{part}`; one of {sorted(PARTS)}")
    return PARTS[part]()


def cots():
    return {
        "motor_l": (DRIVE_MOTOR_ID, P.motor_pose(True)),
        "motor_r": (DRIVE_MOTOR_ID, P.motor_pose(False)),
        "servo": (SERVO_ID, P.servo_pose()),
        "battery": (BATTERY_ID, bd.Pos(BAT_X, BAT_Y, BAT_Z) * bd.Rot(0, 0, 90)),
        "esc": (ESC_ID, bd.Pos(ESC_X, ESC_Y, ESC_Z) * bd.Rot(0, 0, 90)),
        "switch": (SWITCH_ID, P.switch_pose()),
    }


def made_parts():
    made = {}
    for name, fn in PARTS.items():
        if name in ("tub", "wedge", "bracket_l", "bracket_r", "horn", "nose_pin"):
            kind = "print"
        elif name == "top_panel":
            kind = "cf"
        elif name in ("crossbar", "hinge_pin_l", "hinge_pin_r"):
            kind = "steel"
        elif name.startswith("wheel_"):
            kind = "tyre"
        else:
            kind = "sheet"
        made[name] = (fn(), kind)
    return made


def mass_report(made):
    return P.mass_g({k: v for k, v in made.items() if v[1] != "cots"})
