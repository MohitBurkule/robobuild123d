import json, os, unittest
from sldprt import item_pattern, item_endcond
D = os.path.join(os.path.dirname(__file__), '..', '..', 'decoded')
def load(p): return json.load(open(os.path.join(D, p + '.json')))

class T(unittest.TestCase):
    def test_rv01_mirrors_right_plane(self):
        d = load('RV01 Chassis')
        for m in ('Mirror2', 'Mirror7', 'Mirror8'):
            fid = next(f['id'] for f in d['features'] if f['name'] == m)
            r = item_pattern.mirror_plane(d['faces'], fid)
            self.assertEqual(r['ref'], 'Right Plane'); self.assertEqual(r['confidence'], 'high')
    def test_rv15_linear_pitch(self):
        d = load('RV15 BBB Antweight Switch'); f = next(f for f in d['features'] if f['name'] == 'LPattern1')
        r = item_pattern.pattern(d['faces'], f['id'], f)
        self.assertIn([0.6, 0.0, 0.0], [[abs(x) for x in v] for v in r['common_offsets_mm']])
    def test_endcond_offset_and_midplane(self):
        r = item_endcond.classify(load('RV01 Chassis'))
        self.assertTrue(any('offset_from_surface(2mm)' in c for c in r['Cut-Extrude2']['class']))
        r = item_endcond.classify(load('RV04 Drisk spacer'))
        self.assertTrue(r['Boss-Extrude1']['class'][0].startswith('midplane'))
if __name__ == '__main__': unittest.main()
