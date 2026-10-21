"""[fix-S] Side groups: the side panel (wedgelet, fork and hub groups live in their own modules)."""
import math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _sp_ring(zw, z, b, Polygon):
    """One wall section at height z: the inner-face path, offset by the local thickness, closed by half-round caps and
    resampled from the inner rear corner so every section's points correspond (dense polygon sections: one ruling per
    matched point pair, adjacent facets meet at a fraction of a degree)."""
    L = SP_LOFT
    path = _resample(_pchip_open(_sp_path(zw), L["resample"]), L["path"])
    out = _offset_var(path, [_sp_w(y, zw) for _, y in path])
    ring = path + _end_cap(path[-1], out[-1], path[-2]) + out[::-1] + _end_cap(out[0], path[0], path[1])
    # drop the little loops a variable offset makes inside tight bends, round what is left
    poly = Polygon(ring).buffer(0)
    poly = max(getattr(poly, "geoms", [poly]), key=lambda g: g.area).buffer(L["round"], L["arc"]).buffer(-L["round"], L["arc"])
    rg = list(poly.exterior.coords)[:-1]
    if not poly.exterior.is_ccw:
        rg = rg[::-1]
    k = min(range(len(rg)), key=lambda i: math.dist(rg[i], path[0]))
    rg = rg[k:] + rg[:k] + [rg[k]]
    pts = _resample(rg, L["ring"])[:-1]
    return b.Wire.make_polygon([b.Vector(x, y, z) for x, y in pts], close=True)


def _sp_front_round(b, Polygon, box):
    """Concave round (SP_FRONT_ROUND r) where the swing's leaning inner face meets the nose front face, drawn in the plan
    sketch every SP_FRONT_ROUND["dz"] up the nose: the swing section (inner path, outer side) and the nose front are
    closed by r (buffer +r / -r) and what that adds is lofted (ruled) through the heights."""
    fr, y_f, x_h = SP_FRONT_ROUND, SP_NOSE[0][1], SP_HOLLOW_X[0]
    r, x_o = fr["r"], SLAB_X[0]
    win = box(SP_NOSE[0][0], y_f - fr["win"], x_h, y_f + r)   # reaches r into the nose so the fill overlaps it (no coplanar fuse)
    secs = []
    (z0, z1), n = SP_NOSE_Z, max(1, round((SP_NOSE_Z[1] - SP_NOSE_Z[0]) / fr["dz"]))
    land = SP_W_Z[0] + SP_FOOT_LAND   # the wall stands straight up to here, then leans (see side_panel)
    for z in sorted({z0 + (z1 - z0) * i / n for i in range(n + 1)} | {land}):
        zw = _interp(z, [SP_W_Z[0], land, *SP_W_Z[1:]], [SP_W_Z[0], *SP_W_Z])
        path = [p for p in _resample(_pchip_open(_sp_path(zw), SP_LOFT["resample"]), SP_LOFT["path"]) if p[1] >= y_f - fr["win"] - r]
        swing = Polygon(path + [(x_o, path[-1][1]), (x_o, path[0][1])]).buffer(0)
        solid = swing.union(box(x_o, y_f, x_h, y_f + fr["win"]))
        fill = solid.buffer(r, fr["arc"]).buffer(-r, fr["arc"]).difference(swing.buffer(-fr["sink"])).intersection(win)   # sinks into the wall: no sliver
        fill = max(getattr(fill, "geoms", [fill]), key=lambda g: g.area)
        rg = list(fill.exterior.coords)[:-1]
        if not fill.exterior.is_ccw:
            rg = rg[::-1]
        k = min(range(len(rg)), key=lambda i: (rg[i][1], rg[i][0]))   # start every ring at its rear-most point
        rg = rg[k:] + rg[:k] + [rg[k]]
        secs.append(b.Wire.make_polygon([b.Vector(x, y, z) for x, y in _resample(rg, fr["ring"])[:-1]], close=True))
    return b.Solid.make_loft(secs, ruled=True)


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
    dr, hc = SP_CSK["drive_r"].get(key), SP_CSK["head_clear"]
    tool, rec = hole_tool((sgn * SIDE_FACE_X[key], *at), (-sgn, 0, 0), SIDE_BOLT_DES[key], head="csk", into="through", side="head",
                          sink=SIDE_SINK[key], grip=SIDE_FACE_X[key] - far, fit=SP_CSK["fit"][key], csk_clear=SP_CSK["csk_clear"],
                          head_clear=hc if dr is None else SP_CSK["lip"] - SIDE_SINK[key])
    if dr is not None:   # the narrower driver bore from outside the face down to the seat
        tool = _U(tool, _cyl(dr, sgn * (SIDE_FACE_X[key] + hc), sgn * SIDE_BOLT_X[key], at))
    return tool, rec


