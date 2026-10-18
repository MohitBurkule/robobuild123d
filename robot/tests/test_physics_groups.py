"""shape, dynamics, strength and printability groups: a sound design passes, each bad design is caught."""

import copy

import pytest

from robot import spec
from robot.checks import Options, verify
from robot.checks import _physics as ph
from robot.checks import printability as pr

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
CYL = lambda r, h: {"type": "cylinder", "radius": r, "height": h}  # noqa: E731
PLACE = lambda s, at, rot=(0, 0, 0): {"type": "place", "shape": s, "at": list(at), "rot": list(rot)}  # noqa: E731
GROUPS = ["mass", "ground", "power", "spinner", "shape", "dynamics", "strength", "printability"]


def wedge_bot():
    return {"name": "w", "robot_type": "wedge", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(40, 60, 12), "at": [0, 0, 2]},
        {"id": "wl", "kind": "wheel", "material": "tpu", "shape": CYL(10, 6), "at": [-25, -10, 0], "rot": [0, 90, 0]},
        {"id": "wr", "kind": "wheel", "material": "tpu", "shape": CYL(10, 6), "at": [25, -10, 0], "rot": [0, 90, 0]},
        {"id": "wedge", "kind": "wedge", "material": "pla", "process": "fdm", "shape": BOX(40, 4, 1), "at": [0, 32, -9]},
        {"id": "bat", "kind": "battery", "material": "pla", "shape": BOX(20, 30, 6), "at": [0, 0, 2]},
    ]}


def spinner_bot(shaft_r=2.0, disc_hole=False, bearing_od=9.0):
    disc = PLACE(CYL(30, 3), (0, 0, 0))
    if disc_hole:
        disc = {"type": "subtract", "base": disc, "cut": [PLACE(CYL(8, 5), (15, 0, 0))]}
    up = lambda x: {"type": "subtract", "base": PLACE(BOX(6, 14, 34), (x, 30, 5)), "cut": [PLACE(CYL(bearing_od / 2, 7), (x, 30, 16), (0, 90, 0))]}  # noqa: E731
    return {"name": "s", "robot_type": "vertical_spinner", "electronics": {"cells": 2}, "parts": [
        {"id": "chassis", "kind": "structure", "material": "nylon", "process": "fdm", "shape": {"type": "union", "items": [
            PLACE(BOX(50, 70, 8), (0, 0, -6)), up(-12), up(12)]}},
        {"id": "wl", "kind": "wheel", "material": "tpu", "shape": CYL(13, 6), "at": [-30, -10, 1], "rot": [0, 90, 0]},
        {"id": "wr", "kind": "wheel", "material": "tpu", "shape": CYL(13, 6), "at": [30, -10, 1], "rot": [0, 90, 0]},
        {"id": "disc", "kind": "weapon", "material": "steel", "process": "waterjet", "shape": disc, "at": [0, 30, 16], "rot": [0, 90, 0],
         "weapon": {"kind": "disc", "motor": "wm", "cells": 2, "spin_axis": [0, 0, 1]}},
        {"id": "shaft", "kind": "shaft", "material": "steel", "process": "bought", "shape": PLACE(CYL(shaft_r, 32), (0, 0, 0), (0, 90, 0)),
         "at": [0, 30, 16]},
        {"id": "b1", "kind": "bearing", "material": "steel", "process": "bought", "shape": PLACE(CYL(bearing_od / 2, 4), (0, 0, 0), (0, 90, 0)),
         "at": [-12, 30, 16]},
        {"id": "b2", "kind": "bearing", "material": "steel", "process": "bought", "shape": PLACE(CYL(bearing_od / 2, 4), (0, 0, 0), (0, 90, 0)),
         "at": [12, 30, 16]},
        {"id": "wm", "kind": "weapon_motor", "catalog": "bl_1806_2300kv", "at": [0, -20, 10]},
    ]}


def run(d):
    return verify(spec.Spec(d), Options(only=GROUPS, deep=False, fast=True))


def test_wedge_bot_passes():
    rep = run(wedge_bot())
    for fid in ("shape.tall", "shape.aspect", "shape.weapon_leads", "shape.armour_coverage", "dynamics.tip_angle", "dynamics.traction"):
        f = rep.get(fid)
        assert f is not None and f.passed, (fid, f and f.message)


def test_part_ahead_of_wedge_fails():
    d = wedge_bot()
    d["parts"][4]["at"] = [0, 30, 2]  # battery pushed out past the wedge
    rep = run(d)
    assert rep.failed("shape.weapon_leads") and "bat" in rep.get("shape.weapon_leads").parts


def test_exposed_battery_and_tall_body_fail():
    d = wedge_bot()
    d["parts"][4]["at"] = [0, 0, 30]  # battery on a mast above the chassis
    d["parts"][4]["shape"] = BOX(20, 30, 40)
    rep = run(d)
    assert rep.failed("shape.armour_coverage") and rep.failed("shape.tall")


