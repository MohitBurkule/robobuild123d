"""Combat ground-game rules (robot/rules/combat_rules.md): a passing and a failing case for every implemented rule id,
on facts (fast, exact) plus end-to-end runs on small robots that check the geometry measurements behind them."""

import re
from pathlib import Path

import numpy as np
import pytest

from robot import spec
from robot.checks import Options, verify
from robot.checks import combat as C


class J:  # joint stand-in
    def __init__(self, lo, hi, kind="revolute"):
        self.min, self.max, self.kind = lo, hi, kind


def sk(**kw):
    d = {"id": "wedge", "kind": "wedge", "front": True, "ymax": 60.0, "gap": 0.5, "material": "steel", "x0": -40.0, "x1": 40.0,
         "hinged": False, "joint": None, "tip_low": 0.5, "heel_low": 0.8, "tip_spread": 0.1, "t1": 1.0, "t3": 1.5,
         "ramp_deg": 20.0, "entry_deg": 18.0, "blunt_h": 0.0, "overhang": 20.0, "width": 80.0, "E": 200000.0, "t_mid": 1.0,
         "deflection": 0.4, "fasteners": 3, "wheel_gap": 5.0}
    d.update(kw)
    return d


def wp(**kw):
    d = {"id": "disc", "axis": np.array([1.0, 0, 0]), "vertical": True, "gap": 2.0, "high": 40.0, "R": 30.0, "front": 60.0,
         "x0": -2.0, "x1": 2.0, "kind": "disc"}
    d.update(kw)
    return d


def base(**kw):
    F = {"family": "wedge", "floor": 0.0, "gap_med.front": 0.5, "cover_1.5.front": 0.95, "cover_3.left": 0.8, "cover_3.right": 0.8,
         "cover_3.rear": 0.7, "gap_max.corner_fl": 2.0, "gap_max.corner_fr": 2.0, "gap_max.corner_rr": 3.0, "gap_max.corner_rl": 3.0,
         "cover_3.all": 0.8, "open_arc_deg": 10.0, "gap_max.all": 4.0, "gap_p20.front": 0.5, "gap_med.left": 1.5, "gap_med.right": 1.5,
         "front_open_mm": 2.0, "front_gap_spread": 0.5, "skirts": [sk()], "front_skirts": [sk()], "skirt_width": 80.0, "body_width": 84.0,
         "skirt_front_y": 60.0, "body_front_y": 60.0, "struct_front_y": 40.0, "forks": [], "fork_open_mm": None, "fork_tip_spread": None,
         "weapon": [], "com": np.zeros(3), "driven_share": 0.9, "cog_h": 12.0, "track": 70.0, "wheelbase": 60.0, "body_height": 25.0,
         "com_lat_off": 1.0, "com_long_margin": 20.0, "tyre_mats": ["silicone", "silicone"], "wheel_dia": 30.0, "wheel_width": 8.0,
         "driven_sides": 2, "n_wheels": 2, "wheelbase_wheels": 0.0, "stall_torque_gcm": [900.0, 900.0], "mass_g": 145.0, "mu": 1.1,
         "motor_rpm": 2000.0, "touching": [], "wheel_low_spread": 0.0, "belly_gap": 2.0, "interior_gap": 3.0, "drag_area_mm2": 0.0,
         "fastener_gap": 3.0, "switch_gap": 5.0, "inv_shortfall": 0.0, "inv_cover_3.front": 0.8, "inv_min_gap": 1.0, "inv_weapon_gap": [],
         "vertical_frac.front": 0.2, "vertical_frac.sides": 0.6, "wheel_edge.front": 0.0, "wheel_edge.left": 0.0, "wheel_edge.right": 0.0,
         "wheel_edge.rear": 0.0, "wheel_edge.all": 0.0, "wheel_front_y": 20.0, "body_max_x": 42.0, "body_min_x": -42.0, "wheel_max_x": 38.0,
         "wheel_min_x": -38.0, "wheel_top": 29.0, "battery_front_clear": 30.0, "battery_side_clear": 10.0}
    F.update(kw)
    return F


