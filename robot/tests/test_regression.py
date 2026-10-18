"""Port of crates/robot/tests/regression.rs, plus one test per reviewer flaw in review/*.md that the verifier claims
to catch. Every flaw a reviewer or builder found in a real design stays a test: the verifier must keep catching it.

Flaws the verifier does not judge yet (in Rust or Python) are `xfail(strict=True)`, so they turn into a visible XPASS
the day a check lands, and the matching "not checked" line is asserted where one exists.
"""

import json
from pathlib import Path

import pytest

from robot import checks, spec
from robot.checks import CHECKS_REVISION, Options, verify

FIXTURE = Path(__file__).with_name("fixtures_revron_v1.json")  # byte-identical to crates/robot/tests/fixtures/revron_v1.json


def revron_dict():
    return json.loads(FIXTURE.read_text())


def failed(rep, fid):
    return any(not f.passed and f.id == fid for f in rep.findings)


def found(rep, fid):
    return [f for f in rep.findings if f.id == fid]


def run(d, only=None):
    return verify(spec.Spec(d), Options(fast=True, only=only))


def weapons(d):
    return [p for p in d["parts"] if p.get("weapon")]


@pytest.fixture(scope="module")
def rv1():
    """The Revron v1 build (wedge template with a disc on the motor bell), verified once with every group."""
    return run(revron_dict())


# ---- regression.rs ------------------------------------------------------------------------------------------------

def test_revron_v1_cantilevered_disc_is_blocked(rv1):
    assert failed(rv1, "spinner.bearing"), "disc on one motor bearing must be flagged"
    assert failed(rv1, "spinner.mass_share")
    assert failed(rv1, "spinner.exposed"), "weapon motor sits outside the armour"
    assert not rv1.ok


def test_revron_v1_fastener_flaws_are_caught(rv1):
    assert failed(rv1, "fastener.engagement")
    assert failed(rv1, "mfg.thin_wall")


def test_removing_locking_bar_is_blocked():
    d = revron_dict()
    for p in weapons(d):
        p["weapon"]["locking_bar"] = None
    d["parts"] = [p for p in d["parts"] if p["id"] != "lock_pin"]
    d["connections"] = [c for c in d["connections"] if "lock_pin" not in (c["a"], c["b"])]
    assert failed(run(d, ["legal"]), "legal.locking_bar")


def test_overspeed_is_blocked():
    d = revron_dict()
    for p in weapons(d):
        p["weapon"]["reduction"] = 0.1
    assert failed(run(d, ["power"]), "power.tip_speed")


def test_missing_remote_disable_is_blocked():
    d = revron_dict()
    d["electronics"]["weapon_remote_disable"] = False
    assert failed(run(d, ["legal"]), "legal.weapon_disable")


def test_declared_shaft_support_is_verified_not_trusted():
    d = revron_dict()
    for p in weapons(d):
        p["weapon"]["supported_both_ends"] = True
    assert failed(run(d, ["spinner"]), "spinner.bearing")


def test_report_lists_what_it_did_not_check(rv1):
    assert rv1.checks_revision == CHECKS_REVISION
    assert rv1.not_checked, "a pass must never read as 'everything was checked'"


def _cyl_x(r, length):
    return {"type": "place", "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": r, "height": length}}


def _mk(id, kind, shape, at, mat, proc, **kw):
    return {"id": id, "kind": kind, "shape": shape, "at": list(at), "material": mat, "process": proc, **kw}


def shaft_spec(with_shaft=True, fork_gap=8.0, shafts=None):
    disc = _mk("disc", "weapon", {"type": "subtract", "base": _cyl_x(20, 4), "cut": [_cyl_x(2, 6)]}, (0, 0, 20),
               "steel", "machined", weapon={"kind": "spinner", "spin_axis": [1, 0, 0]})
    parts = [disc,
             _mk("fork_l", "structure", {"type": "box", "size": [5, 30, 50]}, (-fork_gap, 0, 20), "nylon", "fdm"),
             _mk("fork_r", "structure", {"type": "box", "size": [5, 30, 50]}, (fork_gap, 0, 20), "nylon", "fdm")]
    if shafts is None:
        shafts = [("axle", 30.0, (0, 0, 20))] if with_shaft else []
    for sid, length, at in shafts:
        parts.append(_mk(sid, "shaft", _cyl_x(2, length), at, "steel", "machined"))
    return {"name": "shaft", "robot_type": "vertical_spinner", "parts": parts}


def test_shaft_through_both_forks_passes_bearing_check():
    rep = run(shaft_spec(True, 8.0), ["spinner"])
    assert not failed(rep, "spinner.bearing"), [f.message for f in found(rep, "spinner.bearing")]


def test_no_shaft_fails_bearing_check():
    assert failed(run(shaft_spec(False, 8.0), ["spinner"]), "spinner.bearing")


def test_shaft_too_short_to_reach_forks_fails_bearing_check():
    assert failed(run(shaft_spec(True, 18.0), ["spinner"]), "spinner.bearing")


