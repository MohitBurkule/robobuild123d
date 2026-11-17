"""Scythe master parameters and derived relations. UNTESTED: never built, run, rendered or verified.

Frame: X right, Y forward (weapon end), Z up, floor at Z = 0 (same as Revron).
Every number used by geometry lives here, as a named master with its source, or as a relation of masters.
COTS dimensions/masses: geometry reads the catalogue (robot.catalog via cots() / revron hw + weapon_motor); the
INDEX.md literals below feed only the mass/energy relations that size the bar (no build needed to evaluate them).

Sizing chain (all relations, evaluated at import):
  envelope (rules)  ->  room = side/2 - margin
  mass budget       ->  bar_r_mass()   (largest bar the 150 g limit carries, MASS_MARGIN kept)
  tyres outside the sweep inside the envelope -> bar_r_geom()
  tip-speed rule    ->  bar_r_tip()
  BAR_L = 2 * min(...) rounded down to 1 mm; then POD_W (track), WPN_AXIS_Y, TUB_R follow from BAR_L.
"""
import math
import os

from robot.profile import Profile

PROFILE = Profile()                          # aws2025 (robot/profile.py)

# ---- size envelope: ONE setting. Default = robot/profile.py (AWS 2025: 150 mm floor square, no overhang at any
# height, no height limit). Optional variant "aws_v43_cube": 101.6 mm (4 in) cube in start config (AWS v4.3 2b).
# Select with use_rules("aws_v43_cube") (reloads this module) or env SCYTHE_CLASSIC_RULES before import.
CUBE_V43 = 101.6                             # mm, AWS rules v4.3 2b (old rule, optional variant only)
ENVELOPES = {
    "aws2025": dict(side=PROFILE.footprint_mm, height=None, tub_g=19.0, top_panel_g=8.0),       # tub/panel g: estimates
    "aws_v43_cube": dict(side=CUBE_V43, height=CUBE_V43, tub_g=17.0, top_panel_g=6.5),
}
RULES = os.environ.get("SCYTHE_CLASSIC_RULES", "aws2025")
ENVELOPE = ENVELOPES[RULES]
FOOTPRINT = ENVELOPE["side"]                 # mm, square floor side (150 default)
HEIGHT_LIMIT = ENVELOPE["height"]            # mm or None (AWS 2025 has no height limit)


def use_rules(name):
    """Switch the envelope variant and re-derive every relation (other modules read params as P.<name> at call time)."""
    import importlib, sys
    if name not in ENVELOPES:
        raise KeyError(f"rules `{name}`; one of {sorted(ENVELOPES)}")
    os.environ["SCYTHE_CLASSIC_RULES"] = name
    return importlib.reload(sys.modules[__name__])


MASS_LIMIT = PROFILE.roller_mass_g           # 150 g (Scythe is a roller: wheels, no walking)
MIN_CLR_MOVING = PROFILE.min_clearance_moving_mm   # 0.4 mm moving-part rule floor
MIN_GROUND_CLR = PROFILE.min_ground_clearance_mm   # 1.0 mm
FOOTPRINT_MARGIN = 1.5                       # mm kept off each envelope face (print tolerance + sizing-box wall)
MASS_MARGIN = 6.0                            # g kept under MASS_LIMIT (scale error, repairs); sets the bar length
MPH_PER_MS = 2.23694                         # unit conversion

# ---- COTS (catalogue ids; the robot/gen templates use the same ids) ----
WEAPON_MOTOR = "gr1507"                      # Revron's motor; fit features via revron weapon_motor.describe()
WPN_CAP_X = 6.7                              # mm bell cap from the motor origin along the shaft (describe()['cap_x'])
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "bbb_wheel_34x6_5"
BATTERY_2S = "lipo_2s_350"                   # 36 x 17 x 11 mm, 21.5 g, 350 mAh: the 180 mAh pack fails the 3 min fight (power.runtime)
BATTERY = os.environ.get("SCYTHE_CLASSIC_BATTERY", BATTERY_2S)
BATTERY_3S = "gnb_3s_300_80c_hv"             # variant (variants.py)
WEAPON_ESC = "bbb_brushless_esc_20a"
DRIVE_RX = "bbb_malenki_nano"                # alt: bbb_dual_esc_v31
SWITCH = "fingertech_mini_switch"
SWITCH_XY = (4.2, 38.7)                    # mm: switch (+1.2 x) and its top-panel key hole: probe --place switch, free box x -0.9..18.1 y 32.4..45.1 at yaw 90
CONNECTOR = "xt30u_m"

# COTS masses (catalogue; was a stale INDEX.md copy: gr1507 19.6 g there, 8.5 g in the catalogue)
def _cat_mass(cid):
    """Catalogue mass (g) of a COTS id: robot.catalog is the single source, so the sizing chain cannot drift from it."""
    from robot import catalog
    return catalog.find(cid).mass_g


