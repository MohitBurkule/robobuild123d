"""Limpet XXT masters and relations.

Frame: X forward (flipper end), Y left, Z up, arena floor at Z = 0, origin on the robot's centre line, mid wheelbase.

Only the MASTERS block holds typed numbers. Every one of them is tagged:
  RULE   - from the AWS antweight rules (known)
  CAT    - read from the repo catalogue (robot/catalog.py), never retyped
  STD    - fastener / material standard via robot/cad/fastener_catalog.py or robot/cad/bay.py
  PHOTO  - proportion SEEN-IN-PHOTO, converted to mm by a GUESS scale (see REFERENCE.md)
  GUESS  - not visible in any source; an engineering guess
Everything below the MASTERS block is a relation.
"""
import importlib.util
import math
import os

from robot import catalog
from robot.cad import bay as bay_lib
from robot.cad import fastener_catalog as fc

# ------------------------------------------------------------------------------------------------ reuse: revron hw
# robots/revron/src/revron/hw.py reads part sizes off the catalogue shapes. It has no package-relative imports, so it is
# loaded by path (importing the revron package would build the whole Revron rig).
_HW_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "revron", "src", "revron", "hw.py")
_spec = importlib.util.spec_from_file_location("revron_hw", os.path.abspath(_HW_PATH))
hw = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hw)

# =================================================================================================== MASTERS
RULE_ERA = "aws_2025"         # RULE: "aws_2025" = 150 mm floor square, no overhang at any height, no height limit
                              #       (repo draft PR #77); "aws_v4_3" = old 4 in (101.6 mm) start cube, any orientation
FOOTPRINT_SQUARE = 150.0      # RULE aws_2025
START_CUBE = 101.6            # RULE aws_v4_3 (the era most Limpet XXT versions were built in; this copy fits both)
MASS_LIMIT_G = 150.0          # RULE antweight, both eras

OVERALL_L = 99.0              # PHOTO/GUESS: flipper tip (rest) to rear of side plate; rest pose under START_CUBE too
OVERALL_W = 96.0              # PHOTO/GUESS: outside face to outside face of the two side plates
FLIPPER_SHARE = 0.305         # PHOTO: flipper plan run / OVERALL_L (aws71, aws74, aws76 three-quarter views)

DRIVE_MOTOR_ID = "n10_300rpm_6v"     # GUESS (CAT entry): four small micro-metal gearmotors, one per wheel
SERVO_ID = "servo_cs07"              # GUESS (CAT entry): SG90-class flipper servo
BATTERY_ID = "lipo_2s_180"           # GUESS (CAT entry): 2S pack, sits in the centre channel (V3.1 photo)
ESC_ID = "malenki_nano"              # GUESS (CAT entry): Rx + dual brushed ESC, the usual UK ant board
SWITCH_ID = "switch_bbb_ant_rvrn2"   # GUESS (CAT entry): screw-on ant switch, removable link per rules

WHEEL_D = 24.0                # PHOTO/GUESS: tyre OD; tyre stands proud of tub top and bottom (invertible)
WHEEL_W = 8.0                 # PHOTO/GUESS: tyre width
WHEEL_PROUD = 1.5             # GUESS: tyre proud of tub top / bottom face (the robot runs either way up)

SHEET_T = 2.0                 # PHOTO/GUESS: clear polycarbonate side plates and flipper (decal on the back face)
LID_T = 1.5                   # PHOTO/GUESS: clear polycarbonate lid plates
WALL = bay_lib.DEFAULT_WALL   # STD: printed tub wall (4 perimeters)
CLEAR = bay_lib.PRINTED_FIT_CLEARANCE   # STD: printed fit clearance per side
RUN_CLEAR = bay_lib.RUNNING_CLEARANCE   # STD: wheel to anything that does not turn with it

PLATE_CHAMFER_FRAC = 0.5      # PHOTO: side-plate corner chamfer as a share of the wheel radius (hexagonal outline)
FLIP_CHAMFER_FRAC = 0.12      # PHOTO: flipper front-corner chamfer as a share of the flipper width
FLIP_SIDE_GAP = 1.0           # GUESS: flipper edge to side plate (it swings between the plates)
FLIP_OPEN_DEG = 42.0          # GUESS: usable flipper travel; the tail would graze the servo tray beyond ~45 deg
FLIP_TIP_LIFT = 2.6           # GUESS: flipper tip height above the floor at rest (stays above the wheel contacts)

