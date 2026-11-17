"""Master parameters and derived coordinates for Disector (150 g AWS 2025).

Frame: X right (+x), Y forward (+y), Z up (+z), floor Z = 0.

Every build function takes its dimensions from this module; features are placed by relation to the named masters
(battery size, wheel position, servo size, ...) rather than by raw coordinates in the builders.
"""

from __future__ import annotations

import math

INV_SQRT2 = 1.0 / math.sqrt(2.0)


def mx(box):
    """Mirror an (x0, x1, y0, y1, z0, z1) box about the X = 0 plane."""
    return (-box[1], -box[0], *box[2:])


# --- Envelope & chassis masters ---
Z_FLOOR_BOT = 2.0        # 2.0 mm ground clearance (>= 1.0 mm)
FLOOR_T = 2.0            # 2.0 mm tub floor
Z_FLOOR_TOP = Z_FLOOR_BOT + FLOOR_T  # 4.0 mm
Z_TOP = 24.0             # tub top deck height
WALL_T = 2.0             # perimeter wall thickness
CORNER_R = 4.0           # external corner fillet radius
Z_CUT_TOP = Z_TOP + 1.0  # pocket cuts run out through the deck plane

TUB_HALF_W = 48.0        # 96 mm wide tub (X in [-48, +48])
Y_REAR = -40.0           # rear wall outer face
Y_FRONT_TOP = 8.0        # top of 45 deg sloped front face
# 45 deg slope from (Y=8, Z=24) to (Y=28, Z=4): Y + Z = 32
Y_FRONT_BOT = Y_FRONT_TOP + (Z_TOP - Z_FLOOR_TOP)  # 28.0 mm

# --- Drive motors & wheels (wheel_20x8, r=10 mm, w=8 mm) ---
WHEEL_R = 10.0
WHEEL_W = 8.0
WHEEL_Z = WHEEL_R        # 10.0 mm -> touches floor Z = 0
WHEEL_Y = -22.0
WHEEL_X = 43.0           # wheels span X = +/-[39.0, 47.0]
MOTOR_X = WHEEL_X - 15.05  # 27.95 mm (n10_2200rpm_6v shaft center at +15.05)
WELL_CLR = 0.5           # wheel well side clearance
WELL_Y_CLR = 2.0         # wheel well clearance fore/aft of the tyre

# Wheel wells (cut through the side wall, mirrored)
WELL_X0 = WHEEL_X - WHEEL_W / 2 - WELL_CLR                       # 38.5
WHEEL_WELL = (WELL_X0, TUB_HALF_W + 1.0, WHEEL_Y - WHEEL_R - WELL_Y_CLR, WHEEL_Y + WHEEL_R + WELL_Y_CLR,
              1.0, Z_TOP - 1.0)
# Drive motor pockets, drop-in from the top, snug on the inner face so the motor (X=17.40 inner) is captured
MOTOR_IN_X = 17.40
MOTOR_POCKET = (MOTOR_IN_X - 0.25, WELL_X0 + 0.1, WHEEL_Y - 5.5, WHEEL_Y + 5.5, Z_FLOOR_TOP - 0.2, Z_CUT_TOP)

# --- Internal electronics ---
# Battery: lipo_2s_350 (36 x 17 x 11)
BAT_L, BAT_W, BAT_H = 36.0, 17.0, 11.0
BAT_AT = [0.0, -5.0, Z_FLOOR_TOP + BAT_H / 2]  # [0, -5, 9.5]
BAY_CLR = 0.15           # snug pocket clearance round the battery (tape/velcro face and pocket walls)
BAT_Y0, BAT_Y1 = BAT_AT[1] - BAT_W / 2, BAT_AT[1] + BAT_W / 2
BAT_BAY = (BAT_AT[0] - BAT_L / 2 - BAY_CLR, BAT_AT[0] + BAT_L / 2 + BAY_CLR,
           BAT_Y0 - BAY_CLR, BAT_Y1 + BAY_CLR, Z_FLOOR_TOP, Z_CUT_TOP)
