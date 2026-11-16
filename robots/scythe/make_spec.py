"""Regenerates robots/scythe/spec.json from src/scythe/params.py (run from the repo root):

  LD_LIBRARY_PATH=/tmp/usrlib/usr/lib/x86_64-linux-gnu .venv/bin/python robots/scythe/make_spec.py

All poses are computed from the params relations; edit params.py, then re-run this.
"""
import json, math, sys
sys.path.insert(0, 'robots/scythe/src')
import scythe.params as P
import scythe.tub as tubm

AY = P.WPN_AXIS_Y
WY = P.wheel_y()
MZ = P.motor_z()
MOT_X = P.motor_x()
WH_X = P.wheel_x()
FTOP = P.tub_floor_z() + P.TUB_FLOOR_T
PANEL_Z0 = P.TUB_TOP_Z - P.TOP_PANEL_T
BAT_Y = P.battery_y()   # pack in the rear bay, inside the rear wall
ESC_X = P.ESC_X         # weapon ESC on the right of the pod (its -X face ports face the pod centre)
ESC_Y = P.esc_y()
RX_Y = P.rx_y()         # rx under the panel, ahead of the switch band, clear of the weapon housing
RX_Z = P.TUB_TOP_Z - P.TOP_PANEL_T - 1.25
SW_Z = 25.7
GRIP_S = P.TOP_PANEL_T + P.BOSS_T
BZ = P.bearing_cz()    # MR83ZZ centre z: on the stator flange face, inside the boss bore

def model(part):
    return {"type": "model", "file": "src/build_scythe.py", "params": {"part": part}}

def holes_s():
    wa = {"arch.edge_distance": "the bl_1806's own base-flange taps on its 16 mm circle (robot.catalog bl_1806_stator): "
           "the motor maker's pattern, not ours - the same waiver class as the GR1507 mount holes (RVRN weapon motors)",
          "fastener.access": "driven from above with the top panel off, exactly like the hspin_bar stator screws (RVRN)",
          "tool_access.driver": "hex1.5 straight down through the panel's clearance holes"}
    return [{"id": f"bolt_s{i}", "designation": "M2x6", "material": "steel",
             "at": [P.BL_SCREW_PCD/2*math.cos(math.radians(a)), AY + P.BL_SCREW_PCD/2*math.sin(math.radians(a)), P.TUB_TOP_Z],
             "dir": [0.0, 0.0, -1.0], "through": ["top_panel", "tub"], "threads_into": "weapon_motor_stator",
             "tool": "hex1.5", "removable": True, "head": "socket", "waive": wa,
             "hole": {"d": 2.0, "length": 6.0, "head": "cap", "head_std": "ISO 4762", "head_dk": 3.8, "head_k": 2.0,
                      "clearance_d": 2.2, "into": "through", "side": "head", "grip": GRIP_S}}
            for i, a in enumerate(P.SCREW_ANGLES)]

def holes_p():
    out = []
    for i, (x, y) in enumerate(tubm.post_xy()):
        out.append({"id": f"bolt_p{i}", "designation": "M2x6", "material": "steel",
                    "at": [x, y, P.TUB_TOP_Z], "dir": [0.0, 0.0, -1.0], "through": ["top_panel"], "threads_into": "tub",
                    "tool": "hex1.5", "removable": True, "head": "button",
                    "hole": {"d": 2.0, "length": 6.0, "head": "button", "head_std": "ISO 7380-1", "head_dk": 3.5,
                             "head_k": 1.3, "clearance_d": 2.2, "into": "through", "side": "head", "grip": P.TOP_PANEL_T}})
    return out

def holes_h():
    wa = {"fastener.access": "the rotor stack (nut, bar, hub) is built on the bench: the csk screws are driven with "
           "the stack off the robot - the same as every bar spinner (RVRN bar bolts)",
          "tool_access.driver": "bench assembly: the bar screws are driven with the rotor stack off the robot"}
    return [{"id": f"bolt_h{i}", "designation": "M2.5x8", "material": "steel",
             "at": [sgn*P.BAR_BOLT_PCD/2, AY, P.nut_top_z()], "dir": [0.0, 0.0, 1.0],
             "through": ["bar"], "threads_into": "weapon_hub", "tool": "hex2.0", "removable": True,
             "head": "countersunk", "waive": wa,
             "hole": {"d": 2.5, "length": 8.0, "head": "csk", "head_std": "ISO 14582", "head_dk": 4.7,
                      "head_k": 1.5, "clearance_d": 2.9, "into": "through", "side": "head",
                      "csk_angle": 90.0, "csk_d": 4.7, "csk_depth": 1.1, "sink": 0.0, "grip": P.BAR_T}}
            for i, sgn in enumerate((1.0, -1.0))]

