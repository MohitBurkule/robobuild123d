"""Side_Panel_alt_sm masters (TPU, STEP frame, right-hand part; the left one is its mirror). No dump exists for the
"sm" panel (ELVRN3.0_Side Panel is a larger family member), so the values are relations to the chassis and the
wheel, set from STEP sections."""
from .params_chassis import HX, HY, AXLE_Z, DECK_Z, CH_H, BOSS_OUT, BOSS_PITCH, BOSS_R, TAB_X_OUT, TAB_W, TAB_LEN, WALL
from .params_drive import WHEEL_OUT, FLOOR_LIFT, TYRE_R
from .params_chassis import AXLE_Y, TAB_HOLE_Z, M3
import math
from robot.cad import fastener_catalog as fc

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
SP_T = WALL                            # TPU wall
SKIN_GAP = 0.8                         # skin inner face off the wheel's outer face at the top
SKIN_BATTER = 29.0                     # deg from vertical: the skin leans out to the floor (STEP 42.5,16 -> 51,1.4)
SKIN_BOT_Z = 1.4                       # skin foot height (STEP frame), clear of a 3.6 mm step
SKIN_OVER_AXLE = 3.0                   # skin top this far over the axle (STEP 11.5)
FORK_W = 5.8                           # fork prong width
FORK_TIP_Y = 98.6                      # prong tip (STEP)
FORK_KNEE_Y = 70.0                     # prong reaches its floor run here
FORK_T = 4.0                           # prong floor-run thickness
FLOOR_CLR = 0.25                       # prong underside above the floor
FORK_TIP_T = 1.5                       # prong tip thickness (TPU min wall)
WHEEL_CLR = 1.0                        # crossbar behind the rear tyre
PLATE_T = 3.0                          # plate on the boss: carries the countersunk M3 heads
NUT_FIT = 0.05                         # press fit of the cross-bolt nut in the TPU land
CROSS_LAND = 2.0                       # crossbar land under the countersunk cross-bolt head (flush, clear of the tyre); its driver path opens out through the skin
# -----------------------------------------------------------------------------------------------------------------------
PLATE_X = (HX + BOSS_OUT, HX + BOSS_OUT + PLATE_T)        # plate on the boss face
PLATE_Y = BOSS_PITCH / 2 + BOSS_R + SP_T                  # half length round the obround
PLATE_Z = (2 * AXLE_Z - DECK_Z, DECK_Z)                   # symmetric about the axle, top at the deck underside
SKIN_TOP = (WHEEL_OUT + SKIN_GAP, AXLE_Z + SKIN_OVER_AXLE)   # inner top corner of the skin (x, z): the wheel top stays proud
STRUT_Y = (PLATE_Y - SP_T, PLATE_Y)                       # front strut from the plate's rear end out to the skin, ahead of the tyre
CROSS_Y = (AXLE_Y + TYRE_R + WHEEL_CLR, HY + TAB_LEN + SP_T)   # rear crossbar on the outer tab face, behind the rear tyre, closed past the tab end
SKIN_Y = (STRUT_Y[0], CROSS_Y[1])                       # skin from the strut to the rear of the tabs
NUT_R = (fc.nut(M3, "thin")[0] + NUT_FIT) / math.sqrt(3)   # cross-bolt nut pocket corner radius
CROSS_Z = (TAB_HOLE_Z - NUT_R - SP_T, TAB_HOLE_Z + NUT_R + SP_T)   # crossbar: a wall round the captive nut above and below
CROSS_TOP = CROSS_Z[1]
FORK_X = (WHEEL_OUT - FORK_W - 0.4, WHEEL_OUT - 0.4)      # prong inside the tyre's outer face line
FLOOR_Z = -FLOOR_LIFT                                     # floor in the STEP frame
CSK_SCREW = "M3x8"

__all__ = [n for n in dir() if not n.startswith("__")]
