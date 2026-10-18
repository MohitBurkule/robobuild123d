"""Join graph: screws, declared joins, explicit `none`, joint pivots, floating parts."""

from robot import spec
from robot.checks import Options, verify

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
REASON = "it carries the side load from hits and is assembled from below with the lid off"


def run(d):
    return verify(spec.Spec(d), Options(only=["connections"], deep=False, fast=True))


def base(**kw):
    d = {"name": "t", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(40, 40, 4)},
        {"id": "lid", "kind": "plate", "material": "pla", "process": "fdm", "shape": BOX(40, 40, 2), "at": [0, 0, 3]},
    ], "fasteners": [], "connections": []}
    d.update(kw)
    return d


def test_floating_part_fails_closed():
    rep = run(base())
    f = rep.get("connection.floating")
    assert f and not f.passed and f.parts == ["lid"] and "Nearest part is `chassis`" in f.message


def test_screw_joins():
    rep = run(base(fasteners=[{"id": "s1", "designation": "M2x6", "at": [0, 0, 4], "through": ["lid", "chassis"]}]))
    assert rep.get("connection.joined").passed


def test_declared_none_and_short_reason():
    rep = run(base(connections=[{"a": "lid", "b": "chassis", "method": "none", "reason": REASON}]))
    assert rep.get("connection.free") and rep.get("connection.joined")
    rep = run(base(connections=[{"a": "lid", "b": "chassis", "method": "glue", "reason": "glued"}]))
    assert rep.failed("connection.reason") and rep.failed("connection.floating")


def test_screw_declared_without_fastener_and_glue_on_wedge():
    rep = run(base(connections=[{"a": "lid", "b": "chassis", "method": "screw", "reason": REASON}]))
    assert rep.failed("connection.screw_missing")
    d = base(connections=[{"a": "lid", "b": "chassis", "method": "glue", "reason": REASON}])
    d["parts"][1]["kind"] = "wedge"
    assert run(d).failed("connection.glue_on_impact")


def test_joint_pivot_off_parts():
    d = base()
    d["parts"][1].update(parent="chassis", joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 0, 50]})
    assert run(d).failed("connection.joint_pivot")
