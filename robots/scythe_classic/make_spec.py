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
from scythe_classic._reuse import weapon_motor  # noqa: E402

PARAMS_PATH = "src/scythe_classic/params.py"

# Hand-placed electronics (x, y, z) in mm, rear pod and cone interior. Checked with `robot verify`.
BATTERY_AT = (-0.58, -30.0, 15.5)     # 1 mm above the floor top (tub contact tolerance)
ESC_AT = (0.0, -14.0, 10.5)
RX_AT = (22.49, -4.0, 10.75)          # Malenki-Nano, yawed 90 deg, rests on the floor (tape)
XT30_AT = (-23.5, -16.0, 15.1)
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
        out.append(_screw(f"stator_{i}", "M2x6", (x, y, TOP_Z), (0, 0, -1), ["top_panel", "tub"], "weapon_motor",
                          "button", _hole(2.0, 6.0, "button")))
    for i, sign in enumerate((-1, 1)):
        out.append(_screw(f"bar_{i}", "M3x8", (sign * P.BAR_BOLT_PCD / 2, P.WPN_AXIS_Y, P.BAR_Z0), (0, 0, 1),
                          ["bar"], "weapon_hub", "csk", _hole(3.0, 8.0, "csk", P.CSK_D)))
    out.append(_screw("dome_0", "M2x10", (0.0, P.WPN_AXIS_Y, SKID_TOP_Z), (0, 0, -1), ["skid_dome", "top_panel"],
                      "weapon_motor", "button", _hole(2.0, 10.0, "button")))
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
         "at": [0, f"P.WPN_AXIS_Y", "P.BAR_Z0"], "rot": [0, 0, 0],
         "weapon": {"kind": "bar", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                    "spin_dir": "ccw", "teeth": 2},
         "secondary_ops": ["countersink"],
         "label": "3 mm steel two-tooth bar, 116 mm, horizontal under the tub"},
        {"id": "weapon_hub", "kind": "hub", "catalog": None, "material": "aluminium", "process": "turned",
         "secondary_ops": ["drilled"],
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "weapon_hub"}},
         "at": [0, "P.WPN_AXIS_Y", "P.bar_top_z()"], "rot": [0, 0, 0], "label": "turned 7075 hub, bar 2x M3"},
        {"id": "caster", "kind": "caster", "catalog": None, "material": "uhmw", "process": "turned",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "caster"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "ball caster under the tub front, ahead of the CoM"},
        {"id": "skid_foot", "kind": "skid", "catalog": None, "material": "uhmw", "process": "turned",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "skid_foot"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "POM-class shaft-end foot"},
        {"id": "skid_dome", "kind": "structure", "catalog": None, "material": "uhmw", "process": "turned",
         "shape": {"type": "model", "file": "src/build_scythe_classic.py", "params": {"part": "skid_dome"}},
         "at": [0, 0, 0], "rot": [0, 0, 0], "label": "POM-class dome on the top panel"},
        {"id": "weapon_motor", "kind": "weapon_motor", "catalog": "gr1507", "at": ["0", "P.WPN_AXIS_Y", "P.wpn_motor_z()"],
         "rot": [0.0, 90.0, 0.0], "label": "GR1507 shaft down"},
        {"id": "drive_motor_r", "kind": "drive_motor", "catalog": "bbb_n10_1000rpm",
         "at": ["P.motor_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 0.0]},
        {"id": "drive_motor_l", "kind": "drive_motor", "catalog": "bbb_n10_1000rpm",
         "at": ["-P.motor_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 180.0]},
        {"id": "wheel_r", "kind": "wheel", "catalog": "bbb_wheel_34x6_5",
         "at": ["P.wheel_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 0.0]},
        {"id": "wheel_l", "kind": "wheel", "catalog": "bbb_wheel_34x6_5",
         "at": ["-P.wheel_x()", "P.wheel_y()", "P.WHEEL_CZ"], "rot": [0.0, 0.0, 180.0]},
        {"id": "battery", "kind": "battery", "catalog": P.BATTERY, "retained": "pocket",
         "at": _fmt(BATTERY_AT), "rot": [0, 0, 0],
         "label": "2S 180 mAh pack in the rear pod (smaller than the old 300 mAh: see params)"},
        {"id": "weapon_esc", "kind": "esc", "catalog": P.WEAPON_ESC, "retained": "velcro",
         "at": _fmt(ESC_AT), "rot": [0, 0, 0]},
        {"id": "drive_rx", "kind": "esc", "catalog": P.DRIVE_RX, "retained": "tape",
         "at": _fmt(RX_AT), "rot": [0, 0, 90]},
        {"id": "switch", "kind": "switch", "catalog": P.SWITCH, "retained": "velcro", "tool_free": True, "marked": True,
         "label": "power switch ON/OFF, reached through the top-panel key hole",
         "at": ["P.SWITCH_XY[0] + 1.2", "P.SWITCH_XY[1]", 12.7], "rot": [0, 0, 0]},
        {"id": "xt30", "kind": "connector", "catalog": P.CONNECTOR, "retained": "velcro",
         "at": _fmt(XT30_AT), "rot": [0, 0, 0]},
    ]


def connections():
    return [
        {"a": "top_panel", "b": "tub", "method": "screw", "reason": "4x M2 rim screws into the cone wall top"},
        {"a": "bar", "b": "weapon_hub", "method": "screw", "reason": "2x M3 countersunk bolts through the bar into the tapped hub"},
        {"a": "weapon_hub", "b": "weapon_motor", "method": "shaft", "reason": "hub bores on the 5 mm shaft, clamped by its screws"},
        {"a": "skid_foot", "b": "bar", "method": "shaft", "reason": "foot turns with the bar on the shaft end, captured by the shaft nut"},
        {"a": "caster", "b": "tub", "method": "screw", "reason": "ball caster housing screwed under the tub front floor"},
        {"a": "skid_dome", "b": "top_panel", "method": "screw", "reason": "M2 screw from the dome through the top panel into the stator base"},
        {"a": "wheel_r", "b": "drive_motor_r", "method": "shaft", "reason": "N10 D-shaft bore, grub screw on the flat"},
        {"a": "wheel_l", "b": "drive_motor_l", "method": "shaft", "reason": "N10 D-shaft bore, grub screw on the flat"},
        {"a": "drive_motor_r", "b": "tub", "method": "interlock", "reason": "N10 body seats in the pod wall"},
        {"a": "drive_motor_l", "b": "tub", "method": "interlock", "reason": "N10 body seats in the pod wall"},
        {"a": "weapon_motor", "b": "tub", "method": "screw", "reason": "stator base screws down through the top panel and boss"},
    ]


def wires():
    return [
        {"id": "w_bat_sw", "from": "battery.xt30", "to": "switch.in", "awg": 24, "kind": "power", "slack_mm": 8},
        {"id": "w_sw_rx", "from": "switch.out", "to": "drive_rx.bat", "awg": 24, "kind": "power", "slack_mm": 8},
        {"id": "w_sw_esc", "from": "switch.out", "to": "weapon_esc.bat", "awg": 24, "kind": "power", "slack_mm": 8},
        {"id": "w_esc_wpn", "from": "weapon_esc.motor", "to": "weapon_motor.phases", "awg": 22, "kind": "power", "slack_mm": 6},
        {"id": "w_rx_m1", "from": "drive_rx.m1", "to": "drive_motor_r.terminals", "awg": 26, "kind": "signal", "slack_mm": 4},
        {"id": "w_rx_m2", "from": "drive_rx.m2", "to": "drive_motor_l.terminals", "awg": 26, "kind": "signal", "slack_mm": 4},
        {"id": "w_rx_wpn", "from": "drive_rx.wpn", "to": "weapon_esc.rx", "awg": 26, "kind": "signal", "slack_mm": 4},
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
