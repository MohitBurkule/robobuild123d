import os, sys, unittest
import numpy as np
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r15'))
from sldprt import displaylist as DL

REV = os.path.join(HERE, '../../revdev/')


class TestRound15DisplayList(unittest.TestCase):
    def test_strip_mesh_volume(self):
        # final-body display mesh (Contents/DisplayLists, triangle strips) vs the reference volumes
        self.assertAlmostEqual(DL.volume(DL.triangles(REV + 'fork 5.SLDPRT')), 150.8, delta=0.3)
        self.assertAlmostEqual(DL.volume(DL.triangles(REV + 'RV15 BBB Antweight Switch.SLDPRT')), 329.8, delta=0.5)
        self.assertAlmostEqual(DL.volume(DL.triangles(REV + 'RV01 Chassis.SLDPRT')), 15714.6, delta=5)

    def test_extent_is_model_frame(self):
        T = DL.triangles(REV + 'fork 5.SLDPRT').reshape(-1, 3)
        np.testing.assert_allclose(T.min(0), [-26.0, -4.3, 0.0], atol=0.01)

    def test_no_display_mesh(self):
        self.assertIsNone(DL.triangles(REV + 'Top Panel.SLDPRT'))


class TestRound15MirrorDerived(unittest.TestCase):
    def test_mirror_plane_fit(self):
        import mirror_derived as MD
        self.assertEqual(MD.source_of('RV18 Wedgelet RH'), 'RV17 Wedgelet LH')
        sc, n, d = MD.fit_plane('RV17 Wedgelet LH', 'RV18 Wedgelet RH')
        self.assertGreater(sc, 0.99)
        np.testing.assert_allclose(np.abs(n), [0, 0, 1]); self.assertAlmostEqual(d, 0.0)


class TestRound15XTMesh(unittest.TestCase):
    def test_fin_vertices(self):
        # decoded start_vertex of fin i is the end of fin i (fork 5 hub cylinder face)
        import json, xt_mesh as X
        J = json.load(open(os.path.join(HERE, '../../decoded/fork 5.json')))
        f = next(f for f in J['faces'] if f['surface_type'] == 'cylinder' and len(f['loops'][0]['edges']) == 4)
        ends = X.loop_ends(f['loops'][0])
        for (e, a, b), (e2, a2, b2) in zip(ends, ends[1:] + ends[:1]):
            self.assertEqual(b, a2)

    def test_uv_planar_face_with_holes(self):
        import json, xt_mesh as X
        J = json.load(open(os.path.join(HERE, '../../decoded/fork 5.json')))
        X.orient_arcs(J)
        f = next(f for f in J['faces'] if f['surface_type'] == 'plane' and len(f['loops']) == 4 and f['params']['point'][2] > 0.001)
        T = np.array(X.uv_mesh(f))
        area = 0.5 * np.linalg.norm(np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0]), axis=1).sum()
        self.assertAlmostEqual(area, 100.48, delta=1.0)    # dump FACE area 1.00485e-4 m2


if __name__ == '__main__':
    unittest.main()
