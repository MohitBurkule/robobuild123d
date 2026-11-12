"""Scythe master parameters and derived relations. UNTESTED: never built, run, rendered or verified.

Frame: X right, Y forward (weapon end), Z up, floor at Z = 0 (same as Revron).
Every number used by geometry lives here, as a named master with its source, or as a relation of masters.
COTS dimensions/masses are read from the catalogue (robot.catalog) through cots(); the literal fallbacks next to
them are the research/cots/INDEX.md values, used only for the static mass/energy tables in BRIEF.md.
"""
import math

from robot.profile import Profile

PROFILE = Profile()                          # aws2025 (robot/profile.py)
CUBE = 101.6                                 # mm: AWS rules v4.3 2b, robot fully inside a 4 in cube in start config
FOOTPRINT = CUBE                             # robot/profile.py footprint_mm (150) is superseded by the cube rule
MASS_LIMIT = PROFILE.roller_mass_g           # 150 g (Scythe is a roller: wheels, no walking)
MIN_CLR_MOVING = PROFILE.min_clearance_moving_mm   # 0.4 mm moving-part rule floor
MIN_GROUND_CLR = PROFILE.min_ground_clearance_mm   # 1.0 mm
FOOTPRINT_MARGIN = 1.5                       # mm kept off each cube face (print tolerance + sizing-box wall)

# ---- COTS (catalogue ids; the robot/gen templates use the same ids) ----
WEAPON_MOTOR = "gr1507"                      # Revron's motor; fit features via revron weapon_motor.describe()
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "bbb_wheel_34x6_5"
BATTERY = "tattu_2s_300_75c_hv"
BATTERY_3S = "gnb_3s_300_80c_hv"             # variant (variants.py)
WEAPON_ESC = "bbb_brushless_esc_20a"
DRIVE_RX = "bbb_malenki_nano"                # alt: bbb_dual_esc_v31
SWITCH = "fingertech_mini_switch"
CONNECTOR = "xt30u_m"

# INDEX.md values (fallback only, for the static tables; geometry calls cots())
INDEX_MASS_G = {WEAPON_MOTOR: 19.6, DRIVE_MOTOR: 8.0, WHEEL: 4.1, BATTERY: 16.0, BATTERY_3S: 28.0,
                WEAPON_ESC: 5.0, DRIVE_RX: 2.3, SWITCH: 2.15, CONNECTOR: 1.5}
WHEEL_D = 34.0                               # INDEX.md bbb_wheel_34x6_5: 34 x 6.5 (+2 boss)
WHEEL_W = 6.5
GR1507_KV = 2850                             # INDEX.md gr1507 row (kV)
SHAFT_D = 5.0                                # INDEX.md gr1507: M5 shaft


def cots(cid):
    """Catalogue entry (mass_g, props, shaft) of a COTS id: the single source for COTS numbers."""
    from robot import catalog
    e = catalog.find(cid)
    if e is None:
        raise KeyError(f"`{cid}` not in robot.catalog")
    return e


# ---- weapon: hardened steel two-tooth bar, horizontal, under the tub ----
STEEL_DENSITY = 7.85e-3                      # g/mm^3, Hardox 500 / EN45 spring steel
BAR_T = 3.0                                  # mm sheet stock (laser cut, then hardened/Hardox as supplied)
BAR_DIAG_MARGIN = 8.0                        # mm off the cube floor diagonal (bar parked corner-to-corner at start)
BAR_L_GEOM_MAX = CUBE * math.sqrt(2) - BAR_DIAG_MARGIN   # 135.7 mm: largest bar parked on the cube floor diagonal
BAR_L_SQUARE = CUBE - 2 * FOOTPRINT_MARGIN   # 98.6 mm: above this the bar MUST be parked on the diagonal at start
BAR_L_TYRE_MAX = 90.0                        # mm: binding limit = own tyres outside the sweep inside the cube (check())
BAR_L = min(BAR_L_GEOM_MAX, BAR_L_TYRE_MAX)  # 90 < BAR_L_SQUARE: fits the cube in any clocking (diagonal parking not needed)
BAR_W_ROOT = 16.0                            # mm width at the hub (bending section: max moment there)
BAR_W_TIP = 10.0                             # mm width at the tooth
BAR_TOOTH_STEP = 4.0                         # mm radial depth of the bite step on each leading edge
BAR_TOOTH_LEN = 10.0                         # mm along the bar from the tip where the step starts
BAR_CORNER_R = 1.0                           # mm laser-cut corner round on non-cutting corners
BAR_Z0 = 2.0                                 # mm underside above floor (brief: ~2 mm, > MIN_GROUND_CLR)
BAR_BOLT = "M3"
BAR_BOLT_D = 3.0
BAR_BOLT_N = 2                               # 2x M3 through bar into hub, PolarLocations
BAR_BOLT_PCD = 11.0                          # mm
BAR_BORE_CLR = 0.1                           # mm radial on the shaft pilot (centres the bar on the shaft)

