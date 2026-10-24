"""Round 10: relation visibility (parameter twin), numbering-based handle tag map,
entity-less and FEFF-less geometric relation records."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); import unittest
from collections import Counter
from sldprt import fstream as FS, validate as V, answer_key as AK

REV = os.path.join(os.path.dirname(__file__), '..', '..', 'revdev')
DUMPS = os.path.join(os.path.dirname(__file__), '..', '..', 'dumps_v2')


def rel_scores(name):
    d = V.feature_stream(os.path.join(REV, name + '.SLDPRT'))
    acc = V.Acc()
    V.evaluate(d, AK.parse(os.path.join(DUMPS, name + '.dump.txt')), acc)
    t = acc.table()
    return t['Relation.type+entities (precision)'], t['Relation.type+entities (recall)']


class Round10(unittest.TestCase):
    def test_stale_dimension_copies_dropped(self):
        p, r = rel_scores('FS1 M2 heatsert')
        self.assertEqual((p['ok'], p['n']), (66, 66))

    def test_handle_tags_from_numbering(self):
        p, r = rel_scores('RV08 1806 Brushless')
        self.assertEqual(p['ok'], p['n'])
        self.assertEqual(r['ok'], r['n'])

    def test_feffless_geometric_relations(self):
        p, r = rel_scores('Top Panel')
        self.assertGreaterEqual(r['ok'] / r['n'], 0.98)

    def test_rename_match(self):
        from sldprt.item_mates import rename_match
        names = {'RV12 N10 2200 RPM-2', 'RV12 N10 2200 RPM-1', 'RV01 Chassis-1', 'RV23 side panel LH-1',
                 'RV24 Mirrorside panel RH-2'}
        self.assertEqual(rename_match('RVRN 1.7 C1 Turnabot Spicy N10 2200 RPM-2', names), 'RV12 N10 2200 RPM-2')
        self.assertEqual(rename_match('side panel multipart-1', names), 'RV23 side panel LH-1')
        self.assertIsNone(rename_match('chassis-1', names))

    def test_split_cstrings(self):
        from sldprt import classrec as CR
        b = b'\x01\x02' + b'\xff\xfe\xff\x02' + 'D1'.encode('utf-16-le') + b'\x00\x00\xff\xfe\xff\x00'
        self.assertEqual([k for k, _, _ in CR.split_cstrings(b)], ['g', 's', 'g', 's'])

    def test_string_templates_train_only(self):
        # templates are learned on the train half; a validation part still gets covered by them
        from sldprt import classrec as CR, objnum as ON
        d = V.feature_stream(os.path.join(REV, 'fork 5 long.SLDPRT'))
        ev, _ = ON.numbering(d)
        recs = CR.decode_templates2(d, ev, V._templates2())
        self.assertTrue(any(r.cls == 'moFavoriteHandle_c' for r in recs))
        self.assertGreater(FS.coverage(d, CR.spans(recs)), 10)


if __name__ == '__main__':
    unittest.main()
