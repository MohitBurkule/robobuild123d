"""Revron params: drisk stack, GR1507 motor, weapon mounts RV02/RV03, disc / spider / spacer. Re-exported by params.py."""
from .params_chassis import *  # noqa: F401,F403
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
MNT_OUT, MNT_SLAB = MNT_IN + MNT_T, MNT_IN + MNT_SLAB_T
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
BSP_T = 1.5                          # printed spacer between the stator base and the right mount
BSP_X = (MNT_IN - BSP_T, MNT_IN)
STAT_HOLE_R, CB_R, CB_CONE_X = 1.12, 2.25, (16.4, 17.15)   # RV03 stator screw clearance d2.24, d4.5 counterbore, its cone
PHASE_VIA = [[11.8, 14.5, 16.0], [11.8, 15.5, 18.2], [11.8, 27.0, 18.2], [11.8, 30.0, 14.5]]   # weapon phase leads: the lug (|X| >= 10.4, up to the deck) closes z 14.5 at y 15..26



WSEG_LO, WSEG_FINE, WSEG_MID, WSEG_HI, WSEG_FN, WSEG_MAX, WSEG_ARC, WSEG_ARC_S = 24, 32, 48, 64, 96, 128, 40, 12   # circle / arc tessellation of the 2D profiles
# weapon mount RV02 (left, shaft end) / RV03 (right, stator): per-side master parameters (STEP measurements)
MNT_SIDE = dict(
    r=dict(top_r=10.0, notch_y=10.17, rim_end=-14.5, slab_eps=0.02, face=(23.88, 0.144, 0.0379)),   # a, kz, ky of |X| = a - kz*Z - ky*Y
    l=dict(top_r=7.0, notch_y=9.0, rim_end=-5.0, slab_eps=0.0, face=(23.48, 0.185, 0.0168)))
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
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
