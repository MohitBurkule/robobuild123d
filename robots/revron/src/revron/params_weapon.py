"""Revron params: drisk stack, GR1507 motor, weapon mounts RV02/RV03, disc / spider / spacer. Re-exported by params.py."""
from .params_chassis import *  # noqa: F401,F403
# GR1507 catalog features the weapon mates to (robot/catalog.py, motor-local: +X = bell top, -X = stator base)
from robot.catalog import bell_dims, STATOR_BACK_X, BELL_SCREW_R, BELL_SCREW_PHASE, BEARINGS, SHAFT_STUB_R, _gr1507_base   # noqa: E402
from robot.cad import fastener_catalog as _fc   # noqa: E402
# One switch swaps the weapon motor model: "datasheet" = real GR1507 (GEPRC drawing: 12-slot wound stator, 4-spoke chamfered cap, side wire exit, M5 thread 8 mm),
# "step" = the simplified RVRN 2.0 STEP motor (solid r4 core, flat cap, no stator, thread 10 mm). Same part ids, mount points and screws in both.
MOTOR_VARIANT = os.environ.get("REVRON_MOTOR_VARIANT", "datasheet")
MOTOR_VARIANTS = {"datasheet": dict(stator="gr1507", can="gr1507_can", thread_len=8.0), "step": dict(stator="gr1507_step", can="gr1507_step_can", thread_len=10.0)}
MOTOR = MOTOR_VARIANTS[MOTOR_VARIANT]
BELL_WALL_R, BELL_TOP_X = bell_dims(MOTOR_VARIANT)   # datasheet: 17.1 mm body, cap top 6.7 above the base back; step: the STEP's 5.2
# weapon frame: on the spin axis (WY, WZ) at the robot centre plane; the GR1507 sits in it with its catalog +X (bell top) turned to world -X
W_FRAME = (0.0, WY, WZ)
MOTOR_FLIP = (0, 0, 180)             # catalog -> weapon frame: half a turn about Z, so the stator base faces RV03 (+X)
MOTOR_PLACE_TOL = 0.8               # reference_cad placement tolerance of the motor: drawing-true bell cap is 1.5 mm above the STEP can (half of it shifts the bbox centre)
BELL_CAP_X = -BELL_TOP_X[1]          # world X of the bell's cap face (the flip mirrors catalog X)

# master parameters of the stack: plate thicknesses; the spider's inner face sits on the bell cap and every X span below is chained from it
SPIDER_T, DISC_T = 3.0, 3.0
SPACER_T = 2 * DISC_T               # the printed spacer is two disc gauges thick (STEP 6.0)
STACK_X0 = round(BELL_CAP_X - SPIDER_T, 6)   # spider outer face: one spider thickness out from the cap
DR_X, _x = {}, STACK_X0
for _n, _t in (("spider", SPIDER_T), ("disc_a", DISC_T), ("spacer", SPACER_T), ("disc_b", DISC_T)):
    DR_X[_n] = (_x, _x + _t)       # spider | disc_a | spacer | disc_b, each flush on the previous one
    _x += _t
