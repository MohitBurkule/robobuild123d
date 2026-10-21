"""Revron params: side panels RV23/24 and wedgelets RV17/18. Re-exported by params.py."""
import math
from .params_weapon import *  # noqa: F401,F403

# ------------------------------------------------------------------------------------------------------------ wedgelet
WEDGE_TOE_H = 0.85                   # ramp Z = 1 + 1.187 (50.1 - Y) lifted so its toe is a 0.85 mm land at full length


# ------------------------------------------------------------------------------------------------------------ side panel
# The wall is the RV23 feature tree rebuilt from analytic faces (SLDPRT: Loft1/2 + Revolve5/6/7), no organic point tables:
# every face is a plane, a cylinder/cone about a vertical axis, or one ruled S-bend patch.
SP_LEAN_DEG = 40.0                  # STEP RV23: the front swing and nose leave the floor 40 deg off vertical (cone half angle)
SP_LEAN = math.tan(math.radians(SP_LEAN_DEG))   # radial run per mm of height of those cones (== the battered nose plane's slope)
SP_X_IN = -31.5                     # chassis-side (inner) face of the straight wall: the lobe pocket gap outside the chassis wall
SP_W_FLOOR, SP_W_TOP = 5.2154, 2.0  # wall thickness battered from the floor (Z FLOOR_Z) to the top (Z SP_Z_TOP): outer face 12.1 deg off vertical
SP_Z_TOP = 16.0                     # full wall height (the rear / mid wall; the profile top line trims it)
SP_MID_Y = (-9.5, 10.5)             # straight mid wall (RV23 Loft2) from the rear bend to the S-bend; its top rises 13 -> SP_Z_TOP
SP_MID_Z_FRONT = 13.0               # mid wall height at its front end (Loft2 sketch at Y 10.5)
SP_BEND_R = (8.0, 4.0)              # rear wall bends out round two 90 deg arcs (RV23 Revolve6, Revolve7), chassis-side radii
SP_FRONT = dict(c=(-38.5, 26.55), r_in=10.55, w=3.0, z_top=12.0, over=5.0)   # front swing (Revolve5): axis (X, Y), chassis-side radius at the floor, radial thickness, top, lead-in deg
SP_BEND_STEPS, SP_BEND_LEVELS, SP_BEND_TENSION = 56, 10, 0.5   # S-bend strips (each turns < the 6 deg seam threshold), Hermite tangent length / chord
SP_REAR_Y_END = -46.0               # the straight rear wall runs on past the rear round (the profile trims it)


# --- side panel + wedgelet shared / derived dimensions (outlines are organic point tables measured on RV23/RV17) ---
RAMP_REACH, RAMP_SLOPE = 50.1, 1.187   # ramp face Z = FLOOR_Z + RAMP_SLOPE (RAMP_REACH - Y), shared by wedgelet and nose
SLAB_X = (-60.0, -20.0)              # X slab the (Y, Z) side profile is extruded through before it is cut to the panel
SP_TOP = [(-32.9, 1.0), (-32.9, 16.0), (-6.7, 16.0), (14.6, 12.0), (19.3, 11.0), (24.0, 10.0), (42.0, 10.0), (RAMP_REACH, 1.0)]   # top line, (Y, Z)
SP_TOP_R = 1.5
SP_REAR_ROUND = ((-32.2, 9.7), 8.2)  # rear end: a full round over the wheel
SP_FOOT = [(-31.6, -12.0), (-42.0, -11.9), (-40.6, -2.1), (-40.8, 3.3), (-42.9, 13.3), (-31.6, 13.3)]   # 1 mm wide foot under the chassis lobe (X, Y)
SP_FOOT_Z = (FLOOR_Z, FLOOR_Z + 1.0)
SP_NOSE_Y0 = SP_FRONT["c"][1]    # nose front face (plane through the swing axis, tangent to the swing's outer cone)
SP_NOSE = [(-52.1, SP_NOSE_Y0), (-51.7, 39.7), (-50.5, 43.0), (-48.4, 45.7), (-45.6, 47.9), (-42.0, 49.6), (-40.0, RAMP_REACH), (-38.5, RAMP_REACH),
           (-38.5, 37.6), (-41.6, 37.6), (-42.4, 37.3), (-42.3, 34.9), (-40.5, 34.5), (-40.5, SP_NOSE_Y0)]   # nose plan (X, Y)
