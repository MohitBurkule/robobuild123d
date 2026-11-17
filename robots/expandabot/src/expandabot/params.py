"""Expandabot (Team Bits Everywhere / Adam Stanley) parametric dimensions.

Every number in the CAD comes from here. Two kinds of bindings:
  MASTERS    values read from the AWS rules, the reference photos (see REFERENCE.md), or the part catalogue
  RELATIONS  everything else, derived from the masters so the assembly stays consistent when a master moves

Coordinate frame:
  +X  left (outboard toward left wheel / left side plate / left clamp arm)
  +Y  forward (toward the central flipper tip and flanking lobster-claw clamping arms)
  +Z  up (floor at Z = 0)
"""
import importlib.util
import math
import os

from robot import catalog
from robot.cad import bay as bay_lib
from robot.cad import fastener_catalog as fc

# Reuse Revron's tiny catalogue-solid loader by path (importing revron would build the whole Revron rig).
_HW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "revron", "src", "revron", "hw.py")
_spec = importlib.util.spec_from_file_location("revron_hw", os.path.abspath(_HW_PATH))
hw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hw)

# =================================================================================================== MASTERS
RULE_ERA = "aws_2025"         # RULE: "aws_2025" = 150 mm floor square, no overhang at any height, no height limit;
                              #       "aws_v4_3" = 101.6 mm (4 in) start cube; this rest pose fits both eras
FOOTPRINT_SQUARE = 150.0      # RULE aws_2025
START_CUBE = 101.6            # RULE aws_v4_3
MASS_LIMIT_G = 150.0          # RULE antweight, both eras

OVERALL_L = 98.0              # PHOTO/GUESS: front claw/flipper tip (rest) to rear face; fits inside 101.6 mm cube
OVERALL_W = 96.0              # PHOTO/GUESS: outside face to outside face of the left and right side guard plates
FLIPPER_SHARE = 0.305         # PHOTO: front weapon / claw run as a share of OVERALL_L (AWS 77 infobox photo)

DRIVE_MOTOR_ID = "n10_300rpm_6v"     # GUESS (CAT entry): two N10 micro-metal gearmotors driving the two rear wheels
SERVO_ID = "servo_cs07"              # GUESS (CAT entry): SG90-class micro servo driving the central flipper
BATTERY_ID = "lipo_2s_180"           # GUESS (CAT entry): 2S 180 mAh LiPo pack in the rear centre channel
ESC_ID = "malenki_nano"              # GUESS (CAT entry): Malenki-Nano integrated Rx + dual brushed ESC
SWITCH_ID = "switch_bbb_ant_rvrn2"   # GUESS (CAT entry): Bristol Bot Builders screw-type ant link switch

WHEEL_D = 26.0                # PHOTO/GUESS: rear foam/TPU tyre OD; stands proud of tub floor and lid
WHEEL_W = 8.0                 # PHOTO/GUESS: rear tyre width
WHEEL_PROUD = 2.05            # GUESS: tyre proud of tub floor/lid (>= 2.0 mm floor clearance so belly never scrapes)

SHEET_T = 2.0                 # PHOTO/GUESS: 2 mm polycarbonate side guard plates, central flipper, and clamping arms
LID_T = 1.5                   # PHOTO/GUESS: 1.5 mm polycarbonate top lid plates
WALL = bay_lib.DEFAULT_WALL   # STD: printed tub wall (4 perimeters = 1.6 mm)
CLEAR = bay_lib.PRINTED_FIT_CLEARANCE   # STD: printed fit clearance per side (0.2 mm)
RUN_CLEAR = bay_lib.RUNNING_CLEARANCE   # STD: wheel running clearance (0.5 mm)