DR_ROT = BELL_SCREW_PHASE            # drisk phase about the axis: the spider is clocked to the bell's screw pattern (STEP Drisk_V4 placement)
DISC_R, DISC_ECC, DISC_ECC_A = 16.5, 0.5, -40.0   # eccentric rim: R16.5 centred 0.5 mm towards -40 deg (balances the tooth)
TOOTH_REACH, TOOTH_A = 6.5, 134.8    # masters: tooth tip reach past the rim and its angle in the drisk frame
TOOTH_R = DISC_R + TOOTH_REACH        # tooth tip radius (STEP 23.0)
BOLT_R, HUB_R = 14.0, BELL_SCREW_R   # stack-bolt circle; spider-to-bell screws on the bell's own screw circle (radii about the weapon axis)
N_STACK = 4                          # bolts / lobes / windows per stack, 90 deg apart
STACK_BOLT_D = 2.0                   # stack screw size (M2): its tap / clearance holes come from the fastener catalog
STACK_TAP_R, STACK_CLR_R = _fc.tap_drill(STACK_BOLT_D) / 2, _fc.clearance(STACK_BOLT_D, "close") / 2
STACK_WALL = 1.5                     # master: material ring every stack plate keeps round a hole, bore or rim (lobes, hub ring, spacer rings)
HALF_PITCH = 180.0 / N_STACK         # windows sit midway between the bolts
# motor GR1507: axis X, stator base X 8.4..10.4 on the right mount via the back spacer X 11.9..13.4
MNT_OUT, MNT_SLAB = MNT_IN + MNT_T, MNT_IN + MNT_SLAB_T
MNT_FRAME = dict(r=(MNT_IN, WY, WZ), l=(-MNT_IN, WY, WZ))   # each mount's frame: its inner face on the weapon axis
# GR1507 shaft and its outboard MR85ZZ (5 x 8 x 2.5) in the RV02 seat
SHAFT_CLR = 0.1                      # radial clearance round the shaft (RV03 hole, spider bore)
BRG_RECESS, BRG_PRESS = 0.1, 0.05    # MR85 sits this far below the RV02 inner face (race clear of the spider); seat interference
SHAFT_INTO_RECESS = 1.3              # the threaded end stands this far past the RV02 slab into the nut recess
SHAFT_R = SHAFT_STUB_R               # GR1507 shaft radius (5 mm, motor catalog)
WSHAFT = dict(r=SHAFT_R, len=-STATOR_BACK_X + MNT_SLAB + SHAFT_INTO_RECESS, x_end=-(MNT_SLAB + SHAFT_INTO_RECESS), thread_pitch=0.8, thread_depth=0.3, thread_len=MOTOR["thread_len"], chamfer=0.4)   # GR1507 shaft: radius, length (back flush with the base), free end in RV02's nut recess
SHAFT_D = 2 * SHAFT_R
BRG_NAME = "mr85"                   # outboard bearing designation (robot.catalog.BEARINGS): bore, OD, width
_bd, _bod, _bw = BEARINGS[BRG_NAME]
BRG = dict(od_r=_bod / 2, w=_bw, bore_r=_bd / 2)   # MR85ZZ from the catalog: the shaft runs in its bore
BRG["x"] = -(MNT_IN + BRG_RECESS + BRG["w"] / 2)   # centred in the RV02 seat
BRG_SEAT_R, NUT_RECESS_R = BRG["od_r"] - BRG_PRESS, 6.0   # MR85 seat (pressed: 7.9 STEP), shaft nut recess
STATOR_PCD = 2 * math.hypot(*_gr1507_base()["cut"][0]["at"][1:])   # stator M2 bolt circle: the motor catalog's base holes
BOSS_OVER = 0.01                     # boss overshoots the battered plane before it is split
MNT_SCREW = ("M3x12", "M3x14")           # mount-to-standoff CSK screws at SA, SB
MOUNT_VARIANT = os.environ.get("REVRON_MOUNT_VARIANT", "original")   # "original" = RV02/RV03 as the STEP draws them; "printable" = nose pad, thickened notch tip, relieved corners, loose screw holes (improvements, not parity)
PRINTABLE = MOUNT_VARIANT == "printable"
MNT_SCREW_FIT = "loose" if PRINTABLE else "close"   # ISO 273: loose slack so the notch face takes the hit first; close = the STEP's d3.2 holes
RV03_BORE_R = SHAFT_R + (SHAFT_CLR if PRINTABLE else 0.0)   # RV03 centre hole: the STEP d5.0 (the shaft ends at the stator base, short of RV03); printable adds the shaft clearance
STATOR_SCREW_FIT = "normal" if PRINTABLE else "close"   # RV03 stator M2 holes: close = the STEP d2.2 (ISO 273 close); normal = d2.4
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
BSP_T = 1.5                          # printed spacer between the stator base and the right mount
BSP_X = (MNT_IN - BSP_T, MNT_IN)
WM_LEN, WM_BITE = 8.0, 1.7           # stator screw M2x8 and the thread it must bite in the 2 mm base (0.8 d = 1.6, plus 0.1)
CB_R = 2.25                          # RV03 stator counterbore d4.5
CB_FLOOR_X = -STATOR_BACK_X + WM_LEN - WM_BITE   # its floor |X| (the button head seats here): the screw tip lands WM_BITE inside the base (STEP 17.15 gives only 1.25: declared deviation)
CB_CONE_X = (CB_FLOOR_X - 0.75, CB_FLOOR_X)      # the STEP's 0.75 lead-in cone under the counterbore (left out, see spec deviations)
CB_STEP_CONE_X = (16.4, 17.4)        # |X| span of the STEP's 45 deg cone (r1.1 -> r2.25): the stator-hole deviation waiver spans it
STATOR_ARMS_DEG = (0, 180, 90, 270)   # the GR1507 base cross arms, in bolt_wm0..3 order
STATOR_DIRS = tuple((round(math.cos(math.radians(a))), round(math.sin(math.radians(a)))) for a in STATOR_ARMS_DEG)   # stator screw directions on the bolt circle