# ---- turned hub (7075-T6): bolts to bell top screws, carries the bar ----
HUB_OD = 17.0                                # mm (> BAR_BOLT_PCD + M3 head)
HUB_H = 5.0                                  # mm turned spacer between bell cap and bar
HUB_SPIGOT = 1.0                             # mm spigot into bell cap recess-free face (centring on shaft instead)
HUB_SHAFT_CLR = 0.02                         # mm radial: H7/g6-ish slide on the 5 mm shaft

# ---- weapon motor stack (shaft down, stator screwed up into the tub boss) ----
GAP_BAR_TUB = 1.5                            # mm air between bar top and tub floor underside (>> MIN_CLR_MOVING)
WPN_AXIS_Y = CUBE / 2 - FOOTPRINT_MARGIN - BAR_L / 2   # 4.3 mm: bar tip (clocked fore-aft) on the front margin
MOTOR_LEN = 15.5                             # mm INDEX.md gr1507 8.5 + 7 (geometry reads describe()['back_x'/'cap_x'])
MOTOR_BELL_CLR = 1.0                         # mm radial bell to tub bore wall (spinning)
BOSS_T = 3.0                                 # mm printed boss the stator screws bite into (heat-set M2)

# ---- tub (printed nylon PA12/PA-CF, FDM) ----
NYLON_DENSITY = 1.02e-3                      # g/mm^3 PA12
PRINT_SOLID_FRACTION = 0.6                   # walls + infill estimate
BAR_BITE_REACH = 8.0                         # mm of tooth exposed beyond the tub rim, all round
TUB_R = BAR_L / 2 - BAR_BITE_REACH           # 37 mm disc radius
TUB_WALL = 2.0                               # mm (> PROFILE.min_wall_fdm_mm)
TUB_FLOOR_T = 2.0                            # mm
TUB_SLOPE_DEG = 35.0                         # side slope from vertical: verticals glance off
TUB_TOP_Z = WHEEL_D - 2 * MIN_GROUND_CLR - 2.0   # body top below tyre top: invertible (wheels > body both sides)
WHEEL_BOSS = 1.0                             # mm wheel hub boss proud of the tyre (INDEX.md "+2 boss", per side estimate)
POD_W = 2 * (CUBE / 2 - FOOTPRINT_MARGIN - WHEEL_BOSS - WHEEL_W)   # 83.6 mm: wide track so the tyres clear the sweep
POD_L = 24.0                                 # mm rear pod length behind the axle line
TOP_PANEL_T = 1.0                            # mm 0.9-1 mm Ti/G10 top panel (Revron panel_top style)
BASE_PANEL_T = 1.0                           # mm printed base panel (Revron panel_base style), pod only
PANEL_SCREW = "M2"                           # Revron fastening: M2 CSK into heat-sets
PANEL_SCREW_N = 6

# ---- drive ----
BAR_TYRE_CLR = 3.0                           # mm plan clearance bar sweep -> nearest tyre point at bar-top height
WHEEL_CZ = WHEEL_D / 2                       # axle height
SKID_H = 1.0                                 # mm skid nub height below tub floor -> sets body ride height
SKID_D = 6.0                                 # mm UHMW/POM button skid
SKID_N = 2                                   # one fore under the weapon boss, one each side mirrored? -> 2 total (front pair)


