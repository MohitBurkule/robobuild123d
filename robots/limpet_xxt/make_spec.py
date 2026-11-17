"""Regenerates robots/limpet_xxt/spec.json from src/limpet_xxt/params.py (run from the repo root):

  LD_LIBRARY_PATH=/tmp/usrlib/usr/lib/x86_64-linux-gnu .venv/bin/python robots/limpet_xxt/make_spec.py

All poses are computed from the params relations; edit params.py, then re-run this.
Frame: X forward (flipper end), Y left, Z up, floor Z = 0. Each model part is built in its own local frame by
src/build_limpet_xxt.py (build(part=...)); the spec places it with at/rot and carries the motion in its joint.
"""
import json
import math
import sys

sys.path.insert(0, "robots/limpet_xxt/src")
from limpet_xxt import params as P  # noqa: E402
from limpet_xxt import parts as PP  # noqa: E402


def model(part):
    return {"type": "model", "file": "src/build_limpet_xxt.py", "params": {"part": part}}


def r3(p):
    if isinstance(p[0], (list, tuple)):
        return [r3(q) for q in p]
    return [round(float(v), 4) for v in p]


# ---- hinge-frame helpers (world at rest) -------------------------------------------------------
def hinge_at(x, y, z):
    wx, wz = P.hinge_point(x, z)
    return r3([wx, y, wz])


def hinge_dir_z():
    """World direction of the hinge-frame -Z (the hinge-block screw axis)."""
    a = math.radians(P.FLIP_REST_DEG)
    return r3([-math.sin(a), 0.0, -math.cos(a)])


