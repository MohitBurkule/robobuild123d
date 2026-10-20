"""A real, proven design (Revron 2.1 class: UK antweight vertical "drisk" spinner) must be passable:
1. low forks / wedgelets / skirts may lead the disc for the ground game (spinner.reach, shape.weapon_leads, archetype.blade_lead);
2. motor-as-hub: the outrunner bell carries the blades, the motor's own shaft runs in ONE extra coaxial bearing
   (kin.double_bearing, kin.shaft_through_stator, archetype.weapon_drive);
3. disc thickness is the blade stack, not motor + spider + hub (archetype.disc_thickness).
Each relaxation keeps a bad case that still fails."""

import copy

import pytest

from robot import spec
from robot.checks import Options, verify

PLA = {"material": "pla", "process": "fdm"}
CYLX = [0, 90, 0]  # local Z -> world +X (the axle runs left-right)
AXZ = 25.0


def cyl(r, h, hole=None):
    c = {"type": "cylinder", "radius": r, "height": h}
    return c if hole is None else {"type": "subtract", "base": c, "cut": [{"type": "cylinder", "radius": hole, "height": h + 2}]}


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def upright(pid, x):
    return {"id": pid, "kind": "structure", **PLA, "at": [x, 0, AXZ],
            "shape": {"type": "subtract", "base": box(4, 10, 10), "cut": [{"type": "place", "rot": CYLX, "shape": cyl(4.5, 10)}]}}


def drisk():
    """Motor-as-hub drisk: outrunner at -x, aluminium spider bolted to its bell, 3 x 2.5 mm blades, the motor's own shaft
    extended through the stack into one flanged bearing in the +x upright, low forks 10 mm ahead of the disc."""
    blade = lambda pid, x: {"id": pid, "kind": "weapon", "material": "steel", "process": "laser", "parent": "disc",  # noqa: E731
                            "at": [x - 2.75, 0, 0], "shape": cyl(24, 2.5, 2.5), "rot": CYLX}
    return {
        "name": "drisk", "robot_type": "vertical_spinner", "archetype": "vertical_spinner_forks",
        "parts": [
            {"id": "base", "kind": "structure", **PLA, "at": [0, -40, 2], "shape": box(60, 30, 4)},
            upright("upl", 16), upright("upr", -20),
            {"id": "disc", "kind": "weapon", "material": "steel", "process": "laser", "at": [2.75, 0, AXZ], "rot": CYLX,
             "shape": cyl(24, 2.5, 2.5),
             "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [2.75, 0, AXZ], "min": 0, "max": 360},
             "weapon": {"kind": "disc", "motor": "wm", "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": True}},
            {**blade("blade_a", 0.25), "rot": [0, 0, 0], "at": [0, 0, -2.5]},
            {**blade("blade_b", 5.25), "rot": [0, 0, 0], "at": [0, 0, 2.5]},
            {"id": "spider", "kind": "other", "role": "spider", "material": "aluminium", "process": "milled", "parent": "disc",
             "at": [0, 0, -5.25], "shape": cyl(8, 3, 2.5)},
            {"id": "shaft", "kind": "shaft", "material": "steel", "shaft_of": "wm", "parent": "disc", "at": [0, 0, -2.75], "shape": cyl(2.5, 36)},
            {"id": "brg", "kind": "bearing", "material": "steel", "at": [16, 0, AXZ], "rot": CYLX, "shape": cyl(4.5, 4, 2.5)},
            {"id": "wm", "kind": "weapon_motor", "catalog": "bl_1806_2300kv", "at": [-11, 0, AXZ]},
            {"id": "fork_l", "kind": "fork", **PLA, "at": [12, 24, 1.5], "shape": box(4, 20, 3)},
            {"id": "fork_r", "kind": "fork", **PLA, "at": [-12, 24, 1.5], "shape": box(4, 20, 3)},
        ],
        "connections": [
            {"a": "disc", "b": "shaft", "method": "press_fit", "reason": "blade stack keyed on the motor shaft, circlip", "mechanical_key": True},
            {"a": "spider", "b": "wm", "method": "screw", "reason": "aluminium spider bolted to the outrunner bell"},
            {"a": "wm", "b": "shaft", "method": "press_fit", "reason": "the motor's own shaft, extended, circlip", "mechanical_key": True},
            {"a": "brg", "b": "upl", "method": "press_fit", "reason": "flanged bearing pressed in the upright"},
            {"a": "brg", "b": "shaft", "method": "shaft", "reason": "inner race on the motor shaft"},
            {"a": "wm", "b": "upr", "method": "screw", "reason": "stator face bolted to the upright"},
            {"a": "upl", "b": "base", "method": "screw", "reason": "upright"},
            {"a": "upr", "b": "base", "method": "screw", "reason": "upright"},
            {"a": "fork_l", "b": "base", "method": "screw", "reason": "fork"},
            {"a": "fork_r", "b": "base", "method": "screw", "reason": "fork"},
        ],
    }


def part(d, pid):
    return next(p for p in d["parts"] if p["id"] == pid)


def run(d, only=("mass", "power", "kinematics", "spinner", "shape", "archetype")):
    rep = verify(spec.Spec(d), Options(only=list(only), deep=False, fast=True))
    return rep


def failed(rep, fid):
    return [f for f in rep.findings if f.id == fid and not f.passed]


def passed(rep, fid):
    fs = [f for f in rep.findings if f.id == fid]
    return bool(fs) and all(f.passed for f in fs)


@pytest.fixture(scope="module")
def good():
    return run(drisk())


def dump(rep):
    return [(f.id, f.message) for f in rep.findings if not f.passed]


