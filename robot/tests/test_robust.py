"""robust group (robot.checks.robust): discovery, usage graph, plan, edits, diff, budgeted runner, findings, report.
No CAD builds: the runner is driven with a fake executor; the worker's source edit and spec hybrid run on tmp files."""

import json
from pathlib import Path
from types import SimpleNamespace as NS

from robot.checks import robust as R
from robot.checks.robust import discover as D, plan as P, report as REP, runner as RUN, usage as U, worker as W

PARAMS = '''"""params"""
import os
# ---- MASTER DESIGN PARAMETERS ----
WALL = 2.0                 # wall
A, B = -3.5, 10            # pair
SA = (30.5, 5.5)
# ----------------------------------
GAP = 0.4                  # bounds: 0.38..0.5
ZERO = 0.0
UNUSED = 7.0
INNER = WALL + GAP
FLAG = False
MOTOR_VARIANT = os.environ.get("X_MOTOR", "datasheet")
MOTOR_VARIANTS = {"datasheet": 1, "step": 2}
GROOVE = os.environ.get("X_GROOVE", "off") == "on"
'''
VARIANTS = '''NAMES = ("pad", "tray")
VARIANTS = {n: False for n in NAMES}
def set_variants(*names):
    for n in VARIANTS:
        VARIANTS[n] = n in names
def variant(name):
    return VARIANTS[name]
'''
PARTS = '''from .params import *
def wall():
    x = INNER * 2
    return x + (1 if variant("pad") else 0)
def plate(n):
    return SA[0] + n + B
def lid():
    return FLAG
PARTS = {"wall": wall, "plate_l": lambda: plate(1), "lid": lid}
'''


def pkg(tmp_path):
    d = tmp_path / "bot" / "src"
    (d / "pk").mkdir(parents=True)
    (d / "pk" / "params.py").write_text(PARAMS)
    (d / "pk" / "variants.py").write_text(VARIANTS)
    (d / "pk" / "parts.py").write_text(PARTS)
    (d / "build.py").write_text("def build(part):\n    return part\n")
    raw = {"name": "t", "parts": [{"id": i, "shape": {"type": "model", "file": "src/build.py", "params": {"part": k}}}
                                  for i, k in (("w", "wall"), ("pl", "plate_l"), ("li", "lid"))] + [{"id": "box", "shape": {"type": "box", "size": [1, 1, 1]}}]}
    return d / "build.py", raw


def test_discover_params_masters_bounds_relations(tmp_path):
    mf, _ = pkg(tmp_path)
    d = D.discover(mf, {"UNUSED": [6, 8]})
    by = {p.name: p for p in d.params}
    assert {"WALL", "A", "B", "SA[0]", "SA[1]", "GAP", "ZERO", "UNUSED"} <= set(by)
    assert by["WALL"].master and by["SA[1]"].master and not by["GAP"].master
    assert by["GAP"].bounds == (0.38, 0.5) and by["UNUSED"].bounds == (6, 8)
    assert by["B"].is_int and by["A"].value == -3.5 and by["SA[0]"].symbol == "SA"
    assert d.relations["INNER"] == ["GAP", "WALL"]
    sw = {s.name: s for s in d.switches}
    assert sw["X_MOTOR"].kind == "choice" and sw["X_MOTOR"].alternatives == ["step"]
    assert sw["X_GROOVE"].alternatives == ["on"]
    assert sw["pad"].kind == "variant" and sw["tray"].kind == "variant"
    assert sw["FLAG"].kind == "flag" and sw["FLAG"].alternatives == [True]


def test_usage_follows_relations_and_ignores_locals(tmp_path):
    mf, raw = pkg(tmp_path)
    u = U.Usage(U.build_graph(D.package_files(mf)), raw)
    assert u.parts_reading("WALL") == ["w"]  # via INNER
    assert u.parts_reading("SA") == ["pl"] and u.parts_reading("B") == ["pl"]
    assert u.parts_reading("x") == []  # a function-local name is not a global read
    assert u.parts_reading("pad", string=True) == ["w"]
    assert u.parts_reading("FLAG") == ["li"] and u.parts_reading("UNUSED") == []


def test_param_jobs_steps_bounds_ints():
    p = D.Param("GAP", "GAP", 0.4, Path("f"), 1, 0, 3, bounds=(0.38, 0.5))
    vals = [j.value for j in P.param_jobs(p, ["w"])]
    assert max(vals) <= 0.5 and min(vals) >= 0.38 and len(vals) == len(set(vals))
    assert P.param_jobs(D.Param("Z", "Z", 0.0, Path("f"), 1, 0, 3), ["w"]) == []  # zero has no relative step
    n = P.param_jobs(D.Param("N", "N", 4, Path("f"), 1, 0, 1, is_int=True), ["w"])
    assert all(j.new_text.isdigit() for j in n) and {j.value for j in n} <= {3.0, 5.0}  # 4 * 1.05 rounds back: dropped
    j = P.param_jobs(D.Param("W", "W", 2.0, Path("f"), 1, 0, 3), ["w"])
    assert [x.id for x in j] == ["W+10%", "W-10%", "W+5%", "W-5%"] and [x.phase for x in j] == [0, 0, 1, 1]


