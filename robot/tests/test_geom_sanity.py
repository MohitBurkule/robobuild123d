"""geom.* (robot.checks.geom_sanity): B-rep / mesh hygiene of made parts. For every finding id one bad shape that must
be flagged and one good shape that must not, on build123d primitives; plus fail-closed behaviour of the group."""

from types import SimpleNamespace as NS

import numpy as np
import pytest
import trimesh

bd = pytest.importorskip("build123d")

from robot.checks import geom_sanity as S  # noqa: E402
from robot.finding import BLOCKER, WARNING  # noqa: E402


# ------------------------------------------------------------------------------------------------ shapes
def cube():
    return bd.Box(10, 10, 10)


def near_miss_stack(shift=0.02):
    """Two 10 mm cubes stacked in Z, the upper one `shift` mm off in X: a boolean that missed by a hair. Leaves two
    `shift` x 10 ledge faces and edges `shift` long."""
    return bd.Box(10, 10, 10) + bd.Pos(shift, 0, 10) * bd.Box(10, 10, 10)


def pad(h):
    """20 x 20 x 5 plate with a 10 x 20 pad standing `h` proud of half its top face."""
    return bd.Box(20, 20, 5) + bd.Pos(5, 0, 2.5 + h / 2) * bd.Box(10, 20, h)


def counterbored(off):
    """20 x 20 x 10 block, d3 through hole on Z, d6 x 3 counterbore whose centre is `off` mm away in X."""
    return bd.Box(20, 20, 10) - bd.Cylinder(1.5, 10) - bd.Pos(off, 0, 3.5) * bd.Cylinder(3, 3)


def tri_box(ext):
    return trimesh.creation.box(extents=ext)


# ------------------------------------------------------------------------------------------------ geom.tiny_edge
def test_tiny_edge_bad_and_good():
    bad = S.tiny_edges(near_miss_stack(0.02), 0.05)
    assert len(bad) >= 2
    assert all(L < 0.05 for _, L in bad) and bad[0][1] == pytest.approx(0.02, abs=2e-3)
    assert np.asarray(bad[0][0]).shape == (3,)
    assert S.tiny_edges(cube(), 0.05) == []
    assert S.tiny_edges(near_miss_stack(2.0), 0.05) == []   # a real 2 mm step is not a leftover


# ------------------------------------------------------------------------------------------------ geom.sliver_face
def test_sliver_face_bad_and_good():
    bad = S.sliver_faces(near_miss_stack(0.02), 0.05)
    assert bad and bad[0][2] == pytest.approx(0.02, abs=2e-3)   # narrow width of the 0.02 x 10 ledge
    assert S.sliver_faces(cube(), 0.05) == []
    assert S.sliver_faces(bd.Box(100, 20, 2), 0.05) == []       # a long 2 mm plate edge is thin in ratio, not a sliver


def test_face_width_math():
    w, ratio = S.face_width(0.02 * 10, 2 * (0.02 + 10))
    assert w == pytest.approx(0.02, rel=0.01) and ratio < 1e-3
    w, ratio = S.face_width(100.0, 40.0)
    assert w == pytest.approx(5.0) and ratio == pytest.approx(1 / 16)


# ------------------------------------------------------------------------------------------------ geom.near_coplanar_step
def test_near_coplanar_step_bad_and_good():
    bad = S.near_coplanar_steps(pad(0.06), 0.1)
    assert bad and bad[0][1] == pytest.approx(0.06, abs=1e-3)
    assert S.near_coplanar_steps(pad(1.0), 0.1) == []    # a real 1 mm step
    assert S.near_coplanar_steps(cube(), 0.1) == []


# ------------------------------------------------------------------------------------------------ geom.near_miss_hole
def test_near_miss_hole_bad_and_good():
    bad = S.near_miss_holes(counterbored(0.05), 0.1)
    assert len(bad) == 1
    at, miss, r1, r2 = bad[0]
    assert miss == pytest.approx(0.05, abs=1e-3) and sorted((round(r1, 2), round(r2, 2))) == [1.5, 3.0]
    assert abs(at[0]) < 0.1 and abs(at[1]) < 0.1
    assert S.near_miss_holes(counterbored(0.0), 0.1) == []   # concentric
    two = bd.Box(20, 20, 10) - bd.Pos(-5, 0, 0) * bd.Cylinder(1.5, 10) - bd.Pos(5, 0, 0) * bd.Cylinder(1.5, 10)
    assert S.near_miss_holes(two, 0.1) == []                 # two separate holes 10 mm apart


