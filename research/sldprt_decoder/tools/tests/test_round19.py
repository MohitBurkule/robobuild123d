import os, sys, unittest, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r19'))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


class _S: pass


class TestRound19(unittest.TestCase):
    def test_rank_alts(self):
        # beam alternatives: greedy choice first, distinct others by score, plus the best every-cell candidate
        import decode_replay as D
        import numpy as np
        s = _S(); a, b = object(), object(); n = np.array([0, 0, 1.0])
        c = lambda sc, cells, ivs, how='uniform': (sc, 'decoded', [(x, n, ivs) for x in cells], None, 2, None, how, (None, None), 0.0)
        best = c(0.9, [a], [(0, 3)])
        s._ecands = [best, c(0.9, [a], [(0, 3)]), c(0.8, [a], [(0, 5)]), c(0.7, [a, b], [(0, 3)]), c(0.5, [a, b], [(0, 5)], 'all')]
        out = D.OracleReplay.rank_alts(s, best, K=3)
        self.assertIs(out[0], best)
        self.assertEqual(len(out), 4)
        self.assertEqual(out[-1][6], 'all')
        self.assertEqual(len({str(x[2]) for x in out}), 4)   # all distinct

    def test_rank_alts_after_fail(self):
        # a feature the greedy step skips (best None) still offers its candidates to the beam
        import decode_replay as D
        import numpy as np
        s = _S(); s._ecands = [(0.3, 'decoded', [(object(), np.array([0, 0, 1.0]), [(0, 1)])], None, 1, None, 'all', (None, None), 0.0)]
        out = D.OracleReplay.rank_alts(s, None, K=3)
        self.assertIsNone(out[0]); self.assertEqual(len(out), 2)

    def test_clone_independent(self):
        import decode_replay as D
        import numpy as np
        s = D.OracleReplay.__new__(D.OracleReplay)
        s.bin = np.zeros(4, bool); s.tools = {}; s.choice = {}; s.order = []; s.cutvox = {}; s.cutman = {}; s.ftime = {}
        c = s.clone(); c.bin[0] = True; c.order.append('x'); c.tools['a'] = 1
        self.assertFalse(s.bin[0]); self.assertEqual(s.order, []); self.assertEqual(s.tools, {})

    def test_repair_multisolid(self):
        # two boxes touching along an edge (RV24 / side panel): not watertight as one mesh,
        # the per-solid repair gives the union volume
        import decode_replay as D
        from build123d import Box, Pos, Compound
        A = Box(1, 1, 1); B = Pos(1, 1, 0) * Box(1, 1, 1)
        M = D.OracleReplay.repair_mf(Compound([A, B]))
        self.assertIsNotNone(M)
        self.assertAlmostEqual(M.volume(), 2.0, places=3)

    def test_crash_counter(self):
        import decode_replay as D, signal
        c0 = D._CRASHES
        crash = D._forked(lambda self: os.kill(os.getpid(), signal.SIGSEGV), 'test')
        with self.assertRaises(RuntimeError): crash(None)
        self.assertEqual(D._CRASHES, c0 + 1)

    def test_gear_dims(self):
        import decode_replay as D
        s = _S(); s.g = _S(); s.g.d = json.load(open(os.path.join(ROOT, 'decoded_corpus', 'gear 38t.json')))
        dd = D.OracleReplay.gear_dims(s)
        self.assertEqual(int(dd['TeethCuts']['Num_teeth']), 38)
        self.assertAlmostEqual(dd['BasProSke']['Diameter'], 16.0)
        self.assertAlmostEqual(dd['TooCutSke']['Base_dia'], 14.283)

    def test_sheet_metal_dims(self):
        d = json.load(open(os.path.join(ROOT, 'decoded_corpus', 'lift.json')))
        import decode_replay as D
        self.assertAlmostEqual(D.sheet_thickness(d), 1.0)
        ef = next(f for f in d['features'] if f['type'] == 'Edge-Flange')
        dd = dict(ef['dims']); self.assertEqual(D.num(dd['D7']), 50.0); self.assertEqual(D.num(dd['D4']), 90.0)

    def test_region_parity(self):
        # even-odd fill of the selected loops: a square with a circular hole
        import decode_replay as D
        sq = [D.DP.Seg(str(i), 0, False, p0=a, p1=b) for i, (a, b) in enumerate([((0, 0, 0), (0.01, 0, 0)), ((0.01, 0, 0), (0.01, 0.01, 0)),
                                                                             ((0.01, 0.01, 0), (0, 0.01, 0)), ((0, 0.01, 0), (0, 0, 0))])]
        ci = D.DP.Seg('c', 1, False, p0=(0.007, 0.005, 0), p1=(0.007, 0.005, 0), c=(0.005, 0.005, 0), r=0.002, dir=1)
        P = D.OracleReplay.parity_inside
        self.assertTrue(P(sq + [ci], (1.0, 1.0)))      # in the square, outside the hole
        self.assertFalse(P(sq + [ci], (5.0, 5.0)))     # in the hole
        self.assertFalse(P(sq + [ci], (15.0, 5.0)))    # outside
        self.assertTrue(P([ci], (5.0, 5.0)))           # the circle alone


if __name__ == '__main__':
    unittest.main()
