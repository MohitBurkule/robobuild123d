"""Mass and size budget estimates used to prune hypotheses before any geometry is built.

Numbers are the lightest realistic build of each choice (catalog masses, taxonomy `mass_budgets_g`); a hypothesis whose
LOW estimate already breaks 150 g or the 150 mm square cannot be built and is pruned.
"""

from __future__ import annotations

from functools import lru_cache

from .. import catalog

def _wc(h):
    from .hypothesis import WEAPON_CLASSES
    return WEAPON_CLASSES[h.weapon]


MASS_LIMIT_G = 150.0
SIZE_LIMIT_MM = 150.0

DRIVE_MOTOR_CATALOG = {"n10": "n10_300rpm_6v", "n20": "n20_1000rpm_6v"}
N_DRIVEN = {"2WD": 2, "2WD_skid": 2, "4WD": 4, "4WD_skid": 2, "6WD": 6, "8WD": 8, "oring_track": 2, "rotating_pods": 4,
            "shuffle": 2, "melty": 2, "gyro_walker": 0}
N_WHEELS = {"2WD": 2, "2WD_skid": 2, "4WD": 4, "4WD_skid": 4, "6WD": 6, "8WD": 8, "oring_track": 4, "rotating_pods": 4,
            "shuffle": 0, "melty": 2, "gyro_walker": 0}
CHASSIS_G = {"2WD": 30.0, "2WD_skid": 30.0, "4WD": 38.0, "4WD_skid": 38.0, "6WD": 46.0, "8WD": 52.0, "oring_track": 40.0,
             "rotating_pods": 48.0, "shuffle": 35.0, "melty": 25.0, "gyro_walker": 30.0}
FRONT_G = {"none": 0.0, "wedge": 8.0, "wedgelets": 4.0, "forks": 4.0, "skirt": 5.0, "plow": 8.0, "weapon_is_front": 0.0}
FASTENERS_WIRES_G = 6.0


@lru_cache(maxsize=None)
def cat_mass(cid: str) -> float:
    if not cid or cid in ("none", "integrated"):
        return 0.0
    try:
        return float(catalog.find(cid).mass_g)
    except Exception:  # noqa: BLE001 - unknown id contributes nothing; the rules flag it
        return 0.0


def wheel_mass(dia: float) -> float:
    return 0.0045 * dia * dia  # 28 mm -> 3.5 g printed hub + tyre


def mass_low(h) -> float:
    """Lightest realistic mass of the hypothesis (grams)."""
    m = CHASSIS_G[h.drive_layout] + FASTENERS_WIRES_G + FRONT_G[h.front]
    n_motors = N_DRIVEN[h.drive_layout]
    if h.transmission == "belt" and h.drive_layout in ("4WD", "6WD", "8WD"):
        n_motors = 2  # one motor per side; belts carry the drive to the other axles (Revron: 2 N10 + 2 O-rings)
    m += n_motors * cat_mass(DRIVE_MOTOR_CATALOG[h.drive_motor])
    m += N_WHEELS[h.drive_layout] * wheel_mass(h.wheel_dia)
    if h.transmission == "belt":
        m += 1.5 * (N_WHEELS[h.drive_layout] - n_motors)  # O-ring + standoff axle per belted wheel
    m += cat_mass(h.battery) + cat_mass(h.drive_esc) + cat_mass(h.weapon_esc) + cat_mass(h.rx)
    m += _wc(h).weapon_mass_g[0]
    if h.wheel_guards:
        m += 2.0
    return m


def width_low(h) -> float:
    """Narrowest track the drive can have: two motors back to back plus the wheels and walls (mm)."""
    motor_len = {"n10": 24.0, "n20": 27.0}[h.drive_motor]
    wheel_w = 8.0 if h.wheel_dia <= 22 else 10.0
    wall = 2.0 if h.wheel_guards else 0.0
    return 2 * (motor_len + wheel_w + 1.0 + wall)


def length_low(h) -> float:
    """Shortest wheelbase + front + weapon reach (mm)."""
    n_axles = max(1, N_WHEELS[h.drive_layout] // 2)
    body = max(50.0, n_axles * (h.wheel_dia + 3.0))
    front = {"none": 0.0, "wedge": 20.0, "wedgelets": 12.0, "forks": 15.0, "skirt": 8.0, "plow": 20.0, "weapon_is_front": 0.0}[h.front]
    weapon = {"front": 25.0, "full_body": 10.0}.get(h.mount, 0.0) if _wc(h).actuator != "none" else 0.0
    return body + front + weapon
