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


def _armour(**kw):
    d = base(**kw)
    d["parts"][1]["kind"] = "armor"
    return d


def test_armour_snap_only_is_blocker():
    rep = run(_armour(connections=[{"a": "lid", "b": "chassis", "method": "snap", "reason": REASON}]))
    assert rep.failed("connection.cover_fasteners")


def test_armour_one_screw_is_blocker_two_pass():
    s = lambda i, x: {"id": i, "designation": "M2x6", "at": [x, 0, 4], "dir": [0, 0, -1], "through": ["lid", "chassis"]}  # noqa: E731
    assert run(_armour(fasteners=[s("s1", -10)])).failed("connection.cover_fasteners")
    f = run(_armour(fasteners=[s("s1", -10), s("s2", 10)])).get("connection.cover_fasteners")
    assert f and f.passed


def test_cots_retained_screws_needs_fasteners():
    d = base(connections=[{"a": "lid", "b": "chassis", "method": "press_fit", "reason": REASON}])
    d["parts"][1]["retained"] = "screws"
    assert run(d).failed("connection.cover_fasteners")


def test_cover_fasteners_reasoned_deviation():
    s = {"id": "s1", "designation": "M2x6", "at": [-10, 0, 4], "dir": [0, 0, -1], "through": ["lid", "chassis"]}
    why = "the reference clamps this panel between two parts; one screw plus that clamp, as in the STEP"
    # good: one real screw + a written deviation -> warning only, not a blocker
    d = _armour(fasteners=[s])
    d["parts"][1]["cover_fasteners_deviation"] = why
    fs = [f for f in run(d).findings if f.id == "connection.cover_fasteners"]
    assert fs and all(f.severity != "blocker" for f in fs) and why in fs[0].message
    # bad: a deviation does not excuse a panel with no screw at all
    d = _armour(connections=[{"a": "lid", "b": "chassis", "method": "snap", "reason": REASON}])
    d["parts"][1]["cover_fasteners_deviation"] = why
    assert any(f.severity == "blocker" and not f.passed for f in run(d).findings if f.id == "connection.cover_fasteners")
    # bad: an empty reason is not a deviation
    d = _armour(fasteners=[s])
    d["parts"][1]["cover_fasteners_deviation"] = " "
    assert any(f.severity == "blocker" for f in run(d).findings if f.id == "connection.cover_fasteners")


def test_glued_part_needs_a_face_to_bond_to():
    # a declared bond is not a free pass (a switch without catalog holes was declared `adhesive` wherever it sat)
    sw = lambda z: {"id": "sw", "kind": "switch", "material": "pla", "process": "fdm", "shape": BOX(10, 4, 4), "at": [0, 0, z], "retained": "adhesive"}
    on = base(); on["parts"].append(sw(6.0))            # sits on the lid top (z 4)
    assert not run(on).failed("connection.bond_no_face")
    off = base(); off["parts"].append(sw(7.0))          # 1 mm above it: nothing to glue to
    assert run(off).failed("connection.bond_no_face")
