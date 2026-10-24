import os, sys, json, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, '..', 'wip_r22')


def _load(name, fn):
    import importlib.util
    if name in sys.modules: return sys.modules[name]
    if W not in sys.path: sys.path.insert(0, W)
    sp = importlib.util.spec_from_file_location(name, os.path.join(W, fn))
    m = importlib.util.module_from_spec(sp); sys.modules[name] = m; sp.loader.exec_module(m)
    return m


def _dr(): return _load('decode_replay_r22', 'decode_replay.py')


class _St:
    """stub final state for OracleReplay.better: (face fraction, IoU)."""
    def __init__(self, F, io):
        self.body = object(); self._fk = (F, io)
    def beam_key(self, final=False): return self._fk[0] + 0.2 * self._fk[1]


class TestRound22(unittest.TestCase):
    def test_better_face_first_with_iou_guard(self):
        D = _dr(); b = D.OracleReplay.better
        self.assertTrue(b(_St(0.60, 0.90), _St(0.50, 0.905)))     # more faces, IoU within the guard
        self.assertFalse(b(_St(0.60, 0.85), _St(0.50, 0.90)))     # more faces but loses > 0.02 IoU
        self.assertTrue(b(_St(0.50, 0.97), _St(0.51, 0.90)))      # much better IoU at about the same faces
        self.assertFalse(b(_St(0.40, 0.91), _St(0.50, 0.90)))

    def test_open_ends(self):
        D = _dr()
        S = D.DP.Seg
        segs = [S('a', 0, False, (0, 0, 0), (0, 1, 0)), S('b', 0, False, (0, 1, 0), (1, 1, 0)), S('c', 0, False, (0, 0, 0), (2, 0, 0))]
        e = sorted(tuple(round(x, 6) for x in p[:2]) for p in D.open_ends(segs))
        self.assertEqual(e, [(1.0, 1.0), (2.0, 0.0)])

    def test_e9_dir2_intervals(self):
        D = _dr()
        rb = D.OracleReplay.__new__(D.OracleReplay)
        rb.plane_offsets = lambda o, n: []; rb.two_dir = lambda F: None
        class F: faces = []; name = 'Cut-Extrude21'
        ivs = rb.intervals(F, 'cut', __import__('numpy').zeros(3), __import__('numpy').array([0, 1.0, 0]), None, None, 9, None)
        self.assertIn([(-D.BIG, D.BIG)], [[tuple(x) for x in v] for v in ivs])

    def test_minor_arc_edge(self):
        XO = _load('xt_oracle_r22', 'xt_oracle.py')
        import numpy as np
        e = {'edge': -1, 'fin_sense': '+', 'curve': {'type': 'circle', 'centre': [0, 0, 0], 'normal': [0, 0, 1], 'x_axis': [1, 0, 0], 'radius': 0.001}}
        E, _ = XO._edge(e, [0.001, 0, 0], [0, 0.001, 0])
        from build123d import Edge
        self.assertAlmostEqual(Edge(E).length, np.pi / 2, places=4)      # quarter arc (mm), not three quarters

    def test_offset_blend_box(self):
        CB = _load('chain_blend_r22', 'chain_blend.py')
        from build123d import Box
        b = Box(10, 10, 10); es = [e for e in b.edges() if abs(e.center().Z - 5) < 1e-6][:1]
        nb = CB.offset_blend(b, es, 1.0, b.volume)
        self.assertIsNotNone(nb)
        self.assertAlmostEqual(b.volume - nb.volume, 10 * (1 - np.pi / 4) if False else 10 * (1 - 3.141592653589793 / 4), delta=0.7)

    def test_xt_oracle_agrees_fs8(self):
        # decode-only XT face oracle reproduces every patch of a body built to match (FS8, R21 brep)
        bp = os.path.join(HERE, '..', 'wip_r21', 'breps', 'FS8.brep')
        if not os.path.exists(bp): self.skipTest('no r21 brep')
        D = _dr(); XO = _load('xt_oracle_r22', 'xt_oracle.py')
        from build123d import import_brep
        d = json.load(open(os.path.join(D.DO.DEC, 'FS8.json')))
        X = XO.xt_faces(d)
        self.assertEqual(XO.count(X, import_brep(bp)), XO.n_patches(X))


if __name__ == '__main__':
    unittest.main()
