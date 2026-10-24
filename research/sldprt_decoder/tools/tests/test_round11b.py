import os, sys, struct, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sldprt import item_structs as IS, item_fr as IF


class TestRound11b(unittest.TestCase):
    def test_cstring(self):
        b = b'\xff\xfe\xff\x02' + 'Hi'.encode('utf-16-le')
        self.assertEqual(IS.cstring(b, 0, len(b)), ('Hi', len(b)))

    def test_fr_full(self):
        b = struct.pack('<HIIiii', 8, 73, 1707330610, 9, -1, 0)
        end, f = IS.fr_full(b, 0, len(b), {73})
        self.assertEqual(f['path'], [9, -1, 0]); self.assertEqual(end, 22)
        self.assertIsNone(IS.fr_full(b + b'\0\0', 0, len(b) + 2, {73}))

    def test_hist_display(self):
        b = b'\x02\x00' + b'\0' * 5 + struct.pack('<II', 101, 0) + b'\0' * 28 + b'\xff' * 16 + b'\0' * 18 \
            + struct.pack('<f', 58.0) + b'\0\0' + struct.pack('<II', 541, 1710100970)
        end, f = IS.hist_display(b, 0, len(b), {541})
        self.assertEqual((end, f['feature_id'], f['a']), (91, 541, 101))

    def test_named_item(self):
        b = b'\xff\xfe\xff\x01' + 'A'.encode('utf-16-le') + struct.pack('<diI', 2.0, -1, 0) + b'\xff\xfe\xff\x00' + b'\0\0' + struct.pack('<d', 0.25)
        end, f = IS.named_item(b, 0, len(b), set())
        self.assertEqual((f['name'], f['value'], end), ('A', 0.25, len(b)))

    def test_chain_triples(self):
        v = [59, 109, 1658478240, 0, 124, 108, 1658478224, 0, 2, 0, 74, 97, 1658478021, 0, 2]
        self.assertIn((109, 1658478240, 124), IF.chain_triples(v))
        self.assertIn((97, 1658478021, 2), IF.chain_triples(v))


if __name__ == '__main__':
    unittest.main()