SCREW_D = 2.0                 # STD: M2 throughout (photos show small button / torx heads)
SCREW_HEAD = "button"         # PHOTO: domed heads on side plates and lids

PRINT_MAT = "pla"             # PHOTO: dark green / white printed tub (V3.x onward)
SHEET_MAT = "pc"              # PHOTO: clear sheet with zebra decals

# ================================================================================================= RELATIONS
# --- catalogue sizes (never retyped)
MOTOR_SHAFT = catalog.find(DRIVE_MOTOR_ID).shaft          # {"at", "dir", "len", "dia"}
_, MOTOR_W, MOTOR_H = hw.size(DRIVE_MOTOR_ID)               # catalogue frame: x along the shaft
MOTOR_L = MOTOR_SHAFT["at"][0] - hw.reach(DRIVE_MOTOR_ID)["x0"]   # body only: back face to shaft root
MOTOR_ENV_X = 5.0             # CAT: motor envelope half-width in robot X (= catalogue Y half)
MOTOR_ENV_Z = 6.0             # CAT: motor envelope half-height in robot Z (= catalogue Z half)
MOTOR_FIT = 0.05              # GUESS: snug printed pocket per side (captures the motor; slides in axially)
SERVO_L, SERVO_W, SERVO_H = hw.size(SERVO_ID)
BAT_L, BAT_W, BAT_H = hw.size(BATTERY_ID)
ESC_L, ESC_W, ESC_H = hw.size(ESC_ID)
SERVO_HOLES = catalog.find(SERVO_ID).props["mount_holes_mm"]

# real servo solid extent (mount tabs stand proud of the nominal frame sizes)
SERVO_BB = hw._solid(SERVO_ID).bounding_box()
SERVO_LEN = SERVO_BB.max.X - SERVO_BB.min.X
SERVO_X_OFF = (SERVO_BB.min.X + SERVO_BB.max.X) / 2
SERVO_FACE_Y = SERVO_BB.max.Z                               # world +Y face of the lying servo (catalog +Z)
SERVO_DROP = max(0.0, SERVO_BB.max.Y - SERVO_W / 2)         # solid hangs below the nominal centre line
SERVO_RISE = max(0.0, -SERVO_BB.min.Y - SERVO_W / 2)        # ... and stands above it

SCREW_CLEAR_D = fc.clearance(SCREW_D)
SCREW_TAP_D = fc.tap_drill(SCREW_D)
INSERT_OD, INSERT_L = fc.insert(SCREW_D)
HEAD_D, HEAD_H = fc.head(SCREW_D, SCREW_HEAD)

# --- heights: the tub sits inside the tyre envelope, proud of neither face -> runs inverted
AXLE_Z = WHEEL_D / 2
TUB_Z0 = WHEEL_PROUD
TUB_H = WHEEL_D - 2 * WHEEL_PROUD - LID_T                  # lid top flush with TUB_Z0 + (WHEEL_D - 2 * WHEEL_PROUD)
TUB_Z1 = TUB_Z0 + TUB_H
LID_Z1 = TUB_Z1 + LID_T

# --- widths: side plate | wheel well | tub | wheel well | side plate
SIDE_Y = OVERALL_W / 2 - SHEET_T / 2                       # side plate mid-plane
WHEEL_Y = OVERALL_W / 2 - SHEET_T - RUN_CLEAR - WHEEL_W / 2
TUB_W = 2 * (WHEEL_Y - WHEEL_W / 2 - RUN_CLEAR)
SPACER_L = SIDE_Y - SHEET_T / 2 - TUB_W / 2                # standoff boss from tub wall to side plate

# --- lengths: flipper run is a photo share of the overall length; the rest is body
FLIP_RUN = OVERALL_L * FLIPPER_SHARE
BODY_L = OVERALL_L - FLIP_RUN                              # side plate length
TUB_L = BODY_L                                             # tub front wall carries the hinge, flush with the plates
BODY_X0 = -OVERALL_L / 2                                   # rear face
BODY_X1 = BODY_X0 + BODY_L                                 # front face
TUB_XC = (BODY_X0 + BODY_X1) / 2
AXLE_DX = BODY_L / 2 - WHEEL_D / 2 - RUN_CLEAR - WALL     # wheel just inside the end bulkhead
AXLES_X = (TUB_XC + AXLE_DX, TUB_XC - AXLE_DX)            # front, rear