PLATE_CHAMFER_FRAC = 0.45     # PHOTO: side-plate corner chamfer as a share of the wheel radius
FLIP_CHAMFER_FRAC = 0.14      # PHOTO: flipper front-corner chamfer as a share of the flipper width
FLIP_OPEN_DEG = 42.0          # GUESS: usable flipper travel before the tail approaches the servo tray
FLIP_TIP_LIFT = 2.4           # GUESS: central flipper tip height at rest (>= 2.0 mm so only wheels & clamp tips touch)
CLAMP_TIP_GAP = 0.45          # PHOTO/GUESS: flanking clamp arm front tip height above floor (0.1..0.6 mm support window)

SCREW_D = 2.0                 # STD: M2 fasteners throughout
SCREW_HEAD = "button"         # PHOTO: M2 button-head screws on top lids, flipper, and clamp arms

PRINT_MAT = "pla"             # PHOTO: red 3D-printed PLA chassis tub and internal mounts
SHEET_MAT = "pc"              # PHOTO: 2 mm / 1.5 mm polycarbonate plates and arms

# ================================================================================================= RELATIONS
# --- catalogue sizes (queried from catalog / solid bounding boxes, never retyped)
MOTOR_SHAFT = catalog.find(DRIVE_MOTOR_ID).shaft          # {"at", "dir", "len", "dia"}
_, MOTOR_W, MOTOR_H = hw.size(DRIVE_MOTOR_ID)             # catalogue frame: +X along shaft
MOTOR_L = MOTOR_SHAFT["at"][0] - hw.reach(DRIVE_MOTOR_ID)["x0"]
MOTOR_ENV_Y = 5.0             # CAT: motor envelope half-width in robot Y (= catalogue Y half)
MOTOR_ENV_Z = 6.0             # CAT: motor envelope half-height in robot Z (= catalogue Z half)
MOTOR_FIT = 0.05              # GUESS: snug printed pocket per side
SERVO_L, SERVO_W, SERVO_H = hw.size(SERVO_ID)
BAT_L, BAT_W, BAT_H = hw.size(BATTERY_ID)
ESC_L, ESC_W, ESC_H = hw.size(ESC_ID)

SERVO_BB = hw._solid(SERVO_ID).bounding_box()
SERVO_LEN = SERVO_BB.max.X - SERVO_BB.min.X
SERVO_Y_OFF = (SERVO_BB.min.X + SERVO_BB.max.X) / 2
SERVO_FACE_X = SERVO_BB.max.Z                             # world +X face of the lying servo (catalogue +Z)
SERVO_DROP = max(0.0, SERVO_BB.max.Y - SERVO_W / 2)
SERVO_RISE = max(0.0, -SERVO_BB.min.Y - SERVO_W / 2)

SCREW_CLEAR_D = fc.clearance(SCREW_D)
SCREW_TAP_D = fc.tap_drill(SCREW_D)
INSERT_OD, INSERT_L = fc.insert(SCREW_D)
HEAD_D, HEAD_H = fc.head(SCREW_D, SCREW_HEAD)

# --- heights (Z): floor at Z = 0
AXLE_Z = WHEEL_D / 2
TUB_Z0 = WHEEL_PROUD
TUB_H = WHEEL_D - 2 * WHEEL_PROUD - LID_T
TUB_Z1 = TUB_Z0 + TUB_H
LID_Z1 = TUB_Z1 + LID_T

# --- widths (X): side plate | wheel well | tub | wheel well | side plate
SIDE_X = OVERALL_W / 2 - SHEET_T / 2                      # side guard plate mid-plane
WHEEL_X = OVERALL_W / 2 - SHEET_T - RUN_CLEAR - WHEEL_W / 2
TUB_W = 2 * (WHEEL_X - WHEEL_W / 2 - RUN_CLEAR)
SPACER_L = SIDE_X - SHEET_T / 2 - TUB_W / 2               # standoff boss from tub wall to side guard plate

