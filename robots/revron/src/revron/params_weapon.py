"""Revron params: drisk stack, GR1507 motor, weapon mounts RV02/RV03, disc / spider / spacer. Re-exported by params.py."""
from .params_chassis import *  # noqa: F401,F403
# GR1507 catalog features the weapon mates to (robot/catalog.py, motor-local: +X = bell top, -X = stator base)
from robot.catalog import BELL_TOP_X, BELL_WALL_R, BELL_SCREW_R, BELL_SCREW_PHASE   # noqa: E402
# One switch swaps the weapon motor model: "datasheet" = real GR1507 (GEPRC drawing: 12-slot wound stator, 4-spoke chamfered cap, side wire exit, M5 thread 8 mm),
# "step" = the simplified RVRN 2.0 STEP motor (solid r4 core, flat cap, no stator, thread 10 mm). Same part ids, mount points and screws in both.
MOTOR_VARIANT = os.environ.get("REVRON_MOTOR_VARIANT", "datasheet")
MOTOR_VARIANTS = {"datasheet": dict(stator="gr1507", can="gr1507_can", thread_len=8.0), "step": dict(stator="gr1507_step", can="gr1507_step_can", thread_len=10.0)}
MOTOR = MOTOR_VARIANTS[MOTOR_VARIANT]
# weapon frame: on the spin axis (WY, WZ) at the robot centre plane; the GR1507 sits in it with its catalog +X (bell top) turned to world -X
W_FRAME = (0.0, WY, WZ)
MOTOR_FLIP = (0, 0, 180)             # catalog -> weapon frame: half a turn about Z, so the stator base faces RV03 (+X)
BELL_CAP_X = -BELL_TOP_X[1]          # world X of the bell's cap face (the flip mirrors catalog X)

# master parameters of the stack: plate thicknesses; the spider's inner face sits on the bell cap and every X span below is chained from it
SPIDER_T, DISC_T, SPACER_T = 3.0, 3.0, 6.0
STACK_X0 = round(BELL_CAP_X - SPIDER_T, 6)   # spider outer face: one spider thickness out from the cap
DR_X, _x = {}, STACK_X0
for _n, _t in (("spider", SPIDER_T), ("disc_a", DISC_T), ("spacer", SPACER_T), ("disc_b", DISC_T)):
    DR_X[_n] = (_x, _x + _t)       # spider | disc_a | spacer | disc_b, each flush on the previous one
    _x += _t
DR_ROT = BELL_SCREW_PHASE            # drisk phase about the axis: the spider is clocked to the bell's screw pattern (STEP Drisk_V4 placement)
DISC_R, DISC_ECC, DISC_ECC_A = 16.5, 0.5, -40.0   # eccentric rim: R16.5 centred 0.5 mm towards -40 deg (balances the tooth)
TOOTH_R, TOOTH_A = 23.0, 134.8
BOLT_R, HUB_R = 14.0, BELL_SCREW_R   # stack-bolt circle; spider-to-bell screws on the bell's own screw circle (radii about the weapon axis)
N_STACK = 4                          # bolts / lobes / windows per stack, 90 deg apart
# motor GR1507: axis X, stator base X 8.4..10.4 on the right mount via the back spacer X 11.9..13.4
MNT_OUT, MNT_SLAB = MNT_IN + MNT_T, MNT_IN + MNT_SLAB_T
MNT_FRAME = dict(r=(MNT_IN, WY, WZ), l=(-MNT_IN, WY, WZ))   # each mount's frame: its inner face on the weapon axis
# GR1507 shaft and its outboard MR85ZZ (5 x 8 x 2.5) in the RV02 seat
SHAFT_CLR = 0.1                      # radial clearance round the shaft (RV03 hole, spider bore)
BRG_RECESS, BRG_PRESS = 0.1, 0.05    # MR85 sits this far below the RV02 inner face (race clear of the spider); seat interference
SHAFT_INTO_RECESS = 1.3              # the threaded end stands this far past the RV02 slab into the nut recess
WSHAFT = dict(r=2.5, len=30.1, x_end=-(MNT_SLAB + SHAFT_INTO_RECESS), thread_pitch=0.8, thread_depth=0.3, thread_len=MOTOR["thread_len"], chamfer=0.4)   # GR1507 shaft: radius, length, free end in RV02's nut recess
SHAFT_D = 2 * WSHAFT["r"]
BRG = dict(od_r=4.0, w=2.5, bore_r=WSHAFT["r"])   # MR85ZZ: the shaft runs in its bore
BRG["x"] = -(MNT_IN + BRG_RECESS + BRG["w"] / 2)   # centred in the RV02 seat
BRG_SEAT_R, NUT_RECESS_R = BRG["od_r"] - BRG_PRESS, 6.0   # MR85 seat (pressed: 7.9 STEP), shaft nut recess
STATOR_PCD, BOSS_OVER = 12.0, 0.01        # stator M2 bolt circle; boss overshoots the battered plane before it is split
MNT_SCREW = ("M3x12", "M3x14")           # mount-to-standoff CSK screws at SA, SB
MNT_SCREW_FIT = "loose"                  # ISO 273 loose clearance: the screws have slack, the notch face takes the hit first
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
BSP_T = 1.5                          # printed spacer between the stator base and the right mount
BSP_X = (MNT_IN - BSP_T, MNT_IN)
STAT_HOLE_R, CB_R, CB_CONE_X = 1.12, 2.25, (16.4, 17.15)   # RV03 stator screw clearance d2.24, d4.5 counterbore, its cone
STATOR_ARMS_DEG = (0, 180, 90, 270)   # the GR1507 base cross arms, in bolt_wm0..3 order
STATOR_DIRS = tuple((round(math.cos(math.radians(a))), round(math.sin(math.radians(a)))) for a in STATOR_ARMS_DEG)   # stator screw directions on the bolt circle



