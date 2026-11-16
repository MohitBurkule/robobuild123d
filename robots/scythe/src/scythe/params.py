"""Scythe master parameters and derived relations.

Frame: X right, Y forward (weapon end), Z up, floor at Z = 0 (same as Revron).
Every number used by geometry lives here, as a named master with its source, or as a relation of masters.
COTS dimensions/masses: geometry reads the catalogue (robot.catalog via cots() / revron hw + the bl_1806 split);
the literals below feed only the mass/energy relations that size the bar (no build needed to evaluate them).

Sizing chain (all relations, evaluated at import):
  envelope (rules)  ->  room = side/2 - margin
  mass budget       ->  bar_r_mass()   (largest bar the 150 g limit carries, MASS_MARGIN kept)
  tyres outside the sweep inside the envelope -> bar_r_geom()
  tip-speed rule    ->  bar_r_tip()
  energy rule       ->  bar_r_energy() (cantilevered undercutter: the bar hangs on the motor's own shaft,
                       so the stored energy is capped under the spinner escalation threshold)
  BAR_L = 2 * min(...) rounded down to 1 mm; then POD_W (track), WPN_AXIS_Y, TUB_R follow from BAR_L.
"""
import math
import os

from robot.profile import Profile

PROFILE = Profile()                          # aws2025 (robot/profile.py)

# ---- size envelope: ONE setting. Default = robot/profile.py (AWS 2025: 150 mm floor square, no overhang at any
# height, no height limit). Optional variant "aws_v43_cube": 101.6 mm (4 in) cube in start config (AWS v4.3 2b).
# Select with use_rules("aws_v43_cube") (reloads this module) or env SCYTHE_RULES before import.
CUBE_V43 = 101.6                             # mm, AWS rules v4.3 2b (old rule, optional variant only)
ENVELOPES = {
    "aws2025": dict(side=PROFILE.footprint_mm, height=None, tub_g=19.0, top_panel_g=8.0),       # tub/panel g: estimates
    "aws_v43_cube": dict(side=CUBE_V43, height=CUBE_V43, tub_g=17.0, top_panel_g=6.5),
}
RULES = os.environ.get("SCYTHE_RULES", "aws2025")
ENVELOPE = ENVELOPES[RULES]
FOOTPRINT = ENVELOPE["side"]                 # mm, square floor side (150 default)
HEIGHT_LIMIT = ENVELOPE["height"]            # mm or None (AWS 2025 has no height limit)


def use_rules(name):
    """Switch the envelope variant and re-derive every relation (other modules read params as P.<name> at call time)."""
    import importlib, sys
    if name not in ENVELOPES:
        raise KeyError(f"rules `{name}`; one of {sorted(ENVELOPES)}")
    os.environ["SCYTHE_RULES"] = name
    return importlib.reload(sys.modules[__name__])


MASS_LIMIT = PROFILE.roller_mass_g           # 150 g (Scythe is a roller: wheels, no walking)
MIN_CLR_MOVING = PROFILE.min_clearance_moving_mm   # 0.4 mm moving-part rule floor
MIN_GROUND_CLR = PROFILE.min_ground_clearance_mm   # 1.0 mm
FOOTPRINT_MARGIN = 1.5                       # mm kept off each envelope face (print tolerance + sizing-box wall)
MASS_MARGIN = 3.0                            # g kept under MASS_LIMIT (the gate limit is 150)
MPH_PER_MS = 2.23694                         # unit conversion

