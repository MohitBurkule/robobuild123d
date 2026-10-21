"""[fix-S] Side groups: the side panel (wedgelet, fork and hub groups live in their own modules)."""
import math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .side_wall import sp_wall


def _sp_tyre_relief(b):
    """Rear tyre relief pocket cutter: the round-ended slot profile (SP_TYRE_RELIEF: true arcs, r about the rear axis line, r_front
    front corners) extruded from the floor to the inner face, its floor edge filleted r_floor (the side's own relief tool: the
    pocket it cuts is plain, the chassis cutter just loses it)."""
    t = SP_TYRE_RELIEF
    (cy, cz), r, yf, rf, (x0, x1) = t["c"], t["r"], t["y_front"], t["r_front"], t["x"]
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


def _side_body(pin=True):
    """The left (RV23) panel's solid, drawn in the frame its SP_* tables were measured in (the STEP assembly frame);
    side_joint.side_panel_local re-bases it on its own datum and mirrors it for RV24. RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon
    b = _b()
    wall = sp_wall(b)   # analytic wall (side_wall.py): cones / planes / one S-bend skin; the profile below trims its top and rear end
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
    he = SP_HOLLOW_END
    hollow_end = _ext(Point(*he["c"]).buffer(he["r"], ARC_N).intersection(Polygon_([(SP_HOLLOW_X[0], he["c"][1] - he["r"]), (SP_HOLLOW_X[1], he["c"][1] - he["r"]), (SP_HOLLOW_X[1], he["c"][1] + he["r"]), (SP_HOLLOW_X[0], he["c"][1] + he["r"])])),
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
            _sp_tyre_relief(b),                                                   # rear tyre relief pocket on the inner face
            _ext(_round(Polygon(SP_NUT_RELIEF), r_out=SP_NUT_RELIEF_R), "yz", *SP_NUT_RELIEF_X)]                  # 1 mm relief round the chassis nut lobe
    ph = SP_PIN_HOLE
    if pin:   # the chassis cutter has no pin hole: it would leave a loose pin of chassis material
        cuts.append(_cyl(ph["d"] / 2, *ph["x"], ph["at"]))
    v = SP_VENT
    for y0 in v["y0"]:     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, v["z0"]), (y0 + v["dy"], v["z0"] + v["dz"])]).buffer(v["r"], cap_style=1)
        cuts.append(_ext(sl, "yz", *v["x"]))
    sh = _S(body, *cuts)
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh
