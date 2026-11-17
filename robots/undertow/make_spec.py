"""Regenerates robots/undertow/spec.json from src/undertow/params.py (run from the repo root):

  LD_LIBRARY_PATH=/tmp/usrlib/usr/lib/x86_64-linux-gnu .venv/bin/python robots/undertow/make_spec.py

All poses are computed from the params relations (catalogue frames included); edit params.py, then re-run this.
"""
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "robots", "undertow", "src"))
sys.path.insert(0, os.path.join(ROOT, "robots", "revron", "src"))
sys.path.insert(0, ROOT)

import build123d as bd

from robot import catalog
from robot.cad.holes import hole_tool
from robot.cad import fastener_catalog as fc

from undertow import params as P, drive, front_forks


def model(part):
    return {"type": "model", "file": "src/build_undertow.py", "params": {"part": part}}


def port_world(cid, at, rot, port, ports=None):
    e = catalog.find(cid)
    p = (ports or e.ports)[port]
    loc = bd.Pos(*at) * bd.Rot(*rot)
    w = loc * bd.Vertex(*p)
    return [round(w.X, 4), round(w.Y, 4), round(w.Z, 4)]


QUAD = {"fr": (1, 1), "fl": (-1, 1), "rr": (1, -1), "rl": (-1, -1)}
MOTOR_AT = {k: drive.motor_pose(sx, sy) for k, (sx, sy) in QUAD.items()}
WHEEL_AT = {k: drive.wheel_pose(sx, sy) for k, (sx, sy) in QUAD.items()}

# the N10's terminals port sits between its two solder tabs; declare the port on a tab face so the wire ends on metal
MOTOR_PORTS = {"terminals": [-12.75, 3.0, 0.0]}
TERM = {k: port_world(P.MOTOR_ID, MOTOR_AT[k][0], MOTOR_AT[k][1], "terminals", MOTOR_PORTS) for k in QUAD}

BAT_AT3 = [P.BAT_AT[0], P.BAT_AT[1], P.BAT_Z]
ESC_AT3 = [P.ESC_AT[0], P.ESC_AT[1], P.ESC_Z]
SW_AT3 = [P.SWITCH_AT[0], P.SWITCH_AT[1], P.SWITCH_Z]
RX_AT3 = [P.RX_AT[0], P.RX_AT[1], P.RX_AT[2]]

BAT_PORT = list(catalog.find(P.BATTERY_ID).ports)[0]
P_BAT = port_world(P.BATTERY_ID, BAT_AT3, P.BAT_ROT, BAT_PORT)
P_SW_IN = port_world(P.SWITCH_ID, SW_AT3, P.SWITCH_ROT, "in")
P_SW_OUT = port_world(P.SWITCH_ID, SW_AT3, P.SWITCH_ROT, "out")
P_ESC_BAT = port_world(P.ESC_ID, ESC_AT3, P.ESC_ROT, "bat")
P_ESC_M1 = port_world(P.ESC_ID, ESC_AT3, P.ESC_ROT, "m1")
P_ESC_M2 = port_world(P.ESC_ID, ESC_AT3, P.ESC_ROT, "m2")
P_ESC_RX = port_world(P.ESC_ID, ESC_AT3, P.ESC_ROT, "rx")
P_RX_ESC = port_world(P.RX_ID, RX_AT3, P.RX_ROT, "esc")

HIGH_Z = 18.0     # wire highway: above every bay part, under the top plate, crosses the full-height rib band only at |y| < 14


def _v(*pts):
    return [list(p) for p in pts]


