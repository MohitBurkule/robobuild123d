import os, sys, unittest, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r20'))


class _Sk: pass


class TestRound20(unittest.TestCase):
    def _seg(self, i, t, con, p0, p1, **k):
        import dump_parser as DP
        return DP.Seg(i, t, con, p0=p0, p1=p1, **k)

    def test_revolve_axes_prefers_own_construction_line(self):
        # flag-0 copies of profile lines ('a..') are not axes; the sketch's own construction line ('c..') is
        import decode_replay as D
        sk = _Sk(); sk.segs = [self._seg('0', 0, False, (0, 0, 0), (1, 0, 0)), self._seg('a1', 0, True, (0, 0, 0), (1, 0, 0)),
                               self._seg('c2', 0, True, (0.004, 0, 0), (0.004, 1, 0))]
        ax = D.OracleReplay.revolve_axes(sk)
        self.assertEqual([s.id for s in ax], ['c2'])

    def test_revolve_axes_fallback(self):
        import decode_replay as D
        sk = _Sk(); sk.segs = [self._seg('a1', 0, True, (0, 0, 0), (1, 0, 0))]
        self.assertEqual([s.id for s in D.OracleReplay.revolve_axes(sk)], ['a1'])

    def test_close_gaps_line(self):
        import decode_replay as D
        m = 1e-3   # segments are in metres
        S = [self._seg('0', 0, False, (0, 0, 0), (10 * m, 0, 0)), self._seg('1', 0, False, (10 * m, 0, 0), (10 * m, 5 * m, 0)),
             self._seg('2', 0, False, (10 * m, 5 * m, 0), (0, 5 * m, 0))]
        g = D.close_gaps(S)
        self.assertEqual(len(g), 1); self.assertEqual(g[0].type, 0)
        self.assertEqual({tuple(round(x / m, 6) for x in g[0].p0[:2]), tuple(round(x / m, 6) for x in g[0].p1[:2])}, {(0, 0), (0, 5)})

    def test_close_gaps_none_when_closed(self):
        import decode_replay as D
        m = 1e-3
        S = [self._seg('0', 0, False, (0, 0, 0), (1 * m, 0, 0)), self._seg('1', 0, False, (1 * m, 0, 0), (0, 1 * m, 0)),
             self._seg('2', 0, False, (0, 1 * m, 0), (0, 0, 0))]
        self.assertEqual(D.close_gaps(S), [])

    def test_close_gaps_concentric_arc(self):
        # ends 45 mm apart, both 35.35 mm from the centre of an existing arc: closed by a minor arc
        import decode_replay as D
        m = 1e-3; c = (-15.35 * m, -40 * m, 0)
        A = (-50.19 * m, -34 * m, 0); B = (-15.35 * m, (-40 + math.dist((-50.19, -34), (-15.35, -40))) * m, 0)
        S = [self._seg('0', 1, False, (-15.35 * m, 4.65 * m, 0), (-60 * m, -40 * m, 0), c=c, r=44.65 * m, dir=1),
             self._seg('1', 0, False, (-60 * m, -40 * m, 0), A), self._seg('2', 0, False, B, (-15.35 * m, 4.65 * m, 0))]
        g = D.close_gaps(S)
        self.assertEqual(len(g), 1); self.assertEqual(g[0].type, 1)
        self.assertAlmostEqual(g[0].r / m, math.dist((-50.19, -34), (-15.35, -40)), places=3)
        a0 = math.atan2(g[0].p0[1] - c[1], g[0].p0[0] - c[0]); a1 = math.atan2(g[0].p1[1] - c[1], g[0].p1[0] - c[0])
        self.assertLess((a1 - a0) % (2 * math.pi), math.pi)   # counter-clockwise minor arc

    def test_beam_upto(self):
        import decode_replay as D
        F = [_Sk() for _ in range(4)]
        for i, f in enumerate(F): f.name = f'f{i}'
        self.assertIsNone(D.beam_upto(F, [dict(feature='f1', status='OK')]))
        self.assertEqual(D.beam_upto(F, [dict(feature='f1', status='FAIL'), dict(feature='f2', status='OK')]), 1)
        self.assertEqual(D.beam_upto(F, [dict(feature='f1', status='OK')], 0.93), 4)   # no failure, low score
        os.environ['R20_BEAMALL'] = '1'
        try: self.assertEqual(D.beam_upto(F, []), 4)
        finally: del os.environ['R20_BEAMALL']


if __name__ == '__main__':
    unittest.main()
