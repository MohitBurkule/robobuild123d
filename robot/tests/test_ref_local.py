"""reference_cad.local / reference_cad.radii: dump-free feature-level comparison against the STEP mesh. One test per
RV01 miss kind from review/code/MISSES.md, each on a small solid built to show it."""

import numpy as np
import trimesh

from robot.checks import ref_local as L
from robot.checks import ref_radii as R
from robot.checks.reference_cad import local_findings


def _mesh(solid):
    v, f = solid.tessellate(0.005, 0.1)
    return trimesh.Trimesh(np.array([[p.X, p.Y, p.Z] for p in v]), np.array(f).reshape(-1, 3), process=True)


def _plate(pocket_r=None, at=(0.0, 0.0), sides=6, extra=()):
    import build123d as b

    s = b.Box(40, 30, 6)
    if pocket_r:
        s = s - b.Pos(at[0], at[1], 1.0) * b.extrude(b.RegularPolygon(pocket_r, sides), 2.0)
    for e in extra:
        s = s + e
    return _mesh(s)


# (1) local tolerance 0.1 mm x 2 mm2: RV01 Fillet13, deck pocket corner arcs 0.16 off (reference_cad.diff at 1 mm saw nothing)
def test_local_blob_over_tenth_reported_identical_quiet():
    ref = _plate(3.3)
    assert L.local_blobs(ref, ref) == []
    bl = L.local_blobs(_plate(3.3, at=(0.18, 0.0)), ref)
    assert bl and max(b["max_mm"] for b in bl) > 0.1 and all(b["area_mm2"] >= 2.0 for b in bl)


# (2) mirror / pattern copies: RV01 Mirror7 / Mirror8, the -X copy repeats the seed's error and must be reported too
def test_every_copy_reported_not_just_the_seed():
    ref = _plate(None, extra=())
    import build123d as b

    lobes = [b.Pos(sx * 12.0, 0, 3.0 + 1.0) * b.Cylinder(4.0, 2.0) for sx in (1, -1)]
    bad = [b.Pos(sx * 12.0, 0, 4.0) * b.Cylinder(4.2, 2.0) for sx in (1, -1)]
    bl = L.local_blobs(_plate(None, extra=bad), _plate(None, extra=lobes))
    xs = sorted(round(b_["centroid"][0]) for b_ in bl)
    assert any(x > 5 for x in xs) and any(x < -5 for x in xs)
    assert ref is not None


def _box_fillet(r_by_sign):
    import build123d as b

    s = b.Box(20, 20, 8)
    for sx, r in r_by_sign.items():
        es = s.edges().filter_by(b.Axis.Z).filter_by(lambda e: e.center().X * sx > 0)
        s = b.fillet(es, r) if r > 0 else s
    return _mesh(s)


# (3) fillet / chamfer radius finder: RV01 Fillet12 / Fillet20, R1.5 (a relation) where the reference has R1
def test_radius_finder_flags_wrong_radius_and_missing_blend():
    ref = _box_fillet({1: 1.0, -1: 1.0})
    assert R.radius_diffs(R.radius_pairs(ref, ref)) == []
    d = R.radius_diffs(R.radius_pairs(_box_fillet({1: 1.5, -1: 1.0}), ref))
    assert d and all(c["at"][0] > 0 for c in d)
    assert abs(d[0]["r_ours"] - 1.5) < 0.1 and abs(d[0]["r_ref"] - 1.0) < 0.1
    sharp = R.radius_diffs(R.radius_pairs(_box_fillet({1: 0.0, -1: 1.0}), ref))
    assert sharp and min(c["r_ours"] for c in sharp) < 0.1


# (3b) chamfered corners per feature: RV01 Chamfer2, ours bevels 4 corners where the reference bevels 2
def test_chamfer_on_extra_corners_found():
    import build123d as b

    def ch(signs):
        s = b.Box(20, 20, 8)
        es = s.edges().filter_by(b.Axis.Z).filter_by(lambda e: (e.center().X > 0, e.center().Y > 0) in signs)
        return _mesh(b.chamfer(es, 1.0))

    ref = ch({(True, True), (False, True)})
    ours = ch({(True, True), (False, True), (True, False), (False, False)})
    d = R.radius_diffs(R.radius_pairs(ours, ref))
    assert len(d) == 2 and all(c["at"][1] < 0 for c in d)


# (4) a drawn pocket compared with the reference pocket, not the catalogue: RV01 Cut-Extrude6, hex AF5.5 vs the drawn one
def test_hex_pocket_compared_with_reference_pocket():
    ref = _plate(3.35)           # the designer's drawn hex (its own clearance)
    ours = _plate(3.175)         # catalogue M3 nut AF 5.5 (circumradius 3.175)
    bl = L.local_blobs(ours, ref)
    assert bl and abs(bl[0]["centroid"][0]) < 4 and abs(bl[0]["centroid"][1]) < 4


# (5) a waiver bounds only its feature: the rest of its sphere is still checked (RV01 Mirror8 under the lobe waiver)
def test_waiver_does_not_blank_its_region():
    ref = _plate(3.35, at=(0, 0))
    import build123d as b

    ours = _plate(3.35, at=(0.2, 0), extra=[b.Pos(5.5, 0, 3.6) * b.Box(2.5, 2.5, 1.2)])
    e = {"deviations": [{"near": [5.5, 0.0, 3.6], "r": 5.0, "reason": "boss added for the switch (RV01 STEP has none)"}]}
    out = local_findings(e, {}, "p", "ref.stl", ours, ref)
    loc = next(f for f in out if f.id == "reference_cad.local")
    assert not loc.passed and "1 waived" in loc.message


# (6) surf faces: a chamfer / fillet corner the dump only gives as a box is sampled on the reference surface
def test_surf_face_samples_snap_to_reference():
    from robot.checks.sldprt_dump import surf_samples

    ref = trimesh.creation.box(extents=(10, 10, 10))
    f = {"type": "surf", "box": np.array([4.9, -2, -2, 5.1, 2, 2]) * 1e-3}
    P = surf_samples(f, np.eye(4), ref)
    assert P is not None and np.allclose(P[:, 0], 5.0, atol=1e-6)
