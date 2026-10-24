import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sldprt import item_sketchplane as I  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(HERE))


class TestSketchPlane(unittest.TestCase):
    def test_inverse_convention(self):
        # stored model->sketch block for a sketch on the Right plane (rotation about Y)
        T = (0, 0, 1, 0, 1, 0, -1, 0, 0, 0, 0, -0.0215)
        M = I.stored_to_sketch2model(T)
        self.assertEqual(M[6:9], (1.0, 0.0, 0.0))       # normal = +X
        self.assertAlmostEqual(M[9], 0.0215)              # origin x = -(R t)_x

    def test_classify(self):
        f = b'\x00' * 30 + b'\x01\x00\x01' + b'\x00' * 100
        self.assertEqual(I.classify(f, 33), 'annotation')
        self.assertEqual(I.classify(f, None), 'identity_default')

    def _part(self, name):
        p = os.path.join(ROOT, 'revdev', name + '.SLDPRT')
        j = os.path.join(ROOT, 'decoded', name + '.json')
        if not (os.path.exists(p) and os.path.exists(j)):
            self.skipTest('data missing')
        return I.decode_part(p, j)

    def test_rv09_circles_on_cylinders(self):
        t = self._part('RV09 Prop spacer')['totals']
        self.assertEqual(t['arcs_hit'], 2)

    def test_rv01_matchable_arcs(self):
        t = self._part('RV01 Chassis')['totals']
        self.assertGreaterEqual(t['arcs_hit'], 76)   # old row reading gave 62


if __name__ == '__main__':
    unittest.main()