# 1. ground game ------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("fid", ["spinner.reach", "shape.weapon_leads", "archetype.blade_lead", "archetype.wedgelets_flank"])
def test_low_forks_may_lead_the_disc(good, fid):
    assert passed(good, fid), dump(good)


def test_wedgelet_kind_and_declared_ground_game_lead():
    d = drisk()
    part(d, "fork_l")["kind"] = "wedgelet"
    part(d, "fork_r")["kind"] = "other"
    part(d, "fork_r")["ground_game"] = True
    rep = run(d, ("mass", "power", "spinner", "shape", "archetype"))
    for fid in ("spinner.reach", "shape.weapon_leads", "archetype.blade_lead"):
        assert passed(rep, fid), dump(rep)


@pytest.mark.parametrize("mut", ["chassis", "tall_fork", "too_far"])
def test_bad_front_still_fails_everywhere(mut):
    d = drisk()
    for s in ("fork_l", "fork_r"):
        p = part(d, s)
        if mut == "chassis":
            p["kind"] = "structure"  # a low chassis plate ahead of the disc is not a fork
        elif mut == "tall_fork":
            p["shape"], p["at"] = box(4, 20, 20), [p["at"][0], 24, 10]
        else:
            p["at"] = [p["at"][0], 40, 1.5]  # 26 mm ahead, past the 15 mm blade_lead max
    rep = run(d, ("mass", "power", "spinner", "shape", "archetype"))
    for fid in ("spinner.reach", "shape.weapon_leads", "archetype.blade_lead"):
        assert failed(rep, fid), (mut, fid, dump(rep))


# 2. motor-as-hub -----------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("fid", ["kin.double_bearing", "kin.shaft_through_stator", "archetype.weapon_drive"])
def test_motor_as_hub_passes(good, fid):
    assert passed(good, fid), dump(good)


def test_motor_as_hub_inferred_without_declaration():
    d = drisk()
    del part(d, "shaft")["shaft_of"]
    rep = run(d, ("mass", "power", "kinematics"))
    assert passed(rep, "kin.shaft_through_stator") and passed(rep, "kin.double_bearing"), dump(rep)


def test_separate_fat_shaft_through_stator_fails():
    d = drisk()
    del part(d, "shaft")["shaft_of"]
    part(d, "shaft")["shape"] = cyl(3.0, 36)
    rep = run(d, ("mass", "power", "kinematics"))
    assert failed(rep, "kin.shaft_through_stator"), dump(rep)


def test_extra_bearing_off_axis_fails():
    d = drisk()
    part(d, "brg")["at"] = [16, 0, AXZ + 0.2]
    rep = run(d, ("mass", "power", "kinematics"))
    assert failed(rep, "kin.double_bearing"), dump(rep)


def test_two_extra_bearings_fail():
    d = drisk()
    d["parts"].append({**copy.deepcopy(part(d, "brg")), "id": "brg2", "at": [12, 0, AXZ]})
    d["connections"] += [{"a": "brg2", "b": "upl", "method": "press_fit", "reason": "second bearing"},
                         {"a": "brg2", "b": "shaft", "method": "shaft", "reason": "inner race"}]
    rep = run(d, ("mass", "power", "kinematics"))
    assert failed(rep, "kin.double_bearing"), dump(rep)


def test_weapon_drive_direct_coupling_is_not_a_hub():
    d = drisk()
    d["connections"] = [c for c in d["connections"] if {c["a"], c["b"]} != {"spider", "wm"}]
    del part(d, "shaft")["shaft_of"]
    for c in d["connections"]:
        if {c["a"], c["b"]} == {"wm", "shaft"}:
            c["reason"] = "oldham coupling to the motor shaft"
    rep = run(d, ("mass", "power", "archetype"))
    assert failed(rep, "archetype.weapon_drive"), dump(rep)


# 3. blade stack thickness --------------------------------------------------------------------------------------------
def test_disc_thickness_is_the_blade_stack():
    d = drisk()
    d["archetype_params"] = {"disc_thickness_mm": [6.5, 8.5]}
    rep = run(d, ("mass", "power", "archetype"))
    assert passed(rep, "archetype.disc_thickness"), dump(rep)
    assert abs(rep.metrics["archetype.disc_thickness_mm"] - 7.5) < 0.2


def test_disc_thickness_still_judged():
    d = drisk()
    d["archetype_params"] = {"disc_thickness_mm": [12.0, 16.0]}  # a drum-thick target: 7.5 mm of blades is not it
    rep = run(d, ("mass", "power", "archetype"))
    assert failed(rep, "archetype.disc_thickness"), dump(rep)


# 4. a cited reference deviation on the leading part downgrades spinner.reach ----------------------------------------
def _front_base():
    d = drisk()
    part(d, "base")["shape"] = box(60, 90, 4)
    part(d, "base")["at"] = [0, 0, 2]
    return d


def _reach(rep):
    return [f for f in rep.findings if f.id == "spinner.reach" and not f.passed]


def test_a_part_leading_the_weapon_is_a_blocker():
    fs = _reach(run(_front_base(), ("spinner",)))
    assert fs and fs[0].severity == "blocker" and "`base`" in fs[0].message, dump(run(_front_base(), ("spinner",)))


def test_cited_deviation_on_the_leading_part_downgrades_spinner_reach():
    d = _front_base()
    part(d, "base")["deviation"] = "RVRN original architecture: RV23 front leads the spider by the same amount at +-30 deg"
    fs = _reach(run(d, ("spinner",)))
    assert fs and all(f.severity == "warning" for f in fs) and "Deviation:" in fs[0].message


def test_uncited_deviation_does_not_downgrade_spinner_reach():
    d = _front_base()
    part(d, "base")["deviation"] = "it leads and that is fine because we like it"
    assert _reach(run(d, ("spinner",)))[0].severity == "blocker"
