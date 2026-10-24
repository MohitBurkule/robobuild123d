"""Unit tests for face_audit.py.  Run: python -m pytest test_face_audit.py -q"""
import os, tempfile
import pytest
import face_audit as fa
from dump_parser import parse_surface


def _dump(lines):
    return [fa._dump_face(parse_surface(l), 'F') for l in lines]


BOX = ['plane n=(0,0,1) o=(0,0,0.01) box=-0.01,-0.01,0.01,0.01,0.01,0.01, area=0.0004']


def test_dump_dedupe_and_units():
    f = _dump(BOX * 2)
    assert len(fa.dedupe(f)) == 1
    assert abs(f[0].area - 400.0) < 1e-6 and abs(f[0].box[3] - 10.0) < 1e-9


def test_split_halves_merge_into_one_patch():
    # SolidWorks splits a cylinder into two halves; they must form one patch
    halves = _dump(['cyl o=(0,0,0) ax=(0,0,1) r=0.0015 box=-0.0015,0,0,0.0015,0.0015,0.003, area=1.41e-5',
                    'cyl o=(0,0,0) ax=(0,0,1) r=0.0015 box=-0.0015,-0.0015,0,0.0015,0,0.003, area=1.41e-5'])
    assert len(fa.make_patches(halves)) == 1


def test_classification():
    ref = _dump(BOX + [
        'cyl o=(0,0,0) ax=(0,0,1) r=0.0015 box=-0.0015,-0.0015,0,0.0015,0.0015,0.01, area=9.42e-5',
        'torus 0.005,0.005,0.01,0,0,1,0.002,0.0005, box=0.0025,0.0025,0.0095,0.0075,0.0075,0.01, area=1e-6'])
    ours = [fa.Face('plane', fa.plane_key((0, 0, 1), (0, 0, 10)), [-10, -10, 10, 10, 10, 10], 400.0),
            # hole rebuilt with wrong radius
            fa.Face('cyl', fa.cyl_key((0, 0, 0), (0, 0, 1), 1.25), [-1.25, -1.25, 0, 1.25, 1.25, 10], 78.5,
                    '', 1.25),
            # stray face
            fa.Face('plane', fa.plane_key((1, 0, 0), (50, 0, 0)), [50, 0, 0, 50, 1, 1], 1.0)]
    r = fa.audit(ref, ours)
    c = r['counts']
    assert c['matched'] == 1 and c['param'] == 1 and c['missing'] == 1 and c['extra'] == 1
    assert r['param'][0]['dump']['radius'] == pytest.approx(1.5)
    assert r['missing'][0]['blend']                      # torus -> fillet face
    assert 'Face audit' in fa.to_markdown(r)


def test_step_roundtrip_against_itself():
    bd = pytest.importorskip('build123d')
    part = bd.Box(20, 20, 10) - bd.Cylinder(1.5, 10)
    part = bd.fillet(part.edges().filter_by(bd.Axis.Z).group_by(bd.Axis.X)[-1], 2)
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 't.step')
        bd.export_step(part, p)
        ours = fa.faces_from_step(p)
        r = fa.audit(ours, fa.faces_from_step(p))
    assert r['counts']['missing'] == 0 and r['counts']['extra'] == 0
    assert any(f.kind == 'cyl' and abs(f.radius - 1.5) < 1e-6 for f in ours)
