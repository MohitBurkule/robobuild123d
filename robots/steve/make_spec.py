"""Emit robots/steve/spec.json from the parametric dimensions in src/steve/params.py."""
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

from steve import params as P  # noqa: E402


def model(part):
    return {"file": "src/build_steve.py", "params": {"part": part}}


def r3(p):
    return [r3(v) if isinstance(v, (list, tuple)) else round(float(v), 4) for v in p]


lid_xc = (P.SLOT_W / 2.0 + P.TUB_W / 2.0) / 2.0
lid_yc = (P.TUB_REAR_Y + P.TUB_DECK_END_Y) / 2.0
lid_zc = P.LID_Z + P.LID_T / 2.0

# Scoop placement: tilted by -SCOOP_ANGLE_DEG around X so front lip sits at (0, SCOOP_TIP_Y, SCOOP_TIP_Z)
# In local frame, front lip is at (0, 0, 0). Rotated by -angle around X:
# local (0, 0, 0) -> world (0, SCOOP_TIP_Y, SCOOP_TIP_Z)
# local (0, SCOOP_LEN, 0) -> world (0, SCOOP_TIP_Y - SCOOP_LEN*cos(a), SCOOP_TIP_Z + SCOOP_LEN*sin(a))
scoop_rot_x = -P.SCOOP_ANGLE_DEG

parts = [
    {"id": "tub", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "color": "#0f3b1e", "model": model("tub"), "at": [0, 0, 0]},

    {"id": "lid_l", "kind": "structure", "material": "polycarbonate", "process": "cnc",
     "color": "#0f3b1e", "model": model("lid_l"), "at": r3([lid_xc, lid_yc, lid_zc])},
    {"id": "lid_r", "kind": "structure", "material": "polycarbonate", "process": "cnc",
     "color": "#0f3b1e", "model": model("lid_r"), "at": r3([-lid_xc, lid_yc, lid_zc])},

    {"id": "guard_l", "kind": "structure", "material": "polycarbonate", "process": "cnc",
     "color": "#0f3b1e", "model": model("guard_l"), "at": r3([P.GUARD_X + P.GUARD_T / 2.0, P.WHEEL_Y, P.AXLE_Z])},
    {"id": "guard_r", "kind": "structure", "material": "polycarbonate", "process": "cnc",
     "color": "#0f3b1e", "model": model("guard_r"), "at": r3([-(P.GUARD_X + P.GUARD_T / 2.0), P.WHEEL_Y, P.AXLE_Z])},

    {"id": "wheel_l", "kind": "wheel", "material": "tpu_95a", "process": "fdm",
     "color": "#222222", "model": model("wheel_l"), "at": r3([P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]),
     "joint": {"type": "revolute", "axis": [1, 0, 0], "anchor": [0, 0, 0], "range": [0, 360]}},
    {"id": "wheel_r", "kind": "wheel", "material": "tpu_95a", "process": "fdm",
     "color": "#222222", "model": model("wheel_r"), "at": r3([-P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]),
     "joint": {"type": "revolute", "axis": [-1, 0, 0], "anchor": [0, 0, 0], "range": [0, 360]}},

    {"id": "flipper", "kind": "weapon", "material": "pla", "process": "fdm", "print_orientation": "+x",
     "color": "#25282a", "model": model("flipper"), "at": r3([0, P.HINGE_Y, P.HINGE_Z]),
     "joint": {"type": "revolute", "axis": [1, 0, 0], "anchor": [0, 0, 0], "range": [0, P.FLIP_OPEN_DEG]}},

    {"id": "scoop", "kind": "weapon", "material": "al_6061", "process": "cnc",
     "color": "#b8c0c8", "model": model("scoop"),
     "at": r3([0, P.SCOOP_TIP_Y - P.HINGE_Y, P.SCOOP_TIP_Z - P.HINGE_Z]), "rot": [scoop_rot_x, 0, 0],
     "parent": "flipper"},

    {"id": "hinge_pin", "kind": "fastener", "material": "steel_mild",
     "color": "#888888", "model": model("hinge_pin"), "at": r3([0, P.HINGE_Y, P.HINGE_Z])},

    # Internal COTS electronics & drive
    {"id": "motor_l", "kind": "motor", "catalog": "n10_300rpm_6v",
     "at": r3([P.MOTOR_X_OFFSET, P.WHEEL_Y, P.AXLE_Z]), "rot": [0, 0, 180]},
    {"id": "motor_r", "kind": "motor", "catalog": "n10_300rpm_6v",
     "at": r3([-P.MOTOR_X_OFFSET, P.WHEEL_Y, P.AXLE_Z]), "rot": [0, 0, 0]},

    {"id": "servo", "kind": "actuator", "catalog": "servo_cs07",
     "at": r3([0, P.SERVO_Y, P.SERVO_Z]), "rot": [0, 90, 0]},
    {"id": "horn", "kind": "structure", "material": "pla", "process": "fdm",
     "color": "#333333", "model": model("horn"), "at": r3([0, P.HORN_Y, P.HORN_Z]),
     "joint": {"type": "revolute", "axis": [1, 0, 0], "anchor": [0, 0, 0], "range": [0, 60]}},

    {"id": "battery", "kind": "battery", "catalog": "lipo_2s_180",
     "at": r3([20.0, -2.0, P.GROUND_CLEARANCE + P.FLOOR_T + 5.0])},
    {"id": "esc_rx", "kind": "electronics", "catalog": "malenki_nano",
     "at": r3([-20.0, -2.0, P.GROUND_CLEARANCE + P.FLOOR_T + 3.0])},
    {"id": "switch", "kind": "electronics", "catalog": "switch_bbb_ant_rvrn2",
     "at": r3([-20.0, -28.0, P.GROUND_CLEARANCE + P.FLOOR_T + 3.0])},
]

spec = {
    "schema_version": "0.1",
    "name": "steve",
    "description": "Steve (Stewie) — UK 150g antweight rear-hinged flipper with wide brushed-metal front scoop and outboard wheel guards.",
    "units": "mm",
    "class": "uk_antweight",
    "mass_limit_g": 150.0,
    "envelope_mm": [101.6, 101.6, 101.6],
    "ground_z": 0.0,
    "parts": parts,
}

out_path = os.path.join(HERE, "spec.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2)
print("Wrote", out_path)
