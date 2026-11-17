"""Buzzkill masters and derived geometric relations.

Frame: X left (+X), Y forward (+Y), Z up (+Z). Wheel centres at Z = 0, floor at Z = -WHEEL_R (-15.0 mm).
Weapon bay is offset on the front-right (-X, +Y), matching the reference robot.
"""

from __future__ import annotations

import math

from robot import catalog as C
from robot.cad import fastener_catalog as FC
from robot.profile import Profile

# --------------------------------------------------------------------------- rules (AWS 2025)
RULES = Profile()
MASS_LIMIT_G = RULES.roller_mass_g          # 150.0 g
FOOTPRINT_MM = RULES.footprint_mm           # 150.0 mm
MOVING_CLR = RULES.min_clearance_moving_mm  # 0.4 mm
MIN_WALL = RULES.min_wall_fdm_mm            # 0.9 mm

# --------------------------------------------------------------------------- COTS selections
WEAPON_MOTOR = "bbb_be1806_2300kv"
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "durahubs_25"
BATTERY = "gnb_2s_450_80c"
WEAPON_ESC = "bbb_brushless_esc_20a"
DRIVE_ESC = "bbb_malenki_nano"
SWITCH = "fingertech_mini_switch"

WHEEL_OD = 25.0
WHEEL_R = WHEEL_OD / 2.0                    # 12.5 mm
WHEEL_W = 8.0
FLOOR_Z = -WHEEL_R                          # -12.5 mm

# --------------------------------------------------------------------------- body envelope
BODY_HALF_W = 65.0                          # 130.0 mm overall width
BODY_Y0 = -40.0                             # rear edge
BODY_Y1 = 45.0                              # front edge
TUB_FLOOR_Z = -11.3                         # 1.2 mm ground clearance
TUB_FLOOR_T = 1.0                           # bottom floor thickness (Z: -11.3 .. -10.3)
TUB_TOP_Z = 13.0                            # top of tub walls (0.5 mm clear above 25 mm wheels)
LID_T = 0.9                                 # top lid thickness (Z: 13.0 .. 13.9)
WALL = 1.25                                 # nominal perimeter wall thickness
CHAMFER_TOP_INSET = 0.0                     # clean single-extrude wall

# --------------------------------------------------------------------------- weapon bay & drisk
# Motor axis along +X. Motor in catalog frame: base [-9.25, -5.75], bell [-5.75, +9.25], shaft [+9.25, +12.25]
# Placed with rot=[0,0,0] at X_MOT = -24.0:
#   base back face at X = -33.25
#   bell spans X = -29.75 .. -14.75 (R = 11.5 mm)
#   bell top face at X = -14.75 (4x M2 on 9 mm circle)
X_MOT = -24.0
Y_AX = 26.0
Z_AX = 15.0                                 # disc R=22.5 -> bottom at -7.5 (5.0 mm off floor), top at +37.5

DISC_OD = 43.0
DISC_R = DISC_OD / 2.0                      # 21.5 mm
DISC_RING_X0 = -16.9                        # drisk ring wraps around the bell (2.7 mm wide)
DISC_RING_X1 = -14.2                        # overlaps DISC_WEB_X0 (-14.75) for 1 solid
DISC_WEB_X0 = -14.75                        # mates to bell top face
DISC_WEB_X1 = -13.25                        # 1.5 mm thick web
DISC_BELL_R = 11.5
DISC_RING_ID = 2 * (DISC_BELL_R + 0.8)      # 24.6 mm (0.8 mm radial clearance around 23 mm bell)

# Weapon bay notch in tub:
NOTCH_X0 = -33.25                           # inner face of outboard upright (mates to motor base)
NOTCH_X1 = -6.0                             # outer face of inboard bearing plate
NOTCH_Y0 = -2.0                             # rear clearance behind 43 mm disc

# Outboard upright (2.0 mm laser-cut titanium plate bolted to tub):
UPRIGHT_X0 = -35.25
UPRIGHT_X1 = -33.25                         # 2.0 mm thick
UPRIGHT_BOSS_R = 11.5                       # circular teardrop around motor base