XT30_POCKET = (-7.0, 7.0, BAT_Y1, BAT_Y1 + 6.0, Z_FLOOR_TOP, 19.0)   # connector pocket in front of the pack
# Malenki Nano: malenki_nano (23 x 16 x 5) in front of right wheel well
MAL_L, MAL_W, MAL_H = 23.0, 16.0, 5.0
MALENKI_AT = [31.5, -1.1, Z_FLOOR_TOP + MAL_H / 2]  # board set back so its bay keeps a rim behind the sloped front
MAL_BAY = (MALENKI_AT[0] - MAL_L / 2 - 0.2, MALENKI_AT[0] + MAL_L / 2,
           MALENKI_AT[1] - MAL_W / 2, MALENKI_AT[1] + MAL_W / 2, Z_FLOOR_TOP, Z_CUT_TOP)
# Brushless ESC: bbb_ant_esc (22 x 11 x 4) in front of left wheel well
WESC_H = 4.0
WPN_ESC_AT = [-31.5, -0.5, Z_FLOOR_TOP + WESC_H / 2]  # [-31.5, -0.5, 6.0]
# Servo: servo_cs07 (23 x 12 x 22.7), rotated [0, -90, 0] so output shaft is along X and the lead exits at the bottom
SERVO_AT = [0.0, -28.0, 19.0]
SERVO_ROT = [0.0, -90.0, 0.0]
SERVO_W, SERVO_D, SERVO_H = 22.7, 12.0, 23.0     # world X, Y, Z of the body
SERVO_EAR_X = 6.9                                # ear plate offset from the servo axis (mirrored with the rotation)
SERVO_EAR_T = 2.5
SERVO_BAY_CLR_X, SERVO_BAY_CLR_Y = 0.85, 0.5
SERVO_BOT = SERVO_AT[2] - SERVO_H / 2            # 7.5
SERVO_BAY = (SERVO_AT[0] - SERVO_W / 2 - SERVO_BAY_CLR_X, SERVO_AT[0] + SERVO_W / 2 + SERVO_BAY_CLR_X,
             SERVO_AT[1] - SERVO_D / 2 - SERVO_BAY_CLR_Y, SERVO_AT[1] + SERVO_D / 2 + SERVO_BAY_CLR_Y,
             SERVO_BOT - 0.5, Z_CUT_TOP)
# Ear-plate clearance (the CS07 mounting ears), on the -X side with the flipped servo
SERVO_EAR_CUT = mx((SERVO_EAR_X - 2.1, SERVO_EAR_X + 2.3, SERVO_BAY[2], SERVO_BAY[3], Z_FLOOR_BOT + 0.8, Z_CUT_TOP))
# Lead channel under the servo: signal lead leaves the bottom face and runs forward into the rear bus
SERVO_LEAD_CH = (-2.5, 2.5, SERVO_AT[1] - 1.5, -18.0, SERVO_BOT - 2.5, SERVO_BOT + 0.5)
# Switch: switch_bbb_ant_rvrn2 at X=15.0, Y=-17.0, flange bottom at Z=24.0
SWITCH_AT = [15.0, -17.0, 22.25]
SW_EAR_DX = 7.5          # mounting ear hole offset from the switch centre
SW_PIT_HALF_X, SW_Y0, SW_Y1 = 5.5, -20.0, -14.0
SW_RIB_HALF = 2.2        # switch mounting ribs under the ear screws (ribs centred 8 mm off the switch centre)
SW_RIB_DX = 8.0
SWITCH_RIBS = [(SWITCH_AT[0] + s * SW_RIB_DX - SW_RIB_HALF, SWITCH_AT[0] + s * SW_RIB_DX + SW_RIB_HALF,
                SW_Y0, SW_Y1, 19.0, Z_TOP) for s in (-1, 1)]

