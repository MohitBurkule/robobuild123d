import os, sys, unittest
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r16'))
ROOT = os.path.join(HERE, '..', '..')


class TestRound16(unittest.TestCase):
    def test_corpus_dump_features(self):
        import corpus_check as CC
        f = CC.dump_features(os.path.join(ROOT, 'dumps_corpus', '10mm standoff 3m alu.dump.txt'))
        self.assertTrue(f and all(t not in ('RefPlane', 'ProfileFeature') for n, t in f))

    def test_face_gate_identity(self):
        # face audit of a dump against itself-derived faces: every patch matches
        sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
        import face_audit as FA
        d = FA.faces_from_dump(os.path.join(ROOT, 'dumps_v2', 'fork 5.dump.txt'))
        r = FA.audit(d, d)
        self.assertEqual(r['counts']['matched'], r['counts']['dump_patches'])

    def test_lookahead_suffix(self):
        # don't-care mask for feature k = union of masks of cuts strictly after k
        src = open(os.path.join(HERE, '..', 'wip_r16', 'decode_replay.py')).read()
        self.assertIn("suf[k + 1] = acc", src); self.assertIn("rin0 | self._suf[k + 1]", src)


if __name__ == '__main__':
    unittest.main()
