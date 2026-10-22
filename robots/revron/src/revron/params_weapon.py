"""Revron params: drisk stack, GR1507 motor, weapon mounts RV02/RV03, disc / spider / spacer. Re-exported by params.py."""
from .params_chassis import *  # noqa: F401,F403
from robot.catalog import BEARINGS   # noqa: E402
from robot.cad import fastener_catalog as _fc   # noqa: E402
from . import weapon_motor as _wm   # noqa: E402
# [fix-B-vers] weapon style (hooks.json `weapon.type`): the drisk is the one built here; any other value fails at spec
# generation with the reason, not silently as a drisk
WEAPON_TYPE = os.environ.get("REVRON_WEAPON_TYPE", "drisk")
WEAPON_TYPES = {"drisk": "vertical drisk: spider on the outrunner bell driving two floating single-tooth discs (RVRN 2.0)",
                "vspin_drum": "not built: a drum needs a full-width rotor between the mounts and a belt or hub motor",
                "vspin_eggbeater": "not built: an eggbeater needs a two-tooth beater and its own hub on the shaft",
                "hspin_bar": "not built: a horizontal bar needs a vertical motor axis and a new chassis front"}


class WeaponTypeError(NotImplementedError):
    """weapon.type names a weapon style the generator does not build."""


if WEAPON_TYPE not in WEAPON_TYPES:
    raise WeaponTypeError(f"weapon.type={WEAPON_TYPE!r} is unknown; known: {sorted(WEAPON_TYPES)}")
if WEAPON_TYPE != "drisk":
    raise WeaponTypeError(f"weapon.type={WEAPON_TYPE!r} is not implemented ({WEAPON_TYPES[WEAPON_TYPE]}); only 'drisk' is built")
# [fix-B-vers] the weapon motor is ONE setting (hooks.json `weapon.motor`, env REVRON_WEAPON_MOTOR = a catalog weapon
# motor id): stator, bell, shaft, mount bores and spider screws all come from that entry (weapon_motor.describe).
# The older switch REVRON_MOTOR_VARIANT picks the GR1507 model: "datasheet" = real GR1507 (GEPRC drawing: 12-slot wound
# stator, 4-spoke chamfered cap, side wire exit, M5 thread 8 mm), "step" = the simplified RVRN 2.0 STEP motor (solid r4
# core, flat cap, no stator, thread 10 mm). Same part ids, mount points and screws in both.
WEAPON_MOTOR = os.environ.get("REVRON_WEAPON_MOTOR", "gr1507")
WEAPON_MOTORS = {   # every catalog weapon motor the setting may name (test_weapon_motor_swap keeps it in step with the catalog)
    "gr1507": "GR1507 2850 kV (default, RVRN 2.0)", "gr1507_step": "GR1507, STEP-simplified model",
    "bbb_be1806_2300kv": "BBB BE1806 2300 kV", "brotherhobby_tc1404_3800kv": "BrotherHobby TC1404 3800 kV",
    "brotherhobby_tc1404_4600kv": "BrotherHobby TC1404 4600 kV", "repeat_2004_1400kv": "Repeat 2004 1400 kV",
    "repeat_2004_2800kv": "Repeat 2004 2800 kV", "emax_eco2207_1900kv": "EMAX ECO 2207 1900 kV",
    "bl_1806_2300kv": "generic 1806 envelope", "bl_2306_1400kv": "generic 2306 envelope", "be1806_bbb": "BE1806 envelope",
    "c_bbb_be1806_2300kv": "research row (cylinder)", "c_repeat_2004_antweight_spinner_motor": "research row (cylinder)"}
if WEAPON_MOTOR not in WEAPON_MOTORS:
    raise _wm.WeaponMotorError(f"weapon.motor={WEAPON_MOTOR!r} is not a catalog weapon motor; known: {sorted(WEAPON_MOTORS)}")