spec = {
  "name": "Scythe (horizontal undercutter bar spinner)",
  "profile": "aws2025",
  "robot_type": "horizontal_spinner",
  "locomotion": "roller",
  "size_rule": "robot/profile.py aws2025: 150 mm floor square, no overhang at any height, no height limit. All values are derived by the src/scythe/params.py relations (the bar is energy- and pitch-limited: the cantilevered undercutter keeps its stored energy under the 20 J spinner escalation threshold and its tip clears the floor at the 5 deg hop pitch), POD_W 65, vertical-wall rear pod, wheels behind the sweep.",
  "weapon_lock": {"type": "external_pin", "note": "made safe outside the robot: the XT30 is unplugged and a 3 mm pit pin dropped through the panel, floor and bar lock holes rests on the floor slab, so the bar cannot turn past it; the pin is a pit tool, not part of the build"},
  "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
  "can_run_inverted": True,
  "claims": [
    {"id": "c_mass", "text": "weighs 150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150.0},
    {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0}
  ],
  "parts": [
    {"id": "tub", "kind": "structure", "material": "nylon", "process": "fdm", "print_orientation": "+z",
     "shape": model("tub"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "sharp_corners_ok": "the flagged concave corners are where the vertical-wall pod meets the sloped disc and the roots of the cradle ribs and panel posts on the shell: short compression ribs and a bonded seam, the same class as the hspin_bar chassis halves",
     "thin_wall_deviation": "the 0.0x mm wall readings are boolean corner points where the diagonal wire-slot cuts and the motor-relief sector faces meet the housing bore (r13) and tube wall (r14.5) - knife edges between cuts, not walls: the tube wall is the full TUB_WALL 1.5 mm all around the housing, and the boss ring 10 mm thick",
     "label": "printed PA tub: sloped disc over the bar + vertical-wall rear pod, motor housing tube, weapon boss, N10 cradles, panel posts"},
    {"id": "top_panel", "kind": "structure", "material": "pa_cf", "process": "fdm", "print_orientation": "+z",
     "shape": model("top_panel"), "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "fixed",
     "sharp_corners_ok": "the concave corners are the disc/pod seam of the top outline, carried on the printed wall below: a skin seam, not a load-bearing notch",
     "label": "1 mm PA-CF top skin: the tension skin the weapon boss hangs from; M2 button screws into printed posts"},
    {"id": "weapon_motor_stator", "kind": "weapon_motor", "catalog": "bl_1806_stator",
     "at": [0.0, AY, MZ], "rot": [0.0, 90.0, 0.0], "rotates_with": "fixed",
     "label": "bl_1806 fixed half, flange up: 4x M2 down through the panel and boss into the flange taps"},
    {"id": "weapon_motor_bell", "kind": "other", "catalog": "bl_1806_can", "parent": "weapon_motor_stator",
     "at": [0.0, 0.0, 0.0], "rot": [0.0, 0.0, 0.0], "rotates_with": "bar",
     "label": "bl_1806 bell: cap down on the hub, spins with the bar; the motor's own shaft (wshaft) is a press fit in its bored core"},
    {"id": "bar", "kind": "weapon", "material": "hardox", "process": "laser", "color": "#d9dde2",
     "shape": model("bar"), "at": [0.0, AY, P.nut_top_z()], "rot": [0.0, 0.0, 0.0], "rotates_with": "bar",
     "joint": {"kind": "revolute", "axis": [0.0, 0.0, 1.0], "pivot": [0.0, AY, P.nut_top_z() + P.BAR_T/2], "min": 0, "max": 360, "default": 0},
     "weapon": {"kind": "bar", "motor": "weapon_motor_stator", "cells": 2, "reduction": 1.0,
                "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": False, "teeth": 2},
     "secondary_ops": ["drilled", "countersink"],
     "label": "3 mm Hardox two-tooth bar, energy/pitch-limited length, horizontal under the tub; csk M2.5s, piloted on the motor's own shaft"},
    {"id": "weapon_hub", "kind": "hub", "material": "aluminium", "process": "lathe",
     "shape": model("weapon_hub"), "parent": "bar", "at": [0.0, 0.0, P.BAR_T], "rot": [0.0, 0.0, 0.0], "rotates_with": "bar",
     "secondary_ops": ["drilled", "tap M2.5 x2"],
     "label": "turned 7075 hub on the motor's own shaft: its cup pilots on the bell cap rim, the bar bolts to it with 2x M2.5"},
    {"id": "wshaft", "kind": "shaft", "material": "steel", "process": "cots",
     "stock": "3 mm silver steel rod, M3 thread 8 at the lower end", "shaft_of": "weapon_motor_bell",
     "shape": {"type": "cylinder", "radius": P.SHAFT_D/2, "height": P.wshaft_len()},
     "parent": "bar", "at": [0.0, 0.0, P.WSHAFT_TIP_Z + P.wshaft_len()/2 - P.nut_top_z()], "rot": [0.0, 0.0, 0.0],
     "rotates_with": "bar",
     "label": "the motor's own shaft, extended: press fit in the bell's bored core, down through hub and bar to the M3 nut thread"},
    {"id": "wbearing", "kind": "bearing", "material": "steel", "process": "cots", "stock": "MR83ZZ 3x8x3",
     "rotates_with": "fixed", "color": "#555555",
     "shape": {"type": "subtract",
               "base": {"type": "cylinder", "radius": P.BEARING_OD_R, "height": P.BEARING_T},
               "cut": [{"type": "cylinder", "radius": P.BEARING_ID_R, "height": P.BEARING_T + 4.0}]},
     "at": [0.0, AY, BZ], "rot": [0.0, 0.0, 0.0],
     "label": "MR83ZZ (3x8x3) in the weapon boss bore: outer race pressed into the boss (the bearing seat on the stator flange face), inner race on the motor's own shaft - the rotor's second support"},
    {"id": "shaft_nut", "kind": "nut", "catalog": "nut_m3_alu", "parent": "bar",
     "at": [0.0, 0.0, P.nut_z0() + P.NUT_T/2 - P.nut_top_z()], "rot": [0.0, 0.0, 0.0], "rotates_with": "bar",
     "label": "M3 nut on the shaft's lower thread: clamps bar + hub up against the bell cap face"},
    {"id": "drive_motor_r", "kind": "motor", "catalog": "bbb_n10_1000rpm",
     "at": [MOT_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 0.0], "retained": "clamp", "exposed": True,
     "exposed_reason": "the N10's shaft and the wheel it drives are outside the pod wall by design, exactly like Revron's outboard belt drives; the gearbox body is inside",
     "label": "right drive: body nested against the pod wall, clamped between gearbox face and wheel"},
    {"id": "drive_motor_l", "kind": "motor", "catalog": "bbb_n10_1000rpm",
     "at": [-MOT_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 180.0], "retained": "clamp", "exposed": True,
     "exposed_reason": "the N10's shaft and the wheel it drives are outside the pod wall by design, exactly like Revron's outboard belt drives; the gearbox body is inside",
     "label": "left drive: mirror of the right"},
    {"id": "wheel_r", "kind": "wheel", "catalog": "bbb_wheel_34x6_5", "at": [WH_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 0.0],
     "retained": "clamp",
     "retained_reason": "the wheel boss clamps the pod wall between itself and the gearmotor's gearbox face, and the D-bore keys the wheel to the 3 mm shaft: the wheel is captured with the clamped motor"},
    {"id": "wheel_l", "kind": "wheel", "catalog": "bbb_wheel_34x6_5", "at": [-WH_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 180.0],
     "retained": "clamp",
     "retained_reason": "the wheel boss clamps the pod wall between itself and the gearmotor's gearbox face, and the D-bore keys the wheel to the 3 mm shaft: the wheel is captured with the clamped motor"},
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY, "at": [0.0, BAT_Y, FTOP + 6.0],
     "rot": [0.0, 0.0, 0.0], "retained": "strap",
     "label": "2S 300 mAh HV pack in the pod's rear bay; a poly strap through printed slots holds it down (the strap carries the inverted load)"},
    {"id": "weapon_esc", "kind": "esc", "catalog": "bbb_brushless_esc_20a", "at": [ESC_X, ESC_Y, FTOP + 2.0],
     "rot": [0.0, 0.0, 0.0], "retained": "adhesive",
     "label": "20 A brushless ESC on the right of the pod floor, bonded on a foam pad"},
    {"id": "drive_rx", "kind": "esc", "catalog": "bbb_malenki_nano", "at": [0.0, RX_Y, RX_Z],
     "rot": [0.0, 0.0, 0.0], "retained": "adhesive",
     "label": "Malenki-Nano combined drive ESC + receiver, taped to the top panel's underside ahead of the switch band"},
    {"id": "switch", "kind": "switch", "catalog": "fingertech_mini_switch", "at": [P.SWITCH_X, P.switch_y(), SW_Z],
     "rot": [0.0, 0.0, 270.0], "retained": "clamp", "marked": True, "tool_free": True,
     "label": "mini switch mid-pod under the panel, clamped to the top panel by its own bushing and nut through the 4 mm key hole"}
  ],
  "fasteners": holes_h() + holes_s() + holes_p(),
  "wires": [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 22, "kind": "power", "slack_mm": 8.0,
     "via": [[0.0, BAT_Y + 8.0, 25.5], [-15.5, BAT_Y + P.BAT_HALF_D, 25.5], [-15.5, P.switch_y() + 3.81, 25.5]]},
    {"id": "w_sw_rx", "from": "switch.out", "to": "drive_rx.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "via": [[-20.0, P.switch_y() - 3.81, 27.5], [-20.0, RX_Y - 6.0, 27.5]]},
    {"id": "w_sw_wesc", "from": "switch.out", "to": "weapon_esc.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "via": [[-20.0, P.switch_y() - 3.81, 20.0], [-20.0, P.switch_y() - 3.81, FTOP + 2.4], [2.0, ESC_Y - 3.0, FTOP + 2.4]]},
    {"id": "w_rx_ml", "from": "drive_rx.m1", "to": "drive_motor_l.terminals", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[16.0, RX_Y + 6.0, 24.0], [-6.0, 24.0, 20.0], [-7.5, WY, 17.0]]},
    {"id": "w_rx_mr", "from": "drive_rx.m2", "to": "drive_motor_r.terminals", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[-16.0, RX_Y + 6.0, 24.0], [6.0, 24.0, 20.0], [7.5, WY, 17.0]]},
    {"id": "w_rx_wpn", "from": "drive_rx.wpn", "to": "weapon_esc.rx", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[16.0, RX_Y - 6.0, 24.0], [2.0, 4.0, 18.0], [2.0, ESC_Y + 3.0, FTOP + 2.4]]},
    {"id": "w_wesc_m", "from": "weapon_esc.motor", "to": "weapon_motor_stator.phases", "awg": 22, "kind": "power", "slack_mm": 10.0,
     "rotor_ok": "the stator's phase port is on the spin axis at the flange face (catalog bl_1806_stator port at local -7): the run climbs the housing-tube wire channel into the boss slot and ends on the axis, so the final segment is inside the swept shaft line by construction - the run itself stays in the static printed channel, 10 mm slack absorbs the bell's axial play",
     "via": [[ESC_X + 11.5, ESC_Y, 18.0], [24.0, 10.0, 22.0], [7.0, 39.0, 22.5], [15.5, 41.0, 16.0],
             [11.0, AY + 11.0, 15.5], [8.5, AY + 8.5, 15.5], [8.5, AY + 8.5, 25.9], [3.2, AY + 3.2, 25.9]]}
  ],
  "connections": [
    {"a": "bar", "b": "wshaft", "method": "shaft", "reason": "the bar's 3.1 mm bore pilots on the motor's own shaft (0.05 mm slide): the shaft centres the bar, the clamp nut sets its height and the M2.5s carry the torque", "mechanical_key": True},
    {"a": "weapon_hub", "b": "wshaft", "method": "shaft", "reason": "the hub's 3.2 mm bore runs on the shaft (0.1 mm slide): the shaft locates it, the clamp and the bar screws carry the torque"},
    {"a": "wshaft", "b": "weapon_motor_bell", "method": "press_fit", "reason": "the motor's own shaft, a press fit in the bell's bored rotor core (the catalogue draws the bore at r1.45); the nut clamps bar + hub to the bell cap face so the stack turns as one", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "wbearing", "b": "tub", "method": "press_fit", "reason": "MR83ZZ outer race pressed into the boss bore (line-to-line at r4.0, 0.05 mm declared press): the bearing seat sits directly on the stator flange face", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "wbearing", "b": "wshaft", "method": "shaft", "reason": "MR83ZZ inner race on the motor's own 3 mm shaft (r1.5 bore on the r1.5 shaft, a slide fit): the shaft runs through the bearing bore, the rotor's second support"},
    {"a": "weapon_hub", "b": "weapon_motor_bell", "method": "press_fit", "reason": "the hub's top cup pilots on the bell's cap rim and the clamp nut seats it hard on the cap face: torque passes through the clamped faces and the shaft's press fit", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "shaft_nut", "b": "wshaft", "method": "press_fit", "reason": "M3 thread on the shaft's lower end: the thread is the key, and the nut clamps bar + hub up against the bell cap face", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "bar", "b": "weapon_hub", "method": "screw", "reason": "2x M2.5 csk through the bar into the hub's tapped holes"},
    {"a": "weapon_motor_stator", "b": "tub", "method": "screw", "reason": "4x M2 through the panel and the printed boss into the stator flange taps: the boss ties the stator to the tension skin"},
    {"a": "top_panel", "b": "tub", "method": "screw", "reason": "8x M2 button through the panel into the printed posts (thread-forming, Revron top-panel style)"},
    {"a": "drive_motor_r", "b": "wheel_r", "method": "press_fit", "reason": "wheel D-bore on the 3 mm D-shaft: the flat carries the drive torque; the wheel boss clamps the pod wall between gearbox and wheel so the motor cannot walk inboard", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "drive_motor_l", "b": "wheel_l", "method": "press_fit", "reason": "wheel D-bore on the 3 mm D-shaft: the flat carries the drive torque; the wheel boss clamps the pod wall between gearbox and wheel so the motor cannot walk inboard", "interference_mm": 0.05, "mechanical_key": True},
    {"a": "drive_motor_r", "b": "tub", "method": "interlock", "reason": "gearmotor seats on its printed cradle pads, the ribs locate it fore-aft and the pod wall takes the gearbox face; the wheel on the shaft clamps the assembly"},
    {"a": "drive_motor_l", "b": "tub", "method": "interlock", "reason": "gearmotor seats on its printed cradle pads, the ribs locate it fore-aft and the pod wall takes the gearbox face; the wheel on the shaft clamps the assembly"},
    {"a": "battery", "b": "tub", "method": "velcro", "reason": "the pack sits on a velcro pad on the pod floor and a poly strap through printed slots holds it down: the strap carries the inverted load, the pad only locates"},
    {"a": "switch", "b": "top_panel", "method": "interlock", "reason": "the switch's mounting bushing passes through the panel's 4 mm key hole and its nut clamps it: the key hole is the interlock"}
  ],
  "allow_overlap": [
    {"a": "wshaft", "b": "weapon_motor_bell", "max_depth_mm": 0.2, "reason": "the motor's own shaft is a press fit in the bell's bored core (the catalogue draws the bore at r1.45, the shaft is r1.5)"},
    {"a": "wbearing", "b": "tub", "max_depth_mm": 0.1, "reason": "the bearing's outer race is a press fit in the boss bore (r4.0 seat, modelled line-to-line)"},
    {"a": "wheel_r", "b": "drive_motor_r", "max_depth_mm": 0.6, "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the D-flat keys the drive"},
    {"a": "wheel_l", "b": "drive_motor_l", "max_depth_mm": 0.6, "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the D-flat keys the drive"}
  ],
  "notes": "Derived by the src/scythe relations; poses computed from params.py. Motor-as-hub weapon (the reference hspin_bar's topology): the bl_1806's own extended shaft carries the rotor from above; the bar is a cantilevered undercutter whose stored energy stays under the 20 J escalation threshold. The battery lead runs around the pack at the pod wall."
}
with open('robots/scythe/spec.json', 'w') as f:
    json.dump(spec, f, indent=1)
