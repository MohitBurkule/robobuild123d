import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sldprt.item_mates import decode_asm_mates, stats  # noqa: E402

ROOT = os.path.join(HERE, '..', '..')
ASM = os.path.join(ROOT, 'revdev', 'rvrn 2.0.SLDASM')
DEC = os.path.join(ROOT, 'decoded')


@unittest.skipUnless(os.path.exists(ASM), 'assembly not present')
class TestMates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = decode_asm_mates(ASM, DEC)
        cls.m = {m['name']: m for m in cls.r['mates']}

    def test_count_and_group(self):
        self.assertEqual(len(self.r['mates']), 112)
        self.assertEqual(self.r['mate_groups'][0]['name'], 'Mates')
        self.assertEqual(self.r['mate_groups'][0]['NumberMates'], 112)

    def test_alignment_flag_matches_geometry(self):
        s = stats(self.r)
        a, b = s['alignment_flag_vs_geometry'].split('/')
        self.assertEqual(a, b)
        self.assertGreater(int(b), 90)

    def test_concentric_axes_coincide(self):
        m = self.m['Concentric3']
        self.assertTrue(m['geometric_check'])
        self.assertEqual(m['alignment'], 'aligned')

    def test_coincident_anti(self):
        m = self.m['Coincident17']
        self.assertEqual(m['alignment'], 'anti-aligned')
        self.assertLess(abs(m['residual_m']), 1e-9)

    def test_distance_values(self):
        self.assertAlmostEqual(self.m['Distance3']['value'], 0.003, 9)
        self.assertAlmostEqual(self.m['Distance3']['measured_m'], 0.003, 9)
        self.assertAlmostEqual(self.m['Distance2']['measured_m'], 0.0005, 9)

    def test_face_match(self):
        e = self.m['Coincident17']['entities'][0]
        self.assertEqual(e['instance_current'][0], 'RV01 Chassis-1')
        self.assertTrue(e['face_match'])


if __name__ == '__main__':
    unittest.main()