MOTOR_VARIANT = os.environ.get("REVRON_MOTOR_VARIANT", "datasheet")
MOTOR_VARIANTS = {"datasheet": "gr1507", "step": "gr1507_step"}
WM = _wm.describe(MOTOR_VARIANTS[MOTOR_VARIANT] if WEAPON_MOTOR == "gr1507" else WEAPON_MOTOR)   # the motor's fitting features
MOTOR = dict(stator=WM["stator"], can=WM["can"], thread_len=WM["thread_len"])
STATOR_BACK_X, BELL_TOP_X, BELL_R = WM["back_x"], WM["cap_x"], WM["bell_r"]   # catalog frame: base back face, bell cap face, bell radius
SHAFT_STUB_R = WM["shaft_r"]
BSP_T = 1.5                          # printed spacer between the stator base and the right mount
BSP_X = (MNT_IN - BSP_T, MNT_IN)
LEAD_GAP = 1.5                       # stator base back face to the back spacer: the phase leads fan out flat in it
# [fix-B-vers] the motor is bolted to RV03: its base back face sits LEAD_GAP + BSP_T inboard of RV03's inner face, so
# the motor and the whole drisk follow MNT_IN (STEP: base back X 10.4, motor origin on the robot centre plane)
MOTOR_X = round(MNT_IN - BSP_T - LEAD_GAP + STATOR_BACK_X, 6)
BASE_BACK_X = round(MOTOR_X - STATOR_BACK_X, 6)   # world X of the base back face
# weapon frame: on the spin axis (WY, WZ) at the robot centre plane; the GR1507 sits in it with its catalog +X (bell top) turned to world -X
W_FRAME = (MOTOR_X, WY, WZ)
MOTOR_FLIP = (0, 0, 180)             # catalog -> weapon frame: half a turn about Z, so the stator base faces RV03 (+X)
MOTOR_PLACE_TOL = 0.8               # reference_cad placement tolerance of the motor: drawing-true bell cap is 1.5 mm above the STEP can (half of it shifts the bbox centre)
BELL_CAP_X = -BELL_TOP_X             # weapon-frame X of the bell's cap face (the flip mirrors catalog X)

# master parameters of the stack: plate thicknesses; the spider's inner face sits on the bell cap and every X span below is chained from it
SPIDER_T, DISC_T = 3.0, 3.0
SPACER_T = 2 * DISC_T               # the printed spacer is two disc gauges thick (STEP 6.0)
STACK_X0 = round(BELL_CAP_X - SPIDER_T, 6)   # spider outer face: one spider thickness out from the cap
DR_X, _x = {}, STACK_X0
for _n, _t in (("spider", SPIDER_T), ("disc_a", DISC_T), ("spacer", SPACER_T), ("disc_b", DISC_T)):
    DR_X[_n] = (_x, _x + _t)       # spider | disc_a | spacer | disc_b, each flush on the previous one
    _x += _t
