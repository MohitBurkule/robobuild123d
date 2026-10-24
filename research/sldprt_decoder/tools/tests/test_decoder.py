"""Run: cd tools && python3 -I -m unittest discover -s tests -v"""
import os
import struct
import sys
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

from sldprt import streams, xt, sketch, meta  # noqa: E402

REVDEV = os.path.join(os.path.dirname(os.path.dirname(HERE)), 'revdev')
RV17 = os.path.join(REVDEV, 'RV17 Wedgelet LH.SLDPRT')


class TestStreams(unittest.TestCase):
    def test_raw_and_nested(self):
        inner = zlib.compress(b'PS\x00\x00' + b'TRANSMIT FILE (partition)' + b'A' * 200, 0)  # level 0 -> 'x\x01' header
        c = zlib.compressobj(9, zlib.DEFLATED, -15)
        raw = c.compress(b'\x14\x06\x01\x00' + b'\x00' * 24 + inner) + c.flush()
        blob = b'junkjunk' + raw + b'tail'
        st = streams.all_streams(blob)
        ps = [x for x in st if streams.classify(x) == 'parasolid']
        self.assertEqual(len(ps), 1)
        self.assertTrue(ps[0]['data'].endswith(b'A' * 200))


def _plane_rec(idx, p, n, x):
    return (b'\x00\x32' + struct.pack('>HI', idx, 7) + struct.pack('>5H', 1, 9, 1, 1, 1) + b'+'
            + struct.pack('>9d', *p, *n, *x))


def _face_rec(idx, surf):
    return (b'\x00\x0e' + struct.pack('>HIH', idx, 99, 1) + struct.pack('>d', 0.0)
            + struct.pack('>5H', 1, 1, 5, 11, surf) + b'-')


class TestXT(unittest.TestCase):
    def test_plane_face_attr(self):
        d = b'PS\x00\x00 TRANSMIT FILE modeller version 3601212 SCH_3601212_1 '
        d += _plane_rec(20, (0, 0, 0.017), (0, 0, 1), (1, 0, 0))
        d += _face_rec(21, 20)
        d += b'\x00\x50' + struct.pack('>IHHH', 1, 30, 1, 31)                        # attdef 30
        d += b'\x00\x4f' + struct.pack('>IH', 12, 31) + b'ATOM_ID_2001'             # its name
        d += b'\x00\x52' + struct.pack('>IH', 5, 40) + struct.pack('>5i', 83, 618, 1710186855, 0, 3)
        d += b'\x00\x51' + struct.pack('>IHIHHHHHH', 1, 41, 5, 30, 21, 1, 1, 1, 1) + struct.pack('>H', 40)
        x = xt.XT(d)
        self.assertEqual(x.surfaces[20]['type'], 'plane')
        self.assertAlmostEqual(x.surfaces[20]['params']['offset_along_normal'], 0.017)
        self.assertEqual(len(x.faces), 1)
        self.assertEqual(x.face_features(21)[0]['feature_id'], 618)


def _sk_rec(rid, payload):
    return struct.pack('<2i', 0, rid) + b'\xff\xff\x1f\x00\x03' + b'\xff' * 8 + b'\x00\x00\x80\xbf' + b'\x00' * 47 + payload


class TestSketch(unittest.TestCase):
    def test_circle(self):
        pt0 = _sk_rec(2, b'\x1e\x00' + struct.pack('<2d', 0.0, 0.0) + b'\x00' * 30)
        pt1 = _sk_rec(1, b'\x1e\x00' + struct.pack('<2d', 0.0016, 0.0) + b'\x00' * 30)
        arc = _sk_rec(1, struct.pack('<3H', 1, 1, 1) + b'\x00\x00' + struct.pack('<d', -1.0)
                      + struct.pack('<3H', 1, 0, 0) + b'\xfe\xff\xff\xff' * 4 + b'\x00' * 20)
        d = b'\xff\xfe\xff\x07' + 'Sketch5'.encode('utf-16-le') + b'\x00' * 20 + pt0 + pt1 + arc
        sk = sketch.decode_sketches(d, ['Sketch5'])[0]
        self.assertEqual(len(sk['points']), 2)
        e = sk['entities'][0]
        self.assertEqual(e['type'], 'circle')
        self.assertAlmostEqual(e['radius'], 0.0016)
        m = sketch.match_dims([('D1', '<MOD-DIAM>3.2')], sk['points'], sk['entities'])
        self.assertEqual(m[0]['matches'][0][3], 'diameter')


class TestMeta(unittest.TestCase):
    def test_keywords(self):
        x = '<Keywords id="1" Name="p"><Extrusion id="103" Name="Cut-Extrude1" DissectableChildren="95"><Dimension Name="D1">12</Dimension></Extrusion><Sketch id="95" Name="Sketch5"/></Keywords>'
        it = meta.parse_keywords(x)
        self.assertEqual(it[103]['dims'], [('D1', '12')])
        self.assertEqual(meta.sketch_parents(it)[95], 103)


@unittest.skipUnless(os.path.exists(RV17), 'reference file not present')
class TestRV17(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from sldprt.decode import decode_file
        cls.r = decode_file(RV17)

    def test_faces(self):
        self.assertEqual(len(self.r['faces']), 73)
        self.assertTrue(all(f['feature_first'] is not None for f in self.r['faces']))

    def test_hole_radius(self):
        hole = [f for f in self.r['faces'] if f['surface_type'] == 'cylinder' and 103 in f['feature_ids_by_time']]
        self.assertAlmostEqual(hole[0]['params']['radius'], 0.0016, places=9)

    def test_sketch1_dims(self):
        s = next(s for s in self.r['sketches'] if s['name'] == 'Sketch1')
        dm = {m['dim']: m['matches'] for m in s['dim_matches']}
        self.assertTrue(dm['D4'] and dm['D4'][0][3] == 'diameter')   # Ø11
        self.assertTrue(dm['D7'] and dm['D7'][0][3] == 'length')     # 9.6

    def test_mass_volume(self):
        mp = self.r['meta']['props']['mass_props']['SW-MassProp-Config-0']['interpretation']
        self.assertAlmostEqual(mp['volume_m3'] * 1e9, 1370.4, places=0)   # STEP INDEX vol=1370


if __name__ == '__main__':
    unittest.main()
