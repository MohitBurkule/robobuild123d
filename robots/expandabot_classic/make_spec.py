"""Emit robots/expandabot_classic/spec.json from src/expandabot_classic/params.py."""
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

from expandabot_classic import params as P  # noqa: E402
from expandabot_classic import parts as PP  # noqa: E402


def model(part):
    return {"type": "model", "file": "src/build_expandabot_classic.py", "params": {"part": part}}


def r3(p):
    return [r3(v) if isinstance(v, (list, tuple)) else round(float(v), 4) for v in p]


LIFTED = "--lifted" in sys.argv
STOWED = "--stowed" in sys.argv
OUT_PATH = (
    "robots/expandabot_classic/spec_lifted.json" if LIFTED
    else "robots/expandabot_classic/spec_stowed.json" if STOWED
    else "robots/expandabot_classic/spec.json"
)

wedge_ang = math.degrees(math.atan2(P.WEDGE_Z1 - P.WEDGE_Z0, P.WEDGE_Y1 - P.WEDGE_Y0))
wedge_lift = 22.0 if LIFTED else 0.0
wedge_eff_ang = wedge_ang + wedge_lift
cb_dy = P.CROSSBAR_Y - P.WEDGE_Y0
cb_dist = cb_dy / math.cos(math.radians(wedge_ang))
cb_y = P.WEDGE_Y0 + cb_dist * math.cos(math.radians(wedge_eff_ang))
cb_z = P.WEDGE_Z0 + cb_dist * math.sin(math.radians(wedge_eff_ang))