def test_tall_narrow_robot_tips_and_cannot_invert():
    d = wedge_bot()
    d["can_run_inverted"] = True
    d["parts"].append({"id": "mast", "kind": "structure", "material": "steel", "process": "bought", "shape": BOX(10, 10, 80), "at": [0, -10, 45]})
    rep = run(d)
    assert rep.failed("dynamics.tip_angle")
    f = rep.get("dynamics.invertible")
    assert not f.passed and f.severity == "blocker"


def test_heavy_wedge_robs_traction():
    d = wedge_bot()
    d["parts"][4].update({"material": "steel", "shape": BOX(36, 14, 8), "at": [0, 22, -2]})
    rep = run(d)
    assert rep.failed("dynamics.traction")


def test_good_spinner():
    rep = run(spinner_bot())
    for fid in ("dynamics.balance", "strength.shaft", "strength.bearing", "shape.weapon_floor_reach", "dynamics.gyro"):
        f = rep.get(fid)
        assert f is not None and f.passed, (fid, f and f.message)
    assert rep.get("strength.upright") is not None


def test_unbalanced_disc_fails():
    rep = run(spinner_bot(disc_hole=True))
    f = rep.get("dynamics.balance")
    assert not f.passed and f.severity == "blocker", f.message


def test_thin_shaft_and_unknown_bearing():
    rep = run(spinner_bot(shaft_r=0.8, bearing_od=9.0))
    f = rep.get("strength.shaft")
    assert not f.passed and f.severity == "blocker", f.message
    rep = run(spinner_bot(bearing_od=10.6))
    assert rep.failed("strength.bearing")


def test_high_disc_does_not_reach_floor():
    d = spinner_bot()
    for p in d["parts"]:
        if p["id"] in ("disc", "shaft", "b1", "b2"):
            p["at"][2] += 20
    rep = run(d)
    assert rep.failed("shape.weapon_floor_reach")


def test_bolt_pullout_shallow_thread():
    d = wedge_bot()
    d["fasteners"] = [{"id": "f1", "designation": "M2x6", "at": [0, 0, 13.4], "dir": [0, 0, -1], "threads_into": "chassis",
                       "through": ["bat"]},
                      {"id": "f2", "designation": "M2x6", "at": [5, 0, 10.0], "dir": [0, 0, -1], "threads_into": "chassis", "through": ["bat"]}]
    d["parts"][4]["at"] = [0, 0, 20]
    rep = run(d)
    # f1 engages only ~0.6 mm of plastic: far below the load share.
    f = next(f for f in rep.findings if f.id == "strength.bolt_pullout" and "f1" in f.parts)
    assert not f.passed


def test_overhang_and_bridge_analysis():
    import trimesh

    cube = trimesh.creation.box((10, 10, 10))
    assert pr.analyse(cube, (0, 0, 1))[0] == pytest.approx(0.0)
    # A table: 40 mm top on two legs; printed upright the top bridges 30 mm.
    legs = [trimesh.creation.box((5, 10, 20)) for _ in range(2)]
    legs[0].apply_translation((-17.5, 0, 0))
    legs[1].apply_translation((17.5, 0, 0))
    top = trimesh.creation.box((40, 10, 3))
    top.apply_translation((0, 0, 11.5))
    t = trimesh.boolean.union(legs + [top]) if trimesh.boolean else None
    if t is None:
        pytest.skip("no boolean engine")
    area, span, _ = pr.analyse(t, (0, 0, 1))
    assert span == pytest.approx(30.0, abs=0.5) and area > 200
    assert pr.analyse(t, (0, 0, -1))[0] < 1.0  # upside down it prints clean


def test_small_hole_and_unprintable_part_flagged():
    d = wedge_bot()
    # A sealed hollow cube: whatever way up, the inner ceiling bridges 26 mm; plus a 1 mm hole through one wall.
    d["parts"].append({"id": "boxy", "kind": "structure", "material": "pla", "process": "fdm", "at": [0, -60, 15], "shape": {
        "type": "subtract", "base": BOX(30, 30, 30), "cut": [BOX(26, 26, 26), PLACE(CYL(0.5, 10), (0, 0, 14), (0, 0, 0))]}})
    rep = run(d)
    assert rep.failed("printability.min_hole")
    assert rep.failed("printability.overhang") or rep.failed("printability.bridge")


def test_bearing_table():
    assert ph.bearing_rating(4.0, 9.0)[0] == "684" and ph.bearing_rating(4.0, 10.6) is None
    M, R, a, b, simple = ph.reactions(100.0, {1.0: (10.0, None), -1.0: (-30.0, None)})
    assert simple and R[1.0] == pytest.approx(75.0) and M == pytest.approx(750.0)