N_HUB = len(WM["top_holes"])          # spider-to-bell screws: the bell-top pattern of the motor entry
HUB_R, HUB_D = WM["top_holes"][0][0], WM["top_holes"][0][2]
DR_ROT = WM["top_holes"][0][1]       # drisk phase about the axis: the spider is clocked to the bell's screw pattern (STEP Drisk_V4 placement)
SERVICE_TURN_MARGIN_DEG = 5.0   # the drisk service turn (drisk.service_turn_deg) keeps the mount screw heads clear over +- this (hand turn)
DISC_R, DISC_ECC, DISC_ECC_A = 16.5, 0.5, -40.0   # eccentric rim: R16.5 centred 0.5 mm towards -40 deg (balances the tooth)
TOOTH_REACH, TOOTH_A = 6.5, 134.8    # masters: tooth tip reach past the rim and its angle in the drisk frame
TOOTH_R = DISC_R + TOOTH_REACH        # tooth tip radius (STEP 23.0)
BOLT_R = 14.0                        # stack-bolt circle (radius about the weapon axis); the spider-to-bell screws sit on the bell's own circle HUB_R
N_STACK = 4                          # bolts / lobes / windows per stack, 90 deg apart
STACK_BOLT_D = 2.0                   # stack screw size (M2): its tap / clearance holes come from the fastener catalog
STACK_TAP_R, STACK_CLR_R = _fc.tap_drill(STACK_BOLT_D) / 2, _fc.clearance(STACK_BOLT_D, "close") / 2
STACK_WALL = 1.5                     # master: material ring every stack plate keeps round a hole, bore or rim (lobes, hub ring, spacer rings)
HALF_PITCH = 180.0 / N_STACK         # windows sit midway between the bolts
# weapon motor: axis X, stator base back face at BASE_BACK_X (GR1507: 10.4) on the right mount via the back spacer X 11.9..13.4
MNT_OUT, MNT_SLAB = MNT_IN + MNT_T, MNT_IN + MNT_SLAB_T
MNT_FRAME = dict(r=(MNT_IN, WY, WZ), l=(-MNT_IN, WY, WZ))   # each mount's frame: its inner face on the weapon axis
# motor shaft and its outboard bearing (GR1507: MR85ZZ 5 x 8 x 2.5) in the RV02 seat
SHAFT_CLR = 0.1                      # radial clearance round the shaft (RV03 hole, spider bore)
BRG_RECESS, BRG_PRESS = 0.1, 0.05    # MR85 sits this far below the RV02 inner face (race clear of the spider); seat interference
SHAFT_INTO_RECESS = 1.3              # the threaded end stands this far past the RV02 slab into the nut recess
SHAFT_R = SHAFT_STUB_R               # motor shaft radius (GR1507: 5 mm, motor catalog)
_X_END = round(-(MNT_SLAB + SHAFT_INTO_RECESS) - MOTOR_X, 6)   # weapon-frame X of the free end in RV02's nut recess
WSHAFT = dict(r=SHAFT_R, len=round(-STATOR_BACK_X - _X_END, 6), x_end=_X_END, thread_pitch=0.8, thread_depth=0.3, thread_len=MOTOR["thread_len"], chamfer=0.4)   # motor shaft: radius, length (back flush with the base), free end in RV02's nut recess
SHAFT_D = 2 * SHAFT_R
BRG_NAME = _wm.pick_bearing(2 * SHAFT_R, BEARINGS)   # outboard bearing designation (robot.catalog.BEARINGS: bore = the motor shaft; GR1507 MR85)
_bd, _bod, _bw = BEARINGS[BRG_NAME]
BRG = dict(od_r=_bod / 2, w=_bw, bore_r=_bd / 2)   # the bearing from the catalog: the shaft runs in its bore
BRG["x"] = -(MNT_IN + BRG_RECESS + BRG["w"] / 2)   # centred in the RV02 seat
BRG_SEAT_R, NUT_RECESS_R = BRG["od_r"] - BRG_PRESS, 6.0   # MR85 seat (pressed: 7.9 STEP), shaft nut recess
STATOR_HOLES = _wm.world_holes(WM["base_holes"])   # [(dY, dZ, screw d)] stator screws about the axis: the motor catalog's base holes
BOSS_OVER = 0.01                     # boss overshoots the battered plane before it is split
MNT_SCREW = ("M3x12", "M3x14")           # mount-to-standoff CSK screws at SA, SB
MOUNT_VARIANT = os.environ.get("REVRON_MOUNT_VARIANT", "original")   # "original" = RV02/RV03 as the STEP draws them; "printable" = nose pad, thickened notch tip, relieved corners, loose screw holes (improvements, not parity)
PRINTABLE = MOUNT_VARIANT == "printable"
MNT_SCREW_FIT = "loose" if PRINTABLE else "close"   # ISO 273: loose slack so the notch face takes the hit first; close = the STEP's d3.2 holes
RV03_BORE_R = SHAFT_R + (SHAFT_CLR if PRINTABLE else 0.0)   # RV03 centre hole: the STEP d5.0 (the shaft ends at the stator base, short of RV03); printable adds the shaft clearance
STATOR_SCREW_FIT = "normal" if PRINTABLE else "close"   # RV03 stator M2 holes: close = the STEP d2.2 (ISO 273 close); normal = d2.4
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
WM_TIP_SHORT = 0.3                   # stator screw tip stops this short of the base's tapped depth
WM_BITE = round(min(WM["base_h"], 3.0) - WM_TIP_SHORT, 6)   # thread the stator screw bites in the base (GR1507 2 mm base: 1.7 >= 0.8 d + 0.1)
WM_WEB = 3.3                         # RV03 counterbore floor this far out from its inner face (STEP RV03: 16.7 - 13.4)
WM_LENS = (3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 25)   # stock button-head lengths
WM_LEN = float(next(L for L in WM_LENS if L >= round(MNT_IN + WM_WEB - BASE_BACK_X + WM_BITE, 6) - 1e-6))   # shortest that reaches (GR1507: M2x8)
WM_D = STATOR_HOLES[0][2]            # stator screw size (GR1507 M2)
WM_DES = f"M{WM_D:g}x{WM_LEN:g}"
CB_R = round(2.25 - _fc.head(2.0, "button")[0] / 2 + _fc.head(WM_D, "button")[0] / 2, 6)   # RV03 stator counterbore: the STEP d4.5 over the M2 button head, same slack for other sizes
CB_FLOOR_X = round(BASE_BACK_X + WM_LEN - WM_BITE, 6)   # its floor |X| (the button head seats here): the screw tip lands WM_BITE inside the base (STEP 17.15 gives only 1.25: declared deviation)
CB_CONE_X = (CB_FLOOR_X - 0.75, CB_FLOOR_X)      # the STEP's 0.75 lead-in cone under the counterbore (left out, see spec deviations)
CB_STEP_CONE_X = (16.4, 17.4)        # |X| span of the STEP's 45 deg cone (r1.1 -> r2.25): the stator-hole deviation waiver spans it
# bolt_wm0..n order: a 4-hole pattern opposite pairs first (GR1507 cross arms 0, 180, 90, 270 deg)
WM_ORDER = (0, 2, 1, 3) if len(STATOR_HOLES) == 4 else tuple(range(len(STATOR_HOLES)))



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
TAB_FRONT_SETBACK = fc.head(M3, 'csk')[0] / 2 + CH_WALL / 2   # tab front face stands short of the axle standoff axis (SA) by the M3 CSK head radius plus a skin: the mount screw into SA clears the tab
TAB = dict(y0=CH_Y1, z0=5.35, h=8.2, y1=SA[0] - TAB_FRONT_SETBACK, cham=1.0)   # chassis tab the notch drops over: rear Y, floor Z, height, front-face Y (follows SA: 26.5 at the STEP's SA), front chamfer
MNT_NOTCH_GAP = 0.1                     # the notch's front face stands this far ahead of the tab's front face (STEP RV02/RV03 notch at Y 26.6)
NOSE_R = 3.25                           # nose arc round the SB standoff; it leaves the outline at the side's rim_end angle (the front edge is the common tangent of rim and nose: STEP RV02 -5, RV03 -14.5)
MNT_HEEL = dict(z=SB[1] - NOSE_R, step=0.4, back=1.8, z_hook=2.5, z_lip=4.5)   # rear foot hooked under the tab: flat underside (tangent to the nose arc), tip step, setback, hook and lip Z
MNT_NOTCH_UP = 2.0                      # the rear face above the tab leans back by this much over the last stretch to the top
# the boss starts above the line from the notch top to (BOSS_NOSE_Y, BOSS_Z): STEP 44.34, 6.34, it runs tangent to the nose
# arc to 0.4 um. [fix-B-robust] That point rides on the nose standoff SB (STEP offset 3.84, 1.84 from it), so the boss
# line follows SB when it moves and stays tangent to the nose arc round it
BOSS_NOSE_DY, BOSS_NOSE_DZ = 3.84, 1.84
from .tub2_lug import top_line_slope   # noqa: E402
BOSS_SLOPE = top_line_slope()           # the boss line is parallel to the chassis lug's top line (tangent from the front-top corner to the nose round SB), so it follows SB with the lug
BOSS_NOSE_Y = SB[0] + BOSS_NOSE_DY
BOSS_Z = MNT_TOP_Z + (BOSS_NOSE_Y - TAB["y0"]) * BOSS_SLOPE   # STEP 6.34 at the default SB
NOSE_PAD_R = 4.1 if PRINTABLE else 0.0                        # local pad round the nose CSK: CSK cone radius (3.2) + a 0.9 mm printed wall (the STEP nose leaves 0.15 mm)
BIG = 60.0                              # a box edge bigger than any part, for the wedgelet's 2D half-plane clip (_mount_clip)
MNT_RELIEF_R = 1.0 if PRINTABLE else 0.0                      # concave corner relief of the profile (tub deck fillet, mfg corner relief)
MNT_CSK_CLEAR = 0.4 if PRINTABLE else 0.2   # extra cone diameter over the DIN 7991 head (dk 6.0): STEP cone d6.2; printable 0.4 floats the seated head so the notch bears a hit first
MNT_CSK_PROUD = 0.0 if PRINTABLE else 0.12   # ISO 10642 head seated on the STEP d6.2 cone stands this far out of the inner face (flush, it would cut 0.08 into the cone; flush_head allows 0.2)
MNT_TIP_WALL, MNT_TIP_REACH = (1.5 if PRINTABLE else 0.0), 3.0    # printed wall: the wedge where the rear notch meets the rim tangent is thickened upward to this within this reach of the notch top (rearmost point and underside unchanged: the underside rides on the chassis tab)


