"""Physics thresholds. Read from the rules profile when it has the attribute, else these defaults (AWS 2025 ants)."""

DEFAULTS = {
    "max_tip_speed_mph": 250.0,
    "min_weapon_energy_j": 3.0,
    "max_spinup_s": 2.0,
    "min_bite_mm": 2.0,           # at closing speed below
    "closing_speed_ms": 2.0,
    "min_gyro_turn_rad_s": 6.0,   # ~1 rev/s yaw without wheel lift
    "min_runtime_s": 180.0,       # 3 min fight
    "avg_current_share": 0.35,    # average draw / peak
    "esc_margin": 1.2,            # ESC continuous >= 1.2 x motor peak
    "min_drive_speed_ms": 1.5,
    "max_drive_speed_ms": 6.0,
    "mu_tyre": 0.9,
    "weapon_fight_rpm_share": 0.85,
}


def limit(profile, key):
    v = getattr(profile, key, None) if profile is not None else None
    return float(v) if v is not None else DEFAULTS[key]
