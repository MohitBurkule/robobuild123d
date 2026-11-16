"""Ripsaw masters and derived relations.

Frame (same as Revron): X right, Y forward (weapon end), Z up, floor at Z = 0. The disc sits on X = 0.

Rule: every number used by geometry lives here, either as a named master (with its source) or as a relation of
masters and catalogue dimensions. COTS sizes come from the catalogue (robot.catalog / robot.cots_alts) through the
reused Revron helpers hw.size() and weapon_motor.describe(); nothing is retyped from a datasheet.

Weapon topology (serviceable): the stator bolts to a printed mount plate (left), the outboard MR63 rides in a printed
post plate (right); both plates bolt to the front wall's integral pads and lift off, and the weapon (disc + bell +
shaft) then slides forward out of the tub. The forks hang on M3 pins through the plates' outer faces.
"""
import math

from robot import catalog as C
from robot.profile import Profile
from robot.cad import fastener_catalog as FC

from ._reuse import hw, weapon_motor

# ------------------------------------------------------------------------------------------------ rules (AWS 2025)
RULES = Profile()                           # robot/profile.py `aws2025`
MASS_LIMIT_G = RULES.roller_mass_g          # 150 g
FOOTPRINT_MM = RULES.footprint_mm           # 150 mm square floor space, no overhang at any height
TIP_LIMIT_MPH = RULES.max_tip_speed_mph     # 600 mph
MOVING_CLR = RULES.min_clearance_moving_mm  # 0.4 mm: rotating to fixed clearance floor
MIN_WALL = RULES.min_wall_fdm_mm            # 0.9 mm printed wall floor
ALLOWANCE_G = RULES.allowance_g             # glue, tape, solder
# Size limit: ONE setting. Default "aws2025" = robot/profile.py footprint (150 mm floor square, no overhang at any
# height, no height limit). Optional "aws_v43_cube" = AWS rules v4.3 2b, 4 inch (101.6 mm) cube in start configuration.
RULES_SIZE = "aws2025"
CUBE_MM = 101.6
ENVELOPE_MARGIN = 2.0     # print shrink / tolerance stack / fork sag kept free inside the limit, each extent
_LIMITS = {"aws2025": (FOOTPRINT_MM, FOOTPRINT_MM, float("inf")), "aws_v43_cube": (CUBE_MM, CUBE_MM, CUBE_MM)}
ENVELOPE_L, ENVELOPE_W, ENVELOPE_H = (v - ENVELOPE_MARGIN for v in _LIMITS[RULES_SIZE])
# body length per size rule; the disc is mass-limited and fits both; asserted against ENVELOPE below
_SIZING = {"aws2025": dict(TUB_BODY_L=72.0, RAIL_L=24.0),
           "aws_v43_cube": dict(TUB_BODY_L=52.0, RAIL_L=18.0)}[RULES_SIZE]

# ------------------------------------------------------------------------------------------------ COTS settings
WEAPON_MOTOR = "repeat_2004_2800kv"         # Repeat DirectDrive 2004: 3 mm through shaft, 3x M3 on 15 both faces
# Battery: the 450 mAh 2S pack. The 350 mAh class browns out at the 2004's 17 A peak (51 mOhm -> 6.5 V under 3.3 V/cell)
# and runs ~169 s against a 180 s fight; the 450 mAh 80C pack (28 g, UK stock) holds the fight and its 40 mOhm keeps
# the bus above 3.3 V/cell at peak (BRIEF.md mass budget re-balanced: disc 60 -> 50 mm pays for the pack).
BATTERY = "c_gnb_gaoneng_2s_450mah_80c_lipo_xt30"
WEAPON_ESC = "bbb_brushless_esc_20a"        # 20 A, no BEC, 2-4S
DRIVE_ESC = "bbb_malenki_nano"              # Rx + 3x 1 A brushed ESC, 1-2S: valid only with a 2S pack
SWITCH = "fingertech_mini_switch"
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "durahubs_30"

WM = weapon_motor.describe(WEAPON_MOTOR)    # back_x, cap_x, bell_r, base_holes, top_holes, shaft_r (catalogue frame, +X = bell)
WM_ENTRY = C.find(WEAPON_MOTOR)
WM_SHAFT_OUT = float(WM_ENTRY.shaft["len"])  # shaft protrusion past the bell face
WM_SHAFT_D = 2 * WM["shaft_r"]
WM_BODY_L = WM["cap_x"] - WM["back_x"]
BEARING = weapon_motor.pick_bearing(WM_SHAFT_D)   # outboard bearing for the 3 mm shaft (catalog BEARINGS); see risks


def _sorted_size(cid):
    """(long, mid, short) bounding-box sizes of a catalogue part (orientation-free)."""
    return tuple(sorted(hw.size(cid), reverse=True))