HOLE_FACE_RISE = 0.7                    # the battered face's highest point over a stator hole axis: the surface the hole is measured from
_HOLE0_DEG = math.degrees(math.atan2(STATOR_HOLES[0][1], STATOR_HOLES[0][0]))
BSP = dict(r=MNT_SIDE["r"]["top_r"], bore_r=round(WM["base_hub_r"] + 0.1, 6), half_deg=24.6, round_in=2.0, round_out=1.0, phase=round(_HOLE0_DEG + HALF_PITCH, 6))   # motor back spacer: flush with RV03's teardrop rim, bore over the base hub (GR1507 r3.9), windows midway between the stator screws
BSP.update(win_in=BSP["bore_r"] + BSP_T, win_out=BSP["r"] - BSP_T)   # windows leave a hub ring and a rim ring one spacer thickness wide


CORNER_R = 1.0                       # master: the stack's machined/printed inside-corner fillet (dog feet, spider and spacer windows)
# param: organic bore dog ramp profile (STEP section fit, per dog pitch): base r, rise, flank t0..t1, R ramp to t2, nose
DOG = dict(r=12.0, rise=1.9, t0=6.6, t1=13.1, t2=54.7, ramp_r=15.3, nose_r=2.0)
# param: end
if BELL_R + SHAFT_CLR > DOG["r"]:
    raise _wm.WeaponMotorError(f"weapon motor `{WM['id']}`: its bell (r{BELL_R:g}) does not fit the disc dog bore (r{DOG['r']:g}) of the drisk")
