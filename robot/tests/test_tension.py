"""Fork springs and belt drives."""

import math

from robot import spec
from robot.checks import Options, verify
from robot.checks.tension import loop_length

BASE = {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "shape": {"type": "box", "size": [60, 60, 10]}}


def _ids(parts):
    rep = verify(spec.Spec({"name": "t", "parts": [BASE] + parts}), Options(only=["tension"], deep=False, fast=True))
    return {f.id: f for f in rep.findings if f.group == "tension"}, rep


def _fork(tensioner):
    return {"id": "fork", "kind": "fork", "material": "pla", "process": "fdm", "parent": "chassis", "at": [0, 35, 0],
            "shape": {"type": "box", "size": [20, 10, 2]},
            "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 30, 0], "min": -10, "max": 10},
            "tensioner": tensioner}


def test_loop_length_equal_pulleys():
    assert math.isclose(loop_length(50, 5, 5), 100 + 10 * math.pi)


def test_fork_without_tensioner_fails():
    f, _ = _ids([_fork(None)])
    assert f["tension.fork_untensioned"].severity == "blocker"


def test_fork_anchor_in_air_fails_and_good_anchors_pass():
    f, _ = _ids([_fork({"kind": "elastic", "adjustable": True, "anchors": [[0, 35, 1], [0, 0, 50]]})])
    assert "tension.fork_anchors" in f
    f, _ = _ids([_fork({"kind": "elastic", "adjustable": True, "anchors": [[0, 38, 1], [0, 10, 5]]})])
    assert f["tension.ok"].passed and len(f) == 1


def _belt_parts(kind, length, tensioner=None, dist=40):
    pul = lambda i, y: {"id": f"p{i}", "kind": "pulley", "material": "pla", "process": "fdm", "at": [0, y, 20],
                        "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": 5, "height": 4}}
    return [pul(1, 0), pul(2, dist),
            {"id": "belt", "kind": "belt", "material": "rubber", "at": [0, 0, 40], "shape": {"type": "box", "size": [1, 1, 1]},
             "belt": {"pulleys": ["p1", "p2"], "kind": kind, "length_mm": length}, "tensioner": tensioner}]


def test_o_ring_stretch():
    need = 80 + 10 * math.pi
    f, _ = _ids(_belt_parts("o_ring", need / 1.10))
    assert "tension.ok" in f
    f, _ = _ids(_belt_parts("o_ring", need))  # 0 % stretch: slips
    assert f["tension.belt_stretch"].severity == "warning"
    f, _ = _ids(_belt_parts("o_ring", need * 1.05))  # loose
    assert f["tension.belt_stretch"].severity == "blocker"


def test_toothed_belt_needs_adjustable_tensioner():
    need = 80 + 10 * math.pi
    f, _ = _ids(_belt_parts("gt2", need))
    assert "tension.belt_no_tensioner" in f
    f, _ = _ids(_belt_parts("gt2", need, {"kind": "slotted_mount", "adjustable": True}))
    assert "tension.ok" in f


def test_missing_length_is_not_a_pass():
    f, rep = _ids(_belt_parts("o_ring", None))
    assert "tension.belt_length" in f and "tension.ok" not in f
    assert any("belt" in s for s in rep.not_checked)


def test_belt_part_without_definition():
    f, _ = _ids([{"id": "b", "kind": "belt", "material": "rubber", "shape": {"type": "box", "size": [1, 1, 1]}}])
    assert "tension.belt_undefined" in f
