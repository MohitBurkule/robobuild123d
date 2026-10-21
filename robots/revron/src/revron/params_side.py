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
SP_W_TOP = 2.0                      # THE wall thickness master: the wall at its full height (Z SP_Z_TOP); the flutes keep this much below the top line
SP_BATTER_DEG = 12.1                # the outer face leans this far off vertical (every battered plane / cone of the wall)
SP_Z_TOP = 16.0                     # full wall height (the rear / mid wall)
SP_W_FLOOR = SP_W_TOP + (SP_Z_TOP - 1.0) * math.tan(math.radians(SP_BATTER_DEG))   # thickness at the floor (Z 1)
SP_MID_Y = (-9.5, 10.5)             # straight mid wall (RV23 Loft2) from the rear bend to the S-bend; its top rises 13 -> SP_Z_TOP
SP_MID_Z_FRONT = 13.0               # mid wall height at its front end (Loft2 sketch at Y 10.5)
SP_BEND_R = (8.0, 4.0)              # rear wall bends out round two 90 deg arcs (RV23 Revolve6, Revolve7), chassis-side radii
SP_FRONT = dict(c=(-38.5, 26.55), r_in=10.55, w=3.0, z_top=10.0, over=5.0)   # front swing (Revolve5): axis (X, Y), chassis-side radius at the floor, radial thickness, top, lead-in deg
BEZIER_DEG = 3                      # a cubic Bezier's handle is a third of the Hermite tangent
SP_BEND_TENSION = 0.8               # S-bend corner-curve tangent length / chord
SP_REAR_Y_END = -46.0               # the straight rear wall runs on past the rear round (the profile trims it)


