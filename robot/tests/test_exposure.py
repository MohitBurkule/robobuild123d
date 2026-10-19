"""Attack exposure (robot.checks.exposure): a vulnerable part an opponent can reach fails; one behind armour passes."""

from types import SimpleNamespace as NS

import numpy as np
import trimesh

from robot.checks import exposure as X


def _box(lo, hi):
    b = trimesh.creation.box(np.subtract(hi, lo))
    b.apply_translation(np.add(lo, hi) / 2)
    return b


def _belt(x=30.0):
    """An O-ring loop in a YZ plane at X = x."""
    t = trimesh.creation.annulus(9, 10, 1.0)
    t.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, (0, 1, 0)))
    t.apply_translation((x, 0, 10))
    return t


def test_belt_outside_the_side_panel_is_exposed():
    chassis = _box((-25, -20, 0), (25, 20, 18))
    open_ = X.exposed_fraction(_belt(), chassis)
    panel = trimesh.util.concatenate([chassis, _box((32, -22, 0), (34, 22, 22)), _box((25, -22, 20), (34, 22, 22)),
                                     _box((25, 20, 0), (34, 22, 22)), _box((25, -22, 0), (34, -20, 22))])   # side panel wrapping the belt
    shielded = X.exposed_fraction(_belt(), panel)
    assert max(open_.values()) > 0.6
    assert shielded["horizontal"] < max(open_.values()) and shielded["horizontal"] < 0.35


def test_esc_under_a_lid_is_shielded_and_open_top_is_not():
    esc = _box((-5, -5, 3), (5, 5, 6))
    tub = _box((-20, -20, 0), (20, 20, 2)).union(_box((-20, -20, 0), (-18, 20, 10))).union(_box((18, -20, 0), (20, 20, 10))) \
        .union(_box((-20, -20, 0), (20, -18, 10))).union(_box((-20, 18, 0), (20, 20, 10)))
    lid = tub.union(_box((-20, -20, 10), (20, 20, 11)))
    assert X.exposed_fraction(esc, tub)["overhead"] > 0.1
    assert max(X.exposed_fraction(esc, lid).values()) < 0.01


def test_redundancy_flags_one_hit_on_both_sides():
    parts = [NS(id="motor_l", kind="motor", catalog="n10", role=None), NS(id="motor_r", kind="motor", catalog="n10", role=None)]
    res_bad = {"motor_l": {"horizontal": 0.7, "overhead": 0, "floor": 0}, "motor_r": {"horizontal": 0.7, "overhead": 0, "floor": 0}}
    res_ok = {"motor_l": {"horizontal": 0.7, "overhead": 0, "floor": 0}, "motor_r": {"horizontal": 0.1, "overhead": 0, "floor": 0}}
    spec = NS(parts=parts)
    assert any(not f.passed for f in X._redundancy(spec, res_bad, {}))
    assert all(f.passed for f in X._redundancy(spec, res_ok, {}))


def test_switch_recessed_vs_proud():
    body = _box((-20, -20, 0), (20, 20, 15))
    assert X.proud_of(_box((-3, -21.5, 5), (3, -17, 9)), [body]) > 0.2      # sticks out of the rear face
    assert X.proud_of(_box((-3, -19.5, 5), (3, -15, 9)), [body]) <= 0.2     # behind the rear face


def test_wire_on_outer_face():
    body = _box((-20, -20, 0), (20, 20, 15))
    assert X.envelope_margin(np.array([[0, 19.8, 7.0]]), [body]) < 1.0
    assert X.envelope_margin(np.array([[0, 10.0, 7.0]]), [body]) >= 1.0


def test_tilt_sweep_finds_the_side_that_loses_the_ground_game():
    body = _box((-20, -20, 4), (20, 20, 15))            # 4 mm off the floor everywhere
    lip = _box((-20, 20, 0), (20, 30, 0.6))              # front lip only
    wheels = [_box((-25, -15, 0), (-21, -5, 10)), _box((21, -15, 0), (25, -5, 10))]
    sw = X.tilt_sweep([body, lip] + wheels, [False, False, True, True])
    assert sw["front"]["pitch +0"] < 1.0
    assert sw["rear"]["pitch +0"] >= 4.0


def test_catch_area_square_face_vs_battered_face():
    square = _box((-20, -20, 0), (20, 20, 20))
    ramp = trimesh.creation.extrude_polygon(__import__("shapely.geometry", fromlist=["Polygon"]).Polygon(
        [(-20, 0), (20, 0), (0, 20)]), 40)                # 45 deg faces both sides, in XZ
    ramp.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, (1, 0, 0)))
    ramp.apply_translation((0, 20, 0))
    a = X.catch_area([square], square)
    b = X.catch_area([ramp], ramp)
    assert a["left"] > 300 and b["left"] < 50
