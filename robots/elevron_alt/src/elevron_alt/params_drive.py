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
# weapon stack along +X: STEP RV08 base at x -13.3 on the left upright, a 15.3 mm can (6374 mm3 / pi 11.5^2), then
# disc, spider and prop mount on the bell face
WEAPON_MOTOR = "be1806_bbb"
STEP_CAN_LEN = 15.5
MOTOR_X0 = -UP_IN + 0.2                # STEP motor base, 0.2 off the upright face
DISC_X = (MOTOR_X0 + STEP_CAN_LEN, MOTOR_X0 + STEP_CAN_LEN + DISC_T)   # disc on the bell face (STEP 2.2 .. 5.2)
SPIDER_X = (DISC_X[1], DISC_X[1] + SPIDER_T)
PROP_X0 = SPIDER_X[1]                  # 8.2: prop-mount flange against the spider
PROP_X1 = PROP_X0 + PROP_LEN           # 22.2
_sh = find(WEAPON_MOTOR).shaft         # catalog: bell face (shaft root) at local x `at`, body symmetric about its origin
MOTOR_AT_X = DISC_X[0] - _sh["at"][0]  # catalog motor placed with its bell face on the disc
MOTOR_BASE_X = MOTOR_AT_X - (_sh["at"][0] + _sh["len"])
MOTOR_SINK = -UP_IN - MOTOR_BASE_X     # the catalog can is longer than the STEP one: its base sinks this far into the upright
MOTOR_R = 11.5                         # catalog can radius
SHAFT_D = 5.0                          # BE1806 shaft through the disc stack into the MF85
ROT_GAP = 0.3                          # prop-mount flange stops short of the MF85 flange (rotor / fixed race)
LEAD_Y = WY - 19.5                     # catalog stator: phase-lead stub tip (local -z 19.5), turned to point forward
BRG = BEARINGS["mf85"]                 # FS4 MF85ZZ flanged: bore, OD, width
BRG_X0 = UP_IN - 0.8                   # flange 0.8 proud of the right upright's inner face (STEP 12.7)
PROP_FLANGE_X1 = BRG_X0 - ROT_GAP

__all__ = [n for n in dir() if not n.startswith("__")]
