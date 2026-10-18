"""External generators and the assembler of the template engine (no verifier run: fast)."""

import pytest

from robot.gen import build
from robot.gen import hypothesis as H
from robot.gen.external import fasteners, front, sh, spinner, wiring

PRESETS = ("wedge", "vspin_drisk", "hspin_bar", "lifter")


@pytest.fixture(scope="module")
def specs():
    return {w: build.build(H.preset(w)) for w in PRESETS}


@pytest.mark.parametrize("w", PRESETS)
def test_build_produces_manufacturable_parts(specs, w):
    d = specs[w]
    ids = [p["id"] for p in d["parts"]]
    assert len(ids) == len(set(ids))
    assert {"chassis_bottom", "chassis_top"} <= set(ids)
    for p in d["parts"]:
        if p.get("catalog"):
            continue
        assert p.get("material") and p.get("process"), p["id"]
        if p["process"] == "fdm":
            assert p.get("print_orientation") or p["id"].startswith("chassis"), p["id"]
    assert d["generator"]["hypothesis"]["weapon"] == w


@pytest.mark.parametrize("w", ("vspin_drisk", "hspin_bar"))
def test_spinners_have_joint_lock_and_bearing(specs, w):
    d = specs[w]
    wp = next(p for p in d["parts"] if p["id"] == "weapon")
    assert wp["joint"]["kind"] == "revolute" and wp["parent"] == "weapon_motor"
    assert wp["process"] == "laser" and wp["material"] == "steel"
    assert d["weapon_lock"]["type"] == "removable_pin"
    assert any(p["kind"] == "bearing" for p in d["parts"])
    assert any(p["kind"] == "shaft" and p["process"] == "cots" for p in d["parts"])


def test_lifter_arm_is_jointed_to_the_servo(specs):
    arm = next(p for p in specs["lifter"]["parts"] if p["id"] == "lifter")
    assert arm["parent"] == "servo" and arm["joint"]["max"] >= 30


def test_every_wire_has_a_channel(specs):
    for w, d in specs.items():
        assert len(d["wires"]) >= 4, w
        assert all(x["from"] and x["to"] for x in d["wires"])


def test_screws_thread_into_inserts_or_motors(specs):
    for d in specs.values():
        ids = {p["id"] for p in d["parts"]}
        for f in d["fasteners"]:
            assert f.get("threads_into") in ids, f


def test_tooth_outline_and_disc():
    pts = spinner.tooth_outline(20.0, teeth=2)
    assert len(pts) == 48 and max(abs(x) for x, _ in pts) <= 20.01
    d = spinner.disc_shape(20, 3, 1.5, [(9, 0, 2)])
    assert d["type"] == "subtract"


def test_wedge_profile_angle():
    prof, ang = front.wedge_profile(36.0, 0.0, 80.0, -14.0)
    assert len(prof) == 4 and 10 < ang < 30


def test_grid_route_avoids_blocks():
    from shapely.geometry import box
    inside = box(-30, -30, 30, 30)
    path = wiring.grid_route((-20, 0), (20, 0), [(-5, 5, -25, 25)], inside)
    assert path is not None
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        for t in (0.0, 0.5, 1.0):
            x, y = x0 + (x1 - x0) * t, y0 + (y1 - y0) * t
            assert not (-5 < x < 5 and -25 < y < 25)


def test_std_screw_lengths():
    assert fasteners.STD_LEN[0] == 4 and 10 in fasteners.STD_LEN


def test_sh_helpers():
    c = sh.cyl_axis(1.0, 0, 10, "x", 0, 0)
    assert c["type"] == "place" and c["rot"] == [0, 90, 0]
