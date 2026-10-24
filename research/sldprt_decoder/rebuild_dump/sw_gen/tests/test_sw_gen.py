"""pytest -q rebuild_dump/sw_gen/tests  (kernel-free tests; replay test skipped without build123d)."""
import math, os, re, glob
import pytest

from sw_gen import SLDPRT
from sw_gen.model import parse_text, parse_asm_mass, parse_refs, find_refs
from sw_gen import sketch as S
from sw_gen.plan import plan_part, Op, fmt
from sw_gen import emit

SAMPLE = """PART T.SLDPRT
FEATURE 13 | Front Plane | RefPlane | id=2 | suppressed=False
  PLANE 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,
FEATURE 14 | Top Plane | RefPlane | id=3 | suppressed=False
  PLANE 1,0,0,0,0,-1,0,1,0,0,0,0,1,0,0,0,
FEATURE 15 | Right Plane | RefPlane | id=4 | suppressed=False
  PLANE -0,-0,-1,0,1,0,1,0,0,0,0,0,1,0,0,0,
FEATURE 16 | Plane1 | RefPlane | id=9 | suppressed=False
  DIM D1@Plane1@T.Part = 0.005
  PARENT Front Plane | RefPlane
  PLANE 1,0,0,0,1,0,0,0,1,0,0,-0.005,1,0,0,0,
FEATURE 17 | Sketch1 | ProfileFeature | id=26 | suppressed=False
  DIM D1@Sketch1@T.Part = 0.02
  DIM D2@Sketch1@T.Part = 0.004
  PARENT Front Plane | RefPlane
  SKETCH_TO_MODEL 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,
  PT 0_1 (0,0,0)
  SEG 1_1 type=0 constr=False p0=(0,0,0) p1=(0.02,0,0)
  SEG 2_2 type=0 constr=False p0=(0.02,0,0) p1=(0.02,0.01,0)
  SEG 3_3 type=0 constr=False p0=(0.02,0.01,0) p1=(0,0.01,0)
  SEG 4_4 type=0 constr=False p0=(0,0.01,0) p1=(0,0,0)
  SEG 5_5 type=1 constr=False c=(0.01,0.005,0) p0=(0.012,0.005,0) p1=(0.012,0.005,0) r=0.002 dir=1
  SEG 6_6 type=0 constr=True p0=(0,0.005,0) p1=(0.02,0.005,0)
  REL type=4 ents=1_1
  REL type=5 ents=2_2
  REL type=4 ents=3_3
  REL type=5 ents=4_4
  REL type=1 ents=1_1
  REL type=15 ents=5_5
  REL type=4 ents=2_2
  CONTOUR 0 closed=True segs=1_1 2_2 3_3 4_4
  CONTOUR 1 closed=True segs=5_5
FEATURE 18 | Boss-Extrude1 | Extrusion | id=30 | suppressed=False
  DIM D1@Boss-Extrude1@T.Part = 0.003
  PARENT Sketch1 | ProfileFeature
  FACE plane n=(0,-1,0) o=(0,0,0) box=0,0,0,0.02,0,0.003, area=6E-05
  FACE cyl o=(0.01,0.005,0) ax=(0,0,1) r=0.002 box=0.008,0.003,0,0.012,0.007,0.003, area=3.7E-05
  EXTRUDE end1=0 d1=0.003 both=False end2=0 d2=0 reverse=False draft1=0 thin=False merge=True
FEATURE 19 | Fillet1 | Fillet | id=31 | suppressed=True
  DIM D1@Fillet1@T.Part = 0.001
  PARENT Boss-Extrude1 | Extrusion
  FACE cyl o=(0,0,0) ax=(0,0,1) r=0.001 box=0,0,0,0.001,0.001,0.003, area=1E-06
  FILLET r=0.001 type=0 items=-1
FEATURE 20 | Thread1 | SweepThread | id=40 | suppressed=False
"""


@pytest.fixture(scope='module')
def part():
    return parse_text(SAMPLE)


def test_entities_and_merges(part):
    sp = S.analyze(part.by_name['Sketch1'])
    kinds = [e.kind for e in sp.ents]
    assert kinds.count('line') == 5 and kinds.count('circle') == 1
    assert sum(1 for e in sp.ents if e.constr) == 1
    assert len(sp.merges) == 4                     # rectangle corners
    assert len({e.key for e in sp.ents}) == len(sp.ents)


def test_relations_verified(part):
    sp = S.analyze(part.by_name['Sketch1'])
    rels = [r[0] for r in sp.rels]
    assert rels.count('sgHORIZONTAL2D') == 2 and rels.count('sgVERTICAL2D') == 2
    assert sp.stats['rels_unverified'] == 1        # "horizontal" on a vertical line is dropped


def test_dims_matched_by_value(part):
    sp = S.analyze(part.by_name['Sketch1'])
    by = {d['name']: d for d in sp.dims}
    assert by['D1']['value'] == pytest.approx(0.02)
    assert by['D2']['kind'] == 'DIA'


