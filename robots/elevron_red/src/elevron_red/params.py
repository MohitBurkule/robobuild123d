"""Elevron Red masters (mm). z = 0 is the wheel axle, +y forward, +x is the robot's right.

Masters come from the Elevron 3.0 "Alt" reference assembly (chassis footprint, wheel stations, side panel
reach, N10 drive stack) and from the two AWS photos (servo lifter module, rear pods, fork taper). Everything
else is derived from them below; part code only uses these names.
"""

# --- drive (Alt assembly: Scalextric F1 tyres on N10 gearmotors) ---
WHEEL_R = 10.75          # tyre outer radius
WHEEL_W = 9.5            # tyre width
HUB_R = 5.5              # hub / tyre bore radius
TRACK_X = 37.0           # wheel centre |x|
AXLE_Y = 26.0            # wheel centre |y| (front +, rear -)
MOTOR = "bbb_n10_1000rpm"
MOTOR_BACK = 12.75       # catalog: body rear (terminal tabs) behind the motor origin
MOTOR_GB = 11.25          # catalog: gearbox face ahead of the origin
MOTOR_SHAFT = 9.0       # catalog: shaft length past the gearbox face
MOTOR_W, MOTOR_H = 12.0, 10.0
SHAFT_BITE = 5.0         # shaft length inside the hub

# --- chassis tub (Alt chassis: 65 wide, 75.8 long, 17 tall) ---
CH_W = 65.0
CH_REAR = -33.3
CH_FRONT = 42.5
CH_H = 17.0
WALL = 1.6
FUSE_LAP = 0.6           # overlap between two colours printed as one body
FIT = 0.25               # pocket clearance per side
WHEEL_GAP = 1.25         # tyre to printed wall
RAMP = 9.0               # front top chamfer (wedge face)

# --- side panels (Alt side panel reach + photo rear pods) ---
SP_TOP = 9.0             # pod top above the axle
SP_LOW = 7.0 
WEB_PLATE = 2.5          # web top plate thickness
WEB_Z0 = -2.0           # side panel web bottom (keyed into the chassis wall)            # rear pod / web top (wheels show above)
SP_OUT = 52.0            # outer face |x|
SP_REAR = -37.0          # rear pod tail
FORK_TIP_Y = 98.6        # fork tip (Alt side panel)
FORK_W_ROOT = 9.0        # fork plan width at the pod
FORK_W_TIP = 3.5         # fork plan width at the tip
FORK_TIP_H = 1.6         # blade thickness at the tip
POD_SKIN = 1.6
VENT_W, VENT_D = 1.6, 0.6  # pod vent grooves (width, depth)
POD_NOSE = 14.0          # pod top runs on past the wheel before the fork rakes down
KEY_TRIM = 2.0           # side panel tongue / flank slot stop this far short of the wheel wells
TAB = 1.2                # side panel key depth into the chassis wall

# --- lifter module (photos: servo housing left of a raked arm, pivot at the rear) ---
MODULE_SIDE = -1         # lifter module built for +x housing, then mirrored: housing on +x (robot right) when -1 (photo)
SERVO = "servo_cs07"
SERVO_L, SERVO_W, SERVO_H = 23.0, 12.0, 22.7   # catalog body (output axis along SERVO_H)
SERVO_EAR_L = 32.0
SERVO_OUT_FROM_END = 6.0                         # output spline from the rear end of the body
HOUSING_X0 = -26.0                               # housing left face
HOUSING_FRONT = 20.0                             # housing front face y
HOUSING_CHAMFER = 3.0
HOUSING_NOSE = 12.0                              # front slope of the housing
HOUSING_ROOF = 1.5                                # extra roof over the servo
PIVOT_BACK = 8.5                                 # pivot ahead of the chassis rear face
PIVOT_Z = 30.0                                   # pivot height above the axle (photo: highest point)
LUG_T = 4.0                                      # pivot lug on the housing
ARM_NOSE = 5.0                                   # arm depth at the knee
ARM_DEPTH = 12.0                                 # arm plate depth behind the knee
ARM_T = 12.0                                     # arm plate thickness
ARM_GAP = 2.6                                    # housing face to arm boss
ARM_BOSS_R = 8.0
HORN_GAP = 0.4                                   # horn to housing / arm
HORN_HUB_R, HORN_W, HORN_L = 3.5, 5.0, 14.0      # white servo horn (photo: lever standing above the housing)
ARM_TIP_Y = 88.0                                 # arm blade tip
ARM_RAIL = 2.5                                   # red top rail depth
ARM_BLADE = 14.0                                 # red blade tip length
ARM_LIFT_DEG = 60.0
CLEAR = 1.0                                      # arm above the chassis top at rest
ARM_STEP = 2.5                                   # photo: the top edge steps down part way along the rake
ARM_STEP_AT = 0.4                                # step position, fraction of the rake from the boss
PIVOT_SCREW = "M3x25"                            # photo: red-capped M3 through the arm boss, stud + nut past the lug
PIVOT_D, PIVOT_L = 3.0, 25.0
CAP_R, CAP_T = 3.5, 1.0                          # red washer under the pivot screw head
NUT = "nut_m3_thin"
NUT_T = 1.8
NUT_AF = 5.5                                     # nut across flats (hex pocket in the lug)

