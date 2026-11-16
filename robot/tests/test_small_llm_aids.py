"""Aids for small LLMs: measured escape moves, root-cause grouping, jiggle solver, cache sees dispatched files."""

import json

from robot import escape, rootcause, spec, world
from robot.checks import Ctx, Options, interference
from robot.finding import BLOCKER, fail
from robot.tests.test_interference import _ctx, box, ids


def test_overlap_message_has_measured_escape():
    c = _ctx([box("a", (0, 0, 0)), box("b", (8, 0, 0), kind="electronics")])
    f = ids(interference.run(c), "interference.overlap")[0]
    assert not f.passed and "Smallest fixes (measured)" in f.message
    mv = escape.options(c.world, c.world.body("a"), c.world.body("b"), 0.0, lambda x, y: 0.0)
    best = mv[0]
    assert abs(best.mm - 2.0) < 0.15 and best.axis in ("+x", "-x") and not best.new_hits
    assert any(h["kind"] == "move" for h in f.repair)


def test_escape_avoids_third_part():
    # b overlaps a by 2 mm on +x side; moving b +x would hit c, so the clean best is a -x (or b in y/z)
    c = _ctx([box("a", (0, 0, 0)), box("b", (8, 0, 0)), box("c", (19, 0, 0))])
    mv = escape.options(c.world, c.world.body("a"), c.world.body("b"), 0.0, lambda x, y: 0.0)
    assert not (mv[0].part == "b" and mv[0].axis == "+x")
    assert any(m.part == "b" and m.axis == "+x" and m.new_hits for m in mv)


def test_rootcause_merges_collision_family():
    fs = [fail("interference.overlap", "interference", BLOCKER, "t", "`tub` and `motor` overlap by 0.6 mm.").on("tub", "motor"),
          fail("fit.interference", "fit", BLOCKER, "t", "`motor` overlaps wall `tub` by 0.6 mm").on("motor", "tub"),
          fail("assembly.blocked", "assembly", BLOCKER, "t", "`motor` is trapped: ... hits `tub`.").on("motor"),
          fail("mfg.thin_wall", "mfg", BLOCKER, "t", "`tub` has walls down to 0.06 mm").on("tub")]
    roots = rootcause.group(fs)
    assert len(roots) == 2
    big = roots[0]
    assert big["primary"] == "interference.overlap" and len(big["findings"]) == 3
    assert "ROOT CAUSES: 2 (from 4 blockers)" in rootcause.text(roots)


def test_jiggle_clears_overlap(tmp_path):
    d = {"name": "t", "parts": [box("tub", (0, 0, 0), (30, 30, 4)),
                                box("bat", (0, 0, 5), (10, 10, 8), kind="battery"),
                                box("sw", (9, 0, 5), (10, 10, 8), kind="electronics")]}
    p = tmp_path / "s.json"
    p.write_text(json.dumps(d))
    from robot.solve import jiggle
    res = jiggle.solve(p, max_move=5, log=lambda *_: None)
    assert res.start > 0.5 and res.final == 0 and not res.left
    assert "tub" not in res.shift and res.new_at   # structure never moves
    r = world.resolve(spec.Spec(res.spec), fast=True)
    c = Ctx(r, world.World.start(r), Options(fast=True))
    assert ids(interference.run(c), "interference.overlap")[0].passed


def test_cache_hashes_dispatched_sibling(tmp_path):
    from robot import cache
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "tub.py").write_text("X = 1\n")
    m = tmp_path / "build.py"
    m.write_text("import importlib\ndef build(part):\n    return importlib.import_module('pkg.' + part)\n")
    h1 = cache.model_hash(m)
    (tmp_path / "pkg" / "tub.py").write_text("X = 2\n")
    assert cache.model_hash(m) != h1


def _param_robot(tmp_path):
    (tmp_path / "params.py").write_text("BAY = 8.0  # battery bay x, mm\nPOCKET_X = BAY  # pocket follows the bay\nPOST_X = 14.0\n")
    (tmp_path / "build.py").write_text(
        "import importlib.util, pathlib, build123d as bd\n"
        "def build(part='tub'):\n"
        "    p = pathlib.Path(__file__).with_name('params.py')\n"
        "    from robot import params_override as po\n"
        "    P = po.load_file(p)\n"
        "    plate = bd.Box(40, 40, 6) - bd.Pos(P.POCKET_X, 0, 0) * bd.Box(10, 10, 6)\n"
        "    return plate + bd.Pos(P.POST_X, 0, 0) * bd.Box(4, 4, 6)\n")
    d = {"name": "t", "params": {"P": "params.py"},
         "parts": [{"id": "tub", "kind": "structure", "shape": {"type": "model", "file": "build.py", "params": {"part": "tub"}},
                    "at": [0, 0, 0], "material": "pla"},
                   box("bat", ["P.BAY", 0, 0], (10, 10, 6), kind="battery")]}
    sp = tmp_path / "spec.json"
    sp.write_text(json.dumps(d))
    return sp


def test_params_override_rederives(tmp_path):
    from robot import params_override as po
    _param_robot(tmp_path)
    with po.active({str(tmp_path / "params.py"): {"BAY": 5.0}}):
        assert po.load_file(tmp_path / "params.py").POCKET_X == 5.0
    assert po.load_file(tmp_path / "params.py").POCKET_X == 8.0
    po.write(tmp_path / "params.py", {"BAY": 6.5})
    assert po.read(tmp_path / "params.py", "BAY") == 6.5 and "# battery bay" in (tmp_path / "params.py").read_text()


def test_jiggle_solves_named_param_with_dependents(tmp_path):
    from robot.solve import jiggle
    sp = _param_robot(tmp_path)
    lv = jiggle.parse_levers(sp, ["params.py:BAY=0:10:0.1"])
    res = jiggle.solve_params(sp, lv, log=lambda *_: None)
    assert res["start"] > 0.2 and res["final"] <= 1e-6, res
    new = res["values"]["params.py:BAY"]
    assert 0 <= new <= 7.2   # bat clears the post; the pocket moved with it (no tub/bat overlap left)
