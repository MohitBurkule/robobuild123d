"""[fix-S] Side groups: side panels, wedgelets, forks, standoffs, hubs, wheels / tyres."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _fork_outline(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = (24.5, 26.0) if s > 0 else (-26.5, -25.0)
    outline = Point(36.3, 6.3).buffer(1.95, 48).union(Polygon([(35.0, 4.9), (36.1, 8.2), (41.0, 8.25), (66.68, 1.49), (51.75, 0.75), (39.0, 0.75), (38.0, 1.5)]))
    outline = _round(outline, r_out=0.3, r_in=0.5).union(Polygon([(60.0, 1.27), (66.68, 1.49), (60.0, 2.5)])).buffer(0.15, 8).buffer(-0.15, 8)   # sharp tip, r0.15 (> kerf) where it joins
    p = outline.difference(Point(SB[0], SB[1]).buffer(2.65, 48)).difference(Point(36.3, 6.3).buffer(0.8, 24))
    p = p.difference(_round(Polygon([(44.15, 2.75), (54.0, 2.75), (44.65, 5.42)]), r_out=0.3))   # lightening window
    # laser kerf / min web: the knife tip cannot be cut sharp; keep the full length but end it in a 0.45 mm land
    p = p.union(_round(Polygon([(64.0, 1.2), (66.68, 1.27), (66.68, 1.72), (64.0, 1.95)]), r_out=0.15)).buffer(0)   # r0.15 (> kerf) land corners
    if s < 0:   # the STEP hangs the left fork 1.1 deg nose-down about its standoff (pin-hole play in the cheek)
        from shapely import affinity
        p = affinity.rotate(p, -1.1, origin=SB)
    return p, x0, x1


def fork(s):
    p, x0, x1 = _fork_outline(s)
    return _ext(p, "yz", x0, x1)


def _fork_slot(s):
    """Seat for the fork tine in the wedgelet nose: the tine outline (window filled) swept straight up out of the
    ramp ahead of Y 42, so the slit is open to the top (the tine drops in) and no TPU film is left over the tine."""
    from shapely.geometry import Polygon
    from shapely import affinity
    p, x0, x1 = _fork_outline(s)
    solid = Polygon(p.exterior)
    up = solid
    for k in range(1, 25):
        up = up.union(affinity.translate(solid, 0, 0.5 * k))
    up = up.intersection(Polygon([(42.0, -1), (80, -1), (80, 30), (42.0, 30)])).union(solid)
    return _ext(up.buffer(0), "yz", x0, x1)


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


def _side_seat(key, at, fastener, sgn=-1):
    """robot.cad.holes (cutter, FastenerRecord) of one side-panel M3 CSK (bolt_s*): head on the outer face seat plane at
    |X| SIDE_BOLT_X[key], clearance through the panel (and wedgelet) down to the far end of the part it clamps
    against (standoff end SA_X / SB_X, chassis nut wall NUT_X). `sgn` -1 builds the left panel's tool, +1 the record for the right."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    far = {"a": SA_X[1], "b": SB_X[1], "c": NUT_X[1]}[key]
    return hole_tool((sgn * SIDE_BOLT_X[key], *at), (-sgn, 0, 0), fastener, head="csk", into="through", side="head",
                     grip=SIDE_BOLT_X[key] - far, fit="normal", csk_clear=SP_CSK["csk_clear"], head_clear=SP_CSK["head_clear"])


def side_panel(s):
    """RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon
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
    SIDE_WALL_DEBUG.append(wall)
    nose_plan = _round(Polygon(SP_NOSE), r_out=SP_NOSE_R)
    bt = SP_BATTER
    z_lo, z_hi = bt["z"]
    batter = _ext(_poly([(bt["x0"], z_lo), (bt["x0"] + bt["slope"] * (z_hi - z_lo), z_hi), (bt["far"], z_hi), (bt["far"], z_lo), (bt["x0"], bt["below"])]), "xz", 0.0, bt["depth"])
    nose_blk = _ext(nose_plan, "xy", *SP_NOSE_Z)
    nose = _I(_I(nose_blk, profile), batter)
    # the nose top continues the wedgelet's ramp so a wedge rides up both as one face
    nose = _one(nose).split(b.Plane(origin=(0.0, RAMP_REACH, FLOOR_Z), z_dir=(0.0, RAMP_SLOPE, 1.0)), keep=b.Keep.BOTTOM)
    # like the wedgelet, the ramp's knife toe stands on a printable land at full reach
    toe = _poly([(SP_TOE_Y0, FLOOR_Z), (RAMP_REACH, FLOOR_Z), (RAMP_REACH, FLOOR_Z + WEDGE_TOE_H), (SP_TOE_Y0, FLOOR_Z + SP_TOE_RUN * RAMP_SLOPE)])
    nose = _U(nose, _I(_I(nose_blk, _ext(toe, "yz", *SLAB_X)), batter))
    # the nose's front-outer corner is chamfered back so a wedge or spinner tooth coming in from the front quarter
    # glances off instead of catching the corner
    nose = _one(nose).split(b.Plane(origin=SP_CHAMFER[0], z_dir=SP_CHAMFER[1]), keep=b.Keep.TOP)
    nose = _S(nose, _ext(_poly(SP_HOLLOW), "yz", *SP_HOLLOW_X))                   # hollow behind the nose wall
    br, bx0, bx1 = SP_BOSS
    boss = _I(_cyl(br, bx0, bx1, SA), profile)                                    # standoff end boss
    body = _U(wall, nose, foot, boss)
    # M3 CSK seats with a head bore out through the battered outer face, so a driver reaches the head and the screw backs straight out
    cr_, cx0, cx1 = SP_SA_CLEAR
    cuts = [_side_seat("a", SA, "M3x10")[0], _side_seat("b", SB, "M3x10")[0], _side_seat("c", NUT, "M3x8")[0],
            _cyl(cr_, cx0, cx1, SA),
            _box(*SP_TYRE_RELIEF),                                                # rear tyre relief on the inner face
            _ext(_poly(SP_NUT_RELIEF), "yz", *SP_NUT_RELIEF_X)]                  # 1 mm relief round the chassis nut lobe
    v = SP_VENT
    for y0 in v["y0"]:     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, v["z0"]), (y0 + v["dy"], v["z0"] + v["dz"])]).buffer(v["r"], cap_style=1)
        cuts.append(_ext(sl, "yz", *v["x"]))
    sh = _S(body, *cuts)
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh if s < 0 else _mirror_x(sh)
