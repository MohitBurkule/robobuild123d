import os
import struct
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sldprt import item_relations as IR  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def rec(t, slots):
    b = struct.pack('<IHHHHH', t, 2, 0, 0, 0xFFFE, 0)
    for tag, i in slots:
        b += struct.pack('<HHiI', tag, i, -1, 0)
    return b + b'\x00' * 40


class TestRelations(unittest.TestCase):
    def test_record_parse(self):
        d = b'\x00' * 8 + rec(4, [(0x80F2, 3)]) + rec(9, [(0x80E7, 1), (0x80F2, 2)])
        r = IR.relation_records(d, 0, len(d))
        self.assertEqual([x['type_code'] for x in r], [4, 9])
        self.assertEqual(r[1]['slots'], [(0x80E7, 1), (0x80F2, 2)])

    def test_inline_classdef_slot(self):
        d = struct.pack('<IHHHHH', 17, 2, 0, 0, 0xFFFE, 0) + b'\xff\xff\x01\x00\x0d\x00sgPointHandle' + \
            struct.pack('<HiI', 0, -1, 0) + b'\x00' * 30
        self.assertEqual(IR.relation_records(d, 0, len(d))[0]['slots'], [('sgPointHandle', 0)])

    def test_verify(self):
        L = {'kind': 'line', 'a': (0, 1), 'b': (2, 1)}
        P = {'kind': 'point', 'p': (1, 1)}
        A = {'kind': 'arc', 'c': (1, 2), 'r': 1.0}
        self.assertTrue(IR.verify(4, [L]))
        self.assertFalse(IR.verify(5, [L]))
        self.assertTrue(IR.verify(12, [P, L]))
        self.assertTrue(IR.verify(9, [L, P]))
        self.assertTrue(IR.verify(6, [A, L]))

    @unittest.skipUnless(os.path.exists(os.path.join(ROOT, 'revdev', 'RV17 Wedgelet LH.SLDPRT')), 'data')
    def test_rv17_horizontal_vertical(self):
        o = IR.decode_part(os.path.join(ROOT, 'revdev', 'RV17 Wedgelet LH.SLDPRT'),
                           os.path.join(ROOT, 'decoded', 'RV17 Wedgelet LH.json'))
        hv = [r['verified'] for s in o['sketches'] for r in s['relations'] if r['type_code'] in (4, 5, 25, 26)]
        ok = sum(1 for v in hv if v)
        bad = sum(1 for v in hv if v is False)
        self.assertGreater(ok, 70)
        self.assertGreater(ok, 8 * bad)


if __name__ == '__main__':
    unittest.main()
