import os, sys, unittest, subprocess
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sldprt import fstream as FS, answer_key as AK, validate as V, classrec as CR, objnum as ON

AB = os.path.join(os.path.dirname(__file__), '../../dumps_ab/')


def _es(n):
    d = V.feature_stream(AB + n + '.SLDPRT')
    D = AK.parse(AB + n + '.dump.txt')
    ex = {f.id: f for f in D.top() if f.extrude}
    dec = FS.decode(d, set(ex))
    return [(dec.endspecs.get(i), f.extrude) for i, f in ex.items()]


class TestRound13(unittest.TestCase):
    def check(self, n):
        for es, x in _es(n):
            self.assertIsNotNone(es)
            self.assertEqual((es.end1, es.end2, es.both), (x['end1'], x['end2'], x['both']), n)

    def test_cut_through_all_variants(self):
        for n in ('AB_CUTEND_079_c02_throughall', 'AB_CUTEND_080_c03_throughallboth',
                  'AB_CUTEND_081_c04_uptonext', 'AB_CUTEND_083_c06_uptosurface'):
            self.check(n)

    def test_boss_two_direction_dir_flag(self):
        for n in ('AB_BOSS_048_midplane', 'AB_BOSS_049_bothdir_d2_5', 'AB_BOSS_046_blind'):
            self.check(n)

    def test_tag_tie_break(self):
        self.check('AB_LPAT_158_flipdir')

    def test_ext_abs_key(self):
        # class 4 (ext_named_item) is S-105 at S=109 and S-99 at S=103: same absolute key
        e = ON.Ev(0, 0, 0, 4, '', 'new')
        self.assertEqual(CR.class_key(e, 109, True), CR.class_key(e, 103, True))
        self.assertNotEqual(CR.class_key(e, 109), CR.class_key(e, 103))

    def test_rv01_rebuilt(self):
        p = os.path.join(os.path.dirname(__file__), '../wip_r13/rv01check.py')
        out = subprocess.run([sys.executable, p], capture_output=True, text=True).stdout
        self.assertIn('extrusions 25 / 25', out)


if __name__ == '__main__':
    unittest.main()
