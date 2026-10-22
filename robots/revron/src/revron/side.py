"""[fix-S] Side groups: the side panel (wedgelet, fork and hub groups live in their own modules)."""
import math, os, sys
from .params import (
    FLOOR_Z, GEO_EPS, HERE, NUT, NUT_X, RAMP_REACH, RAMP_SLOPE, SA,
    SA_X, SB, SB_X, SIDE_BOLT_DES, SIDE_BOLT_X, SIDE_FACE_X, SIDE_SINK, SLAB_X,
    SP_BEND_R, SP_BOSS, SP_CSK, SP_DRIVER_SEATS, SP_FLUTE, SP_FOOT, SP_FOOT_Z,
    SP_FRONT, SP_NOSE_PKT, SP_NOSE_OVER, SP_NOSE_Y0, SP_NOSE_Z, SP_NUT_POCKET, SP_NUT_RELIEF_X,
    SP_REAR, SP_SA_CLEAR, SP_TOE_RUN, SP_TOE_Y0, SP_Z_TOP,
    SP_TYRE_RELIEF, SP_X_IN, WEDGE_TOE_H)
from .common import _I, _S, _U, _b, _box, _cyl, _ext, _one
from .side_wall import sp_wall, nose_body


def _sp_tyre_relief(b):
    """Rear tyre relief pocket cutter: the round-ended slot profile (SP_TYRE_RELIEF: true arcs, r about the rear axis line, r_front
    front corners) extruded from the floor to the inner face, its floor edge filleted r_floor (the side's own relief tool: the
    pocket it cuts is plain, the chassis cutter just loses it)."""
    t = SP_TYRE_RELIEF
    (cy, cz), r = _rear_centres()[1], SP_REAR["r_top"] - t["rim"]   # concentric with the rear end's R6 round, a `rim` inside it
    yf, rf = cy + 2 * r, t["r_front"]                                  # the slot is two radii long
    x1 = SP_X_IN - sum(SP_BEND_R)                                       # the rear wall's inner face (after both bends)
    x0, x1 = x1 - t["depth"], x1 + SP_NOSE_OVER
    V = lambda y, z: b.Vector(x0, y, z)
    k = rf * (1 - math.sqrt(0.5))   # corner arc mid-point offset
    e = [b.Edge.make_line(V(cy, cz + r), V(yf - rf, cz + r)),
         b.Edge.make_three_point_arc(V(yf - rf, cz + r), V(yf - k, cz + r - k), V(yf, cz + r - rf)),
         b.Edge.make_line(V(yf, cz + r - rf), V(yf, cz - r + rf)),
         b.Edge.make_three_point_arc(V(yf, cz - r + rf), V(yf - k, cz - r + k), V(yf - rf, cz - r)),
         b.Edge.make_line(V(yf - rf, cz - r), V(cy, cz - r)),
         b.Edge.make_three_point_arc(V(cy, cz - r), V(cy - r, cz), V(cy, cz + r))]
    tool = b.Solid.extrude(b.Face(b.Wire(e)), b.Vector(x1 - x0, 0, 0))
    floor = min(tool.faces(), key=lambda f: f.center().X)   # the face at the pocket floor
    return tool.fillet(t["r_floor"], floor.edges())


def _arc_pt(c, r, a):
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def _rear_centres():
    """(R10 axis, R6 axis) (Y, Z) of the rear end: the R10 tangent to the floor, the R6 tangent to the top line and internally tangent to it."""
    r_lo, r_hi, y = SP_REAR["r_floor"], SP_REAR["r_top"], SP_REAR["y"]
    c_lo = (y, FLOOR_Z + r_lo)
    return c_lo, (y - math.sqrt((r_lo - r_hi) ** 2 - (c_lo[1] - (SP_Z_TOP - r_hi)) ** 2), SP_Z_TOP - r_hi)


