"""GNC parametric dimensions (masters + relations).

GNC is a 150 g UK antweight: two separate black printed drive pods (two N10 gearmotors and two outboard wheels each,
sloped wedge nose and a green FR4 fork tine on each nose) joined by a low centre bridge that carries a micro servo
lying on its side. The servo swings a yellow printed arm with a wide slotted hook "rake" head (5 hooked tines).

Frame: +X left, +Y forward (forks), +Z up, floor at Z = 0.
"""
import importlib.util
import math
import os

from robot import catalog
from robot.cad import bay as bay_lib
from robot.cad import fastener_catalog as fc

_HW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "revron", "src", "revron", "hw.py")
_spec = importlib.util.spec_from_file_location("revron_hw", os.path.abspath(_HW_PATH))
hw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hw)

# =================================================================================================== MASTERS
FOOTPRINT_SQUARE = 150.0      # RULE aws2025
MASS_LIMIT_G = 150.0          # RULE antweight

DRIVE_MOTOR_ID = "n10_300rpm_6v"
SERVO_ID = "servo_cs07"
BATTERY_ID = "lipo_2s_180"
ESC_ID = "malenki_nano"
SWITCH_ID = "switch_bbb_ant_rvrn2"
INSERT_ID = "heatset_m2"

PRINT_MAT = "pla"             # PHOTO: black printed pods
ARM_MAT = "petg"              # PHOTO: yellow printed arm (tough, not brittle)
SHEET_MAT = "pc"              # lids
FORK_MAT = "petg"             # PHOTO: green fork tines with 3D beveled tip wedge

WALL = bay_lib.DEFAULT_WALL
CLEAR = bay_lib.PRINTED_FIT_CLEARANCE
RUN_CLEAR = bay_lib.RUNNING_CLEARANCE
EPS = bay_lib.CUT_OVERSHOOT

WHEEL_D = 26.0                # PHOTO: knurled black wheels
WHEEL_W = 9.0
TYRE_T = 3.0                  # tread ring radial thickness
WEB_T = 2.0                   # hub web thickness
HUB_R = 3.5                   # hub boss radius
KNURL_N = 24                  # tread grooves (photo: knurled tread)
KNURL_W = 1.0
KNURL_D = 0.6

BELLY_Z = 2.5                 # underside of the pods off the floor
TUB_Z1 = 22.0                 # top rim of the pods (lid seat)
LID_T = 1.5
GAP_HALF = 16.0               # half width of the open channel between the pods (servo + arm lane)
POD_W = 28.0
POD_Y0 = -45.0                # rear face
POD_Y1 = 40.0                 # nose front face
NOSE_Y0 = 26.0                # start of the sloped nose top
NOSE_Z = 12.0                 # nose front-face top height
WHEEL_YR = -30.0
WHEEL_YF = 12.5

MOTOR_ROOT_INSET = 0.8
MOTOR_FIT = 0.05
MOTOR_ENV_Y = 5.0
MOTOR_ENV_Z = 6.0
SHAFT_HOLE_FIT = 0.05
SHAFT_HOLE_OUT = 1.5
BORE_FLAT_Z = 1.0
BORE_FLAT_W = 3.6
BORE_BOX_Z_OFF = 1.5
BORE_BOX_H = 3.0

SCREW_D = 2.0
SCREW_HEAD = "button"

# =================================================================================================== RELATIONS
MOTOR_SHAFT = catalog.find(DRIVE_MOTOR_ID).shaft
MOTOR_L = MOTOR_SHAFT["at"][0] - hw.reach(DRIVE_MOTOR_ID)["x0"]
SERVO_BB = hw._solid(SERVO_ID).bounding_box()
SERVO_L = SERVO_BB.max.X - SERVO_BB.min.X           # 32 incl. ears
SERVO_BODY_L = 23.0                                  # CAT: body box length (ears excluded)
SERVO_T = SERVO_BB.max.Y - SERVO_BB.min.Y            # 12
SERVO_H = SERVO_BB.max.Z - SERVO_BB.min.Z            # 22.7
SERVO_EAR_Z0 = 5.65                                  # CAT: ear flange underside in servo frame (+Z = output)
BAT_L, BAT_W, BAT_H = hw.size(BATTERY_ID)
ESC_L, ESC_W, ESC_H = hw.size(ESC_ID)
SW_L, SW_W, SW_H = hw.size(SWITCH_ID)
SW_BB = hw._solid(SWITCH_ID).bounding_box()

