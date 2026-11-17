"""Real-world electric drive train for the fight sim: brushed/brushless DC motor curves, ESC current limit, battery sag,
battery charge use, motor heating with copper resistance rise and a thermal cut-out.

Motor (per driven hinge):  V_m = duty * V_batt;  I = clip((V_m - Ke*omega) / R(T), -I_max, I_max);  torque = Kt * I
   -> torque falls linearly with speed (no-load speed V/Ke), stall torque Kt*V/R limited by the ESC's current limit.
Battery: V = cells * OCV(SoC) - I_total * R_int; SoC drops with I_total*dt / capacity. Sag slows everything when the
   weapon draws its spin-up current, as on a real 2S 180 mAh antweight pack.
Heat: dT/dt = (I^2 R - (T - T_amb) / R_th) / C_th; R(T) = R20 * (1 + 0.0039 (T - 20)); above T_cut the motor stops.

Spec (sim block, all optional; defaults are typical antweight parts and are reported as guessed):
  battery: {"cells": 2, "mAh": 180, "r_int_ohm": 0.08}
  weapon.motor: {"kv": 3800, "r_ohm": 0.12, "i_max_a": 30}          # brushless outrunner, e.g. GR1507 on a 30 A ESC
  drive.motor: {"no_load_rad_s": 250, "stall_Nm": 0.06, "stall_a": 1.6}  # N10/N20 gearmotor at the wheel
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

T_AMB = 25.0
ALPHA_CU = 0.0039


@dataclass
class Battery:
    cells: int = 2
    mah: float = 180.0
    r_int: float = 0.08
    soc: float = 1.0
    v: float = 8.4
    i: float = 0.0

    def ocv(self):
        return self.cells * (3.45 + 0.75 * max(0.0, min(1.0, self.soc)))  # LiPo 4.2 V full .. 3.45 V empty (linear)

    def update(self, i_total, dt):
        self.i = i_total
        self.v = max(0.0, self.ocv() - i_total * self.r_int)
        self.soc -= max(0.0, i_total) * dt / (self.mah * 3.6)
        return self.v


@dataclass
class Motor:
    name: str
    ke: float  # V s/rad (= Kt in N m/A)
    r20: float  # ohm at 20 C
    i_max: float  # ESC / driver current limit, A
    c_th: float = 8.0  # J/K
    r_th: float = 12.0  # K/W
    t_cut: float = 130.0  # C: windings / magnets give up
    temp: float = T_AMB
    i: float = 0.0
    dead: bool = False
    hist: list = field(default_factory=list)

    @property
    def r(self):
        return self.r20 * (1 + ALPHA_CU * (self.temp - 20.0))

    def torque(self, duty, v_batt, omega):
        if self.dead:
            self.i = 0.0
            return 0.0
        vm = max(-1.0, min(1.0, duty)) * v_batt
        self.i = max(-self.i_max, min(self.i_max, (vm - self.ke * omega) / self.r))
        return self.ke * self.i

    def heat(self, dt):
        p = self.i * self.i * self.r
        self.temp += (p - (self.temp - T_AMB) / self.r_th) * dt / self.c_th
        if self.temp > self.t_cut:
            self.dead = True


def weapon_motor(spec_sim, name):
    m = dict((spec_sim.get("weapon") or {}).get("motor") or {})
    kv = float(m.get("kv", 3800.0))
    return Motor(name, 60.0 / (2 * math.pi * kv), float(m.get("r_ohm", 0.12)), float(m.get("i_max_a", 30.0)),
                 c_th=float(m.get("c_th", 10.0)), r_th=float(m.get("r_th", 10.0)))


def drive_motor(spec_sim, name, v_nom=7.4):
    m = dict((spec_sim.get("drive") or {}).get("motor") or {})
    w0 = float(m.get("no_load_rad_s", (spec_sim.get("drive") or {}).get("max_rad_s", 250.0)))
    ts = float(m.get("stall_Nm", (spec_sim.get("drive") or {}).get("torque_Nm", 0.06)))
    ia = float(m.get("stall_a", 1.6))
    # wheel-referred equivalent motor (gearbox folded in): no-load speed v/ke, stall torque ke*v/R. Its "current" is the
    # wheel-referred one; electrical power vm*i is still right, so battery draw and I^2R heat are right.
    ke = v_nom / w0
    r = ke * v_nom / ts
    m_ = Motor(name, ke, r, 1.2 * ts / ke, c_th=3.0, r_th=25.0)
    m_.stall_a = ia
    return m_


def battery(spec_sim):
    b = dict(spec_sim.get("battery") or {})
    bat = Battery(int(b.get("cells", 2)), float(b.get("mAh", 180.0)), float(b.get("r_int_ohm", 0.08)))
    bat.v = bat.ocv()
    return bat
