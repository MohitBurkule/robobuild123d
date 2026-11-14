"""DFM rules via the pure helpers: bed contact, tall/thin aspect, horizontal holes, sheet tabs, declared fits."""

import numpy as np
import trimesh
from types import SimpleNamespace

from robot.checks.dfm import DEFAULTS, bed_contact, drooping_holes, tab_limit, tall_thin, undeclared_fits


def box(w, d, h):
    return trimesh.creation.box((w, d, h))


def test_bed_contact_flat_face_vs_tilted():
    m = box(20, 20, 5)
    area, foot, pt = bed_contact(m, (0, 0, 1))
    assert abs(area - 400.0) < 1e-6 and abs(foot - 400.0) < 1e-6
    tilted = m.copy()
    tilted.apply_transform(trimesh.transformations.rotation_matrix(np.radians(30), (1, 0, 0)))
    area_t, foot_t, _ = bed_contact(tilted, (0, 0, 1))
    assert area_t < 0.5 * foot_t  # only an edge line touches: too little flat area


def test_tall_thin_aspect():
    h, side, top = tall_thin(box(20, 20, 5), (0, 0, 1))
    assert abs(h - 5) < 1e-6 and abs(side - 20) < 1e-6 and top[2] > 0
    h2, side2, _ = tall_thin(box(2, 3, 40), (0, 0, 1))
    assert h2 / side2 > DEFAULTS["max_aspect"]


def test_drooping_holes_axis_and_size():
    up = np.array([0.0, 0.0, 1.0])
    holes = [(6.0, (1.0, 0.0, 0.0), (0, 0, 0)), (2.0, (1.0, 0.0, 0.0), (5, 0, 0)), (6.0, (0.0, 0.0, 1.0), (0, 5, 0))]
    droop = drooping_holes(holes, up, 4.0)
    assert [d for d, _a, _p in droop] == [6.0]  # wide horizontal axis only; small and vertical holes pass
    assert drooping_holes(holes, up, 8.0) == []


def test_tab_limit_scales_with_thickness():
    assert tab_limit("plywood", 3.0, 1.0) == 3.0
    assert tab_limit("steel", 1.5, 1.0) < 1.5  # hard sheet uses the thinner web factor (0.75 x thickness)


def spec(parts, connections=()):
    return SimpleNamespace(parts=parts, connections=connections,
                           part=lambda pid: next((p for p in parts if p.id == pid), None))


def part(pid, kind="printed", catalog=None, process="fdm", **extra):
    return SimpleNamespace(id=pid, kind=kind, catalog=catalog, method=None, process=process, _extra=extra)


def test_sheet_tab_narrow_neck_fires_wide_does_not():
    from shapely.geometry import Polygon
    from robot.checks.dfm import narrow_features
    necked = Polygon([(0, 0), (10, 0), (10, 4.25), (20, 4.25), (20, 0), (30, 0), (30, 10), (20, 10), (20, 5.75),
                      (10, 5.75), (10, 10), (0, 10)])  # two 10x10 squares joined by a 1.5 mm neck
    assert narrow_features(necked, 2.0)  # dfm.sheet_tab_width: a neck under one thickness fires
    solid_slab = Polygon([(0, 0), (30, 0), (30, 10), (0, 10)])
    assert not narrow_features(solid_slab, 2.0)  # no neck: passes


def test_horizontal_hole_ids_bad_and_good():
    up = np.array([0.0, 0.0, 1.0])
    bad = drooping_holes([(8.0, (1.0, 0.0, 0.0), (0, 0, 0))], up, 6.0)
    good = drooping_holes([(8.0, (0.0, 0.0, 1.0), (0, 0, 0))], up, 6.0)
    assert bad and not good  # dfm.horizontal_hole: a wide hole in the layer plane fires; along the build direction passes


def test_undeclared_fits_ids_bad_and_good():
    from robot.checks.dfm import FIT_METHODS
    m = next(iter(FIT_METHODS))
    a, b = part("a"), part("b")
    bad, judged, _ = undeclared_fits(spec([a, b], [SimpleNamespace(a="a", b="b", method=m)]))
    assert bad and judged == 1  # dfm.undeclared_tolerance: printed bore with no declared fit fires
    fitted = part("a", clearance_mm=0.2)
    bad2, judged2, _ = undeclared_fits(spec([fitted, b], [SimpleNamespace(a="a", b="b", method=m)]))
    assert not bad2 and judged2 == 1  # declared clearance_mm: passes


def test_undeclared_fits_flags_printed_bore_without_fit():
    from robot.checks.dfm import FIT_METHODS
    m = next(iter(FIT_METHODS))
    a = part("a")
    b = part("b")
    s = spec([a, b], [SimpleNamespace(a="a", b="b", method=m)])
    bad, judged, missing = undeclared_fits(s)
    assert judged == 1 and len(bad) == 1 and bad[0][0] is s.connections[0] and not missing
    clear = part("a", clearance_mm=0.2)
    s2 = spec([clear, b], [SimpleNamespace(a="a", b="b", method=m)])
    bad2, judged2, _ = undeclared_fits(s2)
    assert judged2 == 1 and not bad2


def _ctx(parts_meshes):
    """A minimal check ctx: one fdm part per (id, mesh, print_orientation)."""
    import robot.checks.dfm as M

    rps = []
    for pid, mesh in parts_meshes:
        p = SimpleNamespace(id=pid, kind="printed", catalog=None, process="fdm", material=None, _extra={"print_orientation": "+z"})
        rps.append(SimpleNamespace(part=p, cat=None, geom=SimpleNamespace(mesh=mesh, solid=None)))
    spec = SimpleNamespace(raw={}, parts=[rp.part for rp in rps], connections=[],
                           part=lambda pid: next((q for q in [rp.part for rp in rps] if q.id == pid), None))
    ctx = SimpleNamespace(r=SimpleNamespace(spec=spec, parts=rps), world=SimpleNamespace(body=lambda pid: None),
                          not_checked=[], metrics={})
    return ctx, M


def test_fdm_run_emits_bed_contact_and_tall_thin_bad_and_good():
    ctx, M = _ctx([("good", box(20, 20, 5)), ("thin", box(2, 2, 40))])
    out = M.run(ctx)
    bad = {f.id for f in out if not f.passed}
    good = {f.id for f in out if f.passed}
    assert "dfm.bed_contact" in bad and "dfm.tall_thin" in bad  # the 2x2x40 part fails both
    assert "dfm.bed_contact" in good and "dfm.tall_thin" in good  # the 20x20x5 part passes both
    assert not any("dfm.bed_contact / tall_thin" in m for m in ctx.not_checked)


def test_fdm_run_without_orientation_is_not_checked_never_a_pass():
    ctx, M = _ctx([("a", box(20, 20, 5))])
    ctx.r.parts[0].part._extra.pop("print_orientation")
    out = M.run(ctx)
    assert not out and any("print_orientation" in m for m in ctx.not_checked)


def test_undeclared_fits_missing_part_and_catalog_escape():
    from robot.checks.dfm import FIT_METHODS
    m = next(iter(FIT_METHODS))
    s = spec([part("a")], [SimpleNamespace(a="a", b="ghost", method=m)])
    bad, judged, missing = undeclared_fits(s)
    assert not bad and judged == 0 and missing and "ghost" in missing[0]
    c = part("motor", catalog="n10")
    p = part("a")
    s2 = spec([p, c], [SimpleNamespace(a="a", b="motor", method="press")])
    bad2, judged2, _ = undeclared_fits(s2)
    assert not bad2 and judged2 == 0  # catalog part pocket: practice.drawn_vs_catalog owns it
