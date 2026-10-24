"""Mate entity -> component instance + face-creating feature (item_mates.resolve_instances / rep_features)."""
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..")); import unittest
from functools import lru_cache
from sldprt import item_mates as IM, mate_check as MC

ROOT = os.path.join(os.path.dirname(__file__), '..', '..')


@lru_cache(None)
def mates():
    return {m['name']: m for m in IM.decode_asm_mates(os.path.join(ROOT, 'revdev', 'rvrn 2.0.SLDASM'),
                                                     os.path.join(ROOT, 'decoded'))['mates']}


class T(unittest.TestCase):
    def test_rep_feature_id(self):
        self.assertEqual(IM.rep_feature_id('moFromSktEntSurfIdRep_c,42,18,'), 42)

    def test_concentric2_hub_revolve(self):
        e = mates()['Concentric2']['entities']
        self.assertEqual(e[1]['instance_resolved'], 'RV01 Chassis-1')
        self.assertEqual(e[0]['instance_resolved'], 'Micro slx v1.0-1')

    def test_renamed_component_by_name_or_rename(self):
        comps, dm = MC.parse_asmdump(os.path.join(ROOT, 'dumps_v2', 'rvrn 2.0.asmdump.txt'))
        M = mates()
        ok = n = 0
        for m in dm:
            for x in m['ents']:
                if x['i'] < len(M[m['name']]['entities']):
                    n += 1
                    ok += M[m['name']]['entities'][x['i']].get('instance_resolved') == x['comp'].split('/')[0]
        self.assertGreater(ok / n, 0.9)


if __name__ == '__main__':
    unittest.main()