DISC_BORE_ROUND, DISC_HOLE_R_WIN = CORNER_R, 0.44               # bore dog foot fillets; balance window corner radius
DISC_BAL_PTS = [(-13.2, 4.85), (-13.2, 9.08), (-11.68, 7.65)]    # param: organic balance-window hull corners (measured, STEP)
# param: end
DISC_ROUND = dict(r_out=0.0, r_in=1.0)                           # tooth tip sharp (STEP parity) and flank root fillet


SPIDER = dict(r=14.2, lobe_r=STACK_TAP_R + STACK_WALL, round_in=0.8, hub_r=HUB_R + STACK_WALL, win_round=CORNER_R)   # disc, stack-bolt lobes and their root fillet, hub ring round the bell screws, window corners (STEP spider_1)
SPIDER["arm"] = SPIDER["lobe_r"]               # the 4 arms run each lobe's width straight in to the hub: window sides offset one lobe radius off the arm axis
SPIDER["win_r"] = BOLT_R - SPIDER["lobe_r"]     # window rim stops at the inner edge of the lobe circles
SPIDER["bore_r"] = SHAFT_R + SHAFT_CLR          # bore on the shaft collar


SPACER = dict(r=DISC_R - DISC_ECC, bore_r=BELL_R + SHAFT_CLR, arm=2.0, win_round=CORNER_R)
SPACER.update(win_in=SPACER["bore_r"] + STACK_WALL, win_out=SPACER["r"] - STACK_WALL)
SPACER["win_round"] = min(CORNER_R, round((SPACER["win_out"] - SPACER["win_in"]) / 2 - 0.1, 6))   # a bigger bell narrows the window ring: its corners round to fit (GR1507: CORNER_R)   # rim on the discs' inner rim envelope (never proud of a disc); windows: ring 11.4..14.5, sides 2.0 off the bolt axes (STEP section)
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
    return MNT_TOP_Z + (y - TAB["y0"]) * BOSS_SLOPE


