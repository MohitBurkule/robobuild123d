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
    return hole_tool((sgn * SIDE_FACE_X[key], *at), (-sgn, 0, 0), SIDE_BOLT_DES[key], head="csk", into="through", side="head",
                     sink=SIDE_SINK[key], grip=SIDE_FACE_X[key] - far, fit="normal",
                     csk_clear=SP_CSK["csk_clear"], head_clear=SP_CSK["head_clear"])


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
    cuts = [_side_seat(k, at)[0] for k, at in (("a", SA), ("b", SB), ("c", NUT))] + [
            _cyl(cr_, cx0, cx1, SA),
            _box(*SP_TYRE_RELIEF),                                                # rear tyre relief on the inner face
            _ext(_round(Polygon(SP_NUT_RELIEF), r_out=SP_NUT_RELIEF_R), "yz", *SP_NUT_RELIEF_X)]                  # 1 mm relief round the chassis nut lobe
    v = SP_VENT
    for y0 in v["y0"]:     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, v["z0"]), (y0 + v["dy"], v["z0"] + v["dz"])]).buffer(v["r"], cap_style=1)
        cuts.append(_ext(sl, "yz", *v["x"]))
    sh = _S(body, *cuts)
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh if s < 0 else _mirror_x(sh)
