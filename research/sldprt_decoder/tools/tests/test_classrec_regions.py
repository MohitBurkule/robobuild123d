"""classrec.py fixed-prefix layouts and the planar region solve (fstream.planar_faces / face_expand)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); import unittest
from functools import lru_cache
from sldprt import fstream as FS, objnum as ON, classrec as CR, validate as V

REV = os.path.join(os.path.dirname(__file__), '..', '..', 'revdev')


@lru_cache(None)
def part(name):
    d = V.feature_stream(os.path.join(REV, name + '.SLDPRT'))
    ev, _ = ON.numbering(d)
    heads = FS.feature_headers(d)
    return d, ev, heads, CR.decode(d, ev, {h.feature_id for h in heads})


class T(unittest.TestCase):
    def test_fr_feature_ids(self):
        d, ev, heads, recs = part('Top Panel')
        fr = [r for r in recs if r.cls == 'moFR_c']
        self.assertGreater(len(fr), 1000)
        ids = {h.feature_id for h in heads}
        self.assertTrue(all(r.fields['feature_id'] in ids for r in fr))

    def test_handles_and_backup_points(self):
        d, ev, heads, recs = part('RV13 Malenki nano')
        kinds = {r.cls for r in recs}
        self.assertIn('sgPointHandle', kinds)
        self.assertIn('moPointBackedUpData_c', kinds)

    def test_planar_faces_rectangle_with_holes(self):
        d, ev, heads, recs = part('RV26 Base Panel')
        dec = FS.decode(d)
        h = next(h for h in heads if h.name == 'Sketch1')
        faces = FS.planar_faces(dec.sketches[h.feature_id]['sketch'])
        bounded = [f for a, f, p in faces if a > 0]
        self.assertIn([1, 2, 7, 8], bounded)       # outer rectangle
        self.assertIn([13], bounded)                # a hole circle is its own face

    def test_face_expand_adds_attached_loop(self):
        d, ev, heads, recs = part('RV26 Base Panel')
        dec = FS.decode(d)
        h = next(h for h in heads if h.name == 'Sketch1')
        sk = dec.sketches[h.feature_id]['sketch']
        got = FS.face_expand(sk, [[1, 2, 7, 8]])
        self.assertTrue({1, 2, 7, 8, 9, 10, 11, 12, 13} >= got >= {1, 2, 7, 8})


if __name__ == '__main__':
    unittest.main()
