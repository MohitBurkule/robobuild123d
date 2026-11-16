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
MOT_X = P.POD_W/2 - P.TUB_WALL - P.N10_BODY_OUT
WH_X = P.wheel_x()
FTOP = P.tub_floor_z() + P.TUB_FLOOR_T
PANEL_Z0 = P.TUB_TOP_Z - P.TOP_PANEL_T
BAT_Y = -12.0
ESC_Y = 1.5
RX_Y = -1.0
RX_Z = P.TUB_TOP_Z - P.TOP_PANEL_T - 1.25
SW_Z = 25.7
GRIP_S = P.TOP_PANEL_T + P.BOSS_T
WIRE_Z = 24.0          # centre channel: over the drive motors (top 22), under the rx (26.5)
WIRE_Z_SIDE = 23.0     # x = +-28.5 corridor: under the panel posts (24), over the motors (22)

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
    {"id": "wheel_r", "kind": "wheel", "catalog": "bbb_wheel_34x6_5", "at": [WH_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 0.0]},
    {"id": "wheel_l", "kind": "wheel", "catalog": "bbb_wheel_34x6_5", "at": [-WH_X, WY, P.WHEEL_CZ], "rot": [0.0, 0.0, 180.0]},
    {"id": "battery", "kind": "battery", "catalog": P.BATTERY, "at": [0.0, BAT_Y, FTOP + 6.0],
     "rot": [0.0, 0.0, 0.0], "retained": "strap",
     "label": "2S 300 mAh HV pack in the pod behind the motors; a poly strap through printed slots holds it down (the strap carries the inverted load)"},
    {"id": "weapon_esc", "kind": "esc", "catalog": "bbb_brushless_esc_20a", "at": [0.0, ESC_Y, FTOP + 2.0],
     "rot": [0.0, 0.0, 0.0], "retained": "adhesive",
     "label": "20 A brushless ESC on the pod floor ahead of the motors, bonded on a foam pad"},
    {"id": "drive_rx", "kind": "esc", "catalog": "bbb_malenki_nano", "at": [0.0, RX_Y, RX_Z],
     "rot": [0.0, 0.0, 0.0], "retained": "adhesive",
     "label": "Malenki-Nano combined drive ESC + receiver, taped to the top panel's underside ahead of the weapon housing"},
    {"id": "switch", "kind": "switch", "catalog": "fingertech_mini_switch", "at": [0.0, P.switch_y(), SW_Z],
     "rot": [0.0, 0.0, 270.0], "retained": "clamp", "marked": True, "tool_free": True,
     "label": "mini switch in its bay at the pod's rear, clamped to the top panel by its own bushing and nut through the 4 mm key hole"}
  ],
  "fasteners": holes_h() + holes_s() + holes_p(),
  "wires": [
    {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 22, "kind": "power", "slack_mm": 8.0,
     "via": [[0.0, BAT_Y + 8.0, WIRE_Z], [-28.5, BAT_Y + 8.0, WIRE_Z_SIDE], [-28.5, P.switch_y() + 3.8, WIRE_Z_SIDE]]},
    {"id": "w_sw_rx", "from": "switch.out", "to": "drive_rx.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "via": [[-28.5, P.switch_y() - 3.8, WIRE_Z_SIDE], [-28.5, -10.0, WIRE_Z_SIDE], [-18.0, -10.0, 24.5], [-18.0, -10.0, RX_Z - 0.5]]},
    {"id": "w_sw_wesc", "from": "switch.out", "to": "weapon_esc.bat", "awg": 26, "kind": "power", "slack_mm": 8.0,
     "via": [[-28.5, P.switch_y() - 3.8, WIRE_Z_SIDE], [-28.5, 2.0, WIRE_Z_SIDE], [-14.0, 2.0, WIRE_Z_SIDE], [-14.0, 2.0, FTOP + 2.0]]},
    {"id": "w_rx_ml", "from": "drive_rx.m1", "to": "drive_motor_l.terminals", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[16.0, RX_Y + 6.0, WIRE_Z], [-6.5, RX_Y + 6.0, WIRE_Z], [-6.5, WY, WIRE_Z]]},
    {"id": "w_rx_mr", "from": "drive_rx.m2", "to": "drive_motor_r.terminals", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[-16.0, RX_Y + 6.0, WIRE_Z], [6.5, RX_Y + 6.0, WIRE_Z], [6.5, WY, WIRE_Z]]},
    {"id": "w_rx_wpn", "from": "drive_rx.wpn", "to": "weapon_esc.rx", "awg": 26, "kind": "signal", "slack_mm": 8.0,
     "via": [[16.0, RX_Y - 6.0, WIRE_Z], [-14.0, RX_Y - 6.0, WIRE_Z], [-14.0, ESC_Y + 3.0, WIRE_Z]]},
    {"id": "w_wesc_m", "from": "weapon_esc.motor", "to": "weapon_motor_stator.phases", "awg": 22, "kind": "power", "slack_mm": 10.0,
     "via": [[11.5, ESC_Y, WIRE_Z], [17.0, 31.0, WIRE_Z], [15.6, AY + 15.6, 26.0], [11.3, AY + 11.3, 28.4], [3.5, AY + 3.5, 27.2]]}
  ],
  "connections": [
    {"a": "bar", "b": "wshaft", "method": "shaft", "reason": "the bar's 3.1 mm bore pilots on the motor's own shaft (0.05 mm slide): the shaft centres the bar, the clamp nut sets its height and the M2.5s carry the torque", "mechanical_key": True},
    {"a": "weapon_hub", "b": "wshaft", "method": "shaft", "reason": "the hub's 3.2 mm bore runs on the shaft (0.1 mm slide): the shaft locates it, the clamp and the bar screws carry the torque"},
    {"a": "wshaft", "b": "weapon_motor_bell", "method": "press_fit", "reason": "the motor's own shaft, a press fit in the bell's bored rotor core (the catalogue draws the bore at r1.45); the nut clamps bar + hub to the bell cap face so the stack turns as one", "interference_mm": 0.05, "mechanical_key": True},
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
    {"a": "wheel_r", "b": "drive_motor_r", "max_depth_mm": 0.6, "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the D-flat keys the drive"},
    {"a": "wheel_l", "b": "drive_motor_l", "max_depth_mm": 0.6, "reason": "the wheel's D-bore is cut 0.1 mm large on the flat sides so it slides on; the D-flat keys the drive"}
  ],
  "notes": "Derived by the src/scythe relations; poses computed from params.py. Motor-as-hub weapon (the reference hspin_bar's topology): the bl_1806's own extended shaft carries the rotor from above; the bar is a cantilevered undercutter whose stored energy stays under the 20 J escalation threshold. The battery lead runs around the pack at the pod wall."
}
with open('robots/scythe/spec.json', 'w') as f:
    json.dump(spec, f, indent=1)
print('spec written: AY', round(AY,2), 'WY', round(WY,2), 'switch_y', round(P.switch_y(),2), 'BAR_L', P.BAR_L,
      'mass', round(P.total_mass_g(),1), 'E[J]', round(P.energy_j(P.bar_rpm()),1))