WSEG_LO, WSEG_FINE, WSEG_MID, WSEG_HI, WSEG_FN, WSEG_MAX, WSEG_ARC, WSEG_ARC_S = 24, 32, 48, 64, 96, 128, 40, 12   # circle / arc tessellation of the 2D profiles
# weapon mount RV02 (left, shaft end) / RV03 (right, stator): the per-side master parameters of the one plate builder
# (STEP measurements): teardrop top radius about the axis, notch-top Y where its tangent starts, angle where the rim
# leaves for the front edge, and the battered outer face x = MNT_T - drop - lean*z - toe*y in the mount frame
# (x out from the inner face, y, z from the weapon axis): at the axis it sits `drop` below the full plate thickness,
# and leans in with height and towards the nose
MNT_SIDE = dict(
    r=dict(top_r=10.0, notch_y=10.17, rim_end=-14.5, batter=dict(drop=2.4084, lean=0.154, toe=0.0404)),
    l=dict(top_r=7.0, notch_y=9.0, rim_end=-5.0, batter=dict(drop=2.80265, lean=0.1701, toe=0.0158)))
MNT_TOP_Z = CH_Z1                        # top of the rear notch: the teardrop's tangent line starts here
TAB = dict(y0=CH_Y1, z0=5.35, h=8.2, y1=26.5, cham=1.0)   # chassis tab the notch drops over: rear Y, floor Z, height, front-face Y, front chamfer
MNT_NOTCH_GAP = 0.1                     # the notch's front face stands this far ahead of the tab's front face (STEP RV02/RV03 notch at Y 26.6)
NOSE_R = 3.25                           # nose arc round the SB standoff; it leaves the outline at the side's rim_end angle (the front edge is the common tangent of rim and nose: STEP RV02 -5, RV03 -14.5)
MNT_HEEL = dict(z=SB[1] - NOSE_R, step=0.4, back=1.8, z_hook=2.5, z_lip=4.5)   # rear foot hooked under the tab: flat underside (tangent to the nose arc), tip step, setback, hook and lip Z
MNT_NOTCH_UP = 2.0                      # the rear face above the tab leans back by this much over the last stretch to the top
BOSS_Z, BOSS_NOSE_Y = 6.34, 44.34          # the boss starts above the line from the notch top to (BOSS_NOSE_Y, BOSS_Z): STEP, it runs tangent to the nose arc to 0.4 um
NOSE_PAD_R = 4.1 if PRINTABLE else 0.0                        # local pad round the nose CSK: CSK cone radius (3.2) + a 0.9 mm printed wall (the STEP nose leaves 0.15 mm)
BIG = 60.0                              # a box edge bigger than any part, for the wedgelet's 2D half-plane clip (_mount_clip)
MNT_RELIEF_R = 1.0 if PRINTABLE else 0.0                      # concave corner relief of the profile (tub deck fillet, mfg corner relief)
MNT_CSK_CLEAR = 0.4 if PRINTABLE else 0.2   # extra cone diameter over the DIN 7991 head (dk 6.0): STEP cone d6.2; printable 0.4 floats the seated head so the notch bears a hit first
MNT_CSK_PROUD = 0.0 if PRINTABLE else 0.12   # ISO 10642 head seated on the STEP d6.2 cone stands this far out of the inner face (flush, it would cut 0.08 into the cone; flush_head allows 0.2)
MNT_TIP_WALL, MNT_TIP_REACH = (1.5 if PRINTABLE else 0.0), 3.0    # printed wall: the wedge where the rear notch meets the rim tangent is thickened upward to this within this reach of the notch top (rearmost point and underside unchanged: the underside rides on the chassis tab)


