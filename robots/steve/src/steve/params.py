"""Parametric dimensions for Steve (Stewie) — UK 150g rear-hinged flipper.

Frame convention (robot/GUIDE.md):
  +X : Left
  +Y : Forward
  +Z : Up (floor at Z = 0)
"""
import math

# ---- Overall envelope & stance ---------------------------------------------------------------
GROUND_CLEARANCE = 2.0       # mm under chassis floor
WHEEL_D = 28.0               # mm tyre OD
WHEEL_W = 8.0                # mm tyre width
AXLE_Z = WHEEL_D / 2.0       # 14.0 mm -> tyres sit on Z = 0
WHEEL_Y = -20.0              # mm rear axle Y
WHEEL_X = 39.0               # mm wheel centre |X|

# ---- Chassis (tub) ---------------------------------------------------------------------------
TUB_W = 68.0                 # mm main body width (X in [-34, +34])
TUB_REAR_Y = -42.0           # mm rear face
TUB_DECK_END_Y = 8.0         # mm where flat top deck transitions to front slope
TUB_FRONT_Y = 34.0           # mm front nose of chassis side pods
TUB_TOP_Z = 30.0             # mm top of chassis walls (below 1.5 mm lids -> 31.5 mm total)
TUB_FRONT_Z = 12.0           # mm height of front nose of side pods
WALL_T = 2.5                 # mm side/rear wall thickness
FLOOR_T = 2.0                # mm bottom floor thickness

# Central flipper slot in chassis
SLOT_W = 18.0                # mm central channel width (X in [-9, +9])
SLOT_REAR_Y = -38.0          # mm rear of central slot

# Wheel well & outboard wheel guard
WELL_Y_MIN = WHEEL_Y - WHEEL_D / 2.0 - 2.5   # -36.5
WELL_Y_MAX = WHEEL_Y + WHEEL_D / 2.0 + 2.5   # -3.5
GUARD_X = WHEEL_X + WHEEL_W / 2.0 + 2.5      # 45.5 mm inner face of wheel guard
GUARD_T = 1.5                                # mm wheel guard plate thickness
GUARD_H = 26.0                               # mm wheel guard height
GUARD_L = 32.0                               # mm wheel guard length

# ---- Top lids (split left & right) -----------------------------------------------------------
LID_T = 1.5                  # mm polycarbonate/printed top lid thickness
LID_Z = TUB_TOP_Z            # 30.0 mm bottom of lids

# ---- Rear-hinged central flipper arm ---------------------------------------------------------
HINGE_Y = -34.0              # mm rear hinge axis Y
HINGE_Z = 25.0               # mm rear hinge axis Z
HINGE_PIN_D = 2.0            # mm steel hinge pin diameter
ARM_W = 15.0                 # mm flipper arm width (1.5 mm clearance per side in 18 mm slot)
ARM_FRONT_Y = 32.0           # mm front tip of printed flipper arm
ARM_FRONT_Z = 10.0           # mm height of printed arm at front
FLIP_OPEN_DEG = 40.0         # deg upward travel

# ---- Front metal flipper scoop ---------------------------------------------------------------
SCOOP_T = 1.2                # mm brushed aluminium/titanium sheet scoop
SCOOP_TOP_W = 54.0           # mm width at top edge
SCOOP_BOT_W = 82.0           # mm width at front leading edge
SCOOP_LEN = 30.0             # mm sloped length from top edge to front lip
SCOOP_ANGLE_DEG = 24.0       # deg from horizontal (matches front slope)
SCOOP_TIP_Y = 48.0           # mm front leading edge Y
SCOOP_TIP_Z = 0.5            # mm front leading edge Z clearance above floor

# ---- Fasteners -------------------------------------------------------------------------------
M2_CLEAR_D = 2.2
M2_HEAD_D = 3.8
M2_HEAD_H = 1.6
M2_INSERT_D = 3.2
M2_INSERT_L = 3.5

# ---- Electronics & drive ---------------------------------------------------------------------
# N10/N20 motors along X at (WHEEL_Y, AXLE_Z)
MOTOR_X_OFFSET = 22.0        # mm motor body inner end |X|
SERVO_Y = -8.0               # mm flipper servo Y
SERVO_Z = 15.5               # mm flipper servo Z
HORN_Y = SERVO_Y + 5.0
HORN_Z = SERVO_Z + 4.0
