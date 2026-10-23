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
POST_PAD_R = 4.0                       # frame pad round each column screw (edge distance >= 1.5 d)
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


# ---- ramp-module relations (STEP RVRN_revdev vert_mod) ---------------------------------------------------------------
UP_R = 12.5                            # upright tail radius round the weapon axis (the ramp runs up to its top)
UP_X0 = 13.3                           # upright inner faces (slot between the uprights)
TAPER = ((IN_X, 19.15), (16.5, WY + UP_R))   # upright outer face in plan: off the chassis inner wall to the tail
BULK_Y = (IN_Y - VM_T, IN_Y + 2.9)     # bulkhead faces
SLOT_R = 6.0
FRONT_Y = -IN_Y + 0.95                 # leg front ends
LEG_IN = ((22.36, FRONT_Y), (16.37, -15.75))   # leg inner edge
ARCH_Y, ARCH_R = -6.82, 8.0            # front opening between the legs
LEG_DRAFT = 48.5                       # leg inner faces lean back from the deck line (deg from horizontal)
NOTCH_TOP = ((IN_X, 3.35), 8.0)        # side notch: round rear end
NOTCH_LOW = ((21.5, -6.64), 2.0)       # side notch: front corner
NOTCH_X = 19.5
NOTCH_Y = (-12.85, 12.85)              # notch mouth on the inner wall line
HOLLOW_FRONT, HOLLOW_R = -5.9, 3.0

SIDE_POCKET = ((42.59, 22.01), 4.7, (20.0, 23.9), 7.0)   # upright outer pocket: round end (centre, r), front z span, depth
SIDE_POCKET_FRONT, POCKET_STEP = 2.73, 1.51   # pocket floor runs this far into the hollow wall; its slope starts behind the bulkhead face
UP_RECESS_R, UP_RECESS_X = 6.0, 17.8   # bearing-side recess round the axis, from this |x| out
AXIS_HOLE_R = 4.0
MOTOR_HOLES = ((-5.66, -5.66), (-4.24, 4.24), (4.24, -4.24), (5.66, 5.66))   # BE1806 16 x 12 pattern about the axis (y, z)
MOTOR_HOLE_R, MOTOR_CB_R, MOTOR_CB_X = 1.1, 2.5, 17.3
SHROUD = (18.22, -7.22, -6.0, 17.0)    # motor-side shroud: outer radius reached at x, end face x, inner radius there
TUNNEL = ((-7.77, 16.97), (18.5, 25.45), 33.2)   # bulkhead wire tunnel: x span, z span, rear end y
LEAD_SLOT = (-11.3, 2.0, (21.0, 26.0))  # left lead slot along the upright inner face: x, r, z centres
BULK_CH = 61.96                        # bulkhead rear top chamfer: y + z
PRONG = (17.5, 3.0, 0.0)               # prong: inner face |x|, thickness, bottom z
PRONG_TOE = ((38.82, 5.0), 5.0)       # bottom round (centre, r)
PRONG_HEEL = ((0.796, -0.606), 5.0)   # heel line normal (y, z), fillet into the upright underside
PRONG_CLR, PRONG_FRONT = 0.1, 3.0      # off the chassis rear face; front web
TAB_HOLE_R = 1.6
TOP_CH = 3.0                           # ramp top outer edges: equal-distance chamfer
CHAMFER_GROUPS = ("notch",)
ARCH_DRAFT = 40.2                      # arch flare above the lip (deg from vertical)
UP_IN_CH, UP_CH_Y = (1.95, 2.58), (BULK_Y[1] + SLOT_R, 48.4)   # upright top chamfers: inner size, run along y
POST_CB_R, POST_CB_Z = 3.0, DECK_TOP + 2.5   # column screw counterbore and its floor
GROOVES = (3, (4.54, 15.37), (9.955, 14.26), 28.31, 3.68, 5.07, 0.6)   # top grip grooves per side: n, x span, first centre, angle, width, pitch, depth
PRONG_WEB, PRONG_BOSS = 2.0, 4.0       # prong window rim, boss round the cross bolt

__all__ = [n for n in dir() if not n.startswith("__")]
