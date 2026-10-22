"""Electrical rules: every rule id fails on a bad fact set and passes on a good one; plus fact extraction on small specs."""

import pytest

from robot import spec
from robot.checks import Options, verify
from robot.checks.electrical import RULES, awg_amps

ESC = {"max_cells": 3, "cont_a": 5.0, "burst_a": 10.0, "loads_drive": {"m": 1.0}, "loads_weapon": {}}
WESC = {"max_cells": 3, "cont_a": 12.0, "burst_a": 15.0, "loads_drive": {}, "loads_weapon": {"wm": 10.0}}
GOOD = {
    "cells": 2.0, "v_nom": 7.4, "drive_motors": {"m": {"nominal_v": 6.0, "i": 1.0}},
    "weapon_motors": {"wm": {"max_cells": 3, "i": 10.0, "typ": 6.0}}, "escs": {"esc": ESC, "wesc": WESC},
    "wire_currents": {"w1": (22, 8.0)}, "connector": ("xt30", 30.0, 12.0), "switch": ("sw", 15.0, 8.0),
    "receiver": ("rx", True), "escs_unlinked": [], "failsafe": True, "indicator": ("led", True),
    "battery_weapon_gap_mm": 10.0, "battery_shielded": True, "battery_floor": (2.0, True), "battery_removal": (True, "up"),
    "bends": [], "wire_rotating": [], "strain": [], "cells_sources": {"battery": 2.0, "electronics.cells": 2.0},
    "bypass": [], "unpowered": [], "battery_cont": (24.0, 8.0), "runtime_min": 5.0, "no_awg": [], "loose": [],
    "armed": True, "weapon_remote_disable": True,
}
BAD = {
    "drive_motor_voltage": {"v_nom": 14.8},
    "weapon_motor_voltage": {"cells": 4.0},
    "esc_voltage": {"cells": 4.0},
    "esc_drive_current": {"escs": {"esc": dict(ESC, burst_a=0.4, cont_a=0.3)}},
    "esc_weapon_current": {"escs": {"wesc": dict(WESC, burst_a=4.0)}},
    "wire_ampacity": {"wire_currents": {"w1": (30, 8.0)}},
    "connector_rating": {"connector": ("jst_ph", 2.0, 12.0)},
    "switch_rating": {"switch": ("sw", 0.5, 8.0)},
    "receiver_supply": {"receiver": ("rx", False)},
    "failsafe": {"failsafe": False},
    "indicator": {"indicator": ("led", False)},
    "battery_weapon_gap": {"battery_weapon_gap_mm": 1.0},
    "battery_shielded": {"battery_shielded": False},
    "battery_floor": {"battery_floor": (0.0, False)},
    "battery_removable": {"battery_removal": (False, "blocked")},
    "wire_bend_radius": {"bends": [("w1", 1.0, 3.0)]},
    "wire_rotating_clearance": {"wire_rotating": [("w1", "disc", 0.5)]},
    "strain_relief": {"strain": ["`w1` slack 0"]},
    "cells_consistent": {"cells_sources": {"battery": 2.0, "electronics.cells": 3.0}},
    "switch_in_series": {"bypass": ["`esc`"]},
    "power_path": {"unpowered": ["motor `m` has no wire to an ESC"]},
    "battery_c_rating": {"battery_cont": (5.0, 8.0)},
    "runtime": {"runtime_min": 1.0},
    "wire_gauge_declared": {"no_awg": ["w1"]},
    "parts_retained": {"loose": ["battery"]},
    "weapon_disable": {"weapon_remote_disable": False},
}
# Rules whose missing data is unknown (fail closed); others have a defined meaning when the fact is absent.
NO_UNKNOWN = {"receiver_supply", "failsafe", "indicator", "weapon_disable", "weapon_motor_voltage"}


def _passes(p):
    return not isinstance(p, str) and p is not None and bool(p)


def test_every_rule_has_a_bad_case():
    assert set(BAD) == set(RULES)


@pytest.mark.parametrize("rid", sorted(RULES))
def test_rule_good_passes_bad_fails(rid):
    fn = RULES[rid][3]
    p, msg = fn(GOOD)
    assert _passes(p), (rid, msg)
    p, msg = fn(dict(GOOD, **BAD[rid]))
    assert p is not None and not _passes(p), (rid, msg)
    if rid not in NO_UNKNOWN:
        key = next(iter(BAD[rid]))
        p, _ = fn({k: v for k, v in GOOD.items() if k != key})
        assert p is None, rid