BAT_L, BAT_W, BAT_H = _sorted_size(BATTERY)
WESC_L, WESC_W, WESC_H = _sorted_size(WEAPON_ESC)
DESC_L, DESC_W, DESC_H = _sorted_size(DRIVE_ESC)
DM_L, DM_W, DM_H = _sorted_size(DRIVE_MOTOR)
WHEEL_OD, _, WHEEL_W = _sorted_size(WHEEL)
SW_L, SW_W, SW_H = _sorted_size(SWITCH)
DM_SHAFT = C.find(DRIVE_MOTOR).shaft        # {"at", "dir", "len", "dia"} in the gearmotor's own frame

# ------------------------------------------------------------------------------------------------ weapon (disc) masters
DISC_OD = 46.0            # mass budget: 60 mm hardox is ~40 g and pushes the build over 150 g; 46 mm keeps ~27 g
DISC_T = 3.0              # hardox stock list in robot/catalog.py STOCK_THICKNESS["hardox"] (3.0 smallest)
DISC_MAT = "hardox"
FLOOR_GAP = 1.5           # disc rim to floor, upright: lower than an opponent wedge lip, above arena plate seams (R114)
TOOTH_STEP = 6.0          # radial tooth height; >= bite at own top speed (BRIEF.md) so the tooth face takes the bite
RAMP_DEG = 60.0           # angle over which the rim spirals down into the notch in front of the tooth
RIM = 6.0                 # solid rim radial width: the tooth root and the rim carry the impact, windows stay inside it
HUB_LAND = 4.3            # steel left round the bolt circle before the windows start (web >= 0.75 x stock, mfg web)
WIN_N = 3                 # lightening windows, symmetric set
WIN_HALF_DEG = 22.0       # half angle of each window
WIN_ROUND = 1.5           # window corner radius (laser kerf and crack start)
SPOKE_MIN_DEG = 4.0       # narrowest spoke allowed after the balance enlargement
TOOTH_ROOT_R = 0.6        # fillet at the tooth root (laser kerf floor; mfg sharp internal corner)

# relations
DISC_R = DISC_OD / 2
Z_AX = DISC_R + FLOOR_GAP                         # weapon axle height: disc reaches the floor upright
WIN_R_OUT = DISC_R - RIM                          # windows end RIM inside the rim (the notch is local, the rim is not)
WIN_R_IN = max(r for r, _, _ in WM["top_holes"]) + HUB_LAND
DISC_BORE = WM_SHAFT_D + 2 * MOVING_CLR           # disc clears the shaft; torque goes through the 3 bell screws


def _notch_moment():
    """First moment (mm^3 per mm thickness) of the notch material removed in front of the tooth, about the spin axis,
    and the bearing (deg, tooth face at 0) of its centroid. Linear spiral r(t) = R - STEP * t / RAMP; numeric integral."""
    n, R, mx, my, area = 180, DISC_R, 0.0, 0.0, 0.0
    for i in range(n):
        t = (i + 0.5) / n
        a = math.radians(-RAMP_DEG * (1 - t))          # the ramp ends at the tooth face (0 deg), coming from -RAMP
        r = R - TOOTH_STEP * t
        dA = (R * R - r * r) / 2 * math.radians(RAMP_DEG) / n
        rc = (2 / 3) * (R ** 3 - r ** 3) / (R * R - r * r)
        area += dA
        mx += dA * rc * math.cos(a)
        my += dA * rc * math.sin(a)
    return area, math.hypot(mx, my), math.degrees(math.atan2(my, mx))


NOTCH_AREA, NOTCH_MOMENT, NOTCH_BEARING = _notch_moment()
BAL_BEARING = NOTCH_BEARING + 180.0               # the balance window sits opposite the notch centroid
_WIN_RC = (2 / 3) * (WIN_R_OUT ** 3 - WIN_R_IN ** 3) / (WIN_R_OUT ** 2 - WIN_R_IN ** 2)
# extra half angle d on the opposite window, both sides: removed moment ~ 2 * (r_o^2 - r_i^2)/2 * d * rc * cos(half + d/2)
_k = (WIN_R_OUT ** 2 - WIN_R_IN ** 2) * _WIN_RC


def _bal_extra():
    d = 0.0
    for _ in range(50):                               # fixed-point on d (rad); converges in a few steps for these sizes
        d = NOTCH_MOMENT / (_k * max(math.cos(math.radians(WIN_HALF_DEG) + d / 2), 0.2))
    return math.degrees(d)


BAL_EXTRA_DEG = _bal_extra()
assert 360.0 / WIN_N - 2 * WIN_HALF_DEG - BAL_EXTRA_DEG >= SPOKE_MIN_DEG, "balance window eats the spokes: raise TOOTH_STEP/RAMP trade-off"

