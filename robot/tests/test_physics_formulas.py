"""Unit tests for robot.checks.physics.formulas (UNTESTED: written, not run)."""

import math

from robot.checks.physics import formulas as F


def test_tip_speed():
    assert math.isclose(F.tip_speed_ms(60.0, 1.0), 2 * math.pi)


def test_energy():
    w = 2 * math.pi
    assert math.isclose(F.stored_energy_j(2.0, 60.0), 0.5 * 2.0 * w * w)


def test_spinup_infinite_at_free_speed():
    assert F.spinup_time_s(1e-5, 1000, 1000, 0.1) == math.inf


def test_spinup_positive():
    assert 0 < F.spinup_time_s(1e-5, 850, 1000, 0.1) < 1


def test_bite():
    assert math.isclose(F.bite_m(2.0, 600.0, 2), 0.1)


def test_gyro_falls_with_inertia():
    assert F.gyro_turn_rate_limit(2e-5, 20000, 0.15, 0.1) < F.gyro_turn_rate_limit(1e-5, 20000, 0.15, 0.1)


def test_runtime():
    assert math.isclose(F.runtime_s(1000, 0.8, usable=1.0), 4500.0)


def test_push_vs_traction():
    assert F.push_force_n(0.01, 2, 0.02) == 2.0
    assert math.isclose(F.traction_force_n(0.15, 0.5, 1.0), 0.15 * 9.81 * 0.5)