def test_contours(part):
    sp = S.analyze(part.by_name['Sketch1'])
    assert [len(c['keys']) for c in sp.contours] == [4, 1]


def test_plan(part):
    pl = plan_part(part)
    kinds = {fp.name: fp for fp in pl.plans}
    rp = kinds['Plane1'].ops[0]
    assert rp.args[1] == 'OFFSET' and rp.args[2] == 'Front Plane' and rp.args[4] is True
    ex = [o for o in kinds['Boss-Extrude1'].ops if o.kind == 'EXTRUDE'][0]
    assert ex.args[1] is False and ex.args[8] == pytest.approx(0.003)
    assert ex.args[-1] == 'ALL'                    # both contours have surviving side faces
    assert kinds['Thread1'].status == 'SKIP'
    assert any(o.kind == 'SUPPRESS' for o in kinds['Fillet1'].ops)
    sk = [o for o in kinds['Sketch1'].ops if o.kind == 'SKETCH'][0]
    assert sk.args[1] == 'PLANE' and sk.args[2] == 'Front Plane'


def test_fmt_and_lines(part):
    assert fmt(True) == '1' and fmt(1e-20) == '0' and fmt(0.1) == '0.1'
    assert Op('X', ['a|b', 1.5]).line() == 'X|a/b|1.5'


def test_single_macro_structure(part):
    pl = plan_part(part)
    lines = emit.op_lines(pl)
    txt = emit.single_macro('T', lines)
    assert 'Sub main()' in txt and 'Function RunPart' in txt
    assert max(len(l) for l in txt.splitlines()) < 1024
    subs = re.findall(r'^Sub (\w+)', txt, re.M) + re.findall(r'^Function (\w+)', txt, re.M)
    assert len(subs) == len(set(subs))
    # every op kind produced is handled by the interpreter
    disp = set(re.findall(r'Case "([A-Z]+)"', open(emit.INTERP).read()))
    assert {l.split('|')[0] for l in lines if not l.startswith('#')} <= disp


def test_batch_macro():
    t = emit.batch_macro()
    assert 'batch_summary.txt' in t and 'DONE' in t and '.ops.txt' in t


def test_asm_mass():
    p = os.path.join(SLDPRT, 'dumps_v2', 'rvrn 2.0.asmdump.txt')
    if not os.path.exists(p):
        pytest.skip('no asmdump')
    m = parse_asm_mass(p)
    assert 'RV01 Chassis' in m and m['RV01 Chassis']['vol'] > 0


@pytest.mark.parametrize('dump', sorted(glob.glob(os.path.join(SLDPRT, 'dumps_v2', '*.dump.txt')))[:42])
def test_all_revdev_plan(dump):
    from sw_gen.model import load_part, parse_refs
    pl = plan_part(load_part(dump), parse_refs(find_refs(dump)))
    for fp in pl.plans:
        for o in fp.ops:
            assert '\n' not in o.line()


# ---------------------------------------------------------------- dumps_v4_edges / splines / VBA frame
def _v4(name):
    from sw_gen.model import find_edges
    return find_edges(os.path.join(SLDPRT, 'dumps_v2', name + '.dump.txt'))


def test_v4_derived_blend_edges():
    from sw_gen.model import parse_edges
    p = _v4('RV01 Chassis')
    if not p:
        pytest.skip('no dumps_v4_edges')
    e = parse_edges(p)
    for k in ('Fillet19', 'Fillet22', 'Chamfer5'):
        assert e.get(k), k


def test_v4_stale_faces_and_line_mid():
    import numpy as np
    from sw_gen.model import parse_edge_file
    p = _v4('RV17 Wedgelet LH')
    if not p:
        pytest.skip('no dumps_v4_edges')
    d = parse_edge_file(p)
    st = {f['name'] for f in d['features'] if f['stale']}
    assert 'Boss-Extrude7' in st
    for f in d['features']:
        for _, es in f['faces']:
            for x in es:
                if x.kind == 'line':
                    assert np.allclose(x.m, (np.add(x.s, x.e)) / 2)


def test_spline_recovered():
    from sw_gen.model import load_part, edge_curves, parse_edges
    from sw_gen.plan import plan_part
    d = os.path.join(SLDPRT, 'dumps_v2', 'RV17 Wedgelet LH.dump.txt')
    p = _v4('RV17 Wedgelet LH')
    pl = plan_part(load_part(d), None, parse_edges(p), edge_curves(p) if p else [])
    sp = [o for fp in pl.plans if fp.name == 'Sketch21' for o in fp.ops if o.kind == 'SPLINE']
    assert len(sp) == 1 and sp[0].args[2] >= 3


def test_interp_frame_by_hand():
    from sw_gen import emit
    src = open(emit.INTERP, encoding='utf-8').read()
    assert '.MultiplyTransform(' not in src and 'Function LoadTr' in src
