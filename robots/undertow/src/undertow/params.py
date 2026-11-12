"""Undertow masters and derived relations. UNTESTED: never built, run, rendered or verified.

Frame (same as Revron): X right, Y forward (front attachment end), Z up, floor at Z = 0.
Rule: every number used by geometry lives here, as a MASTER (a design choice, with why / source) or a DERIVED relation
of masters and catalogue dimensions. COTS dimensions and masses come from robot/cots_alts.py / robot/catalog.py, never
retyped. The tub is symmetric in X and Y: geometry builds ONE quadrant (+X, +Y) and mirrors it.
"""
import math

from robot import catalog, cots_alts
from robot.profile import Profile
from robot.cad import bay as _bay
from robot.cad import fastener_catalog as fc

from .settings import SETTINGS, ESC_WITH_RX

RULES = Profile()   # aws2025: Antweight World Series 2025 (robot/profile.py, robot/rules/combat_rules.md)

# ---------------------------------------------------------------------------------------------------------- rules
MASS_LIMIT_G = RULES.mass_limit(roller=True)       # 150 g (wheeled robot)
CUBE = 101.6                                      # AWS rules v4.3 sec 2b: fits fully inside a 4 in (101.6 mm) cube in start config (robot/profile.py footprint_mm=150 is NOT this rule)
ENVELOPE_MARGIN = 1.0                              # per side: print / bend tolerance, skirt slop; start envelope must be <= CUBE - 2*margin
ENVELOPE_MAX = CUBE - 2 * ENVELOPE_MARGIN
FOOTPRINT_PROFILE = RULES.footprint_mm            # kept for the repo checker only
GROUND_MIN = RULES.min_ground_clearance_mm         # lowest non-wheel point over the floor
WALL_TPU_MIN = RULES.min_wall_tpu_mm
FORK_ANGLE_RANGE = RULES.wedge_angle_deg           # (min, max) wedge / fork angle the rules checker accepts
MASS_MARGIN_G = 5.0                                # design target: stay this far under MASS_LIMIT_G (weigh-in scales, glue, tape)

# ------------------------------------------------------------------------------------------------- COTS (catalogue)
MOTOR_ID, WHEEL_ID, ESC_ID = SETTINGS["motor"], SETTINGS["wheel"], SETTINGS["esc"]
BATTERY_ID, SWITCH_ID = SETTINGS["battery"], SETTINGS["switch"]
RX_ID = None if ESC_ID in ESC_WITH_RX else SETTINGS["rx"]

MOTOR = cots_alts._resolve(cots_alts.GEARMOTORS)[MOTOR_ID]      # overall, shaft_len, gb_len, mass_g, rpm_nominal, stall_current_a
MOTOR_FMT = cots_alts.GEARMOTOR_FORMAT                           # gb_w x gb_h plate stack (12 x 10 for N10/N20)
WHEEL = cots_alts._resolve(cots_alts.WHEELS)[WHEEL_ID]          # od, width
ESC = cots_alts.ESCS[ESC_ID]                                     # l, w, h, props.cont_current_a
BATTERY = cots_alts.BATTERIES[BATTERY_ID]                        # l, w, h, mah, c
SWITCH = cots_alts.SWITCHES[SWITCH_ID]                           # body, hole_pitch


def cat_mass(cid):
    """Catalogue mass (g) of one COTS part; 0 for None. Same source robot/gen/budget.py:cat_mass uses."""
    return 0.0 if cid is None else float(catalog.find(cid).mass_g)


# ---------------------------------------------------------------------------------------------------- drive masters
N_WHEELS = 4                       # 4WD: all the robot's weight is on driven tyres (pushing force = mu m g, not mu m g * share)
WHEEL_PROUD = 1.5                  # tyre stands this far past BOTH plate faces: drives either way up; >= GROUND_MIN
WHEEL_RUN = _bay.RUNNING_CLEARANCE # wheel to anything that does not turn with it (robot/cad/bay.py, checks/interference)
WHEELBASE = 54.0                   # axle to axle: battery + ESC band between motor rows, length inside ENVELOPE_MAX
SPINE_HALF = 5.5                   # half width of the centre spine between motor backs (sized by the cube width, see HALF_W_ALL)
MOTOR_FIT = _bay.PRINTED_FIT_CLEARANCE   # motor pocket clearance per side (TPU grips the plate stack)