INDEX_MASS_G = {cid: _cat_mass(cid) for cid in (WEAPON_MOTOR, DRIVE_MOTOR, WHEEL, BATTERY_2S, BATTERY_3S,
                                                  WEAPON_ESC, DRIVE_RX, SWITCH, CONNECTOR)}
CELLS = {BATTERY_2S: 2, BATTERY_3S: 3}       # INDEX.md names (2S1P / 3S)
CELL_HV_V = 4.35                             # V per LiHV cell full (both packs are HV); PROFILE.max_cell_v = 4.2 is the
                                             # rule check value -> see BRIEF unsure list
WHEEL_D = 34.0                               # INDEX.md bbb_wheel_34x6_5: 34 x 6.5 (+2 boss)
WHEEL_W = 6.5
WHEEL_BOSS = 1.0                             # mm hub boss proud of the tyre per side (INDEX.md "+2 boss", estimate)
WHEEL_INNER_REACH = 5.25                     # mm wheel origin -> inboard face (catalogue bbb_wheel_34x6_5 bbox, hub boss side)
GR1507_KV = 2850                             # INDEX.md gr1507 row (kV)
SHAFT_D = 5.0                                # INDEX.md gr1507: M5 shaft

# Everything but the bar, g (COTS from INDEX.md, the rest estimates; BRIEF.md mass table mirrors this)
MASS_OTHER_G = {
    "weapon_motor": INDEX_MASS_G[WEAPON_MOTOR], "drive_motors": 2 * INDEX_MASS_G[DRIVE_MOTOR],
    "wheels": 2 * INDEX_MASS_G[WHEEL], "battery": INDEX_MASS_G[BATTERY], "weapon_esc": INDEX_MASS_G[WEAPON_ESC],
    "drive_rx": INDEX_MASS_G[DRIVE_RX], "switch": INDEX_MASS_G[SWITCH], "xt30": INDEX_MASS_G[CONNECTOR],
    "hub_7075": 3.0, "screws_inserts": 3.5, "wires": 4.0, "tub": ENVELOPE["tub_g"], "top_panel": ENVELOPE["top_panel_g"],
    "skids": 0.5, "allowance": PROFILE.allowance_g,
}


def cots(cid):
    """Catalogue entry (mass_g, props, shaft) of a COTS id: the single source for COTS numbers in geometry."""
    from robot import catalog
    e = catalog.find(cid)
    if e is None:
        raise KeyError(f"`{cid}` not in robot.catalog")
    return e


# ---- weapon: hardened steel two-tooth bar, horizontal, under the tub ----
STEEL_DENSITY = 7.85e-3                      # g/mm^3, Hardox 500 / EN45 spring steel
BAR_T = 3.0                                  # mm sheet stock (laser cut, Hardox as supplied)
BAR_W_ROOT = 16.0                            # mm width at the hub (bending section: max moment there)
BAR_W_TIP = 10.0                             # mm width at the tooth
BAR_TOOTH_STEP = 4.0                         # mm radial depth of the bite step on each leading edge
BAR_TOOTH_LEN = 10.0                         # mm along the bar from the tip where the step starts
BAR_CORNER_R = 1.0                           # mm laser-cut corner round on non-cutting corners
BAR_Z0 = 5.0                                 # mm underside above floor: 0.5 tyre squash + 58 mm x tan 3 deg seam = 3.6 (dynamics.floor_margin)
BAR_BOLT = "M3"
BAR_BOLT_D = 3.0
CSK_D = 6.2                                  # mm countersink diameter at the bar underside: M3 csk head dk 6.0 + 0.1 radial clear (was 5.5: head overlapped 0.15)
CSK_DEPTH = 1.75                             # mm: the countersink cone depth; the head sits inside it with no overlap
BAR_BOLT_N = 2                               # 2x M3 through bar into hub, PolarLocations
BAR_BOLT_PCD = 15.0                          # mm (was 11: a 1.3 mm web to the bore failed the sheet-cut rule)
BAR_BORE_CLR = 0.1                           # mm radial on the shaft pilot (centres the bar on the shaft)
LOCK_PIN_R = 20.0                            # mm radius of the rule 5f lock pin hole in the +X arm (clear of the hub, inside the arm)
LOCK_PIN_D = 3.0                             # mm steel lock pin (removable, tethered; pulled before a fight)
BAR_R_STEP = 0.5                             # mm search step of bar_r_geom()

