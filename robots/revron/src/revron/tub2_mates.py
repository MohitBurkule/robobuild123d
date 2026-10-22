"""[tub2] What the chassis clears where the weapon mounts seat on it: the mount slab (its side profile over MNT_SLAB_T, the notch over the
tab and the heel under it) is cut out of the tub. Only the slab can touch the chassis, so the plate's holes and battered boss stay out of it;
the side panels seat on the lobes with no overlap and need no cut."""
import build123d as bd
from .mount import mount_profile, _prism
from .params_chassis import MNT_SLAB_T
from .params_weapon import MNT_FRAME
from . import plate as pl


def mount_slab(side):
    """The mount slab in world coordinates (RV02 mirrored, then placed on its frame)."""
    part = _prism(mount_profile(side), 0.0, MNT_SLAB_T)
    return pl.placed(part if side == "r" else part.mirror(bd.Plane.YZ), MNT_FRAME[side])


def keepouts():
    return [mount_slab("l"), mount_slab("r")]
