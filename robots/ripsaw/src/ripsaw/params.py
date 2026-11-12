"""Ripsaw masters and derived relations. UNTESTED: never built, run, rendered or verified.

Frame (same as Revron): X right, Y forward (weapon end), Z up, floor at Z = 0. The disc sits on X = 0.

Rule: every number used by geometry lives here, either as a named master (with its source) or as a relation of
masters and catalogue dimensions. COTS sizes come from the catalogue (robot.catalog / robot.cots_alts) through the
reused Revron helpers hw.size() and weapon_motor.describe(); nothing is retyped from a datasheet.
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
# body / rail lengths per size rule (the disc is mass-limited at 60 mm and fits both); asserted against ENVELOPE below
_SIZING = {"aws2025": dict(TUB_BODY_L=62.0, RAIL_L=24.0, WHEEL_REAR_BIAS=14.0),
           "aws_v43_cube": dict(TUB_BODY_L=52.0, RAIL_L=18.0, WHEEL_REAR_BIAS=12.0)}[RULES_SIZE]

# ------------------------------------------------------------------------------------------------ COTS settings
WEAPON_MOTOR = "repeat_2004_2800kv"         # Repeat DirectDrive 2004: 3 mm through shaft, 3x M3 on 15 both faces
# Battery: the brief asked for gnb_3s_300_80c_hv. The mass budget (BRIEF.md) puts the 3S build ~13 g over 150 g,
# and 3S also rules out the Malenki-Nano (max 2 cells). Default is therefore the 2S XT30 GNB pack; the alternatives
# are kept as settings. tattu_2s_300_75c_hv is lighter but ships on JST-PH (2 A class plug), wrong for a 20 A weapon.
BATTERY = "gnb_2s_350_70c_hv"
BATTERY_ALTS = ("gnb_3s_300_80c_hv", "tattu_2s_300_75c_hv")
WEAPON_ESC = "bbb_brushless_esc_20a"        # 20 A, no BEC, 2-4S
DRIVE_ESC = "bbb_malenki_nano"              # Rx + 3x 1 A brushed ESC, 1-2S: valid only with a 2S pack
DRIVE_ESC_3S = "bbb_dual_esc_v31"           # use with a 3S pack (2-4S, 5 V BEC) plus a separate receiver
SWITCH = "fingertech_mini_switch"
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "durahubs_30"

WM = weapon_motor.describe(WEAPON_MOTOR)    # back_x, cap_x, bell_r, base_holes, top_holes, shaft_r (catalogue frame, +X = bell)
WM_ENTRY = C.find(WEAPON_MOTOR)
WM_SHAFT_OUT = float(WM_ENTRY.shaft["len"])  # shaft protrusion past the bell face (catalogue: overall - body - rear stub)
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
DISC_OD = 60.0            # brief: ~60 mm; energy scales ~R^4 (BRIEF.md)
DISC_T = 3.0              # hardox stock list in robot/catalog.py STOCK_THICKNESS["hardox"] (3.0 smallest)
DISC_MAT = "hardox"
FLOOR_GAP = 1.5           # disc rim to floor, upright: lower than an opponent wedge lip, above arena plate seams (R114)
TOOTH_STEP = 8.0          # radial tooth height; >= bite at own top speed (BRIEF.md, 7.0 mm), so the tooth face takes the bite
RAMP_DEG = 90.0           # angle over which the rim spirals down into the notch in front of the tooth
RIM = 7.0                 # solid rim radial width: the tooth root and the rim carry the impact, windows stay inside it
HUB_LAND = 3.5            # steel left round the bolt circle before the windows start
WIN_N = 3                 # lightening windows, symmetric set
WIN_HALF_DEG = 28.0       # half angle of each window
WIN_ROUND = 1.5           # window corner radius (laser kerf and crack start)
SPOKE_MIN_DEG = 8.0       # narrowest spoke allowed after the balance enlargement

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

# ------------------------------------------------------------------------------------------------ weapon mount (rails)
DISC_RAIL_CLR = 1.5       # disc side to right rail face (> MOVING_CLR, plus disc wobble on a 3 mm shaft)
RAIL_T = 4.0              # printed rail plate thickness: carries the stator screws / bearing; ~4 perimeters of 0.45 nozzle
BOSS_WALL = 1.5           # printed wall round the bearing
RAIL_L = _SIZING["RAIL_L"]          # rail prong length ahead of the tub body front (per size rule)
RAIL_NOSE = 1.5           # rail material ahead of the bearing boss
WM_X_CAP = -DISC_T / 2                    # bell face against the disc's left face
WM_X_BACK = WM_X_CAP - WM_BODY_L          # stator base back face = left rail inner face
RAIL_L_X = (WM_X_BACK - RAIL_T, WM_X_BACK)
SHAFT_END_X = WM_X_CAP + WM_SHAFT_OUT
BEAR_BORE, BEAR_OD, BEAR_W = BEARING[0], BEARING[1], BEARING[2]
RAIL_R_X = (DISC_T / 2 + DISC_RAIL_CLR, max(SHAFT_END_X, DISC_T / 2 + DISC_RAIL_CLR + RAIL_T) + BOSS_WALL)
BEAR_X = (SHAFT_END_X - BEAR_W, SHAFT_END_X)   # bearing seated flush with the shaft end, blind from outside (cap BOSS_WALL)
BOSS_R = BEAR_OD / 2 + BOSS_WALL
RAIL_TOP = Z_AX + WM["bell_r"] + BOSS_WALL      # rails rise to cover the bell from a top-down hit

# ------------------------------------------------------------------------------------------------ tub / chassis masters
TUB_BODY_L = _SIZING["TUB_BODY_L"]  # body behind the rails (per size rule); battery lies across it
TUB_W = 80.0              # outer width; wheels inside it behind side armour
TUB_FLOOR_Z = 3.0         # tub underside above the floor (wheels carry the robot)
TUB_H = 24.0              # body height: below the wheel OD so the wheels stand proud both ways up
WALL = 1.6                # side / rear wall: TPU-reinforced nylon, > MIN_WALL
CORNER_R = 6.0            # plan-view corner radius: glancing blows slide off
WHEEL_REAR_BIAS = _SIZING["WHEEL_REAR_BIAS"]    # wheel axle ahead of the rear wall (rear-biased: the disc and rails are the front mass)
WHEEL_GAP = 1.0           # tyre to wheel-well wall
PANEL_T_BASE = 1.0        # printed base panel
PANEL_T_TOP = 1.0         # printed top panel (nylon); Ti would cost ~6 g more (BRIEF.md)
PANEL_SCREW = 2.0         # M2 panel screws into heat-set inserts (as Revron)
PANEL_SCREW_N_SIDE = 3    # per long side, GridLocations
PANEL_SCREW_INSET = 4.0   # screw axis from the outer wall

# relations
TUB_TOP_Z = TUB_FLOOR_Z + TUB_H
TUB_Y0 = -TUB_BODY_L / 2
TUB_Y1 = TUB_BODY_L / 2
Y_AX = TUB_Y1 + RAIL_L - RAIL_NOSE - BOSS_R     # weapon axle
DISC_FRONT_Y = Y_AX + DISC_R
WHEEL_R = WHEEL_OD / 2
WHEEL_Z = WHEEL_R                               # wheel stands on the floor
WHEEL_Y = TUB_Y0 + WHEEL_REAR_BIAS
WHEEL_X = TUB_W / 2 - WALL - WHEEL_GAP - WHEEL_W / 2   # inside the tub outline, behind the side wall
WHEEL_PROUD_TOP = WHEEL_Z + WHEEL_R - TUB_TOP_Z        # > 0: drives inverted on the wheels (rails still taller, see risks)
INSERT_D, INSERT_L = FC.insert(PANEL_SCREW)
OVERALL_L = DISC_FRONT_Y - TUB_Y0
OVERALL_H = max(RAIL_TOP, TUB_TOP_Z + PANEL_T_TOP, WHEEL_Z + WHEEL_R)
assert OVERALL_L <= ENVELOPE_L and TUB_W <= ENVELOPE_W and OVERALL_H <= ENVELOPE_H, f"outside the {RULES_SIZE} size limit"
assert WHEEL_PROUD_TOP > 0, "wheels must stand proud of the tub top for inverted driving"

# ------------------------------------------------------------------------------------------------ forks (reuse revron fork_5)
FORK_PIN = 3.0            # M3 hinge pin through the rail outer face; fork free to swing: self-levelling on its tip
FORK_TIP_GAP = 0.0        # fork tip rests ON the floor (gravity); the up-stop sits FORK_LIFT above
FORK_LIFT = 4.0           # up-travel before the fork lands on its stop
FORK_SIDE_CLR = 0.5       # fork sheet to rail outer face

# ------------------------------------------------------------------------------------------------ drive
DRIVE_V_NOM = 6.0         # BBB N10 rpm is quoted at 6 V (cots_alts src)
CELL_V_NOM_HV = 3.8       # LiHV nominal per cell
CELL_V_FULL_HV = 4.35     # LiHV full charge per cell
KV_LOAD = 0.8             # loaded / no-load speed factor (brief: ~0.8), estimate

# ------------------------------------------------------------------------------------------------ mass estimates (made parts)
DENS = {m: C.density(m) for m in ("hardox", "nylon", "titanium")}   # g/cm3 from robot/catalog.py materials
SOLID_FRAC = 0.85         # GUIDE default for printed parts
MASS_EST = {              # g, estimates, NOT measured; the verifier's volume x density replaces these
    "tub": 16.0, "panel_base": 5.0, "panel_top": 5.0, "forks": 4.0, "fasteners_inserts": 3.5, "wires_xt30": 4.0,
    "bearing": 0.3, "fork_pins": 0.6,
}