V = {"family": "vspin"}
# rule id -> (good overrides, bad overrides)
CASES = {
    "R001": ({}, {"gap_med.front": 2.5}),
    "R002": ({}, {"cover_1.5.front": 0.5}),
    "R003": ({}, {"cover_3.left": 0.2}),
    "R004": ({}, {"cover_3.right": 0.2}),
    "R005": ({}, {"cover_3.rear": 0.1}),
    "R006": ({}, {"gap_max.corner_fl": 9.0}),
    "R007": ({}, {"gap_max.corner_fr": 9.0}),
    "R008": ({}, {"gap_max.corner_rr": 9.0}),
    "R009": ({}, {"gap_max.corner_rl": 9.0}),
    "R010": ({}, {"cover_3.all": 0.3}),
    "R011": ({}, {"open_arc_deg": 90.0}),
    "R012": ({}, {"gap_max.all": 30.0}),
    "R013": ({}, {"gap_p20.front": 1.2}),
    "R014": ({}, {"gap_med.right": 4.0}),
    "R015": ({}, {"front_open_mm": 20.0}),
    "R016": ({}, {"front_gap_spread": 6.0}),
    "R020": ({}, {"front_skirts": [sk(gap=0.0)]}),
    "R021": ({}, {"front_skirts": [sk(gap=2.0)]}),
    "R022": ({}, {"front_skirts": [sk(ramp_deg=50.0)]}),
    "R023": ({}, {"front_skirts": [sk(entry_deg=40.0)]}),
    "R024": ({}, {"front_skirts": [sk(t1=3.0)]}),
    "R025": ({}, {"front_skirts": [sk(t3=5.0)]}),
    "R026": ({}, {"front_skirts": [sk(blunt_h=2.0)]}),
    "R027": ({}, {"front_skirts": [sk(material="pla")]}),
    "R028": ({}, {"skirt_width": 40.0}),
    "R029": ({}, {"skirt_front_y": 50.0}),
    "R030": ({}, {"front_skirts": [sk(heel_low=0.2, tip_low=0.6)]}),
    "R031": ({}, {"front_skirts": [sk(tip_spread=1.5)]}),
    "R032": ({}, {"front_skirts": [sk(deflection=3.0)]}),
    "R033": ({}, {"front_skirts": [sk(t_mid=0.5)]}),
    "R034": ({}, {"front_skirts": [sk(overhang=60.0)]}),
    "R035": ({"skirts": [sk(hinged=True, gap=0.1, joint=J(0, 20))]}, {"skirts": [sk(hinged=True, gap=1.5, joint=J(0, 20))]}),
    "R036": ({"skirts": [sk(hinged=True, joint=J(0, 20))]}, {"skirts": [sk(hinged=True, joint=J(0, 4))]}),
    "R037": ({}, {"skirts": [sk(wheel_gap=0.5)]}),
    "R038": ({}, {"skirts": [sk(fasteners=1)]}),
    "R040": (dict(V, forks=[sk(id="f1"), sk(id="f2")]), dict(V, forks=[sk(id="f1")])),
    "R041": ({"fork_open_mm": 10.0}, {"fork_open_mm": 35.0}),
    "R042": ({"fork_tip_spread": 0.2}, {"fork_tip_spread": 1.5}),
    "R043": ({"forks": [sk(ymax=50.0)]}, {"forks": [sk(ymax=30.0)]}),
    "R050": (dict(V, weapon=[wp()]), dict(V, weapon=[wp(gap=9.0)])),
    "R051": ({"weapon": [wp()]}, {"weapon": [wp(gap=0.0)]}),
    "R052": ({"weapon": [wp(vertical=False, gap=5.0)]}, {"weapon": [wp(vertical=False, gap=25.0)]}),
    "R053": (dict(V, weapon=[wp(gap=3.0)], front_skirts=[]), dict(V, weapon=[wp(gap=8.0)], front_skirts=[])),
    "R054": (dict(V, weapon=[wp(front=55.0)]), dict(V, weapon=[wp(front=75.0)])),
    "R060": ({}, {"driven_share": 0.5}),
    "R061": ({}, {"driven_share": 0.6}),
    "R062": ({}, {"cog_h": 40.0}),
    "R063": ({}, {"wheelbase": 15.0}),
    "R064": ({}, {"cog_h": 20.0}),
    "R065": ({}, {"com_lat_off": 8.0}),
    "R066": ({}, {"com_long_margin": 2.0}),
    "R067": ({}, {"tyre_mats": ["pla", "pla"]}),
    "R068": ({}, {"wheel_dia": 12.0}),
    "R069": ({}, {"wheel_width": 3.0}),
    "R070": ({}, {"driven_sides": 1}),
    "R071": ({"n_wheels": 4, "wheelbase_wheels": 50.0}, {"n_wheels": 4, "wheelbase_wheels": 90.0}),
    "R072": ({}, {"track": 30.0}),
    "R073": ({}, {"stall_torque_gcm": [5.0, 5.0]}),
    "R074": ({}, {"motor_rpm": 300.0}),
    "R080": ({}, {"touching": ["chassis"]}),
    "R081": ({"n_wheels": 4}, {"n_wheels": 4, "wheel_low_spread": 1.0}),
    "R082": ({}, {"belly_gap": 0.3}),
    "R083": ({}, {"interior_gap": 1.0}),
    "R084": ({}, {"drag_area_mm2": 400.0}),
    "R085": ({}, {"fastener_gap": 0.0}),
    "R086": ({}, {"switch_gap": 0.5}),
    "R090": ({}, {"inv_shortfall": 6.0}),
    "R091": ({}, {"inv_cover_3.front": 0.1}),
    "R092": ({}, {"inv_min_gap": 0.0}),
    "R093": ({"inv_weapon_gap": [2.0]}, {"inv_weapon_gap": [20.0]}),
    "R094": ({}, {"body_height": 35.0}),
    "R100": ({}, {"body_height": 60.0}),
    "R101": ({}, {"vertical_frac.front": 0.9}),
    "R102": ({}, {"vertical_frac.sides": 1.0}),
    "R110": ({}, {"wheel_edge.front": 0.1}),
    "R111": ({}, {"wheel_edge.left": 0.5}),
    "R112": ({}, {"wheel_edge.rear": 0.5}),
    "R113": ({}, {"wheel_edge.all": 0.3}),
    "R114": ({}, {"wheel_front_y": 58.0}),
    "R115": ({}, {"wheel_max_x": 45.0}),
    "R116": ({"inv_shortfall": 3.0, "wheel_top": 20.0}, {"inv_shortfall": 3.0, "wheel_top": 40.0}),
    "R120": ({}, {"battery_front_clear": 2.0}),
    "R121": ({}, {"battery_side_clear": 1.0}),
}
RULE = {rid: fn for rid, _, _, _, fn, _ in C.RULES}


