"""Generate robots/disector/spec.json and provide build(part=...) entry point."""

from __future__ import annotations

import json
from pathlib import Path

from . import chassis, fasteners as F, front, params as P, weapon

MODEL_FILE = "src/build_disector.py"


def build(part: str):
    builders = {
        "tub": chassis.build_tub,
        "panel_top": chassis.build_panel_top,
        "top_spine": chassis.build_top_spine,
        "wedge_front": front.build_wedge_front,
        "fork_mount_l": lambda: front.build_fork_mount(-1.0),
        "fork_mount_r": lambda: front.build_fork_mount(1.0),
        "fork_l": lambda: front.build_fork(-1.0),
        "fork_r": lambda: front.build_fork(1.0),
        "skid_l": lambda: front.build_skid(-1.0),
        "skid_r": lambda: front.build_skid(1.0),
        "guard_l": lambda: front.build_guard(-1.0),
        "guard_r": lambda: front.build_guard(1.0),
        "eye_l": lambda: front.build_eye(-1.0),
        "eye_r": lambda: front.build_eye(1.0),
        "arm": weapon.build_arm,
        "weapon_shaft": weapon.build_weapon_shaft,
        "disc": weapon.build_disc,
        "locking_bar": weapon.build_locking_bar,
    }
    if part not in builders:
        raise ValueError(f"Unknown part: {part}")
    sol = builders[part]()
    if part != "disc":
        sol = F.apply_holes_to_part(part, sol)
    return sol


def _m(part_id: str) -> dict:
    return {"type": "model", "file": MODEL_FILE, "params": {"part": part_id}}


def _struct(pid, kind, material, color, label=None, **kw):
    """A printed/cut part built from this package's builders (`at`/`rot` identity: shapes are placed in world coords)."""
    d = {"id": pid, "kind": kind, "material": material, "process": kw.pop("process", "fdm"), "color": color,
         "shape": _m(pid), "at": [0, 0, 0], "rot": [0, 0, 0]}
    if label:
        d["label"] = label
    d.update(kw)
    return d


def _parts_chassis() -> list[dict]:
    return [
        _struct("tub", "structure", "nylon", P.COL_CHASSIS, print_orientation="+z", solid_fraction=P.TUB_SOLID,
                sharp_corners_ok="Internal electronics bays and wire channels in nylon tub print with 0.4 mm nozzle corner radius; fastener bosses are in compression",
                label="Unibody nylon chassis tub with sloped front, wheel wells, and electronics bays"),
        _struct("panel_top", "plate", "nylon", P.COL_TOP_PANEL, print_orientation="+z", solid_fraction=P.PANEL_SOLID,
                sharp_corners_ok="Rectangular switch and wire pass-through cutouts in 1.2 mm nylon top plate are unloaded",
                label="Top deck cover plate", tags=["lid"]),   # tag only labels it as the lid for `render --no-lid`
        _struct("top_spine", "plate", "pla", P.COL_TOP_SPINE, print_orientation="+z", solid_fraction=P.PANEL_SOLID,
                label="Black top front clamping strap"),
    ]


def _parts_front() -> list[dict]:
    fm_note = "45-deg counterbored fastener seats and clevis slot are in compression against wedge"
    sk_note = "45-deg counterbored fastener seats are in compression against wedge"
    out = [_struct("wedge_front", "wedge", "aluminium", P.COL_WEDGE, process="laser",
                   label="Aluminium sloped front wedge plate with scoop lip")]
    for t in ("l", "r"):
        out.append(_struct(f"fork_mount_{t}", "armor", "pla", P.COL_ORANGE, print_orientation="+z", sharp_corners_ok=fm_note))
    for t in ("l", "r"):
        out.append(_struct(f"fork_{t}", "fork", "titanium", P.COL_FORK, process="laser"))
    for t in ("l", "r"):
        out.append(_struct(f"skid_{t}", "wedge", "pla", P.COL_ORANGE, print_orientation="+x", sharp_corners_ok=sk_note))
    for t in ("l", "r"):
        out.append(_struct(f"guard_{t}", "armor", "pla", P.COL_ORANGE, print_orientation="+x"))
    for t in ("l", "r"):
        out.append(_struct(f"eye_{t}", "other", "pla", P.COL_EYE_WHITE, print_orientation="+z", retained="press_fit"))
    return out