# ------------------------------------------------------------------------------------------------ geom.open_shell
def test_open_shell_bad_and_good():
    m = tri_box([10, 10, 10])
    assert S.open_edges(m)[:2] == (0, 0) and S.open_edges(m)[2] is None
    holed = trimesh.Trimesh(np.asarray(m.vertices), np.asarray(m.faces)[:-1], process=False)
    nb, nm, at = S.open_edges(holed)
    assert nb == 3 and nm == 0 and at is not None
    fin = np.vstack([np.asarray(m.vertices), [[0.0, 0.0, 20.0]]])   # a loose triangle hung on one cube edge
    e = np.asarray(m.faces)[0][:2]
    extra = trimesh.Trimesh(fin, np.vstack([np.asarray(m.faces), [[e[0], e[1], len(fin) - 1]]]), process=False)
    nb, nm, _ = S.open_edges(extra)
    assert nm == 1 and nb == 2


# ------------------------------------------------------------------------------------------------ geom.zero_thickness
def test_zero_thickness_bad_and_good():
    assert S.zero_thickness([10, 10, 10], 1000.0) == []
    thin = S.zero_thickness([10, 10, 0.1], 10.0)
    assert len(thin) == 1 and "along Z" in thin[0]
    assert S.zero_thickness([10, 10, 0.1], 10.0, sheet=True) == []          # a shim cut from sheet is not judged on gauge
    hollow = S.zero_thickness([40, 30, 20], 40.0)                             # 0.17 % of its box: booleaned away
    assert len(hollow) == 1 and "bounding box" in hollow[0]
    assert S.zero_thickness([40, 30, 20], 40.0, sheet=True) == hollow         # fill is judged for sheet parts too


# ------------------------------------------------------------------------------------------------ geom.off_axis_face
def test_off_axis_face_bad_and_good():
    bad = S.off_axis_faces(bd.Rot(0, 0, 0.3) * bd.Box(10, 10, 10), 0.5)
    assert len(bad) == 4 and all(a == pytest.approx(0.3, abs=0.01) for _, a, _, _ in bad)
    assert {ax for _, _, ax, _ in bad} == {"X", "Y"}
    assert S.off_axis_faces(cube(), 0.5) == []
    assert S.off_axis_faces(bd.Rot(0, 0, 30) * bd.Box(10, 10, 10), 0.5) == []   # a deliberate angle


def test_skew_deg():
    a, ax = S.skew_deg([0.0, 0.0, -1.0])
    assert a == 0.0 and ax == "Z"
    a, ax = S.skew_deg([np.cos(np.radians(89.5)), np.sin(np.radians(89.5)), 0.0])
    assert a == pytest.approx(0.5, abs=1e-6) and ax == "Y"


# ------------------------------------------------------------------------------------------------ group
BREP_IDS = {f"geom.{c}" for c in S.BREP_CHECKS}


def _ctx(geom, extra=None, raw=None, load_errors=None, cat=None, process="fdm"):
    part = NS(id="tub", _extra=extra or {}, process=process, kind="structure")
    rp = NS(part=part, cat=cat, geom=geom)
    spec = NS(raw=raw or {}, name="t")
    return NS(r=NS(spec=spec, parts=[rp], load_errors=load_errors or []), world=NS(body=lambda pid: None),
              not_checked=[], metrics={})


def _fails(out):
    return {(f.id, f.severity) for f in out if not f.passed}


def _passed(out):
    return {f.id for f in out if f.passed}


def _geom(solid, ext=(10, 10, 10), **kw):
    m = tri_box(list(ext))
    return NS(mesh=m, volume=abs(float(m.volume)), solid=solid, **kw)


