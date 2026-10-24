"""Object / class numbering (objnum.py) on real feature streams."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); import struct, unittest
from functools import lru_cache
from sldprt import fstream as FS, objnum as ON, validate as V

REV = os.path.join(os.path.dirname(__file__), '..', '..', 'revdev')


@lru_cache(None)
def stream(name):
    return V.feature_stream(os.path.join(REV, name + '.SLDPRT'))


@lru_cache(None)
def numbered(name):
    d = stream(name)
    ev, fix = ON.numbering(d)
    return d, ev, ON.feature_objects(d, FS.feature_headers(d), ev)


class T(unittest.TestCase):
    def test_start_count_is_first_u32(self):
        d, ev, _ = numbered('RV04 Drisk spacer')
        self.assertEqual(ev[0].kind, 'def')
        self.assertEqual(ev[0].index, struct.unpack_from('<I', d, 0)[0])

    def test_handle_classes_match_relation_slot_tags(self):
        # sgPointHandle / sgLineHandle class indices, recovered independently from relation slots
        for name in ('FS1 M2 heatsert', 'RV15 BBB Antweight Switch', 'Top Panel', 'RV07 Prop mount'):
            d, ev, _ = numbered(name)
            idx = {}
            for e in ev:
                if e.kind == 'def':
                    idx.setdefault(e.name, e.index)
            for t, c in list(FS.tag_map(d).items())[:2]:
                self.assertEqual(t & 0x7fff, idx[c], (name, c))

    def test_cirpattern_seed_is_exact_object_ref(self):
        d, ev, fo = numbered('RV06 Fixed disc')
        h = next(h for h, i, c in fo.values() if h.name == 'CirPattern1')
        refs = ON.seed_list(d, h)
        self.assertEqual(refs, [646])
        fid, drift = ON.resolve_objects(refs, fo, h.offset)[0]
        self.assertEqual(fo[fid][0].name, 'Cut-Extrude1')
        self.assertEqual(drift, 0)

    def test_mirror_seed_list_multiple(self):
        d, ev, fo = numbered('RV12 N10 2200 RPM')
        h = next(h for h, i, c in fo.values() if h.name == 'Mirror2')
        got = [fo[x[0]][0].name for x in ON.resolve_objects(ON.seed_list(d, h), fo, h.offset)]
        self.assertEqual(got, ['Cut-Extrude1', 'Fillet1'])

    def test_float_and_timestamp_tags_rejected(self):
        d = stream('RV15 BBB Antweight Switch')
        self.assertTrue(ON.is_stamp(d, 1481))          # 81 80 1d 66: low half of a timestamp
        offs = {e.offset for e in ON.number(d)}
        self.assertNotIn(1481, offs)
        self.assertIn(1485, offs)


if __name__ == '__main__':
    unittest.main()
