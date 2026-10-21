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
# [fix-C-w7] wedgelet RV17/18 (TPU): every outline is a relation of the shared datums SA, SB, FLOOR_Z and RAMP_REACH, read off the STEP
# faces (robot.cad.sketch_extract / blend_finder), no measured point tables. LH is built once, RH is its mirror.
WG_RAMP_DEG = 50.0          # ramp face angle off the floor; the cheek top line K and the cap-cylinder axis are perpendicular to the ramp
WG_TOP_Z = 15.36            # height of the cheek top corner A where K meets the ramp
WG_SKIN_T = 2.3             # THE skin thickness master (normal to the ramp)
WG_SKIN_RUN = 7.0           # skin plate length along the ramp below K: its hollow starts there, the cap cylinder (R = run + 1, axis 1 above K) bottoms there and the nose top stands at its foot
WG_TAPER_DEG = 18.9         # rear face T leans this far off vertical; it is tangent to the WG_FLANK_R circle about SA
WG_FLANK_R = 10.0           # R10 convex flank blend, also T's stand-off from SA
WG_SA_R = 3.952             # cheek bulb round the 25 mm standoff SA (the flank's first arc)
WG_BOSS_R = 3.5             # ring round SB (block, ring step) = clearance circle round SA in the fork bay
WG_NOTCH = dict(depth=2.5, width=1.5)   # tail-entry notch: depth down T from the cheek corner, width back from T
WG_BAY_Z = 8.6              # fork bay ledge height; the bay is bounded by T, this ledge and the 45 deg tangent to the lug round SB
WG_PIN_SWING = 15.0         # the fork's pin travels this far each side of its rest angle in the kidney slot round SB (r = FK_PIN_DIST)
WG_TOE_CHAMFER = 0.47       # toe chamfer leg (skin inner face to floor, equal legs)
WG_RING_CHAMFER_Y = 44.96   # Chamfer7: the ring step's far edge is chamfered 1 mm x 45 deg round the SB side (cone) and along the floor to this Y (plane)
WG_CHAMFER_END = dict(a=6.77, b=1.68)   # Chamfer7's floor end vertex blend: (dy)^2 = a h - b h^2 (h = chamfer height at that X)
WG_TAB_DEV = dict(x=19.5, yz=(43.7, 5.8), r=2.5)   # reference-diff deviation sphere on the nose tab where the mount boss is taken out of it
WG_MOUNT_GAP = 0.1          # clearance of the nose tab to the weapon mount boss and to the chassis lug round SB
WG_X0 = -38.5               # nose block outer face (also the cap cylinder's axis plane); the slabs follow by thickness
WG_SLAB = (2.0, 1.0, 6.5, 7.5, 4.0)   # block | ring step | skin | cheek | nose tab thicknesses along X
WG_BORES = dict(sa=2.6, sb=1.6, sb_head=2.5)   # radii of the standoff bores through the wedgelet (sb_head: from the ring step on)
WG_TAB_FILM = 0.6           # TPU film limit: slivers thinner than this are dropped from the nose tab
WG_MERGE_EPS = 0.01         # overlap that merges the toe land with the body
ARC_N = 64                  # circle / arc facets per quarter turn
QUARTER_TURN = 90   # deg, tyre shoulder arcs sweep a quarter turn
FORK_RAIL_DEV = dict(x=25.25, y=42.0, z=5.3, r=6.0)   # reference-diff deviation sphere over the fork's rail tunnels in the wedgelet cheek
FORK_DEV = dict(x=25.5, y=66.0, z=1.4, r=2.0)   # reference-diff deviation sphere at the fork tip land (STEP knife tip)
SIDE_DEV_X, SIDE_DEV_R = 41.78, 4.0              # deviation sphere at the nose screw seat (STEP RV23 bore centre X, radius)
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
