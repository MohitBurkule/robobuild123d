"""Closed-form antweight physics (no CAD, no sim). SI units in, SI out unless the name says otherwise.

Pure functions so they unit-test without a build. UNTESTED: written without running.
"""

from __future__ import annotations

import math

G0 = 9.81
MPH_PER_MS = 2.236936


def tip_speed_ms(rpm: float, radius_m: float) -> float:
    return rpm * 2.0 * math.pi / 60.0 * radius_m


def stored_energy_j(inertia_kgm2: float, rpm: float) -> float:
    w = rpm * 2.0 * math.pi / 60.0
    return 0.5 * inertia_kgm2 * w * w


def motor_torque_stall_nm(stall_a: float, kv_rpm_per_v: float) -> float:
    """Kt = 60 / (2 pi kV) N m/A; stall torque = Kt * I."""
    return 60.0 / (2.0 * math.pi * kv_rpm_per_v) * stall_a


def spinup_time_s(inertia_kgm2: float, rpm_target: float, rpm_free: float, stall_torque_nm: float, reduction: float = 1.0) -> float:
    """Linear torque-speed motor: t = J w0 / T0 * ln(1 / (1 - w/w0)), reflected through the reduction."""
    if stall_torque_nm <= 0 or rpm_free <= 0 or rpm_target >= rpm_free:
        return math.inf
    w0 = rpm_free * 2.0 * math.pi / 60.0
    t0 = stall_torque_nm * reduction
    return inertia_kgm2 * w0 / t0 * math.log(1.0 / (1.0 - rpm_target / rpm_free))


def bite_m(closing_speed_ms: float, rpm: float, n_teeth: int) -> float:
    """Depth one tooth bites per revolution share: v / (n * f)."""
    if rpm <= 0 or n_teeth <= 0:
        return 0.0
    return closing_speed_ms / (n_teeth * rpm / 60.0)


def gyro_turn_rate_limit(inertia_kgm2: float, rpm: float, mass_kg: float, track_m: float) -> float:
    """Yaw rate (rad/s) at which the gyro moment J*w*Omega lifts one wheel row: J w Omega = m g track/2."""
    w = rpm * 2.0 * math.pi / 60.0
    if inertia_kgm2 <= 0 or w <= 0:
        return math.inf
    return mass_kg * G0 * track_m / 2.0 / (inertia_kgm2 * w)


def battery_max_a(capacity_mah: float, c_rating: float) -> float:
    return capacity_mah / 1000.0 * c_rating


def runtime_s(capacity_mah: float, avg_current_a: float, usable: float = 0.8) -> float:
    if avg_current_a <= 0:
        return math.inf
    return capacity_mah / 1000.0 * usable / avg_current_a * 3600.0


def drive_top_speed_ms(rpm_free: float, wheel_d_m: float, reduction: float = 1.0, load_factor: float = 0.8) -> float:
    return rpm_free / reduction * load_factor * math.pi * wheel_d_m / 60.0


def push_force_n(stall_torque_nm: float, n_driven: int, wheel_d_m: float, reduction: float = 1.0) -> float:
    """Total wheel force if motors stall (before traction)."""
    if wheel_d_m <= 0:
        return 0.0
    return stall_torque_nm * reduction * n_driven / (wheel_d_m / 2.0)


def traction_force_n(mass_kg: float, driven_share: float, mu: float) -> float:
    return mass_kg * G0 * driven_share * mu
