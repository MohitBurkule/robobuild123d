"""UNTESTED when written (no code runs allowed). Fast tests: no CAD build."""
import json

from robot import build_cmd
from robot.evals import run as ev


def test_bad_json(tmp_path):
    p = tmp_path / "d.json"
    p.write_text("{nope")
    r = build_cmd.run(p, tmp_path, export=False)
    assert not r["ok"] and r["stage"] == "parse" and build_cmd.exit_code(r) == 1


def test_validate_errors_give_next_steps(tmp_path):
    p = tmp_path / "d.json"
    p.write_text(json.dumps({"weapon": {"type": "vspin_drsk"}, "colour": "red"}))
    r = build_cmd.run(p, tmp_path, export=False)
    assert r["stage"] == "validate" and r["errors"] and r["next_steps"]
    assert (tmp_path / "d" / "build_result.json").exists()


def test_slug():
    assert build_cmd.slug_of({"name": "My Bot!"}, "x.json") == "my_bot"


def test_eval_cases_wellformed():
    cs = ev.cases()
    assert len(cs) >= 20 and len({c["id"] for c in cs}) == len(cs)


def test_eval_expected_designs_validate():
    from robot import design_io
    for c in ev.cases():
        if c["expect_ok"]:
            _, _, errs = design_io.validate(c["expected"])
            assert not errs, (c["id"], errs)


def test_eval_scores_expected_as_perfect():
    for c in ev.cases():
        if c["expect_ok"]:
            assert ev.score_case(c, c["expected"])["score"] == 1.0, c["id"]
