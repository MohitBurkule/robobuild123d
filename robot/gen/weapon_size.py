"""Weapon sizing solver (H3): ask for energy or tip speed, get disc dimensions.

An LLM cannot ask for "10 J" today - geometry is constants. `size()` closes the
loop from a requirement to dims: pick the largest radius the rules and chassis
allow, spend the mass cap on it, and report the energy, tip speed, spin-up time
and bite that result - plus the requirement that is binding.

Disc physics: m = rho pi r^2 t; I = m r^2 / 2; E = I omega^2 / 2; tip = omega r
(so E = m v^2 / 4 for a disc). Motor: no-load omega = kv * pi/30 * V (kv in rpm/V);
torque per amp Kt = 60 / (2 pi kv); spin-up t = I omega / (Kt * I_motor).
Bite: v_contact / (rev/s * teeth); the contact speed is the robot's drive speed
(approximated 1.0 m/s when unknown).
"""

from __future__ import annotations

import math
from dataclasses import dataclass

CELL_V = 3.7
RPM_PER_KV_PER_V = math.pi / 30.0  # rad/s per (rpm/V, V)
CONTACT_SPEED_MS = 1.0


@dataclass
class WeaponDims:
    r_mm: float
    t_mm: float
    mass_g: float
    moi_kgm2: float
    rpm_loaded: float
    tip_ms: float
    energy_j: float
    bite_mm: float
    spinup_s: float
    binding: str

    def to_dict(self):
        return dict(self.__dict__)


def _motor_omega_rad_s(kv, cells):
    return kv * RPM_PER_KV_PER_V * CELL_V * cells


def size(kind="disc", *, energy_j=None, tip_speed_ms=None, max_r_mm=24.0, mass_cap_g=40.0,
         density_g_cc=7.85, motor_kv=None, motor_max_current_a=None, cells=2, teeth=1):
    """Dimensions of a `kind` weapon meeting `energy_j` and/or `tip_speed_ms` within the caps.

    `binding` names what limited the design: mass_cap, max_r, tip_speed band, or the energy target met.
    """
    if kind != "disc":
        raise ValueError(f"size() builds discs only today, not {kind!r}")
    if energy_j is None and tip_speed_ms is None:
        raise ValueError("ask for energy_j or tip_speed_ms")
    r = max_r_mm / 1000.0
    rho = density_g_cc * 1000.0
    mass_cap = mass_cap_g / 1000.0
    t = mass_cap / (rho * math.pi * r ** 2)
    m = mass_cap
    moi = 0.5 * m * r ** 2
    binding = "mass_cap"
    if tip_speed_ms is not None:
        omega_req = tip_speed_ms / r
        e_at_tip = 0.5 * moi * omega_req ** 2
        if energy_j is None or e_at_tip >= energy_j:
            omega = omega_req
            binding = "tip_speed"
        else:
            omega = math.sqrt(2 * energy_j / moi)
            binding = "energy_j"
    else:
        omega = math.sqrt(2 * energy_j / moi)
    tip = omega * r
    rpm = omega * 60 / (2 * math.pi)
    energy = 0.5 * moi * omega ** 2
    spinup, bite = None, None
    if motor_kv and motor_max_current_a:
        omega_noload = _motor_omega_rad_s(motor_kv, cells)
        if omega > omega_noload:
            omega = omega_noload * 0.9
            tip = omega * r
            rpm = omega * 60 / (2 * math.pi)
            energy = 0.5 * moi * omega ** 2
            binding = "motor_kv"
        kt = 60.0 / (2 * math.pi * motor_kv)
        spinup = moi * omega / (kt * motor_max_current_a)
        bite = CONTACT_SPEED_MS / (rpm / 60.0 * teeth) * 1000.0
    return WeaponDims(round(r * 1000, 2), round(t * 1000, 3), round(m * 1000, 2), round(moi, 8),
                      round(rpm, 0), round(tip, 2), round(energy, 2),
                      round(bite, 2) if bite else None, round(spinup, 2) if spinup else None, binding)


def energy_for(kind, r_mm, t_mm, density_g_cc=7.85):
    """Energy stored at the disc's mass and a tip speed of 40 m/s (a sanity inverse)."""
    r = r_mm / 1000.0
    m = density_g_cc * 1000.0 * math.pi * r ** 2 * (t_mm / 1000.0)
    return round(0.25 * m * 40.0 ** 2, 2)
