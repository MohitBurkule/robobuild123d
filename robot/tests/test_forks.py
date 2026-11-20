"""Shared parametric fork set (robot/modules/forks.py) via kit.json `forks: {style, ...}` and kitparts `fork_set`."""
import math

import pytest

from robot import kit, kitparts, shapes, xform
from robot.modules import forks


def _ids(parts):
    return {p["id"]: p for p in parts}


def _solid_ok(parts):
    for p in parts:
        if p.get("shape"):
            assert shapes.to_solid(p["shape"], ".").volume > 0.5, p["id"]


def test_tine_spacing_pitch_spread_and_symmetry():
    assert forks.tine_xs(3, pitch=10) == [-10.0, 0.0, 10.0]
    assert forks.tine_xs(2, spread=40) == [-20.0, 20.0]
    assert forks.tine_xs(1, spread=40, x=5) == [5.0]
    xs = forks.tine_xs(4, spread=30, x=12)
    assert abs(sum(xs) / 4 - 12) < 1e-9 and abs((xs[1] - xs[0]) - 10) < 1e-9


def test_plate_and_sheet_rigid():
    plate = forks.fork_parts(n=3, pitch=12, length=30, width=6, taper=0.5, thick=1.5, holes=2)
    assert [p["id"] for p in plate] == ["forks_0", "forks_1", "forks_2"]
    assert all(p["kind"] == "fork" and p["process"] == "laser" and "joint" not in p for p in plate)
    _solid_ok(plate)
    bb = shapes.to_solid(plate[1]["shape"], ".").bounding_box()
    assert abs(bb.size.Y - 38) < 0.3 and abs(bb.size.Z - 1.5) < 1e-6  # tab 8 + length 30, one sheet thick
    sheet = forks.fork_parts(style="sheet", n=4, spread=45, length=25, width=8)
    assert len(sheet) == 1 and sheet[0]["kind"] == "fork"
    _solid_ok(sheet)
    with pytest.raises(ValueError):
        forks.fork_parts(style="spoon")
    with pytest.raises(ValueError):
        forks.fork_parts(lift=True)


def test_taper_narrows_tip():
    s = forks.fork_parts(n=1, length=20, width=8, taper=0.25, tab=0.0, holes=0)
    sol = shapes.to_solid(s[0]["shape"], ".")
    tip = [v for v in sol.vertices() if v.Y > 19.9]
    assert abs(max(v.X for v in tip) - min(v.X for v in tip) - 2.0) < 1e-6


def test_hinge_is_limited_range_not_full_turn():
    ps = _ids(forks.fork_parts(style="plate", n=2, length=45, hinge={"range": [-5, 40], "pin_d": 2}))
    root = ps["forks"]
    j = root["joint"]
    assert j["kind"] == "revolute" and j["axis"] == [1.0, 0.0, 0.0] and (j["min"], j["max"]) == (-5.0, 40.0)
    assert abs(j["max"] - j["min"]) < 360  # kinematics: SectorSweep, not the full-circle sweep
    # moving parts are kind `other` with no `weapon`, so a spinner robot does not treat them as a spinning weapon
    for pid in ("forks", "forks_0", "forks_1"):
        assert ps[pid]["kind"] == "other" and "weapon" not in ps[pid] and ps[pid]["rotates_with"] == "forks"
    assert ps["forks_0"]["parent"] == "forks" and ps["forks_pin"]["kind"] == "pin"
    assert ps["forks_mount"]["kind"] == "plate" and "joint" not in ps["forks_mount"]
    _solid_ok(ps.values())
    sheet = _ids(forks.fork_parts(style="sheet", n=3, hinge=True))
    assert sheet["forks_sheet"]["parent"] == "forks" and sheet["forks_sheet"]["process"] == "laser"