def _side_profile(b):
    """Rear clip of the wall (Y, Z) extruded through the slab: the rear end is a R10 round tangent to the floor that is internally tangent to a
    R6 round tangent to the top line (STEP RV23 faces 36 / 37); everything forward of it is kept."""
    r_lo, r_hi = SP_REAR["r_floor"], SP_REAR["r_top"]
    c_lo, c_hi = _rear_centres()
    a_j = math.atan2(c_hi[1] - c_lo[1], c_hi[0] - c_lo[0])   # direction of the tangency point seen from the R10 axis
    V = lambda p: b.Vector(SLAB_X[0], *p)
    t0, tj, t1 = (c_lo[0], FLOOR_Z), _arc_pt(c_lo, r_lo, a_j), (c_hi[0], SP_Z_TOP)
    a0 = -math.pi / 2                                  # the R10 starts straight below its axis and runs rearwards (clockwise) to the tangency
    e = [b.Edge.make_line(V((t0[0], FLOOR_Z - 1)), V(t0)),
         b.Edge.make_three_point_arc(V(t0), V(_arc_pt(c_lo, r_lo, (a0 + a_j) / 2)), V(tj)),
         b.Edge.make_three_point_arc(V(tj), V(_arc_pt(c_hi, r_hi, (a_j - 1.5 * math.pi) / 2)), V(t1)),   # the R6 runs on clockwise up to straight above its axis
         b.Edge.make_line(V(t1), V((t1[0], SP_Z_TOP + 1))),
         b.Edge.make_line(V((t1[0], SP_Z_TOP + 1)), V((RAMP_REACH, SP_Z_TOP + 1))),
         b.Edge.make_line(V((RAMP_REACH, SP_Z_TOP + 1)), V((RAMP_REACH, FLOOR_Z - 1))),
         b.Edge.make_line(V((RAMP_REACH, FLOOR_Z - 1)), V((t0[0], FLOOR_Z - 1)))]
    return b.Solid.extrude(b.Face(b.Wire(e)), b.Vector(SLAB_X[1] - SLAB_X[0], 0, 0))


def _hull_circles(b, x, c1, r1, c2, r2):
    """Face in the plane X = x: the convex hull of two circles (exact arcs and the two outer tangent lines), r1 >= r2."""
    d = math.dist(c1, c2)
    phi, al = math.atan2(c2[1] - c1[1], c2[0] - c1[0]), math.acos((r1 - r2) / d)
    V = lambda p: b.Vector(x, *p)
    p1, p2 = _arc_pt(c1, r1, phi + al), _arc_pt(c1, r1, phi - al)
    q1, q2 = _arc_pt(c2, r2, phi + al), _arc_pt(c2, r2, phi - al)
    return b.Face(b.Wire([b.Edge.make_three_point_arc(V(p1), V(_arc_pt(c1, r1, phi + math.pi)), V(p2)), b.Edge.make_line(V(p2), V(q2)),
                          b.Edge.make_three_point_arc(V(q2), V(_arc_pt(c2, r2, phi)), V(q1)), b.Edge.make_line(V(q1), V(p1))]))


def _nose_notch(b):   # cut from the fused wall + nose
    """The nose's inner notch (STEP RV23): the standoff-end post stands in a pocket whose floor is X_POST and whose end is the post's edge, the
    SB boss stays as a R3.5 post (the wedgelet's ring round SB) inside a deeper, full-height pocket X_B whose rear corner is rounded r_round."""
    n = SP_NOSE_PKT
    cx, cy = SP_FRONT["c"]
    z0, z1 = SP_NOSE_Z[0] - SP_NOSE_OVER, SP_NOSE_Z[1] + SP_NOSE_OVER
    post_r = SA[0] - SP_NOSE_Y0                       # the post is as wide as the nose is long ahead of the axis: its front side is flush with the nose front face
    y_post = min(SA[0] + post_r, SB[0] - 2 * n["r_round"])   # the post's rear edge = the pocket B's rear wall (always room left for its rounded corner)
    a = _box(n["x_post"], cx + SP_NOSE_OVER, cy - SP_NOSE_OVER, y_post, z0, z1)
    xb = lambda z: n["x_b"] + (z - FLOOR_Z) * math.tan(math.radians(n["draft_deg"]))   # the pocket's end wall leans in towards its roof
    xz = [(cx + SP_NOSE_OVER, z0), (xb(z0), z0), (xb(n["z_top"]), n["z_top"]), (cx + SP_NOSE_OVER, n["z_top"])]
    pb = b.Solid.extrude(b.Face(b.Wire.make_polygon([b.Vector(x, y_post, z) for x, z in xz], close=True)), b.Vector(0, SB[0] - y_post, 0))
    pb = _S(pb, _cyl(n["r_ring"], xb(z0) - 1, cx + 2 * SP_NOSE_OVER, SB))

    def corner(e):   # the one blend the finder reports here (R1, face 88): the edge where the pocket's end wall meets the post's rear wall
        pts = [e.position_at(t) for t in (0.0, 0.5, 1.0)]
        return all(abs(q.Y - y_post) < GEO_EPS and abs(q.X - xb(q.Z)) < GEO_EPS for q in pts)
    pb = _one(pb.fillet(n["r_round"], [e for e in pb.edges() if corner(e)]))
    # above the pocket's roof the cavity runs on as a tapered slot (walls lean `taper_deg`, like its round end: a cone about the swing axis at
    # the end of the nose run); beside the post it starts at the post's axis height, and the post's round stands up in it
    ce = (cx, cy + SP_NOSE_RUN)
    x0, dz = cx - n["r_slot"], z1 - n["z_top"]
    lean = dz * math.tan(math.radians(n["taper_deg"]))
    cone = b.Solid.make_cone(n["r_slot"], n["r_slot"] - lean, dz, b.Plane(origin=(*ce, n["z_top"]), z_dir=(0, 0, 1)))

    def tapered(y0, y1, z_from):   # the slot's cross-section (X, Z) swept along Y
        xz = [(cx + SP_NOSE_OVER, z_from), (x0, z_from), (x0, n["z_top"]), (x0 + lean, z1), (cx + SP_NOSE_OVER, z1)]
        return b.Solid.extrude(b.Face(b.Wire.make_polygon([b.Vector(x, y0, z) for x, z in xz], close=True)), b.Vector(0, y1 - y0, 0))
    slot = _U(_I(cone, _box(x0, cx + SP_NOSE_OVER, ce[1], ce[1] + n["r_slot"], n["z_top"], z1)), tapered(y_post, ce[1], n["z_top"]))
    over_post = _S(tapered(cy, y_post, SA[1]), _cyl(post_r, x0 - 1, n["x_post"], SA))
    return _U(a, pb, slot, over_post)


