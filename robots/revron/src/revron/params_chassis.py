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
CH_Y0, CH_Y1 = -37.6, 15.0           # chassis rear face / front face (where the weapon-mount tabs start)
CH_Z0, CH_Z1 = 2.5, 19.5             # chassis floor underside / rim (top panel and mount notch sit on it)
CH_WALL = 2.0                        # printed wall and deck thickness
WY, WZ = 38.5, 23.5                  # weapon axis (along X)
RY, RZ = -30.5, 11.0                 # N10 shaft (rear axle)
SA = (30.5, 5.5)                     # 25 mm standoff (RV11): front axle (Y, Z)
SB = (40.5, 4.5)                     # 15 mm standoff (RV10): nose (Y, Z)
SA_LEN, SB_LEN = 25.0, 15.0          # catalog standoff lengths
SA_X0, SB_X0 = 17.5, 21.5            # |X| of each standoff's inner end
SO_R = 2.5                           # standoff radius
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
# insert columns: a 2 x 2 grid, each centre a fixed distance in from the inner wall faces, plus the rear boss one wall in front of the rear inner face
INS_PITCH_Y, INS_EDGE = 32.0, (2.5, 2.6)   # grid pitch along Y; column centre to the side wall inner face / to the front wall inner face
INS_COLS = tuple((sx * (CH_IN_X - INS_EDGE[0]), CH_Y1 - CH_WALL - INS_EDGE[1] - k * INS_PITCH_Y) for k in (0, 1) for sx in (-1, 1))
INS = [*INS_COLS, (0.0, CH_Y0 + 2 * CH_WALL)]   # 5 floor inserts / base screws
INSERT_CAT = "heatset_m2_4"          # FS1 M2 heat-set, brass, 3.5 OD x 4
INSERT_OD, INS_LEN = hw.size(INSERT_CAT)[1:]   # knurled OD and length from the catalog
BORE_CH = 0.6                        # chamfer of the heat-set bore at the panel seat and at the rim
# electronics envelopes (catalog boxes at their spec placement, rot z 90): Malenki nano 32 x 20 x 4.4 at (8.67, -3.0, 15.3),
# BBB ant ESC 23.5 x 12 x 5 at (8.63, -7.25, 10.6); the deck cage ribs are dimensioned off these
RX_SIZE, RX_C = (32.0, 20.0, 4.4), (8.67, -3.0, 15.3)     # receiver catalog box (L, W, H) and placed centre
WE_SIZE, WE_C = (23.5, 12.0, 5.0), (8.63, -7.25, 10.6)     # weapon ESC catalog box and placed centre


def _env(c, size):
    """(X, Y, Z) spans of a catalog box rotated 90 deg about Z (length along Y) centred on c."""
    w, l, h = size[1], size[0], size[2]
    return tuple((ci - d / 2, ci + d / 2) for ci, d in zip(c, (w, l, h)))


(RX_X, RX_Y, RX_Z), (WE_X, WE_Y, WE_Z) = _env(RX_C, RX_SIZE), _env(WE_C, WE_SIZE)
DRIVE_MOTOR = "n10_2200rpm_spicy"    # catalog id of the drive gearmotors (RV12): the tub is dimensioned from its plate stack
GB = hw.gearbox(DRIVE_MOTOR)         # plate stack in the motor frame: top, half_w, end, gaps
MOTOR_WALL_GAP = 0.3                 # last gearbox plate to the chassis wall's inner face
MOTX = round(CH_IN_X - MOTOR_WALL_GAP - GB["end"], 6)   # N10 catalog origin |X|: the stack ends a gap short of the wall
KEY_CLR = 0.15                       # chassis key tab to each gearbox plate
N10_KEY = tuple(round(MOTX + g + s * KEY_CLR, 6) for g, s in zip(GB["gaps"][-1], (1, -1))) if GB["gaps"] else None   # |X| of the key tab: the open span between the stack's last two plates less the clearance; none when the gearbox has no such gap
N10_TOP = round(RZ + GB["top"], 6)   # top face of the N10 gearbox plates
KEY_BITE, STOP_CLR = 0.65, 0.1       # key tab reaches this far behind the gearbox front face; the stop wall stands this clear of it
KEY_SPAN = (round(RY + GB["half_w"] - KEY_BITE, 6), round(RY + GB["half_w"] + STOP_CLR + CH_WALL, 6))   # Y span of the key tab / stop wall
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
TOP_XY = tuple(INS[i] for i in (1, 0, 3, 2))   # the four corner insert columns (+X first), screw order of bolt_t*



LAT_GROW = 0.35   # mm, measured from RV01 y=-36 sections (pocket area 38.1 vs 28.2)


from shapely.geometry import Point, Polygon   # noqa: E402
NUT_LOBE = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull   # chassis wall lobe round the thin nut (Y, Z)
NUT_RELIEF_END_Y, NUT_STEP_R = -13.2, 0.0   # Y where the side-panel nut relief ends (RV23 runs on to -13.2; shared with side.py and the tub lobe tail); the lobe-tail step corner is the panel's own square edge (SHARP_OK)
PANEL_IN = 31.4   # inner face of the side panel at the nut lobe (|X|)
LUG_FLOOR_Z, LUG_SCALLOP_R, LUG_BLEND_R, LUG_SB_R = 2.5, 4.0, 4.95, 3.25   # param: organic lug underside arcs fitted to RV01: scallop R (RV01 R4), the blend into the standoff arc (ref R4.95), standoff arc R
LUG_SA_R = 4.5   # standoff end boss round SA (RV01 R4.5)
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
WALL_IN_REAR = CH_Y0 + CH_WALL                   # inner face of the rear wall (Y)
COL_R = 2.75                                      # insert column boss radius (corner blocks, rear boss and deck pockets are tangent to it)
LUG_FACE_X = SB_X0                                # |X| of the lug's inner face the front corner flange blends into
OVERLAP = 0.1                                     # solids reach this far into a neighbour so they fuse
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