parts = [
    {"id": "tub", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "color": "#1c1f22", "shape": model("tub"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "sharp_corners_ok": "Printed PLA tub internal screw bosses and lid pads meet the tub walls at 90-degree junctions; 1.6 mm wall thickness and 3.2 mm boss radii provide ample local stiffness.",
     "label": "black 3D-printed chassis tub with front bulkhead, rear wheel cutouts, and corner wing clevises"},
    {"id": "top_panel", "kind": "armor", "material": "cf_plate", "process": "laser",
     "color": "#1b1e23", "shape": model("top_panel"), "at": r3(PP.top_panel_at()), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1.5 mm carbon-fiber one-piece T-shaped top deck with wheel cutouts and switch travel slot"},
    {"id": "side_l", "kind": "armor", "material": "pc", "process": "laser",
     "color": "#2b593a", "shape": model("side_l"), "at": r3(PP.side_at(1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm dark-green PC left side plate"},
    {"id": "side_r", "kind": "armor", "material": "pc", "process": "laser",
     "color": "#2b593a", "shape": model("side_r"), "at": r3(PP.side_at(-1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm dark-green PC right side plate"},
    {"id": "wedge", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "color": "#1a1c1e", "shape": model("wedge"), "at": r3([0.0, P.WEDGE_Y0, P.WEDGE_Z0]), "rot": [wedge_eff_ang, 0.0, 0.0],
     "rotates_with": "wedge", "retained": "pin",
     "joint": {"kind": "revolute", "axis": [1.0, 0.0, 0.0], "pivot": r3([0.0, P.WEDGE_Y0, P.WEDGE_Z0]),
               "min": 0.0, "max": 24.0, "default": 0.0},
     "label": "black 3D-printed forked front lifter wedge with central window"},
    {"id": "crossbar", "kind": "other", "material": "steel", "process": "cots", "stock": "3 mm steel pin",
     "color": "#b8bec4", "shape": model("crossbar"), "parent": "wedge",
     "at": r3([0.0, cb_dist, 0.0]), "rot": [0.0, 0.0, 0.0], "rotates_with": "wedge", "retained": "press_fit",
     "label": "steel crossbar spanning the forked wedge window"},
    {"id": "nose_pin", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "color": "#e6e8eb", "shape": model("nose_pin"), "at": r3([0.0, P.BODY_Y1 + 0.5, P.NOSE_PIN_Z]), "rot": [0.0, 0.0, 0.0],
     "rotates_with": "fixed", "retained": "press_fit", "label": "white nylon nose stud on front bulkhead"},
    {"id": "horn", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "color": "#e6e8eb", "shape": model("horn"), "at": r3([P.SERVO_X + 10.0, P.SERVO_Y + 1.0, 19.5 if LIFTED else 16.5]),
     "rot": [20.0 if LIFTED else 0.0, 0.0, -40.0], "rotates_with": "fixed", "retained": "press_fit",
     "label": "white printed servo horn extending into open front-left bay"},
]

for s, tag in ((1, "l"), (-1, "r")):
    yaw = (-s * 165.0) if STOWED else (-s * P.WING_DEPLOY_DEG)
    parts += [
        {"id": f"bracket_{tag}", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
         "color": "#4a4e54", "shape": model(f"bracket_{tag}"),
         "at": r3([s * P.WING_PIVOT_X, P.WING_PIVOT_Y, P.WING_PIVOT_Z]), "rot": [0.0, 0.0, yaw],
         "rotates_with": f"bracket_{tag}", "retained": "pin",
         "joint": {"kind": "revolute", "axis": [0.0, 0.0, float(-s)],
                   "pivot": r3([s * P.WING_PIVOT_X, P.WING_PIVOT_Y, P.WING_PIVOT_Z]), "min": P.WING_FOLD_DEG, "max": 0.0, "default": 0.0},
         "label": f"dark-grey printed hinge bracket ({tag})"},
        {"id": f"wing_{tag}", "kind": "other", "material": "pc", "process": "laser",
         "color": "#a7d6bd", "shape": model(f"wing_{tag}"), "parent": f"bracket_{tag}",
         "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": f"bracket_{tag}",
         "label": f"pale-mint G10/PC expanding side wing ({tag})"},
        {"id": f"hinge_pin_{tag}", "kind": "pin", "material": "steel", "process": "cots", "stock": "M2 x 18 dowel pin",
         "color": "#b8bec4", "shape": model(f"hinge_pin_{tag}"),
         "at": r3([s * P.WING_PIVOT_X, P.WING_PIVOT_Y, P.WING_PIVOT_Z]), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
         "label": f"M2 steel hinge pin ({tag})"},
        {"id": f"wheel_{tag}", "kind": "wheel", "material": "tpu", "process": "fdm", "print_orientation": "+x",
         "color": "#8e9499", "shape": model(f"wheel_{tag}"),
         "at": r3([s * P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]), "rot": [0.0, 0.0, 0.0],
         "rotates_with": f"wheel_{tag}",
         "joint": {"kind": "revolute", "axis": [float(s), 0.0, 0.0],
                   "pivot": r3([s * P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]), "min": 0.0, "max": 360.0, "default": 0.0},
         "label": f"grooved grey TPU rear wheel ({tag})"},
        {"id": f"motor_{tag}", "kind": "motor", "catalog": P.DRIVE_MOTOR_ID, "retained": "press_fit",
         "at": r3([s * (P.MOTOR_ROOT_X - P.MOTOR_SHAFT["at"][0]), P.WHEEL_Y, P.AXLE_Z]),
         "rot": [0.0, 0.0, 0.0 if s > 0 else 180.0], "rotates_with": "fixed",
         "label": f"N10 gearmotor ({tag})"},
    ]

parts += [
    {"id": "servo", "kind": "servo", "catalog": P.SERVO_ID, "retained": "press_fit",
     "exposed": True, "exposed_reason": "Servo sits in the open front-left linkage bay for horn access and visual inspection, matching the classic Expandabot layout.",
     "color": "#1e5cb3", "at": r3([P.SERVO_X, P.SERVO_Y, P.SERVO_Z]), "rot": [90.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "blue SG90-class servo under the CF deck"},
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY_ID, "retained": "clamp",
     "at": r3([P.BAT_X, P.BAT_Y, P.BAT_Z]), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2S 180 mAh LiPo pack"},
    {"id": "esc", "kind": "esc", "catalog": P.ESC_ID, "retained": "tape",
     "at": r3([P.ESC_X, P.ESC_Y, P.ESC_Z]), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "Malenki Nano dual brushed ESC + receiver"},
    {"id": "switch", "kind": "switch", "catalog": P.SWITCH_ID, "tool_free": True, "marked": True,
     "at": r3([P.SWITCH_X, P.SWITCH_Y, P.SWITCH_Z]), "rot": [0.0, 0.0, 90.0], "rotates_with": "fixed",
     "label": "BBB ant switch under CF deck with elongated travel slot"},
]

HOLE_M2 = {"d": 2.0, "clearance_d": P.SCREW_CLEAR_D, "into": "through", "side": "head"}
fasteners = []
for i, (px, py) in enumerate(P.TOP_SCREWS_XY):
    parts.append({"id": f"insert_top_{i}", "kind": "insert", "catalog": "heatset_m2",
                  "at": r3([px, py, P.TUB_Z1 - P.INSERT_HALF_L]), "rot": [0.0, 0.0, 0.0],
                  "rotates_with": "fixed", "retained": "press_fit"})
    fasteners.append({"id": f"bolt_top_{i}", "designation": "M2x6", "material": "steel",
                      "at": r3([px, py, P.TOP_Z1]), "dir": [0.0, 0.0, -1.0],
                      "through": ["top_panel"], "threads_into": f"insert_top_{i}", "tool": "hex1.5",
                      "removable": True, "head": "button",
                      "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1",
                               "head_dk": 3.5, "head_k": 1.3, "grip": P.TOP_T}})

for s, tag in ((1, "l"), (-1, "r")):
    for i, sy in enumerate(P.SIDE_SCREW_YS):
        parts.append({"id": f"insert_side_{tag}{i}", "kind": "insert", "catalog": "heatset_m2",
                      "at": r3([s * (P.TUB_W / 2 - P.INSERT_HALF_L), sy, P.SIDE_SCREW_Z]), "rot": [0.0, 90.0, 0.0],
                      "rotates_with": "fixed", "retained": "press_fit"})
        fasteners.append({"id": f"bolt_side_{tag}{i}", "designation": "M2x6", "material": "steel",
                          "at": r3([s * (P.SIDE_X + P.SHEET_T / 2), sy, P.SIDE_SCREW_Z]), "dir": [-float(s), 0.0, 0.0],
                          "through": [f"side_{tag}"], "threads_into": f"insert_side_{tag}{i}", "tool": "hex1.5",
                          "removable": True, "head": "socket",
                          "hole": {**HOLE_M2, "length": 6.0, "head": "cap", "head_std": "ISO 4762",
                                   "head_dk": 3.8, "head_k": 2.0, "grip": P.SHEET_T}})
    yaw_deg = (-s * 165.0) if STOWED else (-s * P.WING_DEPLOY_DEG)
    yaw_rad = math.radians(yaw_deg)
    c_y, s_y = math.cos(yaw_rad), math.sin(yaw_rad)
    # Local wing outer face is at x_loc = s * (BRACKET_W / 2 + 0.05 + WING_T), y_loc = dy
    x_loc = s * (P.BRACKET_W / 2 + P.WING_GAP + P.WING_T)
    dx_in, dy_in = -s * c_y, -s * s_y
    for i, dy in enumerate(P.WING_SCREW_DYS):
        parts.append({"id": f"insert_wing_{tag}{i}", "kind": "insert", "catalog": "heatset_m2",
                      "parent": f"bracket_{tag}",
                      "at": r3([s * (P.BRACKET_W / 2 - P.INSERT_HALF_L), dy, 0.0]),
                      "rot": [0.0, 90.0, 0.0], "rotates_with": f"bracket_{tag}", "retained": "press_fit"})
        wx = s * P.WING_PIVOT_X + x_loc * c_y - dy * s_y
        wy = P.WING_PIVOT_Y + x_loc * s_y + dy * c_y
        fasteners.append({"id": f"bolt_wing_{tag}{i}", "designation": "M2x6", "material": "steel",
                          "at": r3([wx, wy, P.WING_PIVOT_Z]), "dir": r3([dx_in, dy_in, 0.0]),
                          "through": [f"wing_{tag}"], "threads_into": f"insert_wing_{tag}{i}", "tool": "hex1.5",
                          "removable": True, "head": "button",
                          "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1",
                                   "head_dk": 3.5, "head_k": 1.3, "grip": P.WING_T}})

connections = [
    {"a": "wedge", "b": "tub", "method": "shaft",
     "reason": "Printed PLA forked wedge pivots on a front bulkhead hinge pin while resting against the tub front seat."},
]
for i in range(len(P.TOP_SCREWS_XY)):
    connections.append(
        {"a": f"insert_top_{i}", "b": "tub", "method": "press_fit", "interference_mm": 0.1,
         "reason": "Heat-set M2 brass insert anchors into the printed PLA tub lid pad to carry top-plate clamp loads."}
    )
for tag in ("l", "r"):
    for i in range(len(P.SIDE_SCREW_YS)):
        connections.append(
            {"a": f"insert_side_{tag}{i}", "b": "tub", "method": "press_fit", "interference_mm": 0.1,
             "reason": "Heat-set M2 brass insert anchors into the printed PLA tub side boss to retain the outer PC side plate."}
        )
    for i in range(len(P.WING_SCREW_DYS)):
        connections.append(
            {"a": f"insert_wing_{tag}{i}", "b": f"bracket_{tag}", "method": "press_fit", "interference_mm": 0.1,
             "reason": "Heat-set M2 brass insert anchors into the printed PLA hinge bracket to clamp the PC side wing."}
        )
    connections += [
        {"a": f"motor_{tag}", "b": f"wheel_{tag}", "method": "press_fit", "interference_mm": 0.1, "mechanical_key": True,
         "reason": "TPU wheel hub with 3 mm D-bore presses onto the steel N10 D-shaft to transmit drive torque without slipping."},
        {"a": f"motor_{tag}", "b": "tub", "method": "interlock", "mechanical_key": True,
         "reason": "N10 gearmotor gearbox seats inside a closed-top printed PLA pocket in the tub to react drive torque and axial thrust."},
        {"a": f"hinge_pin_{tag}", "b": "tub", "method": "press_fit", "interference_mm": 0.1, "mechanical_key": True,
         "reason": "Steel M2 dowel pin presses into the upper and lower PLA corner clevis ears of the tub to carry radial wing impact shear."},
        {"a": f"wing_{tag}", "b": f"bracket_{tag}", "method": "interlock", "mechanical_key": True,
         "reason": "Laser-cut PC side wing is clamped flush against the printed PLA bracket face and retained by two M2 fasteners into heat-set inserts."},
    ]
connections += [
    {"a": "crossbar", "b": "wedge", "method": "press_fit", "interference_mm": 0.1,
     "reason": "Steel 3 mm crossbar presses into matching side bores in the PLA wedge rails to stiffen the forked prongs against lateral impacts."},
    {"a": "nose_pin", "b": "tub", "method": "press_fit", "interference_mm": 0.1,
     "reason": "Printed nylon-white nose stud presses into the 3.2 mm bore on the front PLA bulkhead for low-load visual alignment."},
    {"a": "servo", "b": "tub", "method": "press_fit", "interference_mm": 0.05,
     "reason": "CS07 servo case seats snugly in the front-left PLA bay between the floor, bulkhead, and CF top deck."},
    {"a": "horn", "b": "servo", "method": "shaft", "interference_mm": 0.05,
     "reason": "Printed PLA servo horn keys onto the servo output spline to transmit actuation torque to the expanding wing linkage."},
    {"a": "battery", "b": "tub", "method": "velcro",
     "reason": "2S 180 mAh LiPo pack seats inside the central PLA battery cradle and is strapped down with a velcro wrap against the tub floor."},
    {"a": "esc", "b": "tub", "method": "tape",
     "reason": "Lightweight Malenki Nano ESC/Rx is secured to the flat PLA bay floor with double-sided foam tape under the CF top tongue."},
    {"a": "switch", "b": "tub", "method": "press_fit",
     "reason": "BBB ant switch housing seats snugly in the printed PLA switch tray under the CF deck with its lever protruding through the slot."},
]

allow_overlap = [
    {"a": "motor_l", "b": "wheel_l", "max_depth_mm": 0.6, "reason": "D-bore hub interference on N10 D-shaft"},
    {"a": "motor_r", "b": "wheel_r", "max_depth_mm": 0.6, "reason": "D-bore hub interference on N10 D-shaft"},
    {"a": "hinge_pin_l", "b": "tub", "max_depth_mm": 0.15, "reason": "M2 hinge pin press-fit into clevis"},
    {"a": "hinge_pin_r", "b": "tub", "max_depth_mm": 0.15, "reason": "M2 hinge pin press-fit into clevis"},
    {"a": "nose_pin", "b": "tub", "max_depth_mm": 0.15, "reason": "nose stud press-fit into front bulkhead"},
    {"a": "horn", "b": "servo", "max_depth_mm": 0.4, "reason": "printed horn keyed onto servo output spline"},
]
for i in range(len(P.TOP_SCREWS_XY)):
    allow_overlap.append({"a": f"insert_top_{i}", "b": "tub", "max_depth_mm": 0.15, "reason": "heat-set press-fit"})
for tag in ("l", "r"):
    for i in range(len(P.SIDE_SCREW_YS)):
        allow_overlap.append({"a": f"insert_side_{tag}{i}", "b": "tub", "max_depth_mm": 0.15, "reason": "heat-set press-fit"})
    for i in range(len(P.WING_SCREW_DYS)):
        allow_overlap.append({"a": f"insert_wing_{tag}{i}", "b": f"bracket_{tag}", "max_depth_mm": 0.15, "reason": "heat-set press-fit"})

ROTOR_NOTE = (
    "All internal wires stay inside the chassis tub well behind the front bulkhead (Y <= 20 mm), "
    "so they never enter the external wedge or wing hinge sweep sectors [expires 2027-12-31]"
)
wires = [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 22, "kind": "power", "slack_mm": 6.0,
     "bundle": "pwr", "rotor_ok": ROTOR_NOTE, "via": r3([[-8.0, -4.0, 9.5], [-16.0, -10.0, 12.0]])},
    {"id": "w_sw_esc", "from": "switch.out", "to": "esc.bat", "awg": 22, "kind": "power", "slack_mm": 6.0,
     "bundle": "pwr", "rotor_ok": ROTOR_NOTE, "via": r3([[-18.0, -9.0, 15.0], [-22.5, 0.0, 10.0]])},
    {"id": "w_esc_ml", "from": "esc.m1", "to": "motor_l.terminals", "awg": 24, "kind": "power", "slack_mm": 6.0,
     "bundle": "drv", "rotor_ok": ROTOR_NOTE},
    {"id": "w_esc_mr", "from": "esc.m2", "to": "motor_r.terminals", "awg": 24, "kind": "power", "slack_mm": 6.0,
     "bundle": "drv", "rotor_ok": ROTOR_NOTE, "via": r3([[-10.0, -2.0, 6.5], [-10.0, -25.0, 10.0]])},
    {"id": "w_esc_srv", "from": "esc.bat", "to": "servo.signal", "awg": 26, "kind": "signal", "slack_mm": 6.0,
     "bundle": "sig", "rotor_ok": ROTOR_NOTE, "via": r3([[-2.0, 2.0, 6.0], [8.0, 2.0, 8.0]])},
]

spec = {
    "name": "Expandabot Classic (Team Bits Everywhere)",
    "profile": "aws2025",
    "robot_type": "wedge",
    "locomotion": "wheeled",
    "can_run_inverted": False,
    "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
    "parts": parts,
    "fasteners": fasteners,
    "wires": wires,
    "connections": connections,
    "allow_overlap": allow_overlap,
}

with open(OUT_PATH, "w") as f:
    json.dump(spec, f, indent=1)
print(f"wrote {OUT_PATH}: {len(parts)} parts, {len(fasteners)} fasteners")
