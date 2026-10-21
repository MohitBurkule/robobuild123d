"""practice.*: best-CAD-practice gates with no reference. Each test rebuilds the shape of one concrete RV01 / RV17 miss
from review/code/MISSES.md and checks the gate fires on it (and stays quiet on the corrected shape)."""

import numpy as np
import trimesh

from robot.checks import practice as P
from robot.checks.reference_cad import claim


def _box(ext, at=(0, 0, 0)):
    m = trimesh.creation.box(extents=ext)
    m.apply_translation(at)
    return m


def _union(*ms):
    import manifold3d  # noqa: F401 - boolean engine

    return trimesh.boolean.union(list(ms))


# 1. point_table: RV01 Fillet7, tub2_lobes.SLIT = 4 (Y, Z) points read off the STEP
def test_point_table_in_function_scope_flagged_unless_organic():
    code = "def slit():\n    SLIT = ((1.0, 2.0), (1.5, 2.5), (2.0, 2.0), (1.5, -1.0))\n    return SLIT\n"
    assert [x[1] for x in P.point_tables(code)] == ["SLIT"]
    tagged = "def slit():\n    # param: organic hand-traced outline from the photo\n    SLIT = ((1.0, 2.0), (1.5, 2.5), (2.0, 2.0), (1.5, -1.0))\n"
    assert P.point_tables(tagged) == []
    assert P.point_tables("A = ((W, H), (W, 0), (0, 0), (0, H))\n") == []   # params, not numbers


# 2. symmetry: RV01 -X rear corner block 0.5 mm proud with no +X twin
def test_symmetric_part_with_one_sided_leftover_is_flagged():
    base = _box((60, 40, 10))
    sym = P.symmetry_plane(base)
    assert sym is not None and sym[0] == 0
    assert P.asymmetric_blobs(base, 0, 0.0) == []
    bad = _union(base, _box((4, 4, 0.5), (-26.0, -16.0, 5.25)))
    sym = P.symmetry_plane(bad)
    assert sym is not None
    bl = P.asymmetric_blobs(bad, sym[0], sym[1])
    assert bl and any(b["centroid"][0] < -20 for b in bl)


def _bmap(rows):
    return [(np.asarray(p, float), np.asarray(t, float) / np.linalg.norm(t), r, turn) for p, t, r, turn in rows]


# 3. mirror_consistency: a mirrored copy whose blend differs from its seed (Chamfer2 / Mirror7: copies not equal)
def test_mirror_copy_with_other_blend_flagged():
    z = (0, 0, 1)
    seed = [((10, 5, h), z, 1.0, 90.0) for h in (0, 1, 2)]
    good = _bmap(seed + [((-10, 5, h), z, 1.0, 90.0) for h in (0, 1, 2)])
    bad = _bmap(seed + [((-10, 5, h), z, 1.5, 90.0) for h in (0, 1, 2)])
    assert P.mirror_mismatches(good, 0, 0.0) == []
    assert len(P.mirror_mismatches(bad, 0, 0.0)) == 6


# 4. blend_consistency: RV17 Fillet1, a blend picked by edge length leaves the short middle segment sharp
def test_blend_stopping_partway_and_two_radii_on_one_run():
    x = (1, 0, 0)
    run = [((s, 0, 0), x, 0.0 if 4 <= s <= 5 else 0.8, 90.0) for s in np.arange(0, 10, 0.75)]
    br = P.blend_breaks(_bmap(run))
    assert br and br[0][1] == "stops"
    two = [((s, 0, 0), x, 1.0 if s < 5 else 1.5, 90.0) for s in np.arange(0, 10, 0.75)]
    assert P.blend_breaks(_bmap(two))[0][1] == "radius"
    one = [((s, 0, 0), x, 1.0, 90.0) for s in np.arange(0, 10, 0.75)]
    assert P.blend_breaks(_bmap(one)) == []


# 5. radius_palette: RV01 Fillet12 / Fillet20, R1.5 (a relation 3 * SKIN / 2) where the part's corners are R1
def test_one_off_radius_next_to_the_common_one():
    z = (0, 0, 1)
    rows = [((i * 3.0, 0, 0), z, 1.0, 90.0) for i in range(40)] + [((0, 50 + i, 0), z, 1.5, 90.0) for i in range(3)]
    sl = P.palette_slips(_bmap(rows))
    assert sl and sl[0][0] == 1.5 and sl[0][2] == 1.0
    assert P.palette_slips(_bmap([r for r in rows if r[2] == 1.0])) == []


# 6. chamfer_corners: RV01 Chamfer3, the deck chamfer stops at the plan corner and leaves a 1.1 mm lump
def test_chamfer_ending_at_a_square_corner():
    ch = [((x, 0, 0), (1, 0, 0), 0.0, 45.0) for x in np.arange(0, 10, 0.75)]
    corner = [((10.5, 0.5, 0), (0, 1, 0), 0.0, 90.0)]
    assert P.chamfer_corner_lumps(_bmap(ch + corner))
    wrapped = [((10.5, y, 0), (0, 1, 0), 0.0, 45.0) for y in np.arange(0.5, 5, 0.75)]
    assert P.chamfer_corner_lumps(_bmap(ch + wrapped)) == []


# 7. drawn_vs_catalog: RV01 Cut-Extrude6, a hex pocket that does not close round its nut
def test_pocket_gaps_close_round_the_nut():
    nut = trimesh.creation.cylinder(radius=3.17, height=2.0, sections=6)
    host = trimesh.creation.box(extents=(20, 20, 6))
    tight = trimesh.creation.cylinder(radius=3.17 + 0.15, height=2.0, sections=6)
    loose = trimesh.creation.cylinder(radius=3.17 + 0.15, height=2.0, sections=6)
    loose.apply_translation((0.4, 0, 0))
    g_tight = P.pocket_gaps(nut, trimesh.boolean.difference([host, tight]))
    g_loose = P.pocket_gaps(nut, trimesh.boolean.difference([host, loose]))
    assert g_tight.max() <= 0.2 + 0.05
    assert g_loose.max() > 0.2 + 0.05


# 8. waiver_bounds: RV01 Mirror8, a lobe-tail waiver whose sphere also held the hex pocket 0.15 off
def test_waiver_claims_only_its_own_blob():
    e = {"deviations": [{"near": [28.0, -12.0, 8.0], "r": 5.0, "reason": "lobe tail trimmed to the side panel (RV01 STEP overlap)"}]}
    items = [{"kind": "moved", "centroid": [28.2, -12.3, 8.1]}, {"kind": "moved", "centroid": [28.5, -9.0, 8.5]}]
    got, held = claim(items, e)
    assert list(got) == [0] and [i for i, _ in held] == [1]


def test_two_sided_code_without_mirror_flagged():
    hand = "def lobes():\n    a = box(4.5, 2).at(21.5, 3.0)\n    b = box(4.5, 2).at(-21.5, -3.0)\n    return a + b\n"
    assert P.two_sided_code(hand)
    loop = "def lobes():\n    out = []\n    for s in (1, -1):\n        out.append(box(4.5, 2).at(s * 21.5, s * 3.0))\n    return out\n"
    assert P.two_sided_code(loop) == []
    mir = "def lobes():\n    a = box(4.5, 2).at(21.5, 3.0)\n    return a + mirror(a)  # -21.5, -3.0\n"
    assert P.two_sided_code(mir) == []