WSEG_LO, WSEG_FINE, WSEG_MID, WSEG_HI, WSEG_FN, WSEG_MAX, WSEG_ARC, WSEG_ARC_S = 24, 32, 48, 64, 96, 128, 40, 12   # circle / arc tessellation of the 2D profiles
# weapon mount RV02 (left, shaft end) / RV03 (right, stator): per-side master parameters (STEP measurements)
MNT_SIDE = dict(
    r=dict(top_r=10.0, notch_y=10.17, rim_end=-14.5, slab_eps=0.02, face=(24.166, 0.154, 0.0404)),   # a, kz, ky of |X| = a - kz*Z - ky*Y
    l=dict(top_r=7.0, notch_y=9.0, rim_end=-5.0, slab_eps=0.0, face=(23.203, 0.1701, 0.0158)))
MNT_TOP_Z = CH_Z1                        # top of the rear notch: the teardrop's tangent line starts here
TAB = dict(y0=CH_Y1, z0=5.35, h=8.2, y1=26.5, cham=1.0)   # chassis tab the notch drops over: rear Y, floor Z, height, front-face Y, front chamfer
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
BSP = dict(r=10.0, bore_r=4.0, win_in=5.5, win_out=8.5, half_deg=24.5, round_in=1.25, round_out=1.0, hole_r=1.1, phase=45.0)   # motor back spacer (Motor_back_spacer_1.stl section fit)


DISC_BORE_RES = 4                       # bore polygon samples per degree
DOG = dict(r=12.0, rise=1.52, t0=5.0, t1=18.0, t2=55.0)       # bore dogs (90 deg pitch): steep rise t0..t1, long ramp back to t2
DISC_BORE_ROUND, DISC_HOLE_R_WIN = 0.5, 0.44                    # bore corner rounding; balance window corner radius
DISC_BAL_PTS = [(-13.2, 4.85), (-13.2, 9.08), (-11.68, 7.65)]    # param: organic balance-window hull corners (measured, STEP)
TOOTH_PTS = [(-11.0, 11.6), (-8.0, 8.0)]   # param: organic tooth flank/root inner corners (measured, STEP)
TOOTH_BACK = (-16.25, 15.0)                # param: organic top of the tooth back face (measured, STEP); its foot is the rim tangent point (smooth join, visual.faceting)
# param: end
DISC_ROUND = dict(r_out=0.2, r_in=0.7)                           # tooth tip land (0.4 laser-cuttable) and root fillet


