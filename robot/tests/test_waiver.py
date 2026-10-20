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