# derived drive geometry
WHEEL_OD, WHEEL_W = WHEEL["od"], WHEEL["width"]
Z_AXLE = WHEEL_OD / 2                                          # axle on the robot mid-plane: identical either way up
Y_AXLE = WHEELBASE / 2
MOTOR_BODY = MOTOR["overall"] - MOTOR["shaft_len"]             # can + gearbox, motor back to gearbox face
X_MOTOR_BACK = SPINE_HALF                                      # motor back face against the spine
X_GB_FACE = X_MOTOR_BACK + MOTOR_BODY                          # gearbox face (shaft root)
X_WHEEL_IN = X_GB_FACE + WHEEL_RUN                             # wheel inner face: runs clear of the gearbox plate
X_WHEEL_C = X_WHEEL_IN + WHEEL_W / 2
X_WHEEL_OUT = X_WHEEL_IN + WHEEL_W
SHAFT_ENGAGE = min(MOTOR["shaft_len"] - WHEEL_RUN, WHEEL_W)   # shaft length inside the hub (check: >= 2/3 of the hub, BRIEF risk)

# ----------------------------------------------------------------------------------------------- chassis masters
WALL = 2.4                         # TPU outer wall: 2 x the rules TPU minimum; flexes and returns under a tooth instead of cracking
RIB = 1.6                          # internal TPU ribs between bays (bay.DEFAULT_WALL)
CORNER_R = 9.0                     # plan-view outer corner radius: no corner for a horizontal spinner tooth to bite
PLATE_T_TOP = 0.8                  # carbon laminate top plate (stiff, light, takes vertical-spinner glancing hits)
PLATE_T_BASE = 0.8                 # carbon laminate base plate (same part number family: invertible robot has two "tops")
PLATE_MATERIAL = "carbon_fibre"
TUB_MATERIAL = "tpu_95a"
PLATE_LIGHTEN_R = 4.0              # radius of the lightening windows over the motor rows (stay clear of bolts and tub ribs)

# derived chassis envelope
Z_BASE = WHEEL_PROUD                                   # base plate underside
Z_TOP = WHEEL_OD - WHEEL_PROUD                         # top plate top face
Z_TUB0, Z_TUB1 = Z_BASE + PLATE_T_BASE, Z_TOP - PLATE_T_TOP
TUB_H = Z_TUB1 - Z_TUB0
HALF_W_TUB = X_WHEEL_OUT + WHEEL_RUN + WALL            # tub outer face, wheel fully inside
HALF_L_TUB = Y_AXLE + WHEEL_OD / 2 + WHEEL_RUN + WALL  # symmetric front / rear
WELL = dict(x0=X_WHEEL_IN - WHEEL_RUN, x1=X_WHEEL_OUT + WHEEL_RUN,      # wheel well, open through both plates
            y0=Y_AXLE - WHEEL_OD / 2 - WHEEL_RUN, y1=Y_AXLE + WHEEL_OD / 2 + WHEEL_RUN)

# ------------------------------------------------------------------------------------------- bays (catalogue parts)
BAT_Y = BATTERY["w"] / 2 + _bay.POUCH_CLEARANCE + RIB / 2      # battery long side along X, front of the centre rib
ESC_Y = -(ESC["w"] / 2 + _bay.PRINTED_FIT_CLEARANCE + RIB / 2) # ESC behind the centre rib
Z_BAY = Z_TUB0                                                 # parts sit on the base plate, drop in from the top (insert -z)
SWITCH_Y = ESC_Y                                               # switch beside the ESC, -X end (spine too narrow at 5.5)
SWITCH_X = -(ESC["l"] / 2 + RIB + SWITCH["body"][0] / 2 + _bay.PRINTED_FIT_CLEARANCE)
SWITCH_ACCESS_R = RULES.driver_access_radius_mm                # access hole in BOTH plates (invertible: reachable either way up)

