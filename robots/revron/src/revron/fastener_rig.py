"""Every screw at its hole: a hole joint on the part the head bears on (z = insertion direction), the screw's `head`
frame mated onto it. The spec reads `at`/`dir` back with joints.seat(). Weapon holes are on the drisk pattern, declared
in the weapon frame (on the spin axis) of the spider / outer disc they belong to."""
from .params import *  # noqa: F401,F403
from .common import _polar
from .side import bolt_x
from .drisk import _disc_local
from .joints import DIGITS

SIDES = ((-1, "l"), (1, "r"))
IN_X, OUT_X = (1, 0, 0), (-1, 0, 0)


def _screw(r, host, label, at, direction, bolt):
    r.hole(host, label, at, direction)
    r.joint(bolt, "head", (0, 0, 0))
    r.mate(host, label, bolt, "head")


def on_mount(n, p):
    """Robot-coordinate point p -> the frame of mount_n (on the weapon axis at its inner face, MNT_FRAME)."""
    return tuple(round(v - o, DIGITS) + 0.0 for v, o in zip(p, MNT_FRAME[n]))


def _weapon_frame(y, z):
    """World (Y, Z) of a drisk-pattern hole -> the weapon frame the spider and discs are drawn in."""
    return y - WY, z - WZ


def screws(r):
    for s, n in SIDES:
        sx, mnt = (s, 0, 0), f"mount_{n}"
        _screw(r, mnt, "csk_a", on_mount(n, (s * (MNT_IN - MNT_CSK_PROUD), *SA)), sx, f"bolt_u{n}a")      # mount into the 25 mm standoff
        _screw(r, mnt, "csk_b", on_mount(n, (s * (MNT_IN - MNT_CSK_PROUD), *SB)), sx, f"bolt_u{n}b")      # mount + lug into the 15 mm standoff
        for k, yz in (("a", SA), ("b", SB), ("c", NUT)):                    # side panel seats: two standoff ends, the nut
            _screw(r, f"side_{n}", f"seat_{k}", (s * bolt_x(k), *yz), (-s, 0, 0), f"bolt_s{n}{k}")
    for k, i in enumerate(WM_ORDER):                                         # RV03 counterbores on the motor's stator screw pattern
        dy, dz, _ = STATOR_HOLES[i]
        _screw(r, "mount_r", f"stator_cb{k}", on_mount("r", (CB_CONE_X[1], WY + dy, WZ + dz)), OUT_X, f"bolt_wm{k}")
    hubs, bolts = _polar(HUB_R, N_HUB), _polar(BOLT_R)                     # spider to bell: the motor's bell-top pattern
    for k in range(max(N_HUB, N_STACK)):
        if k < N_HUB:
            _screw(r, "spider", f"bell_hole{k}", (DR_X["spider"][0], *_weapon_frame(*_disc_local(*hubs[k]))), IN_X, f"bolt_p{k}")
        if k < N_STACK:
            _screw(r, "disc_b", f"stack_hole{k}", (DR_X["disc_b"][1], *_weapon_frame(*_disc_local(*bolts[k]))), OUT_X, f"bolt_d{k}")
