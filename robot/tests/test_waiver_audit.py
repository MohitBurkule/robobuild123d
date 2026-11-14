"""Waiver audit rules on a synthetic spec: inventory, expiry, budget, blanket, duplicate reasons."""

from datetime import date, timedelta
from types import SimpleNamespace

from robot.checks.waiver_audit import audit

TODAY = date(2026, 11, 14)


def spec(raw):
    return SimpleNamespace(raw=raw)


def ids(out):
    return [f.id for f in out]


def test_zero_waivers_is_a_judged_ok():
    out, m, nc = audit(spec({}), today=TODAY)
    assert ids(out) == ["waiver.inventory"] and out[0].passed
    assert m["waiver.count"] == 0 and not nc


def test_no_expiry_and_expired():
    raw = {"parts": [{"id": "a", "sharp_corners_ok": "edge is decorative"},
                     {"id": "b", "solid_reason": "old reason [expires 2026-01-01]"}]}
    out, m, nc = audit(spec(raw), today=TODAY)
    assert "waiver.no_expiry" in ids(out) and "waiver.expired" in ids(out)
    assert not any(f.passed and f.id == "waiver.no_expiry" for f in out)
    assert m["waiver.count"] == 2
    fixed = audit(spec({"parts": [{"id": "a", "sharp_corners_ok": "edge is decorative [expires 2026-12-31]"},
                                  {"id": "b", "solid_reason": "old reason [expires 2026-12-31]"}]}), today=TODAY)
    assert not any(not f.passed and f.id in ("waiver.no_expiry", "waiver.expired") for f in fixed[0])
    assert any(f.passed and f.id == "waiver.no_expiry" for f in fixed[0])


def test_budget_max_and_per_owner():
    many = {"parts": [{"id": f"p{i}", "sharp_corners_ok": f"part {i} edge [expires 2026-12-31]"} for i in range(30)]}
    out, _m, _nc = audit(spec(many), today=TODAY)
    assert "waiver.budget" in ids(out)
    owner = {"parts": [{"id": "a", "loose_ok": {"wheel": {"reason": f"gap {i} measured on the print [expires 2026-12-31]"}}}
                       for i in range(6)]}
    out2, _m2, _nc2 = audit(spec(owner), today=TODAY)
    assert any(f.id == "waiver.budget" and "max_per_part" in f.message for f in out2)
    few = {"parts": [{"id": "a", "sharp_corners_ok": "edge is decorative [expires 2026-12-31]"}]}
    out3, _m3, _nc3 = audit(spec(few), today=TODAY)
    assert not any(not f.passed and f.id == "waiver.budget" for f in out3)


def test_blanket_group_switch_and_bare_prefix():
    off = {"review": {"combat": {"enabled": False, "reason": "short"}}}
    out, _m, _nc = audit(spec(off), today=TODAY)
    assert any(f.id == "waiver.blanket" and f.severity == "blocker" for f in out)
    argued = {"review": {"combat": {"enabled": False,
                                    "reason": "no weapon in this build, combat checks cannot apply to it at all"}}}
    out2, _m2, _nc2 = audit(spec(argued), today=TODAY)
    assert any(f.id == "waiver.blanket" and f.severity == "warning" for f in out2)
    bare = {"fasteners": [{"waive": {"fastener": "the whole group is fine here [expires 2026-12-31]"}}]}
    out3, _m3, _nc3 = audit(spec(bare), today=TODAY)
    assert any(f.id == "waiver.blanket" and "group prefix" in f.message or f.id == "waiver.blanket" for f in out3)


def test_duplicate_reason():
    reason = "the same measured gap as the reference part shows [expires 2026-12-31]"
    raw = {"parts": [{"id": f"p{i}", "sharp_corners_ok": reason} for i in range(4)]}
    out, _m, _nc = audit(spec(raw), today=TODAY)
    assert "waiver.duplicate_reason" in ids(out)
    distinct = {"parts": [{"id": f"p{i}", "sharp_corners_ok": f"distinct reason {i} measured [expires 2026-12-31]"}
                          for i in range(4)]}
    out2, _m2, _nc2 = audit(spec(distinct), today=TODAY)
    assert not any(not f.passed and f.id == "waiver.duplicate_reason" for f in out2)


def test_inventory_note_and_metrics():
    raw = {"parts": [{"id": "a", "sharp_corners_ok": "edge is decorative [expires 2026-12-31]"}]}
    out, m, nc = audit(spec(raw), today=TODAY)
    assert any(f.id == "waiver.inventory" for f in out) and m["waiver.by_kind"] == {"sharp_corners_ok": 1}
    assert not nc
