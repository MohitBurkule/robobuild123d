"""[tub2] What the tub reads from the weapon module: params_weapon.tub_interface() (the weapon owner's contract), gated by weapon.type.
Types without a notch tab (or no weapon at all) give TAB = None: the tub then builds no tab wall, key, key hole, wire slot or rabbet and stays one valid solid."""
from . import params_weapon as _pw
from .params_chassis import SPIDER_TAB_GAP

IFACE = _pw.tub_interface()
TYPES_WITH_TAB = ("drisk",)                                   # weapon types whose mounts drop over a chassis tab
TAB = IFACE.get("tab") if IFACE.get("type") in TYPES_WITH_TAB else None
HAS_TAB = bool(TAB)
MOUNT_IN = IFACE["mount_in"]
MOUNT_FRAMES = IFACE["mount_frames"]


def _spider_out():
    """|X| of the rotor's outer end (what spins out at the stack-bolt circle: the spider's outer face, or the stack-bolt heads when a short motor moves the stack): the interface's `rotor_x` when the weapon module gives it, else its `spider_x`, else the drisk stack chain."""
    if IFACE.get("rotor_x"):
        return max(abs(v) for v in IFACE["rotor_x"])
    if IFACE.get("spider_x"):
        return max(abs(v) for v in IFACE["spider_x"])
    if not HAS_TAB or not hasattr(_pw, "DR_X"):
        return None
    return round(max(abs(_pw.MOTOR_X + v) for v in _pw.DR_X["spider"]), 6)


SPIDER_OUT = _spider_out()
SPIDER_GAP = SPIDER_TAB_GAP                                   # the tab wall's inner face stands at least this far off the spider's outer face
