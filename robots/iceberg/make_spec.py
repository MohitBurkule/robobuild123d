"""Emit robots/iceberg/spec.json from parametric dimensions in src/iceberg/params.py.

Run from repo root:
  .venv/bin/python robots/iceberg/make_spec.py
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from iceberg import params as P  # noqa: E402


def model(part: str):
    return {"type": "model", "file": "src/build_iceberg.py", "params": {"part": part}}


def r3(v):
    return [r3(x) if isinstance(x, (list, tuple)) else round(float(x), 4) for x in v]


def hole_m2(length: float, grip: float):
    return {
        "d": 2.0,
        "clearance_d": 2.2,
        "into": "through",
        "side": "head",
        "length": length,
        "head": "button",
        "head_std": "ISO 7380-1",
        "head_dk": 3.5,
        "head_k": 1.3,
        "grip": grip,
    }


def hole_m16(length: float, grip: float):
    return {
        "d": 1.6,
        "clearance_d": 1.8,
        "into": "through",
        "side": "head",
        "length": length,
        "head": "button",
        "head_std": "ISO 7380-1",
        "head_dk": 2.8,
        "head_k": 1.0,
        "grip": grip,
    }


parts = [
    # ---- Structure: internal tub + green CF top & bottom plates ----
    {
        "id": "tub",
        "kind": "structure",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+z",
        "solid_fraction": 0.55,
        "color": P.COLOR_TUB_DARK,
        "shape": model("tub"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Printed nylon internal frame with 4x N10 motor pockets, electronics bay, and guard bosses",
    },
    {
        "id": "bottom_plate",
        "kind": "structure",
        "material": "cf_plate",
        "process": "laser",
        "color": P.COLOR_GREEN_PLATE,
        "shape": model("bottom_plate"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "0.8 mm dark green carbon-fiber/FR4 bottom chassis plate",
    },
    {
        "id": "top_plate",
        "kind": "structure",
        "material": "cf_plate",
        "process": "laser",
        "color": P.COLOR_GREEN_PLATE,
        "shape": model("top_plate"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "0.8 mm dark green carbon-fiber/FR4 top chassis plate with switch & spinner slots",
    },

    # ---- Weapon uprights & top standoff rod ----
    {
        "id": "upright_l",
        "kind": "structure",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+x",
        "solid_fraction": 0.65,
        "color": P.COLOR_NYLON_WHITE,
        "shape": model("upright_l"),
        "at": [P.UPRIGHT_X_MID, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Left translucent white nylon weapon tower upright",
    },
    {
        "id": "upright_r",
        "kind": "structure",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+x",
        "solid_fraction": 0.65,
        "color": P.COLOR_NYLON_WHITE,
        "shape": model("upright_r"),
        "at": [-P.UPRIGHT_X_MID, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Right translucent white nylon weapon tower upright",
    },
    {
        "id": "top_rod",
        "kind": "structure",
        "material": "aluminium",
        "process": "lathe",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("top_rod"),
        "at": [0.0, P.UPRIGHT_TOP_Y, P.UPRIGHT_TOP_Z],
        "rot": [0.0, 0.0, 0.0],
        "label": "4 mm aluminium top standoff rod spanning between uprights",
    },

    # ---- Weapon assembly ----
    {
        "id": "weapon_motor_stator",
        "kind": "weapon_motor",
        "catalog": "gr1507",
        "at": [P.WPN_MOTOR_X, P.WPN_Y, P.WPN_Z],
        "rot": [0.0, 180.0, 0.0],
        "retained": "press_fit",
        "label": "GR1507 2850 kV weapon motor stator bolted to left upright",
    },
    {
        "id": "weapon_shaft",
        "kind": "shaft",
        "material": "titanium",
        "process": "lathe",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("weapon_shaft"),
        "parent": "weapon_disc",
        "at": [-P.WPN_DISC_X, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "4.0 mm steel live weapon shaft supported by MR84ZZ bearing and GR1507",
    },
    {
        "id": "bearing_r",
        "kind": "bearing",
        "designation": "MR84ZZ",
        "material": "steel",
        "process": "cots",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("bearing"),
        "at": [-P.UPRIGHT_X_MID, P.WPN_Y, P.WPN_Z],
        "rot": [0.0, 0.0, 0.0],
        "label": "MR84ZZ (4x8x3 mm) ball bearing in right upright",
    },
    {
        "id": "weapon_disc",
        "kind": "weapon",
        "material": "titanium",
        "process": "laser",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("weapon_disc"),
        "at": [P.WPN_DISC_X, P.WPN_Y, P.WPN_Z],
        "rot": [0.0, 0.0, 0.0],
        "joint": {
            "kind": "revolute",
            "axis": [1.0, 0.0, 0.0],
            "pivot": [P.WPN_DISC_X, P.WPN_Y, P.WPN_Z],
            "min": 0.0,
            "max": 360.0,
            "default": 0.0,
        },
        "weapon": {
            "kind": "vertical_disc",
            "motor": "weapon_motor_stator",
            "cells": 2,
            "reduction": 1.0,
            "spin_axis": [1.0, 0.0, 0.0],
            "locking_bar": "locking_bar",
        },
        "label": "56 mm OD x 1.5 mm titanium vertical spinner disc",
    },
    {
        "id": "weapon_motor_bell",
        "kind": "other",
        "catalog": "gr1507_can",
        "parent": "weapon_disc",
        "at": [P.WPN_MOTOR_X - P.WPN_DISC_X, 0.0, 0.0],
        "rot": [0.0, 180.0, 0.0],
        "label": "GR1507 rotating motor bell bolted to weapon disc",
    },
    {
        "id": "locking_bar",
        "kind": "locking_bar",
        "material": "pla",
        "process": "fdm",
        "print_orientation": "+z",
        "color": P.COLOR_LOCK_RED,
        "tethered": True,
        "shape": model("locking_bar"),
        "at": [6.0, P.WPN_Y - 4.0, P.WPN_Z + 16.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Removable high-visibility red weapon locking pin",
    },

    # ---- Blue TPU side guards ----
    {
        "id": "guard_l",
        "kind": "armor",
        "material": "tpu",
        "process": "fdm",
        "print_orientation": "+x",
        "solid_fraction": 0.65,
        "color": P.COLOR_TPU_BLUE,
        "shape": model("guard_l"),
        "at": [0.5 * (P.GUARD_X_IN + P.GUARD_X_OUT), 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Left royal-blue TPU side guard",
    },
    {
        "id": "guard_r",
        "kind": "armor",
        "material": "tpu",
        "process": "fdm",
        "print_orientation": "+x",
        "solid_fraction": 0.65,
        "color": P.COLOR_TPU_BLUE,
        "shape": model("guard_r"),
        "at": [-0.5 * (P.GUARD_X_IN + P.GUARD_X_OUT), 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Right royal-blue TPU side guard",
    },

    # ---- Orange fork mounts & titanium hinged forks ----
    {
        "id": "fork_mount_l",
        "kind": "structure",
        "material": "pla",
        "process": "fdm",
        "print_orientation": "+z",
        "color": P.COLOR_ORANGE_MOUNT,
        "shape": model("fork_mount_l"),
        "at": [P.FORK_X, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Left orange front fork clevis mount",
    },
    {
        "id": "fork_mount_r",
        "kind": "structure",
        "material": "pla",
        "process": "fdm",
        "print_orientation": "+z",
        "color": P.COLOR_ORANGE_MOUNT,
        "shape": model("fork_mount_r"),
        "at": [-P.FORK_X, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "label": "Right orange front fork clevis mount",
    },
    {
        "id": "fork_l",
        "kind": "other",
        "material": "titanium",
        "process": "laser",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("fork_l"),
        "at": [P.FORK_X, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "joint": {
            "kind": "revolute",
            "axis": [1.0, 0.0, 0.0],
            "pivot": [P.FORK_X, P.FORK_PIN_Y, P.FORK_PIN_Z],
            "min": 0.0,
            "max": 25.0,
            "default": 0.0,
        },
        "label": "Left 1.5 mm titanium hinged front fork",
    },
    {
        "id": "fork_r",
        "kind": "other",
        "material": "titanium",
        "process": "laser",
        "color": P.COLOR_METAL_SILVER,
        "shape": model("fork_r"),
        "at": [-P.FORK_X, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "joint": {
            "kind": "revolute",
            "axis": [1.0, 0.0, 0.0],
            "pivot": [-P.FORK_X, P.FORK_PIN_Y, P.FORK_PIN_Z],
            "min": 0.0,
            "max": 25.0,
            "default": 0.0,
        },
        "label": "Right 1.5 mm titanium hinged front fork",
    },

    # ---- Electronics ----
    {
        "id": "battery",
        "kind": "battery",
        "catalog": "lipo_2s_350",
        "at": P.BAT_AT,
        "rot": [0.0, 0.0, 90.0],
        "retained": "interlock",
        "label": "2S 350 mAh 30C LiPo battery",
    },
    {
        "id": "drive_rx",
        "kind": "esc",
        "catalog": "bbb_malenki_nano",
        "at": P.RX_AT,
        "rot": [0.0, 0.0, -90.0],
        "retained": "interlock",
        "label": "BBB Malenki-Nano receiver + dual brushed ESC",
    },
    {
        "id": "weapon_esc",
        "kind": "esc",
        "catalog": "bbb_brushless_esc_20a",
        "at": P.ESC_AT,
        "rot": [0.0, 0.0, 90.0],
        "retained": "interlock",
        "label": "BBB 20 A brushless weapon ESC",
    },
    {
        "id": "switch",
        "kind": "switch",
        "catalog": "fingertech_mini_switch",
        "at": P.SW_AT,
        "rot": [0.0, 0.0, 0.0],
        "retained": "press_fit",
        "tool_free": True,
        "marked": True,
        "label": "FingerTech Mini Power Switch (ON/OFF) under top plate slot",
    },
    {
        "id": "xt30",
        "kind": "connector",
        "catalog": "xt30u_m",
        "at": P.XT30_AT,
        "rot": [0.0, 0.0, 0.0],
        "retained": "interlock",
        "label": "XT30U-M power connector",
    },
]

# 4x Drive Motors + 4x Wheels
for pos_tag, wy in (("f", P.WHEEL_FRONT_Y), ("r", P.WHEEL_REAR_Y)):
    for side_tag, sx, rot_z in (("l", 1.0, 0.0), ("r", -1.0, 180.0)):
        tag = f"{pos_tag}{side_tag}"
        parts.append({
            "id": f"drive_motor_{tag}",
            "kind": "motor",
            "catalog": "bbb_n10_1000rpm",
            "at": [sx * P.MOTOR_X, wy, P.AXLE_Z],
            "rot": [0.0, 0.0, rot_z],
            "retained": "press_fit",
            "label": f"N10 1000 rpm drive motor ({tag})",
        })
        parts.append({
            "id": f"wheel_{tag}",
            "kind": "wheel",
            "material": "tpu",
            "process": "fdm",
            "print_orientation": "+x",
            "solid_fraction": 0.65,
            "color": P.COLOR_WHEEL_GRAY,
            "shape": model("wheel"),
            "at": [sx * P.WHEEL_X, wy, P.AXLE_Z],
            "rot": [0.0, 0.0, rot_z],
            "joint": {
                "kind": "revolute",
                "axis": [sx, 0.0, 0.0],
                "pivot": [sx * P.WHEEL_X, wy, P.AXLE_Z],
                "min": 0.0,
                "max": 360.0,
                "default": 0.0,
            },
            "label": f"26 mm OD x 6.5 mm wide wheel ({tag})",
        })

# ---- Fasteners ----
fasteners = []
for idx, (px, py) in enumerate([
    (-28.0, -47.0), (28.0, -47.0),
    (-30.0, -14.0), (30.0, -14.0),
    (-28.0, 19.0), (28.0, 19.0),
]):
    fasteners.append({
        "id": f"scr_top_{idx}",
        "designation": "M2x6",
        "head": "button",
        "tool": "hex1.5",
        "removable": True,
        "at": [px, py, P.TOP_PLATE_Z1],
        "dir": [0.0, 0.0, -1.0],
        "through": ["top_plate"],
        "threads_into": "tub",
        "hole": hole_m2(6.0, P.PLATE_T),
    })
    fasteners.append({
        "id": f"scr_bot_{idx}",
        "designation": "M2x6",
        "head": "button",
        "tool": "hex1.5",
        "removable": True,
        "at": [px, py, P.BOT_PLATE_Z0],
        "dir": [0.0, 0.0, 1.0],
        "through": ["bottom_plate"],
        "threads_into": "tub",
        "hole": hole_m2(6.0, P.PLATE_T),
    })

for sx, tag in ((1.0, "l"), (-1.0, "r")):
    for k, (gy, gz) in enumerate((
        (P.GUARD_MOUNT_Y1, P.GUARD_MOUNT_Z),
        (P.GUARD_MOUNT_Y2, P.GUARD_MOUNT_Z),
        (P.GUARD_MOUNT_Y3, P.GUARD_MOUNT_Z3),
    )):
        fasteners.append({
            "id": f"scr_guard_{tag}_{k}",
            "designation": "M2x8",
            "head": "button",
            "tool": "hex1.5",
            "removable": True,
            "at": [sx * P.GUARD_X_OUT, gy, gz],
            "dir": [-sx, 0.0, 0.0],
            "through": [f"guard_{tag}"],
            "threads_into": "tub",
            "hole": hole_m2(8.0, P.GUARD_X_OUT - P.GUARD_X_IN),
        })
    fasteners.append({
        "id": f"scr_rod_{tag}",
        "designation": "M2x6",
        "head": "button",
        "tool": "hex1.5",
        "removable": True,
        "at": [sx * P.UPRIGHT_X_OUT, P.UPRIGHT_TOP_Y, P.UPRIGHT_TOP_Z],
        "dir": [-sx, 0.0, 0.0],
        "through": [f"upright_{tag}"],
        "threads_into": "top_rod",
        "hole": hole_m2(6.0, P.UPRIGHT_T),
    })
    for k, py in enumerate((-6.0, 14.0)):
        fasteners.append({
            "id": f"scr_upright_{tag}_{k}",
            "designation": "M2x10",
            "head": "button",
            "tool": "hex1.5",
            "removable": True,
            "at": [sx * P.UPRIGHT_TAB_X, py, P.UPRIGHT_Z0 + 3.0],
            "dir": [0.0, 0.0, -1.0],
            "through": [f"upright_{tag}", "top_plate"],
            "threads_into": "tub",
            "hole": hole_m2(10.0, 3.0 + P.PLATE_T),
        })
    fasteners.append({
        "id": f"scr_fork_mount_{tag}",
        "designation": "M2x8",
        "head": "button",
        "tool": "hex1.5",
        "removable": True,
        "at": [sx * P.FORK_X, 26.5, 12.0],
        "dir": [0.0, -1.0, 0.0],
        "through": [f"fork_mount_{tag}"],
        "threads_into": "tub",
        "hole": hole_m2(8.0, 2.5),
    })

import math as _math  # noqa: E402
for idx, ang in enumerate((0, 90, 180, 270)):
    a = _math.radians(ang)
    fasteners.append({
        "id": f"scr_wpn_stator_{idx}",
        "designation": "M2x5",
        "head": "button",
        "tool": "hex1.5",
        "removable": True,
        "at": [P.UPRIGHT_X_OUT, P.WPN_Y + 6.0 * _math.cos(a), P.WPN_Z + 6.0 * _math.sin(a)],
        "dir": [-1.0, 0.0, 0.0],
        "through": ["upright_l"],
        "threads_into": "weapon_motor_stator",
        "hole": hole_m2(5.0, P.UPRIGHT_T),
    })

# ---- Connections ----
connections = [
    {"a": "fork_mount_l", "b": "tub", "method": "screw", "reason": "Bolted and socketed to front left chassis boss to carry fork impact loads"},
    {"a": "fork_mount_r", "b": "tub", "method": "screw", "reason": "Bolted and socketed to front right chassis boss to carry fork impact loads"},
    {"a": "fork_l", "b": "fork_mount_l", "method": "shaft", "reason": "Hinged on M2 steel cross-pin in left clevis"},
    {"a": "fork_r", "b": "fork_mount_r", "method": "shaft", "reason": "Hinged on M2 steel cross-pin in right clevis"},
    {"a": "weapon_motor_stator", "b": "upright_l", "method": "screw", "reason": "4x M2 screws bolt GR1507 stator to left upright"},
    {"a": "bearing_r", "b": "upright_r", "method": "press_fit", "interference_mm": 0.05, "reason": "MR84ZZ bearing seated in right upright bore"},
    {"a": "weapon_shaft", "b": "bearing_r", "method": "shaft", "reason": "4.0 mm live titanium weapon shaft supported by right MR84ZZ bearing"},
    {"a": "weapon_disc", "b": "weapon_shaft", "method": "press_fit", "interference_mm": 0.05, "reason": "Weapon disc keyed onto 4.0 mm live weapon shaft"},
    {"a": "weapon_motor_bell", "b": "weapon_disc", "method": "press_fit", "interference_mm": 0.05, "reason": "GR1507 bell cap press-fit and keyed onto weapon disc boss"},
    {"a": "locking_bar", "b": "upright_l", "method": "pin", "reason": "Removable safety locking pin inserted through upright and disc"},
    {"a": "battery", "b": "tub", "method": "interlock", "reason": "Captured in central battery bay pocket under top plate"},
    {"a": "drive_rx", "b": "tub", "method": "interlock", "reason": "Captured in left electronics bay pocket under top plate"},
    {"a": "weapon_esc", "b": "tub", "method": "interlock", "reason": "Captured in right electronics bay pocket under top plate"},
    {"a": "switch", "b": "tub", "method": "press_fit", "interference_mm": 0.1, "reason": "Captive in rear switch pocket under top plate slot"},
    {"a": "xt30", "b": "tub", "method": "interlock", "reason": "Captured in rear power harness bay pocket"},
]
for pos_tag in ("f", "r"):
    for side_tag in ("l", "r"):
        tag = f"{pos_tag}{side_tag}"
        connections.append({
            "a": f"drive_motor_{tag}",
            "b": "tub",
            "method": "interlock",
            "reason": f"N10 gearmotor ({tag}) boxed along Y and Z in printed tub cradle",
        })
        connections.append({
            "a": f"wheel_{tag}",
            "b": f"drive_motor_{tag}",
            "method": "press_fit",
            "interference_mm": 0.15,
            "reason": f"3 mm D-bore wheel ({tag}) pressed onto N10 output shaft",
        })

# ---- Wires ----
wires = [
    {"id": "w_bat_xt30", "from": "battery.xt30", "to": "xt30.mate", "awg": 20, "kind": "power", "slack_mm": 8.0},
    {"id": "w_xt30_sw", "from": "xt30.wire", "to": "switch.in", "awg": 20, "kind": "power", "slack_mm": 8.0, "via": [[11.5, -27.0, 17.5], [11.5, -25.0, 17.5], [3.0, -25.0, 17.5]]},
    {"id": "w_sw_rx", "from": "switch.out", "to": "drive_rx.bat", "awg": 22, "kind": "power", "slack_mm": 8.0, "via": [[-7.0, -24.0, 17.5], [-14.0, -24.0, 17.5]], "rotor_ok": "fork_r only swings 0..25 deg forward (y>=27.8); wire is inside sealed chassis"},
    {"id": "w_sw_esc", "from": "switch.out", "to": "weapon_esc.bat", "awg": 20, "kind": "power", "slack_mm": 8.0},
    {"id": "w_rx_esc", "from": "drive_rx.wpn", "to": "weapon_esc.rx", "awg": 28, "kind": "signal", "slack_mm": 8.0, "via": [[-14.0, -24.0, 17.5], [14.0, -24.0, 17.5]]},
    {"id": "w_esc_wpn", "from": "weapon_esc.motor", "to": "weapon_motor_stator.phases", "awg": 22, "kind": "motor", "slack_mm": 12.0, "via": [[11.5, 4.0, 22.75]], "rotor_ok": "fork_l only swings 0..25 deg forward (y>=27.8); wire is inside sealed chassis (y<=8)"},
    {"id": "w_rx_fl", "from": "drive_rx.m1", "to": "drive_motor_fl.terminals", "awg": 26, "kind": "motor", "slack_mm": 10.0, "via": [[-14.0, -24.0, 17.5], [12.0, -24.0, 17.5], [12.0, 4.0, 17.5]], "rotor_ok": "fork_r only swings 0..25 deg forward (y>=27.8); wire is inside sealed chassis"},
    {"id": "w_rx_rl", "from": "drive_rx.m1", "to": "drive_motor_rl.terminals", "awg": 26, "kind": "motor", "slack_mm": 10.0, "via": [[-14.0, -24.0, 17.5], [12.0, -24.0, 17.5]], "rotor_ok": "fork_r only swings 0..25 deg forward (y>=27.8); wire is inside sealed chassis"},
    {"id": "w_rx_fr", "from": "drive_rx.m2", "to": "drive_motor_fr.terminals", "awg": 26, "kind": "motor", "slack_mm": 10.0},
    {"id": "w_rx_rr", "from": "drive_rx.m2", "to": "drive_motor_rr.terminals", "awg": 26, "kind": "motor", "slack_mm": 10.0},
]

allow_overlap = [
    {"a": "wheel_fl", "b": "drive_motor_fl", "max_depth_mm": 2.5, "reason": "wheel pressed onto N10 output shaft"},
    {"a": "wheel_fr", "b": "drive_motor_fr", "max_depth_mm": 2.5, "reason": "wheel pressed onto N10 output shaft"},
    {"a": "wheel_rl", "b": "drive_motor_rl", "max_depth_mm": 2.5, "reason": "wheel pressed onto N10 output shaft"},
    {"a": "wheel_rr", "b": "drive_motor_rr", "max_depth_mm": 2.5, "reason": "wheel pressed onto N10 output shaft"},
    {"a": "weapon_shaft", "b": "upright_l", "max_depth_mm": 0.5, "reason": "5 mm shaft clearance in upright bore"},
    {"a": "weapon_shaft", "b": "upright_r", "max_depth_mm": 0.5, "reason": "5 mm shaft clearance in upright bore"},
    {"a": "weapon_shaft", "b": "weapon_disc", "max_depth_mm": 0.5, "reason": "5 mm shaft passes through disc"},
    {"a": "weapon_shaft", "b": "weapon_motor_stator", "max_depth_mm": 0.5, "reason": "5 mm through shaft in GR1507"},
    {"a": "weapon_shaft", "b": "weapon_motor_bell", "max_depth_mm": 2.0, "reason": "5 mm through shaft in GR1507"},
    {"a": "weapon_motor_bell", "b": "weapon_motor_stator", "max_depth_mm": 2.0, "reason": "0.4 mm outrunner motor airgap"},
    {"a": "locking_bar", "b": "upright_l", "max_depth_mm": 2.0, "reason": "removable safety locking pin"},
    {"a": "locking_bar", "b": "weapon_disc", "max_depth_mm": 2.0, "reason": "removable safety locking pin"},
]

spec = {
    "name": "Iceberg",
    "profile": "aws2025",
    "robot_type": "vertical_spinner",
    "locomotion": "roller",
    "generator": "make_spec.py",
    "parts": parts,
    "fasteners": fasteners,
    "connections": connections,
    "wires": wires,
    "allow_overlap": allow_overlap,
    "electronics": {
        "failsafe": True,
        "weapon_remote_disable": True,
        "radio": "2.4GHz",
        "cells": 2,
    },
    "claims": [
        {"id": "c_mass", "text": "Total mass <= 150 g", "metric": "mass_total_g", "op": "<=", "value": 150.0},
        {"id": "c_footprint", "text": "Fits within 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0},
    ],
}

out_path = os.path.join(HERE, "spec.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)
print(f"Wrote {out_path} ({len(parts)} parts, {len(fasteners)} fasteners, {len(wires)} wires)")