def _foot(b):
    """The 1 mm foot under the chassis lobe (STEP RV23 section Z 1.5): a R23 arc with a tangent line off each end (leaning `deg_lo` / `deg_hi`
    off the Y axis), run out to the Y limits, back to the wall at X_IN."""
    f = SP_FOOT
    c, r = f["c"], f["r"]
    ang = {k: math.radians(f[k]) for k in ("a_lo", "a_hi")}   # the radius direction at each tangent point, from +X
    t_lo, t_hi = _arc_pt(c, r, ang["a_lo"]), _arc_pt(c, r, ang["a_hi"])
    end = lambda t, a, y: (t[0] + (y - t[1]) * math.tan(-a), y)   # the tangent line from t, a off the X direction, run out to Y = y
    p_lo, p_hi = end(t_lo, ang["a_lo"], f["y"][0]), end(t_hi, ang["a_hi"], f["y"][1])
    V = lambda p: b.Vector(p[0], p[1], SP_FOOT_Z[0])
    e = [b.Edge.make_line(V(p_lo), V(t_lo)), b.Edge.make_three_point_arc(V(t_lo), V(_arc_pt(c, r, 0.0)), V(t_hi)), b.Edge.make_line(V(t_hi), V(p_hi)),
         b.Edge.make_line(V(p_hi), V((f["x_in"], p_hi[1]))), b.Edge.make_line(V((f["x_in"], p_hi[1])), V((f["x_in"], p_lo[1]))), b.Edge.make_line(V((f["x_in"], p_lo[1])), V(p_lo))]
    return b.Solid.extrude(b.Face(b.Wire(e)), b.Vector(0, 0, SP_FOOT_Z[1] - SP_FOOT_Z[0]))


def _nut_pocket(b):
    n = SP_NUT_POCKET
    from .params import NUT
    return b.Solid.extrude(_hull_circles(b, SP_NUT_RELIEF_X[0], NUT, n["r"], (NUT[0] + n["dy"], n["z"]), n["r2"]), b.Vector(SP_NUT_RELIEF_X[1] - SP_NUT_RELIEF_X[0], 0, 0))


def _flutes(b, body):
    """The three diagonal flutes (STEP RV23): bands `pitch` apart at `deg` below the Y axis, cut `depth` into the outer face (the layer between
    the wall and the wall moved inboard), each from Z0 up to its own level top end (`top`, rear flute first)."""
    from shapely.geometry import LineString, Polygon
    f = SP_FLUTE
    a = math.radians(f["deg"])
    d, nrm = (math.cos(a), -math.sin(a)), (math.sin(a), math.cos(a))
    big = 4 * SP_Z_TOP
    bands = None
    for k in range(f["n"]):
        o = (f["y"] + (k - (f["n"] - 1) / 2) * f["pitch"] * nrm[0], f["z"] + (k - (f["n"] - 1) / 2) * f["pitch"] * nrm[1])
        band = LineString([(o[0] - big * d[0], o[1] - big * d[1]), (o[0] + big * d[0], o[1] + big * d[1])]).buffer(f["w"] / 2, cap_style=2)
        band = band.intersection(Polygon([(-big, f["z0"]), (-big, f["top"][k]), (big, f["top"][k]), (big, f["z0"])]))
        bands = band if bands is None else bands.union(band)
    skin = _S(body, body.moved(b.Location((f["depth"], 0, 0))))
    return _I(skin, _ext(bands, "yz", *SLAB_X))


