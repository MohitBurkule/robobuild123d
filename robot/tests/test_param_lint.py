import json

from robot.checks import param_lint as P
from robot.spec import Spec

BAD = """
def bracket():
    a = box(37.5, 12.3, 4.4)
    b = a.translate((11.7, -6.15, 2.2))
    return b.fillet(0.8)
"""

GOOD = """
W, D, T = 37.5, 12.3, 4.4
R = 0.8
def bracket(w=W):
    a = box(w, D, T)
    b = a.translate((w / 2, -D / 2, T / 2))
    pts = a.vertices()[3]
    return b.fillet(R).rotate(90) * 2
"""

ORGANIC = """
# param: organic B-spline control points traced from the reference blade
def blade():
    return spline([(1.3, 4.7), (5.9, 8.1), (9.2, 3.3), (12.4, 0.6)])

def nose():
    # param: organic nose curve from reference photo
    pts = [(3.1, 2.2), (4.4, 5.5), (7.7, 6.6)]
    # param: end
    return pts
"""

NO_REASON = """
# param: organic
def blade():
    return spline([(1.3, 4.7), (5.9, 8.1)])
"""

DUP = """
def a(): return 3.7
def b(): return 3.7
def c(): return 3.7
"""


def test_bad_flags_literals():
    f = P.lint_source(BAD)["funcs"]["bracket"]
    assert f["count"] == 7 and f["worst"]


def test_good_is_clean():
    assert P.lint_source(GOOD)["funcs"]["bracket"]["count"] == 0


def test_organic_marker_and_region():
    r = P.lint_source(ORGANIC)
    assert r["funcs"]["blade"]["exempt"] and r["funcs"]["blade"]["count"] == 0
    assert r["funcs"]["nose"]["count"] == 0 and not r["problems"]


def test_marker_without_reason_is_problem():
    assert P.lint_source(NO_REASON)["problems"]


def test_spec_exempt_and_duplicates():
    assert P.lint_source(BAD, {"bracket": "x"})["funcs"]["bracket"]["count"] == 0
    assert len(P.lint_source(DUP)["values"][3.7]) == 3


def _spec(tmp_path, src, extra=None):
    (tmp_path / "b.py").write_text(src)
    d = {"name": "t", "parts": [{"id": "p", "kind": "structure", "shape": {"type": "model", "file": "b.py"}}], **(extra or {})}
    return Spec(json.loads(json.dumps(d)), tmp_path)


def test_spec_level_findings(tmp_path):
    out, total = P.lint_spec(_spec(tmp_path, BAD + DUP))
    ids = {(f.id, f.severity, f.passed) for f in out}
    assert ("param.literals", "blocker", False) in ids and ("param.duplicate", "warning", False) in ids and total == 10
    out, _ = P.lint_spec(_spec(tmp_path, GOOD))
    assert all(f.passed for f in out)
    out, _ = P.lint_spec(_spec(tmp_path, BAD, {"param_exempt": [{"func": "bracket"}]}))
    assert any(f.id == "param.exempt_reason" and not f.passed for f in out)
    out, _ = P.lint_spec(_spec(tmp_path, BAD, {"review": {"param": {"max_literals": 10}}}))
    assert not any(f.id == "param.literals" and not f.passed for f in out)
