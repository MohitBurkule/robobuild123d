"""Every screw at its hole: a hole joint on the part the head bears on (z = insertion direction), the screw's `head`
frame mated onto it. The spec reads `at`/`dir` back with joints.seat(). Weapon holes are on the drisk pattern, declared
in the weapon frame (on the spin axis) of the spider / outer disc they belong to."""
from .params import *  # noqa: F401,F403
from .common import _polar
from .drisk import _disc_local

SIDES = ((-1, "l"), (1, "r"))
IN_X, OUT_X = (1, 0, 0), (-1, 0, 0)


def _screw(r, host, label, at, direction, bolt):
    r.hole(host, label, at, direction)
    r.joint(bolt, "head", (0, 0, 0))
    r.mate(host, label, bolt, "head")


def _weapon_frame(y, z):
    """World (Y, Z) of a drisk-pattern hole -> the weapon frame the spider and discs are drawn in."""
    return y - WY, z - WZ


def screws(r):
    for s, n in SIDES:
        sx, mnt = (s, 0, 0), f"mount_{n}"
        _screw(r, mnt, "csk_a", (s * MNT_IN, *SA), sx, f"bolt_u{n}a")      # mount into the 25 mm standoff
        _screw(r, mnt, "csk_b", (s * MNT_IN, *SB), sx, f"bolt_u{n}b")      # mount + lug into the 15 mm standoff
        for k, yz in (("a", SA), ("b", SB), ("c", NUT)):                    # side panel seats: two standoff ends, the nut
            _screw(r, f"side_{n}", f"seat_{k}", (s * SIDE_BOLT_X[k], *yz), (-s, 0, 0), f"bolt_s{n}{k}")
    for k, (u, v) in enumerate(STATOR_DIRS):                                # RV03 counterbores on the stator bolt circle
        dy, dz = STATOR_PCD / 2 * u, STATOR_PCD / 2 * v
        _screw(r, "mount_r", f"stator_cb{k}", (CB_CONE_X[1], WY + dy, WZ + dz), OUT_X, f"bolt_wm{k}")
    for k, (hub_c, bolt_c) in enumerate(zip(_polar(HUB_R), _polar(BOLT_R))):
        _screw(r, "spider", f"bell_hole{k}", (DR_X["spider"][0], *_weapon_frame(*_disc_local(*hub_c))), IN_X, f"bolt_p{k}")
        _screw(r, "disc_b", f"stack_hole{k}", (DR_X["disc_b"][1], *_weapon_frame(*_disc_local(*bolt_c))), OUT_X, f"bolt_d{k}")