def test_revron_v1_wires_and_floor_reach_are_flagged(rv1):
    assert failed(rv1, "spinner.wire_exposed")
    assert failed(rv1, "spinner.invert")
    assert failed(rv1, "spinner.reach")


# ---- review flaws: revron_iter1.md ----------------------------------------------------------------------------------

def test_rev1_weapon_energy_reported_and_low_flagged(rv1):  # A
    assert found(rv1, "power.weapon_energy")
    assert failed(rv1, "spinner.energy_low")
    assert "J" in found(rv1, "spinner.energy_low")[0].message


def test_rev1_battery_current_vs_peak(rv1):  # flaw 9 / F: 180 mAh pack cannot feed the weapon spin-up
    assert failed(rv1, "power.battery")


def test_rev1_lock_pin_must_be_tethered(rv1):  # flaw 11
    assert failed(rv1, "legal.locking_bar_tether")


def test_rev1_weapon_mass_share_warns_below_20pct(rv1):  # I, iter6 #4
    f = [x for x in found(rv1, "spinner.mass_share") if not x.passed][0]
    assert "20%" in f.message


@pytest.mark.xfail(strict=True, reason="E/flaw 4-5: fork stiffness and bolt pull-out under weapon load are not modelled")
def test_rev1_fork_load_path_is_checked(rv1):
    assert not any("Strength" in s or "load path" in s for s in rv1.not_checked)


def test_rev1_strength_is_listed_as_not_checked(rv1):
    assert any("load path" in s for s in rv1.not_checked)


# ---- review flaws: iter6.md (spinner holes) -------------------------------------------------------------------------

def test_iter6_two_stub_shafts_fail_bearing_check():
    # Each stub sits in one fork and reaches into the disc bore; no single shaft spans both supports.
    stubs = [("stub_l", 10.0, (-6, 0, 20)), ("stub_r", 10.0, (6, 0, 20))]
    assert failed(run(shaft_spec(shafts=stubs), ["spinner"]), "spinner.bearing")


def test_iter6_shaft_beside_weapon_fails_bearing_check():
    # A shaft that spans both forks but runs 10 mm below the disc bore carries nothing.
    assert failed(run(shaft_spec(shafts=[("axle", 30.0, (0, 0, 8))]), ["spinner"]), "spinner.bearing")


def test_iter6_energy_threshold_is_stated(rv1):  # #5
    assert "warns below" in found(rv1, "spinner.energy_low")[0].message


# ---- review flaws: wedge_2wd_flaws.md ------------------------------------------------------------------------------

def _box(id, at, size, kind="structure", material="nylon", **kw):
    return {"id": id, "kind": kind, "shape": {"type": "box", "size": list(size)}, "at": list(at), "material": material,
            "process": "fdm", **kw}


def test_wedge1_fused_across_materials_is_blocked():
    d = {"name": "w", "parts": [_box("chassis", (0, 0, 0), (40, 40, 10)),
                                _box("wedge", (0, 25, 0), (40, 10, 2), kind="wedge", material="petg", fused_with="chassis")]}
    assert failed(run(d, ["interference", "connections"]), "connection.fused_mismatch")


@pytest.mark.xfail(strict=True, reason="wedge#1: `fused_with` between same-material parts that only touch faces is "
                                       "accepted; no shared-volume check (Rust behaves the same)")
def test_wedge1_fused_face_touch_only_is_blocked():
    d = {"name": "w", "parts": [_box("chassis", (0, 0, 0), (40, 40, 10)),
                                _box("wedge", (0, 22.5, 0), (40, 5, 2), kind="wedge", fused_with="chassis")]}
    rep = run(d, ["interference", "connections"])
    assert failed(rep, "connection.fused_mismatch") or failed(rep, "connection.floating")


def test_wedge3_weight_on_wedge_tip(rv1):
    assert failed(rv1, "ground.wedge_load")


def test_wedge4_not_invertible(rv1):
    assert failed(rv1, "spinner.invert")


@pytest.mark.xfail(strict=True, reason="wedge#5 / iter2 I: no >=1 mm running clearance check for wheels in pockets "
                                       "(only spinning weapons get interference.spin_clearance)")
def test_wedge5_wheel_running_clearance():
    wheel = {"id": "wheel", "kind": "wheel", "at": [0, 0, 0], "material": "tpu", "process": "fdm",
             "shape": {"type": "place", "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": 14, "height": 8}},
             "joint": {"kind": "revolute", "axis": [1, 0, 0], "min": 0, "max": 360}, "parent": "chassis"}
    pocket = {"type": "subtract", "base": {"type": "box", "size": [20, 40, 40]},
              "cut": [{"type": "box", "size": [9, 29, 29]}]}
    d = {"name": "w", "parts": [{"id": "chassis", "kind": "structure", "shape": pocket, "at": [0, 0, 0],
                                 "material": "nylon", "process": "fdm"}, wheel]}
    rep = run(d, ["interference"])
    assert any(not f.passed and "clearance" in f.id for f in rep.findings)


