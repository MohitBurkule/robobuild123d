"""Feature-level reference comparison (robot.checks.ref_features / ref_diff): a round bore where the reference has a D,
a plain hole where it has a countersink, a missing hole or a misplaced blob must fail; identical parts must pass."""

import math

import numpy as np
import pytest
import trimesh
from shapely.geometry import Point, Polygon

from robot.checks import ref_diff, ref_features


def _plate(bore="round", csk=False, extra_hole=False, shift=0.0):
    """20 x 20 x 4 plate (Z 0..4) with a 5 mm bore at the centre: round, D (1 mm flat) or hex."""
    plate = trimesh.creation.box((20, 20, 4))
    plate.apply_translation((shift, 0, 2))
    if bore == "round":
        cut = trimesh.creation.cylinder(2.5, 10, sections=96)
    elif bore == "D":
        p = Point(0, 0).buffer(2.5, 96).intersection(Polygon([(-3, -3), (3, -3), (3, 1.5), (-3, 1.5)]))
        cut = trimesh.creation.extrude_polygon(p, 10)
        cut.apply_translation((0, 0, -5))
    else:
        r = 2.5 / math.cos(math.radians(30))
        cut = trimesh.creation.extrude_polygon(Polygon([(r * math.cos(math.radians(60 * i)), r * math.sin(math.radians(60 * i))) for i in range(6)]), 10)
        cut.apply_translation((0, 0, -5))
    cut.apply_translation((0, 0, 2))
    m = plate.difference(cut)
    if csk:
        cone = trimesh.creation.cone(4.5, 4.5, sections=96)   # 90 deg cone, apex down
        cone.apply_transform(trimesh.transformations.rotation_matrix(math.pi, (1, 0, 0)))
        cone.apply_translation((0, 0, 4.0))   # 9 mm at the top face down to the 5 mm bore at mid-thickness
        m = m.difference(cone)
    if extra_hole:
        h = trimesh.creation.cylinder(1.0, 10, sections=48)
        h.apply_translation((6, 6, 2))
        m = m.difference(h)
    return m


def test_hole_shape_classifier():
    for kind in ("round", "D", "hex"):
        g = ref_features.section(_plate(kind), 2, 2.0)
        assert [s for _, _, s in ref_features.holes(g)] == [kind]


def test_identical_parts_have_no_feature_diffs():
    d, st = ref_features.compare_sections(_plate("D"), _plate("D"))
    assert not [x for x in d if x["severity"] == "blocker"], d
    assert st["holes_ref"] == st["holes_model"] > 0


def test_round_bore_vs_reference_D_bore_fails():
    d, _ = ref_features.compare_sections(_plate("round"), _plate("D"))
    assert any(x["kind"] == "hole_shape" and x["severity"] == "blocker" for x in d), d


def test_missing_countersink_fails():
    d, _ = ref_features.compare_sections(_plate("round"), _plate("round", csk=True))
    assert any(x["kind"] == "hole_kind" for x in d), d


def test_extra_hole_fails():
    d, _ = ref_features.compare_sections(_plate("round", extra_hole=True), _plate("round"))
    assert any(x["kind"] == "hole_extra" for x in d), d


def test_boolean_diff_blobs():
    a, b = _plate("round"), _plate("round")
    assert not ref_diff.boolean_diff(a, b)["extra"]
    c = _plate("round", extra_hole=True)
    bd = ref_diff.boolean_diff(b, c)   # model b still has material where the reference c has a hole
    assert len(bd["extra"]) == 1 and abs(bd["extra"][0]["volume_mm3"] - math.pi * 4) < 1.5
    assert np.allclose(bd["extra"][0]["centroid"][:2], (6, 6), atol=0.3)


def test_surface_deviation_reports_offset():
    dev = ref_diff.surface_deviation(_plate("round", shift=0.5), _plate("round"), 4000)
    assert 0.4 < dev["model_to_ref"]["max"] < 0.7


def test_gr1507_catalog_envelope_matches_step():
    """GR1507 envelope (STEP part GR1507_1: 19.6 x 19.6 x 30.5 mm along the shaft)."""
    from robot import catalog
    from robot.shapes import to_solid

    bbs = [to_solid(catalog.find(i).shape).bounding_box() for i in ("gr1507_step", "gr1507_step_can")]   # the STEP motor = fixed half + rotor
    lo = [min(getattr(b.min, a) for b in bbs) for a in "XYZ"]
    hi = [max(getattr(b.max, a) for b in bbs) for a in "XYZ"]
    sh = catalog.find("gr1507_step_can").shaft                       # the prop shaft is its own part in the spec; its stick-out ends the envelope
    hi[0] = max(hi[0], sh["at"][0] + sh["len"])
    ext = [h - l for h, l in zip(hi, lo)]
    assert np.allclose(ext[1:], [19.6, 19.6], atol=0.3), ext
    assert abs(ext[0] - 30.5) < 1.5, ext                             # GEPRC drawing 29.1 vs STEP 30.5 (hollow-shaft stick-out)


def test_section_on_a_face_plane_is_moved_off_it():
    # round 53 mount_r: the X=17.40 section lay on the counterbore face plane; d3.2 holes through that face showed in
    # one tessellation and not the other. The section moves PLANE_SHIFT_MM off any face lying in its plane.
    a = trimesh.creation.box((20, 20, 4)); a.apply_translation((0, 0, 2))
    assert ref_features.off_face(1.0, 2, a) == 1.0
    h = ref_features.off_face(4.0, 2, a)
    assert abs(h - 4.0) == pytest.approx(ref_features.PLANE_SHIFT_MM)


def test_one_waiver_claims_every_surface_fragment_inside_it():
    # round 53 mount_r: one flat-floor-vs-cone change samples into 2-3 extra-surface clusters per counterbore
    from robot.checks import reference_cad as rc
    rng = np.random.default_rng(0)
    frag = lambda c: {"kind": "extra", "centroid": list(c), "pts": np.asarray(c) + rng.uniform(-0.3, 0.3, (3, 3))}
    cl = [frag((0, 1.5, 0)), frag((0, -1.5, 0)), frag((0, 0, 6.0))]
    e = {"deviations": [{"near": [0, 0, 0], "r": 3.0, "reason": "STEP counterbore cone; we cut a flat floor"}]}
    assert len(rc.claim(cl, e)[0]) == 1                                   # volume rule: one per kind
    got, held = rc.claim(cl, e, fragments=True)
    assert set(got) == {0, 1} and not held                                # both fragments inside; the far one is not
    cl[1]["pts"] = cl[1]["pts"] + [0, -2.0, 0]                            # a fragment poking out of the sphere
    assert set(rc.claim(cl, e, fragments=True)[0]) == {0}
