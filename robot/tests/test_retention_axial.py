from robot import spec
from robot.checks import Options, verify


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def part(id, kind, at, **kw):
    return {"id": id, "kind": kind, "shape": box(10, 10, 3), "at": at, "material": "steel", "process": "cnc", **kw}


def run(fasteners):
    d = {"name": "r", "parts": [part("spider", "structure", [0, 0, 0]), part("disc", "weapon", [0, 0, 3], rotates_with="spider")],
         "fasteners": fasteners}
    return verify(spec.Spec(d), Options(fast=True, only=["retention"]))


def failed(rep):
    return any(not f.passed and f.id == "retention.axial" for f in rep.findings)


def test_unclamped_rotating_part_is_flagged():
    assert failed(run([]))


def test_clamped_rotating_part_passes():
    f = {"id": "b", "designation": "M2x6", "at": [0, 0, 6], "dir": [0, 0, -1], "through": ["disc"], "threads_into": "spider", "tool": "hex1.5", "head": "socket"}
    assert not failed(run([f]))
