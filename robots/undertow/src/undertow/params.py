"""Undertow masters and derived relations.

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
RULESET = SETTINGS["rules"]
CUBE_V43 = 101.6                                   # AWS v4.3 sec 2b cube side (only for rules="aws_v43_cube")
ENVELOPE = dict(aws2025=dict(side=RULES.footprint_mm, height=None, start_folded=False),
                aws_v43_cube=dict(side=CUBE_V43, height=CUBE_V43, start_folded=True))[RULESET]
ENVELOPE_MARGIN = 1.0                              # per side: print / bend tolerance, skirt slop
ENVELOPE_MAX = ENVELOPE["side"] - 2 * ENVELOPE_MARGIN
HEIGHT_MAX = None if ENVELOPE["height"] is None else ENVELOPE["height"] - 2 * ENVELOPE_MARGIN
START_FOLDED = ENVELOPE["start_folded"]
GROUND_MIN = RULES.min_ground_clearance_mm         # lowest non-wheel point over the floor
WALL_FDM_MIN = RULES.min_wall_fdm_mm               # printed wall minimum for the tub material
FORK_ANGLE_RANGE = RULES.wedge_angle_deg           # (min, max) wedge / fork angle the rules checker accepts
MASS_MARGIN_G = 5.0                                # design target: stay this far under MASS_LIMIT_G

# ------------------------------------------------------------------------------------------------- COTS (catalogue)
MOTOR_ID, WHEEL_ID, ESC_ID = SETTINGS["motor"], SETTINGS["wheel"], SETTINGS["esc"]
BATTERY_ID, SWITCH_ID = SETTINGS["battery"], SETTINGS["switch"]
RX_ID = None if ESC_ID in ESC_WITH_RX else SETTINGS["rx"]

MOTOR = cots_alts._resolve(cots_alts.GEARMOTORS)[MOTOR_ID]      # overall, shaft_len, gb_len, mass_g, rpm_nominal, stall_current_a
WHEEL = cots_alts._resolve(cots_alts.WHEELS)[WHEEL_ID]          # od, width
ESC = cots_alts._resolve(cots_alts.ESCS)[ESC_ID]                # l, w, h, ports
BATTERY = cots_alts._resolve(cots_alts.BATTERIES)[BATTERY_ID]   # l, w, h, mah, c, conn
SWITCH = cots_alts._resolve(cots_alts.SWITCHES)[SWITCH_ID]      # body, hole_pitch

BAT = catalog.find(BATTERY_ID)     # resolved entry: shape frame + ports (pigtail included)
ESC_E = catalog.find(ESC_ID)
SW = catalog.find(SWITCH_ID)
RX_E = catalog.find(RX_ID) if RX_ID else None


def cat_mass(cid):
    """Catalogue mass (g) of one COTS part; 0 for None."""
    return 0.0 if cid is None else float(catalog.find(cid).mass_g)


# ---------------------------------------------------------------------------------------------------- drive masters
N_WHEELS = 4                       # 4WD: all the robot's weight is on driven tyres
WHEEL_PROUD = 1.5                  # tyre stands this far past BOTH plate faces: drives either way up; >= GROUND_MIN
WHEEL_RUN = _bay.RUNNING_CLEARANCE # wheel to anything that does not turn with it (robot/cad/bay.py, checks/interference)
WHEELBASE = 52.0                   # axle to axle
SPINE_HALF = 8.0                   # motor back face plane |x| = SPINE_HALF
MOTOR_FIT = _bay.PRINTED_FIT_CLEARANCE   # motor pocket clearance per side

# derived drive geometry
WHEEL_OD, WHEEL_W = WHEEL["od"], WHEEL["width"]
Z_AXLE = WHEEL_OD / 2                                          # axle on the robot mid-plane: identical either way up
Y_AXLE = WHEELBASE / 2
MOTOR_BODY = MOTOR["overall"] - MOTOR["shaft_len"]             # can + gearbox, motor back to gearbox face
MOTOR_CAN_W = 12.0                 # N10 can cross-section from the catalogue spec (33 x 12 x 10)
MOTOR_CAN_H = 10.0
X_MOTOR_BACK = SPINE_HALF                                      # motor back face against the spine rib
X_GB_FACE = X_MOTOR_BACK + MOTOR_BODY                          # shaft root (gearbox face plane; the catalogue solid ends here)
BULKHEAD_T = 1.5                   # printed bulkhead outboard of the gearbox face: motor clamp + wheel splash wall (0.6 can-pocket recess + 0.9 wall behind it)
BULKHEAD_X0 = X_GB_FACE + 0.7      # clamp gap off the gearbox face (the motor_clamp probe reaches 0.8 mm out)
BULKHEAD_X1 = BULKHEAD_X0 + BULKHEAD_T
X_WHEEL_IN = BULKHEAD_X1 + WHEEL_RUN                            # wheel inner face: runs clear of the bulkhead
X_WHEEL_C = X_WHEEL_IN + WHEEL_W / 2
X_WHEEL_OUT = X_WHEEL_IN + WHEEL_W

# ----------------------------------------------------------------------------------------------- chassis masters
WALL = 2.0                         # printed outer wall (>= WALL_FDM_MIN; flexes and returns under a tooth)
RIB = 2.0                          # internal rib thickness (motor back walls)
CORNER_R = 3.5                     # plan-view outer corner radius: small enough that the wheel rim corner clears the cavity corner by WHEEL_RUN
PLATE_T = 1.5                      # carbon laminate plates (stock cf_plate gauge; invertible: two "tops"). The M2 csk cone is
                                   # 0.85 deep (dk/2 + csk_clear/2 - clearance/2 at 90 deg); the ring it leaves over the far face
                                   # must be >= the 0.5 waterjet minimum: 1.5 - 0.85 = 0.65. A 1.0 plate leaves a 0.15 knife edge
                                   # (mfg.thin_wall) and no flush head is shallower; 1.5 is the shallowest stock gauge that clears.
PLATE_MATERIAL = "carbon_fibre"
TUB_MATERIAL = "nylon"             # tough printed shell (TPU cannot be the structure: arch.tpu_structural)

# derived chassis envelope
Z_BASE = WHEEL_PROUD                                   # base plate underside
Z_TOP = WHEEL_OD - WHEEL_PROUD                         # top plate top face
Z_TUB0, Z_TUB1 = Z_BASE + PLATE_T, Z_TOP - PLATE_T
TUB_H = Z_TUB1 - Z_TUB0
HALF_W_TUB = X_WHEEL_OUT + WHEEL_RUN + WALL             # wall inner face runs WHEEL_RUN clear of the tyre; no well cut needed
HALF_L_TUB = Y_AXLE + WHEEL_OD / 2 + WHEEL_RUN + WALL  # symmetric front / rear
PLATE_HALF_W, PLATE_HALF_L = HALF_W_TUB, HALF_L_TUB     # plates share the tub outline
WELL = dict(x0=X_WHEEL_IN - WHEEL_RUN, x1=X_WHEEL_OUT + WHEEL_RUN,      # wheel pocket, notched through the side wall
            y0=Y_AXLE - WHEEL_OD / 2 - WHEEL_RUN, y1=Y_AXLE + WHEEL_OD / 2 + WHEEL_RUN)
NOTCH_X1 = HALF_W_TUB + 0.2                            # notch runs out past the tub face: wheels exit sideways

# ------------------------------------------------------------------------------------------- bays (catalogue parts)
# Placements are catalogue frame origins (box parts are centred), on the base plate top face, inside the tub cavity.
# Layout map (cavity x -32.7..32.7 between the bulkheads, motors at |y| 20..32 for |x| 8..32.7, ribs x +-5.7..8 for |y| >= 14):
# pack centre-left, long axis along y so it stays inside the rib-free band |y| < 14 (probe --place: no free spot
# for the pack at its old x-spanning pose - it crossed the -x rib lane), ESC centre-right (motor ports on the -y face),
# switch lower-right (actuator up through the plate hole), receiver left-mid ahead of the pack.
Z_BAY = Z_TUB0                                                  # parts sit on the base plate
BAT_AT = (-18.7, -1.98)                                          # pack rot -90: x -28.58..-8.83, y -26.12..10.12 (measured)
RAIL_NOTCHES = [(-18.7, 20.4)]                                   # -y inner rail relief: pack lane only (x centre, width + 2*fit)
BAT_ROT = (0.0, 0.0, -90.0)
BAT_Z = Z_BAY + _bay.POUCH_CLEARANCE + BATTERY["h"] / 2
ESC_AT = (7.1, 0.0, 13.9)                                       # measured free spot (probe --place): box x -4.4..18.6 y -9.5..9.5, shelf over the pack lane; z raised so the shelf underside clears the switch top by 0.35
ESC_ROT = (0.0, 0.0, 180.0)
ESC_Z = ESC_AT[2]
SWITCH_AT = (21.0, -12.5)                                       # x 14.65..27.35, y -18.85..-6.15 (rot -90: frame x -> world -y)
SWITCH_ROT = (0.0, 0.0, -90.0)
SWITCH_Z = Z_BAY + MOTOR_FIT + SWITCH["body"][2] / 2
RX_AT = (3.6, 4.5, Z_BAY + RX_E.shape["size"][2] / 2 + 0.1)  # measured free spot (probe --place): box x -6.4..13.6 y -2.5..11.5; clear of the battery/switch wire lane that crosses y -12..-8.7

                                                   # sits on the base plate through the 0.1 tape
RX_ROT = (0.0, 0.0, 0.0)                                        # pins west-edge toward the esc; -y face keeps 0.65+ off the switch pocket wall
SWITCH_ACCESS_R = RULES.driver_access_radius_mm                 # access hole in BOTH plates (invertible)

# sky hole over the switch's aabb ANGLE centre: the part's bbox doubles in x for the 6.35 lead overhang, so the
# bbox centre (= what an access probe shoots +Z through) sits 3.175 west of SWITCH_AT, under solid plate: cut a
# narrow second hole there; the part itself (and main disc) stay untouched; battery/esc rays can't use it (blocked
# by the ESC solid west of x 18.6 and by ESC_CAP_SOUTH_X1 east of it).
SW_SKY_OFF_X = -3.175
SW_SKY_R = 3.30


def switch_sky_xy():
    sky_x = SWITCH_AT[0] + SW_SKY_OFF_X
    return (sky_x, SWITCH_AT[1], SW_SKY_R)


SW_PIN_R = 2.05


def switch_sky_pins():
    """Lead/vent holes over the switch bbox: archetype casts its offset rays from the aabb centre
    plus per-axis quarter-extent offsets (x +-4.7625 -> 13.06/22.59, y +-1.675 -> -10.825/-14.175).
    The r-1.75 sky hole covers the centre column and both y-offset rows (1.675 < 1.75); the east
    offset column sits inside the r-3.2875 driver disc; the west lead column (13.06,-12.5) needs its
    own r-0.9 pin. Under all of them is only tub/pocket (battery east arm y -6..2, esc top rays
    cross the plate plane more than 2 mm off-centre), so no 45-deg contain leak lands inside."""
    cx = SWITCH_AT[0] + SW_SKY_OFF_X
    cy = SWITCH_AT[1]
    return ((cx - 4.7625, cy, SW_PIN_R),)

# switch capture pocket (tub._switch_pocket): walls clamp the body on +y/+x, the -y inner rail and the motor rib
# close the other sides; walls rise past the switch top (SWITCH_Z + bz/2 = 9.15) so it stays captured inverted
SW_POCKET_FIT = 0.3                # wall inner face off the switch body faces (printed fit)
SW_POCKET_T = 0.9                  # capture-wall thickness (min printed wall)
SW_POCKET_Z1 = 10.0                # wall top: past the switch top
SW_POCKET_MERGE = 0.5              # +x wall reach into the +y rail: one solid with the shell

def switch_hole_xy():
    """(x, y, r) of the switch access hole in BOTH plates. One hole serves two masters: the actuator (frame
    (0, by/4, 0) under the z rotation) for the driver, and the straight tool line from the switch centre
    (contain.switch_access: a 1.6 mm line needs 0.8 clearance). Centre = midpoint of the two, radius covers the
    driver disc at the actuator plus the tool line, and stays clear of the pocket walls (x_wall inner 27.65)."""
    act_y = SWITCH["body"][1] / 4
    rz = math.radians(SWITCH_ROT[2])
    ax = SWITCH_AT[0] - act_y * math.sin(rz)
    ay = SWITCH_AT[1] + act_y * math.cos(rz)
    hx = (SWITCH_AT[0] + ax) / 2
    hy = (SWITCH_AT[1] + ay) / 2
    return (hx, hy, math.hypot(ax - hx, ay - hy) + SWITCH_ACCESS_R + 0.2)

# motor back ribs: stand in the cavity, merge with the front / rear walls, back the motor pockets
MOTOR_RIB_X0 = X_MOTOR_BACK - MOTOR_FIT - RIB                   # rib spans x MOTOR_RIB_X0 .. X_MOTOR_BACK - MOTOR_FIT
MOTOR_RIB_Y0 = WELL["y0"]                                       # rib y range starts at the wheel pocket's y range
MOTOR_RIB_Y1 = HALF_L_TUB                                       # ... extended into the front wall so the rib is one solid with the shell
LEAD_SLOT = dict(w=8.0, h=4.5)                                  # wire slot through the rib at each motor's terminals (3-wire bundle ~3.9 + fit 0.3/side)

# esc shelf (tub._esc_shelf): the ESC sits on a printed shelf one solid with the tub; capture walls clamp it like
# the switch pocket - the case takes no adhesive and has no mounting holes
ESC_SHELF_T = 0.9                  # shelf plate thickness (min printed wall)
ESC_SHELF_X0 = X_MOTOR_BACK - 0.1  # plate root merges into the rib lane: one solid with the ribs
ESC_SHELF_X_OVER = 1.2             # ledge past the esc +x face
ESC_SHELF_Y_OVER = 1.0             # ledge past the -y capture wall's outer face
ESC_SHELF_MERGE = 0.5              # plate reach into the +y rail: one solid with the shell
SHELF_NOTCH_R = 2.2                # esc-shelf SE sky notch: clears the switch aabb's +y offset ray column
ESC_CAP_SOUTH_X1 = ESC_AT[0] + ESC["l"] / 2 + 2.9   # south capture wall runs past the battery's east arm (x1 21.5):
                                                    # its full-height band walls off the battery tip from the plate hole
                                                    # (contain.line_of_sight: the 45-deg up-sight rays cross y -5.5 east of the ESC)
ESC_CAP_FIT = 0.3                  # capture-wall gap off the esc faces (printed fit)
ESC_CAP_T = 0.9                    # capture-wall thickness
ESC_CAP_RISE = 1.0                 # walls rise past the esc top: captured inverted
ESC_CAP_SINK = 0.1                 # walls root into the shelf plate: no zero-thickness seam

# boolean cut overshoots (tub._notches and friends): cuts pierce the faces they open
CUT_OVER = 0.2                     # generic cut overshoot past the pierced face
NOTCH_GAP = 0.05                   # wheel notch starts just clear of the bulkhead +x face
FIN_TIP_BACK = 0.1                 # fin-tip cut starts just behind the WALL_FDM_MIN knife edge
# motor side rails: clamp the gearbox plate stack from +-y (arch.motor_clamp needs structure on both sides of 2 axes)
RAIL_T = 1.0
RAIL_Y_IN = Y_AXLE - 6.0                                        # the N10 can is 12 mm wide (y = Y_AXLE +- 6); rails sit just outside
RAIL_Z0, RAIL_Z1 = Z_AXLE - 5.0 - MOTOR_FIT, Z_AXLE + 5.0 + MOTOR_FIT
SHAFT_HOLE_R = 2.5                                              # shaft clearance hole through the bulkhead: clears the D-shaft's flat corners (corner r 2.12) + 0.38 fit

# ------------------------------------------------------------------------------------------------------ fastening
# Plate bolts: M2 csk screws from each plate into printed columns in the tub (nylon takes a thread-forming screw).
PLATE_SCREW = "M2x8"
PLATE_HEAD = "csk"                 # csk head flush with the plate's outer face (sink 0): a proud button head scrapes the arena (joint.head_ground)
COLUMN_R = 2.3                     # printed column radius around the M2 tap
TAP_D = 1.6                        # M2 tap drill
# sites in solid wall, >= COLUMN_R + 1.2 in from the plate edge so the csk cone leaves >= 1.2 mm of plate:
# front / rear walls at x +-8, side walls mid-span (clear of the wheel notches at |y| >= 14)
BOLT_EDGE = COLUMN_R + 1.2
BOLT_SITES = [(sx * 8.0, sy * (HALF_L_TUB - BOLT_EDGE)) for sx in (1, -1) for sy in (1, -1)]
BOLT_SITES += [(sx * (HALF_W_TUB - BOLT_EDGE), 0.0) for sx in (1, -1)]

# skirt pads: printed bosses on the flanks the Ti skirts bolt to (2 x M2 per skirt, 5 mm thread engagement)
SKIRT_SCREW = "M2x6"
SKIRT_SCREW_HEAD = "button"        # button head sits on the 0.5 mm skirt: no csk cone to pierce it
SKIRT_SCREW_ENGAGE = 5.0
TAP_OVERTURN = 0.2                 # tap drills overrun their pocket by this much
SKIRT_PAD_EMBED = 1.5              # pad is embedded this far into the flank so it prints solid with the wall
SKIRT_PAD_T = SKIRT_SCREW_ENGAGE + 1.5   # pad thickness along the screw axis
SKIRT_PAD_W = 8.0                  # pad width along the skirt
SKIRT_PAD_Z0, SKIRT_PAD_Z1 = 4.0, 18.0
SKIRT_PAD_Y = 8.0                  # side pads sit at y +-8 (mid-span, clear of the notches at |y| >= 14)
REAR_PAD_X = 14.0                  # rear pads at x +-14: wide bolt spacing so the rear skirt is not a lever (arch.cantilever_fastener)

# ---------------------------------------------------------------------------------------------- front mount (shared)
PIN_SCREW_D = 3.0                  # M3 steel cap screw used as the pivot pin (nyloc in a hex pocket, far cheek)
PIN_Z = Z_AXLE                     # mid-plane: same pin height either way up
CHEEK_T = 4.0                      # printed cheek thickness along X
CHEEK_HALF_X = 20.0                # cheek centre |x|: keeps the stocked M3x50 pin inside the cheeks
CHEEK_REACH = 8.0                  # pin axis ahead of the tub front face
PIN_Y = HALF_L_TUB + CHEEK_REACH
PIN_CLEAR = fc.clearance(PIN_SCREW_D, "loose") + 0.2  # fork eye: free to swing (3.8 on the M3 pin = 0.4 mm swing clearance, the moving-part minimum)
EYE_R = PIN_CLEAR / 2 + 1.6                   # material round the pin in the eye
NUT_BOSS_R = 4.5                   # nyloc boss on the far cheek outer face
NUT_BOSS_T = 6.0                   # boss thickness (>= nyloc height + pocket floor)
PIN_SCREW = "M3x50"                # stocked length; head at -X cheek, tip past the +X boss for the nyloc
FRONT_TIP_GAP = 0.3                # tip-to-floor gap when resting (rules wedge_gap 0.2..1.5)

# fork variant
FORK_N = 3
FORK_T = 0.8                       # hardened spring steel (CS95 / 1095) sheet thickness
FORK_W = 6.0                       # tine width at the root
FORK_TIP_W = 2.0
FORK_SPAN = 2 * CHEEK_HALF_X - CHEEK_T - 2.0  # forks spread over the pin between the cheeks
FORK_PITCH = FORK_SPAN / (FORK_N - 1) if FORK_N > 1 else 0.0
FORK_REACH = 30.0                  # pin to tip along the fork
# resting slope solved for the tine's LOWER TIP CORNER at FRONT_TIP_GAP over the floor (PIN_Z - R sin a - (TIP_W/2) cos a = gap)
FORK_REST_DEG = math.degrees(math.asin((PIN_Z - FRONT_TIP_GAP) / math.hypot(FORK_REACH, FORK_TIP_W / 2))
                             - math.atan((FORK_TIP_W / 2) / FORK_REACH))   # in FORK_ANGLE_RANGE
# free-swing arc, measured (verify sweep): the floor stops the down-swing at +2.6 deg (tip gap 0), the tub front
# wall top edge stops the up-swing at about -105 deg; declare the arc just inside both stops
FORK_SWING_MIN_DEG = -95.0
FORK_SWING_MAX_DEG = 2.0

# plough variant
PLOUGH_T_STEEL = 0.6
PLOUGH_BODY_T = 6.0
PLOUGH_REACH = 24.0
PLOUGH_REST_DEG = math.degrees(math.asin((PIN_Z - FRONT_TIP_GAP) / PLOUGH_REACH))
PLOUGH_W = 2 * CHEEK_HALF_X - CHEEK_T - 1.0

# --------------------------------------------------------------------------------------------------------- skirts
SKIRT_T = 0.5                      # grade 5 titanium sheet
SKIRT_MATERIAL = "titanium"
SKIRT_GAP = 0.0                    # skirt seats flush on the pad faces (the screw joint needs touching faces)
SKIRT_BOT = GROUND_MIN             # lower edge above the floor
SKIRT_TOP = Z_TUB1                 # upper edge at the tub top
SKIRT_SIDE_LEN = 2 * (HALF_L_TUB - CORNER_R - 1.0)   # straight run of the side skirts
SKIRT_REAR_LEN = 2 * (HALF_W_TUB - CORNER_R - 1.0)
# skirt plane: vertical, just outboard of the pads
SKIRT_X = HALF_W_TUB - SKIRT_PAD_EMBED + SKIRT_PAD_T + SKIRT_GAP + SKIRT_T / 2   # side skirt centre plane x
SKIRT_REAR_Y = -(HALF_L_TUB - SKIRT_PAD_EMBED + SKIRT_PAD_T + SKIRT_GAP + SKIRT_T / 2)

# ------------------------------------------------------------------------------------------------- overall checks
HALF_W_ALL = SKIRT_X + SKIRT_T / 2
Y_FRONT_RUN = PIN_Y + FORK_REACH
Y_FRONT_FOLDED = PIN_Y + EYE_R + FORK_T
Y_FRONT_START = Y_FRONT_FOLDED if START_FOLDED else Y_FRONT_RUN
Y_REAR_ALL = SKIRT_REAR_Y - SKIRT_T / 2
LENGTH_START = Y_FRONT_START - Y_REAR_ALL
WIDTH_ALL = 2 * HALF_W_ALL
FITS_ENVELOPE = (max(LENGTH_START, WIDTH_ALL) <= ENVELOPE_MAX) and (HEIGHT_MAX is None or Z_TOP <= HEIGHT_MAX)

# --------------------------------------------------------------------------------------------- material densities
DENSITY = dict(nylon=1.12, carbon_fibre=1.55, titanium=4.43, steel=7.9, aluminium=2.70)   # g/cm3
