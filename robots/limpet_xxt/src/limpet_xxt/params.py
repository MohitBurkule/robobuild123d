"""Limpet XXT masters and relations. UNTESTED: written without running anything.

Frame: X forward (flipper end), Y left, Z up, arena floor at Z = 0, origin on the robot's centre line, mid wheelbase.

Only the MASTERS block holds typed numbers. Every one of them is tagged:
  RULE   - from the AWS antweight rules (known)
  CAT    - read from the repo catalogue (robot/catalog.py), never retyped
  STD    - fastener / material standard via robot/cad/fastener_catalog.py or robot/cad/bay.py
  PHOTO  - proportion SEEN-IN-PHOTO, converted to mm by a GUESS scale (see REFERENCE.md)
  GUESS  - not visible in any source; an engineering guess
Everything below the MASTERS block is a relation.
"""
import importlib.util
import math
import os

from robot import catalog
from robot.cad import bay as bay_lib
from robot.cad import fastener_catalog as fc

# ------------------------------------------------------------------------------------------------ reuse: revron hw
# robots/revron/src/revron/hw.py reads part sizes off the catalogue shapes. It has no package-relative imports, so it is
# loaded by path (importing the revron package would build the whole Revron rig).
_HW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "revron", "src", "revron", "hw.py")
_spec = importlib.util.spec_from_file_location("revron_hw", os.path.abspath(_HW_PATH))
hw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hw)

# =================================================================================================== MASTERS
RULE_ERA = "aws_2025"         # RULE: "aws_2025" = 150 mm floor square, no overhang at any height, no height limit
                              #       (repo draft PR #77); "aws_v4_3" = old 4 in (101.6 mm) start cube, any orientation
FOOTPRINT_SQUARE = 150.0      # RULE aws_2025
START_CUBE = 101.6            # RULE aws_v4_3 (the era most Limpet XXT versions were built in; this copy fits both)
MASS_LIMIT_G = 150.0          # RULE antweight, both eras

OVERALL_L = 100.0             # PHOTO/GUESS: flipper tip (rest) to rear of side plate; under START_CUBE too
OVERALL_W = 96.0              # PHOTO/GUESS: outside face to outside face of the two side plates
FLIPPER_SHARE = 0.32          # PHOTO: flipper plan run / OVERALL_L (aws71, aws74, aws76 three-quarter views)

DRIVE_MOTOR_ID = "n10_300rpm_6v"     # GUESS (CAT entry): four small micro-metal gearmotors, one per wheel
SERVO_ID = "servo_cs07"              # GUESS (CAT entry): SG90-class flipper servo
BATTERY_ID = "lipo_2s_180"           # GUESS (CAT entry): 2S pack, sits in the centre channel (V3.1 photo)
ESC_ID = "malenki_nano"              # GUESS (CAT entry): Rx + dual brushed ESC, the usual UK ant board
SWITCH_ID = "switch_bbb_ant_rvrn2"   # GUESS (CAT entry): screw-on ant switch, removable link per rules

WHEEL_D = 24.0                # PHOTO/GUESS: tyre OD; tyre stands proud of tub top and bottom (invertible)
WHEEL_W = 8.0                 # PHOTO/GUESS: tyre width
WHEEL_PROUD = 1.5             # GUESS: tyre proud of tub top / bottom face (the robot runs either way up)

SHEET_T = 2.0                 # PHOTO/GUESS: clear polycarbonate side plates and flipper (decal on the back face)
LID_T = 1.5                   # PHOTO/GUESS: clear polycarbonate lid plates
WALL = bay_lib.DEFAULT_WALL   # STD: printed tub wall (4 perimeters)
CLEAR = bay_lib.PRINTED_FIT_CLEARANCE   # STD: printed fit clearance per side
RUN_CLEAR = bay_lib.RUNNING_CLEARANCE   # STD: wheel to anything that does not turn with it

PLATE_CHAMFER_FRAC = 0.5      # PHOTO: side-plate corner chamfer as a share of the wheel radius (hexagonal outline)
FLIP_CHAMFER_FRAC = 0.12      # PHOTO: flipper front-corner chamfer as a share of the flipper width
FLIP_SIDE_GAP = 1.0           # GUESS: flipper edge to side plate (it swings between the plates)
FLIP_OPEN_DEG = 90.0          # GUESS: flipper travel from rest (servo-limited); expansion happens only after start
FLIP_TIP_LIFT = 0.5           # GUESS: flipper tip height above the floor at rest

