"""Per-fastener waivers (robot/checks/waiver.py)."""

from robot.checks import waiver
from robot.finding import BLOCKER, WARNING, fail
from robot.spec import Spec

GOOD = "RV14 switch screw is a self-tapper per RVRN reference, no hole record"


def _run(waive, fid="fs1", group="fastener", check="fastener.hole_record.length"):
    spec = Spec({"fasteners": [{"id": "fs1", "waive": waive}, {"id": "fs2"}]})
    f = fail(check, group, BLOCKER, "t", "m").on(fid)
    return f, waiver.apply(spec, [f])


def test_valid_waiver_downgrades():
    f, used = _run({"fastener.hole_record": GOOD})
    assert f.severity == WARNING and f"waived: {GOOD}" in f.message
    assert used == [{"fastener": "fs1", "check": f.id, "reason": GOOD, "valid": True}]


def test_no_reason_blocks():
    f, used = _run({"fastener.hole_record": ""})
    assert f.severity == BLOCKER and waiver.INVALID in f.message and not used[0]["valid"]


def test_no_citation_blocks():
    f, _ = _run({"fastener.hole_record": "the screw is fine, trust me, really long reason"})
    assert f.severity == BLOCKER and waiver.INVALID in f.message


def test_other_fastener_unaffected():
    f, used = _run({"fastener.hole_record": GOOD}, fid="fs2")
    assert f.severity == BLOCKER and not used


def test_forbidden_group_unaffected():
    for g in sorted(waiver.FORBIDDEN):
        f, used = _run({g: GOOD}, group=g, check=f"{g}.x")
        assert f.severity == BLOCKER and not used


def test_part_waiver_downgrades():
    reason = "ELVRN3.0 Alt STEP: the TPU fork tips are preloaded 2.25 mm onto the floor"
    spec = Spec({"parts": [{"id": "side_l", "kind": "armor", "waive": {"contain.wheel_ground": reason}}, {"id": "wheel_rl", "kind": "wheel"}]})
    f = fail("contain.wheel_ground", "contain", BLOCKER, "t", "m").on("wheel_rl", "side_l")
    used = waiver.apply(spec, [f])
    assert f.severity == WARNING and used == [{"part": "side_l", "check": f.id, "reason": reason, "valid": True}]


def test_part_waiver_needs_the_part():
    spec = Spec({"parts": [{"id": "side_l", "kind": "armor", "waive": {"contain.wheel_ground": GOOD}}]})
    f = fail("contain.wheel_ground", "contain", BLOCKER, "t", "m").on("wheel_rl")
    assert not waiver.apply(spec, [f]) and f.severity == BLOCKER
