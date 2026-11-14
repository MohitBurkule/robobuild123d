"""Machine-readable fix hints: Finding.hint(...) wins over the default table, prefix lookup, suggest_fixes ranking."""

from robot.finding import BLOCKER, Report, fail, ok
from robot.fix_hints import Hint, hints_for, suggest_fixes


def f(fid, severity=BLOCKER, expected=None, actual=None, parts=None):
    x = fail(fid, "g", severity, "t", "m")
    if expected is not None or actual is not None:
        x.expect(expected, actual)
    if parts:
        x.on(*parts)
    return x


def test_exact_and_prefix_lookup():
    h = hints_for(f("interference.overlap", expected="0", actual="12.5", parts=["a", "b"]))
    assert len(h) == 1 and h[0]["kind"] == "move" and h[0]["direction"] == "move_apart"
    assert h[0]["amount"] == 12.5 and h[0]["parts"] == ["a", "b"]
    p = hints_for(f("wall.too_thin", expected="1.2", actual="0.8"))
    assert p[0]["target"] == "wall thickness" and p[0]["direction"] == "increase" and p[0]["amount"] == 0.4
    assert hints_for(f("no.match.here")) == []


def test_check_hint_wins_and_passing_has_none():
    x = f("interference.overlap")
    x.hint("weapon.clearance", "increase", 3.5, why="rotor hits lug")
    h = hints_for(x)
    assert len(h) == 1 and h[0]["target"] == "weapon.clearance" and h[0]["amount"] == 3.5 and h[0]["why"] == "rotor hits lug"
    assert hints_for(ok("interference.overlap", "g", "t", "m")) == []


def test_to_dict_repair_only_when_failed():
    x = f("mass.over", expected="150", actual="153")
    d = x.to_dict()
    assert [r["kind"] for r in d["repair"]] == ["param"] and d["repair"][0]["unit"] == "g"
    p = ok("mass.over", "g", "t", "m").to_dict()
    assert "repair" not in p


def test_suggest_fixes_ranks_and_groups():
    rep = Report(name="r")
    rep.findings = [
        f("interference.overlap", parts=["a", "b"], expected="0", actual="2"),
        f("interference.sweep", parts=["b", "c"], expected="0", actual="1"),
        f("wall.too_thin", expected="1.2", actual="0.8"),
        f("interference.overlap", severity="warning", parts=["d"], expected="0", actual="9"),
        ok("interference.spin", "g", "t", "m"),
    ]
    rep.finish()
    s = suggest_fixes(rep)
    assert s["count"] == 3 and len(s["ranked"]) == 3  # overlap, sweep and wall have distinct targets
    by_target = {t["target"]: t for t in s["ranked"]}
    assert by_target["placement/clearance of listed parts"]["findings"] == ["interference.overlap"]
    assert "b" in by_target["placement/clearance of listed parts"]["parts"]
    assert all(r["finding"] != "interference.spin" for r in s["hints"])
    w = suggest_fixes(rep, severities=("warning",))
    assert [r["finding"] for r in w["hints"]] == ["interference.overlap"]


def test_hint_roundtrip():
    h = Hint("swap", "screw", "shorten", 2.0, "mm", ["s1"], "too long")
    d = h.to_dict()
    assert d == {"kind": "swap", "target": "screw", "direction": "shorten", "amount": 2.0, "unit": "mm",
                 "parts": ["s1"], "why": "too long"}
