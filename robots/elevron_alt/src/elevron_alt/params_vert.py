"""vert_mod masters: the printed weapon module (top shell + uprights) that sits on the Alt chassis deck. No dump in the
pack matches its 16592 mm3 (open item in the port guide), so the values are relations to the chassis and the weapon
axis, set from RVRN_revdev STEP sections."""
from .params_chassis import CH_H, IN_X, IN_Y, HY, TAB_LEN, TAB_X_OUT, TAB_W, TAB_PITCH, POSTS, WALL, M3
from .params_drive import WY, WZ, UP_IN, UP_T, BRG, MOTOR_SINK, MOTOR_R, LEAD_Y
from robot.cad import fastener_catalog as fc
import math
from .params_chassis import TAB_HOLE_DY
from .params_side import NUT_FIT

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
VM_T = WALL                            # frame / shell / bulkhead wall
SHELL_Y = (-8.0, 33.0)                 # sloped top shell: front edge on the deck, rear bulkhead face
SHELL_TOP = 30.0                       # shell top height at the bulkhead (STEP frame)
SHELL_FRONT = 22.5                     # height of the shell's front wall: the slope runs from its top edge
SHELL_W = (19.5, IN_X)                 # shell half widths at its front edge and from FRONT_FLARE_Y back
FRONT_FLARE_Y = (POSTS[-1][1] + 3.5, POSTS[-1][1] + 8.0)   # shell stays narrow past the rear column screws, then flares
MOTOR_PCD_R, MOTOR_SCREW = 6.25, 2.0   # BE1806 base: 4 x M2 on 12.5 PCD
N_MOTOR_SCREWS, MOTOR_PCD_PHASE = 4, 45.0
MOTOR_HOLE_CLR = 0.1                   # M2 clearance over the screw
MOTOR_CLR = 1.0                        # can pocket clearance: the can rim spins 1 mm off the upright (kin.rub_gap)
BOSS_R = MOTOR_R + MOTOR_CLR + VM_T     # upright boss round the weapon axis: the can pocket plus a printed wall
LEAD_W = 5.6                           # catalog phase-lead stub (5 wide) turned forward: slot in the pocket
DUCT = (3.5, 3.5)                      # phase-lead duct passage (x width, height along the deck): wire slot -> under the shell -> bulkhead -> lead stub
BIG = 1e3                              # a cut tool larger than the part
POST_PAD_R = 3.5                       # frame pad round each column screw (edge distance >= 1.5 d)
FRAME_LEG = 5.0                        # frame leg / rim width
PRONG_W = 3.5                          # prong carries the cross-bolt nut: a thin M3 nut plus a 1.7 wall
UP_WEB = 3.0                           # upright web thickness away from the axis boss (the STEP uprights are webs on a boss)
UP_RIM = 2.5                           # upright lightening window: rim width, and the solid kept round the axis boss
UP_WIN_R = 2.0                          # cross-bolt prong between the chassis tabs
# -----------------------------------------------------------------------------------------------------------------------
DECK_TOP = CH_H                        # the module stands on the chassis deck
TAB_GAP = (TAB_X_OUT - TAB_PITCH, TAB_X_OUT - TAB_W)      # gap between the two chassis tabs (17.5 .. 23.5)
PRONG_CLR = 0.5                        # prong off the outer tab
PRONG_X = (TAB_GAP[1] - PRONG_CLR - PRONG_W, TAB_GAP[1] - PRONG_CLR)
PRONG_Y = (HY, HY + TAB_HOLE_DY + (fc.nut(M3, "thin")[0] + NUT_FIT) / math.sqrt(3) + VM_T)   # past the tab end: a wall behind the nut
POST_HOLE_D = fc.clearance(M3, "normal")                  # module screws into the chassis columns
BRG_SEAT_R = BRG[1] / 2

__all__ = [n for n in dir() if not n.startswith("__")]
