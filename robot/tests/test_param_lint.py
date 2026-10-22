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
    assert P.lint_source(BAD, {"bracket": "x"})["funcs"]["bracket"]["count"] == 0   # keys are qualified names
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
    out, _ = P.lint_spec(_spec(tmp_path, BAD, {"review": {"param": {"max_literals": 10, "reason": "legacy module"}}}))
    assert not any(f.id == "param.literals" and not f.passed for f in out)


def test_pattern_detection():
    assert P.pattern_of([[0, 0], [5, 0], [10, 0]]) == "row"
    assert P.pattern_of([[0, 0], [5, 0], [0, 5], [5, 5]]) == "grid"
    assert P.pattern_of([[10, 0], [0, 10], [-10, 0], [0, -10]]) == "circle"
    assert P.pattern_of([[1.3, 4.7], [5.9, 8.1], [9.2, 3.3]]) is None
    r = P.lint_source("HOLES = [(12.0, 3.0), (24.0, 3.0), (36.0, 3.0)]\nOK = [(1.3, 4.7), (5.9, 8.1), (9.2, 3.3)]\n")
    assert [p[1] for p in r["patterns"]] == ["row"]


def test_mirror_pairs():
    bad = "def arm_left():\n    return box(3.3, 4.4)\ndef arm_right():\n    return box(3.3, 4.4)\n"
    good = "def arm_left():\n    return box(3.3, 4.4)\ndef arm_right():\n    return arm_left().mirror(YZ)\n"
    assert P.lint_source(bad)["mirror_pairs"] == [("arm_left", "arm_right")]
    assert P.lint_source(good)["mirror_pairs"] == []


def test_literal_placement():
    bad = "def place(p):\n    return p.translate((17.5, -4.2, 3.0))\n"
    good = "def place(p, hub):\n    return p.translate(hub.center())\n"
    assert P.lint_source(bad)["placements"] and not P.lint_source(good)["placements"]


def test_unlinked_duplicate():
    from robot.checks.param_lint import param_pool, unlinked
    pool = param_pool("A = 29.5\nB, C = 1.8, 3.0\nT = (21.5, 36.5)\nD = dict(x=4.25)\n")
    assert unlinked(29.5, pool) == "A"
    assert unlinked(21.5, pool) == "T[0]"
    assert unlinked(27.7, pool) == "A - B"
    assert unlinked(4.8, pool) == "B + C"
    assert unlinked(4.25, pool) == "D.x"
    assert unlinked(11.11, pool) is None


def test_module_literals_skip_organic():
    from robot.checks.param_lint import module_literals
    src = "X = 21.5\n# param: organic table\nT = (3.3, 4.4)\n# param: end\ndef f():\n    return 7.7\n"
    assert module_literals(src) == {21.5: [1]}


# ------------------------------------------------------------------ add-ons: copied params, star import, point tables, budget, symmetry
from robot.checks import param_lint as _pl


def test_copied_params_flags_bare_decimals_not_masters_or_tagged():
    src = ("# ---- MASTER DESIGN PARAMETERS ----\nA = 29.5\n# ----\n"
           "B = A - 2.0\nC = 12.7\nD = (3.5, 8.25)\nE = 4.4  # param: datasheet RV12 drawing\n"
           "# param: organic spline\nF = 1.75\nG = dict(x=0.6, y=A)\n")
    cp, nmaster = _pl.copied_params(src)
    assert sorted(n for _l, n, _v in cp) == ["C", "D[0]", "D[1]", "G.x"] and nmaster == 1


def test_star_import_found():
    assert _pl.star_imports("from .params import *\nfrom .common import a\n") == [(1, ".params")]


def test_point_table():
    src = ("P = [(0, 1), (2, 3), (4, 5), (6, 7.5)]\nQ = [(0, 1), (2, 3), (4, 5)]\nR = {'a': (1, 2)}\nS = dict(x=(1, 2))\n"
           "# param: organic traced outline\nT = [(0, 1), (2, 3), (4, 5), (6, 7)]\n")
    assert [n for _l, n, _k in _pl.point_tables(src)] == ["P", "R", "S"]


def test_dump_dims_skips_nested_and_suppressed():
    txt = ("FEATURE 1 | Boss | Extrusion | id=1 | suppressed=False\n  DIM D1@Boss@p.Part = 0.004\n"
           "  DIM D1@Sketch1@p.Part = 0.01\n  FEATURE -1 | Sketch1 | ProfileFeature | id=2 | suppressed=False\n"
           "  DIM D9@Sketch1@p.Part = 0.02\nFEATURE 2 | Cut | ICE | id=3 | suppressed=True\n  DIM D1@Cut@p.Part = 0.001\n"
           "FEATURE 3 | Fillet1 | Fillet | id=4 | suppressed=False\n  DIM D1@Fillet1@p.Part = 0.001\n  DIM D1@Boss@p.Part = 0.004\n")
    assert _pl.dump_dims(txt) == 3


def test_numeric_tokens_and_closure():
    import ast as _ast
    src = "def a():\n    return b(3.5) + 1\n\ndef b(x):\n    return x * 7.25 + 2\n\ndef c():\n    return 9.5\n"
    tree = _ast.parse(src)
    defs = {("m", n.name): n for n in tree.body}
    assert _pl._closure(("m", "a"), defs) == {("m", "a"), ("m", "b")}
    assert _pl.numeric_tokens(src) == 3


def test_mirror_symmetry_detection():
    import trimesh
    box = trimesh.creation.box((10, 4, 2))
    assert _pl.mirror_symmetric(box, 0)
    off = trimesh.util.concatenate([box, trimesh.creation.box((1, 1, 1)).apply_translation((4, 2.5, 0))])
    assert not _pl.mirror_symmetric(off, 0)
    assert _pl.mirror_count("x = a.mirror(P)\ny = mirrored(z)\n") == 2
