"""Revron params: wheel hubs, forks, tyres. Re-exported by params.py."""
import math
from .params_spec import *  # noqa: F401,F403



# --- hubs: rear RV21 (16 x 12) and front RV19 micro (9 x 9) revolve profiles, (x, radius) from the hub's inner face
HUB_FLANGE_T, HUB_GROOVE_C, HUB_GROOVE_W, HUB_GROOVE_CH = 0.7, 1.25, 1.1, 0.25          # flange thickness, O-ring groove centre / width, groove wall chamfer
RH_FLANGE_R, RH_GROOVE_R, RH_SEAT_R, RH_CROWN_H, RH_LIP_R, RH_LEN, RH_WALL_R, RH_WALL_T = 8.0, 7.45, 6.0, 1.0, 6.5, 12.0, 2.88, 0.2
RH_ROOT_R, RH_ROOT_STEP = 1.0, 5                                                       # RV21 Fillet2: R1 concave root between the flange wall and the seat; arc step (deg, under the 6 deg facet seam)
RH_ROOT_X = HUB_GROOVE_C + HUB_GROOVE_W / 2 + HUB_FLANGE_T                              # flange wall plane (= end of the flange land)
RH_SEAT_RAMP = tuple((RH_ROOT_X + RH_ROOT_R * (1 - math.cos(math.radians(a))), RH_SEAT_R + RH_ROOT_R * (1 - math.sin(math.radians(a))))
                     for a in range(0, 90 + RH_ROOT_STEP, RH_ROOT_STEP))                    # flange wall -> seat as a true R1 arc (wall tangent at the top, seat tangent at the foot)
RH_SEAT_X, RH_CROWN_X, RH_SEAT_END, RH_LIP_X = (3.35, 5.25), (6.25, 8.25), 11.1, 11.3   # seat span, crown span, seat end, lip start
_g0, _g1 = HUB_GROOVE_C - HUB_GROOVE_W / 2, HUB_GROOVE_C + HUB_GROOVE_W / 2
REAR_HUB_PROFILE = ((0.0, 0.0), (0.0, RH_FLANGE_R), (_g0, RH_FLANGE_R), (_g0 + HUB_GROOVE_CH, RH_GROOVE_R), (_g1 - HUB_GROOVE_CH, RH_GROOVE_R),
                    (_g1, RH_FLANGE_R), (_g1 + HUB_FLANGE_T, RH_FLANGE_R), *RH_SEAT_RAMP, (RH_SEAT_X[1], RH_SEAT_R),
                    (RH_CROWN_X[0], RH_SEAT_R + RH_CROWN_H), (RH_CROWN_X[1], RH_SEAT_R + RH_CROWN_H), (RH_CROWN_X[1] + RH_CROWN_H, RH_SEAT_R),
                    (RH_SEAT_END, RH_SEAT_R), (RH_LIP_X, RH_LIP_R), (RH_LEN, RH_LIP_R), (RH_LEN, RH_WALL_R), (RH_LEN - RH_WALL_T, RH_WALL_R),
                    (RH_LEN - RH_WALL_T, 0.0))
