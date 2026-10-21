"""[fix-S] Weapon module (kept as one import point): see mount.py and drisk.py."""
from .drisk import disc, disc_outline, drisk_plane, drisk_spacer, floating_disc, spider, weapon_shaft, _disc_local  # noqa: F401
from .mount import (batter_x, lead_groove, lead_groove_section, motor_back_spacer, mount_profile, stator_bolt_circle,  # noqa: F401
                    weapon_mount, _mount_clip, _mount_csk, _mount_profile, _stack_hole, _stator_hole)

__all__ = ["disc", "disc_outline", "drisk_plane", "drisk_spacer", "floating_disc", "spider", "weapon_shaft", "_disc_local",
           "batter_x", "lead_groove", "lead_groove_section", "motor_back_spacer", "mount_profile", "stator_bolt_circle",
           "weapon_mount", "_mount_clip", "_mount_csk", "_mount_profile", "_stack_hole", "_stator_hole"]