# ---- turned hub (7075-T6): bolts to bell top screws, carries the bar ----
HUB_OD = 20.0                                # mm (> BAR_BOLT_PCD + M3 head)
HUB_H = 5.0                                  # mm turned spacer between bell cap and bar
HUB_GAP = 0.0                                 # mm: hub bolted down onto the bar (bar bolts need a contact face; hub is in the bar group)
HUB_SHAFT_CLR = 0.02                         # mm radial slide fit on the 5 mm shaft

# ---- weapon motor stack (shaft down, stator screwed up into the tub boss) ----
GAP_BAR_TUB = 1.2                            # mm air between bar top and tub floor underside (>> MIN_CLR_MOVING)
MOTOR_BELL_CLR = 1.3                         # mm radial bell to tub bore wall (spinning)

# ---- tub (printed nylon PA12/PA-CF, FDM) ----
BAR_BITE_REACH = 8.0                         # mm of tooth exposed beyond the tub rim, all round
TUB_WALL = 1.6                               # mm (> PROFILE.min_wall_fdm_mm)
TUB_FLOOR_T = 1.6                            # mm
TUB_SLOPE_DEG = 35.0                         # side slope from vertical: verticals glance off
TUB_TOP_Z = WHEEL_D - 2 * MIN_GROUND_CLR - 0.9   # body top below tyre top: invertible (wheels > body both sides)
DRIVE_MOTOR_L = 33.0                         # mm N10 body length along its shaft (catalogue bbb_n10_1000rpm, hw.size)
DRIVE_MOTOR_TIP_X = 20.25                    # mm shaft tip from the motor origin (catalogue bbox max X, origin on the axis)
DRIVE_MOTOR_FACE_X = 11.25                   # mm body front (shaft side) face from the motor origin (catalogue: box 9 wide at x 6.75)
DRIVE_MOTOR_REAR_X = -12.75                  # mm rear face (solder tabs) from the motor origin
# Two N10s in the same pod, each shaft pointing outboard to its wheel: the bodies run inboard from each side wall, so
# they must not meet in the middle. Each body spans [wall - L, wall] from its side: width >= 2 (L + wall) + clearance.
POD_W_MIN = 2 * (DRIVE_MOTOR_L + TUB_WALL) + 2 * MIN_CLR_MOVING   # mm (~70.8)
POD_L = 24.0                                 # mm rear pod length behind the axle line
TOP_PANEL_T = 1.0                            # mm top panel (Revron panel_top style)
PANEL_SCREW = "M2"                           # Revron fastening: M2 button into heat-sets
PANEL_SCREW_N = 6

# ---- drive / skids ----
BAR_TYRE_CLR = 3.0                           # mm plan clearance bar sweep -> nearest tyre point at bar-top height
WHEEL_CZ = WHEEL_D / 2                       # axle height
SKID_H = 1.0                                 # mm dome proud of the top panel beyond ground clearance
DOME_SCREW_CLR_D = 2.2                       # mm M2 clearance for the dome screw (through dome and top panel)
SKID_D = 6.0                                 # mm POM button


# ---- relations ----
def room():
    """Half side available inside the envelope."""
    return FOOTPRINT / 2 - FOOTPRINT_MARGIN


def bar_top_z():
    return BAR_Z0 + BAR_T


def tub_floor_z():
    """Tub floor underside: a fixed air gap above the bar."""
    return bar_top_z() + GAP_BAR_TUB


def tyre_half_chord(z):
    """Half length (Y) of the tyre's plan footprint at height z: where the bar plane cuts the tyre."""
    r = WHEEL_D / 2
    return math.sqrt(max(0.0, r * r - (r - z) ** 2))


def _bar_area(L):
    """Plan area of the tapered two-arm bar minus bore, bolt holes and the two bite steps (mm^2)."""
    holes = math.pi * ((SHAFT_D / 2) ** 2 + BAR_BOLT_N * (BAR_BOLT_D / 2) ** 2)
    steps = BAR_TOOTH_STEP * BAR_TOOTH_LEN
    return (BAR_W_ROOT + BAR_W_TIP) / 2 * L - holes - steps


def bar_r_mass():
    """Largest sweep radius the mass budget carries: bar mass = limit - margin - everything else."""
    g = MASS_LIMIT - MASS_MARGIN - sum(MASS_OTHER_G.values())
    area = g / (BAR_T * STEEL_DENSITY)
    holes_steps = -_bar_area(0)              # bore + bolt holes + bite steps (mm^2)
    return (area + holes_steps) / ((BAR_W_ROOT + BAR_W_TIP) / 2) / 2


def x_in_needed(r):
    """Tyre inner-face X the wheels need so the tyres sit BAR_TYRE_CLR outside a sweep r with the robot length
    (bar tip on the front margin -> tyre back on the rear margin) inside the envelope; inf if impossible."""
    dy_max = 2 * room() - r - WHEEL_D / 2 - tyre_half_chord(bar_top_z())
    if dy_max <= 0:
        return math.inf
    need = r + BAR_TYRE_CLR
    return max(POD_W_MIN / 2, math.sqrt(max(0.0, need * need - dy_max * dy_max)))


