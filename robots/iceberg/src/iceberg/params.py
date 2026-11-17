"""Parametric dimensions and layout constants for Iceberg (150 g AWS 2025 4WD vertical spinner).

Coordinate frame:
  +X : left
  +Y : forward (forks and vertical spinner at +Y)
  +Z : up (floor at Z = 0)
"""
from __future__ import annotations

# ---- Overall chassis envelope (mm) ---------------------------------------------------------------
BODY_X_HALF = 34.0       # green top/bottom plates half-width (total 68 mm)
TUB_X_HALF = 32.0        # inner printed tub half-width (total 64 mm)
CHASSIS_Y_MIN = -52.0    # rear edge of plates
CHASSIS_Y_MAX = 24.0     # front edge of plates
CHASSIS_LEN = CHASSIS_Y_MAX - CHASSIS_Y_MIN  # 76.0 mm

PLATE_T = 0.5            # 0.5 mm stock dark green FR4/CF top & bottom plates
BOT_PLATE_Z0 = 3.0       # bottom plate z: 3.0 .. 3.5 (3.0 mm ground clearance)
BOT_PLATE_Z1 = BOT_PLATE_Z0 + PLATE_T
TOP_PLATE_Z1 = 23.0      # top plate z: 22.5 .. 23.0
TOP_PLATE_Z0 = TOP_PLATE_Z1 - PLATE_T
CAVITY_Z0 = BOT_PLATE_Z1 # 3.5
CAVITY_Z1 = TOP_PLATE_Z0 # 22.5 (19.0 mm internal height)

# ---- Drive & wheels ------------------------------------------------------------------------------
WHEEL_OD = 26.0
WHEEL_R = WHEEL_OD / 2.0  # 13.0
WHEEL_W = 6.5
AXLE_Z = WHEEL_R          # 13.0 -> wheel bottom at z = 0.0
WHEEL_REAR_Y = -38.0
WHEEL_FRONT_Y = 8.0
WHEEL_X = 39.5            # wheel center X (spans 36.25 .. 42.75)
MOTOR_X = 22.25           # N10 center X (body 9.5..33.5, shaft 33.5..42.5)

# ---- Blue TPU side guards ------------------------------------------------------------------------
GUARD_X_IN = 45.5         # 2.75 mm clearance outside wheel outer face (42.75), 3.0 mm clear of shaft
GUARD_X_OUT = 47.5        # 2.0 mm thick side guard
GUARD_Y_MIN = -53.0       # rounded rear wrapping behind rear wheel
GUARD_Y_MAX = 23.0        # sloped nose ahead of front wheel
GUARD_Z0 = 3.0
GUARD_Z1 = 21.0
GUARD_MOUNT_Y1 = -21.0    # rear standoff boss (clear of window -18..-12 & rear wheel <= -25)
GUARD_MOUNT_Y2 = -10.0    # mid standoff boss (clear of window -18..-12 & front wheel >= -5)
GUARD_MOUNT_Y3 = 21.5     # front standoff boss (ahead of front wheel, low z=5.5)
GUARD_MOUNT_Z = 12.0
GUARD_MOUNT_Z3 = 5.5

# ---- Weapon & uprights ---------------------------------------------------------------------------
WPN_Y = 8.0               # weapon shaft Y
WPN_Z = 40.0              # weapon shaft Z (clears top_plate & gives >=3.5mm battery-weapon gap)
WPN_DISC_OD = 56.0        # 56 mm OD vertical spinner disc (bottom at z=12.0, top at z=68.0)
WPN_DISC_R = WPN_DISC_OD / 2.0
WPN_DISC_T = 1.5          # 1.5 mm titanium disc
WPN_DISC_X = -3.55        # disc center (-4.30..-2.80), flush against GR1507 bell cap at -2.80
WPN_MOTOR_X = 3.9         # GR1507 origin (rot [0,180,0] -> base at 14.3, bell cap at -2.8)

UPRIGHT_X_IN = 14.3       # inner face of each upright (28.6 mm inner gap for GR1507)
UPRIGHT_X_OUT = 17.5      # outer face of each upright (3.2 mm thick printed nylon)
UPRIGHT_X_MID = 0.5 * (UPRIGHT_X_IN + UPRIGHT_X_OUT)  # 15.9
UPRIGHT_T = UPRIGHT_X_OUT - UPRIGHT_X_IN              # 3.2
UPRIGHT_TAB_X = 20.5      # outboard mounting screw X (clear of upright wall)
UPRIGHT_Z0 = TOP_PLATE_Z1 # 23.0
UPRIGHT_TOP_Y = -4.0
UPRIGHT_TOP_Z = 71.0
UPRIGHT_TOP_R = 5.5

TOP_ROD_R = 2.0           # 4 mm OD aluminium standoff rod
WPN_SHAFT_R = 2.0         # 4.0 mm continuous steel shaft (GR1507 + MR84ZZ)

# ---- Front orange fork mounts & titanium forks ---------------------------------------------------
FORK_X = 24.0             # fork center X (between uprights at 20.5 and wheels at 36.25)
FORK_MOUNT_Y0 = 24.0      # sits flush against front of chassis (y = 24)
FORK_MOUNT_Y1 = 35.0
FORK_PIN_Y = 30.0
FORK_PIN_Z = 7.5
FORK_LEN = 38.0           # extends forward to y = 68 mm
FORK_TIP_Z = 1.0          # 1.0 mm floor clearance at tip

# ---- Electronics positions -----------------------------------------------------------------------
BAT_AT = [0.0, -30.0, CAVITY_Z0 + 5.6]   # lipo_2s_350 (36x17x11) rotated 90 deg -> x=-8.5..8.5, y=-48..-12
RX_AT = [-18.5, -15.2, 11.5]             # bbb_malenki_nano rotated -90 deg, clear of battery (-8.5) & tub boss (-28.2)
ESC_AT = [20.5, -11.0, 10.0]             # bbb_brushless_esc_20a rotated 90 deg -> x=14.5..26.5, y=-22.5..0.5
SW_AT = [0.0, -25.0, 19.32]             # fingertech_mini_switch -> touches top_plate (22.50), clears battery (<=14.6)
XT30_AT = [16.5, -27.0, 9.0]             # xt30u_m -> x=9.6..23.4, y=-29.6..-24.4

# ---- Colors --------------------------------------------------------------------------------------
COLOR_GREEN_PLATE = "#164226"
COLOR_NYLON_WHITE = "#e6eae2"
COLOR_TPU_BLUE = "#283593"
COLOR_ORANGE_MOUNT = "#f24c27"
COLOR_METAL_SILVER = "#b8bec4"
COLOR_WHEEL_GRAY = "#5c6066"
COLOR_TUB_DARK = "#23272c"
COLOR_LOCK_RED = "#ff2e00"
