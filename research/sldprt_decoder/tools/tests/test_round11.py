import sys, os, unittest
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import item_fr


class FR(unittest.TestCase):
    def test_match(self):
        import struct
        d = struct.pack('<HIIiii', 5, 58, 1713131669, 3, -1, 0)
        class E: name = 'moFR_c'
        r = item_fr.decode(d, [(E, 0, len(d))])
        self.assertEqual(r[0]['path'], [3, -1, 0])
        item_fr.match_atoms(r, [(83, 58, 1713131669, 0, 3, -1, 0)])
        self.assertTrue(r[0]['stamp_ok']); self.assertEqual(r[0]['atom'][4], 3)


if __name__ == '__main__':
    unittest.main()
