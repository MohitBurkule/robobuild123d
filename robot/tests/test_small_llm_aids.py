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


def test_probe_mass_and_unknown_material(tmp_path):
    from robot import probe
    d = {"name": "t", "parts": [box("tub", (0, 0, 0), (40, 40, 20)),
                                {**box("skin", (0, 0, 15), (40, 40, 1)), "material": "titanium_gr5"}]}
    p = tmp_path / "s.json"
    p.write_text(json.dumps(d))
    s, r, w = probe._load(p)
    txt = probe.mass_report(s, r, w)
    assert "solid block" in txt and "did you mean `titanium`" in txt


def test_verify_folds_helpers_in(tmp_path):
    from robot import checks
    sp = _param_robot(tmp_path)
    d = json.loads(sp.read_text())
    d["levers"] = [{"param": "params.py:BAY", "lo": 0, "hi": 10, "step": 0.1}]
    sp.write_text(json.dumps(d))
    rep = checks.verify(spec.load(sp), checks.Options(fast=True, only=["interference"]))
    prop = [f for f in rep.findings if f.id == "solve.proposal"]
    assert prop and "BAY 8 ->" in prop[0].message
    assert any(c.get("context") for c in rep.roots)
    assert "FACTS" in rep.helpers["facts"]


def test_line_of_sight_open_top():
    from robot.checks import contain
    walls = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-14, 0, 0), (2, 30, 10)), box("w2", (14, 0, 0), (2, 30, 10)),
             box("w3", (0, -14, 0), (30, 2, 10)), box("w4", (0, 14, 0), (30, 2, 10))]
    bat = box("bat", (0, 0, -2), (10, 10, 6), kind="battery")
    c = _ctx(walls + [bat])
    assert ids(contain.line_of_sight(c), "contain.line_of_sight")[0].passed is False
    c = _ctx(walls + [box("lid", (0, 0, 6), (30, 30, 2)), bat])
    assert ids(contain.line_of_sight(c), "contain.line_of_sight")[0].passed


def test_probe_place_finds_free_spot(tmp_path):
    from robot import probe
    # floor 60x40 with a wall block on the left; a 10x10 brick sitting inside the block must be moved right
    d = {"name": "t", "parts": [{**box("floor", (0, 0, -1), (60, 40, 2)), "kind": "structure"},
                                {**box("wall", (-20, 0, 6), (20, 40, 10)), "kind": "structure"},
                                {**box("brick", (-20, 0, 6), (10, 10, 8)), "kind": "esc"}]}
    p = tmp_path / "s.json"
    p.write_text(json.dumps(d))
    s, r, w = probe._load(p)
    txt = probe.place(s, r, w, "brick", step=2.0)
    assert "free spots" in txt
    first = txt.splitlines()[1]
    x = float(first.split("at (")[1].split(",")[0])
    assert x > -5


def test_proxy_sweep_respects_declared_range(tmp_path):
    from robot import world as world_mod
    from robot.checks import Ctx, Options
    from robot.proxy import interference as pi
    # a flap hinged at x=0 that would hit a post at +90 deg, declared range 0..30 only
    d = {"name": "t", "parts": [{**box("base", (0, 0, -1), (60, 40, 2)), "kind": "structure"},
                                {**box("post", (0, 0, 14), (4, 4, 4)), "kind": "structure"},
                                {**box("flap", (10, 0, 2), (20, 4, 2)), "kind": "structure",
                                 "joint": {"kind": "revolute", "axis": [0, 1, 0], "pivot": [0, 0, 2], "min": -30, "max": 0, "default": 0}}]}
    p = tmp_path / "s.json"
    p.write_text(json.dumps(d))
    s = spec.load(p)
    r = world_mod.resolve(s, fast=True)
    ctx = Ctx(r, world_mod.World.start(r), Options(fast=True))
    assert not [f for f in pi.sweeps(ctx) if not f.passed]