SPIDER = dict(r=14.2, lobe_r=2.3, round_in=0.8, win_r=11.7, win_off=2.3, win_far=20.0, hub_r=6.0, win_round=1.0, bore_r=WSHAFT["r"] + SHAFT_CLR)   # bore on the shaft collar; window: r1 corners, inner arc r6 (STEP spider_1 section, visual.fillet_ref / silhouette)


SPACER = dict(r=16.0, bore_r=BELL_WALL_R[1] + SHAFT_CLR, win_in=11.4, win_out=14.5, half_deg=36.0, win_round=1.0, phase=45.0)
# weapon phase leads (fix-B-leads): RVRN 2.0 runs them free over the lug (RV03 / RV01 have no lead hole or groove). Here the 3 AWG24 leads fan out
# flat through the 1.5 mm stator-to-spacer gap to below the back spacer, twist into one bundle and snap into a C-groove in RV03's inner face that
# runs parallel to the boss's standoff line (so the whole groove sits in the 8 mm boss), back to the lug top, where they drop into the tub.
LEAD_OD, LEAD_TWIST = 1.6, 0.1                                  # AWG24 silicone OD (wire_review.wire_od); hand-twist allowance on the bundle radius
LEAD_BUNDLE_R = LEAD_OD * (0.5 + 1 / math.sqrt(3)) + LEAD_TWIST  # 3 touching round leads: circumscribed radius (wire_review.bundle_radius), 1.82
LEAD_GROOVE_R = LEAD_BUNDLE_R + 0.2                             # groove radius: bundle + printed-clearance
LEAD_MOUTH = LEAD_OD * (1 + math.sqrt(3) / 2)                   # mouth at the inner face = the bundle's narrow width (one lead over two, 2.99): it snaps in flat side first, the round twist cannot fall out
LEAD_LIP = 0.9                                                  # the mouth is a LEAD_MOUTH slot through a lip this thick (one fdm wall, mfg.thin_wall): square lip edges, no knife edge where the round groove meets the face
LEAD_GROOVE_X = MNT_IN + LEAD_LIP + math.sqrt(LEAD_GROOVE_R ** 2 - (LEAD_MOUTH / 2) ** 2)   # groove axis behind the inner face: the slot meets the round groove in the mouth chord
LEAD_FLOOR_W = 0.3                                              # flat strip on the groove floor (no pole where the round ends close)
LEAD_ROUND = 1.5                                                # groove lip / channel chord rounding (mfg.sharp_internal_corner r >= 1)
LEAD_LIG = 0.6                                                  # groove edge above the boss line (floor in the 8 mm boss); also puts the front end clear of the back spacer ring (test_lead_route)
LEAD_Y_REAR = 19.0                                              # groove rear end: its ball end keeps >= LEAD_LIP (one fdm wall, mfg.thin_wall) under RV03's top tangent edge
LEAD_FAN_X = sum(BSP_X) / 2                                     # the bundle turns into the groove round the back spacer rim, mid its thickness (the stator-side gap is 1.5 mm, too thin for it)
LEAD_DEV_R, LEAD_DEV_MAX_MM3 = 3.0, 520                        # reference_cad capsule waiver along the groove: capsule radius (mouth + lip), cap on the volume it may explain (groove ~340 mm3)


def boss_line_z(y):
    """Z of the boss's lower edge (the line from the notch top to the nose, see mount._mount_clip) at Y."""
    return MNT_TOP_Z + (y - TAB["y0"]) * (BOSS_Z - MNT_TOP_Z) / (BOSS_NOSE_Y - TAB["y0"])


def lead_groove_ends():
    """((y, z) rear, (y, z) front) of the phase-lead groove axis in RV03: parallel to the boss line, LEAD_GROOVE_R + LEAD_LIG above it,
    from LEAD_Y_REAR to straight below the weapon axis (WY), where the leads come out of the stator."""
    off = LEAD_GROOVE_R + LEAD_LIG
    return tuple((y, boss_line_z(y) + off) for y in (LEAD_Y_REAR, WY))


_LG = lead_groove_ends()
PHASE_VIA = [[11.8, 14.5, 16.0]] + [[LEAD_GROOVE_X, y, z] for y, z in _LG] + [[LEAD_FAN_X, WY, _LG[1][1]]]   # tub inside -> groove rear -> groove front -> lead fan under the spacer


__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