# lock pin: through both plates and the balance window of the disc at rest (weapon_lock, remove-before-fight)
LOCK_R = 0.5 * (WIN_R_IN + WIN_R_OUT)                # radius of the pin from the spin axis: mid-window
LOCK_ANGLE = BAL_BEARING - 25.0                       # part-frame angle inside window 0, on the plates (the disc default pose aligns it)

# ------------------------------------------------------------------------------------------------ weapon mount (plates)
PLATE_T = 3.0             # printed plate thickness: carries the stator screws / bearing seat
RAIL_L = _SIZING["RAIL_L"]          # plate prong length ahead of the tub body front (per size rule)
RAIL_NOSE = 1.5           # plate material ahead of the motor face
BOSS_WALL = 1.5           # printed wall round the bearing seat
DISC_RAIL_CLR = 1.5       # disc side to plate face (> MOVING_CLR, plus disc wobble on a 3 mm shaft)
PLATE_HEEL_L = 5.0        # plate root depth: bears on the front wall face, carries the mounting screws
PIN_PAD_R = 3.2           # printed pad round the fork hinge pin: keeps the hole clear of the plate's bottom edge

WM_X_CAP = -DISC_T / 2                    # bell face against the disc's left face
WM_X_BACK = WM_X_CAP - WM_BODY_L          # stator base back face = mount plate inner face
SHAFT_END_X = WM_X_CAP + WM_SHAFT_OUT
BEAR_BORE, BEAR_OD, BEAR_W = C.BEARINGS[BEARING]   # pick_bearing returns the catalog name; dimensions come from the table
RAIL_L_X = (WM_X_BACK - PLATE_T, WM_X_BACK)                   # left (stator) plate
RAIL_R_X = (SHAFT_END_X - PLATE_T, SHAFT_END_X)              # right (bearing) plate: bearing flush with the shaft end
BEAR_X = (SHAFT_END_X - BEAR_W, SHAFT_END_X)   # bearing seated flush with the plate's outer face
BOSS_R = BEAR_OD / 2 + BOSS_WALL
RAIL_TOP = Z_AX + WM["bell_r"] + BOSS_WALL      # plates rise to cover the bell from a top-down hit

# ------------------------------------------------------------------------------------------------ tub / chassis masters
TUB_BODY_L = _SIZING["TUB_BODY_L"]  # body behind the plates (per size rule); battery lies across its rear shelf
TUB_W = 80.0              # outer width; wheels inside it behind side armour
TUB_FLOOR_Z = 3.0         # tub underside above the floor (wheels carry the robot)
TUB_H = 24.0              # body height: below the wheel OD so the wheels stand proud both ways up
WALL = 1.6                # side / rear wall: TPU-reinforced nylon, > MIN_WALL
CORNER_R = 6.0            # plan-view corner radius: glancing blows slide off
WHEEL_REAR_BIAS = 27.0     # wheel axle ahead of the rear wall: well cut clears the rear wall, bay holds the 61 mm pack
WHEEL_GAP = 1.0           # tyre to wheel-well wall
PANEL_T_BASE = 1.0        # printed base panel
PANEL_T_TOP = 1.0         # printed top panel (nylon); Ti would cost ~6 g more (BRIEF.md)
PANEL_SCREW = 2.0         # M2 panel screws into heat-set inserts (as Revron)
PANEL_SCREW_Y = 27.0      # screw axes from the tub centreline (clear of the wheel wells)
PANEL_BOSS_T = 5.0        # side-wall boss thickness behind the inner face (insert dia 3.2 + wall)
SHELF_T = 2.4             # rear shelf: battery seat + motor-cradle root (> MIN_WALL)
SHELF_Y1 = 2.0            # shelf front edge (y): under both motor cradle walls
CRADLE_WALL_T = 1.0       # motor cradle side wall thickness (> MIN_WALL)
CRADLE_Y0, CRADLE_Y1 = -12.5, 1.5       # cradle walls: outside the N10 bbox (y -12..0) by 0.5 each side
CRADLE_TOP_Z = 23.0       # top of the cradle walls
MOTOR_BRIDGE_Z0 = 21.2    # bridge underside: 0.2 capture gap over the N10 top at 20 (support.loose limit)
MOTOR_STOP_T = 0.5        # axial stop wall thickness at the gearbox face
PAD_T = 5.0               # front-wall pad thickness (heat-set insert length 4.0 + wall behind)
PLATE_SCREW_Z = (8.0, 15.0, 22.0)        # plate mounting screw heights (through the heel into the wall pads)

