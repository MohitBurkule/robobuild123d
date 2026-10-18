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
    rep, files = export.write_all("wedge_2wd", s, out, checks.Options(deep=False, fast=True), width=400)
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