def _parts_weapon() -> list[dict]:
    tip = P.WPN_MOTOR_AT
    spin = "weapon_motor_bell"      # rotor group label: the bell carries the shaft and the disc
    disc_at = [P.DISC_AT[i] - tip[i] for i in range(3)]      # disc is a child of the bell: placed in the bell frame
    return [
        # The overhead arm is the structural carrier of the weapon motor, so it is a `structure` (wires may route along it)
        _struct("arm", "structure", "nylon", P.COL_ARM, print_orientation="+x"),
        {"id": "weapon_motor_stator", "exposed": True, "kind": "weapon_motor", "catalog": "gr1507", "parent": "arm",
         "exposed_reason": "Overhead hammer-saw motor stator mounted at tip of arm", "at": tip, "rot": P.WPN_MOTOR_ROT},
        {"id": "weapon_motor_bell", "exposed": True, "kind": "other", "catalog": "gr1507_can", "parent": "arm",
         "rotates_with": spin, "exposed_reason": "Rotating outrunner bell carrying the saw disc at tip of overhead arm",
         "at": tip, "rot": P.WPN_MOTOR_ROT,
         "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": P.BELL_PIVOT, "min": -180, "max": 180, "default": 0}},
        {"id": "weapon_shaft", "kind": "shaft", "material": "steel", "process": "cots", "solid_fraction": P.SHAFT_SOLID,
         "shaft_of": "weapon_motor_bell", "rotates_with": spin, "parent": "weapon_motor_bell", "exposed": True,
         "exposed_reason": "GR1507 5 mm threaded prop shaft protruding from motor bell", "color": "#777777",
         "shape": _m("weapon_shaft"), "at": [0, 0, 0], "rot": [0, 0, 0]},
        {"id": "disc", "kind": "weapon", "material": "titanium", "process": "laser", "rotates_with": spin,
         "min_web_mm": P.DISC_MIN_WEB, "min_web_reason": "GR1507 9 mm PCD M2 pattern around 5.2 mm centre bore",
         "color": P.COL_DISC, "parent": "weapon_motor_bell", "shape": _m("disc"), "at": disc_at, "rot": P.DISC_ROT,
         "weapon": {"kind": "overhead_saw", "motor": "weapon_motor_stator", "cells": 2, "reduction": 1.0,
                    "spin_axis": [0, 0, 1], "locking_bar": "locking_bar"}},
        _struct("locking_bar", "locking_bar", "pla", P.COL_LOCK, print_orientation="+x", tethered=True, parent="arm"),
    ]


def _parts_drive_electronics() -> list[dict]:
    drive = []
    for t, sx, yaw in (("l", -1.0, 180), ("r", 1.0, 0)):
        drive.append({"id": f"motor_{t}", "kind": "motor", "catalog": "n10_2200rpm_6v",
                      "at": [sx * P.MOTOR_X, P.WHEEL_Y, P.WHEEL_Z], "rot": [0, 0, yaw]})
    for t, sx, yaw in (("l", -1.0, 180), ("r", 1.0, 0)):
        drive.append({"id": f"wheel_{t}", "kind": "wheel", "catalog": "wheel_20x8",
                      "at": [sx * P.WHEEL_X, P.WHEEL_Y, P.WHEEL_Z], "rot": [0, 0, yaw]})
    return drive + [
        {"id": "battery", "kind": "battery", "catalog": "lipo_2s_350", "retained": "velcro", "at": P.BAT_AT, "rot": [0, 0, 0]},
        {"id": "malenki_rx", "kind": "esc", "catalog": "malenki_nano", "retained": "tape", "at": P.MALENKI_AT, "rot": [0, 0, 0]},
        {"id": "weapon_esc", "kind": "esc", "catalog": "bbb_ant_esc", "retained": "tape", "at": P.WPN_ESC_AT, "rot": [0, 0, 0]},
        {"id": "servo", "exposed": True, "kind": "servo", "catalog": "servo_cs07", "retained": "press_fit",
         "at": P.SERVO_AT, "rot": P.SERVO_ROT},
        {"id": "switch", "kind": "switch", "catalog": "switch_bbb_ant_rvrn2", "tool_free": True, "marked": True,
         "label": "Power slide switch ON/OFF", "at": P.SWITCH_AT, "rot": [0, 0, 0]},
    ]


def _conn(a, b, method, reason, **kw):
    return {"a": a, "b": b, "method": method, "reason": reason, **kw}


