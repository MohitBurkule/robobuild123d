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
    assert D.MOTOR_X0 == pytest.approx(-D.UP_IN)     # motor base flat on the left upright's inner face
    assert D.DISC_X[0] == pytest.approx(D.BELL_X + D.DISC_GAP)
    assert D.BRG_X0 < D.UP_IN < D.BRG_X0 + D.BRG[2]  # flange proud, race in the right upright


def test_side_panel_is_one_solid_and_mirrors():
    r, l = side_panel.side_panel(1), side_panel.side_panel(-1)
    assert len(r.solids()) == 1 and r.is_valid
    assert r.volume == pytest.approx(l.volume, rel=1e-6)
    assert l.bounding_box().max.X == pytest.approx(-r.bounding_box().min.X, abs=1e-6)


def test_side_panel_relations():
    """The crossbar stands behind the rear tyre, the tongue fits the tab gap beside the prong, the wells clear the tyres."""
    assert S.CROSS_Y0 >= C.AXLE_Y + D.TYRE_R
    assert V.PRONG[0] + V.PRONG[1] < S.TONGUE_X[0] < S.TONGUE_X[1] < S.TAB_GAP[1]
    assert S.WELL_R > D.TYRE_R and S.FORK_X[1] < D.WHEEL_OUT


def test_vert_mod_prongs_in_tab_gap():
    assert V.TAB_GAP[0] <= V.PRONG[0] < V.PRONG[0] + V.PRONG[1] < V.TAB_GAP[1]
    s = vert_mod.vert_mod()
    assert s.is_valid and len(s.solids()) == 1


def test_vert_mod_ramp_relations():
    """The ramp runs from the chassis front inner wall at deck height to the top of the upright tail circle; the upright
    underside is tangent to that circle from the chassis rear inner wall line."""
    from elevron_alt import vm_geom as G
    assert G.ramp_z(-C.IN_Y) == pytest.approx(C.CH_H)
    assert G.ramp_z(D.WY) == pytest.approx(D.WZ + V.UP_R)
    s = vert_mod.vert_mod()
    bb = s.bounding_box()
    assert bb.max.Z == pytest.approx(D.WZ + V.SHROUD[0] * math.sin(math.radians(45)), abs=0.05)   # shroud tip, 45 deg up
    assert bb.max.Y == pytest.approx(D.WY + V.SHROUD[0], abs=0.05)   # the shroud flare reaches past the tail
    assert bb.min.Z == pytest.approx(V.PRONG[2], abs=1e-3)


def test_vert_mod_volume_near_step():
    """STEP vert_mod = 16592 mm3; the relation build plus the hardware seats is within 2 %."""
    assert vert_mod.vert_mod().volume == pytest.approx(16592, rel=0.02)


def test_world_floor():
    """Tyres touch the floor: the lowest tyre point is z 0 in the robot world."""
    assert assembly.build("wheel_rr").bounding_box().min.Z == pytest.approx(0.0, abs=1e-3)


def test_interfaces_keep_their_fits():
    """Side pod <-> chassis / module interfaces are offsets of the mating features, so a master change cannot interlock them."""
    assert S.TONGUE_X[0] - (V.TAB_GAP[0] + V.PRONG_T) == pytest.approx(S.FIT)    # tongue off the module prong
    assert V.TAB_GAP[1] - S.TONGUE_X[1] == pytest.approx(S.FIT)                 # and off the outer tab
    assert S.TONGUE_X[1] > S.TONGUE_X[0]
    assert S.LIP_IN_R - C.BOSS_R == pytest.approx(S.LIP_CLR) and S.LIP_CLR > 0  # lip ring clears the boss obround
    assert S.TAB_POCKET[2] > C.HY + C.TAB_LEN                                     # pocket end wall past the tab end
    assert C.TAB_END_R * math.sqrt(2) == pytest.approx(C.CH_H - C.EDGE_CH - C.TAB_HOLE_Z - C.TAB_HOLE_DY)   # tab round tangent to Chamfer3


def test_teardown_names_real_parts():
    from elevron_alt.spec import teardown, make_spec
    ids = {p["id"] for p in make_spec("m.py")["parts"]}
    for t in teardown():
        assert set(t["parts"]) <= ids and abs(sum(c * c for c in t["dir"]) - 1) < 1e-9
