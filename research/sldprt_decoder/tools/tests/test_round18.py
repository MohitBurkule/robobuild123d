import os, sys, unittest, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r18'))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


class TestRound18(unittest.TestCase):
    def test_plane_records_match_dumps(self):
        # every plane_rec / refplane_rec sketch frame of RV17 equals the dump SKETCH_TO_MODEL;
        # the wrong frames are all identity_default (no record found)
        import plane_audit as PA
        rows = PA.audit_sp('RV17 Wedgelet LH')
        self.assertTrue(rows)
        for r in rows:
            if r[1] in ('plane_rec', 'refplane_rec'): self.assertEqual(r[2], 'ok', r)
        self.assertTrue(any(r[1] == 'identity_default' and r[2] != 'ok' for r in rows))

    def test_span_pairs(self):
        import decode_replay as D
        # RV21 Cut-Extrude2: D = 11, planes at -8.5 and 2.5 from the sketch -> (-8.5, 2.5)
        self.assertIn((-8.5, 2.5), D.span_pairs([-8.5, 0.0, 2.5, 4.0], 11.0))
        self.assertEqual(D.span_pairs([0.0, 3.0], 11.0), [])

    def test_sheet_thickness(self):
        import decode_replay as D
        d = json.load(open(os.path.join(ROOT, 'decoded_corpus', 'Steel ring.json')))
        self.assertAlmostEqual(D.sheet_thickness(d), 1.5)
        self.assertIsNone(D.sheet_thickness({'features': [{'type': 'Boss-Extrude', 'dims': [['D1', '3']]}]}))

    def test_fmargin(self):
        import decode_replay as D
        class S: pass
        s = S(); s._cur_doubt = False
        f = D.OracleReplay.fmargin
        self.assertLess(f(s, 'decoded reg=0.2', 'top-revy@0 reg=0.2'), 1e-6)      # decoded may retake the lead
        self.assertGreaterEqual(f(s, 'top-revy@0 reg=0.2', 'decoded reg=0.2'), 2e-3)  # record-backed: alternatives need a margin
        s._cur_doubt = True
        self.assertAlmostEqual(f(s, 'front@17 reg=1.0', 'decoded reg=0.1'), 2e-4)

    def test_crash_policy(self):
        import run_all as RA
        c, sk = {}, []
        RA.crash_policy(c, sk, 'Fillet1'); self.assertEqual(sk, [])
        RA.crash_policy(c, sk, 'Fillet1'); self.assertEqual(sk, ['Fillet1'])

    def test_gear_feature_stream(self):
        # Toolbox gear parts: the feature stream is found (it has no moSketch_c)
        from sldprt import streams as S
        L = S.all_streams(open(os.path.join(ROOT, 'corpus', 'gear2.SLDPRT'), 'rb').read())
        self.assertTrue(any(S.classify(s) == 'features' for s in L))

    def test_forked_blend_isolates_crash(self):
        # an OCC call that segfaults in the forked child becomes an exception in the parent
        import decode_replay as D, signal
        from build123d import Box
        crash = D._forked(lambda self: os.kill(os.getpid(), signal.SIGSEGV), 'test')
        with self.assertRaises(RuntimeError): crash(None)
        ok = D._forked(lambda self, a: Box(a, a, a), 'test')
        self.assertAlmostEqual(ok(None, 2.0).volume, 8.0, places=6)

    def test_forked_fillet_installed(self):
        import decode_replay as D
        from build123d import Box
        from build123d.topology import Mixin3D
        self.assertTrue(getattr(Mixin3D.fillet, '_r18', False))
        b = Box(10, 10, 10); r = b.fillet(1.0, b.edges()[:1])
        import math; self.assertAlmostEqual(r.volume, 1000.0 - (1 - math.pi / 4) * 10.0, places=4)

    def test_edge_hints_fork5(self):
        sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
        from sw_gen import model as SWM
        H = SWM.parse_edges(os.path.join(ROOT, 'dumps_v4_edges', 'fork 5.edges.txt'))
        self.assertIn('Fillet1', H); self.assertGreaterEqual(len(H['Fillet1']), 1)


if __name__ == '__main__':
    unittest.main()
