"""Rule sets. `aws2025` is the Antweight World Series ruleset (version 05.06.25)."""

from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Profile:
    name: str = "aws2025"
    roller_mass_g: float = 150.0
    non_roller_mass_g: float = 225.0
    footprint_mm: float = 150.0  # AWS 2025 rule 3a: 150 mm floor square, no overhang at any height, no height cap (see rules/aws2025_size_weight.md)
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
    fight_s: float = 180.0  # AWS: 3 minute fights
    runtime_margin: float = 1.25  # the pack must last this many fights' worth of the duty cycle
    cell_full_v: float = 4.2

    def mass_limit(self, roller: bool) -> float:
        return self.roller_mass_g if roller else self.non_roller_mass_g


DIR = Path(__file__).parent / "profiles"
META = ("description",)  # keys that are documentation, not Profile fields


def available() -> list[str]:
    """Profile names that exist as robot/profiles/*.json (the selectable rules profiles, E4)."""
    return sorted(p.stem for p in DIR.glob("*.json"))


def description(name: str) -> str:
    return str(_load(name).get("description", ""))


def _load(name: str) -> dict:
    f = DIR / f"{name}.json"
    if not f.exists():
        raise ValueError(f"unknown rules profile `{name}`; available: {', '.join(available())}")
    return json.loads(f.read_text())


def named(name: str) -> Profile:
    """The rules profile `name` (robot/profiles/<name>.json over the Profile defaults).

    Empty name means the defaults (aws2025). Unknown keys and unknown profiles raise
    ValueError: a typo'd threshold must never silently fall back to a default."""
    p = Profile()
    if not name:
        return p
    d = _load(name)
    fields = {f.name for f in dataclasses.fields(Profile)}
    unknown = [k for k in d if k not in fields and k not in META]
    if unknown:
        raise ValueError(f"profile `{name}` has keys that are not Profile fields: {', '.join(sorted(unknown))}")
    for k, v in d.items():
        if k in META or k == "name":
            continue
        if isinstance(getattr(p, k), tuple):
            v = tuple(v)
        setattr(p, k, v)
    p.name = name
    return p