# --- side plate hexagon: chamfers relate to the wheel radius
PLATE_H = WHEEL_D - 2 * WHEEL_PROUD                        # plate edges sit inside the tyre: tyres touch first
PLATE_CHAMFER = WHEEL_D / 2 * PLATE_CHAMFER_FRAC
PLATE_Z0 = TUB_Z0

# --- flipper hinge: outboard of the front wall face so the M2 pin clears the wall top with no groove
HINGE_PIN_D = SCREW_D                                      # M2 screw as hinge pin
HINGE_BOSS_D = HINGE_PIN_D + 2 * WALL
HINGE_X = BODY_X1 + HINGE_PIN_D / 2 + 1.5                    # outboard of the wall face so the pin clears it and the block seat clears the servo tray
HINGE_Z = LID_Z1 - SHEET_T / 2
LID_X1 = HINGE_X - HINGE_BOSS_D / 2 - 0.3                  # lids stop clear of the hinge knuckles
FLIP_DROP = HINGE_Z - FLIP_TIP_LIFT
FLIP_LEN = math.hypot(FLIP_RUN, FLIP_DROP)
FLIP_REST_DEG = math.degrees(math.atan2(FLIP_DROP, FLIP_RUN))   # below horizontal, derived (photo shows ~35-45)
REST_L = (HINGE_X + FLIP_RUN) - BODY_X0                           # start-pose length, flipper tip (rest) to rear face
FLIP_W = 2 * (SIDE_Y - SHEET_T / 2 - FLIP_SIDE_GAP)
FLIP_CHAMFER = FLIP_W * FLIP_CHAMFER_FRAC
HINGE_KNUCKLES = 3                                          # PHOTO: tub/flipper/tub hinge read as alternate knuckles
BLOCK_KNUCKLE_W = 22.0                                      # GUESS: centre knuckle; leaves a 4 mm gap to the tub knuckles
TUB_KNUCKLE_W = FLIP_W / HINGE_KNUCKLES                     # outer knuckles, one per flipper edge
TUB_KNUCKLE_Y = BLOCK_KNUCKLE_W / 2 + 4.0 + TUB_KNUCKLE_W / 2   # centre of each outer knuckle (inner face 4 mm from the block)

# --- inside the tub: four motor pockets at the axles, centre channel = servo (front) + battery (rear)
MOTOR_ROOT_Y = TUB_W / 2                                  # gearbox face flush with the outer wall face (pocket runs through)
MOTOR_INNER_Y = MOTOR_ROOT_Y - MOTOR_L                      # inboard end of the motor body
CHANNEL_HALF_W = MOTOR_INNER_Y - WALL                       # centre channel between the two motors of an axle
SERVO_X = BODY_X1 - WALL - CLEAR - SERVO_L / 2             # servo on its side against the front wall, output axis along Y
BAT_X = BODY_X0 + WALL + CLEAR + BAT_L / 2                  # battery against the rear wall (long black block, V3.1)
ESC_X = -16.0                                               # ESC in the left side zone, between the motor pockets
SW_X = -16.0                                                # switch in the right side zone (clear of the motor pockets)
SIDE_ZONE_Y = (CHANNEL_HALF_W + TUB_W / 2 - WALL / 2) / 2