# ---- COTS (catalogue ids; the robot/gen templates use the same ids) ----
WEAPON_MOTOR = "bl_1806_2300kv"              # 1806 2300 kV outrunner, split pair (stator + can)
WEAPON_MOTOR_STATOR = "bl_1806_stator"       # fixed half (base flange with 4 M2 taps on 16 mm)
WEAPON_MOTOR_CAN = "bl_1806_can"             # rotating half (21 mm bell, bored core for the 3 mm shaft)
DRIVE_MOTOR = "bbb_n10_1000rpm"
WHEEL = "bbb_wheel_34x6_5"
BATTERY = os.environ.get("SCYTHE_BATTERY", "c_typical_2s_300mah_lipo_lihv_betafpv_tbs_")
BATTERY_2S = "c_typical_2s_300mah_lipo_lihv_betafpv_tbs_"
BATTERY_3S = "gnb_3s_300_80c_hv"             # variant (variants.py)
WEAPON_ESC = "bbb_brushless_esc_20a"
DRIVE_RX = "bbb_malenki_nano"                # alt: bbb_dual_esc_v31
SWITCH = "fingertech_mini_switch"
SHAFT_NUT = "nut_m3_alu"

# Catalogue masses (robot.catalog; the mass table mirrors them for the no-build sizing relations)
CAT_MASS_G = {WEAPON_MOTOR: 17.5, DRIVE_MOTOR: 8.0, WHEEL: 4.1, BATTERY_2S: 15.8, BATTERY_3S: 28.0,
              WEAPON_ESC: 5.0, DRIVE_RX: 2.3, SWITCH: 2.15, SHAFT_NUT: 0.1}
CELLS = {BATTERY_2S: 2, BATTERY_3S: 3}
CELL_HV_V = 4.35                             # V per LiHV cell full (both packs are HV); PROFILE.max_cell_v = 4.2 is the
                                             # rule check value -> see BRIEF unsure list
WHEEL_D = 34.0                               # INDEX.md bbb_wheel_34x6_5: 34 x 6.5 (+2 boss)
WHEEL_W = 6.5
WHEEL_BOSS = 2.0                             # mm hub boss proud of the tyre per side (INDEX.md "+2 boss", estimate)
BL_KV = 2300.0                               # robot.catalog bl_1806_2300kv props (kV)
SHAFT_D = 3.0                                # robot.catalog bl_1806 shaft dia (the motor's own shaft, extended)

# bl_1806 split frame (robot/catalog.py _bl1806_*: local X along the axis, +X = bell top / output, origin at the
# can centre; the robot mounts it output-down, so local +X maps to world -Z)
BL_HALF = 7.0                                # mm body half length (can -7..7)
BL_FLANGE_H = 3.5                            # mm base flange thickness (local x -7..-3.5)
BL_FLANGE_R = 9.5                            # mm base flange radius (4 M2 taps on a 16 mm circle)
BL_STACK_R = 9.0                             # mm stator stack (tooth tips) radius
BL_BELL_R = 10.5                             # mm bell outer radius (21 mm can)
BL_BORE_R = 1.55                             # mm stator through-bore (clears the r1.5 shaft)
BL_BELL_BORE_TOP = 5.5                       # mm local-x of the bell core bore's far end (the shaft's upper reach)
BL_SCREW_PCD = 16.0                          # mm base flange tap circle (4 x M2)

