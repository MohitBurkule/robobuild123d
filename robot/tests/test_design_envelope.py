"""One error envelope across the front doors (B6): Schema.errors / Schema.json_schema match design_io's shape."""

import pytest

from robot.design import DesignError, Schema, Setting

S = Schema("testbot", [
    Setting("drive.motor", "choice", "m_a", doc="drive motor", choices=("m_a", "m_b", "m_c")),
    Setting("size.width", "size", "0"),
    Setting("skirts", "flag", "off"),
    Setting("extras", "set", "", choices=("a", "b")),
])


def test_errors_collects_all_not_just_first():
    errs = S.errors({"drive.motor": "m_x", "size.width": "wide", "skirts": "maybe"})
    assert {e["code"] for e in errs} == {"bad_value"}
    assert {e["field"] for e in errs} == {"drive.motor", "size.width", "skirts"}


def test_error_envelope_keys_match_design_io():
    from robot.design_io import _err

    e = S.errors({"drive.motor": "m_b"})  # valid
    assert e == []
    bad = S.errors({"drive.motor": "m_xx"})
    assert set(bad[0]) <= {"code", "field", "message", "value", "allowed", "suggestion", "hint"}
    sample = _err("bad_enum", "f", "m", "v", ("a", "b"))
    assert set(sample) <= {"code", "field", "message", "value", "allowed", "suggestion", "hint"}


def test_error_suggestion_from_close_match():
    errs = S.errors({"drive.motor": "m_b_"})
    assert errs and errs[0].get("suggestion") == "m_b" and errs[0]["allowed"] == ["m_a", "m_b", "m_c"]


def test_unknown_setting_error():
    errs = S.errors({"drive.motorr": "m_a"})
    assert errs[0]["code"] == "unknown_setting" and "drive.motor" in errs[0]["message"]


def test_errors_non_dict():
    assert S.errors(42)[0]["code"] == "bad_type"


def test_errors_accepts_settings_wrapper():
    assert S.errors({"robot": "testbot", "settings": {"skirts": "on"}}) == []


def test_json_schema_roundtrip():
    sch = S.json_schema()
    assert sch["properties"]["skirts"]["type"] == "boolean"
    assert sch["properties"]["drive.motor"]["enum"] == ["m_a", "m_b", "m_c"]
    assert sch["properties"]["extras"]["items"]["enum"] == ["a", "b"]
    assert "number" in sch["properties"]["size.width"]["type"]


def test_valid_values_still_parse():
    d = S.design({"drive.motor": "m_b", "skirts": True, "extras": ["b"], "size.width": "-3.5"})
    assert d["drive.motor"] == "m_b" and d["skirts"] == "on" and d["extras"] == "b"