# Wire channels cut through the tub web (>= 4 mm, so a bundle passes)
BUS_Y0, BUS_Y1 = -19.0, BAT_BAY[2] - 1.2          # rear bus, leaves a 1.2 mm wall behind the pack
BUS_REAR = (-22.0, 20.0, BUS_Y0, BUS_Y1, 5.0, 19.0)
SWITCH_PIT = (SWITCH_AT[0] - SW_PIT_HALF_X, SWITCH_AT[0] + SW_PIT_HALF_X, SW_Y0, BAT_BAY[2], 6.0, Z_CUT_TOP)   # opens into the pack bay (no sliver of wall between them)
BUS_BAT_SLOT = (-4.0, 14.0, BUS_Y1 - 0.5, BAT_BAY[2] + 0.5, 16.0, Z_CUT_TOP)   # lead from the pack over the wall
BUS_FRONT = (-22.0, 22.0, -4.0, 2.0, 6.0, 15.0)
CH_MAL_BUS = (18.0, 23.0, -15.5, 0.0, 5.0, 16.0)       # rear bus -> malenki_rx.bat
WIRE_LANE_Y0 = WHEEL_Y + WHEEL_R + 2.0                # wires stay >= 2 mm off the tyre: lane edge beside the wheel wells
CH_MAL_MOTOR = (22.0, WELL_X0 - 2.0, -15.0, -8.0, 5.0, 16.0)       # malenki -> motor_r & +X loop (inboard of the wheel)
CH_MAL_LANE = (WELL_X0 - 2.0, 46.0, WIRE_LANE_Y0, -8.0, 5.0, 16.0)  # lane along the wheel well, 2 mm off the tyre
CH_MAL_SIDE = (43.0, 46.0, WIRE_LANE_Y0, 5.0, 4.0, 11.5)           # malenki +X side channel (below f_gr_2)
CH_ESC_MOTOR = (-28.0, -22.0, -18.0, -8.0, 6.0, 16.0)  # wpn_esc -> motor_l
CH_ESC_BUS = (-WELL_X0 + 2.0, -18.0, -15.0, -8.0, 5.0, 16.0)    # rear bus -> weapon_esc (inboard of the wheel)
CH_ESC_LANE = mx(CH_MAL_LANE)
CH_ESC_SIDE = mx(CH_MAL_SIDE)                          # weapon_esc -X side channel (below f_gl_2)
CH_ESC_WEAPON = (-21.5, -16.0, BUS_Y0 + 0.5, BUS_Y1, 10.0, Z_CUT_TOP)   # weapon_esc -> weapon_motor vertical slot
CH_MOTOR_L = (-18.5, -13.0, -24.0, -18.0, 7.0, 14.0)   # rear bus -> motor_l.terminals

# Rear corner hollows (lighten the tub; outside the servo bay, corner screws and f_tc)
REAR_HOLLOW = (14.5, WELL_X0 + 4.5, Y_REAR + WALL_T, -31.0, Z_FLOOR_TOP, Z_CUT_TOP)
# Front wedge interior hollow: triangle in Y-Z (leaves a 4.6 mm sloped wall), +/-FRONT_HOLLOW_HALF_W wide
FRONT_WALL_T = 7.4       # normal thickness left in the sloped front wall (the pad screws' tap drills need 6.3 mm + 1 mm of wall)
FRONT_HOLLOW_D = (Y_FRONT_BOT + Z_FLOOR_TOP) - FRONT_WALL_T * math.sqrt(2.0)   # hollow's sloped face: Y + Z
FRONT_HOLLOW_Y0 = MAL_BAY[3] + 1.0       # leaves a 1 mm web in front of the Malenki / weapon-ESC bays
FRONT_HOLLOW_HALF_W = 38.0
FRONT_CORE_WALL_T = 3.0   # mid-width the wall only carries the wedge plate and the eyes (no screws there): thinner
FRONT_CORE_HALF_W = 14.0  # between the fork mounts
FRONT_CORE_D = (Y_FRONT_BOT + Z_FLOOR_TOP) - FRONT_CORE_WALL_T * math.sqrt(2.0)

# --- Top panels ---
PANEL_TOP_T = 1.2
TOP_SPINE_T = 1.6
PANEL_INSET = 0.5                       # panel stands in from the tub edge
PANEL_X = TUB_HALF_W - PANEL_INSET
PANEL_Y0, PANEL_Y1 = Y_REAR + 1.0, Y_FRONT_TOP - 0.2
PANEL_CUT_Z = (Z_TOP - 1.0, Z_TOP + PANEL_TOP_T + 1.0)
PANEL_SERVO_CUT = (SERVO_BAY[0] - 0.8, SERVO_BAY[1] + 0.8, SERVO_BAY[2] - 0.5, SERVO_BAY[3], *PANEL_CUT_Z)
PANEL_SWITCH_CUT = (SWITCH_AT[0] - 10.5, SWITCH_AT[0] + 10.5, SW_Y0, SW_Y1, *PANEL_CUT_Z)
PANEL_WIRE_CUT = (-20.5, -17.0, BUS_Y0 + 0.5, BUS_Y1, *PANEL_CUT_Z)   # weapon phase leads: behind the pack and ESC footprints, so no straight line to them
SPINE_X, SPINE_Y0, SPINE_Y1 = 42.0, 2.0, 7.8

