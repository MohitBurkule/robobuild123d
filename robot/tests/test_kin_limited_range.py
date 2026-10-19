"""Limited-range revolute joints (lifters, flippers) are swept over their range only and are not spin-balanced
(VERIFIER_ISSUES #1 on claude/template-engine-ctcfhz)."""

from test_kinematics import PLA, part, run, wheels  # noqa: F401


def lifter(lo=0, hi=35):
    d = wheels()
    d["parts"].append({"id": "arm", "kind": "structure", **PLA, "at": [0, -13, 12], "shape": {"type": "box", "size": [6, 30, 3]},
                       "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, -28, 12], "min": lo, "max": hi}})
    return d


def fails(rep, cid):
    return [f.message for f in rep.findings if f.id == cid and not f.passed]


def test_lifter_range_clear_passes():
    rep, _ = run(lifter())
    assert not fails(rep, "kin.sweep_static")
    assert not fails(rep, "kin.balance_static")
    assert any(f.id == "kin.sweep_static" for f in rep.findings)


def test_lifter_range_into_base_fails():
    rep, _ = run(lifter(-35, 0))
    assert fails(rep, "kin.sweep_static")


def test_full_turn_arm_still_swept_and_balanced():
    rep, _ = run(lifter(0, 360))
    assert fails(rep, "kin.sweep_static")
    assert fails(rep, "kin.balance_static")
