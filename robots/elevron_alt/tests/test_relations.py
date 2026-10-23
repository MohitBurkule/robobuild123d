"""Unit tests: the Alt masters drive the features that hang off them (relations hold, nothing is a free number)."""
import math

import pytest

from elevron_alt import params_chassis as C, params_drive as D, params_side as S, params_vert as V
from elevron_alt import chassis, side_panel, vert_mod, assembly


def test_chassis_envelope_follows_masters():
    s = chassis.chassis()
    bb = s.bounding_box()
    assert s.is_valid and len(s.solids()) == 1
    assert bb.min.X == pytest.approx(-(C.HX + C.BOSS_OUT), abs=1e-3)
    assert bb.max.X == pytest.approx(C.HX + C.BOSS_OUT, abs=1e-3)
    assert bb.min.Y == pytest.approx(-C.HY, abs=1e-3)
    assert bb.max.Y == pytest.approx(max(C.HY + C.TAB_LEN, C.HY + C.TAB_HOLE_DY + C.TAB_END_R), abs=1e-3)   # STEP: 42.51
    assert bb.max.Z == pytest.approx(C.CH_H, abs=1e-3)


def test_chassis_volume_near_step():
    """STEP Alt_chassis = 18686 mm3 (SolidWorks mass properties); the relation build is within 0.5 %."""
    assert chassis.chassis().volume == pytest.approx(18686.4, rel=0.005)


def test_lattice_windows_clear_ribs():
    """Every centre window edge stays one column radius off the diagonal rib line."""
    w = chassis.lattice_profile()
    a, b = C.POST_PITCH[0] / 2, C.POST_PITCH[1] / 2
    n = math.hypot(a, b)
    for x, y in (p for g in getattr(w, "geoms", [w]) for p in g.exterior.coords):
        if abs(x) < a - C.LAT_RIB_C and abs(y) < b - C.LAT_RIB_C:
            d = min(abs(b * x - a * y), abs(b * x + a * y)) / n
            assert d >= C.LAT_RIB_C - 1e-6


def test_n10_gearbox_on_wall():
    from robot.catalog import find
    assert D.N10_X + find(D.DRIVE_MOTOR).shaft["at"][0] == pytest.approx(C.IN_X)


def test_weapon_stack_is_contiguous():
    assert D.DISC_X[1] == pytest.approx(D.SPIDER_X[0])
    assert D.SPIDER_X[1] == pytest.approx(D.PROP_X0)
    assert D.MOTOR_X0 > -D.UP_IN                     # motor base inside the left upright face
    assert D.BRG_X0 < D.UP_IN < D.BRG_X0 + D.BRG[2]  # flange proud, race in the right upright


def test_side_panel_is_one_solid_and_mirrors():
    r, l = side_panel.side_panel(1), side_panel.side_panel(-1)
    assert len(r.solids()) == 1 and r.is_valid
    assert r.volume == pytest.approx(l.volume, rel=1e-6)
    assert l.bounding_box().max.X == pytest.approx(-r.bounding_box().min.X, abs=1e-6)


def test_side_crossbar_behind_tyre():
    assert S.CROSS_Y[0] >= C.AXLE_Y + D.TYRE_R and S.LAND_Y0 >= C.AXLE_Y + S.HUB_R


def test_vert_mod_prongs_in_tab_gap():
    assert V.TAB_GAP[0] < V.PRONG_X[0] < V.PRONG_X[1] < V.TAB_GAP[1]
    s = vert_mod.vert_mod()
    assert s.is_valid and len(s.solids()) == 1


def test_world_floor():
    """Tyres touch the floor: the lowest tyre point is z 0 in the robot world."""
    assert assembly.build("wheel_rr").bounding_box().min.Z == pytest.approx(0.0, abs=1e-3)