# --- Front wedge & ground game ---
WEDGE_T = 1.0
WEDGE_W = 96.0
WEDGE_SLOPE_LEN = math.hypot(Y_FRONT_BOT - Y_FRONT_TOP, Z_TOP - Z_FLOOR_TOP)  # 20*sqrt(2) = 28.28 mm
WEDGE_LIP_DZ = 3.0       # plate runs this far below the tub's front edge, down towards the floor (scoop lip)
WEDGE_LIP = WEDGE_LIP_DZ / INV_SQRT2
WEDGE_GAP = 0.05         # plate stands off the tub face (no coplanar overlap)
# Midpoint of tub front slope face: Y = 18.0, Z = 14.0
WEDGE_MID_Y = 0.5 * (Y_FRONT_TOP + Y_FRONT_BOT)
WEDGE_MID_Z = 0.5 * (Z_TOP + Z_FLOOR_TOP)
PAD_T = 3.2              # flat 45-deg mounting pad, normal thickness
WEDGE_OUT_D = (Y_FRONT_BOT + Z_FLOOR_TOP) + 2 * WEDGE_GAP + WEDGE_T * math.sqrt(2.0)  # wedge outer face: Y + Z
PAD_OUT_D = WEDGE_OUT_D + PAD_T * math.sqrt(2.0)   # pad outer face: Y + Z
WEDGE_OUT_Y = WEDGE_MID_Y + WEDGE_GAP + WEDGE_T * INV_SQRT2      # wedge outer face mid-point
WEDGE_OUT_Z = WEDGE_MID_Z + WEDGE_GAP + WEDGE_T * INV_SQRT2
EYE_X, EYE_R, EYE_T = 6.5, 4.2, 1.4
EYE_Y = WEDGE_MID_Y + 1.11    # eye seat on the wedge plate
EYE_Z = WEDGE_MID_Z + 1.11

FORK_MOUNT_X = 22.0
FORK_T = 1.5
FORK_PIVOT_Y = 33.5
FORK_PIVOT_Z = 6.0
FORK_TIP_Y = 59.0
FORK_TIP_Z = 0.2
FORK_BACK = 2.3          # fork heel behind pivot pin (web to the pin bore >= 0.75 t for the laser)
FORK_PIN_R = 1.05        # fork bore (M2 clevis pin)
FORK_BORE_R = FORK_PIN_R + 0.05          # mount bore
FORK_TOP_DZ, FORK_BOT_DZ = 2.8, 2.2      # fork heel height above / below the pivot
FORK_NOSE_DY = 3.0                       # top edge runs this far ahead of the pivot before sloping to the tip
FORK_TIP_T = 0.6                         # fork tip edge height
FORK_EAR_X0, FORK_EAR_X1 = 1.1, 4.0     # clevis ear spans |x - cx| in [1.1, 4.0] around the fork slot
FORK_MOUNT_W = 7.5       # mount base half width
FORK_MOUNT_Z0, FORK_MOUNT_Z1 = 2.5, 12.0   # pad runs from Z0 up to Z1 along the slope
FORK_MOUNT_TOE = 1.5     # foot height of the mount pad
FORK_EAR_Y = (FORK_PIVOT_Y - FORK_BACK, FORK_PIVOT_Y + 3.5)
FORK_EAR_Z = (FORK_MOUNT_Z0, FORK_PIVOT_Z + 3.0)
FORK_SLOT_Y1 = FORK_EAR_Y[1] + 0.5
FORK_SLOT_Z = (FORK_MOUNT_Z0 + 1.0, FORK_EAR_Z[1] + 1.0)

SKID_X = 43.0
SK_DX = 1.8              # skid screws stagger across the skid so the pair spans >= 1/3 of the lever arm
SKID_TIP_Y = 52.0
SKID_TIP_Z = 0.2
SKID_HALF_W = SK_DX + 2.1 + 0.9        # staggered screws: head counterbore radius 2.1 and 0.9 mm of wall each side
SKID_Z0, SKID_Z1, SKID_Z2 = 6.0, 20.0, 4.0   # pad foot / top / heel heights along the slope
SKID_TOE_T = 1.5

