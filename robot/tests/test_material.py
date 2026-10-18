"""Material placement: chunky bosses, solid cores, thick walls, load-free bulk, exemptions."""

from robot import spec
from robot.checks import Options, verify

TUB = {"id": "tub", "kind": "structure", "material": "nylon", "process": "fdm",
       "shape": {"type": "subtract", "base": {"type": "box", "size": [40, 60, 30]}, "cut": [{"type": "box", "size": [36, 56, 28]}]}}
INSERT = {"id": "ins", "kind": "insert", "catalog": "heatset_m2", "at": [-18.5, 0, 0], "rot": [0, 90, 0]}
SCREW = {"id": "s", "designation": "M2x10", "at": [-28, 0, 0], "dir": [1, 0, 0], "through": ["pod"], "threads_into": "ins"}
HOLE = {"type": "place", "at": [-24, 0, 0], "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": 1.1, "height": 20}}


def _run(parts, fasteners=()):
    rep = verify(spec.Spec({"name": "t", "parts": parts, "fasteners": list(fasteners)}),
                 Options(only=["material"], deep=False, fast=True))
    return {f.id: f for f in rep.findings if f.group == "material"}, rep


def _pod(base, extra=None):
    p = {"id": "pod", "kind": "structure", "material": "nylon", "process": "fdm",
         "shape": {"type": "subtract", "base": base, "cut": [HOLE]}}
    p.update(extra or {})
    return p


SOLID_POD = {"type": "place", "at": [-24, 0, 0], "shape": {"type": "box", "size": [8, 20, 20]}}
# good pod: a 2 mm side wall plus a round boss (r 3.2) around the screw, nothing else at the screw spot
GOOD_POD = {"type": "union", "items": [
    {"type": "place", "at": [-27, 0, 0], "shape": {"type": "box", "size": [2, 20, 20]}},
    {"type": "place", "at": [-24, 0, 0], "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": 3.2, "height": 8}}]}


def test_solid_pod_at_sideways_screw_is_chunky():
    f, rep = _run([TUB, INSERT, _pod(SOLID_POD)], [SCREW])
    assert f["material.boss_excess"].severity == "warning" and not f["material.boss_excess"].passed
    assert rep.metrics["material.saveable_g.pod"] > 0.2


def test_round_boss_on_thin_wall_passes():
    f, rep = _run([TUB, INSERT, _pod(GOOD_POD)], [SCREW])
    assert "material.boss_excess" not in f and "material.solid_core" not in f
    assert "material.ok" in f


def test_solid_block_flags_core_thick_and_load_free():
    blk = {"id": "blk", "kind": "structure", "material": "nylon", "process": "fdm", "shape": {"type": "box", "size": [40, 40, 20]}}
    f, rep = _run([blk, {"id": "tab", "kind": "structure", "material": "nylon", "process": "fdm", "at": [0, 0, 11],
                         "shape": {"type": "box", "size": [4, 4, 2]}}])
    assert "material.solid_core" in f and "material.thick_wall" in f and "material.load_free" in f
    assert rep.metrics["material.saveable_g"] > 10


def test_shelled_box_passes():
    f, _ = _run([TUB])
    assert not any(not x.passed for x in f.values())
    assert "material.ok" in f


def test_armour_and_solid_reason_are_exempt():
    blk = {"id": "arm", "kind": "armor", "material": "nylon", "process": "fdm", "shape": {"type": "box", "size": [40, 40, 20]}}
    blk2 = dict(blk, id="w", kind="structure", solid_reason="hammer mass")
    f, _ = _run([blk, blk2])
    assert "material.exempt" in f and "material.solid_core" not in f
