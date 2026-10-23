"""vert_mod masters: the printed weapon module on the Alt chassis deck. No dump in the pack matches its 16592 mm3 (open
item in the port guide); every value is a relation to the chassis, the weapon axis and the hardware, measured from the
RVRN_revdev STEP solid's faces (STEP frame)."""
import math

from robot.cad import fastener_catalog as fc
from .params_chassis import CH_H, IN_X, IN_Y, HY, WALL, M3, TAB_X_OUT, TAB_W, TAB_PITCH, TAB_HOLE_DY
from .params_drive import WY, WZ, UP_IN, UP_T

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
VM_T = WALL                            # shell / bulkhead / hollow walls
UP_R = 12.5                            # upright tail radius round the weapon axis; the ramp runs from the chassis front
#                                        inner wall at deck height up to the top of this circle and tops the whole module
UP_TAIL_T = 3.2                        # upright outer face at the tail: this far out from the inner face
TAPER_Y0 = 19.15                       # upright outer faces leave the chassis inner wall line here and run to the tail
BULK_T = 4.9                           # bulkhead, from one wall inside the chassis rear inner wall line
SLOT_R = 6.0                           # slot between the uprights: corner radius
FRONT_CLR = 0.95                       # leg front ends off the chassis front inner wall
LEG_IN = ((IN_X - 5.327, -IN_Y + FRONT_CLR), (IN_X - 11.317, -15.75))   # leg inner edge (deck line): front and rear points (STEP plane)
LEG_DRAFT = 48.48                       # leg inner faces lean back from the deck line (deg from horizontal)
ARCH_Y, ARCH_R = -6.766, 8.0          # arch over the leg opening: its lip line on the deck, corner rounds (STEP: square to the ramp)
ARCH_X = 8.056                         # arch corner centres off the middle (STEP)
ARCH_CH_ANG = 45.0                     # arch edge on the ramp: TOP_CH chamfer at this angle
NOTCH_R, NOTCH_RY = 8.0, 3.35         # side notch: round rear end, centred on the chassis inner wall line (its floor is tangent)
NOTCH_LOW_R, NOTCH_LOW_Y = 2.0, -6.64  # side notch: front corner round, tangent to the floor
NOTCH_Y = (-12.85, 12.85)              # notch mouth on the inner wall line
HOLLOW_EDGE_R = 1.0                    # hollow ceiling into the bulkhead face (STEP)
HOLLOW_FRONT, HOLLOW_R = -5.9, 3.0     # under-shell hollow: front edge beside the lip, corner rounds
POST_PAD_R = 4.0                       # pad round each rear column screw inside the hollow
POST_CB_R, POST_CB_DEPTH = 3.0, 2.5    # column screw counterbores: radius, floor above the deck
NOTCH_CH_Y0 = -0.69                    # the notch-wall chamfer is full size behind this y and runs out to the front corner
TOP_CH = 3.0                           # ramp edges over the side notches: equal-distance chamfer; bulkhead rear edge 45 deg
UP_OUT_CH = ((2.997, 2.942), (2.879, 3.063))   # upright outer top edges: (in on the ramp, down the face), left / right (STEP as drawn, TOP_CH nominal)
UP_IN_CH = (1.95, 2.58)                # upright inner top edges: chamfer across the top, down the face
UP_CH_END = 48.4                       # upright top chamfers run back to here
SIDE_POCKET = ((WY - 16.61, 22.01), 4.7, (20.0, 23.9), 7.0)   # upright outer pocket: round end (centre, r), front z span, depth
SIDE_POCKET_FRONT, POCKET_STEP = 2.73, 1.51   # pocket floor runs this far into the hollow wall; its slope starts behind the bulkhead face
SIDE_HOLE = (26.0, 21.6, 1.6)           # hole through each hollow side wall: y, z, radius
AXIS_HOLE_R = 4.0                      # through both uprights on the weapon axis (the MF85 OD seat on the right)
UP_RECESS_R, UP_RECESS_X = 6.0, 17.8   # bearing side: recess round the axis from this |x| out (prop-mount nut)
MOTOR_PCD = (16.0, 12.0)               # BE1806 base screws: 16 x 12 on the 45 deg diagonals
MOTOR_CB_R = 2.5                       # M2 cap counterbores on the left upright's outer side
SHROUD = (18.22, -7.22, -6.0, 17.0)    # motor-side shroud: outer radius reached at x, end face x, inner radius there
TUNNEL = ((-7.77, 16.97), (18.5, 25.45), 1.0)   # bulkhead tunnel from the hollow: x span, z span, rear wall left
TUNNEL_FLOOR_R = 1.0                   # tunnel's blind end rounded into its walls (STEP)
LEAD_SLOT_R, LEAD_SLOT_H = 2.0, 5.0    # left lead slot along the upright inner face: round ends, straight height (catalog lead stub)
PRONG_T = 3.0                          # prong: against the inner chassis tab, down to the chassis underside
PRONG_TOE = (38.82, 5.0)               # toe round: y, radius (sits on the chassis underside)
PRONG_HEEL = ((0.796, -0.606), 5.0)    # heel line normal (y, z), its fillet into the upright underside
PRONG_CLR, PRONG_FRONT = 0.1, 3.0      # off the chassis rear face; front web
PRONG_WEB, PRONG_BOSS = 2.0, 4.0       # prong window rim, boss round the cross bolt
GROOVES = (3, (4.54, 15.37), (9.955, 14.26), 28.31, 3.68, 5.07, 0.6)   # top grip grooves per side: n, x span, first centre, angle, width, pitch, depth
BIG = 1e3                              # a cut tool larger than the part
# -----------------------------------------------------------------------------------------------------------------------
DECK_TOP = CH_H                        # the module stands on the chassis deck
UP_X0 = UP_IN
TAPER = ((IN_X, TAPER_Y0), (UP_IN + UP_TAIL_T, WY + UP_R))
NOTCH_X = IN_X - NOTCH_R                 # notch floor
NOTCH_TOP = ((IN_X, NOTCH_RY), NOTCH_R)
NOTCH_LOW = ((NOTCH_X + NOTCH_LOW_R, NOTCH_LOW_Y), NOTCH_LOW_R)
BULK_Y = (IN_Y - VM_T, IN_Y - VM_T + BULK_T)
FRONT_Y = LEG_IN[0][1]
POST_CB_Z = DECK_TOP + POST_CB_DEPTH
UP_CH_Y = (BULK_Y[1] + SLOT_R, UP_CH_END)
MOTOR_HOLES = tuple((sd * r * math.cos(math.radians(45)), sd * sz * r * math.sin(math.radians(45)))
                    for r, sz in ((MOTOR_PCD[0] / 2, 1), (MOTOR_PCD[1] / 2, -1)) for sd in (1, -1))
MOTOR_HOLE_R = fc.clearance(2.0, "close") / 2
MOTOR_CB_X = UP_IN + UP_T
POST_HOLE_D = fc.clearance(2.0, "close")   # M2 module screws into the chassis column heat-sets
TAB_HOLE_R = fc.clearance(M3, "close") / 2
TAB_GAP = (TAB_X_OUT - TAB_PITCH, TAB_X_OUT - TAB_W)      # gap between the two chassis tabs (17.5 .. 23.5)
PRONG = (TAB_GAP[0], PRONG_T, 0.0)
LEAD_SLOT = (-(UP_IN - LEAD_SLOT_R), LEAD_SLOT_R, (WZ - LEAD_SLOT_H / 2, WZ + LEAD_SLOT_H / 2))

__all__ = [n for n in dir() if not n.startswith("__")]
