"""[fix-S] Part table and the model-file entry point build()."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub import *  # noqa: F401,F403
from .side import *  # noqa: F401,F403
from .weapon import *  # noqa: F401,F403


# ------------------------------------------------------------------------------------------------------------ misc
PARTS = {
    "base_panel": base_panel, "top_panel": top_panel, "chassis": chassis, "motor_back_spacer": motor_back_spacer,
    "mount_l": lambda: weapon_mount("l"), "mount_r": lambda: weapon_mount("r"),
    "fork_l": lambda: fork(-1), "fork_r": lambda: fork(1),
    "spider": spider, "disc_a": lambda: disc("disc_a"), "disc_b": lambda: disc("disc_b"), "drisk_spacer": drisk_spacer,
    "wedgelet_l": lambda: wedgelet(-1), "wedgelet_r": lambda: wedgelet(1),
    "side_panel_l": lambda: side_panel(-1), "side_panel_r": lambda: side_panel(1),
    "rear_hub_l": lambda: rear_hub(-1), "rear_hub_r": lambda: rear_hub(1),
    "front_hub_l": lambda: front_hub(-1), "front_hub_r": lambda: front_hub(1),
    "rear_tyre_l": lambda: tyre(21.5, 14.0, -42.0, -32.5, (RY, RZ), 1.2), "rear_tyre_r": lambda: tyre(21.5, 14.0, 32.5, 42.0, (RY, RZ), 1.2),
    "front_tyre_l": lambda: tyre(11.0, 7.0, -38.5, -32.5, SA, 0.6), "front_tyre_r": lambda: tyre(11.0, 7.0, 32.5, 38.5, SA, 0.6),
    "so_a_l": lambda: standoff((-SA_X[1], -SA_X[0]), SA), "so_a_r": lambda: standoff(SA_X, SA),
    "so_b_l": lambda: standoff((-SB_X[1], -SB_X[0]), SB), "so_b_r": lambda: standoff(SB_X, SB),
    "esc_tray": esc_tray,
}


def build(part, origin=None):
    """Model-file entry point (robot.shapes `model`): one part in world coordinates, or relative to `origin` (the part's
    `at`, for rotating parts whose frame sits on their spin axis)."""
    s = _solid(PARTS[part]())
    if part == "chassis":   # a failed panel boolean once left 413 mm3 in 7 solids and nothing passed noticed
        assert len(s.solids()) == 1 and s.volume > CHASSIS_MIN_VOLUME, f"chassis collapsed: {s.volume:.0f} mm3 in {len(s.solids())} solids"
    if origin:
        s = s.moved(_b().Location(tuple(-float(v) for v in origin)))
    return s