def lead_groove_ends():
    """((y, z) rear, (y, z) front) of the phase-lead groove axis in RV03: parallel to the boss line, LEAD_GROOVE_R + LEAD_LIG above it,
    from LEAD_Y_REAR to straight below the weapon axis (WY), where the leads come out of the stator."""
    off = LEAD_GROOVE_R + LEAD_LIG
    return tuple((y, boss_line_z(y) + off) for y in (LEAD_Y_REAR, WY))


_LG = lead_groove_ends()
LEAD_VIA_X = round(BASE_BACK_X + LEAD_GAP - 0.1, 6)   # the leads leave the motor in its lead gap, 0.1 short of the back spacer (STEP layout: X 11.8)
LEAD_GROOVE = os.environ.get("REVRON_LEAD_GROOVE", "off") == "on"   # optional RV03 variant (one setting, like MOTOR_VARIANT): "on" cuts the snap-in lead C-groove; default "off" = the original RV03, leads run free over the lug
PHASE_VIA = ([[LEAD_VIA_X, 14.5, 16.0]] + [[LEAD_GROOVE_X, y, z] for y, z in _LG] + [[LEAD_FAN_X, WY, _LG[1][1]]] if LEAD_GROOVE   # tub inside -> groove rear -> groove front -> lead fan under the spacer
             else [[LEAD_VIA_X, 14.5, 16.0], [LEAD_VIA_X, 15.5, 18.2], [LEAD_VIA_X, 27.0, 18.2], [LEAD_VIA_X, 30.0, 14.5]])   # original: over the lug, no channel


# [fix-B-vers] the stack must fit between the mounts: the bell-screw heads on the spider's outer face stay clear of RV02
BELL_HEAD_CLEAR = round(MOTOR_X + DR_X["spider"][0] - _fc.head(HUB_D, "button")[1] + MNT_IN, 6)   # STEP layout: 2.4
if BELL_HEAD_CLEAR < 0.2:
    raise _wm.WeaponMotorError(f"weapon motor `{WM['id']}` at MNT_IN {MNT_IN:g}: the drisk stack does not fit between the mounts "
                               f"(bell-screw heads {BELL_HEAD_CLEAR:+.2f} mm from RV02, the motor sits {LEAD_GAP + BSP_T:g} mm off RV03)")
if N_HUB > 1 and 2 * HUB_R * math.sin(math.pi / N_HUB) < _fc.head(HUB_D, "button")[0] + 0.5:   # heads need room to turn a key between them
    raise _wm.WeaponMotorError(f"weapon motor `{WM['id']}`: its bell-top screws ({N_HUB} x M{HUB_D:g} on r{HUB_R:g}) are closer than one button head: the spider cannot be screwed on")


def tub_interface():
    """[fix-B-vers] What the tub fits to the weapon module, for the selected weapon.type (only 'drisk' is built): the
    tub (A) should read these instead of the weapon constants, so another weapon style can supply its own. Keys:
    type, mount_in (mount inner face |X|), mount_frames, tab (the notch tab RV02/RV03 drop over), clear_r (chassis
    stays outside this radius about the axis), axis (Y, Z), phase_via (lead route over the lug)."""
    return dict(type=WEAPON_TYPE, mount_in=MNT_IN, mount_frames=dict(MNT_FRAME), tab=dict(TAB), clear_r=WEAPON_CLEAR_R,
                axis=(WY, WZ), motor=WM["id"], phase_via=[list(p) for p in PHASE_VIA])


__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