# ------------------------------------------------------------------------------------------------------ fastening
# Revron scheme (aluminium standoffs carry the clamp, printed body floats; M2 CSK both ends) adapted to a TPU tub:
# TPU cannot hold heat-sets, so each site is an M2 aluminium standoff through the tub, M2 CSK screws from both plates.
PLATE_SCREW = "M2x4"
PLATE_HEAD = "csk"
STANDOFF_D = 4.0                   # M2 round standoff OD (catalogue `standoff` not yet in robot/catalog.py: estimate)
BOLT_INSET = WALL + STANDOFF_D / 2 + 0.6   # standoff centre from the tub outer face
# quadrant sites (+X, +Y), mirrored to all four quadrants: in the end wall, centred over the motor body (the corners are
# taken by the wheel wells). Mid sites: Y = 0 just inside the side wall, between the two wheel wells; mirrored in X only.
BOLT_SITES_Q = [(X_MOTOR_BACK + MOTOR_BODY / 2, HALF_L_TUB - BOLT_INSET)]
BOLT_SITES_MID = [(HALF_W_TUB - BOLT_INSET, 0.0)]
RX_X = ESC["l"] / 2 + RIB + 10.0   # receiver beside the ESC (decased FS-iA6 is 20 long: 10 = its half length, catalog.py)

# ---------------------------------------------------------------------------------------------- front mount (shared)
# ONE interface for both fronts: a pivot pin along X on the mid-plane, carried by two tub cheeks. Both attachments hang
# on it and self-level by gravity; inverted they swing over the pin to the new floor.
PIN_SCREW_D = 3.0                  # M3 steel cap screw used as the pivot pin (nyloc at the far cheek)
PIN_Z = Z_AXLE                     # mid-plane: same pin height either way up
CHEEK_T = 4.0                      # TPU cheek thickness along X
CHEEK_REACH = 5.0                  # pin axis ahead of the tub front face (5 not 7: the folded plough must fit the 101.6 cube)
CHEEK_HALF_X = HALF_W_TUB - CORNER_R          # cheeks just inside the front corner radii
PIN_Y = HALF_L_TUB + CHEEK_REACH
PIN_LEN_NEED = 2 * CHEEK_HALF_X + CHEEK_T     # pin length through both cheeks
PIN_SCREW = f"M3x{int(math.ceil(PIN_LEN_NEED / 5.0) * 5 + 5)}"   # next stock length + nut
PIN_CLEAR = fc.clearance(PIN_SCREW_D, "loose")  # fork / plough eye: free to swing
EYE_R = PIN_CLEAR / 2 + 1.6                   # material round the pin in the eye
UP_STOP_DEG = 90.0                            # START CONFIG: attachment folded up vertical against the front-wall stop (inside the cube); it drops onto the floor when the robot first drives/brakes
FRONT_TIP_GAP = 0.3                           # tip-to-floor gap when resting (rules wedge_gap 0.2..1.5): gravity sets it at 0

# fork variant
FORK_N = 5
FORK_T = 0.8                       # hardened spring steel (CS95 / 1095, 48-52 HRC) sheet thickness
FORK_W = 6.0                       # tine width at the root
FORK_TIP_W = 2.0
FORK_SPAN = 2 * CHEEK_HALF_X - CHEEK_T - 2.0  # forks spread over the pin between the cheeks
FORK_PITCH = FORK_SPAN / (FORK_N - 1) if FORK_N > 1 else 0.0
FORK_REACH = 34.0                  # pin to tip along the fork (long reach: under the opponent before its weapon reaches us)
FORK_REST_DEG = math.degrees(math.asin((PIN_Z - FRONT_TIP_GAP) / FORK_REACH))   # resting slope; check in FORK_ANGLE_RANGE
FORK_BEND_R = 1.0 * FORK_T         # inside bend radius of the tip kick-down (hardened sheet: >= 1 t)
FORK_TIP_KICK = 1.5                # tip bent down this far so it skims, not digs
FORK_SPACER_L = FORK_PITCH - FORK_T  # TPU spacer tube between forks on the pin

