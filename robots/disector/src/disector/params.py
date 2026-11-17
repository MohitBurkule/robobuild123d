"""Master parameters and derived coordinates for Disector (150 g AWS 2025).

Frame: X right (+x), Y forward (+y), Z up (+z), floor Z = 0.
"""

from __future__ import annotations

import math

# --- Envelope & chassis masters ---
Z_FLOOR_BOT = 2.0        # 2.0 mm ground clearance (>= 1.0 mm)
FLOOR_T = 2.0            # 2.0 mm tub floor
Z_FLOOR_TOP = Z_FLOOR_BOT + FLOOR_T  # 4.0 mm
Z_TOP = 24.0             # tub top deck height
WALL_T = 2.0             # perimeter wall thickness
CORNER_R = 4.0           # external corner fillet radius

TUB_HALF_W = 48.0        # 96 mm wide tub (X in [-48, +48])
Y_REAR = -40.0           # rear wall outer face
Y_FRONT_TOP = 8.0        # top of 45 deg sloped front face
# 45 deg slope from (Y=8, Z=24) to (Y=28, Z=4): Y + Z = 32
Y_FRONT_BOT = Y_FRONT_TOP + (Z_TOP - Z_FLOOR_TOP)  # 28.0 mm

# --- Drive motors & wheels (wheel_20x8, r=10 mm, w=8 mm) ---
WHEEL_R = 10.0
WHEEL_W = 8.0
WHEEL_Z = WHEEL_R        # 10.0 mm -> touches floor Z = 0
WHEEL_Y = -22.0
WHEEL_X = 43.0           # wheels span X = +/-[39.0, 47.0]
MOTOR_X = WHEEL_X - 15.05  # 27.95 mm (n10_2200rpm_6v shaft center at +15.05)

# --- Internal electronics ---
# Battery: lipo_2s_350 (36 x 17 x 11)
BAT_AT = [0.0, -5.0, Z_FLOOR_TOP + 5.5]  # [0, -5, 9.5]
# Malenki Nano: malenki_nano (23 x 16 x 5) in front of right wheel well
MALENKI_AT = [31.5, -0.5, Z_FLOOR_TOP + 2.5]  # [31.5, -0.5, 6.5]
# Brushless ESC: bbb_ant_esc (22 x 11 x 4) in front of left wheel well
WPN_ESC_AT = [-31.5, -0.5, Z_FLOOR_TOP + 2.0]  # [-31.5, -0.5, 6.0]
# Servo: servo_cs07 (23 x 12 x 22.7), rotated [0, 90, 0] so output shaft is along X
SERVO_AT = [0.0, -28.0, 19.0]
SERVO_ROT = [0.0, 90.0, 0.0]
# Switch: switch_bbb_ant_rvrn2 at X=15.0, Y=-17.0 (clear of arm & top_cover), flange bottom at Z=24.0
SWITCH_AT = [15.0, -17.0, 22.25]

# --- Top panels & covers ---
PANEL_TOP_T = 1.2
TOP_SPINE_T = 1.6
TOP_COVER_Z0 = Z_TOP + PANEL_TOP_T
TOP_COVER_Z1 = 41.0

# --- Front wedge & ground game ---
WEDGE_T = 1.0
WEDGE_W = 96.0
WEDGE_SLOPE_LEN = math.hypot(Y_FRONT_BOT - Y_FRONT_TOP, Z_TOP - Z_FLOOR_TOP)  # 20*sqrt(2) = 28.28 mm
# Midpoint of tub front slope face: Y = 18.0, Z = 14.0
WEDGE_MID_Y = 0.5 * (Y_FRONT_TOP + Y_FRONT_BOT)
WEDGE_MID_Z = 0.5 * (Z_TOP + Z_FLOOR_TOP)
INV_SQRT2 = 1.0 / math.sqrt(2.0)

FORK_MOUNT_X = 22.0
FORK_T = 1.5
FORK_PIVOT_Y = 33.5
FORK_PIVOT_Z = 6.0
FORK_TIP_Y = 59.0
FORK_TIP_Z = 0.2

SKID_X = 43.0
SKID_TIP_Y = 52.0
SKID_TIP_Z = 0.2

GUARD_X0 = 48.0          # bolted flush to tub outer X = +/-48
GUARD_T = 3.0

# --- Overhead hammer-saw arm & weapon ---
ARM_PIVOT = [0.0, -28.0, 35.0]
ARM_TIP = [0.0, -16.0, 80.0]
DISC_OD = 44.0
DISC_R = DISC_OD / 2.0
DISC_T = 1.0
# GR1507 at arm tip: stator back at X=-10.4 -> WPN_MOTOR_AT X=13.40 puts stator back flush on arm X=3.00, bell cap at +6.7 -> X=20.10
WPN_MOTOR_AT = [13.40, -16.0, 80.0]
WPN_MOTOR_ROT = [0.0, 0.0, 0.0]
DISC_AT = [20.60, -16.0, 80.0]
DISC_ROT = [0.0, 90.0, 0.0]

# --- Colors (matching Disector reference photo) ---
COL_CHASSIS = "#1b7a43"      # green chassis
COL_TOP_PANEL = "#1f8a4c"    # green top panel
COL_TOP_COVER = "#2554c7"    # blue top electronics/servo cover
COL_TOP_SPINE = "#1e1e22"    # black top spine strap
COL_WEDGE = "#c8cdd2"        # silver aluminium front wedge
COL_ORANGE = "#f26522"       # orange fork mounts, skids, wheel guards
COL_FORK = "#1e7a56"         # dark green/metallic forks
COL_ARM = "#114d2e"          # dark green overhead arm
COL_DISC = "#0f4226"         # dark green saw disc
COL_LOCK = "#1e64d8"         # blue locking bar
COL_EYE_WHITE = "#f4f4f4"