# --- lengths (Y): rear face at BODY_Y0, tub front face at BODY_Y1, weapon tips at +OVERALL_L / 2
FLIP_RUN = OVERALL_L * FLIPPER_SHARE
BODY_L = OVERALL_L - FLIP_RUN
TUB_L = BODY_L
BODY_Y0 = -OVERALL_L / 2                                  # rear face (-49.0 mm)
BODY_Y1 = BODY_Y0 + BODY_L                                # tub front wall face (+19.11 mm)
TUB_YC = (BODY_Y0 + BODY_Y1) / 2
AXLE_DY = BODY_L / 2 - WHEEL_D / 2 - RUN_CLEAR - WALL
WHEEL_Y = TUB_YC - AXLE_DY                                # 2WD rear axle Y (-33.90 mm)

# --- side guard plates (2 mm PC, chamfered corners)
PLATE_H = WHEEL_D - 2 * WHEEL_PROUD
PLATE_CHAMFER = WHEEL_D / 2 * PLATE_CHAMFER_FRAC
PLATE_Z0 = TUB_Z0
PLATE_HOLE_D = SCREW_CLEAR_D + 0.4

# --- central flipper & hinge (axis along X at (0, HINGE_Y, HINGE_Z))
HINGE_PIN_D = SCREW_D
HINGE_BOSS_D = HINGE_PIN_D + 2 * WALL
HINGE_Y = BODY_Y1 + HINGE_PIN_D / 2 + 1.5                 # outboard of front wall face so pin and block clear wall
HINGE_Z = LID_Z1 - SHEET_T / 2
LID_Y1 = HINGE_Y - HINGE_BOSS_D / 2 - 0.3                 # lids stop clear of the hinge knuckles
FLIP_DROP = HINGE_Z - FLIP_TIP_LIFT
FLIP_LEN = math.hypot(FLIP_RUN, FLIP_DROP)
FLIP_REST_DEG = math.degrees(math.atan2(FLIP_DROP, FLIP_RUN))
REST_L = (HINGE_Y + FLIP_RUN) - BODY_Y0
FLIP_W = 34.0                                             # central flipper width (leaves outboard bays for clamp arms)
FLIP_CHAMFER = FLIP_W * FLIP_CHAMFER_FRAC
BLOCK_KNUCKLE_W = 14.0                                    # centre knuckle width on hinge_block
TUB_KNUCKLE_W = 7.0                                       # outer tub knuckles flanking the centre knuckle
TUB_KNUCKLE_X = BLOCK_KNUCKLE_W / 2 + TUB_KNUCKLE_W / 2 - CLEAR - 0.05
HINGE_PIN_LEN = FLIP_W + 1.0

# --- flanking lobster-claw clamping arms (clamp_l on +X, clamp_r on -X, fixed wedge arms on sloped front tub seats)
CLAMP_GAP_X = 1.5                                         # lateral clearance between central flipper and clamp inner edge
CLAMP_INNER_X = FLIP_W / 2 + CLAMP_GAP_X                  # 18.5 mm: inner X edge of clamp arm and tub seat
CLAMP_SEAT_OUTER_X = TUB_W / 2 - 0.5                      # outer X edge of tub clamp seat
CLAMP_OUTER_X = SIDE_X - SHEET_T / 2 - 1.0                # outer X edge of clamp arm base
CLAMP_TIP_OUTER_X = TUB_W / 2 - 1.0                       # tapered outer X at front tip
CLAMP_X = (CLAMP_INNER_X + CLAMP_SEAT_OUTER_X) / 2        # local X origin of clamp arm & seat
CLAMP_DROP = HINGE_Z - CLAMP_TIP_GAP
CLAMP_REST_DEG = math.degrees(math.atan2(CLAMP_DROP, FLIP_RUN))
CLAMP_LEN = (CLAMP_DROP - SHEET_T * math.cos(math.radians(CLAMP_REST_DEG))) / math.sin(math.radians(CLAMP_REST_DEG))
CLAMP_MOUNT_Y1 = 12.8                                     # front extent of tub clamp seat ahead of HINGE_Y
CLAMP_SEAT_Y0 = BODY_Y1 - WALL                            # rear of tub clamp seat merges into tub front wall
CLAMP_BOLT_Y0 = 5.9                                       # rear screw pair Y along clamp local frame (>=2 mm web to y0)
CLAMP_BOLT_Y1 = 10.7                                      # front screw Y along clamp local frame
CLAMP_BOLT_DX = 4.2                                       # rear screw pair X offset at CLAMP_X +- CLAMP_BOLT_DX
CLAMP_BOLTS_XY = ((-CLAMP_BOLT_DX, CLAMP_BOLT_Y0), (CLAMP_BOLT_DX, CLAMP_BOLT_Y0), (0.0, CLAMP_BOLT_Y1))
CLAMP_BORE_DEPTH = 4.8                                    # blind heat-set bore depth in the sloped tub clamp seat
CLAMP_CUT_H = 30.0                                        # height of plane cutter Box in clamp frame
CLAMP_CUT_W = 60.0                                        # width/length of plane cutter Box in clamp frame

