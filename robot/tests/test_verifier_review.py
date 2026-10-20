"""Regression tests for the verifier findings of code_review_rvrn2.md (#1-#5, #8-#16, #22-#26, #29): each has a bad case
that used to pass silently and a good case that still passes."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace as NS

import numpy as np
import trimesh

from robot.checks import _review as RV
from robot.checks import intent as I
from robot.checks import param_lint as P
from robot.checks import ref_diff as RD
from robot.checks import reference_cad as RC
from robot.checks import retention as RT
from robot.checks import sharp_corner as S
from robot.finding import BLOCKER, INFO, WARNING
from robot.spec import Spec

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "robot" / "tools"))
import ci_gate as G  # noqa: E402

LOOP = (ROOT / "robot" / "tools" / "ci_loop.sh").read_text()


def _fails(out):
    return [(f.id, f.severity) for f in out if not f.passed]


# ---------------------------------------------------------------------------------------------- #1, #3 ci_gate
def test_gate_rejects_unfinished_baseline_or_trial():
    assert not G.decide(-1, 50, -1, 50) and not G.decide(3, 3, -1, 99)     # bad: used to accept
    assert G.decide(3, 3, 5, 5) and G.decide(3, 2, 5, 4)                    # good


def test_count_respects_return_code():
    log = "[BLOCKER] a.x\n1 blockers, 0 warnings"
    assert G.count_blockers(log, 2) == 1 and G.count_blockers(log, 0) == 1
    assert G.count_blockers(log, 137) == -1 and G.count_blockers(log, 1) == -1


def test_vanished_blockers_need_review(tmp_path):
    base = "[BLOCKER] intent.x on a\n[BLOCKER] param.literals f\n2 blockers, 0 warnings"
    same = "[BLOCKER] param.literals f\n[BLOCKER] intent.x on a\n[BLOCKER] new.one\n3 blockers, 0 warnings"
    gone = "[BLOCKER] param.literals f\n1 blockers, 0 warnings"
    assert G.vanished(base, same) == []
    assert G.vanished(base, gone) == ["[BLOCKER] intent.x on a"]
    assert G.vanished(base, "Killed") is None
    (tmp_path / "b").write_text(base), (tmp_path / "t").write_text(gone)
    assert G.main(["vanished", str(tmp_path / "b"), str(tmp_path / "t")]) == 1


def test_check_groups_of_changed_modules():
    known = "intent param reference_cad mfg sharp_corner retention".split()
    os.chdir(ROOT)
    assert G.check_groups(known, ["robot/checks/intent.py", "robot/checks/param_lint.py", "docs/x.md"]) == ["intent", "param"]
    assert G.check_groups(known, ["robot/checks/_review.py"]) == ["all"]     # shared helper: everything


# ---------------------------------------------------------------------------------------------- #2, #13-#15, #26 ci_loop
def test_ci_loop_syntax():
    assert subprocess.run(["bash", "-n", str(ROOT / "robot" / "tools" / "ci_loop.sh")]).returncode == 0


def test_gate_fails_closed_on_setup():
    gate = LOOP[LOOP.index("gate() {"):LOOP.index("gated() {")]
    assert gate.count("|| return 0") == 1 and '[ "${GATE:-1}" = 1 ] || return 0' in gate   # only the GATE=0 switch
    calls = re.findall(r'gwt "\$GWT/\w+" HEAD[^\n]*', gate)
    assert calls and all("|| { ginfra" in c for c in calls)                 # every gwt is checked
    assert "[ $r -eq 1 ] && echo" in LOOP                               # infra holds are not recorded as rejections


def test_verifier_only_branch_runs_verify():
    gate = LOOP[LOOP.index("gate() {"):LOOP.index("gated() {")]
    assert "pytest robot/tests" in gate and "$GPY vanished" in gate and "$GPY groups" in gate


def test_regen_everywhere():
    gate = LOOP[LOOP.index("gate() {"):LOOP.index("gated() {")]
    assert 'regen "$GWT/trial"' in gate and 'regen "$GWT/base"' in gate               # #15
    wait = LOOP[LOOP.index("nothing new: wait"):LOOP.index("blockers_live.prev")]
    assert "merge_all" in wait and "regen_commit" in wait                               # #13
    assert ">/dev/null 2>&1) && git add" not in LOOP and "regen FAILED" in LOOP


def test_last_verified_only_when_complete():
    assert '[ -z "$failed" ] && echo "$sha" > "$P/ci_last_verified"' in LOOP          # #14


def test_loop_small_consistencies():
    assert r"'^\[(param|refactor)\]'" in LOOP                                          # #26 regex
    assert 'ci_gate_baseline_${head}_$(gmode)' in LOOP                                 # same cache mode
    assert 'stat -c %Y "$S/.now"' in LOOP                                              # share clock


# ---------------------------------------------------------------------------------------------- intent #4 #8 #16 #29
def _disc_world(ports_ok=True, extra=()):
    disc = trimesh.creation.cylinder(20, 3, sections=64)
    bodies = {"disc": NS(id="disc", mesh=disc)}
    bodies.update({b: NS(id=b, mesh=trimesh.creation.box((1, 1, 1))) for b in extra})

    def port(r, ref):
        if not ports_ok:
            raise KeyError(ref)
        return np.array([30.0, 0, 0]) if ref == "a" else np.array([30.0, 10, 0])
    return NS(body=lambda i: bodies.get(i), port=port)


def _ctx(raw, world):
    return NS(r=NS(spec=NS(raw=raw)), world=world, metrics={}, not_checked=[])


def test_wire_clear_rotor_unresolvable_is_not_checked():
    e = {"rule": "wire_clear_rotor", "rotor": ["disc"], "axis": [0, 0, 1], "at": [0, 0, 0]}
    raw = {"intent": [e], "wires": [{"id": "w", "from": "a", "to": "b"}]}
    bad = _ctx(raw, _disc_world(False))
    out = I.run(bad)
    assert ("intent.wire_clear_rotor", BLOCKER) in _fails(out) and bad.not_checked     # used to be a pass
    good = _ctx(raw, _disc_world(True))
    assert not _fails(I.run(good)) and not good.not_checked


def test_intent_crash_and_typo_are_blockers():
    for e in ({"rule": "captive_nut", "nut": "nutt", "host": "disc"},       # part id typo
              {"rule": "captive_nutz", "nut": "disc", "host": "disc"}):      # rule typo
        ctx = _ctx({"intent": [e]}, _disc_world())
        assert ("intent." + e["rule"], BLOCKER) in _fails(I.run(ctx)) and ctx.not_checked
    e = {"rule": "captive_nut", "nut": "nutt", "host": "disc", "severity": "warning"}
    assert ("intent.captive_nut", WARNING) in _fails(I.run(_ctx({"intent": [e]}, _disc_world())))


def test_min_wall_all_excluded_is_not_checked():
    box = trimesh.creation.box((20, 20, 10))
    w = NS(body=lambda i: NS(id=i, mesh=box) if i == "p" else None)
    bad = {"rule": "min_wall", "part": "p", "except": [[[-50, -50, -50], [50, 50, 50]]]}
    assert ("intent.min_wall", BLOCKER) in _fails(I.run(_ctx({"intent": [bad]}, w)))
    assert not _fails(I.run(_ctx({"intent": [{"rule": "min_wall", "part": "p"}]}, w)))


def test_tool_count_missing_tool_not_checked():
    e = {"rule": "tool_count", "max": 2}
    w = NS(body=lambda i: None)
    bad = _ctx({"intent": [e], "fasteners": [{"id": "a", "tool": "hex2"}, {"id": "b"}]}, w)
    assert ("intent.tool_count", BLOCKER) in _fails(I.run(bad))
    good = _ctx({"intent": [e], "fasteners": [{"id": "a", "tool": "hex2"}, {"id": "b", "tool": "hex2"}]}, w)
    assert not _fails(I.run(good))


# ---------------------------------------------------------------------------------------------- param_lint #5 #9
LUG = "def lug(w=37.5, h=12.25, r=4.95, t=3.3, k=(13.0, 26.0, 30.4)):\n    return box(w, h, r, t)\n"
LAM = "L = lambda: box(37.5, 12.25, 4.95, 3.3)\n"
CLS = "class T:\n    TABLE = (13.5, 26.25, 30.75, 41.5)\n"
GOOD = "W, H = 37.5, 12.25\ndef lug(w=W, h=H):\n    return box(w, h)\nL = lambda: box(W, H)\nclass T:\n    TABLE = (W, H)\n"


def test_defaults_lambdas_class_attrs_count():
    assert P.lint_source(LUG)["funcs"]["lug"]["count"] == 7
    assert P.lint_source(LAM)["funcs"]["L"]["count"] == 4
    assert P.lint_source(CLS)["funcs"]["T.<body>"]["count"] == 4
    assert all(f["count"] == 0 for f in P.lint_source(GOOD)["funcs"].values())


def test_exempt_by_qualified_name(tmp_path):
    two = "def build():\n    return box(3.3, 4.4, 5.5, 6.6)\nclass K:\n    def build(self):\n        return box(3.3, 4.4, 5.5, 6.6)\n"
    r = P.lint_source(two, {"build": "organic"})
    assert r["funcs"]["build"]["count"] == 0 and r["funcs"]["K.build"]["count"] == 4   # only the exact qualname
    (tmp_path / "b.py").write_text(two)
    (tmp_path / "c.py").write_text("def build():\n    return box(3.3, 4.4, 5.5, 6.6)\n")

    def lint(ex):
        d = {"name": "t", "parts": [{"id": "p", "kind": "structure", "shape": {"type": "model", "file": "b.py"}},
                                    {"id": "q", "kind": "structure", "shape": {"type": "model", "file": "c.py"}}],
             "param_exempt": ex}
        return P.lint_spec(Spec(json.loads(json.dumps(d)), tmp_path))[0]
    out = lint([{"func": "b.py:build", "reason": "spline"}])
    bad = [f.message for f in out if f.id == "param.literals" and not f.passed]
    assert any("c.py" in m for m in bad) and any("K.build" in m for m in bad) and not any("`build`" in m and "b.py" in m for m in bad)
    out = lint([{"func": "build", "reason": "spline"}, {"func": "b.py:nope", "reason": "x"}])
    msgs = [f.message for f in out if f.id == "param.exempt_unused"]
    assert len(msgs) == 2                                          # bare name ignored, stale entry reported


# ---------------------------------------------------------------------------------------------- reference_cad #10 #23, ref_diff #24
def test_deviation_waiver_needs_reason_and_cap():
    good = {"deviations": [{"near": [0, 0, 0], "r": 3.0, "reason": "boss moved"}]}
    assert RC._covered([1, 0, 0], good) == "boss moved"
    assert RC._covered([1, 0, 0], {"deviations": [{"near": [0, 0, 0], "r": 3.0}]}) is None          # no reason
    assert RC._covered([1, 0, 0], {"deviations": [{"near": [0, 0, 0], "r": 9.0, "reason": "x"}]}) is None   # over cap
    assert RC._covered([0, 0, 0], good, [[-10, -1, -1], [10, 1, 1]]) is None   # big blob, centroid inside
    assert RC._covered([0, 0, 0], good, [[-1, -1, -1], [1, 1, 1]]) == "boss moved"
    bad = RC.deviation_findings({"deviations": [{"near": [0, 0, 0], "r": 9}, good["deviations"][0]]}, "p")
    assert [f.severity for f in bad] == [BLOCKER] and not RC.deviation_findings(good, "p")


def test_reference_unknown_part_is_blocker(tmp_path):
    from robot import spec as spec_mod, world as world_mod
    from robot.checks import Ctx, Options
    (tmp_path / "r.stl").write_text("solid x\nendsolid x\n")
    part = {"id": "plate", "kind": "structure", "material": "PLA", "shape": {"type": "box", "size": [4, 4, 4]}}

    def run(cad):
        r = world_mod.resolve(spec_mod.Spec({"name": "t", "parts": [part], "reference_cad": cad}, ROOT), fast=True)
        return RC.run(Ctx(r, world_mod.World.start(r), Options()))
    assert ("reference_cad.unusable", BLOCKER) in _fails(run({"dir": str(tmp_path), "parts": [{"part": "plat", "file": "r.stl"}]}))
    assert ("reference_cad.unusable", WARNING) in _fails(run({"dir": str(tmp_path), "parts": [{"part": "plate", "file": "nope.stl"}]}))


def test_boolean_diff_names_failing_side():
    good = trimesh.creation.box((4, 4, 4))
    opened = trimesh.Trimesh(vertices=[[-2, -2, 0], [2, -2, 0], [0, 2, 0]], faces=[[0, 1, 2]])   # a sheet: not closed
    assert "model not" in RD.boolean_diff(opened, good, 0.01, 0.0, 0.5)["method"]
    assert "reference not" in RD.boolean_diff(good, opened, 0.01, 0.0, 0.5)["method"]
    assert RD.boolean_diff(good, good)["method"] == "brep-mesh boolean"


# ---------------------------------------------------------------------------------------------- sharp_corner #11 #12, _review #25
def test_review_overrides_bounded_and_reasoned():
    d = {"max_literals": 3, "enabled": True}
    assert RV.resolve({"max_literals": 999}, d, RV.BOUNDS["param"])[0]["max_literals"] == 3        # no reason: ignored
    m, probs, act = RV.resolve({"max_literals": 999, "reason": "legacy"}, d, RV.BOUNDS["param"])
    assert m["max_literals"] == 10 and probs and act["reason"] == "legacy"                          # clamped
    assert RV.resolve({"enabled": False}, d, RV.BOUNDS["param"])[0]["enabled"] is True
    assert RV.resolve({"max_literals": 5, "reason": "ok"}, d, RV.BOUNDS["param"]) [0]["max_literals"] == 5
    assert S.params({"sharp_corner": {"min_r_mm": 0}})["min_r_mm"] == 0.5
    assert S.params({"sharp_corner": {"min_r_mm": 0, "reason": "x"}})["min_r_mm"] == 0.3
    f = RV.override_findings({"max_literals": 999}, d, "param", "param.override", "param")
    assert [x.severity for x in f] == [WARNING]


def test_matches_original_keeps_load_corner_warning(tmp_path):
    from robot.tests.test_sharp_corner import _body, _ctx as sctx, bracket
    ref = bracket(0)
    ref.export(tmp_path / "ref.stl")
    raw = {"reference_cad": {"dir": str(tmp_path), "ref_to_world": np.eye(4).tolist(),
                             "parts": [{"part": "br", "file": "ref.stl"}]}}
    screw = trimesh.creation.cylinder(1.5, 8)
    screw.apply_translation((5, 5, 5))
    out = _fails(S.run(sctx(bracket(0), raw=raw, others=[_body("f1", screw, "fastener", True)])))
    assert (S.CID, WARNING) in out and (S.CID, BLOCKER) not in out       # load corner: no longer INFO
    assert not _fails(S.run(sctx(bracket(0), raw=raw)))                   # no load: still INFO


# ---------------------------------------------------------------------------------------------- retention #22
def test_declared_hold_needs_reason():
    from robot.checks import Options, verify
    from robot import spec

    def run(**kw):
        d = {"name": "r", "parts": [{"id": "spider", "kind": "structure", "shape": {"type": "box", "size": [10, 10, 3]}, "at": [0, 0, 0],
                                     "material": "steel", "process": "cnc"},
                                    {"id": "disc", "kind": "weapon", "shape": {"type": "box", "size": [10, 10, 3]}, "at": [0, 0, 3],
                                     "material": "steel", "process": "cnc", "rotates_with": "spider", "retained": "press_fit", **kw}]}
        return verify(spec.Spec(d), Options(fast=True, only=["retention"]))
    bad = run()
    assert any(f.id == "retention.axial" and not f.passed for f in bad.findings)
    good = run(retained_reason="0.05 mm press onto the hardened shaft, shoulder behind")
    assert not any(f.id == "retention.axial" and not f.passed for f in good.findings)
    assert any(f.id == "retention.declared" and f.severity == INFO for f in good.findings)
