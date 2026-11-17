"""Part dispatcher for Iceberg (called by robot/spec.py for model parts)."""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from iceberg import parts as PP  # noqa: E402


BUILDERS = {
    "bottom_plate": PP.build_bottom_plate,
    "top_plate": PP.build_top_plate,
    "tub": PP.build_tub,
    "upright_l": lambda: PP.build_upright(1),
    "upright_r": lambda: PP.build_upright(-1),
    "top_rod": PP.build_top_rod,
    "weapon_shaft": PP.build_weapon_shaft,
    "weapon_disc": PP.build_weapon_disc,
    "weapon_hub": PP.build_weapon_hub,
    "guard_l": PP.build_guard,
    "guard_r": PP.build_guard,
    "fork_mount_l": PP.build_fork_mount,
    "fork_mount_r": PP.build_fork_mount,
    "fork_l": PP.build_fork,
    "fork_r": PP.build_fork,
    "wheel": PP.build_wheel,
    "locking_bar": PP.build_locking_bar,
    "bearing": PP.build_bearing,
}


def build(part: str, **_kwargs):
    if part not in BUILDERS:
        raise ValueError(f"Unknown Iceberg part: {part!r}")
    return BUILDERS[part]()