# --- lid / cover split (photo: black top plate under a red screwed servo cover) ---
LID_T = 1.6                                      # chassis top plate, screwed down; the housing is printed on it
COL_R = 2.45                                     # lid screw column radius (merges with the motor cradle wall)
COVER_COL_R = 2.7                                # cover screw columns: 1.5 mm round the 2.4 clearance hole
LID_SCREWS = ((28.8, 0.0), (-28.8, 0.0))         # world (x, y): one in each side wall; the lid posts key it into the cradles
LID_BOSS_R, LID_BOSS_H = 3.4, 1.0                # raised pads round the lid screw heads (the plate alone is too thin for the counterbore)
SERVO_HOLD = 0.1                                 # cover pad clearance over the servo top
PILOT_R, PILOT_PRE = 0.8, 1.5                    # M2 pilot pre-drilled into the screw columns from their seat face
COVER_COLS = ((-19.5, 3.6), (-12.75, 3.6), (-6.0, 3.6))         # module (x, y): cover screws into columns in the housing, ahead of the servo
COVER_Y1 = 7.5                                   # cover front edge (the housing keeps the sloped nose)
SB_X1, SB_Y, SB_HALF, SB_Z0 = 39.0, 7.0, 2.5, -6.0   # side panel screw blocks on the chassis flank
SIDE_SCREW_X = 36.5
MARK_X, MARK_Y = -14.0, -14.0                    # module (x, y) of the "01" on the cover top
WELL_R = 1.2                                     # wheel well inner corners rounded (no sharp notch at the lid joint)
POD_ROUND = 3.0                                  # photo: pods rounded along the outer top edge

# --- electronics (cavity layout) ---
BATTERY = "lipo_2s_180"
BAT_L, BAT_W, BAT_H = 28.0, 18.0, 10.0
ESC = "malenki_nano"
ESC_L, ESC_W, ESC_H = 23.0, 16.0, 5.0
SWITCH = "switch_slide_12x4"
SW_L, SW_W, SW_H = 11.8, 3.8, 4.0
BAY_Y = 0.0             # battery / ESC row centre
SW_Y = 12.0
SW_LEAD_W = 2.0          # lead window in the switch cradle cap
SW_LIP_L, SW_LIP_W = 5.0, 0.8   # belly slot lips that carry the switch


# ---------------- derived ----------------
def ground_z():
    return -WHEEL_R


def ch_z0():
    return -CH_H / 2


def ch_top():
    return CH_H / 2


def ch_len():
    return CH_FRONT - CH_REAR


def ch_yc():
    return (CH_FRONT + CH_REAR) / 2


def tyre_x0():
    """inner face of a tyre (|x|)"""
    return TRACK_X - WHEEL_W / 2


def well_x():
    """chassis wall face beside a wheel (|x|)"""
    return tyre_x0() - WHEEL_GAP


def well_half():
    return WHEEL_R + WHEEL_GAP


def cavity_half_w():
    return well_x() - WALL


def motor_origin_x():
    return tyre_x0() + SHAFT_BITE - (MOTOR_GB + MOTOR_SHAFT)


def floor_top():
    return ch_z0() + WALL


def pod_inner_x():
    return TRACK_X + WHEEL_W / 2 + WHEEL_GAP


def mid_half_y():
    """side panel web between the wheels reaches |y| < this"""
    return AXLE_Y - WHEEL_R - WHEEL_GAP


def pod_front_y():
    return AXLE_Y + WHEEL_R + 2 * WHEEL_GAP + POD_SKIN


def servo_box():
    """servo envelope after rot [90, 0, 90]: (x len, y len, z len)"""
    return SERVO_H, SERVO_L, SERVO_W


def servo_center():
    sx, sy, sz = servo_box()
    x = HOUSING_X0 + WALL + FIT + sx / 2
    y = CH_REAR + WALL + FIT + max(sy, SERVO_EAR_L) / 2
    z = ch_top() + sz / 2 + FIT
    return x, y, z


def housing_x1():
    sx, _, _ = servo_box()
    return servo_center()[0] + sx / 2 + FIT + WALL


def housing_top():
    return servo_center()[2] + servo_box()[2] / 2 + FIT + WALL + HOUSING_ROOF


def pivot():
    return housing_x1() + ARM_GAP, CH_REAR + PIVOT_BACK, PIVOT_Z


def servo_out():
    """servo output spline (horn centre) on the arm-side face"""
    x, y, z = servo_center()
    return housing_x1(), y + servo_box()[1] / 2 - SERVO_OUT_FROM_END, z


def arm_x0():
    return pivot()[0]


def arm_x1():
    return arm_x0() + ARM_T


def world_x(x):
    """module-frame x to world x (the lifter module is drawn housing-left, arm-right, then mirrored)"""
    return -x if MODULE_SIDE < 0 else x


def bat_center():
    """battery turned lengthwise (rot z 90) against the right wall of the cavity, on the floor"""
    return -(cavity_half_w() - BAT_W / 2 - 3.2), BAY_Y, floor_top() + BAT_H / 2 + 0.1


def esc_center():
    """ESC turned lengthwise (rot z 90) against the left wall, leads clear of the wall"""
    return cavity_half_w() - ESC_W / 2 - 3.5, BAY_Y, floor_top() + ESC_H / 2 + 0.1


def z_split():
    """housing / cover split: where the side chamfers start (just above the servo top plus its fit)"""
    return max(housing_top() - HOUSING_CHAMFER, servo_center()[2] + servo_box()[2] / 2 + FIT)


def lid_z0():
    return ch_top() - LID_T


def servo_lead():
    """servo signal lead exit (module frame): the body end face toward +y, at mid height"""
    x, y, z = servo_center()
    return x, y + servo_box()[1] / 2, z
