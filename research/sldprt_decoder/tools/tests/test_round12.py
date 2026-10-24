import os, sys, struct, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sldprt import objnum as ON, fstream as FS, answer_key as AK, validate as V

AB = os.path.join(os.path.dirname(__file__), '../../dumps_ab/')


class TestRound12(unittest.TestCase):
    def test_pbud_struct(self):
        cls = 0x101
        b = struct.pack('<H', 0x8000 | cls) + struct.pack('<dd', 0.0055, -0.01) + b'\0\0'
        self.assertTrue(ON._struct_ok(b, 0, {cls: 'moPointBackedUpData_c'}))
        self.assertFalse(ON._struct_ok(b[:-2] + b'\1\0', 0, {cls: 'moPointBackedUpData_c'}))
        self.assertFalse(ON._struct_ok(b, 0, {cls: 'moFR_c'}))

    def test_dump_dim_suffix(self):
        self.assertEqual(AK._f('0.01 driven=2 type=2'), 0.01)
        self.assertEqual(AK._f('True'), 1.0)

    def test_plane_ref_variants(self):
        for lead in (b'\x68\x42', b'\x50\x46', b'\x00\x00'):
            b = b'\x01' * 4 + lead + b'\0\0' + struct.pack('<II', 3, 1685614919) + b'\0\0\x02\0'
            self.assertTrue(FS.PLANE_REF.search(b))

    def test_ext_eref(self):
        b = b'\0\0\0\0' + struct.pack('<III', 160, 1711657119, 3)
        self.assertEqual(FS._ext_eref(b, 0, len(b), 160), [3])

    @unittest.skipUnless(os.path.exists(AB + 'AB_MIRROR_175_feat_top.SLDPRT'), 'A/B parts not present')
    def test_ab_mirror(self):
        d = V.feature_stream(AB + 'AB_MIRROR_175_feat_top.SLDPRT')
        h = FS.header_index(d)[41]
        self.assertEqual(FS.mirror_plane_ref(d, h, {2, 3, 4, 40, 41})[0], 3)
        self.assertTrue(ON.seed_list(d, h))


if __name__ == '__main__':
    unittest.main()
