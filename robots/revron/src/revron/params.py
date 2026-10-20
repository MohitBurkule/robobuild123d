"""[fix-S] Revron master dimensions and module-level constants (measured on the RVRN 2.0 STEP)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # src/
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ======================================================================================================================
# Measured layout (RVRN 2.0 STEP, world frame). Each number is a dimension of a feature, not a mesh coordinate list.
# ======================================================================================================================
REF_TO_WORLD = [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
WY, WZ = 38.5, 23.5                  # weapon axis (along X)
SA = (30.5, 5.5)                     # 25 mm standoff (RV11): front axle, X 17.5..42.5
SB = (40.5, 4.5)                     # 15 mm standoff (RV10): nose, X 21.5..36.5
SA_X, SB_X = (17.5, 42.5), (21.5, 36.5)
SO_R = 2.5
NUT = (-11.5, 8.5)                   # side-panel screw into a thin M3 nut in the chassis wall (Y, Z)
NUT_X = (27.7, 29.5)
INS = [(-25.0, 10.4), (25.0, 10.4), (-25.0, -21.6), (25.0, -21.6), (0.0, -33.6)]   # 5 floor inserts / base screws
INS_Z = (5.1, 9.1)                   # FS1 M2 heat-set (3.5 OD x 4)
CSK_M2 = 4.5                         # 90 deg countersink at the face for an ISO 10642 M2 flat head (4.4 x 1.2) + 0.1
PANEL_EAR_R = 3.0
BASE_HOLE, TOP_HOLE = 3.4, 3.5         # csk through-holes: wide enough that the 90 deg seat stops short of the far face (no knife edge)
BOSS_R, BOSS_H = 2.6, 0.3            # base-panel ring boss round each screw (keys into a 2.65 x 0.45 recess in the column foot)
# electronics envelopes (catalog boxes at their spec placement, rot z 90): Malenki nano 32 x 20 x 4.4 at (8.67, -3.0, 15.3),
# BBB ant ESC 23.5 x 12 x 5 at (8.63, -7.25, 10.6); the deck cage ribs are dimensioned off these
RX_X, RX_Y, RX_Z = (8.67 - 10.0, 8.67 + 10.0), (-3.0 - 16.0, -3.0 + 16.0), (15.3 - 2.2, 15.3 + 2.2)
WE_X, WE_Y, WE_Z = (8.63 - 6.0, 8.63 + 6.0), (-7.25 - 11.75, -7.25 + 11.75), (10.6 - 2.5, 10.6 + 2.5)
EAR_R = 2.7                          # top-panel corner ear radius: >= CSK_M2 / 2 + 0.4 mm of Ti round the countersink
RY, RZ = -30.5, 11.0                 # N10 shaft (rear axle)
MOTX = 19.6                          # N10 catalog origin |X| (body 3.7..27.5, shaft to 37.5)
N10_KEY = (23.55, 26.15)             # |X| of the chassis key tab between the N10's last two gearbox plates
CHASSIS_MIN_VOL = 15000.0               # a sound chassis is ~15900 mm3 in one solid; less means a boolean collapsed
KEY_SPAN, KEY_DEV_R = (-26.15, -23.4), 2.5   # Y span of the key tab, radius of its reference-deviation zone
N10_TOP = 17.0                       # top face of the N10 gearbox plates
# chassis RV01
SWX = 24.55   # power switch X: body side 0.05 clear of the 27.5 inner wall face (was 25.0, 0.4 into it)
CH = dict(x=29.5, y0=-37.6, y1=15.0, z0=2.5, z1=19.5, wall=2.0, deck=17.5, cham=2.0)
# drisk
# master parameters of the stack: plate thicknesses and where the first plate starts; every X span below is chained from them
SPIDER_T, DISC_T, SPACER_T, STACK_X0 = 3.0, 3.0, 6.0, -8.2
DR_X, _x = {}, STACK_X0
for _n, _t in (("spider", SPIDER_T), ("disc_a", DISC_T), ("spacer", SPACER_T), ("disc_b", DISC_T)):
    DR_X[_n] = (_x, _x + _t)       # spider | disc_a | spacer | disc_b, each flush on the previous one
    _x += _t
DR_ROT = -54.889                     # drisk phase about the axis (STEP Drisk_V4 placement)
DISC_R, DISC_ECC, DISC_ECC_A = 16.5, 0.5, -40.0   # eccentric rim: R16.5 centred 0.5 mm towards -40 deg (balances the tooth)
TOOTH_R, TOOTH_A = 23.0, 134.8
BOLT_R, HUB_R = 14.0, 4.5            # stack-bolt circle and bell-screw circle (radii about the weapon axis)
N_STACK = 4                          # bolts / lobes / windows per stack, 90 deg apart
# motor GR1507: axis X, stator base X 8.4..10.4 on the right mount via the back spacer X 11.9..13.4
SHAFT_D, SHAFT_CLR, BRG_SEAT_R, NUT_RECESS_R = 5.0, 0.1, 3.95, 6.0   # GR1507 shaft, its clearance in RV03, MR85 seat (8 mm bearing, 7.9 STEP), shaft nut recess
STATOR_PCD, BOSS_OVER = 12.0, 0.01        # stator M2 bolt circle; boss overshoots the battered plane before it is split
MNT_SCREW = ("M3x12", "M3x14")           # mount-to-standoff CSK screws at SA, SB
MNT_SCREW_FIT = "loose"                  # ISO 273 loose clearance: the screws have slack, the notch face takes the hit first
MNT_IN, MNT_T, MNT_SLAB_T = 13.4, 8.0, 4.0   # weapon mount: inner face |X|, total thickness, slab thickness (rest = battered boss)
MNT_OUT, MNT_SLAB = MNT_IN + MNT_T, MNT_IN + MNT_SLAB_T
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
BSP_T = 1.5                          # printed spacer between the stator base and the right mount
BSP_X = (MNT_IN - BSP_T, MNT_IN)
STAT_HOLE_R, CB_R, CB_CONE_X = 1.12, 2.25, (16.4, 17.15)   # RV03 stator screw clearance d2.24, d4.5 counterbore, its cone
PHASE_VIA = [[11.8, 14.5, 16.0], [11.8, 15.5, 18.2], [11.8, 27.0, 18.2], [11.8, 30.0, 14.5]]   # weapon phase leads: the lug (|X| >= 10.4, up to the deck) closes z 14.5 at y 15..26


# ====================================================================================================================
# Parts
# ====================================================================================================================
# panels (RV26 base, Ti top) [fix-T: named params, every panel dimension derives from these]
SEG, SEG_FINE = 64, 128              # shapely buffer resolution (segments per quarter circle) for ears / tangent arcs
CSK_CLEAR = 0.7                      # countersink diameter over the ISO 10642 head (4.5 seat: dk 3.8 + 0.7)
BASE_Z0, BASE_T = 3.5, 1.0           # base panel underside Z, skin thickness
PRELOAD_PAD = dict(c=(22.5, -30.3), s=9.1, h=0.465, r=0.6, sink=0.01)   # N10 preload pad on the base skin: centre |X|/Y, side, height (0.45 + 0.015), corner R, sink into the skin (union overlap)
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


WSEG_LO, WSEG_FINE, WSEG_MID, WSEG_HI, WSEG_FN, WSEG_MAX, WSEG_ARC, WSEG_ARC_S = 24, 32, 48, 64, 96, 128, 40, 12   # circle / arc tessellation of the 2D profiles
# weapon mount RV02 (left, shaft end) / RV03 (right, stator): per-side master parameters (STEP measurements)
MNT_SIDE = dict(
    r=dict(top_r=10.0, notch_y=10.17, rim_end=-14.5, slab_eps=0.02, face=(23.88, 0.144, 0.0379)),   # a, kz, ky of |X| = a - kz*Z - ky*Y
    l=dict(top_r=7.0, notch_y=9.0, rim_end=-5.0, slab_eps=0.0, face=(23.48, 0.185, 0.0168)))
MNT_TOP_Z = 19.5                        # top of the rear notch: the teardrop's tangent line starts here
TAB = dict(y0=15.0, z0=5.35, h=8.2, y1=26.5, cham=1.0)   # chassis tab the notch drops over: rear Y, floor Z, height, front-face Y, front chamfer
MNT_HEEL = dict(z=1.25, step=0.4, back=1.8, z_hook=2.5, z_lip=4.5)   # rear foot hooked under the tab: floor Z, tip step, setback, hook and lip Z
MNT_NOTCH_UP = 2.0                      # the rear face above the tab leans back by this much over the last stretch to the top
NOSE_R, NOSE_A0 = 3.25, -16.0           # nose arc round the SB standoff and where it leaves the outline (deg)
NOSE_PAD_R = 4.1                        # local pad round the nose CSK: CSK cone radius (3.2) + a 0.9 mm printed wall (the STEP nose leaves 0.15 mm)
BOSS_Z = 6.34                           # the boss starts above the line from the notch top to the nose, at this Z at the nose end
BOSS_NOSE_Y = 44.34
BIG = 60.0                              # a box edge bigger than any part, for half-plane clips
MNT_RELIEF_R = 1.0                      # concave corner relief of the profile (tub deck fillet, mfg corner relief)
MNT_CSK_CLEAR = 0.4                     # extra cone diameter over the DIN 7991 head: the seated head floats, so the notch bears a hit before the screws do
MNT_TIP_WALL, MNT_TIP_REACH = 1.5, 3.0    # printed wall: the wedge where the rear notch meets the rim tangent is thickened upward to this within this reach of the notch top (rearmost point and underside unchanged: the underside rides on the chassis tab)


HOLE_FACE_RISE = 0.7                    # the battered face's highest point over a stator hole axis: the surface the hole is measured from
BSP = dict(r=10.0, bore_r=4.0, win_in=5.5, win_out=8.5, half_deg=25.0, win_round=1.5, hole_r=1.05, phase=45.0)   # motor back spacer (STEP)


DISC_BORE_RES = 4                       # bore polygon samples per degree
DOG = dict(r=12.0, rise=1.52, t0=5.0, t1=18.0, t2=55.0)       # bore dogs (90 deg pitch): steep rise t0..t1, long ramp back to t2
DISC_BORE_ROUND, DISC_HOLE_R_WIN = 0.5, 0.44                    # bore corner rounding; balance window corner radius
DISC_BAL_PTS = [(-13.2, 4.85), (-13.2, 9.08), (-11.68, 7.65)]    # param: organic balance-window hull corners (measured, STEP)
TOOTH_PTS = [(-11.0, 11.6), (-8.0, 8.0), (-16.2, 0.0), (-16.25, 15.0)]   # param: organic tooth flank/root polygon (measured, STEP)
# param: end
DISC_ROUND = dict(r_out=0.2, r_in=0.7)                           # tooth tip land (0.4 laser-cuttable) and root fillet


SPIDER = dict(r=14.2, lobe_r=2.3, round_in=0.8, win_r=11.7, win_off=2.3, win_far=20.0, hub_r=5.6, win_round=0.6, bore_r=2.6)


SPACER = dict(r=16.0, bore_r=9.9, win_in=11.4, win_out=14.5, half_deg=36.0, win_round=1.0, phase=45.0)


# ------------------------------------------------------------------------------------------------------------ wedgelet
WEDGE_TOE_H = 0.85                   # ramp Z = 1 + 1.187 (50.1 - Y) lifted so its toe is a 0.85 mm land at full length


# ------------------------------------------------------------------------------------------------------------ side panel
SP_IN = [(-43.5, -41.0), (-43.5, -21.3), (-43.0, -19.6), (-41.2, -17.9), (-37.2, -17.2), (-34.4, -15.7), (-32.3, -13.0), (-31.5, -9.9),
         (-31.5, 11.1), (-31.9, 13.4), (-33.6, 17.5), (-35.5, 20.4), (-37.2, 21.9), (-41.2, 23.3), (-42.7, 26.6)]
# the front swing round the front wheel (inner face X at Y 13, 14, 16, 18, 20, 22, 24, 26.6) at three heights: it leans
# out towards the floor so wheel hits ride up it (STEP RV23: inner face at Y 22 is X -47.6 at the floor, -41.6 at Z 7)
SW_Y = (13.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.6)
SW_X = {1.0: (-32.4, -33.4, -36.6, -44.0, -46.3, -47.6, -48.3, -48.6),
        4.0: (-32.2, -32.7, -34.2, -36.7, -43.0, -45.1, -46.0, -46.6),
        7.5: (-31.7, -32.2, -33.2, -34.4, -36.0, -40.5, -43.0, -43.8),
        9.5: (-31.6, -31.9, -32.8, -33.6, -34.6, -36.4, -39.6, -42.3)}
# wall thickness (normal to the inner face) against height: rear / middle run battered 5 -> 2 mm, the swing ~3.4 mm
SP_W_Z = (1.0, 3.0, 6.0, 9.0, 12.0, 16.0)
SP_FOOT_LAND = 0.85
SP_W_REAR = (5.2, 4.9, 4.3, 3.6, 3.0, 2.1)
SP_W_MID = (5.0, 4.7, 3.5, 2.7, 2.3, 2.0)
SP_W_SWING = (3.3, 3.3, 3.0, 2.6, 2.4, 2.1)
SP_W_Y = (-16.0, -12.0, 11.0, 15.0)   # rear / mid / mid / swing thickness stations along Y
# STEP RV23: the outer face swells 0.7 mm round the nut lobe (Y -11..1) at Z 4..12 (outer X -35.3 at Y -5 vs -34.5 at Y 5, Z 7.5)
SP_BUMP = 0.7
SP_BUMP_Y = (-5.0, 6.0)   # centre, half-width
SP_BUMP_Z = (7.5, 5.0)


# --- side panel + wedgelet shared / derived dimensions (outlines are organic point tables measured on RV23/RV17) ---
RAMP_REACH, RAMP_SLOPE, FLOOR_Z = 50.1, 1.187, 1.0   # ramp face Z = FLOOR_Z + RAMP_SLOPE (RAMP_REACH - Y), shared by wedgelet and nose
SLAB_X = (-60.0, -20.0)              # X slab the (Y, Z) side profile is extruded through before it is cut to the panel
SP_TOP = [(-32.9, 1.0), (-32.9, 16.0), (-6.7, 16.0), (14.6, 12.0), (19.3, 11.0), (24.0, 10.0), (42.0, 10.0), (RAMP_REACH, 1.0)]   # top line, (Y, Z)
SP_TOP_R = 1.5
SP_REAR_ROUND = ((-32.2, 9.7), 8.2)  # rear end: a full round over the wheel
SP_FOOT = [(-31.6, -12.0), (-42.0, -11.9), (-40.6, -2.1), (-40.8, 3.3), (-42.9, 13.3), (-31.6, 13.3)]   # 1 mm wide foot under the chassis lobe (X, Y)
SP_FOOT_Z = (FLOOR_Z, FLOOR_Z + 1.0)
SP_NOSE = [(-52.1, 26.5), (-51.7, 39.7), (-50.5, 43.0), (-48.4, 45.7), (-45.6, 47.9), (-42.0, 49.6), (-40.0, RAMP_REACH), (-38.5, RAMP_REACH),
           (-38.5, 37.6), (-41.6, 37.6), (-42.4, 37.3), (-42.3, 34.9), (-40.5, 34.5), (-40.5, 26.5)]   # nose plan (X, Y)
SP_NOSE_R, SP_NOSE_Z = 0.5, (FLOOR_Z, 10.0)
SP_BATTER = dict(x0=-52.06, slope=0.84, z=(FLOOR_Z, 16.0), below=-5.0, far=0.0, depth=60.0)   # outer face leans in 38 deg: X = x0 + slope (Z - FLOOR_Z)
SP_TOE_Y0 = 47.0                     # the ramp toe's land starts here (Y)
SP_TOE_RUN = 3.1                     # Y run of the ramp skin the toe polygon follows
SP_CHAMFER = ((-120.0, 0.0, 0.0), (1.0, -1.525, -1.4725))   # front-outer corner chamfer plane (origin, normal)
SP_HOLLOW = [(26.5, 3.0), (37.0, 3.0), (37.7, 6.6), (39.0, 10.5), (26.5, 10.5)]   # hollow behind the nose wall (Y, Z)
SP_HOLLOW_X = (-42.0, -38.4)
SP_CSK = dict(csk_clear=0.7, head_clear=12.0)   # M3 ISO 10642 seat (head dk 6.0 + 0.7) + 12 mm driver bore out through the battered face
SP_SA_CLEAR = (2.55, -42.55, -38.0)  # standoff-end clearance bore round SA (R, X0, X1)
SP_BOSS = (3.0, -42.5, -39.5)        # standoff end boss round SA (R, X0, X1)
SP_TYRE_RELIEF = (-45.0, -43.4, -38.7, -24.8, 5.5, 14.5)   # rear tyre relief box on the inner face (x0, x1, y0, y1, z0, z1)
SP_NUT_RELIEF = [(-11.7, 3.8), (0.5, 4.7), (2.3, 5.7), (2.3, 8.3), (0.5, 9.3), (-3.5, 11.0), (-9.5, 13.0), (-11.7, 13.8)]   # STEP RV23 diamond (Y, Z)
SP_NUT_RELIEF_X = (-32.5, -31.4)
CHASSIS_MIN_VOLUME = 15000.0         # mm3: the intact chassis is 15988 mm3 in one solid
SP_NUT_RELIEF_R = 1.0                # relief corners round r1: no sharp concave corner in the printed wall
SP_VENT = dict(y0=(-11.0, -4.5, 2.0), z0=5.0, dy=5.0, dz=6.0, r=1.0, x=(-50.0, -36.5))   # diagonal ESC vent slots
SP_LOFT = dict(resample=400, path=240, ring=481, round=0.6, arc=16)   # section smoothing: pchip samples, path points, ring points, fillet
WG_X = (-38.5, -36.5, -35.5, -29.0, -21.5, -17.5)   # slab edges along X: block | ring step | skin | cheek | nose tab
WG_S1 = (3.5, [(40.5, 1.0), (RAMP_REACH, 1.0), (42.54, 10.0), (39.55, 10.0), (40.23, 8.0)])   # block round SB: (R, tail outline (Y, Z))
WG_S2 = (3.0, [(40.4, 7.5), (39.55, 10.0), (41.92, 10.0), (42.29, 10.31), (RAMP_REACH, 1.0), (46.68, 1.0), (44.96, 1.5), (40.5, 1.5)])
WG_SKIN = [(RAMP_REACH, 1.0), (47.57, 1.0), (46.8, 1.36), (40.79, 8.52), (40.22, 8.04), (37.65, 15.92)]
WG_SKIN_RAKE = ((-34.0, 41.66, 11.06), (-1.24, -0.75, 1.0))   # plane (origin, normal) capping the skin's top edge
WG_CHEEK = [(38.05, 15.36), (RAMP_REACH, 1.0), (26.55, 1.0), (26.59, 6.09), (26.94, 7.22), (27.48, 8.04), (28.7, 9.02), (30.78, 9.78), (32.43, 10.71),
            (36.62, 14.17), (37.1, 12.78), (38.6, 12.78), (37.79, 15.15)]
WG_IN_SLOT = [(38.69, 10.9), (39.12, 11.26), (37.79, 15.15), (38.05, 15.36), (RAMP_REACH, 1.0), (43.75, 1.0), (43.73, 4.82), (43.37, 6.03),
              (42.91, 6.68), (41.0, 8.6), (40.03, 8.6), (39.52, 10.07)]
WG_TAB = [(42.78, 6.82), (44.32, 6.1), (44.69, 7.44), (RAMP_REACH, 1.0), (43.75, 1.0), (43.71, 4.98), (43.37, 6.03)]
ARC_N, ARC_MOUNT, ARC_KIDNEY, WG_MERGE_EPS = 64, 32, 24, 0.01       # circle facets per quarter; overlap that merges the toe land with the wedgelet body
WG_TAB_FILM = 0.6                    # TPU film limit: slivers thinner than this are dropped from the nose tab
WG_MOUNT_GAP = 0.1                   # nose tab clearance to the weapon mount boss
WG_FORK_SLOT_X = (-27.0, -24.5)      # 2.5 mm fork slot through the cheek
WG_BORES = dict(sa=2.6, sb=1.6, sb_head=2.5)   # radii of the standoff bores through the wedgelet (sb_head: block end only)
WG_BORE_X = (-39.0, -17.0)
WG_KIDNEY = ([(36.05, 5.15), (36.95, 7.45)], 0.95, (-29.5, -21.0))   # fork-tail kidney slot (centre line (Y, Z), half width, X span)
WG_TOE = [(48.6, 1.0), (RAMP_REACH, 1.0), (RAMP_REACH, 1.0 + WEDGE_TOE_H), (48.6, 1.0 + 1.5 * RAMP_SLOPE)]   # knife toe on a printable land (Y, Z)



LAT_GROW = 0.35   # mm, measured from RV01 y=-36 sections (pocket area 38.1 vs 28.2)


from shapely.geometry import Point, Polygon   # noqa: E402
NUT_LOBE = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull   # chassis wall lobe round the thin nut (Y, Z)
NUT_RELIEF_END_Y, NUT_STEP_R = -13.2, 0.0   # Y where the side-panel nut relief ends (RV23 runs on to -13.2; shared with side.py and the tub lobe tail); the lobe-tail step corner is the panel's own square edge (SHARP_OK)
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


# ====================================================================================================================
# Spec
# ====================================================================================================================
SOLID = dict(tub=0.8, mount=0.85, hub=0.85, tpu=0.9, shaft=0.05)    # solid_fraction of printed parts (infill and shell mass share)
WEDGE_REF = {-1: "RV17", 1: "RV18"}                      # STEP part ids of the wedgelets and side panels per side
SIDE_REF = {-1: "RV23", 1: "RV24"}
SIDE_BOLT_X = dict(a=46.26, b=41.76, c=35.26)            # |X| of the side-panel screw heads (STEP: seated in a bore below the face; axle standoff, nose standoff, chassis nut)
SIDE_SINK = dict(a=2.15, b=5.75, c=1.05)                 # depth of each screw head below the battered outer face, measured on the STEP side panels RV23 (LH) / RV24 (RH): outer face |X| 48.41 / 47.51 / 36.31 at the screw axes, minus the head planes above
SIDE_FACE_X = {k: SIDE_BOLT_X[k] + SIDE_SINK[k] for k in SIDE_BOLT_X}   # |X| of the battered outer face at each screw
assert all(0 < d <= SP_CSK["head_clear"] for d in SIDE_SINK.values()), "a screw head must sit inside its driver bore (sink <= bore depth)"
SIDE_BOLT_DES = dict(a="M3x10", b="M3x10", c="M3x8")
BASE_BOLT_Z = 3.5                                        # base-panel screw head plane
TOP_BOLT_XY = INS[1::-1] + INS[3:1:-1]                   # top-panel screws sit on the four corner columns, right-hand first
PCT = 100                                                # percent
AWG = dict(power=24, rx=26, motor=28, signal=30)
SLACK = dict(short=6, bench=8, phases=15)                # wire slack allowed, mm
# (id, from, to, awg, kind, slack, extras)
WIRES = [("w_bat_sw", "battery.jst_rcy", "power_switch.in", AWG["power"], "power", SLACK["bench"], dict(connector="jst_rcy")),
         ("w_sw_wesc", "power_switch.out", "wesc.bat", AWG["power"], "power", SLACK["bench"], {}),
         ("w_sw_rx", "power_switch.out", "rxesc.bat", AWG["rx"], "power", SLACK["bench"], {}),
         # phases run rearward in the gap behind the drisk (4 mm axial from the stack), over the front lug (its top is the deck) and down into the tub at the deck front
         ("w_wesc_m", "wesc.motor", "weapon_motor.phases", AWG["power"], "motor", SLACK["phases"], dict(connector="bullet2", count=3, via=PHASE_VIA)),
         ("w_rx_wesc", "rxesc.wpn", "wesc.rx", AWG["signal"], "signal", SLACK["short"], {}),
         ("w_m_l", "rxesc.m2", "motor_l.terminals", AWG["motor"], "motor", SLACK["short"], {}),
         ("w_m_r", "rxesc.m1", "motor_r.terminals", AWG["motor"], "motor", SLACK["short"], {})]


# make_spec tables: weapon shaft, web floors, hub pivots, electronics placements, press-fit interference, belt geometry
WSHAFT = dict(r=2.5, len=30.1, x=3.65)                  # GR1507 shaft: radius, length, start in the motor frame
WEB = dict(spider=0.8, disc=0.9, fork=1.05)             # min_web_mm the designer owns (STEP measures the same webs)
HUB_PIVOT_X = dict(rear=41.6, front=34.5)               # |X| of each hub's revolute pivot
ELEC = dict(battery=(-11.81, -5.4, 12.0), rxesc=(8.67, -3.0, 15.3), wesc=(8.63, -7.25, 10.6), switch_yz=(-5.6, 14.25))   # catalog origins (STEP envelopes)
STATOR_DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))        # stator screw directions on the bolt circle (bolt_wm0..3)
FILLET_REAR_X = 26.77   # |X| where the squared N10 gearbox-plate seat meets its seat arc at the rear wall (measured on our section z=10; RV01 26.5)
SWX_DEV_R = 1.5   # reference_cad deviation radius round each switch pilot (hole shifted 0.45 from the STEP)
SW_SCREW_Y, SW_BOLT_Z, TOP_BOLT_Z = (1.9, -13.1), 16.0, 20.4  # switch screws (Y, head Z) and the top-panel screw head plane
PRESS = dict(hub=0.05, tyre=0.3, micro=0.2, nut=0.05, shaft=0.02, bearing=0.05, pack=0.1)   # press-fit interference per joint, mm
BELT_R, BELT_r = 7.95, 4.2   # O-ring centreline radii: rear / front hub groove floor (7.45, 3.7) + half the 1.0 cs
BELT_X = dict(centre=31.25)                                              # |X| of the O-ring centreline (hub groove centre)
O_RING = (45, 1.0)                                      # stock O-ring ID x cross-section


# intent-probe parameters (rear hub / tyre / nut / seat) and the TPU-print exceptions of the chassis wall
HUB_PROBE_X = 35.0                                      # |X| of the keyed-bore probe point (inside the bore, off its centre line)
HUB_BORE_SPAN, TYRE_SPAN = (30.5, 40.5), (32.5, 42.0)   # |X| of the hub's blind D-bore and of the tyre seat
TYRE_ID, TYRE_STRETCH, NUT_MOVE, WHEEL_MIN_GAP = 13.0, 1.0, 0.3, 1.0   # relaxed F1 tyre ID, its stretch over the crown, nut play, wheel-to-armour gap
SEAT_PLAY, SEAT_TURN_DEG = 0.15, 2.0                      # motor boss play in the keyhole, shaft turn it allows
WALL_MIN = 1.8                                            # printed wall floor: 4+ perimeters on a 2 mm wall
WALL_EXCEPT = [[[-29.6, -37.7, 4.6], [29.6, -35.4, 17.5]], [[-33.0, -38.0, 0.0], [33.0, 44.0, 4.6]]]   # rear truss and base lip (STEP RV01)
FILLET_H, ROTOR_CLEAR = 10.0, 2.0                         # inside-corner fillet probe height; lead-to-rotor clearance


BRG = dict(od_r=4.0, w=2.5, bore_r=2.5, x=-14.75)   # MR85ZZ 5 x 8 x 2.5, centred in the RV02 seat


REF_BOM = [   # RVRN 2.0 STEP part list (research/rvrn_step/INDEX.txt); one row per joint or part family
    dict(role="FS8: base panel 5 x M2 CSK into heat-sets", match=["bolt_b*"], count=5, designation="M2x6", head="countersunk", threads_into="insert"),
    dict(role="FS1 M2 heat-sets (floor)", kind="part", match=["insert_b*", "insert_t*"], count=9, catalog="heatset_m2_4"),
    dict(role="FS9: mount to standoff 2 x M3x12 CSK alu (axle standoff)", match=["bolt_u?a"], count=2, designation="M3x12", head="countersunk", threads_into="standoff", material="aluminium"),
    dict(role="FS9: mount to nose standoff 2 x M3 CSK alu", match=["bolt_u?b"], count=2, designation="M3x14", head="countersunk", threads_into="standoff", material="aluminium",
         deviation="M3x14 instead of the STEP's M3x12: through mount and lug, 12 mm engages 3.9 mm of the 15 mm standoff (< 1.5 d)"),
    dict(role="top panel: 4 x M2 CSK thread-forming (not in the STEP; its countersunk holes are)", match=["bolt_t*"], count=4, designation="M2x5", threads_into="insert",
         deviation="the STEP top panel has 4 countersunk corner holes but no screws; 4 M2x4 CSK thread-forming screws added so the Ti panel cannot peel off"),
    dict(role="side panel to standoff ends: 4 x M3 CSK (STEP M3x8)", match=["bolt_s?a", "bolt_s?b"], count=4, designation="M3x10", head="countersunk", threads_into="standoff",
         deviation="M3x10 instead of the STEP's M3x8: 8 mm engages 4.2 / 2.7 mm of standoff thread, under 1.5 d in aluminium"),
    dict(role="side panel to chassis: 2 x M3x8 CSK into thin nuts", match=["bolt_s?c"], count=2, designation="M3x8", head="countersunk", threads_into="nut"),
    dict(role="M3 thin nuts (BS EN 24036)", kind="part", match=["nut_c*"], count=2, catalog="nut_m3_thin"),
    dict(role="RV11 25 mm + RV10 15 mm alu standoffs", kind="part", match=["so_*"], count=4, material="aluminium"),
    dict(role="GR1507 weapon motor", kind="part", match=["weapon_motor"], count=1, catalog="gr1507"),
    dict(role="Motor back spacer", kind="part", match=["motor_spacer"], count=1),
    dict(role="spider + 2 Drisk_floating_3 + Drisk_spacer_alt_x", kind="part", match=["spider", "disc_a", "disc_b", "dspacer"], count=4),
    dict(role="fork_5 x 2", kind="part", match=["fork_*"], count=2),
    dict(role="RV17/18 wedgelets", kind="part", match=["wedgelet_*"], count=2, material="tpu"),
    dict(role="RV23/24 side panels", kind="part", match=["side_*"], count=2, material="tpu"),
    dict(role="Top panel 0.9 sheet", kind="part", match=["top_panel"], count=1),
    dict(role="RV15 BBB antweight switch", kind="part", match=["power_switch"], count=1, catalog="switch_bbb_ant_rvrn2"),
    dict(role="RV16 Turnabot 2S 180 mAh", kind="part", match=["battery"], count=1, catalog="lipo_2s_180_turnabot"),
    dict(role="RV13 Malenki nano", kind="part", match=["rxesc"], count=1, catalog="malenki_nano_rvrn2"),
    dict(role="RV14 brushless ESC", kind="part", match=["wesc"], count=1, catalog="bbb_ant_esc_rvrn2"),
    dict(role="RV12 N10 2200 rpm x 2", kind="part", match=["motor_l", "motor_r"], count=2, catalog="n10_2200rpm_spicy"),
    dict(role="drisk stack: 4 x M2 into the spider (not in the STEP, holes are)", match=["bolt_d*"], count=4, designation="M2", threads_into="spider",
         deviation="the STEP leaves the r14 stack holes empty; 4 M2x14 added from the back, tapped into the spider (r0.8 tap holes there, the STEP r1.1 clearance elsewhere): no nuts, nothing invented beyond the screws"),
    dict(role="spider to bell: 4 x M2 (not in the STEP)", match=["bolt_p*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the r4.5 holes only"),
    dict(role="stator: 4 x M2 (not in the STEP)", match=["bolt_wm*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the RV03 counterbores only"),
    dict(role="switch: 2 x M2 into the deck pilot holes (not in the STEP)", match=["bolt_sw*"], count=2, designation="M2",
         deviation="the STEP has the two 1.7 pilot holes but no screws"),
    dict(role="nitrile O-ring belts (not in the STEP; hub grooves are)", kind="part", match=["belt_l", "belt_r"], count=2),
    dict(role="battery lead: JST RCY", kind="wire", match=["w_bat_sw"], count=1, connector="jst_rcy"),
    dict(role="weapon phases: 3 x 2 mm bullets", kind="wire", match=["w_wesc_m"], count=1, connector="bullet2"),
]

REF_DIR = "/mnt/project-files/robot-cad/research/rvrn_step/parts"
DRISK_T = None


MICRO_T = {   # STEP Micro_slx_v1_0 instance placements (assembly frame), composed with REF_TO_WORLD
    "l": [[0, -0.33, 0.944, -30.5], [0, 0.944, 0.33, 5.5], [-1, 0, 0, 35.5], [0, 0, 0, 1]],
    "r": [[0, -0.33, -0.944, -30.5], [0, 0.944, -0.33, 5.5], [1, 0, 0, -35.5], [0, 0, 0, 1]],
}


SLIT_DEV_X, SLIT_DEV_R, SLIT_DEV_YZ = 25.75, 2.5, ((46.4, 2.2), (44.4, 6.0), (43.1, 6.2), (44.2, 5.9), (48.5, 2.8))   # fork-tine slit sites in the wedgelet
TOE_DEV_YZ, TOE_DEV_R, TOE_DEV_X = (49.3, 1.4), 4.0, (19.5, 24.0, 28.0, 32.0, 36.5)                             # knife-toe land sites


# reference_cad tolerances and the reasoned-deviation sites (centres + radii of the regions allowed to differ from the STEP)
TOL = dict(tight=0.3, std=0.5, motor=0.6, wedge=0.8, loose=1.0)             # mm: surface deviation allowed per part class
VOL = dict(part=0.25, hub=0.15, motor=0.3, standoff=0.2, switch=0.5)          # fraction: volume mismatch allowed
REF_IOU_MIN = 0.9                                                              # silhouette IoU floor on every axis
COLUMN_TOP_Z, COLUMN_DEV_R, FOOT_DEV_Z, FOOT_DEV_R = 17.5, 3.0, 5.0, 4.0       # tub corner columns: top bore (centre of the 4 mm bore) and flared foot
KEYHOLE_DEV = (28.6, -30.6, 4.5)   # N10 keyhole U-slot (x, y, z=r)
LOBE_DEV, LOBE_DEV_R = (32.0, -13.5, 9.4), 3.5  # param: organic centroid of the lobe-tail trim vs STEP blobs
# param: end
CAGE_RIB_R, BASE_DEV_Z, PANEL_DEV_R, TOP_DEV_Z = 4.5, 4.5, 3.0, 19.95
NOSE_DEV, NOSE_DEV_R = (MNT_IN + 2.0, SB[0] + 1.5, SB[1] - 1.0), 5.0             # mount nose pad (|x|, y, z): thickened nose wall, deviation from the STEP nose
STATOR_DEV_X, TAP_DEV_R = 16.8, 2.0                                              # stator lead-in cone site; tap-hole sites


# robot-level declarations (data tables, not geometry): archetype ranges, targets, claims, allowed overlaps
ARCHETYPE_PARAMS = {"blade_lead_mm": [-30, -10], "axle_height_mm": [22, 25], "disc_thickness_mm": [14, 16], "disc_dia_mm": [44, 48], "teeth": [1, 1],
                    "tub_height_mm": [15, 19], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25],
                    "disc_floor_gap_mm": [5.0, 9.0]}   # STEP: R16.5 drisk on the 23.5 axle sweeps ~7 mm up; the forks and wedgelets work the floor, not the disc
TARGETS = {"length_mm": 107, "width_mm": 104.1, "disc_dia_mm": 46, "wheel_dia_mm": 21.5, "tol_mm": 3,
           "source": "RVRN 2.0 STEP (research/rvrn_step) measured in its assembly frame",
           "note": "GR1507 drisk (single tooth, 3+6+3 on a 3 mm spider) on 8 mm XALT mounts; N10 direct to 21.5 rear tyres, O-rings to 11 mm fronts"}
WEAPON_LOCK = {"type": "external_pin", "note": "pit safety pin handled outside the robot and pulled before a fight: not part of the build, no bore in RV02/RV03 (the STEP has none; user 2026-10-19)"}
REFERENCE_DOC = {"path": "REFERENCE.md", "must_mention": ["GR1507", "180 mAh", "Hardox", "JST RCY", "RV00", "XALT", "0.9 mm"],
                 "must_not_mention": ["through an aluminium spider", "2S ≈350 mAh LiPo"]}
ELECTRONICS = dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2)
MASS_LIMIT_G, SQUARE_MM = 150, 150      # AWS 2025 antweight limits
CLAIMS = [dict(id="c_mass", text=f"weighs {MASS_LIMIT_G} g or less", metric="mass_total_g", op="<=", value=MASS_LIMIT_G),
          dict(id="c_fit", text=f"fits the {SQUARE_MM} mm square", metric="footprint_mm", op="<=", value=SQUARE_MM)]
SHARP_OK = [dict(part="tub", near=[sg * 31.4, -11.7, 5.4], r_mm=1.0, reason="inside corner of the lobe-tail step is the side panel's own square relief edge (STEP RV23 diamond): the TPU panel conforms, rounding it in the tub would leave a 0.07 mm sliver") for sg in (1, -1)] + [dict(part="base_panel", near=[27.9, -21.5, 4.5], r_mm=3.0,
                 reason="screw boss is 0.3 mm tall (any taller breaks the reference silhouette), so its base fillet is capped at R0.25; the STEP pad base is R0.5")]
_ORING = "O-ring is rubber: it squashes 0.16 mm against the plain inner face of the STEP side panel (the STEP has no belt channel)"
_N10_FLAT = "the catalog N10 shaft is drawn round; the hub's D-flat sits on its flat"
ALLOW_OVERLAP = [dict(a="belt_l", b="side_l", max_depth_mm=0.3, reason=_ORING),
                 dict(a="belt_r", b="side_r", max_depth_mm=0.3, reason=_ORING),
                 dict(a="wshaft", b="wbearing", max_depth_mm=0.3, reason="shaft in the MR85 inner race (bearing modelled as one solid)"),
                 dict(a="wshaft", b="weapon_motor", max_depth_mm=2.6, reason="wshaft is the GR1507's own shaft, already drawn inside the catalog motor envelope"),
                 dict(a="motor_l", b="whub_rl", max_depth_mm=0.4, reason=_N10_FLAT),
                 dict(a="motor_r", b="whub_rr", max_depth_mm=0.4, reason=_N10_FLAT),
                 *[dict(a=f"insert_b{i}", b="tub", max_depth_mm=0.2, reason="heat-set insert: 3.5 OD melted into a 3.4 bore (interference by design)") for i in range(len(INS))],
                 *[dict(a=f"insert_{k}", b="tub", max_depth_mm=0.2, reason="heat-set insert: 3.5 / 3.2 OD melted into a 3.4 / 3.1 bore (interference by design)") for k in ("t0", "t1", "t2", "t3")],
                 *[dict(a=f"nut_c{n}", b="tub", max_depth_mm=0.1, reason="thin M3 nut pressed into a hex pocket 0.05 under its flats (captive)") for n in "lr"],
                 dict(a="wbearing", b="mount_l", max_depth_mm=0.1, reason="MR85 8.0 OD pressed into the RV02 7.9 printed seat (0.05 radial interference, the STEP seat size)")]
MODULE_NOTE = "RVRN quick change: 4 M3 out, both mounts with the drisk lift off the chassis tabs"


# real service order (Build Guide): side screws out, side panels off, then each wedgelet comes off its standoffs
# outward together with the fork whose tail sits in its cheek slot; then the standoffs slide out of the lugs.
TEARDOWN = [t for s, n in ((-1, "l"), (1, "r")) for t in (
    dict(parts=[f"wedgelet_{n}", f"fork_{n}"], dir=[s, 0, 0], reason="fork tail is pinned in the wedgelet cheek slot: they slide off the standoffs as one"),
    dict(parts=[f"so_b{n}"], dir=[s, 0, 0], reason="nose standoff slides out of the chassis lug once the mount screw is out"),
    dict(parts=[f"so_a{n}"], dir=[s, 0, 0], reason="axle standoff slides out of the lug with the front hub and wheel on it"))] + [
    # weapon module (fix-B): with both standoff pairs and the front end out, the module (both mounts, motor, drisk, lock)
    # slides forward off the chassis tabs as one unit (the tub's side lugs close the other five ways)
    dict(parts=["mount_r"], dir=[0, 1, 0], reason="RV02/RV03 with the motor and drisk slide forward off the chassis tabs as one quick-change module")]

# bench teardown of the module with RV03 held: RV02 off the shaft end, drisk off the shaft, motor off its 4 stator screws
MODULE_TEARDOWN = [
    dict(parts=["mount_l", "bolt_ula", "bolt_ulb"], dir=[-1, 0, 0], reason="RV02 slides outboard off the shaft end, its CSK screws captive"),
    dict(parts=["spider"], dir=[-1, 0, 0], reason="drisk (spider, discs, spacer, stack bolts) slides off the GR1507 shaft once the 4 bell screws are out"),
    dict(parts=["weapon_motor"], dir=[-1, 0, 0], reason="GR1507 leaves inboard-left once the 4 stator screws are out")]


# the drisk is turned by hand before the nose screws (bolt_u?b) are drawn: in the STEP pose the eccentric rim and tooth flank
# pass within 2.1 mm of their line (heads r3.0); 160 deg about the axis puts the rim 3.07 mm off it, so the screws leave inward
SERVICE_TURN_DEG = 160.0
SERVICE_POSE = [dict(parts=["spider", "disc_a", "disc_b", "dspacer"] + [f"bolt_{c}{k}" for c in "pd" for k in range(N_STACK)],
                     axis_at=[0.0, WY, WZ], axis_dir=[1, 0, 0], deg=SERVICE_TURN_DEG,
                     reason="drisk turned by hand so the rim clears the nose screws; whole stack with its bolts moves as one")]

UNIT = 1          # unit direction-cosine norm (k^2 + h^2 = UNIT) for the belt tangent construction
BELT_DIGITS = 4   # decimals kept on belt path points in the spec



# --- hubs: rear RV21 (16 x 12) and front RV19 micro (9 x 9) revolve profiles, (x, radius) from the hub's inner face
HUB_FLANGE_T, HUB_GROOVE_C, HUB_GROOVE_W, HUB_GROOVE_CH = 0.7, 1.25, 1.1, 0.25          # flange thickness, O-ring groove centre / width, groove wall chamfer
RH_FLANGE_R, RH_GROOVE_R, RH_SEAT_R, RH_CROWN_H, RH_LIP_R, RH_LEN, RH_WALL_R, RH_WALL_T = 8.0, 7.45, 6.0, 1.0, 6.5, 12.0, 2.88, 0.2
RH_SEAT_RAMP = ((2.55, 6.9), (2.75, 6.35), (3.35, RH_SEAT_R))                           # flange-to-seat ramp
RH_SEAT_X, RH_CROWN_X, RH_SEAT_END, RH_LIP_X = (3.35, 5.25), (6.25, 8.25), 11.1, 11.3   # seat span, crown span, seat end, lip start
_g0, _g1 = HUB_GROOVE_C - HUB_GROOVE_W / 2, HUB_GROOVE_C + HUB_GROOVE_W / 2
REAR_HUB_PROFILE = ((0.0, 0.0), (0.0, RH_FLANGE_R), (_g0, RH_FLANGE_R), (_g0 + HUB_GROOVE_CH, RH_GROOVE_R), (_g1 - HUB_GROOVE_CH, RH_GROOVE_R),
                    (_g1, RH_FLANGE_R), (_g1 + HUB_FLANGE_T, RH_FLANGE_R), *RH_SEAT_RAMP, (RH_SEAT_X[1], RH_SEAT_R),
                    (RH_CROWN_X[0], RH_SEAT_R + RH_CROWN_H), (RH_CROWN_X[1], RH_SEAT_R + RH_CROWN_H), (RH_CROWN_X[1] + RH_CROWN_H, RH_SEAT_R),
                    (RH_SEAT_END, RH_SEAT_R), (RH_LIP_X, RH_LIP_R), (RH_LEN, RH_LIP_R), (RH_LEN, RH_WALL_R), (RH_LEN - RH_WALL_T, RH_WALL_R),
                    (RH_LEN - RH_WALL_T, 0.0))
RH_D = dict(r=1.6, flat=0.9, arc_n=60, flat_n=27, crown=0.02)                           # D-bore: radius, flat height above the axis, facet counts, flat crown
RH_BORE_X, RH_NUT_X, RH_NUT_HALF, RH_NUT_Z, RH_GRUB_X, RH_GRUB_ENGAGE = 29.0, 41.0, 2.05, (2.4, 4.4), 34.3, 0.9   # |X| of bore start / slot end, slot half-width, slot z above axis, grub, grub tip past the flat
RH_ORIGIN_X = 30.0                                                                      # |X| of the hub inner face
FH_FLANGE_R, FH_SEAT_R, FH_BORE_R, FH_LEN, FH_RAMP, FH_SEAT_X, FH_GROOVE_FLOOR = 4.5, 3.7, 2.7, 9.0, 0.4, (2.9, 7.9), (0.93, 1.57)
FRONT_HUB_PROFILE = ((0.0, FH_BORE_R), (0.0, FH_FLANGE_R), (HUB_FLANGE_T, FH_FLANGE_R), (0.75, 3.96), (FH_GROOVE_FLOOR[0], FH_SEAT_R),
                     (FH_GROOVE_FLOOR[1], FH_SEAT_R), (1.75, 3.96), (1.8, FH_FLANGE_R), (2.5, FH_FLANGE_R), (2.5, FH_SEAT_R + FH_RAMP),
                     (FH_SEAT_X[0], FH_SEAT_R), (FH_SEAT_X[1], FH_SEAT_R), (FH_SEAT_X[1] + FH_RAMP, FH_SEAT_R + FH_RAMP),
                     (FH_SEAT_X[1] + FH_RAMP, FH_FLANGE_R), (FH_LEN, FH_FLANGE_R), (FH_LEN, FH_BORE_R))
FH_ORIGIN_X = 30.0                                                                      # |X| of the front hub inner face
STANDOFF_BORE_R, TYRE_SECTION_STEP = 1.25, 10                                           # standoff through-bore radius; shoulder arc step (deg)


MNT_TIP_DEV, MNT_TIP_DEV_R = (MNT_IN + 2.0, 12.5, MNT_TOP_Z - 0.2), 4.0   # mount notch-top wedge thickened to a printable wall (|x|, y, z)



# --- side.py: fork, hubs, side-panel width (fix-B lint) ---
FK_X = {1: (24.5, 26.0), -1: (-26.5, -25.0)}      # fork X slab per side sign: asymmetric in the STEP (fork_5_1 24.5..26.0, fork_5_2 -26.5..-25.0), so not a mirror
FK_EYE, FK_EYE_R, FK_PIN_R, FK_SB_R = (36.3, 6.3), 1.95, 0.8, 2.65   # eye on the nose standoff, pin hole, standoff hole
FK_RES, FK_RES_PIN, FK_RES_BUF = 48, 24, 8        # circle / buffer segment counts
FK_BLADE = [(35.0, 4.9), (36.1, 8.2), (41.0, 8.25), (66.68, 1.49), (51.75, 0.75), (39.0, 0.75), (38.0, 1.5)]   # param: organic fork blade outline (measured, STEP)
FK_ROUND = (0.3, 0.5)                             # outer / inner corner radius of the blade
FK_TIP = [(60.0, 1.27), (66.68, 1.49), (60.0, 2.5)]   # param: organic sharp-tip wedge
FK_TIP_R = 0.15                                   # tip join radius (> kerf)
FK_WIN = [(44.15, 2.75), (54.0, 2.75), (44.65, 5.42)]   # param: organic lightening window
FK_WIN_R = 0.3
FK_LAND_R = 0.15                     # land corners round r0.15 (> kerf)
FK_LAND = [(64.0, 1.2), (66.68, 1.27), (66.68, 1.72), (64.0, 1.95)]   # param: organic 0.45 mm kerf land
FK_TILT = -1.1                                    # deg, left fork nose-down about its standoff
FKS_STEPS, FKS_DY = 24, 0.5                       # fork-slot sweep up out of the ramp
FKS_CLIP = (42.0, -1, 80, 30)                     # x0, y0, x1, y1 of the sweep clip box
HUB_X0 = 30.0                                     # hub inboard face X
RH_PROF = [(0.0, 0.0), (0.0, 8.0), (0.7, 8.0), (0.95, 7.45), (1.55, 7.45), (1.8, 8.0), (2.5, 8.0), (2.55, 6.9), (2.75, 6.35), (3.35, 6.0),
           (5.25, 6.0), (6.25, 7.0), (8.25, 7.0), (9.25, 6.0), (11.1, 6.0), (11.3, 6.5), (12.0, 6.5), (12.0, 2.88), (11.8, 2.88), (11.8, 0.0)]   # param: organic RV21 hub revolve profile (STEP)
RH_DR, RH_FLAT, RH_CROWN = 1.6, 0.9, 0.02         # D-bore radius, flat height above axis, flat crown
RH_NARC, RH_NFLAT = 60, 27                        # D-bore arc points / flat divisions
RH_SEAT_R, RH_GRUB_X, RH_GRUB = 6.0, 34.3, "M2x5" # tyre-seat radius, grub X, grub fastener
RH_GRUB_DIR = (0, 0, -1)
RH_X_IN, RH_X_OUT, RH_SLOT_HW, RH_SLOT_Z = 29.0, 41.0, 2.05, (2.4, 4.4)   # D-bore/nut-slot X span, slot half width, slot Z span
FH_PROF = [(0.0, 2.7), (0.0, 4.5), (0.7, 4.5), (0.75, 3.96), (0.93, 3.7), (1.57, 3.7), (1.75, 3.96), (1.8, 4.5), (2.5, 4.5), (2.5, 4.1), (2.9, 3.7),
           (7.9, 3.7), (8.3, 4.1), (8.3, 4.5), (9.0, 4.5), (9.0, 2.7)]   # param: organic RV19 hub revolve profile (STEP)
# param: end
SPW_Y = (-16.0, -12.0, 11.0, 15.0)                # side-panel width stations along Y
SPW_BUMP, SPW_BUMP_YC, SPW_BUMP_YH, SPW_BUMP_ZC, SPW_BUMP_ZH = 0.7, -5.0, 6.0, 7.5, 5.0   # nut-lobe swell: height, Y centre/half, Z centre/half
__all__ = [n for n in dir() if not n.startswith('__')]   # last line: exports every parameter above (incl. the FK_* and hub blocks)
