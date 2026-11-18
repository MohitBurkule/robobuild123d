"""`robot diff A B`: mass delta, newly failing/passing findings, exit 3 on regressions."""

from robot.diffcmd import diff_reports, summarize


def _rep(findings, mass, ok=True):
    return {"ok": ok, "metrics": {"mass_total_g": mass},
            "findings": [{"id": i, "pass": p, "severity": "blocker", "message": "m"} for i, p in findings]}


def test_fixed_new_still():
    a = _rep([("mass.over", False), ("legal.footprint", False), ("fit.band", True)], 152.0)
    b = _rep([("legal.footprint", False), ("interference.overlap", False)], 149.0)
    d = diff_reports(a, b)
    assert d["fixed"] == ["mass.over"]
    assert d["new"] == ["interference.overlap"]
    assert d["still"] == ["legal.footprint"]
    assert d["mass_total_g"] == {"a": 152.0, "b": 149.0, "delta": -3.0}
    assert d["regressed"] is True


def test_no_regressions_when_only_fixed():
    a = _rep([("mass.over", False)], 152.0, ok=False)
    b = _rep([], 149.0, ok=True)
    d = diff_reports(a, b)
    assert d["regressed"] is False and d["fixed"] == ["mass.over"]


def test_regressed_when_ok_flips():
    a = _rep([], 100.0, ok=True)
    b = _rep([("mass.over", False)], 151.0, ok=False)
    assert diff_reports(a, b)["regressed"] is True


def test_identical_reports_are_clean():
    r = _rep([("fit.band", False)], 100.0)
    d = diff_reports(r, r)
    assert d["regressed"] is False and d["fixed"] == [] and d["new"] == []
    assert any("still failing" in line for line in summarize(d))


def test_metric_deltas():
    a = {"ok": True, "metrics": {"mass_total_g": 100.0, "footprint_mm": 140.0}, "findings": []}
    b = {"ok": True, "metrics": {"mass_total_g": 101.5, "footprint_mm": 140.0, "tip_speed_mps": 42.0}, "findings": []}
    m = diff_reports(a, b)["metrics"]
    assert m["mass_total_g"]["delta"] == 1.5
    assert "footprint_mm" not in m


def test_summarize_lines():
    d = diff_reports(_rep([("mass.over", False)], 152.0, ok=False), _rep([], 149.0, ok=True))
    lines = summarize(d)
    assert any("mass:" in line for line in lines) and any("fixed" in line for line in lines)
