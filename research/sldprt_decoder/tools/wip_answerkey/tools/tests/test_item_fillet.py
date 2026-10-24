import json, os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sldprt import item_fillet as I

R = os.path.join(os.path.dirname(os.path.dirname(HERE)))


def _run(p):
    s = os.path.join(R, 'revdev', p + '.SLDPRT')
    j = os.path.join(R, 'decoded', p + '.json')
    if not (os.path.exists(s) and os.path.exists(j)):
        raise unittest.SkipTest('data missing')
    from sldprt import streams as S
    data = open(s, 'rb').read()
    feat = max((x['data'] for x in S.all_streams(data) if S.classify(x) == 'features'), key=len)
    return I.decode(feat, json.load(open(j)))


class T(unittest.TestCase):
    def test_dim_regex(self):
        import struct
        b = (b'\xff\xfe\xff\x02D\x001\x00' + b'\x00' * 7 + b'\x40\xff\xff\xff\xff' + b'\x00' * 4 +
             b'\xff\xfe\xff\x00\x00\x00' + struct.pack('<d', 0.003) + b'\x00\x00\x00' + struct.pack('<I', 166))
        d = I.dims_in(b, 0, len(b))
        self.assertEqual((d[0]['name'], d[0]['value'], d[0]['dim_id']), ('D1', 0.003, 166))

    def test_values_match_keywords(self):
        for p in ('RV01 Chassis', 'RV17 Wedgelet LH', 'RV23 side panel LH'):
            r = _run(p)
            self.assertTrue(r)
            self.assertTrue(all(x['matches_keywords'] for x in r), p)

    def test_rv01_fillet1_edges(self):
        r = {x['name']: x for x in _run('RV01 Chassis')}
        f = r['Fillet1']
        self.assertEqual(f['radius_m'], 0.003)
        self.assertTrue(f['parasolid_radius_match'])
        self.assertEqual(f['n_items_from_radius_copies'], 2)
        self.assertEqual(sorted(sorted(e['parasolid_faces']) for e in f['selected_edges']), [[167, 334], [305, 336]])
        self.assertEqual(r['Chamfer1']['chamfer_type'], 'angle-distance')
        self.assertAlmostEqual(r['Chamfer1']['angle_deg'], 45.0, 6)


if __name__ == '__main__':
    unittest.main()