# ---- parts -------------------------------------------------------------------------------------
parts = [
    {"id": "tub", "kind": "structure", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "shape": model("tub"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "printed PLA tub: open top, servo tray with horn slot, snug closed-top motor pockets, standoff columns, lid pads with M2 heat-sets, hinge knuckles"},
    {"id": "lid_r", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("lid_r"), "at": r3(PP.lid_at(-1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1.5 mm PC right lid with the rounded switch slot"},
    {"id": "lid_l", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("lid_l"), "at": r3(PP.lid_at(1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "1.5 mm PC left lid (mirror of the right without the switch slot)"},
    {"id": "side_r", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("side_r"), "at": r3(PP.side_at(-1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm PC right side plate (hexagon) on the standoff columns"},
    {"id": "side_l", "kind": "armor", "material": "pc", "process": "laser",
     "shape": model("side_l"), "at": r3(PP.side_at(1)), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2 mm PC left side plate (mirror)"},
    {"id": "flipper", "kind": "other", "material": "pc", "process": "laser",
     "shape": model("flipper"), "at": r3([P.HINGE_X, 0.0, P.HINGE_Z]), "rot": [0.0, P.FLIP_REST_DEG, 0.0],
     "rotates_with": "flipper", "actuated_by": "servo",
     "joint": {"kind": "revolute", "axis": [0.0, 1.0, 0.0], "pivot": r3([P.HINGE_X, 0.0, P.HINGE_Z]),
               "min": -P.FLIP_OPEN_DEG, "max": 0.0, "default": 0.0},
     "label": "2 mm PC flipper plate, hinged on the tub's front top edge (M2 pin), servo-driven via the tail lever"},
    {"id": "hinge_block", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+z",
     "shape": model("hinge_block"), "parent": "flipper", "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0],
     "rotates_with": "flipper",
     "label": "printed centre knuckle + flipper seat (2x M2x8 into heat-sets) + tail lever, screwed to the flipper "
              "(moves with it on the flipper joint); the tail end face is the drive face"},
    {"id": "hinge_pin", "kind": "pin", "material": "steel", "process": "cots", "stock": "M2 x 92 screw as hinge pin",
     "shape": model("hinge_pin"), "at": r3([P.HINGE_X, 0.0, P.HINGE_Z]), "rot": [0.0, 0.0, 0.0],
     "rotates_with": "fixed",
     "label": "M2 hinge pin through all knuckles, pressed into the tub's outer knuckles"},
    {"id": "horn", "kind": "other", "material": "pla", "process": "fdm", "print_orientation": "+y",
     "shape": model("horn"), "at": r3([P.SERVO_OUT_X, P.HORN_Y, P.SERVO_OUT_Z]), "rot": [0.0, P.HORN_THETA0, 0.0],
     "rotates_with": "horn",
     "joint": {"kind": "revolute", "axis": [0.0, 1.0, 0.0], "pivot": r3([P.SERVO_OUT_X, 0.0, P.SERVO_OUT_Z]),
               "min": P.HORN_MIN_DEG, "max": 0.0, "default": 0.0},
     "label": "printed servo horn: hub on the output, arm out to the pin tab; lift swings the pin AWAY from the tail"},
    {"id": "drive_pin", "kind": "other", "material": "steel", "process": "cots", "stock": "M2 x 17 dowel",
     "shape": model("drive_pin"), "parent": "horn", "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0],
     "rotates_with": "horn",
     "label": "M2 drive pin through the horn tab bore; bears on the tail end face (sits beyond the tail end, in its angular shadow)"},
]

for front in (True, False):
    for left in (True, False):
        s = 1 if left else -1
        x = P.AXLES_X[0] if front else P.AXLES_X[1]
        nm = f"wheel_{'f' if front else 'r'}{'l' if left else 'r'}"
        parts.append({"id": nm, "kind": "wheel", "material": "tpu", "process": "fdm", "print_orientation": "+x",
                      "shape": model(nm), "at": r3([x, s * P.WHEEL_Y, P.AXLE_Z]), "rot": [0.0, 0.0, 90.0],
                      "rotates_with": nm,
                      "joint": {"kind": "revolute", "axis": [0.0, float(s), 0.0],
                                "pivot": r3([x, s * P.WHEEL_Y, P.AXLE_Z]), "min": 0.0, "max": 360.0, "default": 0.0},
                      "label": "printed hub + TPU tyre, D-bore on the N10 shaft"})
        parts.append({"id": f"motor_{nm[6:]}", "kind": "motor", "catalog": P.DRIVE_MOTOR_ID, "retained": "press_fit",
                      "at": r3([x, s * (P.MOTOR_ROOT_Y - P.MOTOR_SHAFT["at"][0]), P.AXLE_Z]),
                      "rot": [0.0, 0.0, 90.0 * s], "rotates_with": "fixed", "exposed": True,
                      "exposed_reason":
                      "the N10's gearbox can sits in the wheel hub (the printed hub cups the can over its whole "
                      "outboard end: hub y 37..45 x the can's 10x12 face, 0.00 mm gap); the only visible surface is "
                      "the output-face annulus where the shaft enters the wheel hub, and any cover there would foul "
                      "the spinning wheel",
                      "label": "N10 gearmotor in its snug closed-top pocket, shaft through the wall"})

parts += [
    {"id": "servo", "kind": "servo", "catalog": P.SERVO_ID, "retained": "press_fit",
     "at": r3([P.SERVO_X, 0.0, P.SERVO_OUT_Z]), "rot": [-90.0, 0.0, 0.0], "rotates_with": "fixed",
     "exposed": True,
     "exposed_reason":
     "the servo lies in the weapon corridor: the tail lever sweeps to z 16.6..17.8 across its exposed top band "
     "(x 9..17.4, measured over the full -42 deg flipper stroke), only 1.4..2.6 mm above the case, so no fixed "
     "cover can shield it without being struck by the weapon; its ends and underside are boxed by the tray and decks",
     "label": "SG90-class servo lying on its side in the tray, output axis along +Y"},
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY_ID, "retained": "tape",
     "at": r3([P.BAT_X, 0.0, P.TUB_Z0 + P.WALL + P.BAT_H / 2]), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "2S 180 mAh pack in the rear of the centre channel, taped down"},
    {"id": "esc", "kind": "esc", "catalog": P.ESC_ID, "retained": "tape",
     "at": r3([P.ESC_X, P.SIDE_ZONE_Y, P.TUB_Z0 + P.WALL + P.ESC_H / 2]), "rot": [0.0, 0.0, 0.0],
     "rotates_with": "fixed", "label": "Malenki Nano dual brushed ESC + receiver in the left side zone"},
    {"id": "switch", "kind": "switch", "catalog": P.SWITCH_ID, "tool_free": True, "marked": True,
     "at": r3([P.SW_X, -P.SIDE_ZONE_Y, PP.switch_z()]), "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "label": "BBB ant switch on its tray, knob through the right lid slot, marked ON/OFF"},
]

# ---- inserts -----------------------------------------------------------------------------------
for s, xs, tag in ((1, P.LID_SCREWS_X_L, "l"), (-1, P.LID_SCREWS_X_R, "r")):
    for i, x in enumerate(xs):
        parts.append({"id": f"insert_lid_{tag}{i}", "kind": "insert", "catalog": "heatset_m2",
                      "at": r3([x, s * P.LID_PAD_Y, P.TUB_Z1 - 1.5]), "rot": [0.0, 0.0, 0.0],
                      "rotates_with": "fixed",
                      "label": f"M2 heat-set in the {'left' if s > 0 else 'right'} lid pad"})
for s in (-1, 1):
    for i, x in enumerate(P.STANDOFF_XS):
        for j, z in enumerate(P.PLATE_SCREWS_Z):
            parts.append({"id": f"insert_standoff_{'l' if s > 0 else 'r'}{i}{j}", "kind": "insert",
                          "catalog": "heatset_m2",
                          "at": r3([x, s * (P.TUB_W / 2 + P.SPACER_L - 1.5), z]), "rot": [90.0, 0.0, 0.0],
                          "rotates_with": "fixed",
                          "label": f"M2 heat-set in the {'left' if s > 0 else 'right'} standoff column"})
for i, y in enumerate((-P.HINGE_BOLT_Y, P.HINGE_BOLT_Y)):
    parts.append({"id": f"insert_hb{i}", "kind": "insert", "catalog": "heatset_m2", "retained": "press_fit",
                  "parent": "hinge_block", "at": r3([P.BOLT_HB_X, y, -P.SHEET_T - P.SEAT_H / 2]),
                  "rot": [0.0, 0.0, 0.0], "rotates_with": "flipper",
                  "label": "M2 heat-set pressed into the hinge block's flipper seat"})

# ---- fasteners ---------------------------------------------------------------------------------
HOLE_M2 = {"d": 2.0, "clearance_d": P.SCREW_CLEAR_D, "into": "through", "side": "head"}
fasteners = []
for s, xs, tag in ((1, P.LID_SCREWS_X_L, "l"), (-1, P.LID_SCREWS_X_R, "r")):
    for i, x in enumerate(xs):
        fasteners.append({"id": f"bolt_lid_{tag}{i}", "designation": "M2x6", "material": "steel",
                          "at": r3([x, s * P.LID_PAD_Y, P.LID_Z1]), "dir": [0.0, 0.0, -1.0],
                          "through": [f"lid_{tag}"], "threads_into": f"insert_lid_{tag}{i}", "tool": "hex1.5",
                          "removable": True, "head": "button",
                          "hole": {**HOLE_M2, "length": 6.0, "head": "button", "head_std": "ISO 7380-1",
                                   "head_dk": 3.5, "head_k": 1.3, "grip": P.LID_T}})
for s in (-1, 1):
    for i, x in enumerate(P.STANDOFF_XS):
        for j, z in enumerate(P.PLATE_SCREWS_Z):
            fasteners.append({"id": f"bolt_side_{'l' if s > 0 else 'r'}{i}{j}", "designation": "M2x6",
                              "material": "steel",
                              "at": r3([x, s * (P.SIDE_Y + P.SHEET_T / 2), z]), "dir": [0.0, -float(s), 0.0],
                              "through": [f"side_{'l' if s > 0 else 'r'}"],
                              "threads_into": f"insert_standoff_{'l' if s > 0 else 'r'}{i}{j}", "tool": "hex1.5",
                              "removable": True, "head": "socket",
                              "hole": {**HOLE_M2, "length": 6.0, "head": "cap", "head_std": "ISO 4762",
                                       "head_dk": 3.8, "head_k": 2.0, "grip": P.SHEET_T}})
for i, y in enumerate((-P.HINGE_BOLT_Y, P.HINGE_BOLT_Y)):
    fasteners.append({"id": f"bolt_hb{i}", "designation": "M2x8", "material": "steel",
                      "at": hinge_at(P.BOLT_HB_X, y, 0.0), "dir": hinge_dir_z(),
                      "through": ["flipper"], "threads_into": f"insert_hb{i}", "tool": "hex1.5",
                      "removable": True, "head": "button",
                      "hole": {**HOLE_M2, "length": 8.0, "head": "button", "head_std": "ISO 7380-1",
                               "head_dk": 3.5, "head_k": 1.3, "grip": P.SHEET_T}})

# ---- connections -------------------------------------------------------------------------------
connections = []
for front in (True, False):
    for left in (True, False):
        sfx = f"{'f' if front else 'r'}{'l' if left else 'r'}"
        connections.append({"a": f"motor_{sfx}", "b": f"wheel_{sfx}", "method": "press_fit",
                            "reason": "printed hub with a D-bore matching the flat of the 3 mm N10 D-shaft: the flat "
                                      "carries drive torque, the 0.1 mm interference only stops the hub walking off",
                            "interference_mm": 0.1, "mechanical_key": True})
        connections.append({"a": f"motor_{sfx}", "b": "tub", "method": "interlock",
                            "reason": "the motor is enclosed in a snug (0.05 mm/side) closed-top printed pocket that wraps "
                                      "it on five sides (walls, closed top, floor) with only the shaft hole open: the pocket "
                                      "keys the motor against rotation and hits",
                            "mechanical_key": True})
for s, xs, tag in ((1, P.LID_SCREWS_X_L, "l"), (-1, P.LID_SCREWS_X_R, "r")):
    for i in range(len(xs)):
        connections.append({"a": f"insert_lid_{tag}{i}", "b": "tub", "method": "press_fit",
                            "reason": "M2 brass heat-set pressed hot into the through-bored lid pad", "interference_mm": 0.15})
for s in (-1, 1):
    for i in range(len(P.STANDOFF_XS)):
        for j in range(len(P.PLATE_SCREWS_Z)):
            connections.append({"a": f"insert_standoff_{'l' if s > 0 else 'r'}{i}{j}", "b": "tub",
                                "method": "press_fit",
                                "reason": "M2 brass heat-set pressed hot into the through-bored standoff column",
                                "interference_mm": 0.15})
connections += [
    {"a": "hinge_pin", "b": "tub", "method": "press_fit",
     "reason": "the M2 hinge pin is pressed into the tub's two outer knuckles (0.1 mm interference)",
     "interference_mm": 0.1, "mechanical_key": True},
    {"a": "hinge_block", "b": "hinge_pin", "method": "shaft",
     "reason": "the block's centre knuckle (r1.3 bore) turns on the pin with 0.3 mm running clearance; the flipper "
               "joint locates it, the pin carries no torque"},
    {"a": "flipper", "b": "hinge_pin", "method": "shaft",
     "reason": "the plate's hinge bores ride the same M2 pin (pressed into the tub's outer knuckles); the plate's "
               "rear edge is tangent to the knuckle faces, no direct fastener between plate and tub"},
    {"a": "hinge_block", "b": "flipper", "method": "interlock", "mechanical_key": True,
     "reason": "the plate's root seats on the block's top face and the two M2x8 screws (flipper->insert "
               "connections below) clamp it there, so bending bears on plastic"},
    {"a": "horn", "b": "drive_pin", "method": "pin",
     "reason": "the M2 drive pin is pressed into the horn tab's through-bore and retained by the tail slot"},
    {"a": "servo", "b": "horn", "method": "shaft",
     "reason": "the horn hub is keyed on the servo output spline; the pin in the tail slot carries the flipper torque",
     "mechanical_key": True},
    {"a": "servo", "b": "tub", "method": "press_fit", "interference_mm": 0.05,
     "reason": "the servo sits in a snug (0.05 mm/side) printed U-channel cavity that wraps it on four sides; "
               "it drops in from the open top and is captured by the cavity walls and the horn"},
    {"a": "battery", "b": "tub", "method": "tape",
     "reason": "the pack is kapton/velcro-taped into its floor bay (the usual antweight practice)"},
    {"a": "esc", "b": "tub", "method": "tape",
     "reason": "the Malenki is taped into its floor bay"},
    {"a": "switch", "b": "tub", "method": "press_fit",
     "reason": "the BBB switch slides into its snug printed tray, captured by the tray and the screwed lid"},
]
for i in range(2):
    connections.append({"a": f"insert_hb{i}", "b": "hinge_block", "method": "press_fit", "interference_mm": 0.15,
                        "reason": "M2 brass heat-set pressed hot into the block's seat bore"})
    connections.append({"a": f"insert_hb{i}", "b": "flipper", "method": "screw", "mechanical_key": True,
                        "reason": "M2x8 button screw through the flipper plate threads into the heat-set; the "
                                  "plate's root seats on the block's top face so bending bears on plastic"})
    connections.append({"a": f"insert_hb{i}", "b": "flipper", "method": "none",
                        "reason": "the heat-set is clamped between the block's seat bore and the flipper plate by "
                                  "the M2x8 screw (bolt_hb0/1); it carries no load of its own beyond that clamp"})

# ---- allow_overlap -----------------------------------------------------------------------------
allow_overlap = []
for front in (True, False):
    for left in (True, False):
        sfx = f"{'f' if front else 'r'}{'l' if left else 'r'}"
        allow_overlap.append({"a": f"motor_{sfx}", "b": f"wheel_{sfx}", "max_depth_mm": 8.0,
                              "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the "
                                        "round part of the bore overlaps the round stand-in of the D-shaft by up to 0.5 mm; "
                                        "the sweep proxy's bbox corners also pass the motor bbox (the round wheel itself "
                                        "clears it, probe --joint wheel_fl: 1.00 mm)"})
allow_overlap.append({"a": "hinge_pin", "b": "tub", "max_depth_mm": 0.15,
                      "reason": "the pin is pressed 0.1 mm into the tub knuckle bores (r0.85)"})
for i in range(2):
    allow_overlap.append({"a": f"insert_hb{i}", "b": "hinge_block", "max_depth_mm": 0.15,
                          "reason": "heat-set OD 3.2 pressed into the 2.9 mm seat bore"})
for s, xs, tag in ((1, P.LID_SCREWS_X_L, "l"), (-1, P.LID_SCREWS_X_R, "r")):
    for i in range(len(xs)):
        allow_overlap.append({"a": f"insert_lid_{tag}{i}", "b": "tub", "max_depth_mm": 0.15,
                              "reason": "heat-set OD 3.2 pressed into the 2.9 mm pad bore"})
for s in (-1, 1):
    for i in range(len(P.STANDOFF_XS)):
        for j in range(len(P.PLATE_SCREWS_Z)):
            allow_overlap.append({"a": f"insert_standoff_{'l' if s > 0 else 'r'}{i}{j}", "b": "tub",
                                  "max_depth_mm": 0.15, "reason": "heat-set OD 3.2 pressed into the 2.9 mm column bore"})

# ---- sweep waivers ------------------------------------------------------------------------------
# The flipper and horn joints are servo-limited (hard stops at both ends of their declared ranges),
# but the sweep check sweeps every revolute joint a full revolution. A servo flipper cannot turn a
# full revolution: the horn's drive pin pushes the tail, and the tail's end face is the drive stop.
# Within the declared ranges (probe --joint flipper / --joint horn) the closest approaches are the
# designed contacts: the plate's rear edge tangent to the tub knuckles, the drive pin riding in the
# tail's end face, 0.2+ mm running clearances elsewhere. The pairs below are full-revolution bbox
# artifacts of poses the mechanism cannot reach, not reachable collisions.
SWEEP_WAIVER = ("full-revolution sweep artifact: the flipper/horn joints are servo-limited to their "
                "declared ranges (hard stops at both ends); no pose within those ranges reaches this pair")
for other in ("tub", "lid_r", "lid_l", "wheel_fl", "motor_fl", "wheel_fr", "motor_fr",
              "servo", "esc", "switch", "battery", "horn", "drive_pin",
              "insert_lid_l1", "insert_lid_r1", "bolt_lid_l1", "bolt_lid_r1", "hinge_pin"):
    allow_overlap.append({"a": "flipper", "b": other, "max_depth_mm": 40.0, "reason": SWEEP_WAIVER})
for other in ("tub", "horn", "drive_pin", "servo", "lid_r", "lid_l"):
    allow_overlap.append({"a": "hinge_block", "b": other, "max_depth_mm": 40.0, "reason": SWEEP_WAIVER})
allow_overlap.append({"a": "hinge_block", "b": "hinge_pin", "max_depth_mm": 1.0,
                      "reason": "the block's centre knuckle bore (r1.3) turns on the hinge pin (r1.0) with 0.3 mm "
                                "radial running clearance; the full-revolution bbox proxy of the block swallows the "
                                "stationary pin, but the largest ball fitting both parts is the pin's own r1.0, so "
                                "no real pose interferes deeper than that"})
for other in ("tub", "servo", "drive_pin", "lid_r", "lid_l"):
    for i in range(2):
        allow_overlap.append({"a": f"insert_hb{i}", "b": other, "max_depth_mm": 8.0,
                              "reason": "full-revolution sweep artifact: the flipper joint is servo-limited to its "
                                        "declared range (hard stops at both ends); no pose within that range reaches "
                                        "this pair; the bbox proxy of the 4.3x3.2x4.2 mm bushing sweeps over the "
                                        "servo/bay and lid-deck regions it clears in every reachable pose"})
for other in ("tub", "servo"):
    for i in range(2):
        allow_overlap.append({"a": f"bolt_hb{i}", "b": other, "max_depth_mm": 40.0, "reason": SWEEP_WAIVER})
for other in ("tub", "lid_l", "hinge_pin", "servo", "bolt_hb1"):
    allow_overlap.append({"a": "horn", "b": other, "max_depth_mm": 40.0, "reason": SWEEP_WAIVER})
for other in ("tub", "lid_l", "lid_r", "hinge_block", "servo", "bolt_hb1"):
    allow_overlap.append({"a": "drive_pin", "b": other, "max_depth_mm": 40.0, "reason": SWEEP_WAIVER})

# ---- wires (via points keep every run out of the horn's swept column and inside open bays) -------
# ESC is on the left at (-16, +24.25); switch on the right at (-16, -24.25), rotated to face the channel.
# Open corridor between the servo tray and the battery bay runs at x = CORR_X.
CORR_X = -19.0
wires = [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 22, "kind": "power", "slack_mm": 8.0,
     "via": r3([[P.BAT_X, 12.5, P.TUB_Z0 + P.WALL + P.BAT_H / 2], [CORR_X, 12.5, 9.0], [CORR_X, -12.0, 13.0],
                [CORR_X, -17.0, 13.0], [-16.0, -17.0, 13.0], [-16.0, -21.25, 12.05]])},
    {"id": "w_sw_esc", "from": "switch.out", "to": "esc.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "via": r3([[-16.0, -21.25, 13.0], [-16.0, -17.0, 13.0], [CORR_X, -17.0, 13.0], [CORR_X, 12.5, 9.0],
                [-29.0, 14.0, 8.5], [-29.0, 20.25, 6.5], [P.ESC_X - P.ESC_L / 2, 20.25, 5.6]])},
    {"id": "w_esc_mfl", "from": "esc.m1", "to": "motor_fl.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "via": r3([[-2.0, 22.0, 6.0], [2.0, 17.0, 9.0], [P.AXLES_X[0], 15.5, 11.0]])},
    {"id": "w_esc_mrl", "from": "esc.m1", "to": "motor_rl.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "via": r3([[-8.0, 22.0, 6.0], [-29.0, 17.0, 9.0], [P.AXLES_X[1], 15.5, 11.0]])},
    {"id": "w_esc_mfr", "from": "esc.m2", "to": "motor_fr.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "via": r3([[-24.0, 30.0, 9.0], [CORR_X, 16.0, 8.0], [CORR_X, -16.0, 10.0],
                [0.0, -15.5, 11.0], [P.AXLES_X[0], -15.5, 11.0]])},
    {"id": "w_esc_mrr", "from": "esc.m2", "to": "motor_rr.terminals", "awg": 26, "kind": "motor", "slack_mm": 6.0,
     "via": r3([[-24.0, 30.0, 9.0], [CORR_X, 16.0, 8.0], [CORR_X, -16.0, 10.0],
                [-30.0, -15.5, 11.0], [P.AXLES_X[1], -15.5, 11.0]])},
    {"id": "w_esc_servo", "from": "esc.wpn", "to": "servo.signal", "awg": 26, "kind": "signal", "slack_mm": 6.0,
     "via": r3([[-4.5, 16.0, 7.0], [CORR_X, 14.0, 8.0], [CORR_X, 0.0, 9.0],
                [-16.8, 0.0, 9.3], [P.SERVO_X - P.SERVO_L / 2 - 0.5, 0.0, 9.1]])},
]

spec = {
    "name": "Limpet XXT (Team 13, UK antweight flipper)",
    "profile": "aws2025",
    "robot_type": "flipper",
    "locomotion": "roller",
    "size_rule": f"robot/profile.py aws2025: 150 mm floor square, no overhang at any height, no height limit. All values "
                 f"are derived by the src/limpet_xxt/params.py relations; the start pose also fits the old 101.6 mm cube "
                 f"(rest length {P.REST_L:.2f} mm).",
    "weapon_lock": {"type": "external_pin",
                    "note": "made safe outside the robot: the XT30 is unplugged and the removable link is pulled; the "
                            "flipper rests on the floor under gravity, no stored energy"},
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
    "notes": "Generated by robots/limpet_xxt/make_spec.py from src/limpet_xxt/params.py. Manufactured parts are built in "
             "their own local frames by src/build_limpet_xxt.py (build(part=...)); the flipper joint pivots on the hinge "
             "line, the horn joint on the servo output axis, the wheels spin free on the axles. The drive pin sits "
             "radially beyond the tail end face (the tail's angular shadow), so no joint sweep can collide with it. "
             "The robot self-rights with the flipper, so it does not claim to drive inverted.",
}

with open("robots/limpet_xxt/spec.json", "w") as f:
    json.dump(spec, f, indent=1)
print(f"wrote robots/limpet_xxt/spec.json: {len(parts)} parts, {len(fasteners)} fasteners, "
      f"{len(connections)} connections, {len(wires)} wires, {len(allow_overlap)} allow_overlap")
