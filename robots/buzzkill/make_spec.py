"""Emit robots/buzzkill/spec.json from the parametric dimensions in src/buzzkill/params.py.

Run from repo root: .venv312/bin/python robots/buzzkill/make_spec.py
"""

from __future__ import annotations

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

from buzzkill import params as P  # noqa: E402


def model(part: str) -> dict:
    return {"type": "model", "file": "src/buzzkill/parts.py", "params": {"part": part}}


def r3(v):
    if isinstance(v, (list, tuple)):
        return [r3(x) for x in v]
    return round(float(v), 4)


parts = [
    {
        "id": "tub",
        "kind": "structure",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+z",
        "design_wall_mm": P.WALL,
        "shape": model("tub"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "sharp_corners_ok": "FDM printed nylon unibody; 0.4 mm nozzle rounds internal pocket corners in practice [expires 2027-12-31]",
        "label": "Printed black nylon stealth tub with integral outboard weapon upright, wheel wells, and COTS bays",
    },
    {
        "id": "lid",
        "kind": "armor",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+z",
        "design_wall_mm": P.LID_T,
        "shape": model("lid"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "Printed black nylon top lid with slotted grooves, triangular pockets, and switch cutout",
    },
    {
        "id": "hoop",
        "kind": "other",
        "material": "nylon",
        "process": "fdm",
        "print_orientation": "+y",
        "shape": model("hoop"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "Self-righting arch spanning over top of chassis, bolted to both sides",
    },
    # Weapon motor (fixed stator + rotating bell)
    {
        "id": "weapon_motor",
        "kind": "weapon_motor",
        "catalog": f"{P.WEAPON_MOTOR}__fixed",
        "at": r3([P.X_MOT, P.Y_AX, P.Z_AX]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "BBB BE1806 2300kV fixed stator & base mounted to outboard upright",
    },
    {
        "id": "weapon_motor_bell",
        "kind": "other",
        "catalog": f"{P.WEAPON_MOTOR}__bell",
        "at": r3([P.X_MOT, P.Y_AX, P.Z_AX]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "weapon",
        "joint": {
            "kind": "revolute",
            "axis": [1.0, 0.0, 0.0],
            "pivot": r3([P.X_MOT, P.Y_AX, P.Z_AX]),
            "min": 0.0,
            "max": 360.0,
            "default": 0.0,
        },
        "label": "BBB BE1806 2300kV rotating bell",
    },
    {
        "id": "wshaft",
        "kind": "shaft",
        "material": "titanium",
        "process": "bought",
        "stock": "4mm_rod",
        "volume_mm3": 387.0,
        "shape": model("wshaft"),
        "at": r3([P.X_MOT, P.Y_AX, P.Z_AX]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
        "label": "4 mm titanium dead-shaft running from outboard upright through bell & disc into inboard MR84 bearing",
    },
    {
        "id": "wbearing",
        "kind": "bearing",
        "material": "steel",
        "process": "bought",
        "designation": "MR84",
        "stock": "MR84",
        "shape": model("wbearing"),
        "at": r3([0.0, P.Y_AX, P.Z_AX]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
        "label": "MR84 (4x8x3 mm) inboard weapon shaft bearing",
    },
    {
        "id": "disc",
        "kind": "weapon",
        "material": "aluminium",
        "process": "milled",
        "volume_mm3": 6800,
        "shape": model("disc"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "weapon",
        "parent": "weapon_motor_bell",
        "weapon": {
            "kind": "disc",
            "motor": "weapon_motor",
            "cells": 2,
            "reduction": 1.0,
            "spin_axis": [1.0, 0.0, 0.0],
            "locking_bar": "locking_bar",
        },
        "label": "CNC-milled 7075 aluminium 45 mm vertical drisk wrapping around BE1806 bell",
    },
    {
        "id": "locking_bar",
        "kind": "locking_bar",
        "material": "titanium",
        "process": "bought",
        "stock": "3mm_rod",
        "shape": model("locking_bar"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
        "label": "3 mm titanium weapon locking pin",
    },
    # Laser-cut weapon uprights (keeps printed tub free of axle peel loads)
    {
        "id": "upright_outboard",
        "kind": "structure",
        "material": "titanium",
        "process": "laser",
        "shape": model("upright_outboard"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "2.0 mm laser-cut titanium outboard weapon motor upright",
    },
    {
        "id": "upright_inboard",
        "kind": "structure",
        "material": "aluminium",
        "process": "milled",
        "volume_mm3": 1200,
        "shape": model("upright_inboard"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "2.0 mm CNC-milled aluminium inboard MR52 bearing plate",
    },
    # Front wedgelets / forks
    {
        "id": "fork_l",
        "kind": "fork",
        "material": "titanium",
        "process": "laser",
        "secondary_ops": ["countersink"],
        "shape": model("fork_l"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.5 mm laser-cut titanium left front wedgelet",
    },
    {
        "id": "fork_r",
        "kind": "fork",
        "material": "titanium",
        "process": "laser",
        "secondary_ops": ["countersink"],
        "shape": model("fork_r"),
        "at": [0.0, 0.0, 0.0],
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "label": "1.5 mm laser-cut titanium right front wedgelet",
    },
    # Drive motors & wheels
    {
        "id": "drive_motor_l",
        "kind": "motor",
        "catalog": P.DRIVE_MOTOR,
        "at": r3([P.MOTOR_X, P.DRIVE_Y, P.DRIVE_Z]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    },
    {
        "id": "drive_motor_r",
        "kind": "motor",
        "catalog": P.DRIVE_MOTOR,
        "at": r3([-P.MOTOR_X, P.DRIVE_Y, P.DRIVE_Z]),
        "rot": [0.0, 0.0, 180.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    },
    {
        "id": "wheel_l",
        "kind": "wheel",
        "catalog": P.WHEEL,
        "at": r3([P.WHEEL_X, P.DRIVE_Y, P.DRIVE_Z]),
        "rot": [0.0, 0.0, 0.0],
        "retained": "press_fit",
    },
    {
        "id": "wheel_r",
        "kind": "wheel",
        "catalog": P.WHEEL,
        "at": r3([-P.WHEEL_X, P.DRIVE_Y, P.DRIVE_Z]),
        "rot": [0.0, 0.0, 180.0],
        "retained": "press_fit",
    },
    # Electronics
    {
        "id": "battery",
        "kind": "battery",
        "catalog": P.BATTERY,
        "at": r3(P.BAT_AT),
        "rot": r3(P.BAT_ROT),
        "rotates_with": "fixed",
        "retained": "pocket",
    },
    {
        "id": "drive_esc",
        "kind": "esc",
        "catalog": P.DRIVE_ESC,
        "at": r3(P.DESC_AT),
        "rot": r3(P.DESC_ROT),
        "rotates_with": "fixed",
        "retained": "tape",
    },
    {
        "id": "weapon_esc",
        "kind": "esc",
        "catalog": P.WEAPON_ESC,
        "at": r3(P.WESC_AT),
        "rot": r3(P.WESC_ROT),
        "rotates_with": "fixed",
        "retained": "tape",
    },
    {
        "id": "power_switch",
        "kind": "switch",
        "catalog": P.SWITCH,
        "at": r3(P.SW_AT),
        "rot": r3(P.SW_ROT),
        "rotates_with": "fixed",
        "retained": "press_fit",
        "tool_free": True,
        "marked": True,
        "label": "FingerTech mini power switch ON/OFF (top-left deck)",
    },
]

def _hole(length: float, grip: float, head: str = "socket") -> dict:
    if head == "csk":
        return {
            "d": 2.0, "length": length, "head": "csk", "head_std": "ISO 10642",
            "head_dk": 4.4, "head_k": 1.2, "clearance_d": 2.3, "into": "through",
            "side": "head", "csk_angle": 90.0, "csk_d": 4.4, "csk_depth": 1.2, "sink": 0.0, "grip": grip,
        }
    return {
        "d": 2.0, "length": length, "head": "socket", "head_std": "ISO 4762",
        "head_dk": 3.8, "head_k": 2.0, "clearance_d": 2.3, "into": "through",
        "side": "head", "sink": 0.0, "grip": grip,
    }


# Heat-set inserts for lid screws
fasteners = []
for i, (sx, sy) in enumerate(P.LID_SCREWS):
    ins_id = f"ins_lid_{i}"
    parts.append({
        "id": ins_id,
        "kind": "insert",
        "catalog": "heatset_m2",
        "at": r3([sx, sy, P.TUB_TOP_Z - P.INSERT_L / 2.0]),
        "rot": [0.0, 0.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    })
    fasteners.append({
        "id": f"scr_lid_{i}",
        "designation": "M2x6",
        "at": r3([sx, sy, P.TUB_TOP_Z + P.LID_T]),
        "dir": [0.0, 0.0, -1.0],
        "through": ["lid"],
        "threads_into": ins_id,
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "washer": True,
        "hole": _hole(6.0, P.LID_T),
    })

# 4x M2x4 weapon motor base screws through outboard titanium upright
for k, (dy, dz) in enumerate(((6.0, 0.0), (-6.0, 0.0), (0.0, 8.0), (0.0, -8.0))):
    fasteners.append({
        "id": f"scr_wmot_{k}",
        "designation": "M2x4",
        "at": r3([P.UPRIGHT_X0, P.Y_AX + dy, P.Z_AX + dz]),
        "dir": [1.0, 0.0, 0.0],
        "through": ["upright_outboard"],
        "threads_into": "weapon_motor",
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "washer": True,
        "hole": _hole(4.0, 2.0),
    })

# 2x M2x6 outboard upright-to-tub screws + heat-set inserts
for k, uy in enumerate((2.0, 10.0)):
    ins_id = f"ins_uout_{k}"
    parts.append({
        "id": ins_id,
        "kind": "insert",
        "catalog": "heatset_m2",
        "at": r3([P.UPRIGHT_X0 - 1.5, uy, -5.0]),
        "rot": [0.0, -90.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    })
    fasteners.append({
        "id": f"scr_uout_{k}",
        "designation": "M2x6",
        "at": r3([P.UPRIGHT_X1, uy, -5.0]),
        "dir": [-1.0, 0.0, 0.0],
        "through": ["upright_outboard"],
        "threads_into": ins_id,
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "washer": True,
        "hole": _hole(6.0, 2.0),
    })

# 2x M2x6 inboard bearing plate-to-tub screws + heat-set inserts (front tab, clear of disc)
for k, uz in enumerate((-5.0, 5.0)):
    ins_id = f"ins_uin_{k}"
    parts.append({
        "id": ins_id,
        "kind": "insert",
        "catalog": "heatset_m2",
        "at": r3([-4.0 + 1.5, 0.5, uz]),
        "rot": [0.0, 90.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    })
    fasteners.append({
        "id": f"scr_uin_{k}",
        "designation": "M2x6",
        "at": r3([-6.0, 0.5, uz]),
        "dir": [1.0, 0.0, 0.0],
        "through": ["upright_inboard"],
        "threads_into": ins_id,
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "washer": True,
        "hole": _hole(6.0, 2.0),
    })

# 4x M2x5 disc-to-bell screws
for k in range(4):
    ang = math.radians(45.0 + 90.0 * k)
    dy, dz = 4.5 * math.cos(ang), 4.5 * math.sin(ang)
    fasteners.append({
        "id": f"scr_disc_{k}",
        "designation": "M2x5",
        "at": r3([P.DISC_WEB_X1, P.Y_AX + dy, P.Z_AX + dz]),
        "dir": [-1.0, 0.0, 0.0],
        "through": ["disc"],
        "threads_into": "weapon_motor_bell",
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "hole": _hole(5.0, P.DISC_WEB_X1 - P.DISC_WEB_X0),
        "access_before": ["upright_inboard", "wbearing"],
        "reason": "disc bolted to BE1806 bell before inboard bearing plate is installed",
    })

# Hoop side-mount inserts + M2x5 screws
for side_name, s in (("l", 1.0), ("r", -1.0)):
    ins_id = f"ins_hoop_{side_name}"
    parts.append({
        "id": ins_id,
        "kind": "insert",
        "catalog": "heatset_m2",
        "at": r3([s * (P.BODY_HALF_W - 1.5), P.HOOP_Y, P.HOOP_Z_BASE]),
        "rot": [0.0, 90.0 if s < 0 else -90.0, 0.0],
        "rotates_with": "fixed",
        "retained": "press_fit",
    })
    fasteners.append({
        "id": f"scr_hoop_{side_name}",
        "designation": "M2x6",
        "at": r3([s * (P.BODY_HALF_W + 2.6), P.HOOP_Y, P.HOOP_Z_BASE]),
        "dir": [-s, 0.0, 0.0],
        "through": ["hoop"],
        "threads_into": ins_id,
        "tool": "hex1.5",
        "removable": True,
        "head": "socket",
        "washer": True,
        "hole": _hole(6.0, 2.6),
    })

# Fork inserts + M2x5 screws
for fname, fx, fy0 in (("fork_l", P.FORK_L_X, P.FORK_L_Y0), ("fork_r", P.FORK_R_X, P.FORK_R_Y0)):
    for j, fy in enumerate((fy0 + 3.0, fy0 + 9.0)):
        ins_id = f"ins_{fname}_{j}"
        parts.append({
            "id": ins_id,
            "kind": "insert",
            "catalog": "heatset_m2",
            "at": r3([fx, fy, P.TUB_FLOOR_Z + 2.2]),
            "rot": [0.0, 0.0, 0.0],
            "rotates_with": "fixed",
            "retained": "press_fit",
        })
        fasteners.append({
            "id": f"scr_{fname}_{j}",
            "designation": "M2x5",
            "at": r3([fx, fy, P.TUB_FLOOR_Z - 1.0]),
            "dir": [0.0, 0.0, 1.0],
            "through": [fname],
            "threads_into": ins_id,
            "tool": "hex1.5",
            "removable": True,
            "head": "countersunk",
            "hole": _hole(5.0, 1.5, head="csk"),
        })

wires = [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "power_switch.in", "awg": 18, "kind": "power", "slack_mm": 10,
     "via": [[59.0, 12.9, 2.0]]},
    {"id": "w_sw_desc", "from": "power_switch.out", "to": "drive_esc.bat", "awg": 22, "kind": "power", "slack_mm": 10},
    {"id": "w_sw_wesc", "from": "power_switch.out", "to": "weapon_esc.bat", "awg": 18, "kind": "power", "slack_mm": 10},
    {"id": "w_desc_ml", "from": "drive_esc.m1", "to": "drive_motor_l.terminals", "awg": 26, "kind": "motor", "slack_mm": 8},
    {"id": "w_desc_mr", "from": "drive_esc.m2", "to": "drive_motor_r.terminals", "awg": 26, "kind": "motor", "slack_mm": 8},
    {"id": "w_desc_sig", "from": "drive_esc.wpn", "to": "weapon_esc.rx", "awg": 28, "kind": "signal", "slack_mm": 8},
    {"id": "w_wesc_wm", "from": "weapon_esc.motor", "to": "weapon_motor.phases", "awg": 20, "kind": "motor", "slack_mm": 12,
     "via": [[-24.0, 0.0, -5.0], [-24.0, 14.5, 5.0]], "rotor_ok": True},
]

connections = [
    {"a": "upright_inboard", "b": "wbearing", "method": "press_fit", "interference_mm": 0.08,
     "reason": "MR52 bearing pressed into inboard aluminium upright carries radial weapon shaft load"},
    {"a": "wbearing", "b": "wshaft", "method": "shaft",
     "reason": "2 mm weapon shaft turns inside MR52 inner race"},
    {"a": "weapon_motor", "b": "weapon_motor_bell", "method": "shaft",
     "reason": "BE1806 outrunner bell rotates on motor internal bearings"},
    {"a": "drive_motor_l", "b": "wheel_l", "method": "shaft", "interference_mm": 0.3,
     "reason": "DuraHubs 25 mm wheel pressed onto left N10 D-shaft"},
    {"a": "drive_motor_r", "b": "wheel_r", "method": "shaft", "interference_mm": 0.3,
     "reason": "DuraHubs 25 mm wheel pressed onto right N10 D-shaft"},
    {"a": "tub", "b": "drive_motor_l", "method": "press_fit", "interference_mm": 0.1,
     "reason": "Left N10 gearmotor captured in closed tub motor pocket"},
    {"a": "tub", "b": "drive_motor_r", "method": "press_fit", "interference_mm": 0.1,
     "reason": "Right N10 gearmotor captured in closed tub motor pocket"},
    {"a": "tub", "b": "battery", "method": "velcro", "mechanical_key": True,
     "reason": "2S 450mAh LiPo strapped into internal battery bay with retaining rails"},
    {"a": "tub", "b": "drive_esc", "method": "tape", "mechanical_key": True,
     "reason": "Malenki-Nano mounted with double-sided foam tape and retaining rails on tub floor"},
    {"a": "tub", "b": "weapon_esc", "method": "tape", "mechanical_key": True,
     "reason": "20A brushless ESC mounted with double-sided foam tape and retaining pocket on tub floor"},
    {"a": "tub", "b": "power_switch", "method": "press_fit", "interference_mm": 0.05,
     "reason": "FingerTech mini switch seated in top-left switch pocket under lid"},
    {"a": "upright_outboard", "b": "locking_bar", "method": "pin",
     "reason": "3 mm titanium locking pin slides through outboard upright bore to lock weapon disc"},
]

spec = {
    "name": "buzzkill",
    "profile": "aws2025",
    "robot_type": "vertical_spinner",
    "generator": "make_spec.py",
    "parts": parts,
    "fasteners": fasteners,
    "wires": wires,
    "connections": connections,
    "allow_overlap": [
        {"a": "drive_motor_l", "b": "wheel_l", "max_depth_mm": 0.3,
         "reason": "N10 3mm D-shaft press fit into DuraHubs 25mm wheel bore"},
        {"a": "drive_motor_r", "b": "wheel_r", "max_depth_mm": 0.3,
         "reason": "N10 3mm D-shaft press fit into DuraHubs 25mm wheel bore"},
        {"a": "wshaft", "b": "wbearing", "max_depth_mm": 0.15,
         "reason": "4mm weapon shaft running fit inside MR84 bearing inner race"},
        {"a": "wshaft", "b": "weapon_motor", "max_depth_mm": 0.5,
         "reason": "4mm dead-shaft passes through BE1806 stator bore"},
        {"a": "weapon_motor_bell", "b": "wshaft", "max_depth_mm": 0.5,
         "reason": "4mm dead-shaft passes through BE1806 bell center bore"},
    ],
    "electronics": {
        "failsafe": True,
        "weapon_remote_disable": True,
        "radio": "2.4 GHz",
        "cells": 2,
    },
    "claims": [
        {"id": "c_mass", "text": "weighs 150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150},
        {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150},
    ],
}

out_path = os.path.join(HERE, "spec.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)
print(f"Wrote {out_path} ({len(parts)} parts, {len(fasteners)} fasteners)")