def test_awg_table():
    assert awg_amps(22) == 12.0 and awg_amps(32) < awg_amps(30)


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def _spec(**over):
    parts = [
        {"id": "base", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(80, 80, 3), "at": [0, 0, 1.5]},
        {"id": "top", "kind": "armor", "material": "pc", "shape": box(80, 80, 1), "at": [0, 0, 30]},
        {"id": "bat", "kind": "battery", "catalog": "lipo_2s_180", "at": [0, -20, 10], "retained": "velcro"},
        {"id": "esc", "kind": "esc", "catalog": "esc_dual_brushed", "at": [0, 10, 6], "retained": "velcro",
         "ratings": {"max_cells": 2}},
        {"id": "rx", "kind": "receiver", "catalog": "rx_fs_ia6_decased", "at": [20, 10, 6], "retained": "velcro"},
        {"id": "ml", "kind": "motor", "catalog": "n20_1000rpm_6v", "at": [-25, 25, 8]},
        {"id": "sw", "kind": "switch", "catalog": "switch_slide_12x4", "at": [30, -30, 6], "ratings": {"current_a": 5}},
    ]
    wires = [
        {"id": "w1", "from": "bat.xt30", "to": "sw.in", "awg": 24, "kind": "power", "slack_mm": 5},
        {"id": "w2", "from": "sw.out", "to": "esc.bat", "awg": 24, "kind": "power", "slack_mm": 5},
        {"id": "w3", "from": "esc.m1", "to": "ml.terminals", "awg": 28, "kind": "motor", "slack_mm": 5},
        {"id": "w4", "from": "rx.esc", "to": "esc.rx", "awg": 30, "kind": "signal", "slack_mm": 5},
    ]
    d = {"name": "e", "robot_type": "wedge", "parts": parts, "wires": wires, "electronics": {"failsafe": True, "cells": 2}}
    d.update(over)
    rep = verify(spec.Spec(d), Options(only=["electrical"], deep=False, fast=True))
    return {f.id: f for f in rep.findings if f.group in ("electrical", "checks")}, rep


def test_small_robot_good():
    f, rep = _spec()
    assert "checks.crashed" not in f
    for rid in ("esc_voltage", "esc_drive_current", "wire_ampacity", "connector_rating", "switch_rating", "receiver_supply",
                "failsafe", "battery_floor", "battery_removable", "cells_consistent", "switch_in_series", "power_path",
                "battery_c_rating", "runtime", "wire_gauge_declared", "parts_retained", "strain_relief"):
        assert f[f"electrical.{rid}"].passed, (rid, f[f"electrical.{rid}"].message)
    # routes only exist in deep mode: fail closed
    assert not f["electrical.wire_bend_radius"].passed and any("wire_bend_radius" in x for x in rep.not_checked)


def test_small_robot_bad_wiring():
    wires = [{"id": "w1", "from": "bat.xt30", "to": "esc.bat", "kind": "power"},  # bypasses switch, no awg, no slack
             {"id": "w3", "from": "esc.m1", "to": "ml.terminals", "awg": 28, "kind": "motor", "slack_mm": 5}]
    f, _ = _spec(wires=wires, electronics={"failsafe": True, "cells": 3})
    assert f["electrical.switch_in_series"].severity == "blocker" and not f["electrical.switch_in_series"].passed
    assert not f["electrical.wire_gauge_declared"].passed
    assert not f["electrical.strain_relief"].passed
    assert not f["electrical.cells_consistent"].passed
    assert not f["electrical.failsafe"].passed  # ESC not driven from the receiver
    assert not f["electrical.receiver_supply"].passed


def test_weapon_slab_centred_on_weapon(monkeypatch):
    """The weapon's swept slab is centred on the weapon, not mirrored about a far-off axis origin (Revron: a phase lead
    17 mm from the spider was reported 0.4 mm from it)."""
    import types

    import numpy as np
    import trimesh

    from robot.checks import electrical as el

    disc = trimesh.creation.cylinder(radius=10.0, height=3.0, transform=trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    disc.apply_translation([-6.7, 0, 0])
    b = types.SimpleNamespace(part_idx=0, kind="weapon", mesh=disc)
    ctx = types.SimpleNamespace(world=types.SimpleNamespace(bodies=[b]), r=None)
    monkeypatch.setattr(el, "spin_axis", lambda w, r, i: (np.array([0.0, 0, 0]), np.array([1.0, 0, 0])))
    monkeypatch.setattr(el, "rim_radius", lambda b, o, a: 10.0)
    _, o, a, R, half = el._weapon(ctx)
    assert abs(o[0] + 6.7) < 1e-6 and abs(half - 1.5) < 1e-6
