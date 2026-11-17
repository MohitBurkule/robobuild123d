"""Expandabot Classic (Team Bits Everywhere) parametric dimensions.

Matches the classic expanding-pincer build:
  - Black 3D-printed chassis tub & front bulkhead with central white nose stud
  - Dark-green 2 mm PC outer side plates
  - One-piece carbon-fiber T-shaped top plate with rear wheel cutouts & open front corner bays
  - Grooved translucent-grey TPU rear wheels protruding above and below the body
  - Central 3D-printed forked front wedge with steel crossbar
  - Two pale-mint G10/PC expanding side wings on dark-grey printed corner hinge brackets
  - Blue SG90-class servo under the CF deck with white printed horn in the front-left bay

Coordinate frame:
  +X  left (outboard toward left wheel / left side plate / left wing)
  +Y  forward (toward forked wedge)
  +Z  up (floor at Z = 0)
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
RULE_ERA = "aws_2025"
FOOTPRINT_SQUARE = 150.0
MASS_LIMIT_G = 150.0

DRIVE_MOTOR_ID = "n10_300rpm_6v"
SERVO_ID = "servo_cs07"
BATTERY_ID = "lipo_2s_180"
ESC_ID = "malenki_nano"
SWITCH_ID = "switch_bbb_ant_rvrn2"

WHEEL_D = 27.0
WHEEL_W = 10.0
WHEEL_PROUD = 2.0
WHEEL_NOTCHES = 12
WHEEL_NOTCH_D = 1.2
WHEEL_NOTCH_W = 2.0

SHEET_T = 2.0
TOP_T = 1.5
WALL = bay_lib.DEFAULT_WALL        # 1.6 mm
CLEAR = bay_lib.PRINTED_FIT_CLEARANCE  # 0.2 mm
RUN_CLEAR = 1.0                    # 1.0 mm wheel running clearance

SCREW_D = 2.0
SCREW_HEAD = "button"
PRINT_MAT = "pla"
SHEET_MAT = "pc"
TOP_MAT = "cf_plate"

# ================================================================================================= RELATIONS
MOTOR_SHAFT = catalog.find(DRIVE_MOTOR_ID).shaft
_, MOTOR_W, MOTOR_H = hw.size(DRIVE_MOTOR_ID)
MOTOR_L = MOTOR_SHAFT["at"][0] - hw.reach(DRIVE_MOTOR_ID)["x0"]
MOTOR_ENV_Y = 5.0
MOTOR_ENV_Z = 6.0
MOTOR_FIT = 0.05

SERVO_L, SERVO_W, SERVO_H = hw.size(SERVO_ID)
SERVO_BB = hw._solid(SERVO_ID).bounding_box()
SERVO_LEN = SERVO_BB.max.X - SERVO_BB.min.X
SERVO_FACE_Z = SERVO_BB.max.Z
BAT_L, BAT_W, BAT_H = hw.size(BATTERY_ID)
ESC_L, ESC_W, ESC_H = hw.size(ESC_ID)

SCREW_CLEAR_D = fc.clearance(SCREW_D)
INSERT_OD, INSERT_L = fc.insert(SCREW_D)
INSERT_HALF_L = INSERT_L / 2

# --- heights (Z): floor at Z = 0
AXLE_Z = WHEEL_D / 2               # 13.5 mm -> wheel bottom Z = 0, top Z = 27.0
TUB_Z0 = WHEEL_PROUD               # 2.0 mm floor clearance
TUB_Z1 = 22.0                      # top of tub walls
TUB_H = TUB_Z1 - TUB_Z0            # 20.0 mm
TOP_Z1 = TUB_Z1 + TOP_T            # 23.5 mm

# --- widths (X)
BODY_W = 96.0                      # outside-to-outside of dark green side plates
SIDE_X = BODY_W / 2 - SHEET_T / 2  # ±47.0 mm
TUB_W = BODY_W - 2 * SHEET_T       # 92.0 mm (X in [-46, +46])
WHEEL_X = TUB_W / 2 - WHEEL_W / 2 - RUN_CLEAR - 2.0  # ±38.0 mm (X in [33, 43], 2.0 mm CF web outboard)
MOTOR_ROOT_X = WHEEL_X - WHEEL_W / 2 - RUN_CLEAR - 1.0  # 31.0 mm (1.0 mm solid wall to wheel well)
MOTOR_INNER_X = MOTOR_ROOT_X - MOTOR_L
CHANNEL_HALF_W = MOTOR_INNER_X - WALL

# --- lengths (Y)
BODY_Y0 = -44.0
BODY_Y1 = 24.0                     # front bulkhead outer face
BODY_L = BODY_Y1 - BODY_Y0         # 68.0 mm
WHEEL_Y = BODY_Y0 + WHEEL_D / 2 + RUN_CLEAR + WALL  # -27.9 mm

# --- side plates (2 mm dark green PC)
SIDE_Y0 = BODY_Y0 + 1.0
SIDE_Y1 = BODY_Y1 - 6.0            # 18.0 mm: stops cleanly behind front corner wing hinge
SIDE_Z0 = TUB_Z0 + 0.5
SIDE_Z1 = TUB_Z1 - 0.5
SIDE_R = 4.0
SIDE_SCREW_YS = (-10.0, 1.0, 12.0)
SIDE_SCREW_Z = 12.0

# --- top panel (1.5 mm CF one-piece T-deck)
TOP_X_MAX = TUB_W / 2              # 45.0 mm
TOP_REAR_Y0 = BODY_Y0
TOP_FRONT_Y1 = BODY_Y1 - WALL      # 22.4 mm (stops just behind front bulkhead lip)
TOP_BAY_Y0 = 0.0                   # front corner bays open for Y > 0.0
TOP_TONGUE_HALF_X = 24.0           # central tongue width 48 mm over front electronics
TOP_REAR_NOTCH_HALF_X = 11.0
TOP_REAR_NOTCH_Y1 = BODY_Y0 + 8.0
TOP_WHEEL_SLOT_X0 = WHEEL_X - WHEEL_W / 2 - RUN_CLEAR
TOP_WHEEL_SLOT_X1 = WHEEL_X + WHEEL_W / 2 + RUN_CLEAR
TOP_WHEEL_SLOT_Y0 = WHEEL_Y - WHEEL_D / 2 - RUN_CLEAR
TOP_WHEEL_SLOT_Y1 = WHEEL_Y + WHEEL_D / 2 + RUN_CLEAR
TOP_SCREWS_XY = (
    (-27.0, -40.0), (27.0, -40.0),
    (-28.0, -8.0), (28.0, -8.0),
    (-3.2, 19.5), (3.2, 19.5),
)

# --- internal electronics
BAT_X = 0.0
BAT_Y = -12.0
BAT_Z = TUB_Z0 + WALL + BAT_H / 2
ESC_X = -10.5
ESC_Y = 8.5
ESC_Z = TUB_Z0 + WALL + ESC_H / 2
SERVO_X = 23.0
SERVO_Y = 8.8
SERVO_Z = TUB_Z0 + WALL + SERVO_W / 2 + 0.2
SWITCH_X = -22.0
SWITCH_Y = -15.0
SWITCH_Z = TUB_Z1 - 2.25
SW_LEVER_TRAVEL = float((catalog.find(SWITCH_ID).props or {}).get("lever_travel_mm", 3.0))

# --- central forked front wedge + crossbar
WEDGE_Y0 = BODY_Y1 + 0.4           # 23.4 mm (clear of front bulkhead when tilted)
WEDGE_Y1 = 70.0                    # 46.6 mm forward reach
WEDGE_W0 = 44.0                    # base width
WEDGE_TIP_X_IN = 8.0               # inner edge of each prong at tip
WEDGE_TIP_X_OUT = 20.0             # outer edge of each prong at tip
WEDGE_V_Y = 47.0                   # V-notch apex Y
WEDGE_Z0 = 9.5                     # top Z at rear of wedge
WEDGE_Z1 = 2.0                     # tip Z above floor (bottom face > 0.7 mm above floor)
WEDGE_T = 2.6                      # printed wedge thickness
WEDGE_WIN_X = 13.0                 # central rectangular window half-width
WEDGE_WIN_Y0 = 27.5
WEDGE_WIN_Y1 = 42.5
CROSSBAR_Y = 35.0
CROSSBAR_D = 3.0
WEDGE_BOSS_D = 5.4

# --- expanding side wings (mint G10/PC) + dark-grey hinge brackets
BRACKET_L = 16.0
BRACKET_H = 11.0
BRACKET_W = 6.0
WING_PIVOT_X = TUB_W / 2 + BRACKET_W / 2 + 0.3  # ±48.3 mm (clear of tub wall & side plate)
WING_PIVOT_Y = BODY_Y1             # 23.0 mm (front-outer corner)
WING_PIVOT_Z = 11.0
WING_DEPLOY_DEG = 48.0             # deployed angle in default pose (swept forward & outward to corral, fits 150 mm square)
WING_FOLD_DEG = -65.0              # folded angle for compact transport
WING_LEN = 30.0
WING_H = 16.0
WING_T = 2.0
WING_PIN_D = 2.0
WING_PIN_LEN = 17.0
WING_SCREW_DYS = (7.5, 13.0)

# --- white servo horn in open front-left bay & front nose stud
HORN_LEN = 10.5
HORN_W = 4.5
HORN_T = 2.5
NOSE_PIN_D = 3.2
NOSE_PIN_L = 4.0
NOSE_PIN_Z = 14.5

# --- tub & wing feature constants (for param.literals)
WING_ROOT_Y = 4.0
WING_TIP_CHAMFER = 4.0
WING_GAP = 0.05
PAD_R = 3.0
PAD_FRONT_H = 6.0
SIDE_BOSS_R = 3.2
SIDE_BOSS_L = 6.0
CLEVIS_R = 4.0
CLEVIS_T = 3.0
CLEVIS_Z_GAP = 1.65
SW_TRAY_W = 8.5
SW_TRAY_L = 14.0
SW_TRAY_H = 4.0
SW_TRAY_DZ = 8.0
SW_CUT_W = 6.4
SW_CUT_L = 21.0
SW_CUT_H = 12.0
SKID_W = 8.0
SKID_L = 10.0
SKID_H = 1.8
SKID_X = 30.0
SKID_Y = 18.0
WIRE_SLOT_W = 5.0
WIRE_SLOT_H = 4.0

# --- tolerances
EPS = 0.2
SHELL_TOL = 0.15
SLOT_R = 0.25
CHAMFER_R = 1.0


def check():
    problems = []
    if max(BODY_L + (WEDGE_Y1 - BODY_Y1), 2 * (WING_PIVOT_X + WING_LEN * math.sin(math.radians(WING_DEPLOY_DEG)))) > FOOTPRINT_SQUARE:
        problems.append("expanded footprint exceeds 150 mm square")
    if TOP_WHEEL_SLOT_X1 >= SIDE_X - SHEET_T / 2:
        problems.append("wheel slot cuts through side plate")
    return problems