parts = [
    {"id": "tub", "kind": "structure", "material": P.TUB_MATERIAL, "process": "fdm", "print_orientation": "+z",
     "shape": model("tub"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "sharp_corners_ok": ("the flagged concave corners are where the lead slots and tap drills break through the rib / "
                          "pad faces: knife edges between two cuts in an open cavity, not load-bearing notches; every "
                          "structural wall is the full WALL 2.0 mm"),
     "label": "printed nylon shell: hollow cavity, 4 motor spine ribs with lead slots, 6 bolt columns, 6 skirt pads, front pivot cheeks + nyloc boss"},
    {"id": "top_plate", "kind": "structure", "material": P.PLATE_MATERIAL, "process": "waterjet",
     "secondary_ops": ["countersink"],
     "shape": model("top_plate"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1 mm carbon plate: wheel windows open through the side edges, 6x M2 csk, switch access hole"},
    {"id": "base_plate", "kind": "structure", "material": P.PLATE_MATERIAL, "process": "waterjet",
     "secondary_ops": ["countersink"],
     "shape": model("base_plate"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1 mm carbon plate (same outline as the top: invertible), wheel windows through the side edges, 6x M2 csk, switch access hole"},
    {"id": "skirt_r", "kind": "armor", "material": P.SKIRT_MATERIAL, "process": "sheet_bent",
     "shape": model("skirt_r"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "0.5 mm Ti gr5 side skirt, 2x M2 button into the printed flank pads"},
    {"id": "skirt_l", "kind": "armor", "material": P.SKIRT_MATERIAL, "process": "sheet_bent",
     "shape": model("skirt_l"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "0.5 mm Ti gr5 side skirt, 2x M2 button into the printed flank pads"},
    {"id": "skirt_rear", "kind": "armor", "material": P.SKIRT_MATERIAL, "process": "sheet_bent",
     "shape": model("skirt_rear"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "0.5 mm Ti gr5 rear skirt, 2x M2 button into the rear pads"},
]

for k in ("fr", "fl", "rr", "rl"):
    at, rot = MOTOR_AT[k]
    parts.append({"id": f"motor_{k}", "kind": "motor", "catalog": P.MOTOR_ID, "ports": MOTOR_PORTS,
                  "at": [round(v, 4) for v in at], "rot": [round(v, 4) for v in rot], "rotates_with": "fixed",
                  "retained": "clamp",
                  "retained_reason": "the wheel's D-bore is a press fit on the motor shaft and clamps the gearbox face against the spine rib; the rib carries the push load",
                  "label": "N10 gearmotor in its bay, back face on the spine rib, shaft outboard"})

for k in ("fr", "fl", "rr", "rl"):
    at, rot = WHEEL_AT[k]
    sx, sy = QUAD[k]
    parts.append({"id": f"wheel_{k}", "kind": "wheel", "catalog": P.WHEEL_ID,
                  "at": [round(v, 4) for v in at], "rot": [round(v, 4) for v in rot],
                  "joint": {"kind": "revolute", "axis": [1.0, 0.0, 0.0],
                            "pivot": [round(sx * P.X_WHEEL_C, 4), round(sy * P.Y_AXLE, 4), P.Z_AXLE],
                            "min": 0.0, "max": 360.0, "default": 0.0},
                  "retained": "press_fit",
                  "retained_reason": "D-bore press fit (0.05 mm interference) on the 3 mm motor shaft: the flat carries the torque and the fit holds axially",
                  "label": "22x10 wheel on the motor shaft, proud of both plates by 1.5 mm"})

fork_xs = front_forks.fork_xs()
for i, x in enumerate(fork_xs):
    parts.append({"id": f"fork_{i}", "kind": "other", "material": "steel", "process": "laser",
                  "shape": model(f"fork_{i}"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0],
                  "rotates_with": "forks",
                  "joint": {"kind": "revolute", "axis": [1.0, 0.0, 0.0],
                            "pivot": [round(x, 4), P.PIN_Y, P.PIN_Z], "min": P.FORK_SWING_MIN_DEG,
                            "max": P.FORK_SWING_MAX_DEG, "default": 0.0},
                  "label": "0.8 mm spring-steel fork tine on the M3 pivot pin, free to swing (self-levelling)"})

pin_len = fc.parse(P.PIN_SCREW).length
pin_head_d, pin_head_k = fc.head(fc.parse(P.PIN_SCREW).d, "cap")
parts.append({
    "id": "pivot_pin", "kind": "pin", "material": "steel", "process": "lathe", "stock": "6 mm steel rod, M3 thread at the tip",
    "shape": {"type": "union", "items": [
        {"type": "place", "shape": {"type": "cylinder", "radius": fc.parse(P.PIN_SCREW).d / 2,
                                    "height": pin_len},
         "at": [-(P.CHEEK_HALF_X + P.CHEEK_T / 2) + pin_len / 2, P.PIN_Y, P.PIN_Z], "rot": [0.0, 90.0, 0.0]},
        {"type": "place", "shape": {"type": "cylinder", "radius": pin_head_d / 2, "height": pin_head_k},
         "at": [-(P.CHEEK_HALF_X + P.CHEEK_T / 2) - pin_head_k / 2, P.PIN_Y, P.PIN_Z], "rot": [0.0, 90.0, 0.0]},
    ]},
    "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
    "retained": "nut",
    "retained_reason": "M3 nyloc in the press-fit hex pocket of the +X cheek boss threads onto the pin's end and keys it against rotation; the cap head bears on the -X cheek",
    "label": "stocked M3x50 cap screw used as the pivot pin through both cheeks"})

parts += [
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY_ID,
     "at": [round(v, 4) for v in BAT_AT3], "rot": [round(v, 4) for v in P.BAT_ROT], "rotates_with": "fixed",
     "retained": "strap",
     "retained_reason": "pack sits on a foam pad bonded to the base plate and a poly strap over it (the strap carries the inverted load); the cavity walls capture it laterally",
     "label": "2S 180 mAh pack across the middle band, pigtail into the bay"},
    {"id": "esc", "kind": "esc", "catalog": P.ESC_ID,
     "at": [round(v, 4) for v in ESC_AT3], "rot": [round(v, 4) for v in P.ESC_ROT], "rotates_with": "fixed",
     "retained": "clamp",
     "retained_reason": "sits on a printed shelf that is one solid with the tub (top face at the ESC bottom); capture walls on +y/-y rise past its top and the shelf plate holds it down - the ESC case takes no adhesive and has no mounting holes",
     "label": "dual brushed ESC left of centre, ports fanned out (2 channels, 4 motors as 2 parallel pairs)"},
    {"id": "rx", "kind": "receiver", "catalog": P.RX_ID,
     "at": [round(v, 4) for v in RX_AT3], "rot": [round(v, 4) for v in P.RX_ROT], "rotates_with": "fixed",
     "retained": "adhesive",
     "retained_reason": "taped flat to the base plate south of the esc, pins toward the esc, antenna out along the wall away from the motors",
     "label": "decased FS-iA6 receiver flat at the left of the bay"},
    {"id": "switch", "kind": "switch", "catalog": P.SWITCH_ID,
     "at": [round(v, 4) for v in SW_AT3], "rot": [round(v, 4) for v in P.SWITCH_ROT], "rotates_with": "fixed",
     "retained": "clamp",
     "retained_reason": "the tub captures the body in a printed pocket: walls on +y and +x rise past its top, the -y inner rail and the motor rib close -y/-x; the actuator is tool-free through the access hole in both plates",
     "marked": True, "tool_free": True,
     "label": "FingerTech mini switch, actuator up, reachable through the access hole in both plates"},
    {"id": "nut_front", "kind": "nut", "catalog": "nut_m3_thin",
     "at": [P.CHEEK_HALF_X + P.CHEEK_T / 2 + P.NUT_BOSS_T - 1.2, P.PIN_Y, P.PIN_Z], "rot": [0.0, 90.0, 0.0],
     "rotates_with": "fixed",
     "label": "M3 nyloc in the press-fit hex pocket of the +X cheek boss, on the pivot pin"},
]

# ------------------------------------------------------------------------------------------------ fasteners
fasteners = []
for i, (x, y) in enumerate(P.BOLT_SITES):
    for side, z_face, axis in (("t", P.Z_TOP, (0.0, 0.0, -1.0)), ("b", P.Z_BASE, (0.0, 0.0, 1.0))):
        plate = "top_plate" if side == "t" else "base_plate"
        _, rec = hole_tool(at=(x, y, z_face), axis=axis, fastener=P.PLATE_SCREW, head=P.PLATE_HEAD,
                           into="tapped", grip=P.PLATE_T)
        fasteners.append(rec.to_spec(f"bolt_{side}{i}", through=[plate], threads_into="tub", tool="hex1.3",
                                     removable=True, material="steel"))
skirt_zc = (P.SKIRT_PAD_Z0 + P.SKIRT_PAD_Z1) / 2
for j, sy in enumerate((1, -1)):
    for side, sx in (("r", 1), ("l", -1)):
        _, rec = hole_tool(at=(sx * (P.SKIRT_X + P.SKIRT_T / 2), sy * P.SKIRT_PAD_Y, skirt_zc),
                           axis=(-sx, 0.0, 0.0), fastener=P.SKIRT_SCREW, head=P.SKIRT_SCREW_HEAD, into="tapped",
                           side="head", grip=P.SKIRT_T, cbore=0.0)
        fasteners.append(rec.to_spec(f"skirt_{side}{j}", through=[f"skirt_{side}"], threads_into="tub",
                                     tool="hex1.3", removable=True, material="steel"))
for j, sx in enumerate((1, -1)):
    _, rec = hole_tool(at=(sx * P.REAR_PAD_X, P.SKIRT_REAR_Y - P.SKIRT_T / 2, skirt_zc),
                       axis=(0.0, 1.0, 0.0), fastener=P.SKIRT_SCREW, head=P.SKIRT_SCREW_HEAD, into="tapped",
                       side="head", grip=P.SKIRT_T, cbore=0.0)
    fasteners.append(rec.to_spec(f"skirt_rear{j}", through=["skirt_rear"], threads_into="tub",
                                 tool="hex1.3", removable=True, material="steel"))

# ------------------------------------------------------------------------------------------------ wires
# Routes: up to the z=18 highway (above every bay part, under the plates; the full-height rib band at
# |y| >= 14 is crossed only at |y| < 14), along staggered lanes, then down and through the motor lead
# slots (x +-5.5..8.2, y +-22..30, z 9.5..12.5) to the terminals.
wires = [
    {"id": "w_bat_sw", "from": f"battery.{BAT_PORT}", "to": "switch.in",
     "awg": 24, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_BAT, (P_BAT[0], P_BAT[1], HIGH_Z), (P_BAT[0], -12.0, HIGH_Z), (4.5, -12.0, HIGH_Z),
         (4.5, P_SW_IN[1], P_SW_IN[2]), P_SW_IN)},
    {"id": "w_sw_esc", "from": "switch.out", "to": "esc.bat", "awg": 24, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_SW_OUT, (9.5, P_SW_OUT[1], P_SW_OUT[2]), (9.5, P_SW_OUT[1], HIGH_Z), (26.0, P_SW_OUT[1], HIGH_Z),
         (26.0, -8.0, HIGH_Z), (26.0, 6.0, P_ESC_BAT[2]), P_ESC_BAT)},
    {"id": "w_esc_rx", "from": "esc.rx", "to": "rx.esc", "awg": 26, "kind": "signal", "slack_mm": 8.0, "via": _v(
         P_ESC_RX, (20.5, -6.0, P_ESC_RX[2]), (20.5, -6.0, HIGH_Z),
         (P_RX_ESC[0] + 0.3, P_RX_ESC[1], HIGH_Z),
         (P_RX_ESC[0] + 0.3, P_RX_ESC[1], P_RX_ESC[2]), P_RX_ESC)},
    {"id": "w_m1_fr", "from": "esc.m1", "to": "motor_fr.terminals", "awg": 26, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_ESC_M1, (8.2, 12.5, P_ESC_M1[2]), (8.2, 12.5, HIGH_Z), (4.0, 12.5, HIGH_Z),
         (4.0, TERM["fr"][1], HIGH_Z), (4.0, TERM["fr"][1], TERM["fr"][2]), TERM["fr"])},
    {"id": "w_m1_fl", "from": "esc.m1", "to": "motor_fl.terminals", "awg": 26, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_ESC_M1, (8.2, 12.5, P_ESC_M1[2]), (8.2, 12.5, HIGH_Z), (-4.5, 12.5, HIGH_Z),
         (-4.5, TERM["fl"][1], HIGH_Z), (-4.5, TERM["fl"][1], TERM["fl"][2]), TERM["fl"])},
    {"id": "w_m2_rr", "from": "esc.m2", "to": "motor_rr.terminals", "awg": 26, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_ESC_M2, (17.9, 17.0, P_ESC_M2[2]), (17.9, 17.0, HIGH_Z), (17.9, -8.0, HIGH_Z),
         (4.0, -8.0, HIGH_Z), (4.0, TERM["rr"][1], HIGH_Z), (4.0, TERM["rr"][1], TERM["rr"][2]), TERM["rr"])},
    {"id": "w_m2_rl", "from": "esc.m2", "to": "motor_rl.terminals", "awg": 26, "kind": "power", "slack_mm": 8.0, "via": _v(
         P_ESC_M2, (17.2, 17.0, P_ESC_M2[2]), (17.2, 17.0, HIGH_Z), (17.2, 9.0, HIGH_Z),
         (-3.0, 9.0, HIGH_Z), (-3.0, TERM["rl"][1], HIGH_Z), (-3.0, TERM["rl"][1], TERM["rl"][2]), TERM["rl"])},
]

# ------------------------------------------------------------------------------------------------ connections
connections = []
for k in ("fr", "fl", "rr", "rl"):
    connections += [
        {"a": f"wheel_{k}", "b": f"motor_{k}", "method": "shaft",
         "reason": "the wheel's D-bore runs on the motor's 3 mm shaft: the flat carries the drive torque"},
        {"a": f"wheel_{k}", "b": f"motor_{k}", "method": "press_fit", "interference_mm": 0.05,
         "mechanical_key": True,
         "reason": "D-bore press fit on the shaft (the catalogue bore is r1.5, the shaft r1.5: 0.05 mm declared press) - holds the wheel axially"},
        {"a": f"motor_{k}", "b": "tub", "method": "interlock",
         "reason": "gearmotor back face seats on the spine rib and the wheel clamp pulls the gearbox face onto the rib; the rib carries the push load into the shell"},
    ]
for i in range(len(fork_xs)):
    connections.append({"a": f"fork_{i}", "b": "pivot_pin", "method": "shaft",
                        "reason": "the fork eye rides on the M3 pivot pin: free to swing about it, captured axially by the nyloc in the cheek boss"})
connections += [
    {"a": "pivot_pin", "b": "tub", "method": "press_fit",
     "reason": "the pin runs in the loose-clearance bores of both printed cheeks and is locked by the nyloc: it cannot walk"},
    {"a": "nut_front", "b": "pivot_pin", "method": "interlock",
     "reason": "M3 nyloc thread on the pin's end; the press-fit hex pocket in the cheek boss keys the nut"},
    {"a": "nut_front", "b": "tub", "method": "press_fit",
     "reason": "the nyloc sits in the press-fit hex pocket of the +X cheek boss"},
    {"a": "battery", "b": "base_plate", "method": "velcro",
     "reason": "foam pad bonded to the plate plus a poly strap over the pack: the strap carries the inverted load"},
    {"a": "esc", "b": "tub", "method": "interlock",
     "reason": "printed shelf + capture walls in the tub hold the ESC (case takes no adhesive, no mounting holes); the top plate caps it from above"},
    {"a": "rx", "b": "base_plate", "method": "tape",
     "reason": "taped to the base plate at the left, antenna along the wall away from the motors"},
    {"a": "switch", "b": "tub", "method": "interlock",
     "reason": "printed pocket in the tub clamps the body on all four sides, walls rise past the top; nothing tapable under it (1 mm carbon plate) so screws are impossible"},
]

allow_overlap = [
    {"a": f"wheel_{k}", "b": f"motor_{k}", "max_depth_mm": 1000.0,
     "reason": "the wheel is fused to its motor (D-bore press fit on the 3 mm shaft, D-flat keys the drive): coaxial with the revolute axis, so its revolved sweep envelope always contains the shaft - exact overlap 0.26 mm, allowed (probe --joint wheel_fr)"}
    for k in ("fr", "fl", "rr", "rl")
] + [
    {"a": f"fork_{i}", "b": "pivot_pin", "max_depth_mm": 1000.0,
     "reason": "the eye bore rides the pivot pin, coaxial with the revolute axis (PIN_CLEAR 3.8 on the M3 pin, 0.4 mm swing clearance); a revolved envelope always contains its own axle"}
    for i in range(len(fork_xs))
] + [
    {"a": f"fork_{i}", "b": "tub", "max_depth_mm": 2.5,
     "reason": "the fork blade (0.8 thick) swings through the arc slots cut for it; exact closest approach 0.60 mm (probe --joint fork_0) and the deepest tub member inside the sweep arc is the 2.0 mm rail (grid depth 2.0) - overlap depth is capped at 0.4 by the blade thickness"}
    for i in range(len(fork_xs))
] + [
    {"a": f"fork_{i}", "b": other, "max_depth_mm": 1.2,
     "reason": "the fork swings through the arc slots cut for it; the 1.0 mm plates inside the sweep arc are 0.5 deep and exact closest approach is 1.24 mm (probe --joint fork_0)"}
    for i in range(len(fork_xs)) for other in ("top_plate", "base_plate")
] + [
    {"a": f"fork_{i}", "b": f"motor_{k}", "max_depth_mm": 6.5,
     "reason": "the fork swings in its own x-plane (0.8 mm thick at x -17/0/+17) while the motors sit 17.7 mm outboard in x; the proxy sweep sphere covers the motor box but exact geometry never meets (motor can half-width 6.0)"}
    for i in range(len(fork_xs)) for k in ("fr", "fl", "rr", "rl")
]

spec = {
    "name": "Undertow (4WD invertible wedge / control bot)",
    "profile": "aws2025",
    "robot_type": "wedge",
    "locomotion": "roller",
    "archetype": "wedge",
    "size_rule": ("robot/profile.py aws2025: 150 mm floor square, no overhang at any height, no height limit. "
                  f"Derived: width {P.WIDTH_ALL:.1f} mm, length at rest {P.LENGTH_START:.1f} mm, height {P.Z_TOP:.1f} mm "
                  f"(limit {P.ENVELOPE_MAX} mm per side after the 1 mm margin): fits = {P.FITS_ENVELOPE}."),
    "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
    "can_run_inverted": True,
    "claims": [
        {"id": "c_mass", "text": "weighs 150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150.0},
        {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0},
    ],
    "parts": parts,
    "fasteners": fasteners,
    "wires": wires,
    "connections": connections,
    "allow_overlap": allow_overlap,
    "notes": ("Derived by the src/undertow relations; poses computed from params.py and the catalogue frames. "
              "4WD direct drive (N10 + 22x10 wheels, D-bore press fit), printed nylon shell between two 1 mm carbon "
              "plates (6x M2 csk each into printed columns), bolted 0.5 mm Ti skirts on printed pads, hinged spring-steel "
              "forks on a stocked M3x50 pivot pin with a nyloc in a press-fit hex pocket. Wheels drop out -z through the "
              "plate windows; motors and electronics lift out +z; forks slide off the pin. Wires run on a z=18 highway "
              "through the motor lead slots to the terminals."),
}

out = os.path.join(ROOT, "robots", "undertow", "spec.json")
with open(out, "w") as f:
    json.dump(spec, f, indent=1)
print("spec written:", out)
print("width %.1f length %.1f fits %s | parts %d fasteners %d wires %d" % (
    P.WIDTH_ALL, P.LENGTH_START, P.FITS_ENVELOPE, len(parts), len(fasteners), len(wires)))
print("ports: bat", P_BAT, "sw_in", P_SW_IN, "sw_out", P_SW_OUT, "esc_bat", P_ESC_BAT, "m1", P_ESC_M1, "m2", P_ESC_M2,
      "rx_esc", P_ESC_RX, "rx", P_RX_ESC)
print("terms:", {k: TERM[k] for k in TERM})
