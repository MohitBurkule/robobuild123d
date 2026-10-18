import json
from pathlib import Path

import numpy as np
import pytest

from robot import checks, export, render, spec as spec_mod

TEMPLATE = Path(__file__).resolve().parents[1] / "templates" / "wedge_2wd.json"


@pytest.fixture(scope="module")
def exported(tmp_path_factory):
    out = tmp_path_factory.mktemp("export")
    s = spec_mod.load(TEMPLATE)
    rep, files = export.write_all("wedge_2wd", s, out, checks.Options(deep=True, fast=True), width=400)
    return out / "wedge_2wd", rep, files, s


def test_layout(exported):
    root, rep, files, s = exported
    for f in ["spec.json", "report.json", "REPORT.md", "README.md", "step/assembly.step"] + [f"renders/{v}.png" for v in export.VIEWS]:
        assert (root / f).is_file() and (root / f).stat().st_size > 0, f
    for p in s.parts:
        name = export.safe_name(p.id)
        assert (root / "stl" / f"{name}.stl").stat().st_size > 84
        head = (root / "step" / f"{name}.step").read_text()[:200]
        assert head.startswith("ISO-10303-21")
    assert "MANIFOLD_SOLID_BREP" in (root / "step" / "assembly.step").read_text()
    assert (root / "renders/iso.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"


def test_reports_fail_closed(exported):
    root, rep, _, _ = exported
    j = json.loads((root / "report.json").read_text())
    assert j["not_checked"], "fast export must list what it skipped"
    md = (root / "REPORT.md").read_text()
    assert "## NOT CHECKED" in md
    for x in j["not_checked"]:
        assert x in md
    readme = (root / "README.md").read_text()
    assert "renders/iso.png" in readme and "NOT CHECKED" in readme
    assert json.loads((root / "spec.json").read_text())["name"] == j["name"]


def test_render_views_and_markers(exported):
    _, rep, _, s = exported
    w, rep2, _ = render.world_for(s, checks.Options(deep=False, fast=True, only=["mass"]))
    for v in ["top", "section_z", "back", "iso"]:
        img = render.render_array(w, render.named(v, 200))
        assert img is not None and img.shape[1] == 200
        assert (np.abs(img.astype(int) - [222, 222, 226]).sum(-1) > 30).mean() > 0.05  # something drawn
    m = [render.Marker(w.bounds().mean(0), 3)]
    a = render.render_array(w, render.named("top", 200))
    b = render.render_array(w, render.named("top", 200), markers=m)
    assert ((b == render.RED).all(-1).sum()) > ((a == render.RED).all(-1).sum())
    assert render.named("nope") is None


def test_wire_step_is_brep(exported):
    root, rep, files, s = exported
    assert not [x for x in rep.not_checked if "wire:" in x], rep.not_checked
    assert rep.routes, "template has routed wires"
    for rt in rep.routes:
        p = root / "step" / f"{export.safe_name('wire:' + rt.id)}.step"
        txt = p.read_text()
        assert txt.startswith("ISO-10303-21") and "MANIFOLD_SOLID_BREP" in txt, p
    asm = (root / "step" / "assembly.step").read_text()
    for rt in rep.routes:  # identical bolts/inserts are instanced, so check wires by label rather than counting solids
        assert f"'wire:{rt.id}'" in asm


def test_wire_solid_sweep_volume():
    from robot.finding import Route

    pts = [[0, 0, 0], [20, 0, 0], [20, 0, 0], [20, 15, 0], [20, 15, 10], [30, 15, 10]]
    rt = Route("t", 26, "power", 2.0, 55.0, pts)
    sol = export.wire_solid(rt)
    assert sol.is_valid and len(sol.solids()) == 1
    exact = np.pi * 1.0 ** 2 * 55.0
    assert abs(sol.volume - exact) / exact < 0.03  # round corners shave a little off the straight-segment sum
    bb = sol.bounding_box()
    assert abs(bb.min.X) < 0.05 and abs(bb.max.X - 30) < 0.05 and abs(bb.max.Z - 11) < 0.05