def test_plan_ranks_by_readers_and_interleaves(tmp_path):
    mf, raw = pkg(tmp_path)
    d = D.discover(mf)
    u = U.Usage(U.build_graph(D.package_files(mf)), raw)
    jobs, skipped = P.make_plan(d, u, top_n=2)
    kinds = [j.kind for j in jobs]
    assert kinds[0] != "param" and kinds[1] == "param"  # switch flips and +-10 % edits alternate
    assert all(j.phase == 1 for j in jobs[len(jobs) - sum(j.phase for j in jobs):])  # +-5 % last
    assert {"UNUSED", "ZERO"}.isdisjoint({n for n, _ in skipped})  # unread params are not even ranked
    assert len({j.target for j in jobs if j.kind == "param"}) == 2 and skipped
    jobs_all, _ = P.make_plan(d, u, top_n=2, steps="all")
    assert all(j.phase == 0 for j in jobs_all)


def test_edit_rewrites_literal_and_variant_append(tmp_path):
    mf, _ = pkg(tmp_path)
    d = D.discover(mf)
    p = next(x for x in d.params if x.name == "SA[1]")
    j = P.param_jobs(p, ["pl"])[0]
    f = tmp_path / "copy.py"
    f.write_text(Path(p.file).read_text())
    W.apply_edit(f, vars(j))
    ns = {}
    exec(f.read_text().replace("import os", "import os"), ns)
    assert ns["SA"] == (30.5, 5.5 * 1.1) or abs(ns["SA"][1] - 6.05) < 1e-9
    v = next(s for s in d.switches if s.name == "tray")
    jv = P.switch_jobs(v, [])[0]
    f2 = tmp_path / "v.py"
    f2.write_text(VARIANTS)
    W.apply_edit(f2, vars(jv))
    ns = {}
    exec(f2.read_text(), ns)
    assert ns["VARIANTS"] == {"pad": False, "tray": True}
    c = next(s for s in d.switches if s.name == "X_MOTOR")
    f3 = tmp_path / "c.py"
    f3.write_text(PARAMS)
    W.apply_edit(f3, vars(P.switch_jobs(c, [])[0]))
    ns = {}
    exec(f3.read_text(), ns)
    assert ns["MOTOR_VARIANT"] == "step"


def test_hybrid_spec_rebuilds_only_affected(tmp_path, monkeypatch):
    from robot import geom

    monkeypatch.setattr(geom, "cached", lambda k: True)
    base = {"name": "t", "parts": [{"id": i, "shape": {"type": "model", "file": "src/b.py", "params": {"part": i}}} for i in "abc"]
            + [{"id": "box", "shape": {"type": "box", "size": [1, 1, 1]}}]}
    new = json.loads(json.dumps(base))
    new["parts"][2]["at"] = [1, 0, 0]  # spec entry moved: rebuilt even though no static read
    raw, rebuilt = W.hybrid_spec(base, new, {"a"}, "src/b.py", tmp_path / "x" / "b.py", tmp_path, geom.FINE)
    assert rebuilt == ["a", "c"]
    files = {p["id"]: p["shape"].get("file") for p in raw["parts"]}
    assert files["b"] == "src/b.py" and files["a"].endswith("x/b.py")
    monkeypatch.setattr(geom, "cached", lambda k: False)  # not in the cache: built from the edited sources
    _, rebuilt = W.hybrid_spec(base, new, set(), "src/b.py", tmp_path / "x" / "b.py", tmp_path, geom.FINE)
    assert rebuilt == ["a", "b", "c"]


def test_diff_ignores_messages_and_counts_build_errors():
    base = {"blockers": [["integrity.solids", "tub", "28 shells"]]}
    same = {"blockers": [["integrity.solids", "tub", "29 shells"]]}
    assert not RUN.diff(base, same)["broken"]
    new = RUN.diff(base, {"blockers": same["blockers"] + [["interference.overlap", "a,b", "x"]]})
    assert new["broken"] and new["new"][0][0] == "interference.overlap"
    assert RUN.diff(base, {"error": "spec generation failed", "stage": "build", "blockers": []})["broken"]
    t = RUN.diff(base, {"error": "timed out", "stage": "timeout", "blockers": []})
    assert t["timeout"] and not t["broken"]
    assert RUN.diff(base, {"blockers": []})["fixed"] == [("integrity.solids", "tub")]
    vol = {"blockers": [["integrity.volume", "stator", "-83%"]], "rebuilt": ["stator"]}
    assert RUN.diff({"blockers": []}, vol)["broken"]  # a +-10 % param edit that collapses a part
    assert not RUN.diff({"blockers": []}, vol, "choice")["broken"]  # a COTS swap replaces the part on purpose


