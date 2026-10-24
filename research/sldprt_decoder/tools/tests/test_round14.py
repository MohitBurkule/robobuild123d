import os, sys, unittest
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from sldprt import item_doc as DOC, objnum as ON

AB = os.path.join(os.path.dirname(__file__), '../../dumps_ab/')


def _d(n):
    return DOC.decode_file(AB + n + '.SLDPRT')


class TestRound14Doc(unittest.TestCase):
    def test_configurations_active_first(self):
        r = _d('AB_CFG_331_add_two_configs')
        self.assertEqual(r['active_config'], 'Cfg3')
        self.assertEqual(set(r['configurations']), {'Default', 'Cfg2', 'Cfg3'})
        self.assertEqual(_d('AB_CFG_334_rename_default')['configurations'], ['Renamed'])
        self.assertIn('DS2', _d('AB_CFG_335_display_state')['display_states'])

    def test_material_and_appearance(self):
        r = _d('AB_MAT_327_m3_PCHighViscosity')
        self.assertEqual((r['material'], r['material_db']), ('PC High Viscosity', 'SOLIDWORKS Materials'))
        self.assertAlmostEqual(r['part_colour'][7], 0.65)          # transparency
        b = _d('AB_BASE_006_block_a')
        self.assertIsNone(b['material'])
        self.assertEqual([round(x * 255) for x in b['part_colour'][:3]], [202, 209, 238])
        self.assertEqual(b['part_colour'][3:7], [1.0, 1.0, 0.5, 0.3125])

    def test_units(self):
        self.assertEqual(_d('AB_UNITS_347_inch')['units'], {'decimals': 4, 'linear': 3})
        self.assertEqual(_d('AB_UNITS_348_mm_3dec')['units'], {'decimals': 3, 'linear': 0})

    def test_custom_props_views_equations(self):
        p = _d('AB_DOC_321_prop_two')['custom_props']
        self.assertEqual([(x['name'], x['value'], x['type']) for x in p], [('TestProp', 'hello', 'text'), ('Second', 'world', 'text')])
        self.assertEqual(_d('AB_DOC_320_prop_yesno')['custom_props'][0]['type'], 'yesno')
        r = _d('AB_DOC_322_prop_config_specific')
        self.assertEqual((r['custom_props'], [x['name'] for x in r['config_props']]), ([], ['CfgProp']))
        self.assertEqual(_d('AB_VIEW_351_named_view')['views'], ['MyView'])
        self.assertEqual(_d('AB_EQN_338_global_var')['equations'], ['"L" = 15'])


class TestRound14Misc(unittest.TestCase):
    def test_pbud_flag_off_by_default(self):
        self.assertFalse(ON.PBUD_KEEP)

    def test_rebuild_circle_closed_and_voxel_iou(self):
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../rebuild'))
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../wip_r14'))
        import rv01_rebuild as R
        P = R._poly(dict(type='circle', c=(0.0, 0.0), r=1.25))
        self.assertEqual(P[0], P[-1])
        self.assertEqual(len(R.regions([dict(type='circle', c=(0.0, 0.0), r=1.25), dict(type='circle', c=(0.0, 0.0), r=2.5)])), 1)
        import decode_only as DO
        from build123d import Box, Location
        A = DO.tri_of(Box(4, 4, 4)); B = DO.tri_of(Box(4, 4, 4).moved(Location((2, 0, 0))))
        self.assertGreater(DO.iou(A, A)[0], 0.99)
        self.assertAlmostEqual(DO.iou(A, B)[0], 1 / 3, delta=0.03)


if __name__ == '__main__':
    unittest.main()