# plough variant
PLOUGH_T_STEEL = 0.6               # hardened steel face sheet
PLOUGH_BODY_T = 6.0                # TPU body thickness behind the face (shock absorber for horizontal spinners)
PLOUGH_REACH = 26.0                # pin to lip along the face (shorter, stiffer than the forks)
PLOUGH_REST_DEG = math.degrees(math.asin((PIN_Z - FRONT_TIP_GAP) / PLOUGH_REACH))
PLOUGH_W = 2 * CHEEK_HALF_X - CHEEK_T - 1.0
PLOUGH_EDGE_R = 3.0                # rounded side edges in plan

# --------------------------------------------------------------------------------------------------------- skirts
SKIRT_T = 0.5                      # grade 5 titanium sheet
SKIRT_MATERIAL = "titanium_gr5"
SKIRT_BEND_R = 2.0 * SKIRT_T       # rolled hinge knuckle inside radius (Ti gr5 minimum ~2-2.5 t)
SKIRT_PIN_D = 1.0                  # music-wire hinge pin
SKIRT_GAP = 0.5                    # skirt to tub flank when swung in
SKIRT_DROP = 0.4                   # lower edge above the floor when resting (gravity closes it to touching on a bump)
FLANK_DEG = 15.0                   # tub flank V-faces lean this far from vertical (15 not 25: width budget of the 101.6 cube)
SKIRT_PIN_Z = Z_AXLE               # hinge on the mid-plane: the skirt hangs to whichever side is down
SKIRT_DEPTH = (SKIRT_PIN_Z - SKIRT_DROP) / math.cos(math.radians(FLANK_DEG))   # hinge to edge along the sloped leaf
SKIRT_SIDE_LEN = 2 * (HALF_L_TUB - CORNER_R)  # straight run of the sides; corners stay TPU (rounded)
SKIRT_REAR_LEN = 2 * (HALF_W_TUB - CORNER_R)

# ------------------------------------------------------------------------------------------------- overall checks
HALF_W_ALL = HALF_W_TUB + SKIRT_GAP + SKIRT_T + SKIRT_DEPTH * math.sin(math.radians(FLANK_DEG))
# START configuration (what the cube rule measures): attachment folded up vertical on the pin (UP_STOP_DEG = 90)
Y_FRONT_START = PIN_Y + max(EYE_R + FORK_T, PLOUGH_BODY_T + PLOUGH_T_STEEL)   # folded: only its thickness ahead of the pin
Z_TOP_START = max(Z_TOP, PIN_Z + max(FORK_REACH, PLOUGH_REACH))                # folded attachment stands above the plate
Y_FRONT_RUN = PIN_Y + max(FORK_REACH, PLOUGH_REACH)    # after it drops (running config; the cube rule is a start rule)
Y_REAR_ALL = -(HALF_L_TUB + SKIRT_GAP + SKIRT_T + SKIRT_DEPTH * math.sin(math.radians(FLANK_DEG)))
LENGTH_START = Y_FRONT_START - Y_REAR_ALL
WIDTH_ALL = 2 * HALF_W_ALL
FITS_CUBE = max(LENGTH_START, WIDTH_ALL, Z_TOP_START) <= ENVELOPE_MAX
CENTRE_Y_OFFSET = (Y_FRONT_START + Y_REAR_ALL) / 2    # robot is not centred on Y=0 in the cube: place the cube here


# --------------------------------------------------------------------------------------------- material densities
DENSITY = dict(tpu_95a=1.21, carbon_fibre=1.55, titanium_gr5=4.43, spring_steel=7.85, steel=7.85, alu=2.70)   # g/cm3
