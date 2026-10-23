"""[tub2] Compartments: pockets cut from the catalog envelope of whatever sits in them, so a bigger gearmotor, pack or ESC gets room instead of
the tub being redrawn. Each cutter is the placed catalog part (the same pose the assembly rig gives it) less the heat-set bores and the skin round
them; a part that already clears the tub (the default) leaves the tub as it was. Which compartments exist is the declared LAYOUT (hook
chassis.compartments): motor, battery, partition (a rib between the pack bay and the electronics bay)."""
from build123d import Align, Cylinder, Pos
from . import hw
from .common import _U, _one
from .params_chassis import (SWITCH, SWX, DRIVE_MOTOR, MOTX, RY, RZ, LAYOUT, INS, RXESC, WESC, RX_C, WE_C, RX_X, WE_X, CH_Z0, CH_Z1, WALL_IN_REAR)
from .params_hardware import BATTERY, ELEC, BAT_W, SW_SEAT_Z
from .tub2_params import BORE_R, CH_IN_X, STOP_FRONT_Y, WALL_IN_FRONT, SEAT_Z, DECK, SKIN, OVER
from .tub2_util import box_xy

BAY_ROT = (0, 0, 90)                      # boards and the pack stand in their bays turned 90 about Z (assembly_rig._bay)
PARTITION_T = SKIN                        # rib between the pack bay and the electronics bay: one skin thick, centred in the gap between them
TOUCH = OVER ** 3                          # volume under which a part counts as clear of the tub (a tenth of a skin cubed: boolean noise at a shared face)
KEEP = [Pos(x, y, CH_Z0) * Cylinder(BORE_R + SKIN / 2, CH_Z1 - CH_Z0, align=(Align.CENTER, Align.CENTER, Align.MIN)) for x, y in INS]   # the heat-set bore and half a skin of plastic round it (every insert column and the rear boss) stay whole; a part may notch the rest of a column


def _cut(solid):
    """The envelope less the bore sleeves."""
    return solid - _U(*KEEP) if KEEP else solid


def motor_pockets():
    """Both gearmotors at their seats (the left one is the right one turned half a turn about Z)."""
    return [_cut(hw.placed(DRIVE_MOTOR, (s * MOTX, RY, RZ), (0, 0, 0 if s > 0 else 180))) for s in (1, -1)]


def battery_bay():
    return [_cut(hw.placed(BATTERY, ELEC["battery"], BAY_ROT))]


def switch_bay():
    """The power switch at its seat (turned 90 about Z, its wall-facing side SW_CLR off the wall): its pad and slot are drawn for the stock switch, a bigger one gets room."""
    return [_cut(hw.placed(SWITCH, (SWX, *ELEC["switch_yz"]), (0, 0, 90)))]


def pack_drop():
    """The way out of the pack: its footprint straight down from the pad underside (where its ears seat) to the tub's bottom face, less the bore sleeves. The pack leaves through the base opening, so the
    tub must not close over the footprint below it (a narrow chassis lets a column body reach in under the pack)."""
    bb = hw.placed(BATTERY, ELEC["battery"], BAY_ROT).bounding_box()
    return _cut(box_xy(max(bb.min.X, -CH_IN_X), min(bb.max.X, CH_IN_X), max(bb.min.Y, STOP_FRONT_Y), min(bb.max.Y, WALL_IN_FRONT), CH_Z0 - OVER, bb.min.Z + OVER))   # inside the cavity only: the lugs and walls outside it stay whole


def switch_drop():
    """The way out of the switch: its footprint straight down from the pad underside (where its ears seat) to the tub's bottom face, less the bore sleeves (the switch leaves downwards once its screws are out, so a column body
    that reaches in under it must not close over the footprint). Inside the cavity only: the walls stay whole."""
    bb = hw.placed(SWITCH, (SWX, *ELEC["switch_yz"]), (0, 0, 90)).bounding_box()
    return _cut(box_xy(bb.min.X, min(bb.max.X, CH_IN_X), max(bb.min.Y, WALL_IN_REAR), min(bb.max.Y, WALL_IN_FRONT), CH_Z0 - OVER, SW_SEAT_Z))


def electronics_bays():
    return [_cut(hw.placed(c, at, BAY_ROT)) for c, at in ((RXESC, RX_C), (WESC, WE_C))]


def partition():
    """Rib in the gap between the pack bay and the electronics bay, from the stop wall front face to the front wall, base seat to deck."""
    gap0, gap1 = ELEC["battery"][0] + BAT_W / 2, min(RX_X[0], WE_X[0])
    if gap1 - gap0 < PARTITION_T:             # the bays touch: no room for a rib
        return []
    xm = (gap0 + gap1) / 2
    return [box_xy(xm - PARTITION_T / 2, xm + PARTITION_T / 2, STOP_FRONT_Y, WALL_IN_FRONT + OVER, SEAT_Z, DECK + OVER)]


def additions():
    return partition() if "partition" in LAYOUT else []


def cuts():
    return (motor_pockets() if "motor" in LAYOUT else []) + (battery_bay() if "battery" in LAYOUT else []) + electronics_bays() + switch_bay()


def carve(tub):
    """The tub less the pockets of the parts that reach into it. A part that clears the tub (the default) leaves it untouched; the cut can leave a
    sliver where an envelope grazes a fillet, so the result is healed (the pockets are the exact catalog solids, with their own curved faces)."""
    hit = [c for c in cuts() if (tub & c).volume > TOUCH]
    if not hit:
        return tub
    if "battery" in LAYOUT and (tub & battery_bay()[0]).volume > TOUCH:   # the pack notches the tub: it must also be able to leave downwards
        hit.append(pack_drop())
    if (tub & switch_bay()[0]).volume > TOUCH:   # the switch notches the tub: it must also be able to leave downwards
        hit.append(switch_drop())
    out = _one(tub.cut(*hit).clean())
    return out if out.is_valid else _one(out.fix())