SCREW_D = 2.0                 # STD: M2 throughout (photos show small button / torx heads)
SCREW_HEAD = "button"         # PHOTO: domed heads on side plates and lids

PRINT_MAT = "pla"             # PHOTO: dark green / white printed tub (V3.x onward)
SHEET_MAT = "pc"              # PHOTO: clear sheet with zebra decals

# ================================================================================================= RELATIONS
# --- catalogue sizes (never retyped)
MOTOR_SHAFT = catalog.find(DRIVE_MOTOR_ID).shaft          # {"at", "dir", "len", "dia"}
_, MOTOR_W, MOTOR_H = hw.size(DRIVE_MOTOR_ID)               # catalogue frame: x along the shaft
MOTOR_L = MOTOR_SHAFT["at"][0] - hw.reach(DRIVE_MOTOR_ID)["x0"]   # body only: back face to shaft root
SERVO_L, SERVO_W, SERVO_H = hw.size(SERVO_ID)
BAT_L, BAT_W, BAT_H = hw.size(BATTERY_ID)
ESC_L, ESC_W, ESC_H = hw.size(ESC_ID)
SERVO_HOLES = catalog.find(SERVO_ID).props["mount_holes_mm"]

SCREW_CLEAR_D = fc.clearance(SCREW_D)
SCREW_TAP_D = fc.tap_drill(SCREW_D)
INSERT_OD, INSERT_L = fc.insert(SCREW_D)
HEAD_D, HEAD_H = fc.head(SCREW_D, SCREW_HEAD)

# --- heights: the tub sits inside the tyre envelope, proud of neither face -> runs inverted
AXLE_Z = WHEEL_D / 2
TUB_Z0 = WHEEL_PROUD
TUB_H = WHEEL_D - 2 * WHEEL_PROUD - LID_T                  # lid top flush with TUB_Z0 + (WHEEL_D - 2 * WHEEL_PROUD)
TUB_Z1 = TUB_Z0 + TUB_H
LID_Z1 = TUB_Z1 + LID_T

# --- widths: side plate | wheel well | tub | wheel well | side plate
SIDE_Y = OVERALL_W / 2 - SHEET_T / 2                       # side plate mid-plane
WHEEL_Y = OVERALL_W / 2 - SHEET_T - RUN_CLEAR - WHEEL_W / 2
TUB_W = 2 * (WHEEL_Y - WHEEL_W / 2 - RUN_CLEAR)
SPACER_L = SIDE_Y - SHEET_T / 2 - TUB_W / 2                # standoff boss from tub wall to side plate

# --- lengths: flipper run is a photo share of the overall length; the rest is body
FLIP_RUN = OVERALL_L * FLIPPER_SHARE
BODY_L = OVERALL_L - FLIP_RUN                              # side plate length
TUB_L = BODY_L                                             # tub front wall carries the hinge, flush with the plates
BODY_X0 = -OVERALL_L / 2                                   # rear face
BODY_X1 = BODY_X0 + BODY_L                                 # front face = hinge line
TUB_XC = (BODY_X0 + BODY_X1) / 2
AXLE_DX = BODY_L / 2 - WHEEL_D / 2 - RUN_CLEAR - WALL     # wheel just inside the end bulkhead
AXLES_X = (TUB_XC + AXLE_DX, TUB_XC - AXLE_DX)            # front, rear

# --- side plate hexagon: chamfers relate to the wheel radius
PLATE_H = WHEEL_D - 2 * WHEEL_PROUD                        # plate edges sit inside the tyre: tyres touch first
PLATE_CHAMFER = WHEEL_D / 2 * PLATE_CHAMFER_FRAC
PLATE_Z0 = TUB_Z0

# --- flipper: hinged on the tub top front edge, rest pose touches the floor ahead
HINGE_X = BODY_X1
HINGE_Z = LID_Z1 - SHEET_T / 2
FLIP_DROP = HINGE_Z - FLIP_TIP_LIFT
FLIP_LEN = math.hypot(FLIP_RUN, FLIP_DROP)
FLIP_REST_DEG = math.degrees(math.atan2(FLIP_DROP, FLIP_RUN))   # below horizontal, derived (photo shows ~35-45)
FLIP_W = 2 * (SIDE_Y - SHEET_T / 2 - FLIP_SIDE_GAP)
FLIP_CHAMFER = FLIP_W * FLIP_CHAMFER_FRAC
HINGE_KNUCKLES = 3                                          # PHOTO: tub/flipper/tub hinge read as alternate knuckles
HINGE_PIN_D = SCREW_D                                      # M2 screw as hinge pin
HINGE_BOSS_D = HINGE_PIN_D + 2 * WALL

