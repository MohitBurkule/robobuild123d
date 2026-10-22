"""Elevron Alt drive and weapon masters (RVRN_revdev STEP placements, STEP frame). Wheels, hubs, tyres and the
Drisk_floating_3 disc are the Revron parts; only where they sit is new."""
from robot.catalog import BEARINGS, find
from .params_chassis import HX, IN_X, AXLE_Y, AXLE_Z

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
TYRE_OD, TYRE_W = 21.5, 9.5            # RV22 Scalextric F1 tyre (Revron TY_REAR)
HUB_LEN = 12.0                         # RV21 rear hub length (Revron RH_LEN)
WHEEL_GAP = 0.2                        # hub inner face off the chassis side wall (STEP: 29.7 vs 29.5)
WY, WZ = 59.2, 23.5                    # weapon spin axis (along X): spiderSL / Drisk centre in the STEP
UP_IN, UP_T = 13.5, 6.0                # vert_mod uprights: inner face |X| and thickness
DISC_T, SPIDER_T = 3.0, 3.0            # Drisk_floating_3 Hardox, spiderSL
PROP_LEN = 14.0                        # RV07 prop mount (15 dia x 14)
# -----------------------------------------------------------------------------------------------------------------------
TYRE_R = TYRE_OD / 2
FLOOR_LIFT = TYRE_R - AXLE_Z           # STEP frame -> robot world (floor at z 0): 2.25
HUB_X0 = HX + WHEEL_GAP                # hub inner face |X|
TYRE_X0 = HUB_X0 + HUB_LEN - TYRE_W    # tyre flush with the hub's outer end
WHEEL_OUT = HUB_X0 + HUB_LEN           # outermost wheel face |X| (41.7)
AXLES = (-AXLE_Y, AXLE_Y)              # front (standoff idler) and rear (N10) axle lines
DRIVE_MOTOR = "n10_2200rpm_spicy"
N10_X = IN_X - find(DRIVE_MOTOR).shaft["at"][0]   # gearbox face on the wall inner face, shaft out through the keyhole (19.6)
# weapon stack along +X from the motor base on the left upright's inner face
MOTOR_LEN = 20.5                       # BE1806: base to bell face (catalog)
MOTOR_X0 = -UP_IN + 0.2                # motor base 0.2 off the upright (STEP RV08 x -13.3)
MOTOR_X1 = MOTOR_X0 + MOTOR_LEN        # bell face (7.2)
PROP_X1 = UP_IN + UP_T + 2.7           # prop-mount end past the right upright (STEP 22.2)
PROP_X0 = PROP_X1 - PROP_LEN           # 8.2: the spider sits against it
SPIDER_X = (PROP_X0 - SPIDER_T, PROP_X0)
DISC_X = (SPIDER_X[0] - DISC_T, SPIDER_X[0])
BRG = BEARINGS["mf85"]                 # FS4 MF85ZZ flanged: bore, OD, width
BRG_X0 = UP_IN - 0.8                   # flange 0.8 proud of the right upright's inner face (STEP 12.7)

__all__ = [n for n in dir() if not n.startswith("__")]