# --- servo tray: printed U-channel around the servo (open top so the servo drops in / lifts out), horn slot in +Y wall
TRAY_WALL = WALL                                            # tray wall thickness round the servo cavity
TRAY_LIP = 1.05                                             # tray wall height above the servo top face
TRAY_TOP_Z = TUB_Z0 + WALL + SERVO_W + SERVO_DROP + SERVO_RISE + TRAY_LIP   # tray top (tail clears it over the whole flip range)
TRAY_HALF_Y = CHANNEL_HALF_W - 0.3
CAV_FIT = MOTOR_FIT                                         # switch tray cavity clearance per side
SERVO_CAV_FIT = 0.2                                         # servo cavity clearance per side (catalog tabs stand proud)
HORN_SLOT_X0, HORN_SLOT_X1 = 2.0, 16.0                     # horn swing window in the tray's +Y wall
HORN_SLOT_Z0 = 5.0                                          # clears the horn hub bottom
HORN_SLOT_MARGIN = 0.35                                     # slot overshoot past the tray wall in Y
LEAD_SLOT_HALF_Y = 4.0                                      # servo lead slot in the tray's -X wall
LEAD_SLOT_Z0, LEAD_SLOT_Z1 = 7.5, 11.0

# --- motor pockets: snug (MOTOR_FIT per side), closed top, through the outer wall
POCKET_OUT = 0.1                                            # pocket overshoot past the wall outer face
SHAFT_HOLE_IN = 0.75                                        # shaft hole reach into the cavity
SHAFT_HOLE_OUT = 1.5                                        # shaft hole reach past the wall face into the wheel well
SHAFT_HOLE_FIT = 0.05
BORE_FLAT_Z = 1.0                                           # CAT: N10 D-flat chord height (shaft box z <= +1.0)
BORE_FLAT_W = 3.6                                           # wheel D-bore flat width
BORE_R = MOTOR_SHAFT["dia"] / 2 + CLEAR / 3                 # wheel bore radius (slides on the shaft)

# --- hinge relief: the front wall's top corner is notched away over the whole hinge-block swing envelope
# (the tail's lower edge sweeps down to z ~19 mm over the wall band at full lift; the notch bottom clears the
# servo tray top by a full printable wall)
RELIEF_X0 = TUB_XC + TUB_L / 2 - WALL - 0.7                 # notch starts inboard of the wall inner face
RELIEF_X1 = TUB_XC + TUB_L / 2 + 0.7                         # notch ends outboard of the wall outer face
RELIEF_HALF_Y = (BLOCK_KNUCKLE_W - 2 * CLEAR) / 2 + 2.3      # clears the block knuckle (±10.7) with margin
RELIEF_Z0 = TRAY_TOP_Z + 0.95                                # notch bottom: >= 0.9 mm of wall above the tray top
LOAD_DIST = 3.5                                             # sharp_corner load zone is 3 mm around fasteners; + margin

# --- flipper drive: the hinge block's tail lever runs back along the centre channel; the servo horn's drive pin
# bears on the tail's end face. The pin sits radially beyond the tail end, in the tail's angular shadow, so the
# swept tail band never reaches it.
SERVO_OUT_DX = (SERVO_LEN - SERVO_W) / 2                    # GUESS relation: output one half-width in from the front end
SERVO_OUT_X = SERVO_X + SERVO_OUT_DX
SERVO_OUT_Z = TUB_Z0 + WALL + SERVO_W / 2 + SERVO_DROP + 0.05   # lying on its side: catalogue y (width) is now Z
HORN_HALF_Y = 0.7                                           # horn plate half-thickness in Y
HORN_Y = SERVO_FACE_Y + 0.2 + HORN_HALF_Y                   # horn mid-plane, outboard of the servo face, in the channel
TAIL_L = 14.0                                               # tail length; at full lift its bottom edge clears the servo top
TAIL_W = HINGE_BOSS_D                                       # tail as wide as the hinge boss
TAIL_H = HINGE_BOSS_D
PIN_LEVER = TAIL_L + HINGE_PIN_D / 2 + 0.3                  # pin axis radius from the hinge (beyond the tail end face)
HORN_ARM_W = 4.0                                            # horn arm width (z in the horn frame)
HORN_TAB = (6.0, 4.5)                                       # tab plate (x, z) centred on the pin
HORN_PIN_BORE_R = 1.05                                      # drive pin through-bore in the tab
HORN_MAX_DEG = 20.0                                         # servo travel; negative = lift (pin swings AWAY from the tail)
HORN_MIN_DEG = -HORN_MAX_DEG


def _rot_y(deg, x, z):
    """Rotate the XZ point (x, z) about +Y by deg (build123d Rot(0, deg, 0) convention)."""
    a = math.radians(deg)
    return (x * math.cos(a) + z * math.sin(a), -x * math.sin(a) + z * math.cos(a))