# --- inside the tub: four motor pockets at the axles, centre channel = servo (front) + battery (rear)
MOTOR_ROOT_Y = TUB_W / 2                                  # gearbox face flush with the outer wall face (pocket runs through)
MOTOR_INNER_Y = MOTOR_ROOT_Y - MOTOR_L                      # inboard end of the motor body
CHANNEL_HALF_W = MOTOR_INNER_Y - WALL                       # centre channel between the two motors of an axle
SERVO_X = BODY_X1 - WALL - CLEAR - SERVO_L / 2             # servo on its side against the front wall, output axis along Y
BAT_X = BODY_X0 + WALL + CLEAR + BAT_L / 2                  # battery against the rear wall (long black block, V3.1)
ESC_X = TUB_XC                                              # ESC in the left side zone, switch in the right
SIDE_ZONE_Y = (CHANNEL_HALF_W + WALL + TUB_W / 2 - WALL) / 2

# --- flipper drive: the flipper's printed hinge block carries a tail lever that runs back along the centre channel
# (the bar seen in the lid slot on aws71/72/74); the servo horn lifts / drops the tail end through a pin in a slot.
SERVO_OUT_DX = (SERVO_L - SERVO_W) / 2                      # GUESS relation: output one half-width in from the front end
SERVO_OUT_X = SERVO_X + SERVO_OUT_DX
SERVO_OUT_Z = TUB_Z0 + WALL + SERVO_W / 2                   # lying on its side: catalogue y (width) is now Z
HORN_R = SERVO_W                                            # GUESS relation: horn reach = servo body width
TAIL_L = HINGE_X - SERVO_OUT_X + HORN_R                     # tail reaches past the horn tip so the pin stays in the slot
TAIL_W = HINGE_BOSS_D                                       # tail as wide as the hinge boss
TAIL_SLOT_L = 2 * HORN_R * (1 - math.cos(math.radians(FLIP_OPEN_DEG / 2)))   # pin travel along the tail

# --- side-plate fixing: photos show a screw mid-plate (all versions) plus screws near the ends whose seat is hidden.
# The wheels fill the plate ends at axle height, so this copy uses one standoff column mid-wheelbase with two screws
# (GUESS), spaced to clear the wheel swept circles.
WHEEL_GAP_X = (AXLES_X[0] - AXLES_X[1]) - WHEEL_D - 2 * RUN_CLEAR   # clear span between front and rear tyres
STANDOFF_D = min(WHEEL_GAP_X, INSERT_OD + 2 * WALL)
PLATE_SCREWS_X = (TUB_XC,)
PLATE_SCREWS_Z = (AXLE_Z - PLATE_H / 4, AXLE_Z + PLATE_H / 4)
LID_SCREW_INSET = WALL + HEAD_D / 2
LID_SCREWS_X = (BODY_X0 + LID_SCREW_INSET, BODY_X1 - LID_SCREW_INSET)

# --- start pose: flipper at rest. A raised flipper is post-start motion, modelled as the flipper joint angle; it only
# grows the height, which neither era's plan-view check counts against (v4.3 allowed expansion after the start).
START_FLIP_DEG = 0.0                                        # 0 = rest (wedge on the floor); FLIP_OPEN_DEG = fully up


def check():
    """Rule / packaging relations to assert before trusting a build (not run here)."""
    problems = []
    if RULE_ERA == "aws_2025" and max(OVERALL_L, OVERALL_W) > FOOTPRINT_SQUARE:
        problems.append("plan view leaves the 150 mm floor square (no overhang allowed at any height)")
    if RULE_ERA == "aws_v4_3" and max(OVERALL_L, OVERALL_W, WHEEL_D) > START_CUBE:
        problems.append("start pose leaves the 101.6 mm cube")
    if 2 * CHANNEL_HALF_W < max(SERVO_H, BAT_W) + 2 * CLEAR:
        problems.append("centre channel narrower than servo/battery")
    if MOTOR_SHAFT["len"] < RUN_CLEAR + WHEEL_W:
        problems.append("motor shaft too short to reach across the gap and through the wheel")
    if BAT_X + BAT_L / 2 + CLEAR > SERVO_X - SERVO_L / 2 - CLEAR:
        problems.append("battery and servo overlap in the centre channel")
    if WHEEL_GAP_X < INSERT_OD + 2 * WALL:
        problems.append("standoff column wider than the gap between the tyres")
    if SPACER_L <= 0:
        problems.append("no room for side-plate standoffs")
    return problems