SP_NOSE_R, SP_NOSE_Z = 0.5, (FLOOR_Z, 10.0)
SP_BATTER = dict(x0=SP_FRONT["c"][0] - SP_FRONT["r_in"] - SP_FRONT["w"], slope=SP_LEAN, z=(FLOOR_Z, 16.0), below=-5.0, far=0.0, depth=60.0)   # outer face leans in 40 deg (the swing's outer cone continues it): X = x0 + slope (Z - FLOOR_Z)
SP_TOE_Y0 = 47.0                     # the ramp toe's land starts here (Y)
SP_TOE_RUN = 3.1                     # Y run of the ramp skin the toe polygon follows
SP_CHAMFER = ((-120.0, 0.0, 0.0), (1.0, -1.525, -1.4725))   # front-outer corner chamfer plane (origin, normal)
SP_HOLLOW = [(26.5, 3.0), (37.0, 3.0), (37.7, 6.6), (39.0, 10.5), (26.5, 10.5)]   # hollow behind the nose wall (Y, Z)
SP_HOLLOW_X = (-42.0, -38.4)
# STEP RV23: above Z0 the hollow runs on forward over the SB pocket and ends in a round in plan (vertical axis, X, Y)
SP_HOLLOW_END = dict(c=(-38.5, 36.6), r=3.6, z0=7.25)
# M3 ISO 10642 seats (head dk 6.0 + csk_clear) + a driver bore out through the battered face, per screw. STEP RV23 nose
# (a, b): the 90 deg seat is the dk + 0.7 cone but the driver bore is only r `drive_r` 3.10 (the cone's rim is a 0.25 mm
# undercut at the seat; the seat's own r0 bore runs just `lip` above it) and the shank is a close fit (r 1.6); the
# chassis-nut screw (c) keeps the r0 driver bore and the normal fit
SP_CSK = dict(csk_clear=0.7, fit=dict(a="close", b="close", c="normal"), drive_r=dict(a=3.1, b=3.1), lip=0.05, head_clear=12.0)
SP_SA_CLEAR = (2.6, -42.55, -38.0)   # STEP RV23 r 2.6: standoff-end clearance bore round SA (R, X0, X1)
# STEP RV23: standoff end boss ring round SA (X0 -> X1): r 4.0 up into the nose roof to `x_ch`, then a 45 deg chamfer
# down to r_end, which runs on to the standoff end
SP_BOSS = dict(r=4.0, r_end=3.3, x=(-SA_X[1], -SA_X[1] + 3.0), x_ch=-40.75)   # [fix-C-j1] boss face = the 25 mm standoff's outboard end
# STEP RV23 rear tyre relief pocket on the inner face (measured on RV23 sections X -43.7..-44.9): a round-ended slot, r 5 round about
# the rear wheel axis line (Y, Z) with its front corners r1.75 (the r1.5 floor fillet stays inside them), from the floor X to the inner face; the floor edge is rounded r1.5 (Fillet5)
SP_TYRE_RELIEF = dict(c=(-34.4, 10.0), r=5.0, y_front=-24.4, r_front=1.75, x=(-45.0, -43.4), r_floor=1.5)
SP_NUT_RELIEF_X = (-32.5, -31.4)
# [fix-C-j1] the panel is modelled once, left hand (RV23, -X); RV24 is its YZ mirror. Its frame sits on the SA standoff
# end (the boss face the 25 mm standoff seats against); each screw seat sits on the axis of the part it clamps.
SP_BUILT_SIDE = -1
SPEC_DP = 6                          # decimals of solved positions written to the spec (micron noise-free)
SP_SEAT_AXIS = dict(a=SA, b=SB, c=NUT)   # (Y, Z) of each side screw: 25 mm standoff, 15 mm standoff, chassis nut
SIDE_DEV_X, SIDE_DEV_R = 41.78, 4.0              # deviation sphere at the nose screw seat (STEP RV23 bore centre X, radius)
CHASSIS_MIN_VOLUME = 15000.0         # mm3: the intact chassis is 15988 mm3 in one solid
SP_NUT_RELIEF_R = 1.0                # relief corners round r1: no sharp concave corner in the printed wall
SP_PIN_HOLE = dict(d=2.05, at=(2.92, 12.07), x=(-36.0, -31.0))   # STEP RV23: d1.25 cross hole along X through the wall at the nut lobe top (Y, Z; X span)
SP_VENT = dict(y0=(-11.0, -4.5, 2.0), z0=5.0, dy=5.0, dz=6.0, r=1.0, x=(-50.0, -36.5))   # diagonal ESC vent slots
# [fix-C wedgelet] measured polyline arcs rebuilt as true arcs (sampled finer than the 6 deg facet-seam threshold)
WG_ARC_STEP = 3   # deg per sampled chord of a wedgelet profile arc