# --- side panel + wedgelet shared / derived dimensions (outlines are organic point tables measured on RV23/RV17) ---
RAMP_REACH = 50.1
RAMP_SLOPE = 1.187   # ramp face Z = FLOOR_Z + RAMP_SLOPE (RAMP_REACH - Y), shared by wedgelet and nose
SLAB_X = (-60.0, -20.0)              # X slab the (Y, Z) side profile is extruded through before it is cut to the panel
GEO_EPS = 1e-4                      # coordinate match tolerance when picking edges by position
# rear end (STEP RV23 sections): a R10 round tangent to the floor, internally tangent to a R6 round tangent to the top line; the one number is
# the R10 axis Y (the R6 axis follows from the tangency)
SP_REAR = dict(y=-30.5, r_floor=10.0, r_top=6.0)
SP_FOOT = dict(c=(-63.58, -0.07), r=23.021, a_lo=-7.8, a_hi=11.2, y=(-13.3, 15.2), x_in=-35.0)   # 1 mm foot under the chassis lobe (STEP section): R23 arc about c, its tangent lines leave at these radius angles (deg from +X), run out to y, back to the wall at x_in
SP_FOOT_Z = (FLOOR_Z, FLOOR_Z + 1.0)
SP_NOSE_Y0 = SP_FRONT["c"][1]    # nose front face (plane through the swing axis, tangent to the swing's outer cone)
SP_NOSE_RUN = 10.0                   # the nose is the swing's outer cone swept on this far along +Y (its round end is the hollow's axis)
SP_NOSE_OVER = 1.0                   # cutters overshoot the faces they open
# nose notch (STEP RV23 sections): the standoff-end post (R3.952 round SA) stands in a pocket (floor X_POST); behind it a deeper pocket (X_B, rear corner r_round)
# keeps the wedgelet ring round SB as a R3.5 post
SP_NOSE_PKT = dict(x_post=-40.5, x_b=-42.5, draft_deg=2.2, r_round=1.0, r_ring=3.5, z_top=8.0, r_slot=3.65, taper_deg=18.9)   # z_top: the pocket's roof, above it a slot round the nose-run end
SP_NOSE_Z = (FLOOR_Z, 10.0)   # SP_NOSE_Z[1] is also the top of the swing and of the S-bend's front end
SP_TOE_Y0 = 47.0                     # the ramp toe's land starts here (Y)
SP_TOE_RUN = 3.1                     # Y run of the ramp skin the toe polygon follows
# M3 ISO 10642 seats (head dk 6.0 + csk_clear) + a driver bore out through the battered face, per screw. STEP RV23 nose
# (a, b): the 90 deg seat is the dk + 0.7 cone but the driver bore is only r `drive_r` 3.10 (the cone's rim is a 0.25 mm
# undercut at the seat; the seat's own r0 bore runs just `lip` above it) and the shank is a close fit (r 1.6); the
# chassis-nut screw (c) keeps the r0 driver bore and the normal fit
SP_DRIVER_SEATS = "abc"               # all three screws get the narrower driver bore (STEP RV23: r 3.10 at the chassis nut too)
SP_CSK = dict(csk_clear=0.7, fit="close", drive_r=3.1, lip=0.05, head_clear=12.0)   # drive_r: narrower driver bore of the two standoff seats
SP_SA_CLEAR = (2.6, -42.55, -38.0)   # STEP RV23 r 2.6: standoff-end clearance bore round SA (R, X0, X1)
# STEP RV23: the lip on the post's inner face: a ring round SA, r 3.25, `h` tall, its root edge chamfered 45 deg
SP_BOSS = dict(r=3.25, h=1.0, chamfer=0.5)
# STEP RV23 rear tyre relief pocket on the inner face (measured on RV23 sections X -43.7..-44.9): a round-ended slot, r 5 round about
# the rear wheel axis line (Y, Z) with its front corners r1.75 (the r1.5 floor fillet stays inside them), from the floor X to the inner face; the floor edge is rounded r1.5 (Fillet5)
SP_TYRE_RELIEF = dict(rim=1.0, depth=1.5, r_front=1.75, r_floor=1.5)   # round end concentric with the rear R6, `rim` inside it; `depth` into the rear wall's inner face
SP_NUT_RELIEF_X = (-32.5, -31.4)
# [fix-C-j1] the panel is modelled once, left hand (RV23, -X); RV24 is its YZ mirror. Its frame sits on the SA standoff
# end (the boss face the 25 mm standoff seats against); each screw seat sits on the axis of the part it clamps.
SP_BUILT_SIDE = -1
SPEC_DP = 6                          # decimals of solved positions written to the spec (micron noise-free)
SP_SEAT_AXIS = dict(a=SA, b=SB, c=NUT)   # (Y, Z) of each side screw: 25 mm standoff, 15 mm standoff, chassis nut
SIDE_DEV_X, SIDE_DEV_R = 41.78, 4.0              # deviation sphere at the nose screw seat (STEP RV23 bore centre X, radius)
CHASSIS_MIN_VOLUME = 15000.0         # mm3: the intact chassis is 15988 mm3 in one solid
# chassis-nut relief (STEP RV23, section X -32): the hull of the R4.6 round about the nut axis NUT and a small R2.1 round `dy` further along Y at height `z`
SP_NUT_POCKET = dict(r=4.6, r2=2.1, dy=12.0, z=6.921)
# three diagonal flutes on the outer face (STEP RV23): width / pitch / angle off the Y axis, the middle one through (Y 0, Z `z`), `depth` deep along X,
# each from Z `z0` up to its own level top end (`top`, rear flute first)
SP_FLUTE = dict(n=3, w=1.6, pitch=3.0, deg=30.0, y=0.0, z=10.0, z0=4.2, top=(14.1, 13.1, 12.4), depth=0.53)
# [fix-C wedgelet] measured polyline arcs rebuilt as true arcs (sampled finer than the 6 deg facet-seam threshold)
WG_RING_CHAMFER, WG_RING_CHAMFER_Y = 1.0, 44.96    # Chamfer7: the ring step's far edge is chamfered 45 deg round the SB side (cone) and along the floor to this Y (plane)
WG_CHAMFER_END = dict(a=6.77, b=1.68)   # Chamfer7's floor end vertex blend: (dy)^2 = a h - b h^2 (h = chamfer height at that X)
WG_TAB_DEV = dict(x=19.5, yz=(43.7, 5.8), r=2.5)   # reference-diff deviation sphere on the nose tab where the mount boss is taken out of it
WG_STEP_FILLET = 1.0                 # Fillet1: skin-to-ring-step blend
WG_MOUNT_GAP = 0.1                   # clearance of the nose tab to the weapon mount boss and to the chassis lug round SB
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


