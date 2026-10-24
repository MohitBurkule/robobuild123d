"""Per-record-type tests for the structural layer (container, XT nodes, schema delta, MFC)."""
import os
import struct
import sys
import unittest
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from sldprt import container as C, xt_struct as X, mfc  # noqa: E402

NULL = bytes.fromhex('c2bc928f996e0000')
P = lambda *v: struct.pack('>%dH' % len(v), *v)
I = lambda v: struct.pack('>i', v)
D = lambda *v: struct.pack('>%dd' % len(v), *v)


class TestContainer(unittest.TestCase):
    def test_section(self):
        pay = b'hello world' * 10
        comp = zlib.compressobj(9, zlib.DEFLATED, -15)
        cd = comp.compress(pay) + comp.flush()
        name = C.rol4(b'Contents/Test')
        hdr = C.HDR.pack(C.MAGIC, 8, 0, zlib.crc32(pay), len(cd), len(pay), len(name))
        blob = b'\x00' * 7 + hdr + name + cd + b'\x01' * 5
        secs, gaps = C.parse(blob)
        self.assertEqual(len(secs), 1)
        self.assertEqual(secs[0].name, 'Contents/Test')
        self.assertTrue(secs[0].crc_ok)
        self.assertEqual(gaps, [(0, 7), (len(blob) - 5, len(blob))])


class TestXTRecords(unittest.TestCase):
    def _one(self, b, name):
        r = X.parse_record(b + P(14), 0)
        self.assertIsNotNone(r)
        self.assertEqual(r.name, name)
        self.assertEqual(r.end, len(b))
        return r

    def test_face(self):
        b = P(14, 100) + I(7) + P(1) + NULL + P(2, 3, 4, 11, 50) + b'+' + P(1, 1, 2, 3, 4)
        r = self._one(b, 'FACE')
        self.assertEqual(r.fields[7], 50)

    def test_edge_vertex_point(self):
        self._one(P(16, 5) + I(1) + P(1) + NULL + P(6, 1, 1, 7, 1, 1, 3), 'EDGE')
        self._one(P(18, 8) + I(1) + P(1, 9, 1, 1, 10) + NULL + P(3), 'VERTEX')
        self._one(P(29, 10) + I(1) + P(1, 8, 1, 1) + D(0.001, 0.002, 0.003), 'POINT')

    def test_loop_fin(self):
        self._one(P(15, 20) + I(1) + P(1, 21, 100, 1), 'LOOP')
        self._one(P(17, 21) + P(1, 20, 21, 21, 1, 22, 5, 1, 1) + b'-', 'FIN')

    def test_surfaces_curves(self):
        self._one(P(50, 30) + I(1) + P(1, 1, 1, 1, 1) + b'+' + D(0, 0, 0, 0, 0, 1, 1, 0, 0), 'PLANE')
        self._one(P(51, 31) + I(1) + P(1, 1, 1, 1, 1) + b'+' + D(0, 0, 0, 0, 0, 1, 0.002, 1, 0, 0), 'CYLINDER')
        self._one(P(30, 32) + I(1) + P(1, 1, 1, 1, 1) + b'+' + D(0, 0, 0, 1, 0, 0), 'LINE')
        self._one(P(31, 33) + I(1) + P(1, 1, 1, 1, 1) + b'+' + D(0, 0, 0, 0, 0, 1, 1, 0, 0, 0.003), 'CIRCLE')

    def test_variable_nodes(self):
        r = self._one(P(82) + struct.pack('>I', 3) + P(40) + struct.pack('>3i', 1, 2, 3), 'INT_VALUES')
        self.assertEqual(r.var, [1, 2, 3])
        r = self._one(P(81) + struct.pack('>I', 2) + P(41) + I(5) + P(30, 21, 1, 1, 1, 1) + P(40, 1), 'ATTRIBUTE')
        self.assertEqual(r.var, [40, 1])

    def test_ff_first_occurrence(self):
        b = P(29) + b'\xff' + P(10) + I(1) + P(1, 8, 1, 1) + D(0, 0, 0)
        self._one(b, 'POINT')

    def test_delta(self):
        blob = b'\x07CCCCCDI\x0clegal_owners\x00\x00\x00\x11\x01lCZ'
        delta, end = X.parse_delta(blob, 0)
        self.assertEqual(end, len(blob))
        self.assertEqual(delta['n_base'], 7)
        self.assertEqual(delta['ops'][6], ('I', 'legal_owners', 0, 17, 'l'))

    def test_walk_gap_reported(self):
        good = P(29, 10) + I(1) + P(1, 8, 1, 1) + D(0, 0, 0)
        blob = b'PS\x00\x00 \x05SCH_1' + good + b'\x00\x01\x56' + P(29, 11) + I(1) + P(1, 8, 1, 1) + D(0, 0, 0)
        nodes, gaps, cov, unk = X.walk(blob)
        self.assertEqual([n.index for n in nodes], [10, 11])
        self.assertEqual(len(gaps), 1)
        self.assertLess(cov, 100)


class TestMFC(unittest.TestCase):
    def test_classdef_cstring_dim(self):
        b = (b'\xff\xff\x01\x00\x0d\x00moExtrusion_c' + b'\xff\xfe\xff\x02' + 'D1'.encode('utf-16-le')
             + b'\x00' * 8 + b'\x40' + b'\xff' * 4 + b'\x00' * 4 + b'\xff\xfe\xff\x00\x00\x00' + struct.pack('<d', 0.0018))
        r = mfc.scan(b)
        self.assertEqual(r['records']['ClassDef'], 1)
        self.assertGreaterEqual(r['records']['CString'], 1)
        dv = mfc.dim_values(b)[0]
        self.assertAlmostEqual(dv.value['value'], 0.0018)


if __name__ == '__main__':
    unittest.main()


class TestEndSpec(unittest.TestCase):
    def test_form_a_depth(self):
        import struct
        from sldprt import mo_classes as M
        b = bytearray(800); b[0:4] = b'\x2d\x82\x00\x00'; b[4] = 1; b[26:28] = b'\xd5\x81'
        struct.pack_into('<d', b, 733, 0.012)
        x = M.parse_endspec(bytes(b), 0)
        assert x.form == 'A_blind' and abs(x.depth_m - 0.012) < 1e-12 and not x.dir2
