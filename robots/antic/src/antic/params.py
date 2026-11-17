"""Parametric dimensions for AntiC (150g antweight pneumatic flipper)."""

# Coordinate frame: X right, Y forward, Z up, floor Z = 0.

# Overall envelope (mm)
LENGTH = 108.0
WIDTH = 96.0
HEIGHT = 48.0

# Chassis base & side rails
BASE_T = 2.0
BASE_Z = 2.0  # ground clearance under baseplate
SIDE_RAIL_T = 2.0
SIDE_RAIL_X = 46.0  # outer face at X = +-47 mm (width = 94 mm)

# 4WD Geared Drivetrain (2 wheels + 1 central spur gear per side)
WHEEL_R = 12.5       # 25 mm OD ribbed/toothed wheels
WHEEL_W = 10.0
WHEEL_X = 38.0       # wheel center X
WHEEL_REAR_Y = -36.0
WHEEL_FRONT_Y = -8.0
WHEEL_Z = WHEEL_R    # 12.5 mm so wheels touch Z = 0
GEAR_Y = -22.0       # central spur gear between rear & front wheels
GEAR_Z = 22.0
GEAR_R = 4.2
GEAR_W = 6.0
AXLE_R = 1.5

# Pneumatic system
TANK_R = 13.5        # 27 mm OD buffer tank / CO2 cylinder
TANK_L = 58.0
TANK_Y = -20.0
TANK_Z = 27.0
HEX_NUT_R = 6.5      # blue anodized hex fitting on right side
HEX_NUT_T = 5.0
RAM_R = 5.5          # blue pneumatic actuator cylinder
RAM_L = 34.0

# Flipper / Wedge assembly
HINGE_Y = -10.0
HINGE_Z = 46.0
FRONT_TIP_Y = 52.0
FRONT_TIP_Z = 0.5
WEDGE_W = 88.0       # fits cleanly between side rails
FLIPPER_T = 2.5
TIP_T = 2.0
SKIRT_T = 1.2

# Electronics bay (rear open-top bay)
ELEC_Y_MIN = -44.0
ELEC_Y_MAX = -26.0
ELEC_Z = 33.0