WG_FLANK = dict(c=SA, r=3.9519, lean=105.84, r2=10.0, end=-50)   # (centre (Y, Z) of the R4, R, centre-line angle, R of the second arc, its end angle)
WG_NOSE_ARC = dict(c=SB, r=LUG_SB_R + WG_MOUNT_GAP)                          # nose arc round (Y, Z), vertical tangent at its foot: the tab and the slot share it
_NA = WG_NOSE_ARC
# fork-tail entry (RV17 Cut-Extrude20, 1 mm deep from the nose face, floor edges rounded Fillet9 r0.5) opens the kidney arc slot:
# its rear edge runs from the slot's outer wall (at `ring_end` deg) up to the notch floor `top` above SB, `width` wide, the front
# edge tangent to the slot's upper end cap. dY (rear_dy) and `top` are measured from SB.
WG_ENTRY = dict(ring_end=170.0, top=8.28, rear_dy=-1.9015, width=1.5, depth=1.0, fillet=0.5)
WG_X = (-38.5, -36.5, -35.5, -29.0, -21.5, -17.5)   # slab edges along X: block | ring step | skin | cheek | nose tab
WG_S1 = (3.5, [(40.5, 1.0), (RAMP_REACH, 1.0), (42.54, 10.0), (39.55, 10.0), (40.23, 8.0)])   # block round SB: (R, tail outline (Y, Z))
WG_S2 = (WG_S1[0], [(40.4, 7.5), (39.55, 10.0), (41.92, 10.0), (42.29, 10.31), (RAMP_REACH, 1.0), (46.68, 1.0), (SB[0], 1.0)])   # ring step: (R of the boss round SB as the block, tail outline (Y, Z))
WG_CHEEK = [(38.05, 15.36), (RAMP_REACH, 1.0), (26.55, 1.0), *_wg_flank(),
            (36.62, 14.17), (SB[0] + WG_ENTRY["rear_dy"] - WG_ENTRY["width"], SB[1] + WG_ENTRY["top"]),
            (SB[0] + WG_ENTRY["rear_dy"], SB[1] + WG_ENTRY["top"]), (37.79, 15.15)]
WG_IN_SLOT = [(38.69, 10.9), (39.12, 11.26), (37.79, 15.15), (38.05, 15.36), (RAMP_REACH, 1.0), (43.75, 1.0), *_wg_arc(_NA["c"], _NA["r"], 0, _wg_ang(_NA["c"], (42.91, 6.68))),
              (41.0, 8.6), (40.03, 8.6), (39.52, 10.07)]
WG_TAB = [(42.78, 6.82), (44.32, 6.1), (44.69, 7.44), (RAMP_REACH, 1.0), (43.75, 1.0), *_wg_arc(_NA["c"], _NA["r"], 0, _wg_ang(_NA["c"], (42.78, 6.82)))[:-1]]
WG_SKIN = [(RAMP_REACH, 1.0), (47.57, 1.0), (46.8, 1.36), (40.79, 8.52), (40.22, 8.04), WG_CHEEK[-1], WG_CHEEK[0]]   # skin tops out on the cheek's top corner
# skin top cap: in (X, W = Z - k Y) the cap is a circular arc rising to the full skin height (vertical tangent at
# X = centre + R); swept along (0, 1, k). Fitted on 12 STEP X sections from X -35 to -30.65 (residual < 0.03 mm)
WG_SKIN_CAP = dict(k=0.84, c=(-41.166, -16.147), r=10.554)   # param: organic skin cap arc (slope k, centre (X, W), R) fitted to RV17
# param: end
# param: end
ARC_N, ARC_MOUNT, ARC_KIDNEY, WG_MERGE_EPS = 64, 32, 24, 0.01       # circle facets per quarter; overlap that merges the toe land with the wedgelet body
WG_TAB_FILM = 0.6                    # TPU film limit: slivers thinner than this are dropped from the nose tab
WG_FORK_SLOT_X = (-27.0, -24.5)      # 2.5 mm fork slot through the cheek
WG_BORES = dict(sa=2.6, sb=1.6, sb_head=2.5)   # radii of the standoff bores through the wedgelet (sb_head: block end only)
WG_BORE_X = (-39.0, -17.0)
WG_KIDNEY = dict(r=4.5, hw=1.0, a_lo=171.7, a_hi=140.0, x=(-29.5, -21.0))   # fork-tail kidney: an arc slot about SB (centre-line R, half width, end angles deg, X span)
WG_TOE = [(48.6, 1.0), (RAMP_REACH, 1.0), (RAMP_REACH, 1.0 + WEDGE_TOE_H), (48.6, 1.0 + 1.5 * RAMP_SLOPE)]   # knife toe on a printable land (Y, Z)
QUARTER_TURN = 90   # deg, tyre shoulder arcs sweep a quarter turn
FORK_RAIL_DEV = dict(x=25.25, y=42.0, z=5.3, r=6.0)   # reference-diff deviation sphere over the fork's rail tunnels in the wedgelet cheek
FORK_DEV = dict(x=25.5, y=66.0, z=1.4, r=2.0)   # reference-diff deviation sphere at the fork tip land (STEP knife tip)
SIDE_DEV_X, SIDE_DEV_R = 41.78, 4.0              # deviation sphere at the nose screw seat (STEP RV23 bore centre X, radius)
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
