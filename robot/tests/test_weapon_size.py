"""Weapon sizing solver (robot/gen/weapon_size.py): energy/tip-speed targets to dims."""

import math

import pytest

from robot.gen import weapon_size as ws


def test_energy_target_meets_within_mass_cap():
    d = ws.size(energy_j=10.0, max_r_mm=24.0, mass_cap_g=40.0, density_g_cc=7.85)
    assert d.mass_g <= 40.0 + 1e-6 and d.energy_j >= 10.0
    assert d.binding in ("mass_cap", "energy_j")
    assert d.r_mm == 24.0 and d.t_mm > 0


def test_disc_energy_identity():
    d = ws.size(energy_j=8.0, max_r_mm=20.0, mass_cap_g=30.0)
    assert abs(d.energy_j - 0.25 * (d.mass_g / 1000) * d.tip_ms ** 2) < 0.05


def test_tip_speed_target_binds():
    d = ws.size(tip_speed_ms=60.0, max_r_mm=24.0, mass_cap_g=40.0)
    assert d.binding == "tip_speed" and abs(d.tip_ms - 60.0) < 0.1


def test_energy_and_tip_together_pick_the_binding_one():
    d = ws.size(energy_j=5.0, tip_speed_ms=60.0, max_r_mm=24.0, mass_cap_g=40.0)
    assert d.tip_ms >= 60.0 - 1e-6 and d.energy_j >= 5.0


def test_motor_kv_caps_the_omega_and_gives_spinup_bite():
    d = ws.size(energy_j=10.0, max_r_mm=20.0, mass_cap_g=30.0, motor_kv=2300, motor_max_current_a=15.0, cells=2)
    omega_noload = 2300 * ws.RPM_PER_KV_PER_V * 3.7 * 2
    assert d.rpm_loaded <= omega_noload * 0.9 * 60 / (2 * math.pi) + 1
    assert d.spinup_s is not None and d.spinup_s > 0
    assert d.bite_mm is not None and d.bite_mm > 0


def test_bite_shrinks_with_more_teeth():
    a = ws.size(energy_j=10.0, max_r_mm=20.0, mass_cap_g=30.0, motor_kv=2300, motor_max_current_a=15.0, teeth=1)
    b = ws.size(energy_j=10.0, max_r_mm=20.0, mass_cap_g=30.0, motor_kv=2300, motor_max_current_a=15.0, teeth=2)
    assert b.bite_mm < a.bite_mm


def test_requires_a_target():
    with pytest.raises(ValueError):
        ws.size(max_r_mm=20.0)


def test_unknown_kind_rejected():
    with pytest.raises(ValueError):
        ws.size("drum", energy_j=5.0)


def test_energy_for_sanity_inverse():
    e = ws.energy_for("disc", 24.0, 3.0)
    assert 0 < e < 200
