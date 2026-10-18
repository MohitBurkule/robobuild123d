"""Manufacturing: wall thickness per material and process, and the print bed."""

from robot import spec
from robot.checks import Options, verify
from robot.checks.mfg import min_wall_for
from robot.profile import Profile

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def _rep(parts):
    return verify(spec.Spec({"name": "t", "parts": parts}), Options(only=["mfg"], deep=False, fast=True))


def _ids(rep):
    return {f.id: f for f in rep.findings if f.group == "mfg"}


def test_min_wall_per_material():
    p = Profile()
    assert min_wall_for(p, "fdm", "pla") == 0.9
    assert min_wall_for(p, "fdm", "tpu") == 1.2
    assert min_wall_for(p, "resin", "resin") == 0.8
    assert min_wall_for(p, "fdm", "pla_cf") == 1.0
    assert min_wall_for(p, None, "hdpe") == 1.0 and min_wall_for(p, None, "pp") == 1.0
    assert min_wall_for(p, None, "steel") == 0.3 and min_wall_for(p, None, "aluminium") == 0.5
    assert min_wall_for(p, None, "tape") == 0.0


def test_thin_printed_plate_fails_and_thick_passes():
    thin = _ids(_rep([{"id": "p", "kind": "structure", "material": "pla", "process": "fdm", "shape": {"type": "box", "size": [30, 30, 0.5]}}]))
    assert "mfg.thin_wall" in thin and thin["mfg.thin_wall"].severity == "blocker"
    thick = _ids(_rep([{"id": "p", "kind": "structure", "material": "pla", "process": "fdm", "shape": {"type": "box", "size": [30, 30, 3]}}]))
    assert "mfg.thin_wall" not in thick and thick["mfg.walls"].passed


def test_metal_sheet_allows_thin_wall_and_tpu_needs_more():
    steel = _ids(_rep([{"id": "p", "kind": "plate", "material": "steel", "shape": {"type": "box", "size": [30, 30, 0.8]}}]))
    assert "mfg.thin_wall" not in steel
    tpu = _ids(_rep([{"id": "p", "kind": "structure", "material": "tpu", "process": "fdm", "shape": {"type": "box", "size": [30, 30, 1.0]}}]))
    assert tpu["mfg.thin_wall"].severity == "warning"  # 1.0 >= 0.7 * 1.2


def test_bed():
    f = _ids(_rep([{"id": "p", "kind": "structure", "material": "pla", "process": "fdm", "shape": {"type": "box", "size": [200, 20, 5]}}]))
    assert "mfg.bed" in f
    f = _ids(_rep([{"id": "p", "kind": "plate", "material": "hdpe", "shape": {"type": "box", "size": [200, 20, 5]}}]))
    assert "mfg.bed" not in f  # not printed


def test_wedge_template_finds_real_sliver():
    # chassis_bottom: battery pocket ends at y=17.4, wire channel starts at y=17.5 -> 0.1 mm wall (Rust's grid missed it).
    s = spec.load(ROOT / "tests" / "fixtures_wedge_rust.json")
    cut = s.part("chassis_bottom").shape["base"]["cut"][1]  # the template has since been fixed; re-create the sliver
    cut["at"] = [0.0, 19.2, -2.25]
    rep = verify(s, Options(only=["mfg"], deep=False))
    thin = [f for f in rep.findings if f.id == "mfg.thin_wall"]
    assert any(f.parts == ["chassis_bottom"] for f in thin)
    assert rep.metrics["min_wall_mm"] < 0.2
