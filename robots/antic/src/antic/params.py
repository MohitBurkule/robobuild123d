"""Parametric dimensions for AntiC (150g antweight pneumatic flipper)."""

# Coordinate frame: X right, Y forward, Z up, floor Z = 0.

# Overall envelope (mm)
LENGTH = 108.0
WIDTH = 96.0
HEIGHT = 48.0

# Chassis base & side rails
BASE_T = 2.0
BASE_Z = 2.0
SIDE_RAIL_T = 2.0
SIDE_RAIL_X = 44.5  # outer face at X = +-45.5 mm

# 4WD Geared Drivetrain (2 wheels + 1 central spur gear per side)
WHEEL_R = 12.5       # 25 mm OD ribbed/toothed wheels
WHEEL_W = 10.0
WHEEL_X = 37.5       # wheel center X
WHEEL_REAR_Y = -36.0
WHEEL_FRONT_Y = -6.0
WHEEL_Z = WHEEL_R    # 12.5 mm so wheels touch Z = 0
GEAR_Y = -21.0       # central spur gear right between rear & front wheels
GEAR_Z = 12.5        # collinear with wheel axles!
GEAR_R = 5.4
GEAR_W = 6.0
AXLE_R = 1.6

# Pneumatic system
TANK_R = 14.5        # 29 mm OD silver buffer tank / CO2 cylinder
TANK_L = 56.0
TANK_Y = -20.0
TANK_Z = 27.0
HEX_NUT_R = 6.5      # blue anodized hex fitting on right side
HEX_NUT_T = 4.5
RAM_R = 5.5          # blue pneumatic actuator cylinder
RAM_L = 32.0

# Flipper / Wedge assembly
HINGE_Y = -10.0
HINGE_Z = 46.0
FRONT_TIP_Y = 52.0
FRONT_TIP_Z = 0.5
WEDGE_W = 91.0       # full width meeting the side rails cleanly
FLIPPER_T = 2.5
TIP_T = 2.0
SKIRT_T = 1.2
