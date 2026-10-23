"""Section rings must close when shared vertices sit at k + 0.5 of the old 0.001 rounding grid (visual.holes deck pockets
at z 17.65 were dropped: round(,3) split 1.0005 / 1.00049999 so linemerge left the ring open)."""
import numpy as np
from shapely.geometry import LineString
from shapely.ops import linemerge, unary_union

from robot.checks.ref_features import snap_segments


def _square_segments(eps=1e-12):
    # pocket outline whose corners sit exactly on half-steps of the 0.001 grid, the two segments meeting at each corner
    # disagreeing in the last float bits (as trimesh.mesh_plane produces)
    c = [(1.0005, 2.0005), (4.0005, 2.0005), (4.0005, 5.0005), (1.0005, 5.0005)]
    segs = []
    for i in range(4):
        s, e = np.array(c[i]), np.array(c[(i + 1) % 4])
        segs.append([s + eps, e - eps])
    return np.array(segs)


def _rings(segs):
    mg = linemerge(unary_union([LineString(s) for s in segs]))
    return [g for g in getattr(mg, "geoms", [mg]) if g.is_ring]


def test_old_rounding_left_the_ring_open():
    q = np.round(_square_segments(), 3)
    assert not _rings(q)     # the bug being fixed: the corner rounds to 1.0 on one segment and 1.001 on the next


def test_snapped_ring_closes():
    r = _rings(snap_segments(_square_segments()))
    assert len(r) == 1 and abs(abs(__import__("shapely").geometry.Polygon(r[0]).area) - 9.0) < 1e-6


def test_snap_keeps_distinct_vertices_and_drops_degenerate():
    segs = np.array([[[0, 0], [0.002, 0]], [[0.002, 0], [0.002 + 1e-9, 0]]])
    out = snap_segments(segs)
    assert len(out) == 1 and np.allclose(out[0], [[0, 0], [0.002, 0]])   # 2 um apart stays apart; zero-length dropped
    assert len(snap_segments(np.zeros((0, 2, 2)))) == 0



def test_pocket_touching_outer_outline_is_still_a_hole():
    """tub deck pockets at z 17.65: a pocket outline touching the wall outline at a vertex makes a degree-4 node; linemerge
    split the outer outline into two open lines there, the outer ring was lost and no pocket counted as a hole."""
    from robot.checks.ref_features import holes, section_region

    def ring(pts):
        return [LineString([pts[i], pts[(i + 1) % len(pts)]]) for i in range(len(pts))]

    outer = ring([(-20, -15), (20, -15), (20, 15), (-20, 15)])
    pocket = ring([(-6, 15), (0, 11), (6, 15), (0, 5)])               # two vertices ON the outer outline (as at z 17.65)
    free = ring([(-15, -9), (-9, -9), (-9, -3), (-15, -3)])
    noded = unary_union(outer + pocket + free)
    mg = linemerge(noded)
    assert sum(g.is_ring for g in getattr(mg, "geoms", [mg])) == 1    # old path: outer + touching pocket lost (open lines)
    out = section_region(noded)
    assert abs(out.area - (1200 - 36 - 36)) < 1e-6        # both pockets cut, the wall kept
    # the free pocket is a hole again (with the wall outline lost it was a separate solid); the chevron is cut out too
    assert any(abs(d - 2 * (36 / 3.141592653589793) ** 0.5) < 0.01 and abs(c[0] + 12) < 0.01 for c, d, _ in holes(out))
    assert not out.contains(__import__("shapely").geometry.Point(0, 8))