SCREW_CLEAR_D = fc.clearance(SCREW_D)
INSERT_OD, INSERT_L = fc.insert(SCREW_D)
INSERT_HALF_L = INSERT_L / 2

# --- heights
AXLE_Z = WHEEL_D / 2
FLOOR_Z = BELLY_Z + WALL                  # top of the pod floor
LID_Z1 = TUB_Z1 + LID_T
TUB_H = TUB_Z1 - BELLY_Z

# --- widths
POD_XI = GAP_HALF                         # inner face of a pod
POD_XO = GAP_HALF + POD_W                 # outer face
POD_XC = (POD_XI + POD_XO) / 2
WHEEL_X = POD_XO + RUN_CLEAR + WHEEL_W / 2
OVERALL_W = 2 * (WHEEL_X + WHEEL_W / 2)
MOTOR_ROOT_X = POD_XO - MOTOR_ROOT_INSET
MOTOR_INNER_X = MOTOR_ROOT_X - MOTOR_L
MOTOR_AT_X = MOTOR_ROOT_X - MOTOR_SHAFT["at"][0]
POD_IN_XI = POD_XI + WALL                 # inner cavity faces of a pod (|x|)
POD_IN_XO = POD_XO - WALL
POD_L = POD_Y1 - POD_Y0
POD_YC = (POD_Y0 + POD_Y1) / 2

# --- motor housings (closed top, open outboard face for axial insertion, open under-tunnel for wiring)
HOUSE_HALF_Y = MOTOR_ENV_Y + MOTOR_FIT + WALL
HOUSE_X0 = MOTOR_INNER_X - WALL            # inner end wall of the housing (|x| = 20.05 mm)
POCKET_HALF_Y = MOTOR_ENV_Y + MOTOR_FIT
POCKET_HALF_Z = MOTOR_ENV_Z + MOTOR_FIT
TERM_SLOT_H = 5.0                          # slot in the housing end wall for the motor leads
TERM_SLOT_W = 5.5

# --- nose + front plow bumper
NOSE_RUN = POD_Y1 - NOSE_Y0
NOSE_DROP = TUB_Z1 - NOSE_Z
NOSE_DEG = math.degrees(math.atan2(NOSE_DROP, NOSE_RUN))
NOSE_WALL_DY = WALL / math.cos(math.radians(NOSE_DEG))  # vertical thickness of the sloped top skin
PLOW_Y1 = POD_Y1 + 10.5
PLOW_TIP_Z0 = 1.0
PLOW_TIP_Z1 = 2.3
PLOW_STEP_Y = POD_Y1 + 3.0
PLOW_STEP_Z = 11.8
CAV_FRONT_Y = POD_Y1 - 6.0                 # solid nose block ahead of here (fork seat)
PLOW_POCKET_DX = (-4.2, 3.2)               # two bolt-access pockets on the sloped front plow face
PLOW_POCKET_HW = 1.8
PLOW_POCKET_Y0 = POD_Y1 + 1.8
PLOW_POCKET_Y1 = POD_Y1 + 4.4
PLOW_POCKET_Z0 = 4.0
PLOW_POCKET_Z1 = 9.0

