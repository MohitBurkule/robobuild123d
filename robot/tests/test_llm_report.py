"""Compact LLM report (robot/llm_report.py): budget, delta, dedupe, root-cause order."""

from robot.llm_report import compact


def _rep(findings, mass=149.0, ok=True):
    return {"ok": ok, "tier": "full", "gate": "design", "metrics": {"mass_total_g": mass, "mass_lo_g": mass - 2,
            "mass_hi_g": mass + 2, "mass_limit_g": 150},
            "findings": [{"id": i, "pass": p, "severity": s, "message": "m", "expected": "1", "actual": "2",
                          "parts": parts, "repair": []} for i, p, s, *rest in findings for parts in [rest[0] if rest else []]],
            "not_checked": ["x"], "not_run": []}


def test_blockers_first_and_root_cause_order():
    rep = _rep([("combat.R1", False, "blocker"), ("mass.over", False, "blocker"), ("legal.footprint", False, "blocker")])
    c = compact(rep)
    ids = [b["id"] for b in c["blockers"]]
    assert ids.index("legal.footprint") < ids.index("mass.over") < ids.index("combat.R1")


def test_dedupe_same_id_same_parts():
    rep = _rep([("fit.band", False, "blocker", ["p1"]), ("fit.band", False, "blocker", ["p1"]),
                ("fit.band", False, "blocker", ["p2"])])
    c = compact(rep)
    assert len(c["blockers"]) == 2 and c["counts"]["blockers"] == 3


def test_delta_between_iterations():
    prev = _rep([("mass.over", False, "blocker"), ("legal.footprint", False, "blocker")], 152.0, ok=False)
    cur = _rep([("legal.footprint", False, "blocker"), ("fit.band", False, "blocker")], 149.0)
    c = compact(cur, prev)
    assert c["delta"]["fixed"] == ["mass.over"]
    assert c["delta"]["new"] == ["fit.band"]
    assert c["delta"]["still"] == ["legal.footprint"]
    assert c["delta"]["mass_g"] == -3.0


def test_budget_trims_warnings_never_blockers():
    many = [(f"warn.{i}", False, "warning") for i in range(50)]
    rep = _rep(many + [("mass.over", False, "blocker")])
    c = compact(rep, budget_chars=1200)
    assert len(c["blockers"]) == 1
    assert len(json_len := __import__("json").dumps(c)) <= 1200 or not c["warnings"]


def test_mass_block():
    c = compact(_rep([], mass=149.0))
    assert c["mass"] == {"total": 149.0, "lo": 147.0, "hi": 151.0, "limit": 150}
