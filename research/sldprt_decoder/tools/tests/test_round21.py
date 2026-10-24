import os, sys, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r21'))


def _dr():
    """wip_r21/decode_replay, whichever wip dir an earlier test module put first on sys.path."""
    import importlib.util
    if 'decode_replay_r21' in sys.modules: return sys.modules['decode_replay_r21']
    w = os.path.join(HERE, '..', 'wip_r21'); sys.path.insert(0, w)
    sp = importlib.util.spec_from_file_location('decode_replay_r21', os.path.join(w, 'decode_replay.py'))
    m = importlib.util.module_from_spec(sp); sys.modules['decode_replay_r21'] = m; sp.loader.exec_module(m)
    return m


class _S:
    def __init__(self, kind, **p): self.kind, self.params = kind, p


class TestRound21(unittest.TestCase):
    def test_order_chain(self):
        import importlib.util as _u; _s = _u.spec_from_file_location('chain_blend_r21', os.path.join(HERE, '..', 'wip_r21', 'chain_blend.py')); CB = _u.module_from_spec(_s); _s.loader.exec_module(CB)
        from build123d import Edge
        es = [Edge.make_line((0, 0, 0), (1, 0, 0)), Edge.make_line((2, 0, 0), (3, 0, 0)), Edge.make_line((1, 0, 0), (2, 0, 0))]
        o = CB.order_chain(es)
        self.assertEqual([round(e.center().X, 3) for e in o], [0.5, 1.5, 2.5])

    def test_components(self):
        import importlib.util as _u; _s = _u.spec_from_file_location('chain_blend_r21', os.path.join(HERE, '..', 'wip_r21', 'chain_blend.py')); CB = _u.module_from_spec(_s); _s.loader.exec_module(CB)
        from build123d import Edge
        es = [Edge.make_line((0, 0, 0), (1, 0, 0)), Edge.make_line((5, 0, 0), (6, 0, 0)), Edge.make_line((1, 0, 0), (1, 1, 0))]
        self.assertEqual(sorted(sorted(c) for c in CB.components(es)), [[0, 2], [1]])

    def test_variants_fillet_box(self):
        import importlib.util as _u; _s = _u.spec_from_file_location('chain_blend_r21', os.path.join(HERE, '..', 'wip_r21', 'chain_blend.py')); CB = _u.module_from_spec(_s); _s.loader.exec_module(CB)
        from build123d import Box
        b = Box(10, 10, 10); es = b.edges()[:3]
        tags = [t for t, nb in CB.variants(b, es, 1.0, 'fillet', b.volume)]
        self.assertIn('chain-ordered', tags)
        self.assertIn('per-edge', tags)

    def test_sequential_chamfer(self):
        import importlib.util as _u; _s = _u.spec_from_file_location('chain_blend_r21', os.path.join(HERE, '..', 'wip_r21', 'chain_blend.py')); CB = _u.module_from_spec(_s); _s.loader.exec_module(CB)
        from build123d import Box
        b = Box(10, 10, 10)
        nb = CB.sequential(b, b.edges()[:2], 1.0, 'chamfer', b.volume)
        self.assertIsNotNone(nb); self.assertLess(nb.volume, b.volume)

    def test_bend_radius_from_xt(self):
        D = _dr()
        rb = D.OracleReplay.__new__(D.OracleReplay)
        faces = [dict(surface_type='cylinder', params=dict(point=(0, 0, 0), axis=(0, 1, 0), radius=r)) for r in (0.0007366, 0.0022366, 0.006)]
        class G: pass
        rb.g = G(); rb.g.faces = faces
        self.assertAlmostEqual(rb.bend_radius(0.74, 1.5), 0.7366, 6)
        self.assertEqual(rb.bend_radius(0.74, 1.0), 0.74)   # no r + T partner: display value kept

    def test_sketch_feat_memo(self):
        # g.link consumes a sketch; a second lookup of the same feature (cloned state) must still find it
        D = _dr()
        class Sk: segs = [1]
        class SF: sketch = Sk()
        class G:
            def __init__(self): self.ec = {}; self.used = set()
            def link(self, n):
                if 'Sketch2' in self.used: return None
                self.used.add('Sketch2'); return 'Sketch2'
        class P: by_name = {'Sketch2': SF()}
        class F: name = 'Revolve4'; decoded = None
        rb = D.OracleReplay.__new__(D.OracleReplay); rb.g = G(); rb.part = P()
        self.assertIsNotNone(rb.sketch_feat(F)); self.assertIsNotNone(rb.sketch_feat(F))

    def test_k_defer(self):
        D = _dr()
        os.environ['R21_DK'] = '3'
        try: self.assertEqual(D.K_DEFER(), 4)
        finally: del os.environ['R21_DK']


if __name__ == '__main__':
    unittest.main()