# --- forks (tines emerging from the outer-lower corner of the front plow blocks)
FORK_T = 1.6
FORK_W = 4.2                               # 4.2 mm wide so 2.2 mm M2 clearance holes leave >= 1.0 mm wall on each side
FORK_TIP_W = 5.0
FORK_TIP_L = 9.0
FORK_TIP_PEAK_DY = 1.2
FORK_TIP_PEAK_Z = 3.2
FORK_TIP_GAP = 0.6                         # tine tip above the floor
FORK_RUN = 36.0                            # horizontal reach ahead of the front plow
FORK_DEG = 14.0                            # tine slope
FORK_SEAT_L = 11.0                         # length of the sloped seat inside the front plow block
FORK_BOLT_S = (3.2, 7.6)                   # bolt stations along the tine from its root (4.4 mm apart, >= 3.2 mm from root)
FORK_X = POD_XO - 4.5                      # PHOTO: forks emerge near the outer edge of each front plow block
FORK_LEN = FORK_RUN / math.cos(math.radians(FORK_DEG)) + FORK_SEAT_L
# the tine top surface passes through the tip point; root station s = 0 at the back of the seat
_FS, _FC = math.sin(math.radians(FORK_DEG)), math.cos(math.radians(FORK_DEG))
FORK_TIP_Y = POD_Y1 + 1.0 + FORK_RUN
FORK_TIP_Z = FORK_TIP_GAP + FORK_T / _FC   # top surface height at the tip
FORK_ROOT_Y = FORK_TIP_Y - FORK_LEN * _FC
FORK_ROOT_Z = FORK_TIP_Z + FORK_LEN * _FS
FORK_SEAT_BELLY = BELLY_Z                  # seat underside never below the belly line
FORK_BORE_DEPTH = 5.2
FORK_CHAN_Z_OFF = 8.0 - FORK_T - 0.1
FORK_CHAN_H = 16.0
FORK_CHAN_EXTRA_L = 1.0
FORK_CBORE_R = 2.1
FORK_CBORE_Z = 8.0
FORK_CBORE_H = 16.0


def fork_point(s, h=0.0):
    """World (y, z) of a point at station s along the tine top surface (root at s = 0), offset h along local +Z."""
    return (FORK_ROOT_Y + s * _FC + h * _FS, FORK_ROOT_Z - s * _FS + h * _FC)


# --- centre bridge: floor plate under the servo + rear hollow cross member with a wire channel
BRIDGE_Y0 = POD_Y0
BRIDGE_Y1 = 2.0
XBAR_Y1 = POD_Y0 + 9.0                     # rear cross member front face
XBAR_Z1 = 14.0                             # cross member top
CHAN_W = 5.5                               # wire channel (Y) through the cross member
CHAN_H = 6.0
CHAN_Z0 = FLOOR_Z + 0.5
CHAN_Y_INSET = 1.0
HOUSE_UNDER_W = 5.5

# --- servo lying on its side against the right pod, output axis along +X
SERVO_X = -POD_XI + CLEAR + SERVO_H / 2
SERVO_FACE_X = SERVO_X + SERVO_H / 2
SERVO_Z = FLOOR_Z + SERVO_T / 2 + MOTOR_FIT
SERVO_Y = -12.0
SERVO_OUT_DY = (SERVO_L - SERVO_T) / 2     # output spline one half-width in from the front end
PIVOT_Y = SERVO_Y + SERVO_OUT_DY
PIVOT_Z = SERVO_Z
CRADLE_WALL = WALL
CRADLE_X1 = SERVO_X + SERVO_EAR_Z0 - CLEAR  # cradle end walls stop under the ear flange
CRADLE_Z1 = SERVO_Z + SERVO_T / 2 - 2.0     # cradle walls rise to 2 mm below the servo top