# ---- derived relations ----
def bar_sweep_r():
    return BAR_L / 2


def bar_top_z():
    return BAR_Z0 + BAR_T


def tub_floor_z():
    """Tub floor underside: a fixed air gap above the bar."""
    return bar_top_z() + GAP_BAR_TUB


def tyre_half_chord(z):
    """Half length (Y) of the tyre's plan footprint at height z: where the bar plane cuts the tyre."""
    r = WHEEL_D / 2
    return math.sqrt(max(0.0, r * r - (r - z) ** 2))


def wheel_x():
    """Wheel centre X (right side; left is mirrored): tyre inner face on the pod side."""
    return POD_W / 2 + WHEEL_W / 2


def wheel_y():
    """Wheel centre Y: the nearest point of the tyre footprint at bar-top height sits BAR_TYRE_CLR outside the sweep."""
    need = bar_sweep_r() + BAR_TYRE_CLR
    x_in = wheel_x() - WHEEL_W / 2
    dy = math.sqrt(max(0.0, need * need - x_in * x_in)) + tyre_half_chord(bar_top_z())
    return WPN_AXIS_Y - dy


def overall_extent():
    """(x_half, y_front, y_rear) with the bar clocked worst-case (across X and along Y)."""
    x_half = max(bar_sweep_r(), wheel_x() + WHEEL_W / 2 + WHEEL_BOSS)
    return x_half, WPN_AXIS_Y + bar_sweep_r(), wheel_y() - WHEEL_D / 2


def bar_mass_g():
    """Plan area of the tapered bar (trapezoid each arm) x thickness x density, minus bore and bolt holes."""
    arm = (BAR_W_ROOT + BAR_W_TIP) / 2 * (BAR_L / 2)
    holes = math.pi * ((SHAFT_D / 2) ** 2 + BAR_BOLT_N * (BAR_BOLT_D / 2) ** 2)
    step = 2 * 0.5 * BAR_TOOTH_STEP * BAR_TOOTH_LEN
    return (2 * arm - holes - step) * BAR_T * STEEL_DENSITY


def bar_moi_kgm2():
    """Estimate: thin bar 1/12 m L^2 (taper ignored, slight overestimate)."""
    return bar_mass_g() / 1000 / 12 * (BAR_L / 1000) ** 2


def bar_rpm(volts, kv=GR1507_KV, eff=0.8):
    """Estimate: no-load kV x V x 0.8 (loaded / ESC / sag)."""
    return kv * volts * eff


def tip_speed_ms(rpm):
    return rpm * 2 * math.pi / 60 * bar_sweep_r() / 1000


def energy_j(rpm):
    w = rpm * 2 * math.pi / 60
    return 0.5 * bar_moi_kgm2() * w * w


def bite_mm(rpm, closing_ms=2.0, teeth=2):
    """Bite = closing speed / (teeth x rev/s)."""
    return closing_ms * 1000 / (teeth * rpm / 60)


def check():
    """Rule checks as asserts (call from build; nothing runs at import)."""
    x_half, yf, yr = overall_extent()
    half_room = FOOTPRINT / 2 - FOOTPRINT_MARGIN
    assert x_half <= half_room, f"width {2 * x_half:.1f} > {2 * half_room:.1f}"
    assert yf - yr <= FOOTPRINT - 2 * FOOTPRINT_MARGIN, f"length {yf - yr:.1f} over the square"
    assert BAR_L <= BAR_L_GEOM_MAX
    assert BAR_L <= BAR_L_SQUARE, "bar longer than the cube side: park it on the diagonal at start"
    assert TUB_TOP_Z + SKID_H + MIN_GROUND_CLR <= CUBE
    assert BAR_Z0 >= MIN_GROUND_CLR
    assert TUB_TOP_Z + MIN_GROUND_CLR <= WHEEL_D, "body taller than wheels: not invertible"
    assert tip_speed_ms(bar_rpm(8.4)) / 0.44704 <= PROFILE.max_tip_speed_mph
    return True