# --- inside the tub: two rear motor pockets, centre channel = servo (front) + battery (rear), side zones = ESC + switch
MOTOR_ROOT_INSET = 0.8                                    # gearbox front face recessed inside tub outer wall
MOTOR_ROOT_X = TUB_W / 2 - MOTOR_ROOT_INSET
MOTOR_INNER_X = MOTOR_ROOT_X - MOTOR_L
CHANNEL_HALF_W = MOTOR_INNER_X - WALL                     # centre channel between the motor pockets
SERVO_Y = BODY_Y1 - WALL - CLEAR - SERVO_L / 2            # servo on its side against the front wall, output axis along X
SERVO_OUT_DY = (SERVO_LEN - SERVO_W) / 2                  # output spline one half-width in from the front end
SERVO_OUT_Y = SERVO_Y + SERVO_OUT_DY
SERVO_OUT_Z = TUB_Z0 + WALL + SERVO_W / 2 + SERVO_DROP + 0.05   # servo rests on the tub floor
BAT_Y = BODY_Y0 + WALL + CLEAR + BAT_L / 2                # battery against the rear wall in the centre channel
SIDE_ZONE_X = (CHANNEL_HALF_W + TUB_W / 2 - WALL / 2) / 2
ESC_Y = -14.0                                             # ESC in the left (+X) side zone, ahead of rear motor pocket
SW_Y = -14.0                                              # switch in the right (-X) side zone, ahead of rear motor pocket

# --- servo tray & relief notch
TRAY_WALL = WALL
TRAY_LIP = 1.05
TRAY_TOP_Z = TUB_Z0 + WALL + SERVO_W + SERVO_DROP + SERVO_RISE + TRAY_LIP
TRAY_HALF_X = CHANNEL_HALF_W - 0.3
CAV_FIT = MOTOR_FIT
SERVO_CAV_FIT = 0.2
HORN_SLOT_Y0, HORN_SLOT_Y1 = 1.0, 15.0
HORN_SLOT_Z0 = 5.0
HORN_SLOT_MARGIN = 0.35
LEAD_SLOT_HALF_X = 4.0
LEAD_SLOT_Z0, LEAD_SLOT_Z1 = 7.5, 11.0

# --- motor pockets & wheel D-bore
POCKET_OUT = 0.1
SHAFT_HOLE_IN = 0.75
SHAFT_HOLE_OUT = 1.5
SHAFT_HOLE_FIT = 0.05
BORE_FLAT_Z = 1.0
BORE_FLAT_W = 3.6
BORE_R = MOTOR_SHAFT["dia"] / 2 + CLEAR / 3
BORE_BOX_Z_OFF = 1.5
BORE_BOX_H = 3.0

# --- hinge relief on the tub front wall top edge
RELIEF_Y0 = TUB_YC + TUB_L / 2 - WALL - 0.7
RELIEF_Y1 = TUB_YC + TUB_L / 2 + 0.7
RELIEF_HALF_X = BLOCK_KNUCKLE_W / 2 - CLEAR + 0.15
RELIEF_Z0 = TRAY_TOP_Z + 0.95

