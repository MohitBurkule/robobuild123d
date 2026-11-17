"""Spinner-in-motion checks: unit tests of the pure pieces."""
import math

from robot.checks import spin_dyn


def test_floor_drop_formula():
    reach = 58.0
    drop = spin_dyn.TYRE_SQUASH_MM + reach * math.sin(math.radians(spin_dyn.FLOOR_TILT_DEG))
    assert 3.4 < drop < 3.6


def test_motor_kt_from_kv():
    # Kt = 60 / (2 pi kv): a 3000 kv motor at 30 A gives ~0.095 N m
    kv, amps = 3000.0, 30.0
    assert abs(60 / (2 * math.pi * kv) * amps - 0.0955) < 1e-3


def test_run_all_never_raises():
    class Ctx:
        not_checked = []
        metrics = {}
    out = spin_dyn.run_all(Ctx(), 0.0, (0, 0, 5))
    assert out == [] and Ctx.not_checked  # every sub-check failed soft and said so
