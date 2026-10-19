"""Design intent: every generated feature records why it exists, and sizes follow from the intent."""

import copy
import math

import pytest

from robot.gen import build, gate, intent
from robot.gen import hypothesis as H

HYPS = ["wedge", "none_pusher", "weapon=none_pusher,front=plow", "lifter", "hspin_bar", "vspin_drisk",
        "weapon=vspin_drisk,front=wedgelets,drive_layout=4WD,transmission=belt,battery=lipo_2s_180,wheel_dia=20"]


@pytest.fixture(scope="module")
def specs():
    return {t: build.build(H.Hypothesis.parse(t)) for t in HYPS}


def test_intent_record_rejects_unknown_purpose_and_empty_reason():
    with pytest.raises(ValueError):
        intent.I("looks_nice", "because", "1 mm")
    with pytest.raises(ValueError):
        intent.I("load_path", "", "1 mm")
    with pytest.raises(ValueError):
        intent.I("load_path", "carries the hit", " ")
    assert intent.valid(intent.I("mass", "carries nothing", "verifier saveable_g"))


@pytest.mark.parametrize("t", HYPS)
def test_every_generated_feature_has_an_intent(specs, t):
    assert intent.check(specs[t]) == []


def test_every_purpose_is_from_the_list_and_features_cover_parts(specs):
    d = specs["vspin_drisk"]
    feats = d["generator"]["features"]
    assert {f["intent"]["purpose"] for f in feats} <= set(intent.PURPOSES)
    targets = {f["target"] for f in feats if f["op"] == "part"}
    assert {p["id"] for p in d["parts"]} <= targets
    assert all(f["src"].endswith(tuple(f":{i}" for i in range(1, 10000))) for f in feats[:20])


def test_check_flags_a_feature_without_intent(specs):
    d = copy.deepcopy(specs["wedge"])
    d["parts"].append({"id": "mystery_block", "kind": "structure", "at": [0, 0, 0], "rot": [0, 0, 0]})
    d["generator"]["features"][0]["intent"] = None
    out = intent.check(d)
    assert any("mystery_block" in m for m in out)
    assert any("no intent" in m and m.startswith(d["generator"]["features"][0]["op"]) for m in out)


def test_check_flags_spec_without_feature_record():
    assert intent.check({"parts": []}) != []


def test_gate_refuses_a_spec_with_a_feature_without_intent(monkeypatch):
    real = build.build

    def no_intent(*a, **k):
        d = real(*a, **k)
        d["generator"]["features"][3]["intent"] = None
        return d

    monkeypatch.setattr(build, "build", no_intent)
    with pytest.raises(gate.Rejected) as e:
        gate.gate(H.preset("wedge"), fast=True, max_layouts=1, seeds=(0,))
    assert "intent" in str(e.value.attempts[-1]["blockers"][0])


def test_sizing_follows_from_intent():
    # light load: the print minimum governs; heavy load: bending governs
    assert intent.wall_for(10.0, 25.0) == intent.MIN_WALL_FDM
    assert intent.wall_for(200.0, 25.0) > intent.MIN_WALL_FDM
    assert intent.wall_for(200.0, 25.0, "tpu") > intent.wall_for(200.0, 25.0, "nylon")
    assert intent.boss_r_for(2.0) == pytest.approx(3.2 / 2 + 1.2)
    assert intent.screw_dir([0, 0, -3]) == [0.0, 0.0, -1.0]
    assert intent.pocket_gap("press_fit") < intent.pocket_gap("velcro")
    assert intent.chamfer_for("impact") > intent.chamfer_for("print")
    ring = intent.belt_ring_for(45.0, 5.1, 5.1, 0.08)
    assert ring * math.pi * 1.08 == pytest.approx(90.0 + 2 * math.pi * 5.1)


def test_wall_and_chamfer_come_from_the_intent_helpers(specs):
    from robot.gen.external import shell
    d = specs["wedge"]
    wall = next(f for f in d["generator"]["features"] if f["op"] == "wall")
    assert "side hit" in wall["intent"]["load_or_constraint"]
    assert shell.EDGE_CHAMFER == intent.chamfer_for("print")


def test_4wd_belt_drive_is_built_with_belts_and_front_wheels(specs):
    d = specs[HYPS[-1]]
    ids = {p["id"] for p in d["parts"]}
    assert {"belt_l", "belt_r", "wheel_fl", "wheel_fr", "pulley_l", "pulley_fl", "axle_fl", "axle_fr"} <= ids
    belt = next(p for p in d["parts"] if p["id"] == "belt_l")
    assert belt["belt"]["pulleys"] == ["pulley_l", "pulley_fl"]
    forks = [p for p in d["parts"] if p["kind"] == "fork"]
    assert len(forks) == 2 and all(p["material"] == "tpu" for p in forks)  # front=wedgelets honoured on the drisk
    assert any(f.get("threads_into") == "axle_fl" for f in d["fasteners"])  # wedgelet hangs on the front axle


def test_belt_is_a_stock_o_ring(specs):
    from robot.checks.bom import STOCK_ORINGS
    belt = next(p for p in specs[HYPS[-1]]["parts"] if p["id"] == "belt_l")["belt"]
    st = belt["stock"]
    assert st["id_mm"] in STOCK_ORINGS[st["cs_mm"]]
    assert belt["length_mm"] == pytest.approx(math.pi * st["id_mm"], rel=0.01)


def test_spider_pair_is_two_discs_on_a_spider_bolted_up():
    d = build.build(H.Hypothesis.parse("weapon=vspin_drisk,disc_stack=spider_pair,battery=lipo_2s_180"))
    assert intent.check(d) == []
    ids = {p["id"]: p for p in d["parts"]}
    assert {"weapon", "disc_b", "spider"} <= set(ids)
    assert ids["disc_b"]["parent"] == "weapon" and ids["spider"]["rotates_with"] == "weapon"
    stack = [f for f in d["fasteners"] if f.get("threads_into") == "disc_b"]
    assert len(stack) == 2 and all("spider" in f["through"] for f in stack)


def test_tub_chassis_mounts_uprights_on_standoffs():
    d = build.build(H.Hypothesis.parse(HYPS[-1] + ",chassis=tub"))
    assert intent.check(d) == []
    ids = {p["id"] for p in d["parts"]}
    assert {"tub", "lid", "base_panel", "so_r0", "so_l1"} <= ids and "chassis_top" not in ids
    assert any(f.get("threads_into") == "so_l0" and "upright_l" in f["through"] for f in d["fasteners"])