def test_every_rule_has_cases_and_ids_are_unique():
    ids = [r[0] for r in C.RULES] + [r[0] for r in C.NOT_CHECKED]
    assert len(ids) == len(set(ids))
    assert set(CASES) == set(RULE)
    assert len(RULE) >= 60 and len(ids) >= 100


def test_knowledge_base_lists_every_rule():
    text = (Path(__file__).resolve().parents[1] / "rules" / "combat_rules.md").read_text()
    kb = set(re.findall(r"^### (R\d{3})", text, re.M))
    assert len(kb) >= 100
    assert set(RULE) <= kb and {r[0] for r in C.NOT_CHECKED} <= kb


@pytest.mark.parametrize("rid", sorted(CASES))
def test_rule_good_and_bad(rid):
    good, bad = CASES[rid]
    sg = RULE[rid](base(**good))
    sb = RULE[rid](base(**bad))
    assert sg[0] is True, (rid, sg)
    assert sb[0] is False, (rid, sb)


def test_missing_data_is_not_a_pass():
    assert C.r060(base(com=None))[0] is None
    assert C.r073(base(mu=None))[0] is None
    assert C.r067(base(tyre_mats=[None, "tpu"]))[0] is None
    assert C.r001(base(**{"gap_med.front": None}))[0] is None


