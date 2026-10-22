"""Revron params: masters, chassis layout, panels, lug blend (RV01 / RV26 / Ti top). Re-exported by params.py."""
import json, math, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from .variants import variant   # tub deviations (open_keyhole, pad_preload) are opt-in switches, see variants.py
from . import hw
from robot.cad import fastener_catalog as fc   # standard fastener / insert dimensions
from robot.world import csk_dims

# ======================================================================================================================
# Measured layout (RVRN 2.0 STEP, world frame). Each number is a dimension of a feature, not a mesh coordinate list.
# ======================================================================================================================
# ---- MASTER DESIGN PARAMETERS (everything below is constrained to these, or is a catalog / measured organic value) ----
CH_HALF_W = 29.5                     # chassis outer half-width |X| (outer side-wall face)
CH_Y0, CH_Y1_STOCK = -37.6, 15.0     # chassis rear face / stock front face; CH_Y1 (below) = the front face, which a longer pack pushes forward
CH_Z0, CH_Z1 = 2.5, 19.5             # chassis floor underside / rim (top panel and mount notch sit on it)
CH_WALL = 2.0                        # printed wall and deck thickness
WY, WZ = 38.5, 23.5                  # weapon axis (along X)
# drive location (hook drive.location): the drive axle line Y per declared location; the tub's motor features (keyhole, key tab, stop wall, pad recess)
# and the pack bay follow RY (the pack butts the stop wall); the rear-only structure (rear boss, lattice window) does not move with it
DRIVE_LOCATION = os.environ.get("REVRON_DRIVE_LOCATION", "rear")
DRIVE_LOCATIONS = {"rear": dict(ry=-30.5), "mid": dict(ry=-8.0), "front": dict(ry=5.0)}
RY, RZ = DRIVE_LOCATIONS[DRIVE_LOCATION]["ry"], 11.0   # N10 shaft (rear axle at the default location)
WHEEL_OD_F = 11.0                    # front wheel outer diameter (RV20 Scalextric micro tyre): the front axle stands at its radius, the nose follows
SO_R = 2.5                           # standoff radius
SA_Y, SA_Z = 30.5, WHEEL_OD_F / 2    # front axle (Y, Z): axle height = wheel radius
SA = (SA_Y, SA_Z)                    # 25 mm standoff (RV11): front axle (Y, Z)
SB_DROP, SB_WHEEL_CLR = 1.0, 0.5     # nose standoff axis this far under the axle line (STEP 5.5 -> 4.5); its surface this clear of the front tyre
SB_Y = max(40.5, round(SA_Y + math.sqrt((WHEEL_OD_F / 2 + SO_R + SB_WHEEL_CLR) ** 2 - SB_DROP ** 2), 6))   # nose Y: at least the STEP's 40.5, and never nearer the front wheel than its radius + the standoff radius + a clearance
SB = (SB_Y, WHEEL_OD_F / 2 - SB_DROP)   # 15 mm standoff (RV10): nose (Y, Z)
# the rotor axis keeps at least its distance (WY, WZ master and the STEP's standoff positions) from each mount-screw axis: the heads back out inboard
# past the disc, so when SA / SB rise (or close in) the rotor rises with them; at the STEP standoffs this changes nothing
_STEP_SCREW_AXES = ((30.5, 5.5), (40.5, 4.5))
_REACH = [math.hypot(WY - y, WZ - z) for y, z in _STEP_SCREW_AXES]
WZ = max(WZ, *[round(p[1] + math.sqrt(r ** 2 - (WY - p[0]) ** 2), 6) for p, r in zip((SA, SB), _REACH) if r > abs(WY - p[0])])
SA_LEN, SB_LEN = 25.0, 15.0          # catalog standoff lengths
SA_X0, SB_X0 = 17.5, 21.5            # |X| of each standoff's inner end
M2, M3 = 2.0, 3.0                    # thread diameters of the screws the tub is drilled for
M3_THIN_NUT_T = fc.nut(M3, 'thin')[1]   # thin M3 nut thickness (ISO 4035)
MNT_IN, MNT_T, MNT_SLAB_T = 13.4, 8.0, 4.0   # weapon mount: inner face |X|, total thickness, slab thickness (rest = battered boss)
FLOOR_Z = 1.0                        # ground-contact plane of the ramps / side feet
# ---------------------------------------------------------------------------------------------------------------------
CH_IN_X = CH_HALF_W - CH_WALL        # inner face of the side walls (27.5)
REF_TO_WORLD = [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
SA_X, SB_X = (SA_X0, SA_X0 + SA_LEN), (SB_X0, SB_X0 + SB_LEN)   # standoff |X| spans: inner end + catalog length
NUT = (-11.5, 8.5)                   # side-panel screw into a thin M3 nut in the chassis wall (Y, Z)
NUT_X = (CH_HALF_W - M3_THIN_NUT_T, CH_HALF_W)   # nut pocket opens on the outer wall face, one nut deep
# ---- insert columns: a 2 x 2 grid plus the rear-centre boss, placed against what sits in the tub ----------------------------------------
INSERT_CAT = "heatset_m2_4"          # FS1 M2 heat-set, brass, 3.5 OD x 4
INSERT_OD, INS_LEN = hw.size(INSERT_CAT)[1:]   # knurled OD and length from the catalog
BORE_CH = 0.6                        # chamfer of the heat-set bore at the panel seat and at the rim
KNURL = 0.25                         # FS1 M2 heat-set: knurl depth
BORE_R = INSERT_OD / 2 - KNURL       # heat-set bore = the insert's core (the knurl melts in)
KEEP_R = BORE_R + CH_WALL / 4        # the bore and half a skin of plastic round it: the sleeve no part may notch, so no part may stand in it either
SLEEVE_CLR = 0.2                     # a part stands this clear of a bore sleeve
COL_R = 2.75                         # insert column boss radius (corner blocks, rear boss and deck pockets are tangent to it)
WALL_IN_REAR = CH_Y0 + CH_WALL       # inner face of the rear wall (Y)
DRIVE_MOTOR = os.environ.get("REVRON_DRIVE_MOTOR", "n10_2200rpm_spicy")    # catalog id of the drive gearmotors (RV12): the tub is dimensioned from its plate stack
GB = hw.gearbox(DRIVE_MOTOR)         # plate stack in the motor frame: top, half_w, end, gaps
MOTOR_WALL_GAP = 0.3                 # last gearbox plate to the chassis wall's inner face
MOTX = round(CH_IN_X - MOTOR_WALL_GAP - GB["end"], 6)   # N10 catalog origin |X|: the stack ends a gap short of the wall
KEY_CLR = 0.15                       # chassis key tab to each gearbox plate
N10_KEY = tuple(round(MOTX + g + s * KEY_CLR, 6) for g, s in zip(GB["gaps"][-1], (1, -1))) if GB["gaps"] else None   # |X| of the key tab: the open span between the stack's last two plates less the clearance; none when the gearbox has no such gap
KEY_BITE, STOP_CLR = 0.65, 0.1       # key tab reaches this far behind the gearbox front face; the stop wall stands this clear of it
KEY_SPAN = (round(RY + GB["half_w"] - KEY_BITE, 6), round(RY + GB["half_w"] + STOP_CLR + CH_WALL, 6))   # Y span of the key tab / stop wall
MOT = hw.reach(DRIVE_MOTOR)          # the gearmotor's catalog envelope in its own frame (x0..x1 along the shaft, y0..y1 across)
MOT_X, MOT_Y = (MOTX + MOT["x0"], MOTX + MOT["x1"]), (RY + MOT["y0"], RY + MOT["y1"])   # the +X motor's |X| and Y spans in the tub (the -X motor is its mirror)
BATTERY = os.environ.get("REVRON_BATTERY", "lipo_2s_180_turnabot")      # RV16 pack, catalog id
BAT_LEN = hw.size(BATTERY)[0]        # pack length: in the bay it runs along Y, butting the stop wall
TAB_FRONT_SETBACK = fc.head(3.0, 'csk')[0] / 2 + CH_WALL / 2   # tab front face stands short of the axle standoff axis (SA) by the M3 CSK head radius plus a skin: the mount screw into SA clears the tab
PACK_FRONT_GAP = 0.2                 # pack front face to the front wall's inner face
CH_Y1_MAX = SA[0] - TAB_FRONT_SETBACK - CH_WALL   # the front wall can come this far forward and still leave the weapon-mount tab one wall to stand on
CH_Y1 = max(CH_Y1_STOCK, min(CH_Y1_MAX, round(KEY_SPAN[1] + BAT_LEN + PACK_FRONT_GAP + CH_WALL, 6)))   # front face: the stock 15.0 unless the pack (against the stop wall) is longer than it holds
INS_PITCH_Y, INS_EDGE = 32.0, (2.5, 2.6)   # stock grid pitch along Y; column centre to the side wall inner face / to the front wall inner face
INS_X = CH_IN_X - INS_EDGE[0]        # column |X|
ROW_FRONT = CH_Y1 - CH_WALL - INS_EDGE[1]                          # front row Y (follows the front wall)
ROW_REAR = CH_Y1_STOCK - CH_WALL - INS_EDGE[1] - INS_PITCH_Y       # rear row Y (stays when the front wall moves forward)


def _clear_of_motor(y, lo, hi):
    """Row Y moved out of the gearmotor's Y span (plus a bore sleeve and its clearance each side) when the motor's X span covers the column: to the nearer free side within lo..hi."""
    pad = KEEP_R + SLEEVE_CLR
    if not (MOT_X[0] - pad < INS_X < MOT_X[1] + pad and MOT_Y[0] - pad < y < MOT_Y[1] + pad):
        return y
    free = [v for v in (MOT_Y[0] - pad, MOT_Y[1] + pad) if lo <= v <= hi]
    return min(free, key=lambda v: abs(v - y)) if free else y


_front = round(_clear_of_motor(ROW_FRONT, ROW_REAR + 2 * COL_R, ROW_FRONT), 6)
_rear = round(_clear_of_motor(ROW_REAR, WALL_IN_REAR + COL_R, _front - 2 * COL_R), 6)
INS_COLS = tuple((sx * INS_X, y) for y in (_front, _rear) for sx in (-1, 1))
# rear-centre boss: one wall in front of the rear inner face, unless the gearmotor's stack reaches the boss's bore sleeve (it ends short of the
# axis, or crosses it): then the boss moves out in front of the motor, a sleeve + clearance clear of it, and stands free of the rear wall
BOSS_REAR_Y = CH_Y0 + 2 * CH_WALL
BOSS_AT_REAR = not (MOT_X[0] < KEEP_R + SLEEVE_CLR and MOT_Y[0] - KEEP_R - SLEEVE_CLR < BOSS_REAR_Y < MOT_Y[1] + KEEP_R + SLEEVE_CLR)
BOSS_Y = BOSS_REAR_Y if BOSS_AT_REAR else round(MOT_Y[1] + KEEP_R + SLEEVE_CLR, 6)
INS = [*INS_COLS, (0.0, BOSS_Y)]   # 5 floor inserts / base screws
# electronics envelopes (catalog boxes at their spec placement, rot z 90): Malenki nano 32 x 20 x 4.4 at (8.67, -3.0, 15.3),
# BBB ant ESC 23.5 x 12 x 5 at (8.63, -7.25, 10.6); the deck cage ribs are dimensioned off these
RXESC = os.environ.get("REVRON_RXESC", "malenki_nano_rvrn2")   # receiver / drive ESC catalog id
RX_SIZE, RX_C = hw.size(RXESC), (8.67, -3.0, 15.3)     # receiver catalog box (L, W, H) (32 x 20 x 4.4 at the default) and placed centre
WESC = os.environ.get("REVRON_WESC", "bbb_ant_esc_rvrn2")   # weapon ESC catalog id
WE_SIZE, WE_C = hw.size(WESC), (8.63, -7.25, 10.6)     # weapon ESC catalog box (23.5 x 12 x 5 at the default) and placed centre


def _env(c, size):
    """(X, Y, Z) spans of a catalog box rotated 90 deg about Z (length along Y) centred on c."""
    w, l, h = size[1], size[0], size[2]
    return tuple((ci - d / 2, ci + d / 2) for ci, d in zip(c, (w, l, h)))


(RX_X, RX_Y, RX_Z), (WE_X, WE_Y, WE_Z) = _env(RX_C, RX_SIZE), _env(WE_C, WE_SIZE)
# declared compartment layout (hook chassis.compartments): the interior compartments the tub carves, by name. motor = the pocket for the gearmotor body
# and the stop wall / key tab / ledge that locate it; battery = the bay cut from the pack's catalog envelope; partition = the rib splitting the pack bay
# from the electronics bay beside it
COMPARTMENT = os.environ.get("REVRON_COMPARTMENTS", "standard")
COMPARTMENTS = {"standard": ("motor", "battery"), "none": (), "split_battery_bay": ("motor", "battery", "partition")}
LAYOUT = COMPARTMENTS[COMPARTMENT]
N10_TOP = round(RZ + GB["top"], 6)   # top face of the N10 gearbox plates
# chassis RV01
SW_HALF_W, SW_CLR = 2.9, 0.05   # power switch body half-width, its clearance to the inner wall face
SW_HALF, SW_WALL_CLEAR = SW_HALF_W, SW_CLR   # fix-joints names (switch joint in joints.py)
SWX = CH_IN_X - SW_CLR - SW_HALF_W   # power switch X: body side 0.05 clear of the 27.5 inner wall face (was 25.0, 0.4 into it)
CH = dict(x=CH_HALF_W, y0=CH_Y0, y1=CH_Y1, z0=CH_Z0, z1=CH_Z1, wall=CH_WALL, deck=CH_Z1 - CH_WALL, cham=CH_WALL)
# drisk

# ====================================================================================================================
# Parts
# ====================================================================================================================
# panels (RV26 base, Ti top) [fix-T: named params, every panel dimension derives from these]
SEG, SEG_FINE = 64, 128              # shapely buffer resolution (segments per quarter circle) for ears / tangent arcs
BASE_HEAD_DK = csk_dims(M2)[0]       # modelled M2 CSK head diameter (robot.world.csk_dims: 2.2 d = 4.4, 90 deg, 1.2 deep)
BASE_CSK_SEAT_CLR = 0.1              # diametral clearance between that head and the seat cone
BASE_CSK_CLEAR = BASE_HEAD_DK + BASE_CSK_SEAT_CLR - fc.head(M2, 'csk')[0]   # hole_tool's csk_clear is added to the catalog dk (3.8): seat 4.5 at the face, cone parallel to the head so the 4.4 head never touches (r5 overlap 0.09)
BASE_CSK_CLEAR_STEP = fc.clearance(M2, 'close') + 2 * 0.5 - fc.head(M2, 'csk')[0]   # original RV26 seat: dk 3.2 = the 2.2 hole plus Chamfer1 0.5 each side (panel volume matches the STEP to 0.03 %)
BASE_Z0, BASE_T = 3.5, 1.0           # base panel underside Z, skin thickness
INS_Z = (BASE_Z0 + BASE_T + BORE_CH, BASE_Z0 + BASE_T + BORE_CH + INS_LEN)   # the insert sits on the bore floor, a chamfer above the panel seat; bore mouth a length above
PAD_EDGE, PAD_DY = 0.25, 0.2          # N10 preload pad: its outer edge this far in from the wall inner face; its centre this far off the motor axis (Y)
PAD_S = 2 * GB["half_w"] - 0.5      # pad side: the gearbox width less a margin
PRELOAD_PAD = dict(c=(round(CH_IN_X - PAD_EDGE - PAD_S / 2, 6), round(RY + PAD_DY, 6)), s=PAD_S, h=0.465 if variant("pad_preload") else 0.25, r=0.85, sink=0.01)   # N10 preload pad on the base skin: centre |X|/Y, side, height (0.45 + 0.015: closes the 0.2 mm the STEP leaves under the N10, intent.seat_locates), corner R, sink into the skin (union overlap)
BASE_IN = 1.4                       # RV26 outline edge in from the chassis outer face (rear and side); the front edge is the front wall inner face
BASE_OUT = dict(x=round(CH_HALF_W - BASE_IN, 6), y0=round(CH_Y0 + BASE_IN, 6), y1=CH_Y1 - CH_WALL, r=0.8)   # RV26 outline 56.2 x 49.2, R0.8 corners
TOP_Z0, TOP_T = CH["z1"], 0.9               # Ti top panel sits on the chassis rim, 0.9 thick
TOP_X = 23.0                         # |X| of the top-panel side edges beside the switch
TOP_SHOULDER_Y = 7.9                 # front edge between the shoulders and the tab
TOP_NOTCH_X = (13.0, 21.0)           # |X| span of the front notches clearing the weapon-mount tabs (tab is |X| < 13)
TOP_TAB_Y = 11.9                     # tab front edge
ESC_TRAY = dict(gap=0.1, wall=1.25, lip=1.0, fuse=0.01, rail_end=1.0, rail_x=(1.4, 2.6))   # TPU ESC tray: walls >= 1.2, rails inset from the board -x / +x edges
CHAIKIN_Q = 0.25                     # Chaikin corner-cutting ratio (side-panel spline smoothing)
TOP_SCREW_WEB = True                 # ONE switch for the top-screw feature set: web + tap pilot under the corner columns' rim and bolt_t0..3 (off: the STEP's through-bore and no screws)
TOP_XY = tuple(INS[i] for i in (1, 0, 3, 2))   # the four corner insert columns (+X first), screw order of bolt_t*



LAT_GROW = 0.35   # mm, measured from RV01 y=-36 sections (pocket area 38.1 vs 28.2)


from shapely.geometry import Point, Polygon   # noqa: E402
NUT_LOBE = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull   # chassis wall lobe round the thin nut (Y, Z)
NUT_RELIEF_END_Y, NUT_STEP_R = -13.2, 0.0   # Y where the side-panel nut relief ends (RV23 runs on to -13.2; shared with side.py and the tub lobe tail); the lobe-tail step corner is the panel's own square edge (SHARP_OK)
PANEL_IN = 31.4   # inner face of the side panel at the nut lobe (|X|)
LUG_FLOOR_Z, LUG_SCALLOP_R, LUG_BLEND_R = 2.5, 4.0, 4.95   # param: organic lug underside arcs fitted to RV01: scallop R (RV01 R4), the blend into the standoff arc (ref R4.95)
LUG_SB_R = SB[1] - LUG_FLOOR_Z + 1.25   # standoff arc R round SB (3.25 at the STEP): its underside dips this far below the axis line to a skin under the lug floor, so the blend beneath the floor exists whatever the nose height
LUG_SA_R = SA[1] - LUG_FLOOR_Z + 1.5   # standoff end boss round SA (RV01 R4.5 at the STEP axle height): reaches the same depth under the lug floor whatever the wheel radius
# param: end
# the blend circle (R4.95) sits under the lug floor, tangent to it and to the standoff arc round SB: its centre follows from both
_blend_c = (SB[0] - math.sqrt((LUG_BLEND_R + LUG_SB_R) ** 2 - (SB[1] - (LUG_FLOOR_Z - LUG_BLEND_R)) ** 2), LUG_FLOOR_Z - LUG_BLEND_R)
LUG_SCALLOP_YT = _blend_c[0]   # the flat floor after the scallop ends where the blend begins
_k = LUG_SB_R / (LUG_BLEND_R + LUG_SB_R)
_blend_t = (SB[0] + _k * (_blend_c[0] - SB[0]), SB[1] + _k * (_blend_c[1] - SB[1]))   # blend / standoff-arc tangent point
_corner = (SB[0] - math.sqrt(LUG_SB_R ** 2 - (LUG_FLOOR_Z - SB[1]) ** 2), LUG_FLOOR_Z)   # where the floor would meet the standoff arc
LUG_BLEND_FILL = Polygon([(LUG_SCALLOP_YT, LUG_FLOOR_Z), _corner, SB, _blend_c]).difference(Point(_blend_c).buffer(LUG_BLEND_R, 96))   # cusp material the blend keeps
# the scallop (R4) is tangent to the floor and to the SA boss round, so the underside runs boss round -> scallop -> flat floor with no cusp
_sc = (SA[0] + math.sqrt((LUG_SA_R + LUG_SCALLOP_R) ** 2 - (SA[1] - (LUG_FLOOR_Z - LUG_SCALLOP_R)) ** 2), LUG_FLOOR_Z - LUG_SCALLOP_R)   # scallop centre
LUG_SCOOP_YT = _sc[0]   # Y where the scallop meets the lug floor
_ta = math.atan2(_sc[1] - SA[1], _sc[0] - SA[0])   # direction SA -> scallop centre: the tangent point on the boss round
LUG_BOSS_UNDER = Polygon([(SA[0] + LUG_SA_R * math.cos(a), SA[1] + LUG_SA_R * math.sin(a)) for a in [1.5 * math.pi + (_ta + 2 * math.pi - 1.5 * math.pi) * i / 24 for i in range(25)]]
                         + [(SA[0] + LUG_SA_R * math.cos(_ta), -20.0), (SA[0], -20.0)])   # hull fill under the boss round, from its bottom to the tangent point
LUG_SCALLOP = Point(LUG_SCOOP_YT, LUG_FLOOR_Z - LUG_SCALLOP_R).buffer(LUG_SCALLOP_R, 128).intersection(
    Polygon([(0.0, -20.0), (LUG_SCOOP_YT, -20.0), (LUG_SCOOP_YT, LUG_FLOOR_Z), (0.0, LUG_FLOOR_Z)])).union(
    Polygon([(LUG_SCOOP_YT, -20.0), (LUG_SCALLOP_YT, -20.0), (LUG_SCALLOP_YT, LUG_FLOOR_Z), (LUG_SCOOP_YT, LUG_FLOOR_Z)])).union(LUG_BOSS_UNDER)   # boss-round underside, R scoop, then the flat floor to the blend
# param: end
# --- tub_front/tub_shell relations ---
WALL_IN_FRONT = CH_Y1 - CH_WALL                  # inner face of the front wall (Y)
LUG_FACE_X = SB_X0                                # |X| of the lug's inner face the front corner flange blends into
SPIDER_TAB_GAP = 0.6                              # measured (STEP): the weapon spider's closest sweep to the tab wall's bevel
MOTOR_SLIDE_MAX = 2.2                             # measured (STEP): drive motor travel inboard before it touches the tub wall, plus margin
SIDE_SOLID_FRACTION = 0.9                         # side panel print infill: solid fraction
OVERLAP = 0.1                                     # solids reach this far into a neighbour so they fuse
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