def _jobs():
    return [P.Job("SW=on", "SW", "choice"), P.Job("W+10%", "W", "param", phase=0), P.Job("W-10%", "W", "param", phase=0),
            P.Job("V+10%", "V", "param", phase=0), P.Job("W+5%", "W", "param", phase=1), P.Job("V+5%", "V", "param", phase=1)]


def _spec(tmp_path):
    s = tmp_path / "spec.json"
    s.write_text(json.dumps({"name": "t", "parts": []}))
    return s


def test_runner_adaptive_second_pass_only_where_first_broke(tmp_path):
    seen = []

    def ex(job, timeout):
        seen.append(job["id"])
        bl = [["x.y", "p", ""]] if job["id"] in ("W+10%",) else []
        return {"id": job["id"], "blockers": bl, "seconds": 1}

    out = RUN.run(_jobs(), _spec(tmp_path), "src/b.py", budget_s=900, workers=2, execute=ex, log=lambda *a: None)
    assert "W+5%" in out["results"] and "V+5%" not in out["results"]
    assert any(x.startswith("V+5%") for x in out["not_run"]) and seen[0] == "baseline"
    assert out["results"]["W+10%"][2]["broken"] and not out["results"]["SW=on"][2]["broken"]


def test_runner_stops_at_budget(tmp_path):
    t = [0.0]

    def clock():
        return t[0]

    def ex(job, timeout):
        t[0] += 400
        return {"id": job["id"], "blockers": []}

    out = RUN.run(_jobs(), _spec(tmp_path), "src/b.py", budget_s=900, workers=1, execute=ex, clock=clock, log=lambda *a: None)
    assert len(out["results"]) == 2 and len(out["not_run"]) >= 2  # baseline 400 + 2 jobs passes 900: rest not run


def test_runner_baseline_failure_runs_nothing(tmp_path):
    out = RUN.run(_jobs(), _spec(tmp_path), "src/b.py", execute=lambda j, t: {"error": "boom", "stage": "worker"}, log=lambda *a: None)
    assert not out["results"] and len(out["not_run"]) == len(_jobs())


def test_findings_severity_flag_and_report(tmp_path, monkeypatch):
    j = P.Job("W+10%", "W", "param", value=2.2, base=2.0)
    res = {"blockers": [["interference.overlap", "a,b", "0.3 mm3"]], "rebuilt": ["a"], "seconds": 5}
    out = {"baseline": {"blockers": [], "seconds": 3}, "results": {"W+10%": (j, res, RUN.diff({"blockers": []}, res))},
           "not_run": ["V+5%"], "seconds": 10}
    f = R.findings(out, "warning")
    assert len(f) == 1 and f[0].severity == "warning" and f[0].parts == ["a", "b"] and "interference.overlap" in f[0].message
    assert R.findings(out, "blocker")[0].severity == "blocker"
    monkeypatch.setenv("ROBOT_ROBUST_BLOCKER", "1")
    assert R.config({})["blocker"] is True
    assert R.config({"review": {"robust": {"top_n": 3}}})["top_n"] == 3
    md = REP.markdown("t", "abc", out, [j], [("X", 2)], dict(R.DEFAULTS))
    assert "`W`" in md and "interference.overlap" in md and "V+5%" in md and "`X` (2)" in md


def test_group_skips_in_child_and_without_models(monkeypatch, tmp_path):
    ctx = NS(r=NS(spec=NS(raw={"parts": [{"id": "b", "shape": {"type": "box"}}]}, base_dir=tmp_path)), not_checked=[], metrics={})
    monkeypatch.setenv("ROBOT_ROBUST_CHILD", "1")
    assert R.run(ctx) == []
    monkeypatch.delenv("ROBOT_ROBUST_CHILD")
    (tmp_path / "spec.json").write_text("{}")
    out = R.run(ctx)
    assert out and out[0].passed and out[0].id == "robust.sweep"


def test_group_registered():
    from robot import checks

    assert ("robust", True) in checks.GROUPS


def test_job_key_is_checkout_independent(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    keys = []
    for root in (a, b):
        (root / "src").mkdir(parents=True)
        job = {"id": "W+10%", "spec": str(root / "spec.json"), "file": str(root / "src" / "params.py"), "new_text": "2.2", "timeout": 5}
        keys.append(RUN.job_key(job, "src", {"name": "t"}))
    assert keys[0] == keys[1]
    assert RUN.job_key(dict(job, new_text="2.4"), "src", {"name": "t"}) != keys[1]


def test_subprocess_execute_cleans_up_after_a_timeout(tmp_path, monkeypatch):
    import tempfile

    monkeypatch.setattr(tempfile, "tempdir", str(tmp_path))
    res = RUN.subprocess_execute({"id": "x", "spec": str(tmp_path / "missing.json")}, timeout=0.01)
    assert res["stage"] in ("timeout", "worker") and not list(tmp_path.glob("robust_job_*"))