# Inboard bearing (MR84: 4 mm ID, 8 mm OD, 3.0 mm wide) in 2.0 mm CNC-milled aluminium plate:
BEARING_ID = 4.0
BEARING_OD = 8.0
BEARING_W = 3.0
BEARING_X0 = -7.0
BEARING_X1 = -4.0                           # seated in inboard plate X = -6.0 .. -4.0

# Shaft (4 mm steel rod): bridges from bell/disc into inboard MR84 bearing
SHAFT_R = 2.0
SHAFT_X0 = -11.25                           # 0.5 mm clear of BE1806 shaft end (-11.75)
SHAFT_X1 = -4.2                             # ends inside MR84 bearing, 0.2 mm clear of tub wall

# --------------------------------------------------------------------------- drive (2WD enclosed)
DRIVE_Y = -25.5
DRIVE_Z = 0.0
WHEEL_X = 43.5                              # wheel center X (+-43.5 mm; outer face at +-47.5)
MOTOR_X = 23.0                              # N10 body centered around +-23 mm

# --------------------------------------------------------------------------- electronics placements
# Battery: GNB 2S 450mAh (61 x 17 x 14 mm + XT30 lead on +Y in catalog frame).
# Rotated -90 deg around Z so 61 mm is along Y (-17.6 .. 43.4), 17 mm along X (2.5 .. 19.5), XT30 pointing +X:
BAT_AT = [11.0, 12.9, -3.3]
BAT_ROT = [0.0, 0.0, -90.0]

# Malenki-Nano: 32 x 19 x 2.5 mm. Flat on tub floor (X=24..56, Y=-9.5..9.5) clear of battery and wheel_l:
DESC_AT = [40.0, 0.0, -9.05]
DESC_ROT = [0.0, 0.0, 0.0]

# Weapon ESC (20A): 23 x 12 x 4 mm. Placed flat on tub floor (Z = -10.3 .. -6.3) below right drive motor:
WESC_AT = [-24.0, -22.0, -8.3]
WESC_ROT = [0.0, 0.0, 90.0]

# Switch (FingerTech Mini): 12.7 x 12.7 x 6.35 mm. On top-left deck (like photo), recessed under lid slot:
SW_AT = [48.0, 12.0, 9.0]
SW_ROT = [0.0, 0.0, 90.0]

# --------------------------------------------------------------------------- forks / wedgelets
FORK_T = 1.5                                # 1.5 mm titanium
FORK_L_Y0 = 28.0                            # left fork bolted to front of tub
FORK_R_Y0 = -2.0                            # right fork bolted to beveled front-right of tub
FORK_Y1 = 51.0                              # tip leads at Y = 51.0
FORK_Z_TIP = FLOOR_Z + 0.6                  # -11.9 mm (0.6 mm off floor)
FORK_L_X = -1.0                             # left of weapon bay
FORK_R_X = -43.0                            # right of outboard upright (under beveled front)

# --------------------------------------------------------------------------- hoop (self-righter)
HOOP_Y = -6.0
HOOP_R_TUBE = 1.5                           # 3.0 mm diameter arch
HOOP_X_SPAN = 67.5                          # bows outward above side walls (BODY_HALF_W=65)
HOOP_Z_BASE = 4.0
HOOP_Z_PEAK = 48.0                          # clears 39.0 mm disc top

# --------------------------------------------------------------------------- fasteners (heatset M2)
INSERT_D, _ = FC.insert(2)                # 3.2 mm hole dia for M2 heat-set insert
INSERT_L = 3.0                              # heatset_m2 catalog length (3.0 mm)

LID_SCREWS = [
    (61.5, 4.0),
    (61.5, -18.0),
    (26.0, 40.5),
    (24.0, -36.5),
    (-24.0, -36.5),
    (-61.5, -18.0),
    (-61.5, 0.0),
]

# Outer stealth polygon (CCW in XY; front-right beveled back to (-36.25, 14) for upright + motor access)
OUTER_POLY = [
    (-36.0, BODY_Y0),
    (36.0, BODY_Y0),
    (BODY_HALF_W, -20.0),
    (BODY_HALF_W, 16.0),
    (34.0, BODY_Y1),
    (-4.0, BODY_Y1),
    (-4.0, NOTCH_Y0),
    (-35.25, NOTCH_Y0),
    (-35.25, 14.0),
    (-BODY_HALF_W, 2.0),
    (-BODY_HALF_W, -20.0),
]
