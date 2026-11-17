"""Emit robots/gnc/spec.json from src/gnc/params.py and src/gnc/parts.py.

Run from repo root: python3 robots/gnc/make_spec.py
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC = os.path.join(HERE, "src")
for _p in (ROOT, SRC):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from gnc import params as P  # noqa: E402
from gnc import parts as PP  # noqa: E402


def model(part):
    return {"type": "model", "file": "src/build_gnc.py", "params": {"part": part}}


def r3(p):
    return [r3(v) if isinstance(v, (list, tuple)) else round(float(v), 4) for v in p]


def fork_at(s, side, h=0.0):
    wy, wz = P.fork_point(s, h)
    return r3([side * P.FORK_X, wy, wz])


def fork_dir_z():
    a = math.radians(P.FORK_DEG)
    return r3([0.0, -math.sin(a), -math.cos(a)])


parts = [
    {
        "id": "tub",
        "kind": "structure",
        "material": P.PRINT_MAT,
        "process": "fdm",
        "print_orientation": "+z",
        "color": "#1e1e1e",
        "shape": model("tub"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "sharp_corners_ok": "internal corners are seams where printed bay walls, lid pads, and bridge meet the pod walls [expires 2027-12-31]",
        "label": "black FDM PLA twin-pod chassis with centre bridge, servo cradle, and sloped nose fork seats",
    },
    {
        "id": "lid_l",
        "kind": "armor",
        "material": P.SHEET_MAT,
        "process": "laser",
        "color": "#1e1e1e",
        "shape": model("lid_l"),
        "at": r3(PP.lid_at(1)),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.5 mm left pod top lid",
    },
    {
        "id": "lid_r",
        "kind": "armor",
        "material": P.SHEET_MAT,
        "process": "laser",
        "color": "#1e1e1e",
        "shape": model("lid_r"),
        "at": r3(PP.lid_at(-1)),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.5 mm right pod top lid with switch cutout",
    },
    {
        "id": "fork_l",
        "kind": "fork",
        "material": P.FORK_MAT,
        "process": "laser",
        "color": "#2f6b3c",
        "shape": model("fork_l"),
        "at": fork_at(0.0, 1),
        "rot": [-P.FORK_DEG, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.6 mm FR4 left front fork tine",
    },
    {
        "id": "fork_r",
        "kind": "fork",
        "material": P.FORK_MAT,
        "process": "laser",
        "color": "#2f6b3c",
        "shape": model("fork_r"),
        "at": fork_at(0.0, -1),
        "rot": [-P.FORK_DEG, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.6 mm FR4 right front fork tine",
    },
    {
        "id": "arm",
        "kind": "other",
        "material": P.ARM_MAT,
        "process": "fdm",
        "print_orientation": "+x",
        "color": "#d9f018",
        "shape": model("arm"),
        "at": r3([0.0, P.PIVOT_Y, P.PIVOT_Z]),
        "rot": [P.ARM_REST_DEG, 0.0, 0.0],
        "rotates_with": "arm",
        "actuated_by": "servo",
        "joint": {
            "kind": "revolute",
            "axis": [1.0, 0.0, 0.0],
            "pivot": r3([0.0, P.PIVOT_Y, P.PIVOT_Z]),
            "min": P.ARM_MIN_DEG,
            "max": 0.0,
            "default": 0.0,
        },
        "label": "yellow FDM PETG overhead rake arm with 5 hooked tines",
    },
]

for side, stag in ((1, "l"), (-1, "r")):
    for y, ftag in ((P.WHEEL_YF, "f"), (P.WHEEL_YR, "r")):
        tag = f"{ftag}{stag}"
        parts.append({
            "id": f"wheel_{tag}",
            "kind": "wheel",
            "material": "tpu",
            "process": "fdm",
            "print_orientation": "+x",
            "color": "#181818",
            "shape": model(f"wheel_{tag}"),
            "at": r3([side * P.WHEEL_X, y, P.AXLE_Z]),
            "rot": [0.0, 0.0, 0.0],
            "rotates_with": f"wheel_{tag}",
            "joint": {
                "kind": "revolute",
                "axis": [float(side), 0.0, 0.0],
                "pivot": r3([side * P.WHEEL_X, y, P.AXLE_Z]),
                "min": 0.0,
                "max": 360.0,
                "default": 0.0,
            },
            "label": f"26 mm knurled TPU wheel ({tag}) on N10 D-shaft",
        })
        parts.append({
            "id": f"motor_{tag}",
            "kind": "motor",
            "catalog": P.DRIVE_MOTOR_ID,
            "retained": "press_fit",
            "at": r3([side * P.MOTOR_AT_X, y, P.AXLE_Z]),
            "rot": [0.0, 0.0, 90.0 * (1 - side)],
            "rotates_with": "fixed",
            "label": f"N10 gearmotor ({tag}) in closed-top pod pocket",
        })

parts += [
    {
        "id": "servo",
        "kind": "servo",
        "catalog": P.SERVO_ID,
        "retained": "press_fit",
        "at": r3([P.SERVO_X, P.SERVO_Y, P.SERVO_Z]),
        "rot": [90.0, 0.0, 90.0],
        "rotates_with": "fixed",
        "label": "CS07 micro servo lying on its side in centre cradle",
    },
    {
        "id": "battery",
        "kind": "battery",
        "catalog": P.BATTERY_ID,
        "retained": "tape",
        "at": r3([P.BAT_X, P.BAT_Y, P.BAT_Z]),
        "rot": [0.0, 0.0, 90.0],
        "rotates_with": "fixed",
        "label": "2S 180 mAh LiPo in left pod",
    },
    {
        "id": "esc",
        "kind": "esc",
        "catalog": P.ESC_ID,
        "retained": "tape",
        "at": r3([P.ESC_X, P.ESC_Y, P.ESC_Z]),
        "rot": [0.0, 0.0, 90.0],
        "rotates_with": "fixed",
        "label": "Malenki Nano ESC+Rx in right pod",
    },
    {
        "id": "switch",
        "kind": "switch",
        "catalog": P.SWITCH_ID,
        "tool_free": True,
        "marked": True,
        "at": r3([P.SW_X, P.SW_Y, P.SW_Z]),
        "rot": [0.0, 0.0, 90.0],
        "rotates_with": "fixed",
        "label": "BBB ant switch in right pod",
    },
]

# Inserts & fasteners
HOLE_M2 = {"d": 2.0, "clearance_d": P.SCREW_CLEAR_D, "into": "through", "side": "head"}
fasteners = []

for side, stag in ((1, "l"), (-1, "r")):
    for i, y in enumerate(P.LID_SCREWS_Y):
        parts.append({
            "id": f"insert_lid_{stag}{i}",
            "kind": "insert",
            "catalog": P.INSERT_ID,
            "at": r3([side * P.LID_PAD_X, y, P.TUB_Z1 - P.INSERT_HALF_L]),
            "rot": [0.0, 0.0, 0.0],
            "rotates_with": "fixed",
            "retained": "press_fit",
        })
        fasteners.append({
            "id": f"bolt_lid_{stag}{i}",
            "designation": "M2x6",
            "material": "steel",
            "at": r3([side * P.LID_PAD_X, y, P.LID_Z1]),
            "dir": [0.0, 0.0, -1.0],
            "through": [f"lid_{stag}"],
            "threads_into": f"insert_lid_{stag}{i}",
            "tool": "hex1.5",
            "removable": True,
            "head": "button",
            "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1", "head_dk": 3.5, "head_k": 1.3, "grip": P.LID_T},
        })

    for i, s in enumerate(P.FORK_BOLT_S):
        parts.append({
            "id": f"insert_fork_{stag}{i}",
            "kind": "insert",
            "catalog": P.INSERT_ID,
            "at": fork_at(s, side, -P.FORK_T - P.INSERT_HALF_L),
            "rot": [-P.FORK_DEG, 0.0, 0.0],
            "rotates_with": "fixed",
            "retained": "press_fit",
        })
        fasteners.append({
            "id": f"bolt_fork_{stag}{i}",
            "designation": "M2x6",
            "material": "steel",
            "at": fork_at(s, side, 0.0),
            "dir": fork_dir_z(),
            "through": [f"fork_{stag}"],
            "threads_into": f"insert_fork_{stag}{i}",
            "tool": "hex1.5",
            "removable": True,
            "head": "button",
            "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1", "head_dk": 3.5, "head_k": 1.3, "grip": P.FORK_T},
        })

connections = []
allow_overlap = []
for side, stag in ((1, "l"), (-1, "r")):
    for ftag in ("f", "r"):
        tag = f"{ftag}{stag}"
        connections.append({
            "a": f"motor_{tag}",
            "b": f"wheel_{tag}",
            "method": "press_fit",
            "interference_mm": 0.1,
            "mechanical_key": True,
            "reason": "printed wheel D-bore on N10 3 mm D-shaft",
        })
        connections.append({
            "a": f"motor_{tag}",
            "b": "tub",
            "method": "interlock",
            "mechanical_key": True,
            "reason": "snug closed-top printed motor pocket in pod",
        })
        allow_overlap.append({
            "a": f"motor_{tag}",
            "b": f"wheel_{tag}",
            "max_depth_mm": 0.6,
            "reason": "wheel D-bore overlaps round stand-in of N10 shaft",
        })
    for i in range(len(P.LID_SCREWS_Y)):
        connections.append({
            "a": f"insert_lid_{stag}{i}",
            "b": "tub",
            "method": "press_fit",
            "interference_mm": 0.15,
            "reason": "M2 heat-set insert pressed into lid pad",
        })
        allow_overlap.append({
            "a": f"insert_lid_{stag}{i}",
            "b": "tub",
            "max_depth_mm": 0.15,
            "reason": "heat-set OD 3.2 pressed into 3.0 mm bore",
        })
    for i in range(len(P.FORK_BOLT_S)):
        connections.append({
            "a": f"insert_fork_{stag}{i}",
            "b": "tub",
            "method": "press_fit",
            "interference_mm": 0.15,
            "reason": "M2 heat-set insert pressed into nose fork seat",
        })
        allow_overlap.append({
            "a": f"insert_fork_{stag}{i}",
            "b": "tub",
            "max_depth_mm": 0.25,
            "reason": "heat-set OD 3.2 pressed into 3.0 mm bore",
        })

connections += [
    {"a": "servo", "b": "tub", "method": "press_fit", "interference_mm": 0.05, "reason": "servo seated in centre cradle"},
    {"a": "servo", "b": "arm", "method": "shaft", "clearance_mm": 0.05, "mechanical_key": True, "reason": "arm hub keyed on servo output spline"},
    {"a": "battery", "b": "tub", "method": "tape", "reason": "2S LiPo taped into left pod bay"},
    {"a": "esc", "b": "tub", "method": "tape", "reason": "Malenki Nano taped into right pod bay"},
    {"a": "switch", "b": "tub", "method": "press_fit", "reason": "switch seated in right pod tray under lid"},
]

wires = [
    {
        "id": "w_bat_sw",
        "from": "battery.xt30",
        "to": "switch.in",
        "awg": 22,
        "kind": "power",
        "slack_mm": 8.0,
        "via": r3([[P.BAT_X, P.POD_Y0 + 6.5, 8.5], [0.0, P.POD_Y0 + 6.5, 8.5], [P.SW_X, P.POD_Y0 + 6.5, 8.5]]),
    },
    {
        "id": "w_sw_esc",
        "from": "switch.out",
        "to": "esc.bat",
        "awg": 26,
        "kind": "power",
        "slack_mm": 6.0,
    },
    {
        "id": "w_esc_mfl",
        "from": "esc.m1",
        "to": "motor_fl.terminals",
        "awg": 26,
        "kind": "motor",
        "slack_mm": 8.0,
        "via": r3([[0.0, P.POD_Y0 + 6.5, 8.5], [P.POD_IN_XI + 3.0, P.WHEEL_YF, 10.0]]),
    },
    {
        "id": "w_esc_mfr",
        "from": "esc.m2",
        "to": "motor_fr.terminals",
        "awg": 26,
        "kind": "motor",
        "slack_mm": 6.0,
    },
    {
        "id": "w_esc_servo",
        "from": "esc.wpn",
        "to": "servo.signal",
        "awg": 26,
        "kind": "signal",
        "slack_mm": 6.0,
    },
]

spec = {
    "name": "GNC",
    "profile": "aws2025",
    "robot_type": "lifter",
    "locomotion": "wheeled",
    "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
    "can_run_inverted": False,
    "claims": [
        {"id": "c_mass", "text": "weighs 150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150.0},
        {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0},
    ],
    "parts": parts,
    "fasteners": fasteners,
    "wires": wires,
    "connections": connections,
    "allow_overlap": allow_overlap,
}

with open(os.path.join(HERE, "spec.json"), "w") as f:
    json.dump(spec, f, indent=1)
print(f"wrote robots/gnc/spec.json: {len(parts)} parts, {len(fasteners)} fasteners")