def _side_body():
    """The left (RV23) panel's solid, drawn in the frame its SP_* tables were measured in (the STEP assembly frame);
    side_joint.side_panel_local re-bases it on its own datum and mirrors it for RV24. RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon, box
    b = _b()
    # the battered, leaning wall is one smooth (non-ruled) loft through six band sections floor -> top: the inner face
    # path leans out in the front swing and the thickness thins with height (outer face battered), all as smooth
    # functions of Z so the outer surface has no steps.
    # the floor section is repeated SP_FOOT_LAND higher: the wall rises straight for that height before it leans, so
    # the leaning outer face meets the floor in a printable land, not a knife edge
    z0 = SP_W_Z[0]
    secs = [_sp_ring(zw, z, b, Polygon) for zw, z in [(z0, z0), (z0, z0 + SP_FOOT_LAND)] + [(q, q) for q in SP_W_Z[1:]]]
    wall = _U(b.Solid.make_loft(secs[:2], ruled=True), b.Solid.make_loft(secs[1:], ruled=False))
    side = _round(Polygon(SP_TOP), r_out=SP_TOP_R)
    (cy, cz), cr = SP_REAR_ROUND   # rear end a full round over the wheel
    side = side.union(Point(cy, cz).buffer(cr, ARC_N))
    profile = _ext(side, "yz", *SLAB_X)
    foot = _ext(_poly(SP_FOOT), "xy", *SP_FOOT_Z)
    wall = _I(wall, profile)
    nose_plan = _round(Polygon(SP_NOSE), r_out=SP_NOSE_R)
    bt = SP_BATTER
    z_lo, z_hi = bt["z"]
    batter = _ext(_poly([(bt["x0"], z_lo), (bt["x0"] + bt["slope"] * (z_hi - z_lo), z_hi), (bt["far"], z_hi), (bt["far"], z_lo), (bt["x0"], bt["below"])]), "xz", 0.0, bt["depth"])
    # the front swing never stands proud of the battered plane (it meets the nose flush)
    clip = _ext(_poly([(bt["x0"], z_lo), (bt["x0"] + bt["slope"] * (z_hi + SP_CLIP_OVER - z_lo), z_hi + SP_CLIP_OVER),
                       (SLAB_X[0], z_hi + SP_CLIP_OVER), (SLAB_X[0], bt["below"]), (bt["x0"], bt["below"])]), "xz", 0.0, bt["depth"])
    wall = _S(wall, clip)
    nose_blk = _ext(nose_plan, "xy", *SP_NOSE_Z)
    nose = _I(_I(_U(nose_blk, _sp_front_round(b, Polygon, box)), profile), batter)
    # the nose top continues the wedgelet's ramp so a wedge rides up both as one face
    nose = _one(nose).split(b.Plane(origin=(0.0, RAMP_REACH, FLOOR_Z), z_dir=(0.0, RAMP_SLOPE, 1.0)), keep=b.Keep.BOTTOM)
    # like the wedgelet, the ramp's knife toe stands on a printable land at full reach
    toe = _poly([(SP_TOE_Y0, FLOOR_Z), (RAMP_REACH, FLOOR_Z), (RAMP_REACH, FLOOR_Z + WEDGE_TOE_H), (SP_TOE_Y0, FLOOR_Z + SP_TOE_RUN * RAMP_SLOPE)])
    nose = _U(nose, _I(_I(nose_blk, _ext(toe, "yz", *SLAB_X)), batter))
    # the nose's front-outer corner is chamfered back so a wedge or spinner tooth coming in from the front quarter
    # glances off instead of catching the corner
    nose = _one(nose).split(b.Plane(origin=SP_CHAMFER[0], z_dir=SP_CHAMFER[1]), keep=b.Keep.TOP)
    he = SP_HOLLOW_END
    hollow_end = _ext(Point(*he["c"]).buffer(he["r"], ARC_N).intersection(box(SP_HOLLOW_X[0], he["c"][1] - he["r"], SP_HOLLOW_X[1], he["c"][1] + he["r"])),
                      "xy", he["z0"], SP_HOLLOW[-1][1])
    nose = _S(nose, _ext(_poly(SP_HOLLOW), "yz", *SP_HOLLOW_X), hollow_end)       # hollow behind the nose wall, round front end
    bs_ = SP_BOSS
    (bx0, bx1), x_ch, ch = bs_["x"], bs_["x_ch"], bs_["r"] - bs_["r_end"]   # 45 deg chamfer: its X run is its radial drop
    boss = _I(_U(_cyl(bs_["r"], bx0, x_ch, SA), b.Solid.make_cone(bs_["r"], bs_["r_end"], ch, b.Plane(origin=(x_ch, *SA), z_dir=(1, 0, 0))),
                 _cyl(bs_["r_end"], x_ch + ch, bx1, SA)), profile)                 # standoff end boss
    body = _U(wall, nose, foot, boss)
    # M3 CSK seats with a head bore out through the battered outer face, so a driver reaches the head and the screw backs straight out
    cr_, cx0, cx1 = SP_SA_CLEAR
    cuts = [_side_seat(k, at)[0] for k, at in (("a", SA), ("b", SB), ("c", NUT))] + [
            _cyl(cr_, cx0, cx1, SA),
            _box(*SP_TYRE_RELIEF),                                                # rear tyre relief on the inner face
            _ext(_round(Polygon(SP_NUT_RELIEF), r_out=SP_NUT_RELIEF_R), "yz", *SP_NUT_RELIEF_X)]                  # 1 mm relief round the chassis nut lobe
    ph = SP_PIN_HOLE
    cuts.append(_cyl(ph["d"] / 2, *ph["x"], ph["at"]))
    v = SP_VENT
    for y0 in v["y0"]:     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, v["z0"]), (y0 + v["dy"], v["z0"] + v["dz"])]).buffer(v["r"], cap_style=1)
        cuts.append(_ext(sl, "yz", *v["x"]))
    sh = _S(body, *cuts)
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh
