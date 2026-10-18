"""Rule sets. `aws2025` is the Antweight World Series ruleset (version 05.06.25)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Profile:
    name: str = "aws2025"
    roller_mass_g: float = 150.0
    non_roller_mass_g: float = 225.0
    footprint_mm: float = 150.0  # side of the square floor space, no overhang at any height
    max_tip_speed_mph: float = 600.0
    max_cell_v: float = 4.2
    require_locking_bar: bool = True
    require_tool_free_switch: bool = True
    contact_tol_mm: float = 0.08  # overlap deeper than this is a collision; shallower counts as touching
    min_clearance_moving_mm: float = 0.4
    wedge_gap_mm: tuple = (0.2, 1.5)
    wedge_angle_deg: tuple = (6.0, 30.0)
    min_wall_fdm_mm: float = 0.9
    min_wall_tpu_mm: float = 1.2
    min_wall_resin_mm: float = 0.8
    mass_warn_frac: float = 0.98
    engagement_d: float = 1.5
    driver_access_radius_mm: float = 2.6
    driver_access_len_mm: float = 14.0
    wire_bend_x_dia: float = 3.0
    allowance_g: float = 1.2  # glue, paint, tape and solder not modelled
    capture_slop_mm: float = 1.2
    min_ground_clearance_mm: float = 1.0
    bed_mm: tuple = (180.0, 180.0, 180.0)
    fight_s: float = 120.0
    cell_full_v: float = 4.2

    def mass_limit(self, roller: bool) -> float:
        return self.roller_mass_g if roller else self.non_roller_mass_g


def named(name: str) -> Profile:
    p = Profile()
    if name:
        p.name = name
    return p