def test_wedge6_part_near_but_not_attached_is_floating():  # also iter2 A/B: 1 mm away from everything
    d = {"name": "w", "parts": [_box("chassis", (0, 0, 0), (40, 40, 4)),
                                _box("battery", (0, 0, 8), (20, 20, 10), kind="battery", material=None)]}
    d["parts"][1].pop("material"), d["parts"][1].pop("process")
    d["parts"][1]["mass_g"] = 10
    rep = run(d, ["interference", "connections"])
    assert any(not f.passed and f.id == "connection.floating" and "battery" in f.parts for f in rep.findings)


def test_wedge2_7_strength_and_load_path_listed_as_not_checked(rv1):
    assert any("Strength" in s and "load path" in s for s in rv1.not_checked)


# ---- review flaws: iter2.md ----------------------------------------------------------------------------------------

REASON = "Long enough reasoning sentence that explains the load path, the materials and the assembly order"


def _pair(method, kind_b="other", material_b="petg", **conn):
    return {"name": "c", "parts": [_box("chassis", (0, 0, 0), (40, 40, 4)),
                                   _box("b", (0, 0, 4), (20, 20, 4), kind=kind_b, material=material_b)],
            "connections": [{"a": "chassis", "b": "b", "method": method, "reason": REASON, **conn}]}


def test_iter2_glue_on_impact_part_is_blocked():  # 1 / C
    assert failed(run(_pair("glue", kind_b="wedge"), ["connections"]), "connection.glue_on_impact")


def test_iter2_glue_on_nylon_is_blocked():  # C
    assert failed(run(_pair("glue"), ["connections"]), "connection.glue_low_energy")


def test_iter2_short_reason_is_not_reasoning():  # D
    d = _pair("screw")
    d["connections"][0]["reason"] = "it holds"
    assert failed(run(d, ["connections"]), "connection.reason")


def test_iter2_claim_with_missing_metric_is_blocker():  # 8
    d = {"name": "c", "parts": [_box("chassis", (0, 0, 0), (40, 40, 4))],
         "claims": [{"id": "fit", "text": "fits", "metric": "no_such_metric", "op": "<=", "value": 1}]}
    rep = run(d, ["mass"])
    f = found(rep, "claim.unknown_metric")
    assert f and not f[0].passed and f[0].severity == "blocker" and not rep.ok


def test_iter2_wires_outside_armour_are_flagged(rv1):  # F, revron flaw 7 / D
    assert failed(rv1, "spinner.wire_exposed")


# ---- review flaws: iter3.md ----------------------------------------------------------------------------------------

@pytest.mark.xfail(strict=True, reason="iter3 A: `mechanical_key: true` is a self-declared bool that lifts the glue "
                                       "ban with no geometric evidence (same in Rust)")
def test_iter3_mechanical_key_needs_evidence():
    assert failed(run(_pair("glue", mechanical_key=True), ["connections"]), "connection.glue_low_energy")


@pytest.mark.xfail(strict=True, reason="iter3 B: `retained: tape` links any part of any mass to structure within "
                                       "0.5 mm; no mass or contact-area limit")
def test_iter3_tape_on_heavy_part_is_rejected():
    d = {"name": "t", "parts": [_box("chassis", (0, 0, 0), (60, 60, 4)),
                                _box("lump", (0, 0, 12), (50, 50, 20), kind="other", material="steel", retained="tape")]}
    d["parts"][1]["process"] = "machined"
    assert failed(run(d, ["interference", "connections"]), "connection.floating")


def test_iter3_press_fit_interference_out_of_range():  # C (range only; per-material table not implemented)
    assert failed(run(_pair("press_fit", interference_mm=0.8), ["connections"]), "connection.press_fit_interference")


def test_iter3_fastener_engagement(rv1):  # E
    assert failed(rv1, "fastener.engagement")


def test_iter3_missing_group_is_reported_not_silent(monkeypatch):  # F / G
    monkeypatch.setattr(checks, "GROUPS", checks.GROUPS + [("no_such_group", False)])
    rep = run({"name": "c", "parts": [_box("chassis", (0, 0, 0), (40, 40, 4))]}, ["no_such_group"])
    assert failed(rep, "checks.missing")
    assert any("no_such_group" in s for s in rep.not_checked)


def test_iter3_crashed_group_is_blocker(monkeypatch):  # F: never a silent pass
    from robot.checks import legal
    monkeypatch.setattr(legal, "run", lambda ctx: 1 / 0)
    rep = run({"name": "c", "parts": [_box("chassis", (0, 0, 0), (40, 40, 4))]}, ["legal"])
    assert failed(rep, "checks.crashed") and not rep.ok
    assert any("legal" in s for s in rep.not_checked)


# ---- review flaws: iter4.md ----------------------------------------------------------------------------------------

def test_iter4_wire_tether_listed_as_not_checked(rv1):  # A
    assert any("Wire tether" in s for s in rv1.not_checked)


def test_iter4_trapped_part_and_tool_access_exist():  # assembly sweep + fastener access (detailed in other files)
    from robot.tests.test_assembly_rs import _robot
    rep = verify(_robot(False), Options(fast=True, only=["interference", "assembly"]))
    assert failed(rep, "assembly.blocked")