def hinge_point(x, z, flip_deg=0.0):
    """World XZ of a hinge-frame point (x, 0, z) at flipper angle `flip_deg` (0 = rest)."""
    rx, rz = _rot_y(FLIP_REST_DEG - flip_deg, x, z)
    return (HINGE_X + rx, HINGE_Z + rz)


# drive pin world position at rest: on the tail centre line, PIN_LEVER from the hinge
PIN_X, PIN_Z = hinge_point(-PIN_LEVER, 0.0)
# horn reach / rest angle from the servo output to the pin (XZ plane)
HORN_R = math.hypot(PIN_X - SERVO_OUT_X, PIN_Z - SERVO_OUT_Z)
HORN_THETA0 = math.degrees(math.atan2(-(PIN_Z - SERVO_OUT_Z), PIN_X - SERVO_OUT_X))

# --- side-plate fixing: two standoff columns in the clear span between the tyres, two screws per column
WHEEL_GAP_X = (AXLES_X[0] - AXLES_X[1]) - WHEEL_D - 2 * RUN_CLEAR   # clear span between front and rear tyres
STANDOFF_D = min(WHEEL_GAP_X / 2 - RUN_CLEAR, INSERT_OD + 2 * WALL)
STANDOFF_XS = (TUB_XC - WHEEL_GAP_X / 4, TUB_XC + WHEEL_GAP_X / 4)  # two columns inside the clear span
PLATE_SCREWS_Z = (AXLE_Z - PLATE_H / 4, AXLE_Z + PLATE_H / 4)

# --- lid fixing: wall-thickening pads with M2 heat-sets (no separate bosses); the pad bottom seam stays
# >= 3 mm below the bolt tip so the sharp corner sits outside the fastener load zone
# pad X positions sit in the free zones: rear of the rear motor pocket, and between the front pocket and the hinge
LID_SCREW_INSET = 4.0                                       # screw centre inset from the tub outer wall face
LID_PAD_Y = 32.0                                            # pad centre |y| (inside the wall, clear of the ESC / switch)
LID_PAD_D = 7.0                                             # pad size along Y
LID_PAD_H = 8.0                                             # pad hangs this far down from the wall top (bottom seam >= 3 mm below the M2x6 bolt tip)
LID_PAD_BORE_FLOOR = 2.2                                    # blind insert bore leaves this floor under the pad (mouth fillet eats 1 mm)
LID_PADS = ((-45.5, 7.5), (13.9, 8.0))                      # (screw X, pad width X): rear pad merges into the rear wall corner; front pad +x face buries 0.2 past the cavity front face so the seam fillet can't collide with the cavity corner fillet
LID_SCREWS_X_L = tuple(x for x, _w in LID_PADS)             # left lid: clear of the ESC footprint (ESC slides out +z)
LID_SCREWS_X_R = tuple(x for x, _w in LID_PADS)             # right lid: clear of the switch tray and the lid slot
LID_SLOT_R = 0.5                                            # corner radius on the switch slot in the right lid (>= laser kerf)