HOLE_FACE_RISE = 0.7                    # the battered face's highest point over a stator hole axis: the surface the hole is measured from
BSP = dict(r=MNT_SIDE["r"]["top_r"], bore_r=4.0, half_deg=24.6, round_in=2.0, round_out=1.0, phase=HALF_PITCH)   # motor back spacer: flush with RV03's teardrop rim, bore over the base hub
BSP.update(win_in=BSP["bore_r"] + BSP_T, win_out=BSP["r"] - BSP_T)   # windows leave a hub ring and a rim ring one spacer thickness wide


CORNER_R = 1.0                       # master: the stack's machined/printed inside-corner fillet (dog feet, spider and spacer windows)
# param: organic bore dog ramp profile (STEP section fit, per dog pitch): base r, rise, flank t0..t1, R ramp to t2, nose
DOG = dict(r=12.0, rise=1.9, t0=6.6, t1=13.1, t2=54.7, ramp_r=15.3, nose_r=2.0)
# param: end
DISC_BORE_ROUND, DISC_HOLE_R_WIN = CORNER_R, 0.44               # bore dog foot fillets; balance window corner radius
DISC_BAL_PTS = [(-13.2, 4.85), (-13.2, 9.08), (-11.68, 7.65)]    # param: organic balance-window hull corners (measured, STEP)
# param: end
DISC_ROUND = dict(r_out=0.0, r_in=1.0)                           # tooth tip sharp (STEP parity) and flank root fillet


SPIDER = dict(r=14.2, lobe_r=STACK_TAP_R + STACK_WALL, round_in=0.8, hub_r=HUB_R + STACK_WALL, win_round=CORNER_R)   # disc, stack-bolt lobes and their root fillet, hub ring round the bell screws, window corners (STEP spider_1)
SPIDER["arm"] = SPIDER["lobe_r"]               # the 4 arms run each lobe's width straight in to the hub: window sides offset one lobe radius off the arm axis
SPIDER["win_r"] = BOLT_R - SPIDER["lobe_r"]     # window rim stops at the inner edge of the lobe circles
SPIDER["bore_r"] = SHAFT_R + SHAFT_CLR          # bore on the shaft collar


SPACER = dict(r=DISC_R - DISC_ECC, bore_r=BELL_WALL_R[1] + SHAFT_CLR, arm=2.0, win_round=CORNER_R)
SPACER.update(win_in=SPACER["bore_r"] + STACK_WALL, win_out=SPACER["r"] - STACK_WALL)   # rim on the discs' inner rim envelope (never proud of a disc); windows: ring 11.4..14.5, sides 2.0 off the bolt axes (STEP section)
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
LEAD_GROOVE = os.environ.get("REVRON_LEAD_GROOVE", "off") == "on"   # optional RV03 variant (one setting, like MOTOR_VARIANT): "on" cuts the snap-in lead C-groove; default "off" = the original RV03, leads run free over the lug
PHASE_VIA = ([[11.8, 14.5, 16.0]] + [[LEAD_GROOVE_X, y, z] for y, z in _LG] + [[LEAD_FAN_X, WY, _LG[1][1]]] if LEAD_GROOVE   # tub inside -> groove rear -> groove front -> lead fan under the spacer
             else [[11.8, 14.5, 16.0], [11.8, 15.5, 18.2], [11.8, 27.0, 18.2], [11.8, 30.0, 14.5]])   # original: over the lug, no channel


__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