def bar_r_geom():
    """Largest sweep radius with the bar across X inside the room and the tyres (x_in_needed) inside it too."""
    r = room()
    while r > 0 and x_in_needed(r) + WHEEL_W + WHEEL_BOSS > room():
        r -= BAR_R_STEP
    return r


def max_volts():
    return CELLS[BATTERY] * CELL_HV_V


def bar_rpm(volts=None, kv=GR1507_KV, eff=0.8):
    """Estimate: no-load kV x V x 0.8 (load / ESC / sag)."""
    return kv * (max_volts() if volts is None else volts) * eff


def bar_r_tip():
    """Largest sweep radius under the profile tip-speed limit at full pack voltage."""
    w = bar_rpm() * 2 * math.pi / 60
    return PROFILE.max_tip_speed_mph / MPH_PER_MS / w * 1000


BAR_L_OLD = 116.0                            # mm: the old Scythe bar (f363606). The 2S 180 pack's 12.5 g would allow 128 mm, which
                                             # widens the track to ~79 mm: cap at the old length to keep the look.
BAR_L = math.floor(min(2 * min(bar_r_mass(), bar_r_geom(), bar_r_tip()), BAR_L_OLD))   # mm tip to tip
POD_W = 2 * x_in_needed(BAR_L / 2)           # mm between tyre inner faces (52 at the 150 default; 83.6 in the cube)
WPN_AXIS_Y = room() - BAR_L / 2              # bar tip (clocked fore-aft) on the front margin
TUB_R = BAR_L / 2 - BAR_BITE_REACH           # tub disc radius


def bar_sweep_r():
    return BAR_L / 2


def motor_x():
    """Right N10 origin X: the body's shaft-side face sits on the inner face of the pod wall, so the 9 mm shaft crosses
    the wall (2 mm) and the 0.4 mm gap and sits 6.6 mm deep in the wheel hub bore. The left motor is mirrored (rot 180 about Z)."""
    return POD_W / 2 - TUB_WALL - DRIVE_MOTOR_FACE_X


def wheel_x():
    """Wheel centre X (right side; left is mirrored): the inboard hub face clears the pod's outer wall."""
    return POD_W / 2 + WHEEL_INNER_REACH + MIN_CLR_MOVING


def wheel_y():
    """Wheel centre Y: the nearest point of the tyre footprint at bar-top height sits BAR_TYRE_CLR outside the sweep."""
    need = bar_sweep_r() + BAR_TYRE_CLR
    x_in = wheel_x() - WHEEL_INNER_REACH
    dy = math.sqrt(max(0.0, need * need - x_in * x_in)) + tyre_half_chord(bar_top_z())
    return WPN_AXIS_Y - dy


def overall_extent():
    """(x_half, y_front, y_rear) with the bar clocked worst-case (across X and along Y)."""
    x_half = max(bar_sweep_r(), wheel_x() + WHEEL_W / 2 + WHEEL_BOSS)
    return x_half, WPN_AXIS_Y + bar_sweep_r(), wheel_y() - WHEEL_D / 2


def bar_mass_g():
    return _bar_area(BAR_L) * BAR_T * STEEL_DENSITY


def total_mass_g():
    return bar_mass_g() + sum(MASS_OTHER_G.values())


def bar_moi_kgm2():
    """Estimate: thin bar 1/12 m L^2 (taper ignored, slight overestimate)."""
    return bar_mass_g() / 1000 / 12 * (BAR_L / 1000) ** 2


def wpn_motor_z():
    """Weapon motor origin Z (shaft down): the bell cap sits on the hub top face."""
    return bar_top_z() + HUB_GAP + HUB_H + WPN_CAP_X


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
    assert x_half <= room() + 1e-6, f"width {2 * x_half:.1f} > {2 * room():.1f}"
    assert yf - yr <= 2 * room() + 1e-6, f"length {yf - yr:.1f} over the envelope"
    if HEIGHT_LIMIT is not None:
        assert TUB_TOP_Z + SKID_H + MIN_GROUND_CLR <= HEIGHT_LIMIT
    assert total_mass_g() <= MASS_LIMIT - MASS_MARGIN + 1e-6
    assert tip_speed_ms(bar_rpm()) * MPH_PER_MS <= PROFILE.max_tip_speed_mph
    assert BAR_Z0 >= MIN_GROUND_CLR
    assert TUB_TOP_Z + MIN_GROUND_CLR <= WHEEL_D, "body taller than wheels: not invertible"
    return True