def _connections() -> list[dict]:
    c = [
        _conn("panel_top", "tub", "screw", "Top deck panel closes electronics bays and clamps drive motors"),
        _conn("top_spine", "tub", "screw", "Top front strap clamps top panel to chassis front"),
        _conn("wedge_front", "tub", "screw", "Aluminium front wedge absorbs horizontal impacts"),
    ]
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"fork_mount_{t}", "wedge_front", "screw", f"{side} fork clevis mount carries ground-scraping fork loads"))
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"fork_{t}", f"fork_mount_{t}", "shaft", f"{side} fork pivots freely on M2 clevis pin to follow the floor"))
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"skid_{t}", "wedge_front", "screw", f"{side} outer skid bolts to front wedge corner"))
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"guard_{t}", "tub", "screw", f"{side} wheel guard bolts to side wall to shield wheel"))
    for t in ("l", "r"):
        c.append(_conn(f"eye_{t}", "wedge_front", "snap", "Decorative googly eye snapped into recessed boss on front wedge"))
    c += [
        _conn("arm", "servo", "shaft", "Overhead hammer-saw arm pivots on servo output spline"),
        _conn("weapon_motor_stator", "arm", "screw", "Brushless motor stator bolted to overhead arm tip"),
        _conn("weapon_motor_bell", "weapon_motor_stator", "shaft", "Motor bell spins on stator shaft bearings"),
        _conn("weapon_shaft", "weapon_motor_bell", "press_fit", "GR1507 5 mm steel shaft pressed into motor bell",
              interference_mm=P.SHAFT_PRESS_MM, mechanical_key=True),
        _conn("disc", "weapon_motor_bell", "screw", "Titanium saw disc bolted directly to motor bell"),
        _conn("locking_bar", "arm", "pin", "Removable safety pin locks into arm and blocks saw disc rotation during pit handling"),
    ]
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"motor_{t}", "tub", "snap", f"{side} N10 gearmotor captured in pocket under top panel"))
    for t, side in (("l", "Left"), ("r", "Right")):
        c.append(_conn(f"wheel_{t}", f"motor_{t}", "press_fit", f"{side} wheel press-fit onto 3 mm D-shaft", interference_mm=P.WHEEL_PRESS_MM))
    c += [
        _conn("battery", "tub", "snap", "LiPo battery captured in snug pocket under top panel with velcro"),
        _conn("malenki_rx", "tub", "snap", "Malenki Nano ESC/Rx captured in snug pocket under top panel"),
        _conn("weapon_esc", "tub", "snap", "Weapon ESC captured in snug pocket under top panel"),
        _conn("servo", "tub", "snap", "Hammer-saw servo captured in tight rear chassis pocket"),
        _conn("switch", "tub", "screw", "Power slide switch bolted to top chassis mounting bosses"),
    ]
    return c


def _wire(wid, frm, to, kind, awg, slack, **kw):
    return {"id": wid, "from": frm, "to": to, "via": [list(v) for v in P.WIRE_VIAS[wid]], "awg": awg, "kind": kind,
            "slack_mm": slack, **kw}


def _wires() -> list[dict]:
    note = "Routed inside enclosed chassis tub; arm is a limited-angle overhead servo (-60..10 deg)"
    arm_reason = "Motor phase leads zip-tied along moving overhead hammer-saw arm with pivot service loop"
    return [
        _wire("w_bat_sw", "battery.xt30", "switch.in", "power", P.AWG_POWER, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_sw_mal", "switch.out", "malenki_rx.bat", "power", P.AWG_POWER, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_sw_wesc", "switch.out", "weapon_esc.bat", "power", P.AWG_POWER, P.SLACK_LONG, rotor_ok=note),
        _wire("w_mal_ml", "malenki_rx.m1", "motor_l.terminals", "motor", P.AWG_MOTOR, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_mal_mr", "malenki_rx.m2", "motor_r.terminals", "motor", P.AWG_MOTOR, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_mal_servo", "malenki_rx.wpn", "servo.signal", "signal", P.AWG_SIGNAL, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_mal_wesc", "malenki_rx.wpn", "weapon_esc.rx", "signal", P.AWG_SIGNAL, P.SLACK_SHORT, rotor_ok=note),
        _wire("w_wesc_wm", "weapon_esc.motor", "weapon_motor_stator.phases", "motor", P.AWG_PHASE, P.SLACK_LOOP,
              rotor_ok="Routed along overhead arm spine with service loop at pivot", exposed_reason=arm_reason, external=True),
    ]


def make_spec() -> dict:
    return {
        "name": "Disector",
        "profile": "aws2025",
        "robot_type": "overhead_saw",
        "locomotion": "roller",
        "generator": "src/disector/make_spec.py",
        "proven_design": {"robot": "Disector", "source": "UK antweight that already fights (builder's design); servo top is open on the real robot, no added cover"},
        "parts": _parts_chassis() + _parts_front() + _parts_weapon() + _parts_drive_electronics(),
        "fasteners": F.build_fastener_records(),
        "connections": _connections(),
        "wires": _wires(),
        "electronics": {
            "failsafe": True,
            "weapon_remote_disable": True,
            "radio": "AFHDS 2A (Malenki-Nano built-in)",
            "cells": 2,
        },
        "claims": [
            {"id": "c_mass", "text": "150 g or less", "metric": "mass_total_g", "op": "<=", "value": P.MASS_LIMIT_G},
            {"id": "c_footprint", "text": "Fits 150 mm square", "metric": "footprint_mm", "op": "<=", "value": P.FOOTPRINT_LIMIT_MM},
        ],
    }


def main() -> None:
    out_path = Path(__file__).resolve().parents[2] / "spec.json"
    out_path.write_text(json.dumps(make_spec(), indent=2) + "\n")
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
