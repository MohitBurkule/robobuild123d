"""Round 8: global class-index assignment, zlib/Parasolid blobs, external id objects, crossing
splits, moFavoriteHandle_c, whole-object templates."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); import struct, unittest, zlib
from functools import lru_cache
from sldprt import fstream as FS, objnum as ON, classrec as CR, validate as V, answer_key as AK

REV = os.path.join(os.path.dirname(__file__), '..', '..', 'revdev')
DUMPS = os.path.join(os.path.dirname(__file__), '..', '..', 'dumps_v2')


@lru_cache(None)
def stream(name):
    return V.feature_stream(os.path.join(REV, name + '.SLDPRT'))


@lru_cache(None)
def numbered(name):
    d = stream(name)
    ev, fix = ON.numbering(d)
    return d, ev, ON.feature_objects(d, FS.feature_headers(d), ev)


def seeds(name):
    d, ev, fo = numbered(name)
    top = AK.parse(os.path.join(DUMPS, name + '.dump.txt')).top()
    ids = {f.name: f.id for f in top}
    hidx = {}
    for h in FS.feature_headers(d):
        hidx.setdefault(h.feature_id, h)
    out = {}
    for f in top:
        if f.type in ('CirPattern', 'MirrorPattern', 'LPattern') and f.id in hidx:
            par = {fo[ids[p]][1] for p, t in f.parents if t != 'RefPlane' and ids.get(p) in fo}
            out[f.name] = (ON.seed_list(d, hidx[f.id]), par)
    return out


class Round8(unittest.TestCase):
    def test_dp_class_index_zero_led_first_object(self):
        # moDisplayDistanceDim_c's first object starts with 16 zero bytes: no 4-byte signature,
        # so the round-7 resync could not vote; the DP matches its instances (tag 0x8304)
        d, ev, _ = numbered('RV01 Chassis')
        idx = {e.offset: e.index for e in ev if e.kind == 'def'}
        self.assertEqual(idx[41372], 772)
        self.assertEqual(idx[165308] + 1, 2946)      # Chamfer1 = Mirror1 seed object ref

    def test_seed_refs_exact(self):
        s = seeds('RV04 Drisk spacer')['CirPattern1']
        self.assertEqual(set(s[0]), s[1])             # [902, 846] both exact
        s = seeds('RV06 Fixed disc')['CirPattern3']
        self.assertIn(1054, s[1])
        s = seeds('RV08 1806 Brushless')['CirPattern1']
        self.assertIn(618, s[1])

    def test_ext_id_object(self):
        # 01 00 00 00 | 6b 80 (external class S-7) | u16 id 0x030c | 00 00 : counted
        d, ev, _ = numbered('RV04 Drisk spacer')
        self.assertIn(33168, {e.offset for e in ev})

    def test_zlib_blobs_are_parasolid_and_tagless(self):
        d = stream('RV06 Fixed disc')
        bl = CR.ps_blobs(d)
        self.assertTrue(bl and all(raw > 0 for _, _, raw in bl))
        a, b, raw = [x for x in bl if x[0] <= 53282 < x[1]][0]
        self.assertEqual(len(zlib.decompress(d[a + 24:b])), raw)
        _, ev, _ = numbered('RV06 Fixed disc')
        self.assertFalse([e for e in ev if a <= e.offset < b])

    def test_split_crossings(self):
        X = [(1, [(-1.0, -1.0), (1.0, 1.0)]), (2, [(-1.0, 1.0), (1.0, -1.0)])]
        out = FS._split_crossings(X)
        self.assertEqual(sorted(s for s, _ in out), [1, 1, 2, 2])
        mids = {pl[-1] for s, pl in out if s == 1} & {pl[0] for s, pl in out if s == 1}
        self.assertEqual(len(mids), 1)
        self.assertAlmostEqual(list(mids)[0][0], 0.0)
        # end-point contacts are not split
        self.assertEqual(len(FS._split_crossings([(1, [(0, 0), (1, 0)]), (2, [(1, 0), (1, 1)])])), 2)

    def test_favorite_handle_value(self):
        d, ev, _ = numbered('fork 5')
        vals = [r.fields['value'] for r in CR.decode(d, ev) if r.cls == 'moFavoriteHandle_c']
        self.assertTrue(any(abs(v - 0.026) < 1e-12 for v in vals))   # D8@Sketch1 (0.038 in fork 5 long)
        d, ev, _ = numbered('fork 5 long')
        vals = [r.fields['value'] for r in CR.decode(d, ev) if r.cls == 'moFavoriteHandle_c']
        self.assertTrue(any(abs(v - 0.038) < 1e-12 for v in vals))

    def test_templates_generalise(self):
        tm = V._templates()
        self.assertIn('moDisplayDistanceDim_c', tm)
        d, ev, _ = numbered('fork 5 long')          # validation-half part
        got = CR.decode_templates(d, ev, tm)
        n = sum(1 for e in ev if e.kind == 'new' and e.name in tm)
        self.assertGreater(len(got), 0.8 * n)


if __name__ == '__main__':
    unittest.main()


class Round9(unittest.TestCase):
    def test_objref_not_stamp(self):
        # RV01: 'T(moSegmRightTrimEdgeIdRep_c) | 4f44 (objref 0x444f) | 7983 (next tag)' is counted
        d, ev, _ = numbered('RV01 Chassis')
        offs = {e.offset for e in ev}
        import re
        hits = [m.start() for m in re.finditer(re.escape(b'\x4f\x44\x79\x83\x7c\x04'), d)]
        self.assertTrue(hits and all(h - 2 in offs for h in hits[:10]))

    def test_cap_plane_is_not_side_face_evidence(self):
        # RV26 Sketch1: the outer outline lies in the cap planes but bounds no side face
        T = (1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0)
        cap = [{'kind': 'plane', 'n': (0, 0, 1), 'o': (0, 0, 0)}]
        side = [{'kind': 'plane', 'n': (0, 1, 0), 'o': (0, 0, 0), 'box': [-1, 0, 0, 1, 0, 1]}]
        sg = {'type': 0, 'p0': (-0.5, 0, 0), 'p1': (0.5, 0, 0)}
        self.assertFalse(V.seg_has_face(sg, T, cap))
        self.assertTrue(V.seg_has_face(sg, T, side))
        self.assertFalse(V.seg_has_face({'type': 0, 'p0': (2, 0, 0), 'p1': (3, 0, 0)}, T, side))