def test_mesh_only_part_is_not_checked_not_passed():
    m = tri_box([10, 10, 10])
    ctx = _ctx(NS(mesh=m, volume=1000.0))           # no `solid`: mesh only
    out = S.run(ctx)
    assert not (_passed(out) & BREP_IDS) and not _fails(out)
    line = next(s for s in ctx.not_checked if "`tub`" in s and "no B-rep" in s)
    assert all(f"geom.{c}" in line for c in S.BREP_CHECKS)
    assert "geom.zero_thickness" in _passed(out)     # what the mesh allows was really judged
    ctx = _ctx(NS(mesh=m, volume=1000.0, solid=None))
    assert not (_passed(S.run(ctx)) & BREP_IDS) and any("no B-rep" in s for s in ctx.not_checked)


def test_failed_geometry_is_not_checked_not_passed():
    ctx = _ctx(_geom(cube()), load_errors=[("tub", "geometry failed: ValueError: boom")])
    out = S.run(ctx)
    assert out == [] and any("`tub`" in s and "did not load" in s for s in ctx.not_checked)


def test_clean_part_passes_every_brep_check():
    ctx = _ctx(_geom(cube()))
    out = S.run(ctx)
    assert not _fails(out) and BREP_IDS <= _passed(out) and not ctx.not_checked


def test_catalog_part_is_skipped():
    ctx = _ctx(_geom(near_miss_stack(0.02)), cat=NS(id="n20"))
    assert S.run(ctx) == [] and ctx.not_checked == []


def test_run_flags_and_escalates_tiny_edges():
    out = S.run(_ctx(_geom(near_miss_stack(0.02))))
    f = _fails(out)
    assert ("geom.tiny_edge", WARNING) in f and ("geom.sliver_face", WARNING) in f
    tiny = next(x for x in out if x.id == "geom.tiny_edge")
    assert tiny.parts == ["tub"] and tiny.at is not None and tiny.fix_hint and tiny.expected
    raw = {"review": {"geom": {"max_tiny_edges": 1, "reason": "test: any tiny edge blocks"}}}
    assert ("geom.tiny_edge", BLOCKER) in _fails(S.run(_ctx(_geom(near_miss_stack(0.02)), raw=raw)))


def test_run_severities_of_hole_step_and_skew():
    assert ("geom.near_miss_hole", BLOCKER) in _fails(S.run(_ctx(_geom(counterbored(0.05), (20, 20, 10)))))
    assert ("geom.near_coplanar_step", WARNING) in _fails(S.run(_ctx(_geom(pad(0.06), (20, 20, 5)))))
    assert ("geom.off_axis_face", WARNING) in _fails(S.run(_ctx(_geom(bd.Rot(0, 0, 0.3) * bd.Box(10, 10, 10)))))


def test_opt_out_needs_a_real_reason():
    ok_ = {"geom_ok": {"tiny_edge": "0.02 mm ledge is the laser kerf witness mark", "sliver_face": "short"}}
    out = S.run(_ctx(_geom(near_miss_stack(0.02)), extra=ok_))
    ids = {i for i, _ in _fails(out)}
    assert "geom.tiny_edge" not in ids and "geom.sliver_face" in ids   # a reason under 20 chars exempts nothing


def test_zero_thickness_in_run_and_sheet_exempt():
    flat = NS(mesh=tri_box([10, 10, 0.1]), volume=10.0)
    assert ("geom.zero_thickness", BLOCKER) in _fails(S.run(_ctx(flat)))
    assert ("geom.zero_thickness", BLOCKER) not in _fails(S.run(_ctx(flat, process="laser")))


def test_open_shell_only_when_integrity_is_off():
    m = tri_box([10, 10, 10])
    holed = trimesh.Trimesh(np.asarray(m.vertices), np.asarray(m.faces)[:-1], process=False)
    g = NS(mesh=holed, volume=1000.0)
    on = S.run(_ctx(g))
    assert not any(f.id == "geom.open_shell" for f in on)             # integrity.solids owns it
    off = S.run(_ctx(g, raw={"integrity": {"enabled": False}}))
    assert ("geom.open_shell", BLOCKER) in _fails(off)
    good = S.run(_ctx(NS(mesh=m, volume=1000.0), raw={"integrity": {"enabled": False}}))
    assert "geom.open_shell" in _passed(good)