# --- flipper linkage: horn + drive pin in the tail's angular shadow
HORN_HALF_X = 0.7
HORN_X = SERVO_FACE_X + 0.2 + HORN_HALF_X
LID_SEAM_X = 0.2                                          # midline half-gap between left and right lids
LID_SLOT_Y0 = 7.1                                         # rear Y of front lid slot for hinge_block seat & tail
LID_SLOT_HALF_X = BLOCK_KNUCKLE_W / 2 + 0.05              # half-width X of front lid slot clearing hinge_block
HORN_LID_Y0, HORN_LID_Y1 = 1.6, 12.4                      # Y span of narrow horn slot in lid_l
HORN_LID_MARGIN = 0.35                                    # X margin around horn in lid_l slot
HORN_HUB_R = 3.0
HORN_ARM_EXTRA = 3.0
HORN_ARM_OFF = 1.5
TAIL_L = 14.0
TAIL_W = BLOCK_KNUCKLE_W - 2 * CLEAR                      # full centre-knuckle width so tail shields the lid slot at rest
TAIL_H = HINGE_BOSS_D
TAIL_DROP = 1.6                                           # downward skirt depth ahead of drive pin to shield diagonal rays
TAIL_SKIRT_INSET = 2.5                                    # rear inset of tail skirt from tip so drive pin clears
PIN_LEVER = TAIL_L + HINGE_PIN_D / 2 + 0.3
HORN_ARM_W = 4.0
HORN_TAB = (6.0, 4.5)
HORN_PIN_BORE_R = 1.05
HORN_MAX_DEG = 20.0
HORN_MIN_DEG = -HORN_MAX_DEG


def _rot_x(deg, y, z):
    """Rotate the YZ point (y, z) about +X by deg (build123d Rot(deg, 0, 0) convention)."""
    a = math.radians(deg)
    return (y * math.cos(a) - z * math.sin(a), y * math.sin(a) + z * math.cos(a))


def hinge_point(y, z, flip_deg=0.0):
    """World YZ of a hinge-frame point (0, y, z) at flipper lift angle `flip_deg` (0 = rest)."""
    ry, rz = _rot_x(-FLIP_REST_DEG + flip_deg, y, z)
    return (HINGE_Y + ry, HINGE_Z + rz)


def clamp_point(y, z):
    """World YZ of a clamp-frame point (0, y, z) at rest."""
    ry, rz = _rot_x(-CLAMP_REST_DEG, y, z)
    return (HINGE_Y + ry, HINGE_Z + rz)


PIN_Y, PIN_Z = hinge_point(-PIN_LEVER, 0.0)
HORN_R = math.hypot(PIN_Y - SERVO_OUT_Y, PIN_Z - SERVO_OUT_Z)
HORN_THETA0 = math.degrees(math.atan2(PIN_Z - SERVO_OUT_Z, PIN_Y - SERVO_OUT_Y))

# --- side-plate standoff columns in the clear span forward of the rear wheels
WHEEL_FRONT_CLEAR_Y = WHEEL_Y + WHEEL_D / 2 + RUN_CLEAR
STANDOFF_SPAN_Y = BODY_Y1 - WALL - WHEEL_FRONT_CLEAR_Y
STANDOFF_D = INSERT_OD + 2 * WALL
STANDOFF_YS = (WHEEL_FRONT_CLEAR_Y + STANDOFF_SPAN_Y * 0.28,
               WHEEL_FRONT_CLEAR_Y + STANDOFF_SPAN_Y * 0.76)
PLATE_SCREWS_Z = (AXLE_Z - PLATE_H / 4, AXLE_Z + PLATE_H / 4)