# --- hinge block seat: thick enough for M2x8 self-tap engagement >= 2.5 d in printed plastic
SEAT_H = 10.0
SEAT_X0 = 5.5                                                # seat's low corner clears the tub front wall at rest; the web fuses it to the knuckle
SEAT_L = 10.0                                               # seat length along the hinge frame
SEAT_TOP_FILLET_R = 1.0                                     # seat top rim / insert-bore mouth fillet (bolt load zone needs r >= 1)
SEAT_HOLE_D = INSERT_OD - CLEAR                             # insert bore through the seat (heat-set pressed in)
SEAT_W = BLOCK_KNUCKLE_W - 2 * CLEAR + 2.0                  # seat width along Y (a little wider than the knuckle)
HINGE_BOLT_Y = 7.0                                          # flipper-seat screw axis |Y| in the hinge frame
BOLT_HB_X = SEAT_X0 + SEAT_L / 2                             # flipper-seat screw axis X in the hinge frame (seat centre)
SEAT_WEB_X0 = 0.5                                           # web fusing knuckle to seat: x range, at the seat's top rim
SEAT_WEB_X1 = SEAT_X0 + 0.5                                 # web reaches this far outboard (overlaps the seat face)
SEAT_WEB_H = 1.6                                            # web height (z from -SHEET_T-SEAT_WEB_H to -SHEET_T)
SEAT_WEB_FILLET_R = 1.0                                     # web seam fillet radius (hinge load zone needs r >= 1)
SEAM_DZ = 0.9                                               # seam-edge filter: z window below the seat top rim
SEAM_DZ_TOP = 0.1                                           # seam-edge filter: z window above the seat top rim
KNUCKLE_RIM_FILLET_R = 0.6                                  # knuckle OUTER rim fillet (never the bore rim)
RIM_TOL = 0.05                                              # edge-plane match tolerance for rim filters
SELECT_TOL = 0.1                                            # edge-selector box slack around a feature's nominal extent
BORE_GUARD = 0.2                                            # rim filter keeps only edges this far outside the bore radius
KNUCKLE_BORE_R = HINGE_PIN_D / 2 + 0.3                       # block knuckle bore (running fit on the pin)
PIN_TUB_BORE_R = HINGE_PIN_D / 2 - 0.15                      # tub knuckle bore (press fit on the pin)
PLATE_HOLE_D = SCREW_CLEAR_D + 0.4                           # side-plate clearance holes
PIN_Y0 = -TAIL_W / 2 - 0.9 - HORN_Y                          # drive pin inner end, horn frame
PIN_Y1 = HORN_HALF_Y                                         # drive pin outer end, horn frame

# --- start pose: flipper at rest. A raised flipper is post-start motion, modelled as the flipper joint angle; it only
# grows the height, which neither era's plan-view check counts against (v4.3 allowed expansion after the start).
START_FLIP_DEG = 0.0                                        # 0 = rest (wedge on the floor); FLIP_OPEN_DEG = fully up


def check():
    """Rule / packaging relations to assert before trusting a build."""
    problems = []
    if RULE_ERA == "aws_2025" and max(OVERALL_L, OVERALL_W) > FOOTPRINT_SQUARE:
        problems.append("plan view leaves the 150 mm floor square (no overhang allowed at any height)")
    if RULE_ERA == "aws_v4_3" and REST_L > START_CUBE + 0.01:
        problems.append("start pose leaves the 101.6 mm cube")
    if 2 * CHANNEL_HALF_W < max(SERVO_H, BAT_W) + 2 * CLEAR:
        problems.append("centre channel narrower than servo/battery")
    if MOTOR_SHAFT["len"] < RUN_CLEAR + WHEEL_W:
        problems.append("motor shaft too short to reach across the gap and through the wheel")
    if BAT_X + BAT_L / 2 + CLEAR > SERVO_X - SERVO_L / 2 - CLEAR:
        problems.append("battery and servo overlap in the centre channel")
    if WHEEL_GAP_X < INSERT_OD + 2 * WALL:
        problems.append("standoff column wider than the gap between the tyres")
    if SPACER_L <= 0:
        problems.append("no room for side-plate standoffs")
    if LID_X1 >= HINGE_X - HINGE_BOSS_D / 2:
        problems.append("lids reach the hinge knuckles")
    servo_top = SERVO_OUT_Z - SERVO_BB.min.Y
    for f in (0.0, FLIP_OPEN_DEG):
        _, tip_z = hinge_point(-TAIL_L, -TAIL_H / 2, f)
        if tip_z < servo_top + RUN_CLEAR:
            problems.append(f"tail bottom edge dips to {tip_z:.2f} mm at flip {f:.0f} deg, grazing the servo top {servo_top:.2f}")
    if PIN_LEVER < TAIL_L + HINGE_PIN_D / 2 + 0.2:
        problems.append("drive pin not beyond the tail end face")
    for d in (0.0, HORN_MIN_DEG):
        px, pz = _rot_y(HORN_THETA0 + d, HORN_R, 0.0)
        wx, wz = SERVO_OUT_X + px, SERVO_OUT_Z + pz
        if math.hypot(wx - HINGE_X, wz - HINGE_Z) < TAIL_L + HINGE_PIN_D / 2 + 0.2:
            problems.append(f"drive pin sweeps into the tail band at horn angle {d:.0f} deg")
    return problems