def _wg_arc(c, r, a0, a1, step=WG_ARC_STEP):
    """Points round centre c (radius r) from angle a0 to a1 (deg), one chord per `step` deg, both ends included."""
    import math as _m
    n = max(2, int(_m.ceil(abs(a1 - a0) / step)))
    return [(c[0] + r * _m.cos(_m.radians(a0 + (a1 - a0) * k / n)), c[1] + r * _m.sin(_m.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def _wg_ang(c, p):
    import math as _m
    return _m.degrees(_m.atan2(p[1] - c[1], p[0] - c[0]))


def _wg_flank():
    """Cheek flank = two tangent arcs measured on the STEP section (fit residual < 0.01): a concave R4 from the wall foot, then a
    convex R10 (centres on the line at `lean` deg), ending where the straight shoulder takes over at `end` deg."""
    import math as _m
    c1, r1, lean, r2, end = WG_FLANK["c"], WG_FLANK["r"], WG_FLANK["lean"], WG_FLANK["r2"], WG_FLANK["end"]
    c2 = (c1[0] + (r1 + r2) * _m.cos(_m.radians(lean)), c1[1] + (r1 + r2) * _m.sin(_m.radians(lean)))
    return _wg_arc(c1, r1, 180, lean)[:-1] + _wg_arc(c2, r2, lean - 180, end)


WG_FLANK = dict(c=(30.55, 5.5), r=4.0, lean=106, r2=10.0, end=-50)   # (centre (Y, Z) of the R4, R, centre-line angle, R of the second arc, its end angle)
WG_NOSE_ARC = dict(c=(40.48, 4.49), r=3.27)                          # nose arc round (Y, Z), vertical tangent at its foot: the tab and the slot share it
_NA = WG_NOSE_ARC
WG_X = (-38.5, -36.5, -35.5, -29.0, -21.5, -17.5)   # slab edges along X: block | ring step | skin | cheek | nose tab
WG_S1 = (3.5, [(40.5, 1.0), (RAMP_REACH, 1.0), (42.54, 10.0), (39.55, 10.0), (40.23, 8.0)])   # block round SB: (R, tail outline (Y, Z))
WG_S2 = (3.0, [(40.4, 7.5), (39.55, 10.0), (41.92, 10.0), (42.29, 10.31), (RAMP_REACH, 1.0), (46.68, 1.0), (44.96, 1.5), (40.5, 1.5)])
WG_CHEEK = [(38.05, 15.36), (RAMP_REACH, 1.0), (26.55, 1.0), *_wg_flank(),
            (36.62, 14.17), (37.1, 12.78), (38.6, 12.78), (37.79, 15.15)]
WG_IN_SLOT = [(38.69, 10.9), (39.12, 11.26), (37.79, 15.15), (38.05, 15.36), (RAMP_REACH, 1.0), (43.75, 1.0), *_wg_arc(_NA["c"], _NA["r"], 0, _wg_ang(_NA["c"], (42.91, 6.68))),
              (41.0, 8.6), (40.03, 8.6), (39.52, 10.07)]
WG_TAB = [(42.78, 6.82), (44.32, 6.1), (44.69, 7.44), (RAMP_REACH, 1.0), (43.75, 1.0), *_wg_arc(_NA["c"], _NA["r"], 0, _wg_ang(_NA["c"], (42.78, 6.82)))[:-1]]
WG_SKIN = [(RAMP_REACH, 1.0), (47.57, 1.0), (46.8, 1.36), (40.79, 8.52), (40.22, 8.04), WG_CHEEK[-1], WG_CHEEK[0]]   # skin tops out on the cheek's top corner
# skin top cap: in (X, W = Z - k Y) the cap is a circular arc rising to the full skin height (vertical tangent at
# X = centre + R); swept along (0, 1, k). Fitted on 12 STEP X sections from X -35 to -30.65 (residual < 0.03 mm)
WG_SKIN_CAP = dict(k=0.84, c=(-41.166, -16.147), r=10.554)   # param: organic skin cap arc (slope k, centre (X, W), R) fitted to RV17
# param: end
# fork-tail entry: between the kidney and the cheek's top notch the STEP opens the kidney to the notch over the last
# 1.05 mm before the nose tab, so the fork tail drops into the kidney from above
WG_TAIL_ENTRY = ([(35.08, 5.3), (37.36, 12.78), (37.36, 13.2), (38.14, 13.2), (38.14, 12.78), (38.2, 10.0), (38.04, 7.25)], -22.55)   # param: organic entry outline (Y, Z) mid-slot on RV17, X start (ends at the nose tab)
# param: end
ARC_N, ARC_MOUNT, ARC_KIDNEY, WG_MERGE_EPS = 64, 32, 24, 0.01       # circle facets per quarter; overlap that merges the toe land with the wedgelet body
WG_TAB_FILM = 0.6                    # TPU film limit: slivers thinner than this are dropped from the nose tab
WG_MOUNT_GAP = 0.1                   # nose tab clearance to the weapon mount boss
WG_FORK_SLOT_X = (-27.0, -24.5)      # 2.5 mm fork slot through the cheek
WG_BORES = dict(sa=2.6, sb=1.6, sb_head=2.5)   # radii of the standoff bores through the wedgelet (sb_head: block end only)
WG_BORE_X = (-39.0, -17.0)
WG_KIDNEY = ([(36.05, 5.15), (36.95, 7.45)], 0.95, (-29.5, -21.0))   # fork-tail kidney slot (centre line (Y, Z), half width, X span)
WG_TOE = [(48.6, 1.0), (RAMP_REACH, 1.0), (RAMP_REACH, 1.0 + WEDGE_TOE_H), (48.6, 1.0 + 1.5 * RAMP_SLOPE)]   # knife toe on a printable land (Y, Z)
QUARTER_TURN = 90   # deg, tyre shoulder arcs sweep a quarter turn
FORK_DEV = dict(x=25.5, y=66.0, z=1.4, r=2.0)   # reference-diff deviation sphere at the fork tip land (STEP knife tip)
SIDE_DEV_X, SIDE_DEV_R = 41.78, 4.0              # deviation sphere at the nose screw seat (STEP RV23 bore centre X, radius)
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