RH_D = dict(r=1.6, flat=0.9, arc_n=60, flat_n=27, crown=0.02)                           # D-bore: radius, flat height above the axis, facet counts, flat crown
RH_BORE_X, RH_NUT_X, RH_NUT_HALF, RH_NUT_Z, RH_GRUB_X, RH_GRUB_ENGAGE = 29.0, 41.0, 2.05, (2.4, 4.4), 34.3, 0.9   # |X| of bore start / slot end, slot half-width, slot z above axis, grub, grub tip past the flat
RH_GAP = 0.5                                                                            # Distance2: hub inner face off the chassis wall
RH_ORIGIN_X = CH_HALF_W + RH_GAP                                                        # |X| of the hub inner face
# RV19 micro hub (Revolve1 + Fillet1 + Chamfer1), drawn from its inner face: flange, O-ring groove, flange, 6 mm tyre seat, flange
FH_BORE_R, FH_FLANGE_R, FH_SEAT_R, FH_FLANGE_T, FH_GROOVE_W, FH_SEAT_W = 2.7, 4.5, 3.7, 0.5, 1.5, 6.0   # bore, flange and seat radii, flange width, O-ring groove width, tyre seat width
FH_FILLET, FH_GUSSET = 0.5, 0.4                                                          # Fillet1: groove roots; Chamfer1: 45 deg gussets at the seat ends
FH_LEN = 3 * FH_FLANGE_T + FH_GROOVE_W + FH_SEAT_W                                       # 9
FH_ORIGIN_X = RH_ORIGIN_X                                                               # Coincident82: the front hub inner face is in the rear hub's plane
# RV22 rear tyre (Revolve1 + Chamfer1 + Fillet1): bore with a centre groove for the hub crown; RV20 micro tyre: plain ring, 4 chamfers
TY_REAR = dict(od=21.5, bore=12.0, groove_r=7.0, groove_w=2.5, w=9.5, chamfer=1.0, fillet=0.5)
TY_FRONT = dict(od=11.0, id=7.0, w=6.0, chamfer=0.2)
TY_ARC_STEP = 5                                                                          # deg per fillet segment (under the 6 deg facet seam)
SO_TAP_R, SO_PITCH, SO_CHAMFER = 1.25, 0.5, 0.2                                        # RV10/RV11: M3 tap bore radius, thread pitch, 45 deg end chamfer (Chamfer1)
SO_THREAD_H = 0.625 * math.sqrt(3) / 2 * SO_PITCH                                       # thread depth (5/8 H, Profile_Height 0.2706); flat root P/8 wide, 60 deg flanks


MNT_TIP_DEV, MNT_TIP_DEV_R = (MNT_IN + 2.5, 11.5, MNT_TOP_Z + 0.9), 5.0   # mount notch-top wedge thickened to a printable wall (|x|, y, z)



# --- fork_5 (Mirrorfork 5 sketch, the designer's driving dims; everything else in fork.py is a relation) ---
# fork_5 frame: the sketch plane (u, v) with the origin on the 15 mm standoff axis, extruded +w FK_T. The assembly places it by
# the STEP transform: origin on the standoff axis at X = FK_X0[side], extruded towards the chassis centre, turned FK_TILT[side] deg.
FK_EYE_D, FK_PIN_DIST, FK_PIN_ANG = 7.5, 4.5, 65.0                      # D2 eye round the standoff, D5 pin distance, D4 angle from the sketch's vertical (the pin boss is tangent to the eye's top line)
FK_TIP, FK_RAIL, FK_FILLET, FK_T = (26.0, 4.3), 2.0, 0.2, 1.5          # D8/D9 tip (back, down), D6/D7/D10 rails, Fillet1, Boss-Extrude1
FK_WEB = 1.12                                                          # laser min web (0.75 x 1.5 mm Ti): the standoff hole and the pin hole are cut a web inside their rings (STEP: 1.10 and 1.098 -> d5.26 / d1.46 for the STEP's d5.3 / d1.5)
FK_KERF = 0.15                                                         # laser kerf: the knife tip ends in a land 3 kerfs wide, its corners r >= kerf
FK_BOT_ANG = 2.825                                                     # deg, lower edge tangent to the eye: the STEP hangs the right fork with that edge level (Parallel2)
FK_X0 = {1: 26.0, -1: -25.0}                                           # |X| of the sketch plane per side: asymmetric in the STEP (fork_5_1 at 26.0, fork_5_2 at -25.0)
FK_TILT = {1: FK_BOT_ANG, -1: 1.763}                                   # deg nose-down about the standoff (the left fork floats in the wedgelet cheek)
FK_X = {1: (FK_X0[1] - FK_T, FK_X0[1]), -1: (FK_X0[-1] - FK_T, FK_X0[-1])}   # X slab per side
FK_RES = 24                                                            # arc segments per quarter turn (3.75 deg: fitted to true arcs)

FORK_DEV = dict(x=25.5, y=66.0, z=1.4, r=2.0)   # reference-diff deviation sphere at the fork tip land (STEP knife tip)
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
