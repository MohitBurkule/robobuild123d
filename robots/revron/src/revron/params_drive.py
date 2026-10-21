"""Revron params: wheel hubs, forks, tyres. Re-exported by params.py."""
from .params_spec import *  # noqa: F401,F403



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
QUARTER_TURN = 90   # deg, tyre shoulder arcs sweep a quarter turn
STANDOFF_BORE_R, TYRE_SECTION_STEP = 1.25, 10                                           # standoff through-bore radius; shoulder arc step (deg)


MNT_TIP_DEV, MNT_TIP_DEV_R = (MNT_IN + 2.5, 11.5, MNT_TOP_Z + 0.9), 5.0   # mount notch-top wedge thickened to a printable wall (|x|, y, z)



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
# param: end
FK_TILT = -1.1                                    # deg, left fork nose-down about its standoff
FKS_STEPS, FKS_DY = 24, 0.5                       # fork-slot sweep up out of the ramp
FKS_CLIP = (42.0, -1, 80, 30)                     # x0, y0, x1, y1 of the sweep clip box

TYRE_REAR = dict(od_id=(21.5, 14.0), x=(32.5, 42.0), shoulder=1.2)    # RV21 F1 tyre on the N10 shaft (right side; the left is mirrored)
TYRE_FRONT = dict(od_id=(11.0, 7.0), x=(32.5, 38.5), shoulder=0.6)     # micro tyre on the nose standoff
FORK_DEV = dict(x=25.5, y=66.0, z=1.4, r=2.0)   # reference-diff deviation sphere at the fork tip land (STEP knife tip)
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
