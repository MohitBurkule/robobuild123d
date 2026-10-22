"""robot.drawing: views, features, layout, sheet, dims, check, output, on small test parts."""
import numpy as np
import pytest

bd = pytest.importorskip("build123d")
from build123d import Box, Cylinder, Pos, fillet, chamfer, Axis  # noqa: E402

from robot.drawing import annotate, check, features as F, layout, sheet, views as Vw  # noqa: E402
from robot.drawing.canvas import Canvas, fmt  # noqa: E402
from robot.drawing.parts import PartInfo  # noqa: E402


def plate():
    """40 x 30 x 6 plate, 4 x d3.2 through holes, R2 vertical corner fillets, 1 mm top chamfer on one edge."""
    p = Box(40, 30, 6)
    p = fillet(p.edges().filter_by(Axis.Z), 2.0)
    p = chamfer(p.edges().filter_by(Axis.X).sort_by(Axis.Z)[-1:].sort_by(Axis.Y)[:1], 1.0)
    for x, y in ((-15, -10), (15, -10), (-15, 10), (15, 10)):
        p = p - Pos(x, y, 0) * Cylinder(1.6, 6)
    return p


@pytest.fixture(scope="module")
def part():
    return plate()


def test_fmt():
    assert fmt(2.0) == "2.00" and fmt(1.995) == "1.995" and fmt(81.35) == "81.35"


def test_view_axes_match_project_to_viewport(part):
    for name in Vw.VIEW_DIRS:
        V = Vw.project(part, Vw.make_view(name))
        lo, hi = V.bbox()
        bb = part.bounding_box()
        corners = np.array([[x, y, z] for x in (bb.min.X, bb.max.X) for y in (bb.min.Y, bb.max.Y) for z in (bb.min.Z, bb.max.Z)])
        p2 = np.array([V.to2d(c) for c in corners])
        assert np.allclose(p2.min(0), lo, atol=1e-3) and np.allclose(p2.max(0), hi, atol=1e-3), name
        assert V.hidden or name != "front"


def test_features(part):
    H = F.holes(part)
    assert len(H) == 4 and all(abs(h.d - 3.2) < 1e-6 and abs(h.depth - 6) < 1e-6 for h in H)
    radii = {round(f.r, 3) for f in F.fillets(part, hole_list=H)}
    assert 2.0 in radii
    assert {round(c.leg, 3) for c in F.chamfers(part)} == {1.0}


def test_layout_scale_and_alignment(part):
    vs = {n: Vw.project(part, Vw.make_view(n)) for n in ("front", "top", "left")}
    pl = layout.place_views(vs, (0, 0, 400, 270), {n: dict(l=10, r=10, b=10, t=10) for n in vs})
    assert pl.scale in layout.SCALES
    # projection alignment: a model point keeps sheet x between front and top, sheet y between front and left
    p = np.array([12.0, 7.0, 3.0])
    assert abs(pl.to_sheet("front", vs["front"].to2d(p))[0] - pl.to_sheet("top", vs["top"].to2d(p))[0]) < 1e-9
    assert abs(pl.to_sheet("front", vs["front"].to2d(p))[1] - pl.to_sheet("left", vs["left"].to2d(p))[1]) < 1e-9


def test_occupancy():
    o = layout.Occupancy()
    o.add((0, 0, 10, 10), "text-a")
    assert not o.free((5, 5, 12, 12)) and o.free((20, 20, 25, 25))
    assert not o.segment_free((-5, 5), (15, 5)) and o.segment_free((-5, 20), (15, 20))


def test_sheet_zones():
    sh = sheet.make_sheet("A1")
    assert (sh.cols, sh.rows) == (16, 12)
    c = Canvas(sh.w, sh.h)
    sheet.draw_frame(c, sh)
    sheet.title_block(c, sh, dict(title="T"))
    assert any(it.kind == "text" and it.text == "16" for it in c.walk())


def _draw(part, **kw):
    from robot.drawing.drawing import make_drawing
    info = PartInfo("plate", part, "PLATE", "P1", "pla_st", 1.0, **kw)
    return info, make_drawing(info, "A3", date="2026-01-01")


def test_drawing_dims_match_model(part, tmp_path):
    info, d = _draw(part, hole_roles=[(3.2, (0, 0, 1), "CLEARANCE")])
    labels = [it.attrs.get("label") for it in d.canvas.walk() if it.kind == "group" and it.attrs.get("cls") in ("dim", "callout")]
    assert "40.00" in labels and "30.00" in labels and "6.00" in labels
    assert any(lb.startswith("4x ⌀3.20") and "CLEARANCE" in lb for lb in labels)
    res = check.check_svg(d.svg, part)
    assert res and all(r.ok for r in res), [r for r in res if not r.ok]
    assert d.mass_g == pytest.approx(part.volume * 1.24 / 1000)


def test_check_catches_wrong_text(part):
    info, d = _draw(part)
    bad = d.svg.replace('data-label="40.00"', 'data-label="40.50"', 1)
    assert not all(r.ok for r in check.check_svg(bad, part))


def test_insert_bore_and_reference_checks(part):
    m = check.Model(part)
    info = PartInfo("plate", part, insert_bores=[("x", 3.5, [[15, 10]], (0, 0, 1))])
    assert check.check_insert_bores(info, m)[0].ok            # 3.2 bore, 0.3 under a 3.5 insert
    info.insert_bores = [("x", 3.5, [[15, 10]], (0, 0, 1))]
    assert not check.check_insert_bores(info, m, undersize=(0.1, 0.2))[0].ok
    ref = check.Model(part - Pos(0, 0, 0) * Cylinder(1.0, 6))  # reference has one more hole
    res = check.compare_reference(m, ref)
    assert any(not r.ok and "missing" in r.why for r in res)
    assert all(r.ok for r in check.compare_reference(m, m))


def test_svg_to_pdf(part, tmp_path):
    from robot.drawing.drawing import write
    info, d = _draw(part)
    used = write(d, tmp_path / "p.pdf", png=False)
    assert (tmp_path / "p.pdf").stat().st_size > 1000 and used in ("cairosvg", "rsvg-convert", "matplotlib")
