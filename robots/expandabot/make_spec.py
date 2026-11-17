"""Emit robots/expandabot/spec.json from the parametric dimensions in src/expandabot/params.py.

Every part is built in its own local frame by src/build_expandabot.py (build(part=...)) and placed here by at/rot.
Moving parts carry a revolute joint in the spec:
  flipper (+ child hinge_block + child inserts)  revolute about X at (0, HINGE_Y, HINGE_Z), range [0, FLIP_OPEN_DEG]
  horn (+ child drive_pin)                       revolute about X at (0, SERVO_OUT_Y, SERVO_OUT_Z), range [0, HORN_MAX_DEG]
  wheel_l, wheel_r                               revolute about +-X at (±WHEEL_X, WHEEL_Y, AXLE_Z), range [0, 360]

Run from the repo root:  python robots/expandabot/make_spec.py
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

from expandabot import params as P  # noqa: E402
from expandabot import parts as PP  # noqa: E402


def model(part):
    return {"type": "model", "file": "src/build_expandabot.py", "params": {"part": part}}


def r3(p):
    return [r3(v) if isinstance(v, (list, tuple)) else round(float(v), 4) for v in p]


# ---- hinge & clamp frame helpers (world at rest) -----------------------------------------------
def hinge_at(x, y, z):
    wy, wz = P.hinge_point(y, z)
    return r3([x, wy, wz])


def hinge_dir_z():
    """World direction of the hinge-frame -Z (the hinge-block screw axis)."""
    a = math.radians(P.FLIP_REST_DEG)
    return r3([0.0, -math.sin(a), -math.cos(a)])


def clamp_at(s, dx, y, z):
    wy, wz = P.clamp_point(y, z)
    return r3([s * P.CLAMP_X + dx, wy, wz])


def clamp_dir_z():
    """World direction of the clamp-frame -Z (the clamp-arm screw axis)."""
    a = math.radians(P.CLAMP_REST_DEG)
    return r3([0.0, -math.sin(a), -math.cos(a)])


# ---- parts -------------------------------------------------------------------------------------
parts = [
    {"id": "tub", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "shape": model("tub"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "sharp_corners_ok": "the flagged concave corners are the seams where the printed lid pads, standoff columns, "
                         "front clamp mounts, and servo/switch trays root into the tub walls and floor (all one FDM "
                         "print, 0.4 mm nozzle rounds them in practice; short compression bosses loaded in bearing) "
                         "[expires 2027-12-31]",
     "label": "printed red PLA tub: open top, servo tray with horn slot, two closed-top rear motor pockets, "
              "standoff columns, lid pads, sloped front clamp seats, outer hinge knuckles"},
    {"id": "lid_r", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("lid_r"), "at": r3(PP.lid_at(-1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1.5 mm PC right lid with the rounded switch slot"},
    {"id": "lid_l", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("lid_l"), "at": r3(PP.lid_at(1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1.5 mm PC left lid (mirror of the right without the switch slot)"},
    {"id": "side_r", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("side_r"), "at": r3(PP.side_at(-1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm PC right side guard plate (hexagon) on the standoff columns"},
    {"id": "side_l", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("side_l"), "at": r3(PP.side_at(1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm PC left side guard plate (mirror)"},
    {"id": "clamp_l", "kind": "wedge", "material": "pc", "process": "laser",
     "shape": model("clamp_l"), "at": r3([P.CLAMP_X, P.HINGE_Y, P.HINGE_Z]), "rot": [-P.CLAMP_REST_DEG, 0.0, 0.0],
     "rotates_with": "fixed",
     "label": "2 mm PC left lobster-claw clamping arm bolted to the tub's left sloped front mount, tip 0.8 mm off the floor"},
    {"id": "clamp_r", "kind": "wedge", "material": "pc", "process": "laser",
     "shape": model("clamp_r"), "at": r3([-P.CLAMP_X, P.HINGE_Y, P.HINGE_Z]), "rot": [-P.CLAMP_REST_DEG, 0.0, 0.0],
     "rotates_with": "fixed",
     "label": "2 mm PC right lobster-claw clamping arm (mirror) bolted to the tub's right sloped front mount"},
    {"id": "flipper", "kind": "other", "material": "pc", "process": "laser",
     "shape": model("flipper"), "at": r3([0.0, P.HINGE_Y, P.HINGE_Z]), "rot": [-P.FLIP_REST_DEG, 0.0, 0.0],
     "rotates_with": "flipper", "actuated_by": "servo",
     "joint": {"kind": "revolute", "axis": [1.0, 0.0, 0.0], "pivot": r3([0.0, P.HINGE_Y, P.HINGE_Z]),
               "min": 0.0, "max": P.FLIP_OPEN_DEG, "default": 0.0},
     "label": "2 mm PC central flipper blade between the lobster claws, hinged on the M2 pin and servo-driven via the tail lever"},
    {"id": "hinge_block", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "shape": model("hinge_block"), "parent": "flipper", "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0],
     "rotates_with": "flipper", "retained": "press_fit",
     "sharp_corners_ok": "the flagged concave corner is where the printed centre knuckle meets the web and seat box "
                         "(one FDM print, 0.4 mm nozzle rounds it; compression seat loaded in bearing) "
                         "[expires 2027-12-31]",
     "label": "printed centre knuckle + flipper seat (2x M2x8 into heat-sets) + tail lever, screwed to the flipper"},
    {"id": "hinge_pin", "kind": "pin", "material": "steel", "process": "cots", "stock": "M2 x 35 dowel pin as hinge pin",
     "shape": model("hinge_pin"), "at": r3([0.0, P.HINGE_Y, P.HINGE_Z]), "rot": [0.0, 0.0, 0.0],
     "rotates_with": "fixed",
     "label": "M2 steel hinge pin through all three knuckles, pressed into the tub's outer knuckles"},
    {"id": "horn", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+x",
     "shape": model("horn"), "at": r3([P.HORN_X, P.SERVO_OUT_Y, P.SERVO_OUT_Z]), "rot": [P.HORN_THETA0, 0.0, 0.0],
     "rotates_with": "horn",
     "joint": {"kind": "revolute", "axis": [1.0, 0.0, 0.0], "pivot": r3([0.0, P.SERVO_OUT_Y, P.SERVO_OUT_Z]),
               "min": 0.0, "max": P.HORN_MAX_DEG, "default": 0.0},
     "label": "printed servo horn: hub on the output spline, arm out to the pin tab"},
    {"id": "drive_pin", "kind": "other", "material": "steel", "process": "cots", "stock": "M2 x 16 dowel",
     "shape": model("drive_pin"), "parent": "horn", "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0],
     "rotates_with": "horn", "retained": "pin",
     "label": "M2 drive pin through the horn tab bore; bears on the tail end face (sits in its angular shadow)"},
]

for left in (True, False):
    s = 1 if left else -1
    tag = "l" if left else "r"
    parts.append({"id": f"wheel_{tag}", "kind": "wheel", "material": "tpu", "process": "fdm", "print_orientation": "+x",
                  "shape": model(f"wheel_{tag}"), "at": r3([s * P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]), "rot": [0.0, 0.0, 0.0],
                  "rotates_with": f"wheel_{tag}",
                  "joint": {"kind": "revolute", "axis": [float(s), 0.0, 0.0],
                            "pivot": r3([s * P.WHEEL_X, P.WHEEL_Y, P.AXLE_Z]), "min": 0.0, "max": 360.0, "default": 0.0},
                  "label": f"printed hub + TPU tyre ({'left' if left else 'right'} rear), D-bore on the N10 shaft"})
    parts.append({"id": f"motor_{tag}", "kind": "motor", "catalog": P.DRIVE_MOTOR_ID, "retained": "press_fit",
                  "at": r3([s * (P.MOTOR_ROOT_X - P.MOTOR_SHAFT["at"][0]), P.WHEEL_Y, P.AXLE_Z]),
                  "rot": [0.0, 0.0, 90.0 * (1 - s)], "rotates_with": "fixed",
                  "label": f"N10 gearmotor in its snug closed-top {'left' if left else 'right'} rear pocket"})

parts += [
    {"id": "servo", "kind": "servo", "catalog": P.SERVO_ID, "retained": "press_fit",
     "at": r3([0.0, P.SERVO_Y, P.SERVO_OUT_Z]), "rot": [90.0, 0.0, 90.0], "rotates_with": "fixed",
     "label": "SG90-class servo lying on its side in the centre tray, output axis along +X"},
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY_ID, "retained": "tape",
     "at": r3([0.0, P.BAT_Y, P.TUB_Z0 + P.WALL + P.BAT_H / 2]), "rot": [0.0, 0.0, 90.0], "rotates_with": "fixed",
     "label": "2S 180 mAh LiPo pack in the rear of the centre channel, taped down"},
    {"id": "esc", "kind": "esc", "catalog": P.ESC_ID, "retained": "tape",
     "at": r3([P.SIDE_ZONE_X, P.ESC_Y, P.TUB_Z0 + P.WALL + P.ESC_H / 2]), "rot": [0.0, 0.0, 90.0],
     "rotates_with": "fixed", "label": "Malenki Nano dual brushed ESC + receiver in the left side zone"},
    {"id": "switch", "kind": "switch", "catalog": P.SWITCH_ID, "tool_free": True, "marked": True,
     "at": r3([-P.SIDE_ZONE_X, P.SW_Y, PP.switch_z()]), "rot": [0.0, 0.0, 90.0], "rotates_with": "fixed",
     "label": "BBB ant switch on its tray in the right side zone, knob through the right lid slot, marked ON/OFF"},
]

# ---- inserts -----------------------------------------------------------------------------------
for s, ys, tag in ((1, P.LID_SCREWS_Y_L, "l"), (-1, P.LID_SCREWS_Y_R, "r")):
    for i, y in enumerate(ys):
        parts.append({"id": f"insert_lid_{tag}{i}", "kind": "insert", "catalog": "heatset_m2",
                      "at": r3([s * P.LID_PAD_X, y, P.TUB_Z1 - P.INSERT_HALF_L]), "rot": [0.0, 0.0, 0.0],
                      "rotates_with": "fixed", "retained": "press_fit",
                      "label": f"M2 heat-set in the {'left' if s > 0 else 'right'} lid pad"})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i, y in enumerate(P.STANDOFF_YS):
        for j, z in enumerate(P.PLATE_SCREWS_Z):
            parts.append({"id": f"insert_standoff_{tag}{i}{j}", "kind": "insert", "catalog": "heatset_m2",
                          "at": r3([s * (P.TUB_W / 2 + P.SPACER_L - P.INSERT_HALF_L), y, z]), "rot": [0.0, 90.0, 0.0],
                          "rotates_with": "fixed", "retained": "press_fit",
                          "label": f"M2 heat-set in the {'left' if s > 0 else 'right'} standoff column"})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i, (dx, by) in enumerate(P.CLAMP_BOLTS_XY):
        parts.append({"id": f"insert_clamp_{tag}{i}", "kind": "insert", "catalog": "heatset_m2",
                      "at": clamp_at(s, dx, by, -P.SHEET_T - P.INSERT_HALF_L),
                      "rot": [-P.CLAMP_REST_DEG, 0.0, 0.0], "rotates_with": "fixed", "retained": "press_fit",
                      "label": f"M2 heat-set in the {'left' if s > 0 else 'right'} front clamp seat"})
for i, x in enumerate((-P.HINGE_BOLT_X, P.HINGE_BOLT_X)):
    parts.append({"id": f"insert_hb{i}", "kind": "insert", "catalog": "heatset_m2",
                  "parent": "hinge_block", "at": r3([x, P.BOLT_HB_Y, -P.SHEET_T - P.SEAT_H / 2]),
                  "rot": [0.0, 0.0, 0.0], "rotates_with": "flipper", "retained": "press_fit",
                  "label": "M2 heat-set pressed into the hinge block's flipper seat"})

# ---- fasteners ---------------------------------------------------------------------------------
HOLE_M2 = {"d": 2.0, "clearance_d": P.SCREW_CLEAR_D, "into": "through", "side": "head"}
fasteners = []
for s, ys, tag in ((1, P.LID_SCREWS_Y_L, "l"), (-1, P.LID_SCREWS_Y_R, "r")):
    for i, y in enumerate(ys):
        fasteners.append({"id": f"bolt_lid_{tag}{i}", "designation": "M2x6", "material": "steel",
                          "at": r3([s * P.LID_PAD_X, y, P.LID_Z1]), "dir": [0.0, 0.0, -1.0],
                          "through": [f"lid_{tag}"], "threads_into": f"insert_lid_{tag}{i}", "tool": "hex1.5",
                          "removable": True, "head": "button",
                          "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1",
                                   "head_dk": 3.5, "head_k": 1.3, "grip": P.LID_T}})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i, y in enumerate(P.STANDOFF_YS):
        for j, z in enumerate(P.PLATE_SCREWS_Z):
            fasteners.append({"id": f"bolt_side_{tag}{i}{j}", "designation": "M2x6", "material": "steel",
                              "at": r3([s * (P.SIDE_X + P.SHEET_T / 2), y, z]), "dir": [-float(s), 0.0, 0.0],
                              "through": [f"side_{tag}"],
                              "threads_into": f"insert_standoff_{tag}{i}{j}", "tool": "hex1.5",
                              "removable": True, "head": "socket",
                              "hole": {**HOLE_M2, "length": 6.0, "head": "cap", "head_std": "ISO 4762",
                                       "head_dk": 3.8, "head_k": 2.0, "grip": P.SHEET_T}})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i, (dx, by) in enumerate(P.CLAMP_BOLTS_XY):
        fasteners.append({"id": f"bolt_clamp_{tag}{i}", "designation": "M2x6", "material": "steel",
                          "at": clamp_at(s, dx, by, 0.0), "dir": clamp_dir_z(),
                          "through": [f"clamp_{tag}"], "threads_into": f"insert_clamp_{tag}{i}", "tool": "hex1.5",
                          "removable": True, "head": "button",
                          "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1",
                                   "head_dk": 3.5, "head_k": 1.3, "grip": P.SHEET_T}})
for i, x in enumerate((-P.HINGE_BOLT_X, P.HINGE_BOLT_X)):
    fasteners.append({"id": f"bolt_hb{i}", "designation": "M2x8", "material": "steel",
                      "at": hinge_at(x, P.BOLT_HB_Y, 0.0), "dir": hinge_dir_z(),
                      "through": ["flipper"], "threads_into": f"insert_hb{i}", "tool": "hex1.5",
                      "removable": True, "head": "button",
                      "hole": {**HOLE_M2, "length": 8.0, "head": "button", "head_std": "ISO 7380-1",
                               "head_dk": 3.5, "head_k": 1.3, "grip": P.SHEET_T}})

# ---- connections -------------------------------------------------------------------------------
connections = []
for left in (True, False):
    tag = "l" if left else "r"
    connections.append({"a": f"motor_{tag}", "b": f"wheel_{tag}", "method": "press_fit",
                        "reason": "printed hub with a D-bore matching the flat of the 3 mm N10 D-shaft: the flat "
                                  "carries drive torque, the 0.1 mm interference stops the hub walking off",
                        "interference_mm": 0.1, "mechanical_key": True})
    connections.append({"a": f"motor_{tag}", "b": "tub", "method": "interlock",
                        "reason": "the motor is enclosed in a snug (0.05 mm/side) closed-top printed pocket that wraps "
                                  "it on five sides (walls, closed top, floor) with only the shaft hole open",
                        "mechanical_key": True})
for s, ys, tag in ((1, P.LID_SCREWS_Y_L, "l"), (-1, P.LID_SCREWS_Y_R, "r")):
    for i in range(len(ys)):
        connections.append({"a": f"insert_lid_{tag}{i}", "b": "tub", "method": "press_fit",
                            "reason": "M2 brass heat-set pressed hot into the lid pad bore", "interference_mm": 0.15})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i in range(len(P.STANDOFF_YS)):
        for j in range(len(P.PLATE_SCREWS_Z)):
            connections.append({"a": f"insert_standoff_{tag}{i}{j}", "b": "tub", "method": "press_fit",
                                "reason": "M2 brass heat-set pressed hot into the standoff column bore",
                                "interference_mm": 0.15})
    for i in range(len(P.CLAMP_BOLTS_XY)):
        connections.append({"a": f"insert_clamp_{tag}{i}", "b": "tub", "method": "press_fit",
                            "reason": "M2 brass heat-set pressed hot into the sloped front clamp seat bore",
                            "interference_mm": 0.15})
connections += [
    {"a": "hinge_pin", "b": "tub", "method": "press_fit",
     "reason": "the M2 hinge pin is pressed into the tub's two outer knuckles (0.1 mm interference)",
     "interference_mm": 0.1, "mechanical_key": True},
    {"a": "hinge_block", "b": "hinge_pin", "method": "none",
     "reason": "the block's centre knuckle (r1.3 bore) turns on the pin with 0.3 mm running clearance; the flipper "
               "joint locates it, the pin carries no torque"},
    {"a": "horn", "b": "drive_pin", "method": "pin", "clearance_mm": 0.05,
     "reason": "the M2 drive pin is pressed into the horn tab's through-bore and retained by the tail"},
    {"a": "servo", "b": "horn", "method": "shaft", "clearance_mm": 0.05,
     "reason": "the horn hub is keyed on the servo output spline; the pin on the tail carries the flipper torque",
     "mechanical_key": True},
    {"a": "servo", "b": "tub", "method": "press_fit", "interference_mm": 0.05,
     "reason": "the servo sits in a snug printed U-channel cavity that wraps it on four sides"},
    {"a": "battery", "b": "tub", "method": "tape",
     "reason": "the pack is kapton/velcro-taped into its floor bay"},
    {"a": "esc", "b": "tub", "method": "tape",
     "reason": "the Malenki is taped into its floor bay"},
    {"a": "switch", "b": "tub", "method": "press_fit",
     "reason": "the BBB switch slides into its snug printed tray, captured by the tray and the screwed lid"},
]
for i in range(2):
    connections.append({"a": f"insert_hb{i}", "b": "hinge_block", "method": "press_fit", "interference_mm": 0.15,
                        "reason": "M2 brass heat-set pressed hot into the block's seat bore"})

# ---- allow_overlap -----------------------------------------------------------------------------
allow_overlap = []
for left in (True, False):
    tag = "l" if left else "r"
    allow_overlap.append({"a": f"motor_{tag}", "b": f"wheel_{tag}", "max_depth_mm": 0.6,
                          "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the "
                                    "round part of the bore overlaps the round stand-in of the D-shaft by up to 0.5 mm"})
allow_overlap.append({"a": "hinge_pin", "b": "tub", "max_depth_mm": 0.15,
                      "reason": "the pin is pressed 0.15 mm into the tub knuckle bores (r0.85)"})
for i in range(2):
    allow_overlap.append({"a": f"insert_hb{i}", "b": "hinge_block", "max_depth_mm": 0.15,
                          "reason": "heat-set OD 3.2 pressed into the 3.0 mm seat bore"})
for s, ys, tag in ((1, P.LID_SCREWS_Y_L, "l"), (-1, P.LID_SCREWS_Y_R, "r")):
    for i in range(len(ys)):
        allow_overlap.append({"a": f"insert_lid_{tag}{i}", "b": "tub", "max_depth_mm": 0.15,
                              "reason": "heat-set OD 3.2 pressed into the 3.0 mm pad bore"})
for s in (-1, 1):
    tag = "l" if s > 0 else "r"
    for i in range(len(P.STANDOFF_YS)):
        for j in range(len(P.PLATE_SCREWS_Z)):
            allow_overlap.append({"a": f"insert_standoff_{tag}{i}{j}", "b": "tub", "max_depth_mm": 0.15,
                                  "reason": "heat-set OD 3.2 pressed into the 3.0 mm column bore"})
    for i in range(len(P.CLAMP_BOLTS_XY)):
        allow_overlap.append({"a": f"insert_clamp_{tag}{i}", "b": "tub", "max_depth_mm": 0.15,
                              "reason": "heat-set OD 3.2 pressed into the 3.0 mm clamp-seat bore"})

# ---- wires -------------------------------------------------------------------------------------
CORR_Y = -17.0
ROTOR_NOTE = ("the flipper joint only rotates 0..42 deg above rest in front of the tub; the wire stays inside the "
              "rear/mid chassis tub well behind the servo tray and never enters the flipper's physical sector sweep "
              "[expires 2027-12-31]")
wires = [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 22, "kind": "power", "slack_mm": 8.0,
     "rotor_ok": ROTOR_NOTE,
     "via": r3([[-11.0, P.BAT_Y, P.TUB_Z0 + P.WALL + P.BAT_H / 2], [-11.0, CORR_Y, 9.5],
                [-16.0, CORR_Y, 13.8], [-20.5, -17.0, 13.8]])},
    {"id": "w_sw_esc", "from": "switch.out", "to": "esc.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "rotor_ok": ROTOR_NOTE,
     "via": r3([[-20.5, -14.0, 13.8], [-16.0, CORR_Y, 13.8], [11.0, CORR_Y, 9.5],
                [18.0, -25.0, 8.5], [P.SIDE_ZONE_X, P.ESC_Y - P.ESC_L / 2, 6.2]])},
    {"id": "w_esc_ml", "from": "esc.m1", "to": "motor_l.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "rotor_ok": ROTOR_NOTE,
     "via": r3([[19.5, -2.5, 6.5], [13.0, -18.0, 9.5], [13.0, P.WHEEL_Y, 11.5]])},
    {"id": "w_esc_mr", "from": "esc.m2", "to": "motor_r.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "rotor_ok": ROTOR_NOTE,
     "via": r3([[19.5, -25.5, 8.5], [11.0, CORR_Y, 8.5], [-11.0, CORR_Y, 10.0],
                [-13.0, P.WHEEL_Y, 11.5]])},
    {"id": "w_esc_servo", "from": "esc.wpn", "to": "servo.signal", "awg": 26, "kind": "signal", "slack_mm": 6.0,
     "rotor_ok": ROTOR_NOTE,
     "via": r3([[27.5, -2.5, 7.5], [14.0, CORR_Y, 8.5], [0.0, CORR_Y, 9.5],
                [0.0, P.SERVO_Y - P.SERVO_L / 2 - 0.5, 9.5]])},
]

spec = {
    "name": "Expandabot (Team Bits Everywhere, 8x AWS antweight champion)",
    "profile": "aws2025",
    "robot_type": "flipper",
    "sim": {"forward": [0, 1], "strategy": "lifter", "drive": {"max_rad_s": 150, "torque_Nm": 0.06}, "lifter": {"group": "flipper", "up_rad": 1.2, "down_rad": 0.0, "torque_Nm": 0.25, "lock": ["horn"]}, "danger": [{"deg": 0, "half_deg": 35, "reach_mm": 70}]},
    "locomotion": "wheeled",
    "size_rule": f"robot/profile.py aws2025: 150 mm floor square, no overhang at any height, no height limit. All values "
                 f"are derived by the src/expandabot/params.py relations; the start pose also fits the old 101.6 mm cube "
                 f"(rest length {P.REST_L:.2f} mm).",
    "weapon_lock": {"type": "external_pin",
                    "note": "made safe outside the robot: the XT30 is unplugged and the removable link is pulled; the "
                            "flipper rests down under gravity, no stored energy"},
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
    "notes": "Generated by robots/expandabot/make_spec.py from src/expandabot/params.py. Manufactured parts are built in "
             "their own local frames by src/build_expandabot.py (build(part=...)); the central flipper joint pivots on "
             "the front hinge line between the two fixed lobster-claw clamping arms (clamp_l, clamp_r), the horn joint "
             "pivots on the servo output axis, and the two rear wheels spin free on the N10 axles.",
}

with open("robots/expandabot/spec.json", "w") as f:
    json.dump(spec, f, indent=1)
print(f"wrote robots/expandabot/spec.json: {len(parts)} parts, {len(fasteners)} fasteners, "
      f"{len(connections)} connections, {len(wires)} wires, {len(allow_overlap)} allow_overlap")
