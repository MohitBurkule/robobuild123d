"""Side_Panel_alt_sm masters (TPU, STEP frame, right-hand part; the left one is its mirror). No dump exists for the "sm"
panel (ELVRN3.0_Side Panel is a larger family member): the values are relations to the chassis, the wheels and the
module, measured off the RVRN_revdev STEP solid's faces (its left solid, which sits clear of the chassis everywhere; the
right one is 0.25 mm inboard of its mirror)."""
import math

from robot.cad import fastener_catalog as fc

from .params_chassis import HX, HY, CH_H, AXLE_Y, AXLE_Z, BOSS_OUT, BOSS_R, BOSS_PITCH, TAB_X_OUT, TAB_W, TAB_PITCH, TAB_LEN, WALL, M3
from .params_drive import TYRE_R, WHEEL_OUT, FLOOR_LIFT
from .params_vert import TAB_GAP, PRONG_T

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
SP_T = WALL                            # TPU wall
FIT = 0.25                             # TPU running fit off the chassis tabs and the module prong
NUT_FIT = 0.05                         # thin-nut pocket over the nut's flats
TPU_HOLE_ALLOW = 0.1                   # TPU pilot over the tap drill (STEP tongue pilot 2.6)
UNDER = (46.16, 0.0853)                # underside plane: z 0 at this y, rising forward (the pod rakes the forks down)
GUARD_X = WHEEL_OUT - 2.2              # wheel-guard spine: its drafted wall leans in to an apex over this line
GUARD_END = (9.4, 9.6)                 # guard spines end this far ahead of / behind each axle (inside the tyre circle)
GUARD_R0, GUARD_DRAFT, GUARD_T = 12.814, 35.03, 3.28   # guard wall: offset from the spine at z 0, draft, normal thickness
GUARD_FACE = 3.0                       # the rear guard's inner face stands this far out from the spine above the tyre
GUARD_FRONT_CLR = 0.8                  # the rear guard's inner side is cut back from just ahead of its spine
GUARD_TIP_R = 0.5                      # round on the rear guard's top edge (its inner face meets the drafted outer face)
GROOVE = (16.98, 6.0, 3.0, 0.5, (2.62, 10.81), -0.857, 4, 3.0)   # diagonal grip grooves: first centre y, pitch, width, depth, z span, dy/dz, count, z of the first centre
WELL_CLR = 1.25                        # wheel wells round both axles over the tyre radius
LIP = 1.0                              # plate lip wrapping the boss sides
LIP_CLR = 0.3                          # lip off the boss obround
PLATE_CSK_SINK = 1.1                         # boss screw heads sit this far down their bores under the plate flank
PLATE_T = 1.8                          # plate on the boss under the countersunk M3 heads
PLATE_TOP_DROP, PLATE_FLAT = 1.0, 3.0  # plate top under the chassis top, flat this far either side of the middle
PLATE_OUT = (0.966, 0.259, 35.53)      # plate's slanted outer face n.(x, z) = d (15 deg)
STRUT_Y0 = 9.5                         # flanks from the plate's top out to each guard end start this far off the middle
STRUT_TOP = (34.5, 15.3, 1.3)          # flank top: x, z where it leaves the plate top, outward fall dz/dx
CROSS_Y0, CROSS_TOP = 37.8, 14.0       # crossbar front face behind the rear tyre, crossbar top
TONGUE_FRONT = (0.997, 0.078, 33.51)   # tongue front face n.(y, z) = d
TONGUE_TOP = (0.217, 0.976, 21.86)     # tongue top face
REAR_SLOPE = (0.819, 0.574, 39.82)     # crossbar / tongue rear face
ROOT_TOP = (0.340, 0.940, 24.10)       # fork-root top face
POCKET_X1, POCKET_CH = 32.25, 48.58    # pocket round the outer chassis tab: outer wall x, underside chamfer y + z
POCKET_R = 3.0                         # pocket outer corner round
ROOT_EDGE = (-0.707, 0.579, 0.406, 7.11)   # fork-root inner face n.(x, y, z) = d
FLARE_MIN = 0.3                        # the blend from the fork into the rear guard ends where it is this wide
FORK_FLOOR_CLR = 0.25                  # fork underside above the floor (clip_forks variant only)
FORK_TYRE_IN = 0.2                     # fork outer face inside the tyre's outer face
POCKET_END_CLR = 0.2                   # tab pocket's end wall past the chassis tab end
FORK_W = 5.74                          # fork prong width, its outer face just inside the tyre's outer face
FORK_T = 4.0                           # fork thickness over the underside
FORK_TIP = (98.61, (0.499, 0.867, 45.26), 83.22, 84.74)   # tip y, tip top plane, tooth riser y span
FORK_RISER = (0.867, 0.499)            # tooth riser face normal (-y, +z)
# -----------------------------------------------------------------------------------------------------------------------
GUARD_Y = (-(AXLE_Y - GUARD_END[0]), AXLE_Y - GUARD_END[0], AXLE_Y + GUARD_END[1])
WELL_R = TYRE_R + WELL_CLR
PLATE_X0 = HX + BOSS_OUT               # plate on the boss face
PLATE_X = (PLATE_X0, PLATE_X0 + PLATE_T)
LIP_X0 = PLATE_X0 - LIP
LIP_IN_R = BOSS_R + LIP_CLR
PLATE_OB = (BOSS_PITCH / 2, BOSS_R + SP_T, CH_H - PLATE_TOP_DROP, PLATE_FLAT)
WELL_X = (LIP_X0, GUARD_X + GUARD_FACE)
STRUT_Y1 = AXLE_Y - WELL_R             # the flanks end where the wheel wells begin
TONGUE_PILOT = fc.tap_drill(M3) + TPU_HOLE_ALLOW   # the cross bolt cuts its thread in the TPU tongue
TONGUE_X = (TAB_GAP[0] + PRONG_T + FIT, TAB_GAP[1] - FIT)   # between the module prong and the outer tab, a running fit off each
TAB_POCKET = (TONGUE_X[1], POCKET_X1, HY + TAB_LEN + POCKET_END_CLR, POCKET_CH)
FORK_X = (WHEEL_OUT - FORK_TYRE_IN - FORK_W, WHEEL_OUT - FORK_TYRE_IN)

__all__ = [n for n in dir() if not n.startswith("__")]