# relations
TUB_TOP_Z = TUB_FLOOR_Z + TUB_H
TUB_Y0 = -TUB_BODY_L / 2
TUB_Y1 = TUB_BODY_L / 2
PLATE_Y0 = TUB_Y1                     # plates bear on the front wall outer face
Y_AX = TUB_Y1 + RAIL_L - RAIL_NOSE - BOSS_R     # weapon axle
PLATE_NOSE_Y = Y_AX + WM["bell_r"] + RAIL_NOSE  # plate nose covers the bell's front face from a hit
DISC_FRONT_Y = Y_AX + DISC_R
WHEEL_R = WHEEL_OD / 2
WHEEL_Z = WHEEL_R                               # wheel stands on the floor
WHEEL_Y = TUB_Y0 + WHEEL_REAR_BIAS
WHEEL_X = TUB_W / 2 - WALL - WHEEL_GAP - WHEEL_W / 2   # inside the tub outline, behind the side wall
WHEEL_PROUD_TOP = WHEEL_Z + WHEEL_R - TUB_TOP_Z        # > 0: drives inverted on the wheels (plates still taller, see risks)
INSERT_D, INSERT_L = FC.insert(PANEL_SCREW)
PLATE_SCREW_CLR = FC.clearance(PANEL_SCREW)            # M2 clearance through the plate heel / front wall
STATOR_SCREW_CLR = FC.clearance(3.0)                   # M3 clearance through the mount plate
OVERALL_L = DISC_FRONT_Y - TUB_Y0
OVERALL_H = max(RAIL_TOP, TUB_TOP_Z + PANEL_T_TOP, WHEEL_Z + WHEEL_R)
assert OVERALL_L <= ENVELOPE_L and TUB_W <= ENVELOPE_W and OVERALL_H <= ENVELOPE_H, f"outside the {RULES_SIZE} size limit"
assert WHEEL_PROUD_TOP > 0, "wheels must stand proud of the tub top for inverted driving"
assert WHEEL_Y - WHEEL_OD / 2 - WHEEL_GAP > TUB_Y0 + WALL, "wheel well cut must clear the rear wall"

# battery bay (world): pack lies flat on the shelf, XT30 forward toward the switch run
BAT_AT = (-7.0, -24.0, TUB_FLOOR_Z + SHELF_T + BAT_H / 2)
assert BAT_AT[0] - BAT_L / 2 > -(TUB_W / 2 - WALL), "battery must clear the left wall"
assert BAT_AT[0] + BAT_L / 2 < WHEEL_X - WHEEL_W / 2 - 0.5, "battery must clear the wheels"
assert BAT_AT[1] - BAT_W / 2 > TUB_Y0 + WALL, "battery must clear the rear wall"
assert BAT_AT[1] + BAT_W / 2 <= WHEEL_Y - DM_W / 2 - 0.5, "battery must clear the drive motors"

# electronics bays (world): ESCs high on the walls / shelf, switch under the top-panel keyway
WESC_AT = (-26.4, 8.0, TUB_TOP_Z - WESC_H)
DESC_AT = (0.0, -24.0, TUB_TOP_Z - PANEL_T_TOP - DESC_H)
SW_AT = (25.7, 16.0, 20.65)

# ------------------------------------------------------------------------------------------------ forks (reuse revron fork_5)
FORK_PIN = 3.0            # M3 hinge pin through the plate outer face; fork free to swing: self-levelling on its tip
FORK_TIP_GAP = 0.0        # fork tip rests ON the floor (gravity); the up-stop sits FORK_LIFT above
FORK_LIFT = 4.0           # up-travel before the fork lands on its stop
FORK_SIDE_CLR = 0.5       # fork sheet to plate outer face

# ------------------------------------------------------------------------------------------------ drive
DRIVE_V_NOM = 6.0         # BBB N10 rpm is quoted at 6 V (cots_alts src)
CELL_V_NOM_HV = 3.8       # LiHV nominal per cell
CELL_V_FULL_HV = 4.35     # LiHV full charge per cell
KV_LOAD = 0.8             # loaded / no-load speed factor (brief: ~0.8), estimate

# ------------------------------------------------------------------------------------------------ mass estimates (made parts)
DENS = {m: C.density(m) for m in ("hardox", "nylon", "titanium")}   # g/cm3 from robot/catalog.py materials
SOLID_FRAC = 0.85         # GUIDE default for printed parts
MASS_EST = {              # g, estimates, NOT measured; the verifier's volume x density replaces these
    "tub": 22.0, "panel_base": 7.0, "panel_top": 5.0, "mount_l": 2.2, "post_r": 2.2, "forks": 4.0,
    "fasteners_inserts": 3.5, "wires_xt30": 4.0, "bearing": 0.3, "fork_pins": 0.6,
}
