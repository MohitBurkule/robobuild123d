"""Ground: wheel contact, clearance, wedge gap, stance hull."""

from robot import spec
from robot.checks import Options, verify
from robot.checks.ground import hull, margin

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
WHEEL = {"type": "cylinder", "radius": 10, "height": 6}


def robot(wheel_z=0.0, wedge_z=-9.0, chassis_z=0.0):
    return {"name": "t", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(40, 60, 6), "at": [0, 0, chassis_z]},
        {"id": "wl", "kind": "wheel", "material": "tpu", "shape": WHEEL, "at": [-25, -10, 0], "rot": [0, 90, 0]},
        {"id": "wr", "kind": "wheel", "material": "tpu", "shape": WHEEL, "at": [25, -10, wheel_z], "rot": [0, 90, 0]},
        {"id": "wedge", "kind": "wedge", "material": "pla", "process": "fdm", "shape": BOX(40, 4, 1), "at": [0, 32, wedge_z]},
    ]}


def run(d):
    return verify(spec.Spec(d), Options(only=["mass", "ground"], deep=False, fast=True))


def test_hull_and_margin():
    h = hull([(0, 0), (10, 0), (10, 10), (0, 10), (5, 5)])
    assert len(h) == 4 and abs(margin(h, (5, 5)) - 5) < 1e-9 and margin(h, (20, 5)) < 0
    assert margin(hull([(0, 0), (1, 1)]), (0, 0)) == float("-inf")


def test_good_stance():
    rep = run(robot())
    assert rep.get("ground.wheels_touch").passed
    assert rep.get("ground.wedge_gap").passed, rep.get("ground.wedge_gap").message
    assert rep.get("ground.stance").passed and rep.get("ground.clearance").passed


def test_floating_wheel_and_low_body():
    rep = run(robot(wheel_z=2.0, chassis_z=-8.0))
    assert rep.failed("ground.wheel_floating") and rep.failed("ground.clearance")


def test_wedge_too_high_gives_no_support():
    rep = run(robot(wedge_z=-5.0))
    assert rep.failed("ground.wedge_gap") and rep.failed("ground.stance")