# --- lid fixing pads along the tub side walls (rear of rear motor pocket, and forward near the front wall)
LID_SCREW_INSET = 4.0
LID_PAD_X = TUB_W / 2 - LID_SCREW_INSET
LID_PAD_D = 7.0
LID_PAD_H = 7.0
LID_PAD_BORE_FLOOR = 2.2
LID_PADS = ((-44.5, 7.5), (12.5, 6.5))
LID_SCREWS_Y_L = tuple(y for y, _w in LID_PADS)
LID_SCREWS_Y_R = tuple(y for y, _w in LID_PADS)
LID_SLOT_R = 0.25
LID_SLOT_MARGIN = 0.6
SWITCH_POKE_Z = 0.5
INSERT_HALF_L = 1.5
PAD_MOUTH_R = 1.5
SHELL_FILLET_R = 1.0
SHELL_TOL = 0.1

# --- hinge block seat (M2x8 screws through flipper into heat-sets in the block seat)
SEAT_H = 10.0
SEAT_Y0 = 5.5
SEAT_L = 10.0
SEAT_TOP_FILLET_R = 1.0
SEAT_HOLE_D = INSERT_OD - CLEAR
SEAT_W = BLOCK_KNUCKLE_W - 2 * CLEAR
HINGE_BOLT_X = 3.6
BOLT_HB_Y = SEAT_Y0 + SEAT_L / 2
SEAT_WEB_Y0 = 0.5
SEAT_WEB_Y1 = SEAT_Y0 + 0.5
SEAT_WEB_H = 1.6
SEAT_WEB_FILLET_R = 1.0
SEAM_DZ = 0.9
SEAM_DZ_TOP = 0.1
KNUCKLE_RIM_FILLET_R = 0.6
RIM_TOL = 0.05
BORE_GUARD = 0.2
KNUCKLE_BORE_R = HINGE_PIN_D / 2 + 0.3
PIN_TUB_BORE_R = HINGE_PIN_D / 2 - 0.15
PIN_X0 = 2.0 - HORN_X
PIN_X1 = HORN_HALF_X

START_FLIP_DEG = 0.0


def check():
    """Rule / packaging relations to assert before trusting a build."""
    problems = []
    if RULE_ERA == "aws_2025" and max(OVERALL_L, OVERALL_W) > FOOTPRINT_SQUARE:
        problems.append("plan view leaves the 150 mm floor square")
    if RULE_ERA == "aws_v4_3" and REST_L > START_CUBE + RIM_TOL:
        problems.append("start pose leaves the 101.6 mm cube")
    if 2 * CHANNEL_HALF_W < max(SERVO_H, BAT_W) + 2 * CLEAR:
        problems.append("centre channel narrower than servo/battery")
    if MOTOR_SHAFT["len"] < RUN_CLEAR + WHEEL_W:
        problems.append("motor shaft too short to reach across the gap and through the wheel")
    if BAT_Y + BAT_L / 2 + CLEAR > SERVO_Y - SERVO_L / 2 - CLEAR:
        problems.append("battery and servo overlap in the centre channel")
    if SPACER_L <= 0:
        problems.append("no room for side-plate standoffs")
    if LID_Y1 >= HINGE_Y - HINGE_BOSS_D / 2:
        problems.append("lids reach the hinge knuckles")
    servo_top = SERVO_OUT_Z - SERVO_BB.min.Y
    for f in (0.0, FLIP_OPEN_DEG):
        _, tip_z = hinge_point(-TAIL_L, -TAIL_H / 2, f)
        if tip_z < servo_top + RUN_CLEAR:
            problems.append(f"tail bottom edge dips to {tip_z:.2f} mm at flip {f:.0f} deg, grazing servo top {servo_top:.2f}")
    if PIN_LEVER < TAIL_L + HINGE_PIN_D / 2 + BORE_GUARD:
        problems.append("drive pin not beyond the tail end face")
    for d in (0.0, HORN_MAX_DEG):
        py, pz = _rot_x(HORN_THETA0 + d, HORN_R, 0.0)
        wy, wz = SERVO_OUT_Y + py, SERVO_OUT_Z + pz
        if math.hypot(wy - HINGE_Y, wz - HINGE_Z) < TAIL_L + HINGE_PIN_D / 2 + BORE_GUARD:
            problems.append(f"drive pin sweeps into the tail band at horn angle {d:.0f} deg")
    return problems