GUARD_X0 = 48.0          # bolted flush to tub outer X = +/-48
GUARD_T = 3.0
GUARD_PROFILE = [(-39.0, 4.0), (-4.0, 4.0), (-4.0, 16.0), (-16.0, 22.0), (-32.0, 22.0), (-39.0, 14.0)]

# --- Overhead hammer-saw arm & weapon ---
ARM_PIVOT = [0.0, -28.0, 35.0]
ARM_TIP = [0.0, -16.0, 80.0]
ARM_HALF_T = 3.0
ARM_BASE_HALF_Y = 4.0
ARM_BASE_DZ = 1.5
ARM_MID_FRONT = (-30.0, 48.0)
ARM_MID_BACK = (-38.0, 52.0)
ARM_HEAD_R = 8.5
ARM_FILLET = 1.0
ARM_BORE_R = 2.6
DISC_OD = 44.0
DISC_R = DISC_OD / 2.0
DISC_T = 1.0
# GR1507 at arm tip: stator back at X=-10.4 -> WPN_MOTOR_AT X=13.40 puts stator back flush on arm X=3.00, bell cap at +6.7 -> X=20.10
WPN_MOTOR_AT = [13.40, -16.0, 80.0]
WPN_MOTOR_ROT = [0.0, 0.0, 0.0]
DISC_AT = [20.60, -16.0, 80.0]
DISC_ROT = [0.0, 90.0, 0.0]
STATOR_PCD_R = 6.0       # GR1507 M2 pattern: 12 mm PCD along +/-Y
DISC_PCD_R = 4.5         # disc M2 pattern: 9 mm PCD
DISC_HOLE_PHASE = -54.889   # degrees, matches the GR1507 top holes
DISC_FACE_X = DISC_AT[0] + DISC_T / 2
BELL_PIVOT = [DISC_AT[0] - DISC_T / 2 - 0.5, WPN_MOTOR_AT[1], WPN_MOTOR_AT[2]]   # on the spin axis, inside the bell cap

# Weapon shaft: GR1507 5 mm threaded steel shaft (29.1 mm total, 7.2 mm of M5 x 0.8 thread)
SHAFT_END_X = 18.70
SHAFT_LEN = 29.10
SHAFT_THREAD_LEN = 7.2
SHAFT_PITCH = 0.8
SHAFT_R = 2.5
SHAFT_THREAD_DEPTH = 0.43
SHAFT_CHAMFER = 0.4

# Disc teeth
DISC_TEETH = 4
DISC_ROOT_DEPTH = 4.5
DISC_TOOTH_ANGLES = (0.35, 1.05, 1.15)    # back, tip, gullet (rad from each tooth start)
DISC_FILLET = 0.3
DISC_BORE_R = 2.6
DISC_HOLE_R = 1.15

# Locking bar: spine stands off the arm face (clear of stator screw heads); pin plugs into an arm socket
LOCK_SPINE_T = 2.5
LOCK_SPINE_OFF = 2.5      # gap between arm face and spine (> M2 cap head height)
LOCK_SPINE_Y0 = ARM_TIP[1] - 16.5
LOCK_SPINE_Y1 = LOCK_SPINE_Y0 + 18.0
LOCK_SPINE_Z0 = ARM_TIP[2] - 20.5
LOCK_SPINE_H = 46.5
LOCK_X0 = -(ARM_HALF_T + LOCK_SPINE_OFF + LOCK_SPINE_T)    # outer face of the spine
LOCK_BAR_END_X = 23.0
LOCK_BAR_R = 1.5
LOCK_BAR_Z = ARM_TIP[2] + 24.5   # stop bar outside the disc rim (24.5 > 22 radius)
LOCK_PIN_R = 1.5
LOCK_PIN_DEPTH = 4.0      # engagement into arm (arm is 6 mm thick)
LOCK_PIN_Y = ARM_TIP[1] - 15.0
LOCK_PIN_Z = ARM_TIP[2] - 19.0
LOCK_WIN_Y = (LOCK_SPINE_Y0 + 4.0, LOCK_SPINE_Y1 - 3.0)     # spine window over the stator screws (driver access, lighter)
LOCK_WIN_Z = (LOCK_SPINE_Z0 + 6.0, LOCK_SPINE_Z0 + LOCK_SPINE_H - 6.5)
SOCKET_CLR = 0.1