def test_no_front_skirt_fails_a_wedge_but_not_a_spinner():
    assert C.r020(base(front_skirts=[]))[0] is False
    assert C.r020(base(family="hspin", front_skirts=[]))[0] == C.NA


# ---- end to end on small robots ----------------------------------------------------------------------------------------

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
WHEEL = {"type": "cylinder", "radius": 15, "height": 8}


def bot(wedge_z=-14.5, wedge_t=1.0, skirts=True, tyre="tpu"):
    """80 x 80 chassis 20 mm tall; wheels 30 mm on the floor at z = -15; a 1 mm steel wedge sloped 15 deg at the front."""
    parts = [
        {"id": "chassis", "kind": "structure", "material": "nylon", "process": "fdm", "shape": BOX(80, 80, 20), "at": [0, 0, 0]},
        {"id": "wl", "kind": "wheel", "material": tyre, "shape": WHEEL, "at": [36, -10, 0], "rot": [0, 90, 0]},
        {"id": "wr", "kind": "wheel", "material": tyre, "shape": WHEEL, "at": [-36, -10, 0], "rot": [0, 90, 0]},
        {"id": "wedge", "kind": "wedge", "material": "steel", "process": "laser", "shape": BOX(80, 30, wedge_t),
         "at": [0, 52, wedge_z + 15 * 0.2588 + wedge_t / 2 * 0.9659], "rot": [-15, 0, 0]},
    ]
    if skirts:
        for s, x in (("l", 41), ("r", -41)):
            parts.append({"id": f"skirt_{s}", "kind": "wedge", "material": "uhmw", "shape": BOX(2, 80, 14), "at": [x, 0, -7.5]})
        parts.append({"id": "skirt_rear", "kind": "wedge", "material": "uhmw", "shape": BOX(84, 2, 14), "at": [0, -41, -7.5]})
    return {"name": "t", "robot_type": "wedge", "ground_z": -15.0, "parts": parts}


def run(d):
    return verify(spec.Spec(d), Options(only=["mass", "combat"], deep=False, fast=True))


def test_skirted_wedge_has_a_ground_game():
    rep = run(bot())
    for rid in ("R001", "R002", "R003", "R004", "R005", "R010", "R020", "R021", "R080"):
        f = rep.get(f"combat.{rid}")
        assert f is not None and f.passed, (rid, f and f.message)
    assert rep.metrics["combat.cover_3.all"] > 0.6


def test_raised_wedge_and_no_skirts_lose_the_floor():
    rep = run(bot(wedge_z=-11.0, skirts=False))
    for rid in ("R001", "R002", "R003", "R004", "R005", "R021"):
        assert rep.failed(f"combat.{rid}"), rid


def test_ramp_angle_and_tyres_measured():
    rep = run(bot(tyre="pla"))
    assert rep.failed("combat.R067")
    f = rep.get("combat.R022")
    assert f.passed and "15.00 deg" in f.message, f.message


def test_combat_never_blocks_the_reference_wedge():
    tpl = Path(__file__).resolve().parents[1] / "templates" / "wedge_2wd.json"
    rep = verify(spec.load(tpl), Options(only=["mass", "ground", "combat"], deep=False, fast=True))
    assert not [f for f in rep.findings if f.group == "combat" and not f.passed and f.severity == "blocker"]
    assert any("combat.R017" in n for n in rep.not_checked)
