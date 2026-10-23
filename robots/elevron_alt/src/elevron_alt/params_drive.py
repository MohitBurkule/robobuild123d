"""Elevron Alt drive and weapon masters (RVRN_revdev STEP placements, STEP frame). Wheels, hubs, tyres and the
Drisk_floating_3 disc are the Revron parts; only where they sit is new."""
from robot.catalog import BEARINGS, BE1806_X0, find
from .params_chassis import HX, IN_X, AXLE_Y, AXLE_Z

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
TYRE_OD, TYRE_W = 21.5, 9.5            # RV22 Scalextric F1 tyre (Revron TY_REAR)
HUB_LEN = 12.0                         # RV21 rear hub length (Revron RH_LEN)
WHEEL_GAP = 0.2                        # hub inner face off the chassis side wall (STEP: 29.7 vs 29.5)
WY, WZ = 59.2, 23.5                    # weapon spin axis (along X): spiderSL / Drisk centre in the STEP
UP_IN = 13.3                           # vert_mod uprights: inner face |X| (the BE1806 base bolts flat to the left one)
UP_T = 4.0                             # left upright under the motor screw heads (counterbore floor)
DISC_GAP = 1.0                         # floating disc rides the bell's X boss, this far off the bell face (STEP 2.2)
DISC_PHASE = 200.0                     # disc and spider turned about the axis from the Revron drawing to the STEP's tooth angle
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
# weapon stack along +X (RVRN_revdev STEP): RV08 BE1806 base flat on the left upright at x -13.3, bell face at 1.2, the
# floating disc on its X boss, spider and prop mount
WEAPON_MOTOR = "be1806_stator"
MOTOR_X0 = -UP_IN                      # motor base on the upright's inner face
MOTOR_AT_X = MOTOR_X0 - BE1806_X0      # catalog origin
_sh = find(WEAPON_MOTOR).shaft
BELL_X = MOTOR_AT_X + _sh["at"][0]     # bell face (1.2)
DISC_X = (BELL_X + DISC_GAP, BELL_X + DISC_GAP + DISC_T)   # 2.2 .. 5.2
SPIDER_X = (DISC_X[1], DISC_X[1] + SPIDER_T)
PROP_X0 = SPIDER_X[1]                  # 8.2: prop-mount flange against the spider
PROP_X1 = PROP_X0 + PROP_LEN           # 22.2
MOTOR_BASE_X = MOTOR_X0
MOTOR_R = 11.5                         # catalog can radius
BASE_SKIN = 0.5                        # the shaft stops this far inside the stator base
SHAFT_D = 5.0                          # BE1806 shaft through the disc stack into the MF85
ROT_GAP = 0.3                          # prop-mount flange stops short of the MF85 flange (rotor / fixed race)
LEAD_Y = WY - 19.5                     # catalog stator: phase-lead stub tip (local -z 19.5), turned to point forward
BRG = BEARINGS["mf85"]                 # FS4 MF85ZZ flanged: bore, OD, width
BRG_X0 = UP_IN - 0.6                   # flange 0.6 proud of the right upright's inner face (STEP 12.7)
RUB_GAP = 1.0                          # weapon parts off the module (kin.rub_gap)
PROP_FLANGE_X1 = min(BRG_X0 - ROT_GAP, UP_IN - RUB_GAP)

__all__ = [n for n in dir() if not n.startswith("__")]