def test_lift_servo_coaxial_with_hinge():
    for side in (1, -1):
        ps = _ids(forks.fork_parts(n=2, hinge=True, lift={"servo": "servo_cs07"}, x=0, _side=side))
        sv, root = ps["forks_servo"], ps["forks"]
        assert sv["catalog"] == "servo_cs07" and root["actuated_by"] == "forks_servo"
        M = xform.pose(sv["at"], sv["rot"])
        o = xform.apply(M, [forks.SERVO_OUT[0], forks.SERVO_OUT[1], 0.0])
        d = xform.apply_dir(M, [0, 0, 1])
        assert abs(o[1]) < 1e-6 and abs(o[2]) < 1e-6  # output on the hinge axis
        assert abs(abs(d[0]) - 1) < 1e-9 and d[0] * side < 0  # pointing back at the forks
        assert ps["forks_horn"]["parent"] == "forks" and side * ps["forks_horn"]["shape"]["base"]["items"][0]["at"][0] > 0
        _solid_ok(ps.values())


def test_mirror_pair():
    ps = _ids(forks.fork_parts(n=2, pitch=8, x=25, mirror=True, hinge=True, lift=True))
    assert {"forks_l", "forks_r", "forks_l_servo", "forks_r_servo", "forks_l_0", "forks_r_1"} <= set(ps)
    assert ps["forks_l"]["joint"]["pivot"][0] == 25.0 and ps["forks_r"]["joint"]["pivot"][0] == -25.0
    assert ps["forks_l_servo"]["at"][0] > 25 and ps["forks_r_servo"]["at"][0] < -25  # servos outboard
    assert abs(ps["forks_l_servo"]["at"][0] + ps["forks_r_servo"]["at"][0]) < 1e-6


def test_kit_backward_compatible_and_style():
    legacy = kit.build({"forks": {"n": 2}})
    f = _ids(legacy["parts"])
    assert f["fork_0"]["kind"] == "wedge" and "forks" not in f  # no style: the legacy tines, unchanged
    s = kit.build({"weapon": {"kind": "disc", "radius": 30}, "wheels": {"radius": 14},
                   "forks": {"style": "plate", "n": 2, "length": 40, "pitch": 10, "x": 27, "mirror": True,
                             "hinged": True, "range": [-5, 40], "lift": True}})
    ps = _ids(s["parts"])
    assert ps["forks_l"]["joint"]["min"] == -5.0 and ps["forks_r"]["joint"]["max"] == 40.0
    assert ps["forks_l"]["joint"]["pivot"][2] >= -14 + 6.5  # lift raises the hinge so the servo clears the floor
    _solid_ok(s["parts"])
    rigid = kit.build({"wheels": {"radius": 14}, "forks": {"style": "sheet", "n": 4, "length": 30}})
    p = _ids(rigid["parts"])["forks"]
    sol = shapes.place(shapes.to_solid(p["shape"], "."), xform.pose(p["at"], p["rot"]))
    assert abs(sol.bounding_box().min.Z - (-14 + 0.3)) < 0.05  # auto tilt: tips 0.3 mm off the floor


def test_kitparts_fork_set_and_module():
    s = kitparts.expand([{"part": "fork_set", "id": "fk", "at": [20, 50, -10], "mirror": "x", "hinge": True,
                          "n": 2, "pitch": 8}])
    ps = _ids(s)
    assert ps["fk_l"]["joint"]["pivot"] == [20.0, 50.0, -10.0] and ps["fk_r"]["joint"]["pivot"] == [-20.0, 50.0, -10.0]
    assert ps["fk_l_0"]["at"] == ps["fk_r_0"]["at"] or ps["fk_l_0"]["parent"] == "fk_l"  # children stay parent-relative
    assert "fork_set" in kitparts.describe()
    from robot.modules import REGISTRY, make
    assert "forks" in REGISTRY
    res = make("forks", name="fs", params={"n": 2, "hinge": True}).build()
    assert {"fs", "fs_0", "fs_1", "fs_mount", "fs_pin"} <= set(res.parts)
    assert math.isfinite(res.parts["fs_0"].volume)