def _side_seat(key, at, sgn=-1):
    """robot.cad.holes (cutter, FastenerRecord) of one side-panel M3 CSK (bolt_s*): the STEP seats the head SIDE_FACE_X -
    SIDE_BOLT_X below the battered outer face, in a driver bore from the face; clearance runs on through the panel (and
    wedgelet) to the far end of the part it clamps (standoff end SA_X / SB_X, chassis nut wall NUT_X). `sgn` -1 builds the
    left panel's tool, +1 the record for the right."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    far = {"a": SA_X[1], "b": SB_X[1], "c": NUT_X[1]}[key]
    dr, hc = SP_CSK["drive_r"] if key in SP_DRIVER_SEATS else None, SP_CSK["head_clear"]
    tool, rec = hole_tool((sgn * SIDE_FACE_X[key], *at), (-sgn, 0, 0), SIDE_BOLT_DES[key], head="csk", into="through", side="head",
                          sink=SIDE_SINK[key], grip=SIDE_FACE_X[key] - far, fit=SP_CSK["fit"], csk_clear=SP_CSK["csk_clear"],
                          head_clear=hc if dr is None else SP_CSK["lip"] - SIDE_SINK[key])
    if dr is not None:   # the narrower driver bore from outside the face down to the seat; the csk cone is cut off where it meets it (no undercut)
        tool = _U(tool, _cyl(dr, sgn * (SIDE_FACE_X[key] + hc), sgn * SIDE_BOLT_X[key], at))
        tool = _I(tool, _cyl(dr, sgn * (SIDE_FACE_X[key] + hc), sgn * far, at))
    return tool, rec


def _side_body(pin=True):   # pin: kept for the chassis-cutter call (tub_lobes.panel_mating); the STEP panel has no pin hole
    """The left (RV23) panel's solid, drawn in the frame its SP_* tables were measured in (the STEP assembly frame);
    side_joint.side_panel_local re-bases it on its own datum and mirrors it for RV24. RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import Polygon
    b = _b()
    wall = sp_wall(b)   # analytic wall (side_wall.py): cones / planes / one S-bend skin; the profile below trims its rear end
    profile = _side_profile(b)   # the rear end clip
    foot = _foot(b)
    wall = _I(wall, profile)
    nose_blk = nose_body(b)
    # the nose top is the wedgelet's ramp (the swing's 40 deg cone is tangent to it, so a wedge rides up both as one face); like the
    # wedgelet, the ramp's knife toe stands on a printable land at full reach
    z1 = SP_NOSE_Z[1]
    ramp = Polygon([(SP_NOSE_Y0 - SP_NOSE_OVER, FLOOR_Z), (RAMP_REACH, FLOOR_Z), (RAMP_REACH, FLOOR_Z + WEDGE_TOE_H),
                    (SP_TOE_Y0, FLOOR_Z + SP_TOE_RUN * RAMP_SLOPE), (RAMP_REACH - (z1 - FLOOR_Z) / RAMP_SLOPE, z1), (SP_NOSE_Y0 - SP_NOSE_OVER, z1)])
    nose = _I(nose_blk, _ext(ramp, "yz", *SLAB_X))
    bs_ = SP_BOSS      # the standoff-end lip on the post's face: a chamfered ring round SA (STEP RV23 faces 86 / 85 / 2)
    x0, ch = SP_NOSE_PKT["x_post"], bs_["chamfer"]
    boss = _U(b.Solid.make_cone(bs_["r"] + ch, bs_["r"], ch, b.Plane(origin=(x0, *SA), z_dir=(1, 0, 0))), _cyl(bs_["r"], x0 + ch, x0 + bs_["h"], SA))
    body = _U(_S(_U(wall, nose, foot), _nose_notch(b)), boss)   # the inner notch round the wedgelet block is cut through the swing's lead-in too
    # M3 CSK seats with a head bore out through the battered outer face, so a driver reaches the head and the screw backs straight out
    cr_, cx0, cx1 = SP_SA_CLEAR
    cuts = [_side_seat(k, at)[0] for k, at in (("a", SA), ("b", SB), ("c", NUT))] + [
            _cyl(cr_, cx0, cx1, SA),
            _sp_tyre_relief(b),                                                   # rear tyre relief pocket on the inner face
            _nut_pocket(b)]                                                       # relief round the chassis nut lobe
    sh = _S(_S(body, _flutes(b, body)), *cuts)   # the flutes cut first, from the wall as it stands before the seat bores
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh
