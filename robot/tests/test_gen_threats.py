"""Threat model: every rule has a bad and a good case (robot/gen/threats.py)."""

import pytest

from robot.gen import intent, threats
from robot.gen import hypothesis as H


def _spec(parts=(), feats=(), fasteners=(), wires=(), accepted=None):
    return {"parts": list(parts), "fasteners": list(fasteners), "wires": list(wires),
            "generator": {"features": list(feats), "ground_game": {"accepted": accepted or {}}}}


def _feat(target, op="part", **kw):
    it = intent.I("protection", "test", "test", threats=kw.pop("threats", ["vspin_side"]), **kw)
    return {"op": op, "target": target, "intent": it}


def _lt(gap=0.4, door=0.0, bite=None):
    return {d: {"gap_mm": gap, "door_frac": door, "bite": bite or {}, "bite_h_mm": 5.0 if bite else None}
            for d in threats.DIRS8}


# ---- intent: every feature names its threats
def test_intent_requires_known_threats():
    with pytest.raises(ValueError):
        intent.I("load_path", "carries the hit", "1 mm")
    with pytest.raises(ValueError):
        intent.I("load_path", "carries the hit", "1 mm", threats=["laser_beams"])
    with pytest.raises(ValueError):
        intent.I("load_path", "carries the hit", "1 mm", threats=["wall_slam"], shield="prayer")
    assert intent.valid(intent.I("load_path", "carries the hit", "1 mm", threats=["wall_slam", "CF-ST04"], shield="recessed"))


# ---- lift and throw
def test_ground_game_unskirted_direction_fails_unless_accepted():
    bad = threats.ground_game_problems(_spec(), _lt(gap=3.0, door=0.9))
    assert len(bad) == 8 and all("un-skirted" in m for m in bad)
    acc = {d: "the hypothesis leaves it to the wheels" for d in threats.DIRS8}
    assert threats.ground_game_problems(_spec(accepted=acc), _lt(gap=3.0, door=0.9)) == []
    assert threats.ground_game_problems(_spec(), _lt()) == []


def test_ground_game_bite_edge_fails_unless_accepted():
    bad = threats.ground_game_problems(_spec(), _lt(bite={"bolt_x": 4.0}))
    assert len(bad) == 8 and all("bite edge" in m for m in bad)
    acc = {d + ".bite": "spare sheet" for d in threats.DIRS8}
    assert threats.ground_game_problems(_spec(accepted=acc), _lt(bite={"bolt_x": 4.0})) == []


def test_hypothesis_states_its_ground_game():
    g = H.ground_game(H.Hypothesis.parse("wedge"))
    assert g["front"] and g["skirts"] and g["trade"] and g["lip_material"]
    assert "left" not in g["accepted"]  # default skirts cover the sides
    g = H.ground_game(H.Hypothesis.parse("wedge,skirts=none"))
    assert {"left", "right", "rear"} <= set(g["accepted"])


# ---- shielding rule
def test_reached_fragile_part_needs_honest_shield_or_accepted_risk():
    belt = {"id": "belt_l", "kind": "belt"}
    exp = {"belt_l": {"vspin_side": 12.0}}
    assert threats.part_problems(_spec([belt], [_feat("belt_l")]), exp)  # no answer
    assert threats.part_problems(_spec([belt], [_feat("belt_l", shield="inside_hull")]), exp)  # claims hidden, is not
    assert threats.part_problems(_spec([belt], [_feat("belt_l", shield="guarded", threats=["wall_slam"])]), exp)  # unnamed
    assert threats.part_problems(_spec([belt], [_feat("belt_l", shield="guarded")]), exp) == []
    assert threats.part_problems(_spec([belt], [_feat("belt_l", accepted_risk="spare O-ring")]), exp) == []
    assert threats.part_problems(_spec([belt], [_feat("belt_l", shield="inside_hull")]), {}) == []  # hidden: fine


# ---- per-side wire path
def test_each_drive_side_has_its_own_lead():
    m = [{"id": "motor_l", "kind": "motor", "at": [20, 0, 0]}, {"id": "motor_r", "kind": "motor", "at": [-20, 0, 0]}]
    good = [{"id": "a", "from": "esc.m1", "to": "motor_l.t"}, {"id": "b", "from": "esc.m2", "to": "motor_r.t"}]
    assert threats.wire_sides(_spec(m, wires=good)) == []
    assert threats.wire_sides(_spec(m, wires=good[:1]))
    one_side = [dict(m[0]), dict(m[1], at=[10, 0, 0])]
    assert threats.wire_sides(_spec(one_side, wires=good))


# ---- lip / fork rules CF-AS01..04
def test_lip_rules():
    _, miss = threats.lip_rules("acetate", 15.0, 0.5, 1.2, False, 30.0, 0.7, 20.0, 30.0, True, contact_mm2=30.0)
    assert miss == [], miss
    _, miss = threats.lip_rules("tpu", 30.0, 0.0, 0.0, False, 3.0, 4.0, 20.0, 3.0, False)
    assert {"CF-AS01", "CF-AS02", "CF-AS04"} <= set(miss)


# ---- whole robots: impact-face screws, compression, belts inside, all answered
@pytest.fixture(scope="module")
def drisk4():
    from robot.gen import build
    d = build.build(H.Hypothesis.parse(
        "weapon=vspin_drisk,front=wedgelets,drive_layout=4WD,transmission=belt,battery=lipo_2s_180,wheel_dia=20"))
    return d, threats._world(d)


def test_generated_robot_answers_every_threat(drisk4):
    d, w = drisk4
    assert threats.check(d, w=w) == []


def test_belts_enclosed(drisk4):
    d, w = drisk4
    exp = threats.exposure(d, w)
    belts = [p["id"] for p in d["parts"] if p.get("kind") == "belt"]
    assert belts and not any(exp.get(b) for b in belts)


def test_fastener_heads_flagged_on_impact_faces(drisk4):
    d, w = drisk4
    exp = threats.exposure(d, w)
    f = next(f for f in d["fasteners"] if f["id"].startswith("bolt_up") and f["id"] in exp)
    feats = [x for x in d["generator"]["features"] if x.get("target") != f["id"]]
    bad = dict(d, generator=dict(d["generator"], features=feats))
    assert any(f["id"] in m for m in threats.check(bad, exp, w))


def test_uprights_in_compression(drisk4):
    d, w = drisk4
    chassis = [p["id"] for p in d["parts"] if p.get("kind") == "structure" and p["id"].startswith("chassis")]
    assert threats.compression_ok(w, "upright_l", chassis)
    assert not threats.compression_ok(w, "upright_l", [])


def test_fixed_bites_are_no_longer_accepted():
    # wedge ramp ends are closed by cheeks, Ti fork bolts are countersunk: the hypothesis no longer accepts those bites
    assert "front_left.bite" not in H.ground_game(H.Hypothesis.parse("wedge"))["accepted"]
    acc = H.ground_game(H.Hypothesis.parse("vspin_drisk"))["accepted"]
    assert "left.bite" not in acc and "rear_left.bite" not in acc


def test_switch_slides_across_the_robot():
    from robot.gen import build
    h = H.Hypothesis.parse("wedge")
    plan, _ = build._base(h, None)
    sw = next(c for c in build.layout_inputs(plan, h).components if c.id == "power_switch")
    assert sw.rot_choices == (0.0,)
