"""Revron params: masters, chassis layout, panels, lug blend (RV01 / RV26 / Ti top). Re-exported by params.py."""
import json, math, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

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
M3_THIN_NUT_T = 1.8                  # DIN 439 M3 thin nut thickness
MNT_IN, MNT_T, MNT_SLAB_T = 13.4, 8.0, 4.0   # weapon mount: inner face |X|, total thickness, slab thickness (rest = battered boss)
FLOOR_Z = 1.0                        # ground-contact plane of the ramps / side feet
# ---------------------------------------------------------------------------------------------------------------------
CH_IN_X = CH_HALF_W - CH_WALL        # inner face of the side walls (27.5)
REF_TO_WORLD = [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
SA_X, SB_X = (SA_X0, SA_X0 + SA_LEN), (SB_X0, SB_X0 + SB_LEN)   # standoff |X| spans: inner end + catalog length
NUT = (-11.5, 8.5)                   # side-panel screw into a thin M3 nut in the chassis wall (Y, Z)
NUT_X = (CH_HALF_W - M3_THIN_NUT_T, CH_HALF_W)   # nut pocket opens on the outer wall face, one nut deep
INS = [(-25.0, 10.4), (25.0, 10.4), (-25.0, -21.6), (25.0, -21.6), (0.0, -33.6)]   # 5 floor inserts / base screws
INS_Z = (5.1, 9.1)                   # FS1 M2 heat-set (3.5 OD x 4): bore floor and mouth Z (insert sits on the bore floor)
INS_LEN = INS_Z[1] - INS_Z[0]
CSK_M2 = 4.5                         # 90 deg countersink at the face for an ISO 10642 M2 flat head (4.4 x 1.2) + 0.1
PANEL_EAR_R = 3.0
TOP_HOLE = 3.5         # csk through-holes: wide enough that the 90 deg seat stops short of the far face (no knife edge)
# electronics envelopes (catalog boxes at their spec placement, rot z 90): Malenki nano 32 x 20 x 4.4 at (8.67, -3.0, 15.3),
# BBB ant ESC 23.5 x 12 x 5 at (8.63, -7.25, 10.6); the deck cage ribs are dimensioned off these
RX_SIZE, RX_C = (32.0, 20.0, 4.4), (8.67, -3.0, 15.3)     # receiver catalog box (L, W, H) and placed centre
WE_SIZE, WE_C = (23.5, 12.0, 5.0), (8.63, -7.25, 10.6)     # weapon ESC catalog box and placed centre


def _env(c, size):
    """(X, Y, Z) spans of a catalog box rotated 90 deg about Z (length along Y) centred on c."""
    w, l, h = size[1], size[0], size[2]
    return tuple((ci - d / 2, ci + d / 2) for ci, d in zip(c, (w, l, h)))


(RX_X, RX_Y, RX_Z), (WE_X, WE_Y, WE_Z) = _env(RX_C, RX_SIZE), _env(WE_C, WE_SIZE)
EAR_R = 2.7                          # top-panel corner ear radius: >= CSK_M2 / 2 + 0.4 mm of Ti round the countersink
MOTX = 19.6                          # N10 catalog origin |X| (body 3.7..27.5, shaft to 37.5)
N10_KEY = (23.55, 26.15)             # |X| of the chassis key tab between the N10's last two gearbox plates
CHASSIS_MIN_VOL = 15000.0               # a sound chassis is ~15900 mm3 in one solid; less means a boolean collapsed
KEY_SPAN, KEY_DEV_R = (-26.15, -23.4), 2.5   # Y span of the key tab, radius of its reference-deviation zone
N10_TOP = 17.0                       # top face of the N10 gearbox plates
# chassis RV01
SW_HALF_W, SW_CLR = 2.9, 0.05   # power switch body half-width, its clearance to the inner wall face
SWX = CH_IN_X - SW_CLR - SW_HALF_W   # power switch X: body side 0.05 clear of the 27.5 inner wall face (was 25.0, 0.4 into it)
CH = dict(x=CH_HALF_W, y0=CH_Y0, y1=CH_Y1, z0=CH_Z0, z1=CH_Z1, wall=CH_WALL, deck=CH_Z1 - CH_WALL, cham=CH_WALL)
# drisk

# ====================================================================================================================
# Parts
# ====================================================================================================================
# panels (RV26 base, Ti top) [fix-T: named params, every panel dimension derives from these]
SEG, SEG_FINE = 64, 128              # shapely buffer resolution (segments per quarter circle) for ears / tangent arcs
BASE_CSK_CLEAR = -0.6                # base-panel seat 3.2 at the face = STEP RV26 (dk 3.8 - 0.6)
BASE_Z0, BASE_T = 3.5, 1.0           # base panel underside Z, skin thickness
PRELOAD_PAD = dict(c=(22.5, -30.3), s=9.1, h=0.465, r=0.6, sink=0.01)   # N10 preload pad on the base skin: centre |X|/Y, side, height (0.45 + 0.015: closes the 0.2 mm the STEP leaves under the N10, intent.seat_locates), corner R, sink into the skin (union overlap)
BASE_FILLET, BASE_EDGE_TOL, BASE_EDGE_UP, FLAT_TOL = 0.25, 0.02, 0.1, 1e-3   # base skin joint fillet; edge selection tolerances (height band, face rise, flatness)
BASE_OUT = dict(x=28.1, y0=-36.2, y1=13.0, r=0.8)   # RV26 outline 56.2 x 49.2, R0.8 corners
PANEL_EAR_EDGE = 3.0                 # a screw closer than this to the outline edge gets a PANEL_EAR_R ear
PANEL_R_IN = 0.5                     # concave blend where the ears meet the outline
TOP_Z0, TOP_T = CH["z1"], 0.9        # Ti top panel sits on the chassis rim, 0.9 thick
TOP_X = 23.0                         # |X| of the top-panel side edges beside the switch
TOP_Y0, TOP_Y1 = -24.1, 12.9         # rear edge, front of the shoulders
TOP_SHOULDER_Y = 7.9                 # front edge between the shoulders and the tab
TOP_NOTCH_X = (13.0, 21.0)           # |X| span of the front notches clearing the weapon-mount tabs (tab is |X| < 13)
TOP_TAB_Y = 11.9                     # tab front edge
TOP_CUT_Y = 14.0                     # notch / tab cutters run past the panel front (ears end at Y 13.1)
TOP_FILL_YT = (1.0, -12.5)           # Y where each concave ear-to-edge arc meets the |X| 23 edge (front, rear ear row)
TOP_FILL_X = 26.6                    # outer X of the arc fill boxes (past the ears)
TOP_R_OUT, TOP_R_IN = 0.4, 1.2       # top-panel edge rounds
ESC_TRAY = dict(gap=0.1, wall=1.25, lip=1.0, fuse=0.01, rail_end=1.0, rail_x=(1.4, 2.6))   # TPU ESC tray: walls >= 1.2, rails inset from the board -x / +x edges
CHAIKIN_Q = 0.25                     # Chaikin corner-cutting ratio (side-panel spline smoothing)
TOP_XY = tuple(INS[i] for i in (1, 0, 3, 2))   # the four corner insert columns (+X first), screw order of bolt_t*



LAT_GROW = 0.35   # mm, measured from RV01 y=-36 sections (pocket area 38.1 vs 28.2)


from shapely.geometry import Point, Polygon   # noqa: E402
NUT_LOBE = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull   # chassis wall lobe round the thin nut (Y, Z)
NUT_RELIEF_END_Y, NUT_STEP_R = -13.2, 0.0   # Y where the side-panel nut relief ends (RV23 runs on to -13.2; shared with side.py and the tub lobe tail); the lobe-tail step corner is the panel's own square edge (SHARP_OK)
SP_NUT_RELIEF_RUN = 1.0   # the relief floor runs on past NUT_RELIEF_END_Y until it dies out in the inner face's rear sweep (RV23: floor X-32.5 meets the sweep at Y-13.37, ours at -13.45), so it ends with no step wall
SP_NUT_RELIEF_Y1 = NUT_RELIEF_END_Y - SP_NUT_RELIEF_RUN
SP_NUT_RELIEF = [(SP_NUT_RELIEF_Y1, 3.8), (0.5, 4.7), (2.3, 5.7), (2.3, 8.3), (0.5, 9.3), (-3.5, 11.0), (-9.5, 13.0), (SP_NUT_RELIEF_Y1, 13.8)]   # STEP RV23 diamond (Y, Z)
PANEL_IN = 31.4   # inner face of the side panel at the nut lobe (|X|)
LUG_FLOOR_Z, LUG_SCALLOP_R, LUG_BLEND_R, LUG_SB_R = 2.5, 8.6, 4.95, 3.25   # param: organic lug underside arcs fitted to RV01: scallop R, the blend into the standoff arc (ref R4.95), standoff arc R
# param: end
# the blend circle (R4.95) sits under the lug floor, tangent to it and to the standoff arc round SB: its centre follows from both
_blend_c = (SB[0] - math.sqrt((LUG_BLEND_R + LUG_SB_R) ** 2 - (SB[1] - (LUG_FLOOR_Z - LUG_BLEND_R)) ** 2), LUG_FLOOR_Z - LUG_BLEND_R)
LUG_SCALLOP_YT = _blend_c[0]   # the big scallop arc ends tangent to the floor where the blend begins
_k = LUG_SB_R / (LUG_BLEND_R + LUG_SB_R)
_blend_t = (SB[0] + _k * (_blend_c[0] - SB[0]), SB[1] + _k * (_blend_c[1] - SB[1]))   # blend / standoff-arc tangent point
_corner = (SB[0] - math.sqrt(LUG_SB_R ** 2 - (LUG_FLOOR_Z - SB[1]) ** 2), LUG_FLOOR_Z)   # where the floor would meet the standoff arc
LUG_BLEND_FILL = Polygon([(LUG_SCALLOP_YT, LUG_FLOOR_Z), _corner, SB, _blend_c]).difference(Point(_blend_c).buffer(LUG_BLEND_R, 96))   # cusp material the blend keeps
LUG_SCALLOP = Point(LUG_SCALLOP_YT, LUG_FLOOR_Z - LUG_SCALLOP_R).buffer(LUG_SCALLOP_R, 128).intersection(
    Polygon([(0.0, -20.0), (LUG_SCALLOP_YT, -20.0), (LUG_SCALLOP_YT, LUG_FLOOR_Z), (0.0, LUG_FLOOR_Z)]))
# param: end
# --- tub_front/tub_shell relations ---
WALL_IN_FRONT = CH_Y1 - CH_WALL                  # inner face of the front wall (Y)
WALL_IN_REAR = CH_Y0 + CH_WALL                   # inner face of the rear wall (Y)
COL_R = 2.75                                      # insert column boss radius (corner blocks, rear boss and deck pockets are tangent to it)
LUG_FACE_X = SB_X0                                # |X| of the lug's inner face the front corner flange blends into
OVERLAP = 0.1                                     # solids reach this far into a neighbour so they fuse
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
