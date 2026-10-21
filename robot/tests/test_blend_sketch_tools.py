"""blend_finder / sketch_extract on synthetic solids with known blends and dims (no reference data)."""
import numpy as np
from build123d import Axis, Box, Cylinder, Pos, chamfer, fillet

from robot.cad import blend_finder as bf
from robot.cad import sketch_extract as se


def _block():
    b = Box(30, 20, 10)
    b = fillet(b.edges().filter_by(Axis.Z), 2.0)                 # 4 vertical R2 corners
    b = chamfer(b.edges().group_by(Axis.Z)[-1], 1.0)            # top outline chamfer 1
    return b - Pos(5, 0, 0) * Cylinder(3, 20)                    # plain hole: not a blend


def test_blend_finder_recovers_fillets_and_chamfer():
    bl = bf.find(_block())
    kinds = {(b.kind, b.size) for b in bl}
    assert ("fillet", 2.0) in kinds and ("chamfer", 1.0) in kinds
    assert not any(b.kind == "fillet" and b.size == 3.0 for b in bl)      # the hole wall is not a fillet
    ch = [b for b in bl if b.kind == "chamfer"]
    assert len(ch) == 1 and ch[0].n_faces >= 8                             # one tangent chain all round the top


def test_fillet_convexity():
    bl = [b for b in bf.find(_block()) if b.kind == "fillet" and b.size == 2.0]
    assert bl and all(b.convex for b in bl)
    pocket = Box(30, 20, 10) - fillet(Box(10, 6, 20).edges().filter_by(Axis.Z), 1.0)
    inner = [b for b in bf.find(pocket) if b.kind == "fillet"]
    assert inner and all(not b.convex and b.size == 1.0 for b in inner)


def test_sketch_extract_dims_and_relations():
    sk = se.extract(_block(), (0, 0, 0), (0, 0, 1), u=(1, 0, 0))
    d = sk.dims
    vals = np.array(list(d.values()))
    for want in (2.0, 6.0, 26.0, 16.0, 30.0, 20.0):                      # corner R, hole D, flat lengths, W, H
        assert np.any(np.abs(vals - want) < 1e-6), want
    kinds = {r[0] for r in sk.relations}
    assert {"tangent", "equal", "parallel", "perpendicular", "horizontal", "vertical", "symmetric_v"} <= kinds
    assert abs(d["W"] - 30) < 1e-6 and abs(d["H"] - 20) < 1e-6
    hole = [k for k, (c, r, _f) in sk.arcs.items() if abs(r - 3) < 1e-6]
    assert hole and any(abs(d[f"{hole[0]}.midv"] - 5) < 1e-6 for _ in [0])  # hole 5 off the mid line


def test_section_planes_cover_each_direction():
    pl = se.section_planes(_block(), min_faces=1, skin=0.05)
    ns = {tuple(np.round(n, 3)) for _o, n in pl}
    assert (0.0, 0.0, 1.0) in ns