print('spec written: AY', round(AY,2), 'WY', round(WY,2), 'switch_y', round(P.switch_y(),2), 'BAR_L', P.BAR_L,
      'mass', round(P.total_mass_g(),1), 'E[J]', round(P.energy_j(P.bar_rpm()),1))

# Expr variant for the PR #84 param jiggle (`robot jiggle --param src/scythe/params.py:NAME=...`): the same spec with
# param-linked `at` entries as expressions, so a solved master moves the parts together with the pockets/holes the
# model re-derives. Written next to the real spec (SCYTHE_EXPR_SPEC=robots/scythe/jiggle_spec.json); never committed.
import os
EXPR_OUT = os.environ.get('SCYTHE_EXPR_SPEC')
if EXPR_OUT:
    import copy
    sp = copy.deepcopy(spec)
    sp['params'] = {'P': 'src/scythe/params.py'}
    EXPR_AT = {
        'weapon_motor_stator': ['0.0', 'P.WPN_AXIS_Y', 'P.motor_z()'],
        'bar': ['0.0', 'P.WPN_AXIS_Y', 'P.nut_top_z()'],
        'wbearing': ['0.0', 'P.WPN_AXIS_Y', 'P.bearing_cz()'],
        'drive_motor_r': ['P.motor_x()', 'P.wheel_y()', 'P.WHEEL_CZ'],
        'drive_motor_l': ['-P.motor_x()', 'P.wheel_y()', 'P.WHEEL_CZ'],
        'wheel_r': ['P.wheel_x()', 'P.wheel_y()', 'P.WHEEL_CZ'],
        'wheel_l': ['-P.wheel_x()', 'P.wheel_y()', 'P.WHEEL_CZ'],
        'battery': ['0.0', 'P.battery_y()', 'P.tub_floor_z()+P.TUB_FLOOR_T+6.0'],
        'weapon_esc': ['P.ESC_X', 'P.esc_y()', 'P.tub_floor_z()+P.TUB_FLOOR_T+2.0'],
        'drive_rx': ['0.0', 'P.rx_y()', 'P.TUB_TOP_Z-P.TOP_PANEL_T-1.25'],
        'switch': ['P.SWITCH_X', 'P.switch_y()', '25.7'],
    }
    for p in sp['parts']:
        if p['id'] in EXPR_AT:
            p['at'] = EXPR_AT[p['id']]
    for fh in sp['fasteners']:
        if fh['id'].startswith('bolt_s'):
            i = int(fh['id'][6:]); a = P.SCREW_ANGLES[i]
            fh['at'] = [f'(P.BL_SCREW_PCD/2)*math.cos(math.radians({a}))',
                        f'P.WPN_AXIS_Y+(P.BL_SCREW_PCD/2)*math.sin(math.radians({a}))', 'P.TUB_TOP_Z']
        elif fh['id'].startswith('bolt_p'):
            i = int(fh['id'][6:])
            if i >= 4:  # pod-wall posts follow POD_W; the 4 disc-rim posts do not
                dy = P.POD_POST_Y[(i - 4) // 2]
                sgn = '1.0' if i % 2 == 0 else '-1.0'
                fh['at'] = [f'{sgn}*(P.POD_W/2-P.TUB_WALL-P.POST_R/2)', f'P.wheel_y()+({dy})', 'P.TUB_TOP_Z']
        elif fh['id'].startswith('bolt_h'):
            i = int(fh['id'][6:]); sgn = (1.0, -1.0)[i]
            fh['at'] = [f'{sgn}*(P.BAR_BOLT_PCD/2)', 'P.WPN_AXIS_Y', 'P.nut_top_z()']
    with open(EXPR_OUT, 'w') as f:
        json.dump(sp, f, indent=1)
    print('expr spec written:', EXPR_OUT)