# --- arm + rake head (built in the pivot frame: arm along local +Y, rotated to ARM_REST_DEG about X)
# Under Rot(110, 0, 0): local +Y points UP (+Z) and slightly BACK (-Y); local -Z points FORWARD (+Y) and slightly DOWN (-Z);
# local +Z points BACKWARD (-Y) and slightly UP (+Z).
ARM_REST_DEG = 110.0                        # PHOTO: arm bar leans back ~20 deg from vertical
ARM_MIN_DEG = -80.0                         # swing forward (hammer / grab stroke)
HUB_R_ARM = 4.6
HUB_X0 = SERVO_FACE_X + 0.3
HUB_X1 = POD_XI - 1.2
ARM_X = (HUB_X0 + HUB_X1) / 2
ARM_T = HUB_X1 - HUB_X0                     # arm hub width along X
ARM_BAR_X1 = 8.5                            # right-hand (+X) face of the central arm post
ARM_L = 52.0                                # pivot to ring centre along local +Y
ARM_W = 9.2                                 # PHOTO: thick sturdy arm bar in side view
ARM_ROOT_W = 8.4
HEAD_W = 76.0                               # PHOTO: 5-tine rake width spanning across the pods
HEAD_RO = 20.5
HEAD_RI = 15.0
HEAD_DZ = -4.5                              # ring centre slightly forward of the arm bar axis so the arm bar joins the bottom-rear of the C-arch
HEAD_GAP_DEG = (-225.0, -45.0)              # 180 deg open front-bottom mouth (-225 deg = +135 deg around to -45 deg through -135 deg)
TINES = 5
TINE_T = 8.0
SPINE_DEPTH = 4.0                           # spine depth near the arm junction
SPINE_DY0 = -19.5
SPINE_DY1 = -13.5
SPINE_DZ0 = 1.0
SPINE_DZ1 = 9.0
TAIL_ANG0 = 105.0
TAIL_ANG1 = 135.0
TAIL_PTS = (
    (-11.5, 19.5),
    (-16.0, 22.8),
    (-19.5, 26.2),
    (-21.2, 28.0),
    (-22.2, 26.5),
    (-20.5, 16.5),
    (-19.5, 1.0),
    (-13.5, 1.0),
)
TAIL_L = 13.0                               # PHOTO: curved lower rear tail on each tine
TAIL_TIP_W = 1.2
SPINE_X0 = -HEAD_W / 2

# --- wheel spoke cutouts
WHEEL_SPOKES = 3
WHEEL_SPOKE_PHASE = 30.0
WHEEL_WIN_IN_PAD = 0.8
WHEEL_WIN_OUT_PAD = 0.8
WHEEL_WIN_ANG_IN = 34.0
WHEEL_WIN_ANG_OUT = 38.0

# --- electronics
BAT_X = POD_XC
BAT_Y = (WHEEL_YR + HOUSE_HALF_Y + WHEEL_YF - HOUSE_HALF_Y) / 2
BAT_Z = FLOOR_Z + BAT_H / 2
BAT_RIM_REAR_TRIM = 4.5
ESC_X = -(POD_IN_XO - CLEAR - ESC_W / 2)
ESC_Y = BAT_Y
ESC_Z = FLOOR_Z + ESC_H / 2
SW_X = -(POD_IN_XI + CLEAR + SW_W / 2)
SW_Y = BAT_Y
SW_TRAY_HALF_Y = 1.2
SWITCH_POKE_Z = 0.5
SW_Z = LID_Z1 + SWITCH_POKE_Z - SW_BB.max.Z
BAY_WALL_H = 2.5                            # low locating walls round the battery (top at 6.0 mm, below motor wire tunnel at 6.95 mm)
BAY_FIT = 0.25

# --- lids + inserts (PHOTO: button-head lid screws sit near the INNER edge of each pod lid)
LID_INSET = 4.0
LID_PAD_X = POD_XI + LID_INSET
LID_PAD_D = 6.5
LID_PAD_H = 6.0
LID_BORE_EXTRA = 2.2
LID_SCREWS_Y = (POD_Y0 + 6.0, NOSE_Y0 - 5.0)
LID_Y0, LID_Y1 = POD_Y0, NOSE_Y0
LID_SLOT_R = 0.5

OVERALL_L = FORK_TIP_Y


def check():
    problems = []
    if MOTOR_INNER_X < POD_IN_XI + WALL:
        problems.append("motor does not fit across the pod")
    if BAT_L + 2 * CLEAR > (WHEEL_YF - HOUSE_HALF_Y) - (WHEEL_YR + HOUSE_HALF_Y):
        problems.append("battery does not fit between the motor housings")
    if MOTOR_SHAFT["len"] < RUN_CLEAR + WHEEL_W * 0.6:
        problems.append("motor shaft too short")
    if HUB_X1 - HUB_X0 < 4:
        problems.append("no room for the arm hub")
    return problems
