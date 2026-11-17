"""Write spec.json for Scythe Classic from the scythe_classic masters (run: python robots/scythe_classic/make_spec.py).

Every coordinate that depends on the layout (weapon axis, bar, hub, motors, wheels, fastener positions) is written as
a relation of scythe_classic.params, so a master change moves the parts, their holes and their fasteners together.
Hand-placed electronics use the named positions below. The spec's `params` entry lets the verifier evaluate the
`at` expressions against the same module (robot/spec.py).
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "src"))

import scythe_classic.panels as panels  # noqa: E402
import scythe_classic.params as P  # noqa: E402
import scythe_classic.skids as skids  # noqa: E402
from scythe_classic._reuse import weapon_motor  # noqa: E402

PARAMS_PATH = "src/scythe_classic/params.py"

# Hand-placed electronics (x, y, z) in mm, rear pod and cone interior. Checked with `robot verify`.
FLOOR_IN = P.tub_floor_z() + P.TUB_FLOOR_T   # z of the pod cavity floor (inside the tub): electronics sit on it
BATTERY_AT = (-19.1, 15.6, FLOOR_IN + 0.5 + 5.5)   # probe --place battery: safe box x -21.9..-16.4, y 10.6..20.6 at yaw 90
ESC_AT = (0.0, -14.0, FLOOR_IN + 0.5 + 2.0)
RX_AT = (25.6, 14.9, FLOOR_IN + 0.5 + 1.25)   # probe --place drive_rx: free box x 16.1..35.1 y -1.1..30.9          # Malenki-Nano, yawed 90 deg, rests on the floor (tape)
XT30_AT = (-19.6, -31.4, FLOOR_IN + 0.5 + 5.1)   # probe --place xt30 (pod rear): free box x -26.5..-12.8 y -34.0..-28.8 at yaw 90
TOP_Z = P.TUB_TOP_Z                 # top face of the top panel
SKID_TOP_Z = TOP_Z + P.MIN_GROUND_CLR + P.SKID_H


def _fmt(v):
    return [round(float(c), 3) for c in v]


def _hole(d, length, head, dk=None):
    h = {"d": d, "length": length, "head": head, "clearance_d": d + 0.2, "into": "through", "side": "head",
         "grip": 1.0, "sink": 0.0}
    if head == "csk":
        h.update(csk_angle=90.0, csk_d=dk, csk_depth=P.CSK_DEPTH, head_std="ISO 14581")   # = bar.countersinks() depth
    return h


def _screw(fid, designation, at, direction, through, threads_into, head, hole):
    return {"id": fid, "designation": designation, "material": "steel", "at": _fmt(at), "dir": list(direction),
            "through": through, "threads_into": threads_into, "tool": "hex1.3" if head != "csk" else "hex2.5",
            "hole": hole, "head": "countersunk" if head == "csk" else "button", "removable": True}


def fasteners():
    out = []
    for i, (x, y) in enumerate(panels.rim_xy()):
        out.append(_screw(f"rim_{i}", "M2x6", (x, y, TOP_Z), (0, 0, -1), ["top_panel"], "tub", "button",
                          _hole(2.0, 6.0, "button")))
    for i, (r, deg, _d) in enumerate(weapon_motor.describe(P.WEAPON_MOTOR)["base_holes"]):
        x = r * math.cos(math.radians(deg))
        y = P.WPN_AXIS_Y + r * math.sin(math.radians(deg))
        out.append(_screw(f"stator_{i}", "M2x3", (x, y, TOP_Z), (0, 0, -1), ["top_panel"], "weapon_motor_stator",
                          "button", _hole(2.0, 3.0, "button")))
    for i, sign in enumerate((-1, 1)):
        out.append(_screw(f"bar_{i}", "M3x8", (sign * P.BAR_BOLT_PCD / 2, P.WPN_AXIS_Y, P.BAR_Z0), (0, 0, 1),
                          ["bar"], "weapon_hub", "csk", _hole(3.0, 8.0, "csk", P.CSK_D)))
    for i, sx in enumerate(skids.ARM_SCREW_X):   # skid arm riser: M2 from the pod cavity down through the tub floor into the arm
        out.append(_screw(f"arm_{i}", "M2x8", (sx, sum(skids.ARM_RISER_Y) / 2, FLOOR_IN), (0, 0, -1), ["tub"], "skid_arm",
                          "button", _hole(2.0, 8.0, "button")))
    return out


def parts():
    wpn = (0.0, P.WPN_AXIS_Y)
    return [
        {"id": "tub", "kind": "structure", "catalog": None, "material": "nylon", "process": "fdm",
         "print_orientation": "+z", "solid_fraction": 0.4,
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "tub"}},
         "at": [0, 0, 0], "rot": [0, 0, 0],
         "label": "printed nylon tub: sloped cone over the bar, vertical rear pod carrying the N10s"},
        {"id": "top_panel", "kind": "structure", "catalog": None, "material": "pa_cf", "process": "fdm",
         "print_orientation": "+z",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "top_panel"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "1 mm PA-CF top skin, M2 button screws"},
        {"id": "bar", "kind": "weapon", "catalog": None, "material": "steel", "process": "sheet_cut",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "bar"}},
         "at": [0, f"P.WPN_AXIS_Y", "P.BAR_Z0"], "rot": [0, 0, 0], "rotates_with": "weapon",
         "joint": {"kind": "revolute", "axis": [0.0, 0.0, 1.0], "pivot": [0.0, P.WPN_AXIS_Y, 0.0], "min": 0, "max": 360, "default": 0},
         "weapon": {"kind": "bar", "motor": "weapon_motor_stator", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                    "spin_dir": "ccw", "teeth": 2, "locking_bar": "lock_pin"},
         "secondary_ops": ["countersink"],
         "label": "3 mm steel two-tooth bar, 116 mm, horizontal under the tub"},
        {"id": "weapon_hub", "kind": "hub", "catalog": None, "material": "aluminium", "process": "turned",
         "secondary_ops": ["drilled"],
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "weapon_hub"}},
         "at": [0, "P.WPN_AXIS_Y", "P.bar_top_z() + P.HUB_GAP"], "rot": [0, 0, 0], "rotates_with": "weapon",
         "label": "turned 7075 hub, bar 2x M3"},
        {"id": "weapon_shaft", "kind": "shaft", "catalog": None, "material": "steel", "process": "turned", "shaft_of": "weapon_motor_can",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "weapon_shaft"}},
         "rotates_with": "weapon", "at": [0, 0, 0], "rot": [0, 0, 0],
         "label": "5 mm steel weapon shaft through the bar bore, the hub and the caster bearing"},
        {"id": "bearing_caster", "kind": "bearing", "catalog": None, "material": "steel", "process": "cots", "rotates_with": "fixed",
         "stock": "MR85ZZ 5 x 8 x 2.5",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "bearing_caster"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "MR85ZZ bearing: inner ring on the shaft, outer ring in the caster puck"},
        {"id": "lock_pin", "kind": "locking_bar", "catalog": None, "material": "steel", "process": "turned", "tethered": True,
         "color": [255, 90, 0], "retained": "pin",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "lock_pin"}},
         "at": [0, 0, 0], "rot": [0, 0, 0],
         "label": "rule 5f lock: removable 3 mm steel pin through the bar's lock hole into the tub floor (orange, tethered)"},
        {"id": "skid_arm", "kind": "structure", "catalog": None, "material": "pa_cf", "process": "fdm", "print_orientation": "+z",
         "solid_fraction": 1.0,
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "skid_arm"}},
         "at": [0, 0, 0], "rot": [0, 0, 0],
         "label": "printed strip under the whole bar sweep, from the pod floor to a puck on the axis holding the MR85 (bar passes 1.1 mm over it)"},
        {"id": "skid_dome", "kind": "structure", "catalog": None, "material": "uhmw", "process": "turned",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "skid_dome"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "POM button on the top panel (inverted front contact), stem plugged in a 3 mm panel hole"},
        {"id": "weapon_motor_stator", "kind": "weapon_motor", "catalog": "gr1507", "at": ["0", "P.WPN_AXIS_Y", "P.wpn_motor_z()"],
         "rot": [0.0, 90.0, 0.0], "label": "GR1507 shaft down"},
        {"id": "weapon_motor_can", "kind": "other", "role": "rotor", "catalog": "gr1507_can",
         "rotates_with": "weapon", "at": ["0", "P.WPN_AXIS_Y", "P.wpn_motor_z()"], "rot": [0.0, 90.0, 0.0],
         "label": "GR1507 bell and core: spins with the hub and shaft round the fixed stator"},
        {"id": "drive_motor_r", "kind": "motor", "catalog": "bbb_n10_1000rpm", "retained": "press_fit",
         "at": ["P.motor_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 0.0]},
        {"id": "drive_motor_l", "kind": "motor", "catalog": "bbb_n10_1000rpm", "retained": "press_fit",
         "at": ["-P.motor_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 180.0]},
        {"id": "wheel_r", "kind": "wheel", "catalog": "bbb_wheel_34x6_5",
         "at": ["P.wheel_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [90.0, 0.0, 0.0]},   # rx 90: the hub's D flat sits on the N10 shaft flat
        {"id": "wheel_l", "kind": "wheel", "catalog": "bbb_wheel_34x6_5",
         "at": ["-P.wheel_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [90.0, 0.0, 180.0]},
        {"id": "battery", "kind": "battery", "catalog": P.BATTERY, "retained": "strap",
         "retained_reason": "hook-and-loop strap over the pack, anchored to rib pegs in the pod; undone to change the pack",
         "at": _fmt(BATTERY_AT), "rot": [0, 0, 90],
         "label": "2S 180 mAh pack in the rear pod (smaller than the old 300 mAh: see params)"},
        {"id": "weapon_esc", "kind": "esc", "catalog": P.WEAPON_ESC, "retained": "tape",
         "retained_reason": "double-sided foam tape under the ESC onto the pod floor; the board weighs 5 g",
         "at": _fmt(ESC_AT), "rot": [0, 0, 0]},
        {"id": "drive_rx", "kind": "esc", "catalog": P.DRIVE_RX, "retained": "tape",
         "at": _fmt(RX_AT), "rot": [0, 0, 90]},
        {"id": "switch", "kind": "switch", "catalog": P.SWITCH, "retained": "velcro", "tool_free": True, "marked": True,
         "label": "power switch ON/OFF, reached through the top-panel key hole",
         "at": ["P.SWITCH_XY[0] + 1.2", "P.SWITCH_XY[1]", FLOOR_IN + 3.175], "rot": [0, 0, 90]},
        {"id": "xt30", "kind": "connector", "catalog": P.CONNECTOR,
         "at": _fmt(XT30_AT), "rot": [0, 0, 90], "retained": "snap"},
    ]


def connections():
    return [
        {"a": "top_panel", "b": "tub", "method": "screw", "reason": "4x M2 rim screws into the cone wall top"},
        {"a": "bar", "b": "weapon_hub", "method": "screw", "reason": "2x M3 countersunk bolts through the bar into the tapped hub"},
        {"a": "weapon_hub", "b": "weapon_motor_can", "method": "press_fit", "mechanical_key": True,
         "reason": "hub clamped to the bell top by the bell screws (key: flats on the shaft)"},
        {"a": "weapon_shaft", "b": "weapon_hub", "method": "press_fit", "mechanical_key": True,
         "reason": "shaft pressed into the hub bore, grub screw on the flat"},
        {"a": "weapon_shaft", "b": "bearing_caster", "method": "press_fit", "reason": "MR85 inner ring pressed on the 5 mm shaft"},
        {"a": "bearing_caster", "b": "skid_arm", "method": "press_fit", "reason": "MR85 outer ring pressed in the skid arm's puck bore"},
        {"a": "skid_arm", "b": "tub", "method": "screw", "reason": "2x M2 from the pod cavity through the tub floor into the arm riser"},
        {"a": "lock_pin", "b": "tub", "method": "pin", "reason": "pin seats in a socket in the tub floor underside; tethered to the tub"},
        {"a": "switch", "b": "tub", "method": "snap", "reason": "snaps into a moulded cradle on the tub floor"},
        {"a": "xt30", "b": "tub", "method": "snap", "reason": "XT30 clips into a moulded holder on the pod floor"},
        {"a": "skid_dome", "b": "top_panel", "method": "snap", "reason": "the dome's 2.9 mm stem snaps into a 3 mm top-panel hole; a hit on the dome presses it onto the panel"},
        {"a": "wheel_r", "b": "drive_motor_r", "method": "press_fit", "mechanical_key": True, "reason": "N10 D-shaft bore, grub screw on the flat"},
        {"a": "wheel_l", "b": "drive_motor_l", "method": "press_fit", "mechanical_key": True, "reason": "N10 D-shaft bore, grub screw on the flat"},
        {"a": "drive_motor_r", "b": "tub", "method": "interlock", "reason": "N10 body seats in the pod wall"},
        {"a": "drive_motor_l", "b": "tub", "method": "interlock", "reason": "N10 body seats in the pod wall"},
        {"a": "weapon_motor_stator", "b": "top_panel", "method": "screw", "reason": "4x M2x3 from the top panel into the stator base"},
    ]


def wires():
    return [
        {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 24, "kind": "power", "slack_mm": 8},
        {"id": "w_sw_rx", "from": "switch.out", "to": "drive_rx.bat", "awg": 24, "kind": "power", "slack_mm": 8},
        {"id": "w_sw_esc", "from": "switch.out", "to": "weapon_esc.bat", "awg": 24, "kind": "power", "slack_mm": 8, "via": [[16.0, 36.0, 18.0], [18.0, -2.0, 18.0]]},
        {"id": "w_esc_wpn", "from": "weapon_esc.motor", "to": "weapon_motor_stator.phases", "awg": 22, "kind": "power", "slack_mm": 6},
        {"id": "w_rx_m1", "from": "drive_rx.m1", "to": "drive_motor_r.terminals", "awg": 26, "kind": "signal", "slack_mm": 4},
        {"id": "w_rx_m2", "from": "drive_rx.m2", "to": "drive_motor_l.terminals", "awg": 26, "kind": "signal", "slack_mm": 4},
        {"id": "w_rx_wpn", "from": "drive_rx.wpn", "to": "weapon_esc.rx", "awg": 26, "kind": "signal", "slack_mm": 4, "via": [[22.0, -2.0, 18.0]]},
    ]


def build():
    return {
        "name": "Scythe Classic (horizontal undercutter bar spinner, old f363606 look)",
        "generator": "make_spec.py",
        "profile": "aws2025",
        "robot_type": "horizontal_spinner",
        "locomotion": "roller",
        "params": {"P": PARAMS_PATH},
        "parts": parts(),
        "fasteners": fasteners(),
        "connections": connections(),
        "wires": wires(),
        "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
        "notes": "Generated by make_spec.py from scythe_classic.params. Do not edit by hand.",
    }


def main():
    out = os.path.join(HERE, "spec.json")
    with open(out, "w") as fh:
        json.dump(build(), fh, indent=1)
        fh.write("\n")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