# --- Fastener layout ---
PT_X, PT_Y_FRONT, PT_Y_REAR = 45.0, 5.5, -37.0     # top panel corner screws (>= 1.35 mm in from the edges)
SP_X, SP_Y = 15.0, 5.5                             # top spine screws (thread into the solid front-top of the tub)
WF_X = 32.0                                        # wedge screws at the slope mid-height
FM_Z, FM_DX = 11.5, 4.2                            # fork mount screws: height on the pad, offset either side of the fork
SK_Z = (19.0, 11.1)                                # skid screw heights on the pad (low one keeps its tap drill 0.9 mm off the tub underside)
GUARD_SCREWS = [(-36.5, 10.0), (-6.5, 13.5)]       # wheel guard screws (Y, Z), above/below the wheel well
SW_SCREW_Z = Z_TOP + 0.5                           # switch ear top
PAD_GRIP = PAD_T + WEDGE_T                         # pad plus wedge plate

# --- Spec data ---
TUB_SOLID, PANEL_SOLID = 0.55, 0.85       # printed solid fraction (infill + walls)
SHAFT_SOLID = 0.01
DISC_MIN_WEB = 0.75                        # GR1507 pattern web (mm); laser min web otherwise 0.75 x thickness
SHAFT_PRESS_MM, WHEEL_PRESS_MM = 0.05, 0.1
MASS_LIMIT_G, FOOTPRINT_LIMIT_MM = 150.0, 150.0
AWG_POWER, AWG_MOTOR, AWG_SIGNAL, AWG_PHASE = 20, 24, 26, 22
SLACK_SHORT, SLACK_LONG, SLACK_LOOP = 8, 10, 15

# Wire waypoints (mm): routing hints that keep each wire in the channels cut for it
WIRE_Y_WHEEL = -9.0                        # lane beside the wheel wells (>= 2 mm off the tyre, clear of the board edge)
WIRE_VIAS = {
    "w_bat_sw": [(0.0, 5.5, 18.0), (12.0, -14.0, 18.0)],
    "w_sw_mal": [(15.0, -17.5, 13.0), (19.5, -15.5, 13.0), (19.5, -4.5, 10.0)],
    "w_sw_wesc": [(15.0, -17.5, 13.0), (-19.5, -10.5, 10.0), (-36.5, WIRE_Y_WHEEL, 10.0), (-44.5, WIRE_Y_WHEEL, 8.0), (-44.5, -4.0, 8.0)],
    "w_mal_ml": [(45.0, 3.5, 8.0), (45.0, WIRE_Y_WHEEL, 11.0), (36.5, WIRE_Y_WHEEL, 11.0), (20.0, -16.0, 12.0), (-14.0, -16.0, 12.0), (-14.0, -22.0, 10.0)],
    "w_mal_mr": [(21.5, 3.5, 12.0), (21.5, -12.0, 12.0)],
    "w_mal_servo": [(36.5, WIRE_Y_WHEEL, 11.0), (21.0, -12.0, 11.0), (14.0, -15.8, 9.0), (2.0, -16.5, 6.5), (0.0, -24.0, 6.0)],
    "w_mal_wesc": [(45.0, -4.5, 8.0), (45.0, WIRE_Y_WHEEL, 11.0), (36.5, WIRE_Y_WHEEL, 11.0), (20.0, -15.5, 12.0), (-20.5, -15.5, 12.0),
                   (-20.5, -10.5, 10.0), (-36.5, WIRE_Y_WHEEL, 10.0), (-44.5, WIRE_Y_WHEEL, 8.0)],
    "w_wesc_wm": [(-19.0, -16.5, 12.0), (-19.0, -16.5, 26.5), (-4.0, -28.0, 35.0), (-4.0, -25.0, 58.0)],
}

# --- Colors (matching Disector reference photo) ---
COL_CHASSIS = "#1b7a43"      # green chassis
COL_TOP_PANEL = "#1f8a4c"    # green top panel
COL_TOP_SPINE = "#1e1e22"    # black top spine strap
COL_WEDGE = "#c8cdd2"        # silver aluminium front wedge
COL_ORANGE = "#f26522"       # orange fork mounts, skids, wheel guards
COL_FORK = "#1e7a56"         # dark green/metallic forks
COL_ARM = "#114d2e"          # dark green overhead arm
COL_DISC = "#0f4226"         # dark green saw disc
COL_LOCK = "#1e64d8"         # blue locking bar
COL_EYE_WHITE = "#f4f4f4"