# Everything but the bar, g. COTS from the catalogue, the rest measured from the built solids (tub/panel printed at
# 0.85 solid fraction, hub 7075, silver-steel shaft, alloy screws + nut).
MASS_OTHER_G = {
    "weapon_motor": CAT_MASS_G[WEAPON_MOTOR], "drive_motors": 2 * CAT_MASS_G[DRIVE_MOTOR],
    "wheels": 2 * CAT_MASS_G[WHEEL], "battery": CAT_MASS_G[BATTERY], "weapon_esc": CAT_MASS_G[WEAPON_ESC],
    "drive_rx": CAT_MASS_G[DRIVE_RX], "switch": CAT_MASS_G[SWITCH],
    "hub_7075": 2.6, "shaft_nut": CAT_MASS_G[SHAFT_NUT], "wshaft_steel": 1.4, "screws": 3.4, "wires": 2.0,
    "tub": 16.0, "top_panel": 4.0, "allowance": PROFILE.allowance_g,
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
BAR_BORE_CLR = 0.05                          # mm radial on the shaft pilot (centres the bar on the shaft)
BAR_BOLT_D = 2.5                             # M2.5 bar-to-hub screws (1.5d = 3.75 mm into the 4 mm hub)
BAR_BOLT_N = 2                               # 2x through bar into hub, on the centreline
BAR_BOLT_PCD = 15.0                          # mm (edge distance in the hub: 11.5 - 7.5 = 4.0 >= 1.5d)
BAR_LOCK_X = 18.0                            # mm: the weapon-lock pin hole along the +X arm (clear of the
                                             # counterbores at 7.5 and inside the panel's disc at the top)
BAR_LOCK_D = 3.2                             # mm pin hole (a 3 mm pit pin drops through panel, floor and bar)
BAR_R_STEP = 0.5                             # mm search step of bar_r_geom()
ENERGY_LIMIT_J = 18.0                        # J stored-energy cap: the bar hangs on the motor's own extended
                                             # shaft (cantilevered undercutter), so the spinner escalation
                                             # threshold (20 J) must never trip

# ---- rotor stack, bottom up (all z relations derive from these) ----
# M3 nut -> bar -> hub -> bell cap face (the motor's own shaft runs through the lot); an MR83ZZ in the boss
# above the stator flange is the rotor's second support (the motor's own bearings are the first).
NUT_T = 2.4                                  # mm M3 nut thickness (catalogue nut_m3_alu)
HUB_H = 4.0                                  # mm turned spacer between bell cap and bar (>= 1.5d of the M2.5s)
HUB_OD_R = 11.5                              # mm hub outer radius (edge distance for the M2.5 taps)
HUB_BORE_R = 1.6                             # mm hub bore on the shaft
HUB_CUP_ID_R = 10.6                          # mm the hub's top cup pilots on the bell rim (bell r 10.5)
HUB_CUP_H = 2.0                              # mm cup depth at the top of the hub
WSHAFT_TIP_Z = 1.0                           # mm the shaft's lower end above the floor (threaded M3 for the nut)
MOTOR_BELL_CLR = 1.0                         # mm radial hub to tub bore wall (spinning)
BEARING_T = 2.5                              # mm MR83ZZ 3 x 5 x 2.5 width (the boss's bore is its press seat)
BEARING_OD_R = 2.5                           # mm MR83ZZ outer race
BEARING_ID_R = 1.5                            # mm MR83ZZ inner race (a slide fit on the 3 mm shaft)

# ---- weapon motor mount (stator flange up, screwed through the panel and the printed boss) ----
BOSS_T = 2.5                                 # mm printed boss ring between the flange top face and the panel: the
                                             # MR83ZZ's press seat (the bearing sits directly on the flange face)
BOSS_ID_R = 2.45                             # mm the bearing's press seat (OD 5.0 with 0.05 interference)
BOSS_OD_R = 14.0                             # mm boss outer radius (merges into the housing tube wall)
WIRE_SLOT_IN_R = 2.5                         # mm the phase-lead slot starts outside the bearing's outer race
WIRE_SLOT_W = 3.2                            # mm the phase-lead slot through the boss ring at SLOT_ANGLE_DEG (between
                                             # the flange tap circle)
SLOT_ANGLE_DEG = 45.0                        # deg: between the flange's 4 M2 taps (0/90/180/270)
SCREW_ANGLES = (0.0, 90.0, 180.0, 270.0)      # deg: the bl_1806 base-flange tap phases (catalogue local y/z +-8)
BL_SCREW_CLR_R = 1.1                         # mm: the M2 stator screw clearance bores through panel and boss

# ---- tub (printed nylon PA12/PA-CF, FDM) ----
BAR_BITE_REACH = 8.0                         # mm of tooth exposed beyond the tub rim, all round
TUB_WALL = 1.5                               # mm (> PROFILE.min_wall_fdm_mm 0.9; the mass budget is tight
TUB_FLOOR_T = 1.6                            # mm
TUB_SLOPE_DEG = 15.0                         # side slope from vertical: verticals glance off; shallow enough that
                                             # the pack fits under the sloped wall at its full height
TUB_TOP_Z = WHEEL_D - 2 * MIN_GROUND_CLR - 2.0   # body top below tyre top: invertible (wheels > body both sides)
# pod width the internals need: two N10 bodies (24.5 mm each) nested against the walls with a 6.5 mm centre gap
# the battery lead passes through, plus the walls
POD_W_MIN = 65.0
POD_REAR = 52.0                               # mm the pod extends behind the axle line: the N10s (6) + the ESC bay +
                                              # the battery bay + the switch bay, inside the rear envelope margin
TOP_PANEL_T = 1.0                            # mm top panel (Revron panel_top style)
PANEL_SCREW = "M2"                            # Revron fastening: M2 button into printed posts
PANEL_SCREW_N = 6

# ---- drive ----
BAR_TYRE_CLR = 3.0                           # mm plan clearance bar sweep -> nearest tyre point at bar-top height
WHEEL_CZ = WHEEL_D / 2                       # axle height
# N10 gearmotor solid extents in the catalogue frame, x along the shaft (bbb_n10_1000rpm): body -12.75..11.75,
# shaft stub to 20.25. The body nests against the pod wall, outboard face to wall, so the shaft still reaches
# the wheel and the two bodies leave a 5.9 mm centre gap for the battery lead.
N10_BODY_IN = -12.75
N10_BODY_OUT = 11.75
N10_HALF_Y = 6.0                            # mm gearmotor body half width (catalogue solid)
N10_HALF_Z = 5.0                            # mm gearmotor body half height (axle at WHEEL_CZ)
CRADLE_RIB_T = 1.2                           # mm printed rib thickness flanking each N10
CRADLE_RIB_H = 16.0                          # mm rib top: locates the gearbox's lower half, motor still drops out
CRADLE_CLR = 0.4                             # mm gap motor-to-rib (assembly clearance)
CRADLE_PAD_TOP = 11.95                       # mm: the motor rests on the pad with 0.05 mm fit clearance
POST_R = 3.0                                  # mm: printed post the panel screws thread into
POST_Z0 = 24.0                                # mm: post base (merged with the sloped disc wall)
DISC_POST_IN = 2.5                            # mm: disc rim posts sit this far inboard of the wall centre
PANEL_OVERHANG = 0.9                          # mm: the panel grows past the tub top so screw heads stay on skin
POD_POST_Y = (-12.0, -20.0)                   # mm, relative to the axle line: pod-wall post positions (clear of
                                              # the cradle ribs and the wire corridor under the posts)
SKID_PAD_R = 4.0                             # mm rear skid pad radius (printed with the tub, behind the sweep)
SKID_PAD_X = 22.0                            # mm rear skid pads off the centreline (two, for the stance polygon)
SKID_PAD_BAY = 6.0                           # mm the pads sit this far off the pod's rear wall inner face
SWITCH_BAY = 8.0                             # mm: the switch bay centre this far off the pod's rear wall inner face
SWITCH_KEY_OFF_X = 3.175                     # mm: the switch's mounting bushing sits this far +X at rot 270
NOSE_DOWN_DEG = 5.0                          # deg: the threat model's nose-down pitch (CF-OW01 hop-on-hit)
PITCH_CLR_MM = 0.3                           # mm the bar's front tip must still clear the floor at NOSE_DOWN_DEG
SPINNER_ENERGY_CAP_J = 20.0                  # J: the spinner escalation threshold (energy over this makes the
                                             # cantilevered undercutter's open side a blocker, so stay under it)
MM_PER_M = 1000.0                            # mm per m (unit conversions)
MOI_TWELFTH = 12.0                          # 1/12 in I = m (L^2 + W^2) / 12
ROTOR_REST_MOI_KGM2 = 1.0e-6                  # kg m^2: bell + hub + nut + shaft + screws near the axis


def switch_y():
    """World Y of the slide switch (in its bay at the rear of the pod, clear of the pack bay ahead of it)."""
    return wheel_y() - POD_REAR + TUB_WALL + SWITCH_BAY


# ---- relations ----
def room():
    """Half side available inside the envelope."""
    return FOOTPRINT / 2 - FOOTPRINT_MARGIN


def nut_z0():
    """Nut underside z: the whole rotor stack is stacked down from the panel (bearing -> motor -> hub -> bar ->
    nut), so the bar sits as high as the stance allows."""
    return TUB_TOP_Z - TOP_PANEL_T - (BEARING_T + 2 * BL_HALF + HUB_H + BAR_T + NUT_T)


def nut_top_z():
    return nut_z0() + NUT_T


def bar_z0():
    return nut_top_z()


def bar_top_z():
    return bar_z0() + BAR_T


def motor_z():
    """Weapon motor origin z: the bell cap face sits on the hub top (bl_1806: cap face at local +7)."""
    return bar_top_z() + HUB_H + BL_HALF


def flange_top_z():
    """Stator base-flange top face z (bl_1806: flange back at local -7)."""
    return motor_z() + BL_HALF


def boss_bottom_z():
    return flange_top_z() + 2.0


def tub_floor_z():
    """Tub floor underside: the floor top stays MIN_CLR_MOVING under the N10 bodies (the axle-height gearmotors
    sit on it), and the floor rides above the bar with its centre bore clearing the spinning hub."""
    return WHEEL_CZ - N10_HALF_Z - MIN_CLR_MOVING - TUB_FLOOR_T


def wshaft_top_z():
    """The motor's own shaft, extended: from the nut thread up through the MR83ZZ in the boss, flush under the panel."""
    return TUB_TOP_Z - TOP_PANEL_T - 0.1


def wshaft_len():
    return wshaft_top_z() - WSHAFT_TIP_Z


def housing_in_r():
    """Printed housing tube / floor bore: clears the spinning hub (r 11.5) by 1.0 mm; the bell (r 10.5) inside
    the hub's sweep gets 2.0 mm."""
    return HUB_OD_R + MOTOR_BELL_CLR


def housing_out_r():
    return housing_in_r() + TUB_WALL


def tyre_half_chord(z):
    """Half length (Y) of the tyre's plan footprint at height z: where the bar plane cuts the tyre."""
    r = WHEEL_D / 2
    return math.sqrt(max(0.0, r * r - (r - z) ** 2))


def _bar_area(L):
    """Plan area of the tapered two-arm bar minus bore, bolt holes, lock hole and the two bite steps (mm^2)."""
    holes = math.pi * ((SHAFT_D / 2 + BAR_BORE_CLR) ** 2 + BAR_BOLT_N * (BAR_BOLT_D / 2) ** 2 + (BAR_LOCK_D / 2) ** 2)
    steps = BAR_TOOTH_STEP * BAR_TOOTH_LEN
    return (BAR_W_ROOT + BAR_W_TIP) / 2 * L - holes - steps


def bar_r_mass():
    """Largest sweep radius the mass budget carries: bar mass = limit - margin - everything else."""
    g = MASS_LIMIT - MASS_MARGIN - sum(MASS_OTHER_G.values())
    area = g / (BAR_T * STEEL_DENSITY)
    holes_steps = -_bar_area(0)              # bore + bolt holes + lock hole + bite steps (mm^2)
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


def bar_rpm(volts=None, kv=BL_KV, eff=0.85):
    """Estimate: no-load kV x V x 0.85 (load / ESC / sag), the same factor the energy check uses."""
    return kv * (max_volts() if volts is None else volts) * eff


def bar_r_tip():
    """Largest sweep radius under the profile tip-speed limit at full pack voltage."""
    w = bar_rpm() * 2 * math.pi / 60
    return PROFILE.max_tip_speed_mph / MPH_PER_MS / w * 1000


def bar_moi_kgm2(L=None):
    """Estimate: bar about its centre, I = m ((2L)^2 + W^2) / MOI_TWELFTH (taper ignored, slight overestimate)
    + the rotor stack's share (bell, hub, nut, shaft, screws, all near the axis)."""
    L = BAR_L / 2 if L is None else L
    m = _bar_area(2 * L) * BAR_T * STEEL_DENSITY / MM_PER_M
    return m / MOI_TWELFTH * ((2 * L / MM_PER_M) ** 2 + (BAR_W_ROOT / MM_PER_M) ** 2) + ROTOR_REST_MOI_KGM2


def bar_r_energy():
    """Largest sweep radius whose stored energy stays under ENERGY_LIMIT_J (cantilevered weapon rule)."""
    w = bar_rpm() * 2 * math.pi / 60
    r = 1.0
    while r < room() and 0.5 * bar_moi_kgm2(r) * w * w <= ENERGY_LIMIT_J:
        r += BAR_R_STEP
    return r - BAR_R_STEP


def bar_r_pitch():
    """Largest sweep radius whose front tip still clears the floor slab at NOSE_DOWN_DEG (the hop-on-hit pitch
    about the wheels, CF-OW01): tip drop = (tip_y - wheel_y) tan(NOSE_DOWN_DEG) must fit under the bar."""
    r = 1.0
    while r < room():
        ay = room() - r
        need = r + BAR_TYRE_CLR
        x_in = POD_W_MIN / 2
        dy = math.sqrt(max(0.0, need * need - x_in * x_in)) + tyre_half_chord(bar_top_z())
        drop = (ay + r - (ay - dy)) * math.tan(math.radians(NOSE_DOWN_DEG))
        if bar_z0() - drop < PITCH_CLR_MM:
            return r - BAR_R_STEP
        r += BAR_R_STEP
    return r - BAR_R_STEP


BAR_L = math.floor(2 * min(bar_r_mass(), bar_r_geom(), bar_r_tip(), bar_r_energy(), bar_r_pitch()))   # mm tip to tip
POD_W = 2 * x_in_needed(BAR_L / 2)           # mm between tyre inner faces (52 at the 150 default; 83.6 in the cube)
WPN_AXIS_Y = room() - BAR_L / 2              # bar tip (clocked fore-aft) on the front margin
TUB_R = BAR_L / 2 - BAR_BITE_REACH           # tub disc radius


def bar_sweep_r():
    return BAR_L / 2


def wheel_x():
    """Wheel centre X (right side; left is mirrored): the hub boss bears on the pod wall's outer face, so the
    tyre plane clears the wall and the wall is clamped between gearbox face and wheel."""
    return POD_W / 2 + WHEEL_W / 2 + WHEEL_BOSS


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
    return _bar_area(BAR_L) * BAR_T * STEEL_DENSITY


def total_mass_g():
    return bar_mass_g() + sum(MASS_OTHER_G.values())


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
        assert TUB_TOP_Z + MIN_GROUND_CLR <= HEIGHT_LIMIT
    assert total_mass_g() <= MASS_LIMIT - MASS_MARGIN + 1e-6
    assert tip_speed_ms(bar_rpm()) * MPH_PER_MS <= PROFILE.max_tip_speed_mph
    assert energy_j(bar_rpm()) <= SPINNER_ENERGY_CAP_J, "weapon energy over the cantilever escalation threshold"
    assert WSHAFT_TIP_Z >= MIN_GROUND_CLR
    assert bar_z0() - (WPN_AXIS_Y + bar_sweep_r() - wheel_y()) * math.tan(math.radians(NOSE_DOWN_DEG)) >= PITCH_CLR_MM
    assert TUB_TOP_Z + MIN_GROUND_CLR <= WHEEL_D, "body taller than wheels: not invertible"
    return True
