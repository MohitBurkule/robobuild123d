"""Design patch language (robot/design_io/patch.py): apply/diff round trip and error shapes."""

import pytest

from robot.design_io import patch


def test_set_nudge_unset_roundtrip():
    a = {"weapon": {"type": "hspin_bar"}, "body": {"zt": 12.0}, "skirts": "on"}
    b = {"weapon": {"type": "vspin_drisk"}, "body": {"zt": 13.5}}
    p = patch.diff(a, b)
    out, errs = patch.apply(a, p)
    assert out == b and errs == []
    assert {"op": "set", "path": "weapon.type", "value": "vspin_drisk"} in p
    assert {"op": "nudge", "path": "body.zt", "delta": 1.5} in p
    assert {"op": "unset", "path": "skirts"} in p


def test_apply_does_not_mutate_input():
    a = {"body": {"zt": 12.0}}
    patch.apply(a, [{"op": "nudge", "path": "body.zt", "delta": 2}])
    assert a == {"body": {"zt": 12.0}}


def test_apply_set_creates_nested_path():
    out, errs = patch.apply({}, [{"op": "set", "path": "drive.motor", "value": "n10"}])
    assert out == {"drive": {"motor": "n10"}} and errs == []


def test_apply_errors_are_actionable():
    a = {"weapon": {"type": "hspin_bar"}}
    out, errs = patch.apply(a, [{"op": "unset", "path": "weapon.typee"},
                                {"op": "nudge", "path": "weapon.type", "delta": 1},
                                {"op": "nudge", "path": "body.zt", "delta": "x"},
                                {"op": "set", "path": "weapon.type"},
                                {"op": "explode", "path": "x"},
                                {"op": "set", "path": "", "value": 1}])
    codes = {e["code"] for e in errs}
    assert "unknown_path" in codes and "bad_type" in codes and "bad_op" in codes
    unknown = next(e for e in errs if e["code"] == "unknown_path")
    assert unknown["allowed"] == ["weapon", "weapon.type"]
    assert out == a


def test_diff_identical_is_empty():
    a = {"weapon": {"type": "wedge"}}
    assert patch.diff(a, dict(a)) == []


def test_numbers_nudge_only_when_exact():
    p = patch.diff({"zt": 10}, {"zt": 12.5})
    assert p == [{"op": "nudge", "path": "zt", "delta": 2.5}]
    p = patch.diff({"zt": 10}, {"zt": "12%"})
    assert p == [{"op": "set", "path": "zt", "value": "12%"}]
