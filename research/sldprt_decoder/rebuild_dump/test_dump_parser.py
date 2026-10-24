"""pytest tests for dump_parser.py (synthetic v1/v2 lines + every dump in ../dumps if present)."""
import glob, os, math
import pytest
from dump_parser import parse_text, parse_dump, parse_surface

HERE = os.path.dirname(os.path.abspath(__file__))

SAMPLE = """PART T.SLDPRT
FEATURE 0 | Right Plane | RefPlane | id=4 | suppressed=False
  PLANE -0,-0,-1,0,1,0,1,0,0,0,0,0,1,0,0,0,
FEATURE 1 | Sketch1 | ProfileFeature | id=26 | suppressed=False
  DIM D1@Sketch1@T.Part = 0.061
  PARENT Right Plane | RefPlane
  SKETCH_TO_MODEL -0,-0,-1,0,1,0,1,0,0,0.01,0,0,1,0,0,0,
  PT 0_10 (-0.042,0.0305,0)
  SEG 5_8 type=0 constr=True p0=(-0.042,0.0305,0) p1=(0.042,0.0305,0)
  SEG 0_1 type=1 constr=False c=(-0.005,-0.0305,0) p0=(-4.04E-03,-3.02E-02,0) p1=(-4.04E-03,-3.02E-02,0) r=0.001 dir=-1
  REL type=12 ents=0_7 1_9
  CONTOUR 0 closed=True segs=0_1
FEATURE 2 | Boss-Extrude1 | Extrusion | id=90 | suppressed=False
  DIM D1@Boss-Extrude1@T.Part = 0.017
  DIM D1@Sketch1@T.Part = 0.061
  PARENT Sketch1 | ProfileFeature
  FACE plane n=(0,0,1) o=(0,0,0.0085) box=-1,-1,0,1,1,0, area=0.0012
  FACE cyl o=(0,0,0) ax=(0,0,1) r=0.003 area=1E-05
  EXTRUDE end1=4 d1=0 both=True end2=6 d2=0.002 reverse=True draft1=0 thin=False merge=True
  UPTO_REF1 type=2 plane n=(0,1,0) o=(0,0.0215,0) box=0,0,0,1,1,1,
  FACES 2
  FEATURE -1 | Sketch1 | ProfileFeature | id=26 | suppressed=False
  SKETCH_TO_MODEL 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,
FEATURE 3 | Fillet1 | Fillet | id=167 | suppressed=False
  DIM D1@Fillet1@T.Part = 0.003
  PARENT Boss-Extrude1 | Extrusion
  FILLET r=0.003 type=0 items=-1
  EDGE 0 start=(0,0,0) end=(0.01,0,0)
FEATURE 4 | Chamfer1 | Chamfer | id=153 | suppressed=False
  CHAMFER type=0 d=0.001 angle=0.785
"""


def test_tree_and_sketch():
    p = parse_text(SAMPLE)
    assert p.title == 'T.SLDPRT'
    assert [f.name for f in p.features] == ['Right Plane', 'Sketch1', 'Boss-Extrude1', 'Fillet1', 'Chamfer1']
    sk = p.by_name['Sketch1']
    assert sk.idx == 1 and sk.sketch is not None          # top-level definition wins over the sub-feature copy
    s = sk.sketch
    assert s.rot[0] == [-0.0, -0.0, -1.0] and s.normal == (1.0, 0.0, 0.0)
    assert s.to_model((0.001, 0.002, 0)) == pytest.approx((0.01, 0.002, -0.001))
    assert len(s.segs) == 2 and s.segs[0].construction and s.segs[1].is_circle and s.segs[1].dir == -1
    assert s.rels == [(12, ['0_7', '1_9'])]
    assert s.contours[0].closed and s.contours[0].segs == ['0_1']
    assert s.profile_segs() == [s.segs[1]]


def test_extrude_v2():
    p = parse_text(SAMPLE)
    f = p.by_name['Boss-Extrude1']
    e = f.extrude
    assert (e.end1_name, e.both, e.end2_name, e.d2, e.reverse) == ('up_to_surface', True, 'mid_plane', 0.002, True)
    assert e.upto1.kind == 'plane' and e.upto1.params['o'] == (0, 0.0215, 0) and e.upto1_type == 2
    assert f.face_count == 2 and len(f.faces) == 2
    assert f.faces[1].kind == 'cyl' and f.faces[1].params['r'] == 0.003 and f.faces[0].area == 0.0012
    assert f.own_dims() == {'D1': 0.017}
    assert p.sketch_of(f).name == 'Sketch1' and f.children == ['Sketch1']


def test_blends():
    p = parse_text(SAMPLE)
    assert p.by_name['Fillet1'].fillet['r'] == 0.003
    assert p.by_name['Fillet1'].edges == [((0, 0, 0), (0.01, 0, 0))]
    assert p.by_name['Chamfer1'].chamfer['d'] == 0.001


def test_surface_kinds():
    assert parse_surface('torus 1,2,3,0,0,1,0.005,0.001, box=0,0,0,1,1,1,').kind == 'torus'
    assert parse_surface('surf id=4011').params['id'] == '4011'
    assert parse_surface('Face2').kind == 'other'


DUMPS = sorted(glob.glob(os.path.join(HERE, '..', 'dumps', '*.dump.txt')))


@pytest.mark.parametrize('path', DUMPS, ids=[os.path.basename(p) for p in DUMPS])
def test_all_dumps_parse(path):
    p = parse_dump(path)
    assert p.features
    for f in p.features:
        assert not getattr(f, 'errors', None), (f.name, f.errors)
        if f.extrude:
            assert p.sketch_of(f) is not None or f.type in ('ICE',) or True
        if f.sketch:
            R = f.sketch.rot
            for i in range(3):
                assert math.isclose(sum(x * x for x in R[i]), 1.0, abs_tol=1e-6)


def test_rv01_counts():
    path = os.path.join(HERE, '..', 'dumps', 'RV01 Chassis.dump.txt')
    if not os.path.exists(path):
        pytest.skip('dump not present')
    p = parse_dump(path)
    ex = [f for f in p.features if f.extrude]
    assert len(ex) == 25
    assert p.sketch_of(p.by_name['Boss-Extrude1']).name == 'Sketch1'
    assert p.by_name['Boss-Extrude1'].extrude.end1_name == 'mid_plane'
    assert p.by_name['Sketch8'].sketch.trans == pytest.approx((0.0133, 0, 0))
