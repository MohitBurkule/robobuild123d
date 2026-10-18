"""Port of crates/robot/tests/assembly.rs: a part sealed in a closed cavity is flagged, the same part in an open pocket is not."""

from robot import spec
from robot.checks import Options, verify


def _box(x, y, z, at=(0, 0, 0)):
    b = {"type": "box", "size": [x, y, z]}
    return {"type": "place", "at": list(at), "shape": b} if any(at) else b


def _robot(open_top):
    cuts = [_box(10, 10, 10)] + ([_box(10, 10, 30, (0, 0, 10))] if open_top else [])
    shell = {"type": "subtract", "base": _box(30, 30, 30), "cut": cuts}
    part = lambda id, kind, shape: {"id": id, "kind": kind, "shape": shape, "at": [0, 0, 0], "material": "nylon", "process": "fdm"}
    return spec.Spec({"name": "assembly test", "profile": "aws2025",
                      "parts": [part("housing", "structure", shell), part("block", "other", _box(9, 9, 9))]})


def test_sealed_part_cannot_be_assembled():
    rep = verify(_robot(False), Options(fast=True, only=["interference", "assembly"]))
    assert any(not f.passed and f.id == "assembly.blocked" and "block" in f.parts for f in rep.findings)


def test_part_in_open_pocket_can_be_assembled():
    rep = verify(_robot(True), Options(fast=True, only=["interference", "assembly"]))
    bad = [f.message for f in rep.findings if not f.passed and f.id == "assembly.blocked"]
    assert not bad, bad
    assert any(f.passed and f.id == "assembly.order" for f in rep.findings)
