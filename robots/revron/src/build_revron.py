"""Revron (RVRN 2.0) generator.

Every part is built here from scratch with build123d, from named dimensions measured on the RVRN 2.0 STEP
(research/rvrn_step, measured with trimesh sections, never imported). The spec (robots/revron/spec.json) references the
parts as `{"type": "model", "file": <this file>, "params": {"part": "<name>"}}`, so `build(part=...)` below is the only
geometry entry point; running this file as a script writes the spec.

Frame: X right, Y forward (weapon end), Z up, floor at Z = 0. RVRN 2.0 assembly frame -> ours: X = -z_ref,
Y = -x_ref, Z = y_ref (a proper rotation, no offset), so left-hand parts (RV02, RV17, RV23) sit at -X.

Architecture (RVRN 2.0 STEP): GR1507 drisk on two 8 mm printed XALT HD weapon mounts (RV03 carries the stator through a
1.5 mm back spacer, RV02 the threaded shaft end in an outboard bearing); a 3 mm aluminium spider on the bell drives two
3 mm Hardox single-tooth eccentric "floating" discs and a 6 mm printed spacer on 4 long M2. The mounts drop onto the
chassis tabs (notch), 4 M3x12 CSK alu screws through the mounts and the chassis lugs into 2 x 25 + 2 x 15 mm alu
standoffs; TPU wedgelets (RV17/18, with the 1.5 mm Ti forks in their cheek slots) and S-shaped TPU side panels
(RV23/24) slide over the standoffs, 6 M3x8 CSK (4 standoff ends + 2 into captive thin nuts in the chassis wall).
Printed closed-top chassis (RV01) with an X-ribbed deck, 1 mm printed base panel on 5 M2 CSK into heat-sets, 0.9 mm
Ti top panel bonded on the deck. N10s in keyhole side-wall pockets drive the rear F1 tyres; O-rings drive the front
micro wheels on the 25 mm standoffs.
"""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# ======================================================================================================================
# Measured layout (RVRN 2.0 STEP, world frame). Each number is a dimension of a feature, not a mesh coordinate list.
# ======================================================================================================================
REF_TO_WORLD = [[0, 0, -1, 0], [-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1]]
WY, WZ = 38.5, 23.5                  # weapon axis (along X)
SA = (30.5, 5.5)                     # 25 mm standoff (RV11): front axle, X 17.5..42.5
SB = (40.5, 4.5)                     # 15 mm standoff (RV10): nose, X 21.5..36.5
SA_X, SB_X = (17.5, 42.5), (21.5, 36.5)
SO_R = 2.5
NUT = (-11.5, 8.5)                   # side-panel screw into a thin M3 nut in the chassis wall (Y, Z)
NUT_X = (27.7, 29.5)
INS = [(-25.0, 10.4), (25.0, 10.4), (-25.0, -21.6), (25.0, -21.6), (0.0, -33.6)]   # 5 floor inserts / base screws
INS_Z = (5.1, 9.1)                   # FS1 M2 heat-set (3.5 OD x 4)
CSK_M2 = 4.5                         # 90 deg countersink at the face for an ISO 10642 M2 flat head (4.4 x 1.2) + 0.1
PANEL_EAR_R = 3.0
BASE_HOLE, TOP_HOLE = 3.4, 3.5         # csk through-holes: wide enough that the 90 deg seat stops short of the far face (no knife edge)
BOSS_R, BOSS_H = 2.6, 0.3            # base-panel ring boss round each screw (keys into a 2.65 x 0.45 recess in the column foot)
# electronics envelopes (catalog boxes at their spec placement, rot z 90): Malenki nano 32 x 20 x 4.4 at (8.67, -3.0, 15.3),
# BBB ant ESC 23.5 x 12 x 5 at (8.63, -7.25, 10.6); the deck cage ribs are dimensioned off these
RX_X, RX_Y, RX_Z = (8.67 - 10.0, 8.67 + 10.0), (-3.0 - 16.0, -3.0 + 16.0), (15.3 - 2.2, 15.3 + 2.2)
WE_X, WE_Y, WE_Z = (8.63 - 6.0, 8.63 + 6.0), (-7.25 - 11.75, -7.25 + 11.75), (10.6 - 2.5, 10.6 + 2.5)
EAR_R = 2.7                          # top-panel corner ear radius: >= CSK_M2 / 2 + 0.4 mm of Ti round the countersink
RY, RZ = -30.5, 11.0                 # N10 shaft (rear axle)
MOTX = 19.6                          # N10 catalog origin |X| (body 3.7..27.5, shaft to 37.5)
N10_KEY = (23.55, 26.15)             # |X| of the chassis key tab between the N10's last two gearbox plates
N10_TOP = 17.0                       # top face of the N10 gearbox plates
# chassis RV01
SWX = 24.55   # power switch X: body side 0.05 clear of the 27.5 inner wall face (was 25.0, 0.4 into it)
CH = dict(x=29.5, y0=-37.6, y1=15.0, z0=2.5, z1=19.5, wall=2.0, deck=17.5, cham=2.0)
# drisk
DR_X = dict(spider=(-8.2, -5.2), disc_a=(-5.2, -2.2), spacer=(-2.2, 3.8), disc_b=(3.8, 6.8))
DR_ROT = -54.889                     # drisk phase about the axis (STEP Drisk_V4 placement)
DISC_R, DISC_ECC, DISC_ECC_A = 16.5, 0.5, -40.0   # eccentric rim: R16.5 centred 0.5 mm towards -40 deg (balances the tooth)
TOOTH_R, TOOTH_A = 23.0, 134.8
BOLT_R, HUB_R = 14.0, 4.5
# motor GR1507: axis X, stator base X 8.4..10.4 on the right mount via the back spacer X 11.9..13.4
MNT_IN, MNT_OUT = 13.4, 21.4         # weapon mount |X| span (8 mm): 4 mm slab + 4 mm battered boss
MNT_SLAB = 17.4
WEAPON_CLEAR_R = 16.0                # chassis material stays outside this radius about the weapon axis (rotor + 1 mm)
BSP_X = (11.9, 13.4)
STAT_HOLE_R, CB_R, CB_CONE_X = 1.12, 2.25, (16.4, 17.15)   # RV03 stator screw clearance d2.24, d4.5 counterbore, its cone
# RV00 weapon lock pin (Build Guide rule; not in the STEP): a d4 TPU pin pushed in from outside through RV02 into one of
# the spider's quarter windows, parked against the window's outer arc. Drisk-local window centre angle 45 deg at r9.6:
# the pin spans r7.6..11.6 (bolt_p heads end at r6.25, window arc r11.7, bolt_d heads start r12.25), its tip stops
# 0.3 mm short of disc_a so only the spider bears on it.
LOCK_R, LOCK_RC, LOCK_A = 2.0, 9.6, 45.0
LOCK_TIP_X = DR_X["spider"][1] - 0.3


# ---------------------------------------------------------------------------------------------------------------- 2D
def _arc(c, r, a0, a1, n=24):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def _poly(pts):
    from shapely.geometry import Polygon
    return Polygon(pts).buffer(0)


def _round(p, r_out=0.0, r_in=0.0):
    """Shapely polygon with convex corners rounded r_out and concave corners r_in (2D fillets)."""
    if r_in:
        p = p.buffer(r_in, join_style=1).buffer(-r_in, join_style=1)
    if r_out:
        p = p.buffer(-r_out, join_style=1).buffer(r_out, join_style=1)
    return p


def _tangent_line_circle(p, c, r, upper=True):
    """Tangent point on circle (c, r) of a line from point p (upper / lower side seen from p)."""
    dx, dy = c[0] - p[0], c[1] - p[1]
    d = math.hypot(dx, dy)
    a = math.atan2(dy, dx)
    b = math.asin(r / d)
    t = a + (b if upper else -b)
    L = math.sqrt(d * d - r * r)
    return (p[0] + L * math.cos(t), p[1] + L * math.sin(t))


# ---------------------------------------------------------------------------------------------------------------- 3D
def _b():
    import build123d as b
    return b


def _face(poly, plane):
    """build123d face of a shapely polygon (with holes) drawn on `plane` ('xy', 'yz', 'xz') at offset 0."""
    b = _b()
    def to3(u, v):
        return {"xy": (u, v, 0.0), "yz": (0.0, u, v), "xz": (u, 0.0, v)}[plane]
    def wire(ring):
        pts = [b.Vector(*to3(u, v)) for u, v in list(ring.coords)[:-1]]
        return b.Wire.make_polygon(pts, close=True)
    polys = getattr(poly, "geoms", [poly])
    faces = []
    for p in polys:
        if p.area < 1e-6:
            continue
        f = b.Face(wire(p.exterior), [wire(i) for i in p.interiors])
        faces.append(f)
    return faces


def _ext(poly, plane, a0, a1):
    """Prism of a shapely polygon on `plane`, extruded along its normal from a0 to a1."""
    b = _b()
    n = {"xy": (0, 0, 1), "yz": (1, 0, 0), "xz": (0, 1, 0)}[plane]
    a0, a1 = min(a0, a1), max(a0, a1)
    out = None
    for f in _face(poly, plane):
        s = b.Solid.extrude(f, b.Vector(*[c * (a1 - a0) for c in n])).moved(b.Location(tuple(c * a0 for c in n)))
        out = s if out is None else out.fuse(s)
    return out


def _cyl(r, a0, a1, c, axis="x"):
    b = _b()
    a0, a1 = min(a0, a1), max(a0, a1)
    d = {"x": (1, 0, 0), "y": (0, 1, 0), "z": (0, 0, 1)}[axis]
    o = {"x": (a0, c[0], c[1]), "y": (c[0], a0, c[1]), "z": (c[0], c[1], a0)}[axis]
    return b.Solid.make_cylinder(r, a1 - a0, b.Plane(origin=o, z_dir=d))


def _box(x0, x1, y0, y1, z0, z1):
    b = _b()
    return b.Solid.make_box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0)).moved(b.Location((min(x0, x1), min(y0, y1), min(z0, z1))))


def _csk(d_hole, d_head, at, axis, sign, depth=8.0, head=3.0):
    """Countersink + clearance for a flat head screw whose head is flush at `at` (face point), shank going `sign`
    along `axis`: a 90 deg cone from d_head at the face down to d_hole, the clearance hole, and a head bore outward."""
    b = _b()
    d = [0.0, 0.0, 0.0]
    d[{"x": 0, "y": 1, "z": 2}[axis]] = float(sign)
    h = (d_head - d_hole) / 2
    cone = b.Solid.make_cone(d_head / 2, d_hole / 2, h, b.Plane(origin=at, z_dir=d))
    hole = b.Solid.make_cylinder(d_hole / 2, depth, b.Plane(origin=at, z_dir=d))
    head = b.Solid.make_cylinder(d_head / 2, head, b.Plane(origin=at, z_dir=[-c for c in d]))
    return cone.fuse(hole, head)


def _one(x):
    """Normalise a boolean result (Solid / Compound / ShapeList) to a single shape."""
    b = _b()
    if isinstance(x, (list, tuple)) or type(x).__name__ == "ShapeList":
        x = list(x)
        return x[0] if len(x) == 1 else b.Compound(x)
    return x


def _U(*s):
    s = [_one(x) for x in s if x is not None]
    return _one(s[0].fuse(*s[1:]).clean()) if len(s) > 1 else s[0]


def _S(base, *c):
    c = [_one(x) for x in c if x is not None]
    base = _one(base)
    return _one(base.cut(*c).clean()) if c else base


def _I(a, b_):
    return _one(_one(a).intersect(_one(b_)))


def _mirror_x(s):
    return s.mirror(_b().Plane.YZ)


def _solid(x):
    b = _b()
    if isinstance(x, b.Solid):
        return x
    sols = x.solids()
    if len(sols) == 1:
        return sols[0]
    return b.Compound(list(sols))


# ====================================================================================================================
# Parts
# ====================================================================================================================
TOP_XY = ((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))


def _panel_seat(which, i):
    """(cutter, FastenerRecord) of the M2 flat-head seat in the base / top panel (robot.cad.holes, head side only): the
    90 deg seat is 4.5 at the face (ISO 10642 dk 3.8 + 0.7: also clears the verifier's 4.4 head); the panels add a wider
    relief hole (BASE_HOLE / TOP_HOLE) so the seat stops short of the far face."""
    sys.path.insert(0, ROOT)
    from robot.cad.holes import hole_tool
    if which == "base":
        x, y = INS[i]
        return hole_tool((x, y, 3.5), (0, 0, 1), "M2x6", head="csk", into="through", side="head", grip=1.0 + BOSS_H, csk_clear=0.7)
    x, y = TOP_XY[i]
    return hole_tool((x, y, 20.4), (0, 0, -1), "M2x5", head="button", into="through", side="head", grip=0.9, cbore=0.0)   # 0.9 Ti is too thin for an M2 flat-head seat (1.2 tall): a button head bears flat on the face, plain 2.2 clearance hole


def _panel_outline(grow):
    """RV26 outline (56.2 x 49.2, R0.8) plus R3.0 ears round the screws that sit 2.6 mm from its edge, so the 4.5
    countersink keeps a rim; `grow` > 0 gives the matching chassis rabbet."""
    from shapely.geometry import Point
    p = _round(_poly([(-28.1 - grow, -36.2 - grow), (28.1 + grow, -36.2 - grow), (28.1 + grow, 13.0 + grow), (-28.1 - grow, 13.0 + grow)]), r_out=0.8)
    for x, y in INS:
        if min(13.0 - y, y + 36.2) < 3.0:
            p = p.union(Point(x, y).buffer(PANEL_EAR_R + grow, 64))
    return _round(p, r_in=0.5)


def base_panel():
    """RV26: 1 mm printed panel under the open chassis, 5 M2 CSK into the floor heat-sets; two 0.45 mm pads under the
    N10 gearboxes preload the motors up into their keyhole pockets."""
    z0, t = 3.5, 1.0
    out = _panel_outline(0.0)
    b = _b()
    body = _solid(_ext(out, "xy", z0, z0 + t))
    for s in (1, -1):   # [fix-D] 0.45: top 4.95, 0.05 under the N10; plain boxes (not shapely polylines) so the base can take a fillet
        pad = b.Pos(s * 22.5, -30.3, z0 + t - 0.01 + 0.2325) * b.Box(9.1, 9.1, 0.465)
        body = body + b.fillet(pad.edges().filter_by(b.Axis.Z), 0.6)
    # the 1 mm skin is thinner than the 1.2 mm M2 flat head: a 0.3 mm ring boss over each screw gives the seat 1.3 mm of
    # material (no knife edge under the head) and keys the panel into the column feet, so side hits shear the bosses, not the screws
    for x, y in INS:
        body = body + b.Pos(x, y, z0 + t - 0.01 + (BOSS_H + 0.01) / 2) * b.Cylinder(BOSS_R, BOSS_H + 0.01)
    # R0.25 where pads and bosses meet the skin: no sharp internal corner in the print (the STEP has r 0.5 at the pads)
    skin_top = z0 + t
    def _base_edge(e):
        if abs(e.center().Z - skin_top) > 0.02 or abs(e.bounding_box().max.Z - e.bounding_box().min.Z) > 1e-3:
            return False
        fs = [f for f in body.faces() if any(e.is_same(x) for x in f.edges())]
        return len(fs) == 2 and any(f.bounding_box().max.Z > skin_top + 0.1 and f.bounding_box().min.Z < skin_top + 0.01 for f in fs)
    body = b.fillet([e for e in body.edges() if _base_edge(e)], 0.25)
    cuts = [_panel_seat("base", i)[0] for i in range(len(INS))] + [_cyl(BASE_HOLE / 2, z0 - 1, z0 + 3, (x, y), "z") for x, y in INS]   # 4.5 countersink (STEP RV26 has 3.2 x 0.5; an ISO 10642 M2 head is 4.4 x 1.2, so a smaller seat leaves it proud and binding) then the 2.2 hole
    return _S(body, *cuts)


def top_panel():
    """0.9 mm Ti top panel: four countersunk 2.2 holes in the corner ears over the insert columns take M2 flat-head thread-forming screws
    into 1.7 pilots in the column tops (the STEP has the holes, not the screws). The
    front notches clear the weapon-mount tabs; it stops at |X| 23 beside the switch so the switch stays reachable."""
    z0, t = 19.5, 0.9
    core = _poly([(-23.0, -24.1), (23.0, -24.1), (23.0, 7.9), (21.0, 7.9), (21.0, 12.9), (-21.0, 12.9), (-21.0, 7.9), (-23.0, 7.9)])
    tab = _poly([(-13.0, 7.0), (13.0, 7.0), (13.0, 11.9), (-13.0, 11.9)])
    notch = [_poly([(s * 13.0, 7.9), (s * 21.0, 7.9), (s * 21.0, 13.5), (s * 13.0, 13.5)]) for s in (1, -1)]
    from shapely.geometry import Point
    ears = [Point(x, y).buffer(EAR_R, 64) for x, y in ((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))]
    blocks = [_poly([(s * 21.0, 8.6), (s * 25.0, 8.6), (s * 25.0, 12.9), (s * 21.0, 12.9)]) for s in (1, -1)] + \
             [_poly([(s * 21.0, -24.1), (s * 25.0, -24.1), (s * 25.0, -19.0), (s * 21.0, -19.0)]) for s in (1, -1)]
    # the ears run into the side edges along concave arcs (STEP): each arc is tangent to the |X| 23 edge and to its ear
    fills = []
    for sx in (1, -1):
        for ey, yt in ((10.4, 1.0), (-21.6, -12.5)):
            d = abs(ey - yt)
            R = (4.0 + d * d - EAR_R ** 2) / (4.0 + 2 * EAR_R)   # (R - 2)^2 + d^2 = (R + EAR_R)^2: arc tangent to the edge and the ear
            cx = sx * (23.0 + R)
            box = _poly([(sx * 23.0, yt), (sx * 26.6, yt), (sx * 26.6, ey), (sx * 23.0, ey)])
            fills.append(box.difference(Point(cx, yt).buffer(R, 128)))
    p = core
    fills += [_poly([(sx * 21.0, 7.9), (sx * 25.0, 7.9), (sx * 25.0, 12.9), (sx * 21.0, 12.9)]) for sx in (1, -1)]
    for q in ears + fills:
        p = p.union(q)
    for q in notch:
        p = p.difference(q)
    p = p.difference(_poly([(-13.0, 11.9), (13.0, 11.9), (13.0, 14.0), (-13.0, 14.0)]))   # tab front edge at Y 11.9
    p = _round(p, r_out=0.4, r_in=1.2)
    body = _ext(p, "xy", z0, z0 + t)
    # 2.2 holes countersunk (90 deg, 4.5 at the top face; STEP 3.65) for M2 flat heads into the column-top pilots: the 1.2 head is
    # deeper than the 0.9 plate, so its tip sinks into the chamfer at the column top
    return _S(body, *[_panel_seat("top", i)[0] for i in range(4)])


def _fork_outline(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = (24.5, 26.0) if s > 0 else (-26.5, -25.0)
    outline = Point(36.3, 6.3).buffer(1.95, 48).union(Polygon([(35.0, 4.9), (36.1, 8.2), (41.0, 8.25), (66.68, 1.49), (51.75, 0.75), (39.0, 0.75), (38.0, 1.5)]))
    outline = _round(outline, r_out=0.3, r_in=0.5).union(Polygon([(60.0, 1.27), (66.68, 1.49), (60.0, 2.5)])).buffer(0.15, 8).buffer(-0.15, 8)   # sharp tip, r0.15 (> kerf) where it joins
    p = outline.difference(Point(SB[0], SB[1]).buffer(2.65, 48)).difference(Point(36.3, 6.3).buffer(0.8, 24))
    p = p.difference(_round(Polygon([(43.85, 2.75), (54.0, 2.75), (44.35, 5.42)]), r_out=0.3))   # lightening window
    # laser kerf / min web: the knife tip cannot be cut sharp; keep the full length but end it in a 0.45 mm land
    p = p.union(Polygon([(64.0, 1.2), (66.68, 1.27), (66.68, 1.72), (64.0, 1.95)])).buffer(0)
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


def _mount_profile(r_top):
    """Weapon mount side profile (Y, Z): a teardrop round the weapon axis (R r_top) running down to the standoffs,
    with the notch that drops over the chassis tab (open to the rear)."""
    c = (WY, WZ)
    t0 = _tangent_line_circle((10.17 if r_top > 8 else 9.0, 19.5), c, r_top, upper=True)
    a0 = math.degrees(math.atan2(t0[1] - c[1], t0[0] - c[0]))
    rim = _arc(c, r_top, a0, -14.5 if r_top > 8 else -5.0, 40)
    pts = rim + [(43.6, 3.6)] + _arc(SB, 3.25, -16.0, -90.0, 12)[1:] + [(15.4, 1.25), (13.2, 2.5), (13.2, 4.5), (15.0, 4.5), (15.0, 5.35), (25.5, 5.35), (26.5, 6.35),   # notch front face on the lug (0 gap): the lug bears a hit before the screws
                 (26.5, 12.55), (25.5, 13.55), (15.0, 13.55), (15.0, 17.5), (13.0, 19.5), ((10.17 if r_top > 8 else 9.0), 19.5)]
    p = _poly(pts)
    return _round(p, r_out=0.0, r_in=0.0)


def weapon_mount(side):
    """RV02 (left, shaft end) / RV03 (right, stator): 8 mm printed XALT HD plates. A 4 mm slab carries the full
    profile; the outer 4 mm is a boss above the standoff line whose outer face is battered (leans in 7.7 deg) so side
    hits glance off. The rear notch drops over the chassis tab: the tab, not the screws, takes fore/aft load."""
    from shapely.geometry import Point, Polygon
    s = 1 if side == "r" else -1
    r_top = 10.0 if side == "r" else 7.0
    prof = _mount_profile(r_top)
    xi, xm, xo = s * MNT_IN, s * MNT_SLAB, s * MNT_OUT
    eps = 0.02 if side == "r" else 0.0           # RV03's STEP slab face sits just inside X 17.40, RV02's on it (feature sections at 17.40)
    slab = _ext(prof, "yz", xi, xm - s * eps)
    # boss: the part of the profile above the line from the notch top to the nose, battered on its outer face
    line_lo = Polygon([(15.0, 19.5), (44.34, 6.34), (60, 6.34), (60, 60), (0, 60), (0, 19.5)])
    bp = prof.intersection(line_lo)
    boss = _ext(bp, "yz", xm - s * eps, xo + s * 0.01)
    # outer battered face (STEP): one plane leaning in with height and towards the nose,
    # |X| = a - kz * Z - ky * Y  (RV02: a 23.48, kz 0.185, ky 0.0168; RV03: 23.88, 0.144, 0.0379)
    a_, kz, ky = (23.88, 0.144, 0.0379) if side == "r" else (23.48, 0.185, 0.0168)
    bb = _b()
    boss = _one(boss).split(bb.Plane(origin=(s * a_, 0.0, 0.0), z_dir=(s * 1.0, ky, kz)), keep=bb.Keep.BOTTOM)
    body = _U(slab, boss)
    cuts = []
    if side == "r":
        cuts.append(_cyl(2.6, -30, 30, (WY, WZ)))                                    # shaft end clearance (5 mm shaft + 0.1)
        bb_ = _b()
        for dy, dz in ((6, 0), (-6, 0), (0, 6), (0, -6)):                           # GR1507 stator M2 on 12 mm
            # catalog hole (robot.cad.holes): button-head M2, head seat on the STEP d4.5 counterbore floor at X 17.15,
            # ISO 273 normal clearance through the 3.75 mm slab; the STEP lead-in cone is left out (flat seat, see reference deviation)
            cut, _ = _stator_hole(s, dy, dz)
            cuts.append(cut)
    else:
        cuts.append(_cyl(3.95, -30, 30, (WY, WZ)))                                   # outboard bearing seat (8 mm)
        cuts.append(_cyl(6.0, xm, xo + s, (WY, WZ)))                                 # shaft nut recess
        cuts.append(_cyl(LOCK_R - 0.05, xi - s, xo + 3 * s, _lock_yz()))             # RV00 lock pin bore: 0.05 radial TPU press (held, pulls by hand)
    for (y, z) in (SA, SB):                                                          # M3 CSK into the standoffs, flush inside
        cuts.append(_mount_csk(s, y, z, "M3x12" if (y, z) == SA else "M3x14")[0])   # catalog CSK hole (robot.cad.holes)
    return _S(body, *cuts)


def _mount_csk(s, y, z, fastener):
    """robot.cad.holes cutter + record for a mount-to-standoff M3 CSK (bolt_u*): head flush in the inner face, ISO 10642
    countersink (d7.0 vs the STEP's 6.2 for a DIN 7991 head: the catalog head must sit in it) and ISO 273 normal 3.4
    clearance through the 4 mm slab, so the notch, not the shank, takes fore/aft load."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool((s * MNT_IN, y, z), (s, 0, 0), fastener, head="csk", into="through", side="head", grip=MNT_SLAB - MNT_IN, fit="normal")


def _stator_hole(s, dy, dz):
    """robot.cad.holes cutter + record for one RV03 stator screw (bolt_wm*): M2x8 button, head on the X 17.15 floor."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    y, z = WY + dy, WZ + dz
    # RV03 battered outer face |X| (STEP plane, see weapon_mount), its highest point 0.7 mm off the hole axis:
    # the surface the hole is measured from on a leaning face
    face = 23.88 - 0.144 * z - 0.0379 * y + 0.7 * math.hypot(0.144, 0.0379)
    depth = face - CB_CONE_X[1]                     # counterbore down to the STEP floor at X 17.15
    cut, rec = hole_tool((s * face, y, z), (-s, 0, 0), "M2x8", head="button", into="through", side="head",
                         grip=face - MNT_IN, cbore=depth, cbore_clear=2 * CB_R - 3.5, fit="normal")
    return _one(cut.solids()[0] if hasattr(cut, "solids") and len(cut.solids()) == 1 else cut), rec


def _switch_hole(yy):
    """robot.cad.holes record for a switch screw: M2x3 button thread-forming up into the 1.7 pilot of the deck pad (3.0 mm of pad above its 16.0 head seat)."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool((SWX, yy, 16.0), (0, 0, 1), "M2x3", head="button", into="tapped", side="thread", engage=3.0)


def motor_back_spacer():
    """1.5 mm printed spacer between the GR1507 stator base and RV03: clears the motor's rear bearing boss and wires."""
    from shapely.geometry import Point
    p = Point(WY, WZ).buffer(10.0, 64).difference(Point(WY, WZ).buffer(3.95, 48))
    from shapely.geometry import Polygon
    ring = Point(WY, WZ).buffer(8.45, 96).difference(Point(WY, WZ).buffer(5.05, 64))
    for sy in (1, -1):   # 4 wire / lightening windows between the screw webs: annular sectors, r0.5 corners
        for sz in (1, -1):
            q = Polygon([(WY + sy * 2.45, WZ + sz * 2.45), (WY + sy * 12, WZ + sz * 2.45), (WY + sy * 12, WZ + sz * 12), (WY + sy * 2.45, WZ + sz * 12)])
            p = p.difference(_round(ring.intersection(q), r_out=0.75))
    for dy, dz in ((6, 0), (-6, 0), (0, 6), (0, -6)):
        p = p.difference(Point(WY + dy, WZ + dz).buffer(1.05, 24))
    return _ext(p, "yz", *BSP_X)


# ------------------------------------------------------------------------------------------------------------ drisk
def _disc_local(u, v):
    """Drisk-local (u, v) -> world (Y, Z): STEP Drisk_V4 rotation about the axis, then the ref -> world map."""
    a = math.radians(DR_ROT)
    xr = u * math.cos(a) - v * math.sin(a) - 38.5
    yr = u * math.sin(a) + v * math.cos(a) + 23.5
    return (-xr, yr)


def _to_world_poly(p):
    from shapely.geometry import Polygon
    ext = [_disc_local(u, v) for u, v in list(p.exterior.coords)]
    ints = [[_disc_local(u, v) for u, v in list(i.coords)] for i in p.interiors]
    return Polygon(ext, ints).buffer(0)


def disc_outline():
    """Single-tooth eccentric disc (local frame): rim R16.5 centred 0.5 mm off towards -40 deg so the rim mass
    balances the tooth; the tooth leaves the rim with a straight leading flank to R23 at 134.8 deg, and its back face
    drops back to the rim; the root is filleted."""
    from shapely.geometry import Point, Polygon
    ea = math.radians(DISC_ECC_A)
    rim = Point(DISC_ECC * math.cos(ea), DISC_ECC * math.sin(ea)).buffer(DISC_R, 128)
    ta = math.radians(TOOTH_A)
    tip = (TOOTH_R * math.cos(ta), TOOTH_R * math.sin(ta))
    tooth = Polygon([tip, (-11.0, 11.6), (-8.0, 8.0), (-16.2, 0.0), (-16.25, 15.0)])
    return _round(rim.union(tooth), r_out=0.2, r_in=0.7)   # r0.2 on the tooth tip: a 0.4 laser-cuttable land


def floating_disc():
    from shapely.geometry import MultiPoint, Point, Polygon
    p = disc_outline()
    def r_bore(a):   # 12 mm bore with 4 ramped drive dogs (90 deg pitch): steep rise 5..18 deg, long ramp back to 55
        t = a % 90.0
        return 12.0 + (1.52 * (t - 5) / 13 if 5 <= t < 18 else 1.52 * (55 - t) / 37 if 18 <= t < 55 else 0.0)
    bore = Polygon([(r_bore(a / 4) * math.cos(math.radians(a / 4)), r_bore(a / 4) * math.sin(math.radians(a / 4))) for a in range(1440)])
    bore = _round(bore, r_out=0.5, r_in=0.5)
    p = p.difference(bore)
    for k in range(4):
        a = math.radians(90 * k)
        p = p.difference(Point(BOLT_R * math.cos(a), BOLT_R * math.sin(a)).buffer(1.1, 32))
    # balance window by the tooth (STEP): a rounded triangle, the hull of three corner radii -- a straight radial-ish back
    # edge at u -13.65, the lower corner at v 4.85, the upper at v 9.1, the inner corner at (-11.65, 7.65)
    p = p.difference(MultiPoint([(-13.2, 4.85), (-13.2, 9.08), (-11.68, 7.65)]).buffer(0.44, 32).convex_hull)
    return p


def disc(which):
    x0, x1 = DR_X[which]
    return _ext(_to_world_poly(floating_disc()), "yz", x0, x1)


def spider():
    """3 mm aluminium spider on the GR1507 bell: 5.2 bore on the shaft collar, 4 M2 on r4.5 into the bell, 4 lobes
    with the r14 stack bolts, 4 quarter windows."""
    from shapely.geometry import Point, Polygon
    p = Point(0, 0).buffer(14.2, 128)
    for k in range(4):
        a = math.radians(90 * k)
        p = p.union(Point(BOLT_R * math.cos(a), BOLT_R * math.sin(a)).buffer(2.3, 48))
    p = _round(p, r_in=0.8)
    for sx in (1, -1):
        for sy in (1, -1):
            q = Point(0, 0).buffer(11.7, 96).intersection(Polygon([(sx * 2.3, sy * 2.3), (sx * 20, sy * 2.3), (sx * 20, sy * 20), (sx * 2.3, sy * 20)]))
            hub = Point(0, 0).buffer(5.6, 64)   # hub ring round the 4 bell screws
            q = q.difference(hub)
            p = p.difference(_round(q, r_out=0.6))
    p = p.difference(Point(0, 0).buffer(2.6, 48))
    for k in range(4):
        a = math.radians(90 * k)
        for r in (HUB_R, BOLT_R):
            p = p.difference(Point(r * math.cos(a), r * math.sin(a)).buffer(1.1, 32))
    return _ext(_to_world_poly(p), "yz", *DR_X["spider"])


def drisk_spacer():
    """6 mm printed spacer between the discs: bore 19.8 round the bell, 4 r14 bolt holes, 4 arc windows."""
    from shapely.geometry import Point, Polygon
    p = Point(0, 0).buffer(16.0, 128).difference(Point(0, 0).buffer(9.9, 96))
    for sx in (1, -1):
        for sy in (1, -1):
            q = Point(0, 0).buffer(14.4, 96).difference(Point(0, 0).buffer(11.5, 96)).intersection(
                Polygon([(sx * 2.0, sy * 2.0), (sx * 20, sy * 2.0), (sx * 20, sy * 20), (sx * 2.0, sy * 20)]))
            p = p.difference(_round(q, r_out=0.5))
    for k in range(4):
        a = math.radians(90 * k)
        p = p.difference(Point(BOLT_R * math.cos(a), BOLT_R * math.sin(a)).buffer(1.1, 32))
    return _ext(_to_world_poly(p), "yz", *DR_X["spacer"])


# ------------------------------------------------------------------------------------------------------------ wheels
def _revolve_x(profile, x_at, c):
    """Solid of revolution about the X axis through c = (Y, Z): profile [(x, r)] in local x from x_at."""
    b = _b()
    pts = [b.Vector(x_at + x, c[0], c[1] + r) for x, r in profile]
    f = b.Face(b.Wire.make_polygon(pts, close=True))
    return b.Solid.revolve(f, 360, b.Axis((0, c[0], c[1]), (1, 0, 0)))


def rear_hub(s):
    """RV21 printed rear hub (16 x 12): blind D-bore on the N10 3 mm D-shaft (the flat drives, the blind end stops it
    axially), O-ring groove inboard between 8 mm flanges, a 14 mm tyre seat with a raised 7 mm crown that holds the F1
    tyre, a 6.5 mm outer lip; M2 grub into a captive nut slot on the flat."""
    from shapely.geometry import Point, Polygon
    # STEP RV21, except: groove flanges 0.7 thick (STEP 0.5, under the 0.63 printable floor) with the groove narrowed
    # symmetrically to 1.1 (the 1.0 O-ring still seats, centre unchanged), and a 0.4 flat on the outer lip (the STEP
    # lip runs out to a knife edge that prints as a ragged single line)
    prof = [(0.0, 0.0), (0.0, 8.0), (0.7, 8.0), (0.95, 7.45), (1.55, 7.45), (1.8, 8.0), (2.5, 8.0), (2.55, 6.9), (2.75, 6.35), (3.35, 6.0),
            (5.25, 6.0), (6.25, 7.0), (8.25, 7.0), (9.25, 6.0), (11.1, 6.0), (11.3, 6.5), (12.0, 6.5), (12.0, 2.88), (11.8, 2.88), (11.8, 0.0)]
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    body = _revolve_x(prof, s * 30.0, (RY, RZ))
    # D outline: R1.6 arc under a flat 0.9 above the axis; the flat carries vertices every 0.1 mm so it stays a facet
    # strip (a two-vertex chord reads as round to section probes); a 0.02 crown keeps the facets from being merged
    fa = math.degrees(math.asin(0.9 / 1.6))
    hx = 1.6 * math.cos(math.radians(fa))
    arc = [(RY + 1.6 * math.cos(math.radians(180.0 - fa + (180.0 + 2 * fa) * k / 59)),
            RZ + 1.6 * math.sin(math.radians(180.0 - fa + (180.0 + 2 * fa) * k / 59))) for k in range(60)]
    d = Polygon(arc + [(RY + hx - 2 * hx * k / 27, RZ + 0.9 - 0.02 * math.sin(math.pi * k / 27)) for k in range(1, 27)])   # 0.02 crown: no face merge
    # blind D-bore (flat 0.9 above the axis); an M2 nut slot open at the inner face (STEP: 4.1 x 2, AF 4 nut + 0.1);
    # the M2 grub threads the nut down onto the flat. Its hole is cut by robot.cad.holes as a tapped (1.6) bore so it
    # stays inside the 1.9 mm tyre-seat flat (a 2.4 clearance hole breaks into both 45 deg ramps as knife edges);
    # the grub is a set screw, so it gets no spec fastener (no head to seat)
    from robot.cad.holes import hole_tool
    top = 6.0   # tyre-seat radius at the grub
    grub, _rec = hole_tool((s * 34.3, RY, RZ + top), (0, 0, -1), "M2x5", head="cap", into="tapped", side="thread", engage=top - 0.9)   # tip 0.4 past the flat: breaks cleanly into the bore (STEP: through)
    slot = _box(s * 29.0, s * 41.0, RY - 2.05, RY + 2.05, RZ + 2.4, RZ + 4.4)
    return _S(body, _ext(d, "yz", s * 29.0, s * 41.0), slot, grub)


def front_hub(s):
    """RV19 micro hub (9 x 9) running on the 25 mm standoff: 6 mm tyre seat between two 9 mm flanges, an O-ring
    groove inboard."""
    # STEP RV19, except all three flanges 0.7 thick (STEP 0.5): the groove flanges grow into the groove (1.1 wide, centre
    # unchanged) and the outer flange grows 0.2 outboard so the 6 mm tyre seat keeps its width
    prof = [(0.0, 2.7), (0.0, 4.5), (0.7, 4.5), (0.75, 3.96), (0.93, 3.7), (1.57, 3.7), (1.75, 3.96), (1.8, 4.5), (2.5, 4.5), (2.5, 4.1), (2.9, 3.7),
            (8.1, 3.7), (8.5, 4.1), (8.5, 4.5), (9.2, 4.5), (9.2, 2.7)]
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    return _revolve_x(prof, s * 30.0, SA)


def tyre(od, idd, x0, x1, c, shoulder=0.0):
    """Rubber tyre envelope; `shoulder` rounds the tread corners (the F1 tyre's moulded R1.2 shoulders, STEP RV22)."""
    if shoulder <= 0:
        return _S(_cyl(od / 2, x0, x1, c), _cyl(idd / 2, x0 - 1, x1 + 1, c))
    R, rs = od / 2, shoulder
    prof = [(0.0, idd / 2)] + [(rs - rs * math.cos(math.radians(a)), R - rs + rs * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    prof += [(x1 - x0 - rs + rs * math.cos(math.radians(a)), R - rs + rs * math.sin(math.radians(a))) for a in range(90, -1, -10)]
    prof += [(x1 - x0, idd / 2)]
    return _revolve_x(prof, x0, c)


def standoff(L_x, c):
    return _S(_cyl(SO_R, *L_x, c), _cyl(1.25, L_x[0] - 1, L_x[1] + 1, c))


# ------------------------------------------------------------------------------------------------------------ wedgelet
WEDGE_TOE_H = 0.85                   # ramp Z = 1 + 1.187 (50.1 - Y) lifted so its toe is a 0.85 mm land at full length
def wedgelet(s):
    """RV17/18 TPU wedgelet (left built, right mirrored), slabs along X measured on the STEP sections:
    an outer block round the 15 mm standoff end (X 36.5..38.5), a ring step (35.5..36.5), a 2.3 mm ramp skin over a
    hollow whose top edge is capped by a raked plane (29..35.5), the cheek round both standoffs with the fork-tail
    kidney slot (21.5..29) and the 2.5 mm fork slot through it, and a nose tab (17.5..21.5). Ramp face 50 deg:
    Z = 1 + 1.187 (50.1 - Y)."""
    from shapely.geometry import LineString, Point, Polygon
    P = lambda pts: Polygon(pts).buffer(0)  # noqa: E731
    s1 = Point(*SB).buffer(3.5, 64).union(P([(40.5, 1.0), (50.1, 1.0), (42.54, 10.0), (39.55, 10.0), (40.23, 8.0)]))
    s2 = Point(*SB).buffer(3.0, 64).union(P([(40.4, 7.5), (39.55, 10.0), (41.92, 10.0), (42.29, 10.31), (50.1, 1.0), (46.68, 1.0), (44.96, 1.5), (40.5, 1.5)]))
    skin = P([(50.1, 1.0), (47.57, 1.0), (46.8, 1.36), (40.79, 8.52), (40.22, 8.04), (37.65, 15.92)])
    cheek = P([(38.05, 15.36), (50.1, 1.0), (26.55, 1.0), (26.59, 6.09), (26.94, 7.22), (27.48, 8.04), (28.7, 9.02), (30.78, 9.78), (32.43, 10.71),
               (36.62, 14.17), (37.1, 12.78), (38.6, 12.78), (37.79, 15.15)])
    in_slot = P([(38.69, 10.9), (39.12, 11.26), (37.79, 15.15), (38.05, 15.36), (50.1, 1.0), (43.75, 1.0), (43.73, 4.82), (43.37, 6.03), (42.91, 6.68),
                 (41.0, 8.6), (40.03, 8.6), (39.52, 10.07)]).union(Point(*SA).buffer(3.5, 64))
    tab = P([(42.78, 6.82), (44.32, 6.1), (44.69, 7.44), (50.1, 1.0), (43.75, 1.0), (43.71, 4.98), (43.37, 6.03)])
    # the nose tab bears on the weapon mount's nose: take the mount's boss outline (its side profile above the
    # notch-to-nose line) out of the tab in 2D and drop any sliver thinner than a TPU wall, so no film is left
    mprof = _mount_profile(7.0 if s < 0 else 10.0).intersection(P([(15.0, 19.5), (44.34, 6.34), (60, 6.34), (60, 60), (0, 60), (0, 19.5)]))
    tab = tab.difference(mprof.buffer(0.4, 32)).buffer(-0.6, join_style=2).buffer(0.6, join_style=2)
    bb = _b()
    sk = _one(_ext(skin, "yz", -35.5, -29.0)).split(bb.Plane(origin=(-34.0, 41.66, 11.06), z_dir=(-1.24, -0.75, 1.0)), keep=bb.Keep.BOTTOM)
    body = _U(_ext(s1, "yz", -38.5, -36.5), _ext(s2, "yz", -36.5, -35.5), sk, _ext(cheek, "yz", -29.0, -21.5), _ext(tab, "yz", -21.5, -17.5) if not tab.is_empty else None)
    kid = LineString([(36.05, 5.15), (36.95, 7.45)]).buffer(0.95, 24)
    cuts = [_ext(cheek.difference(in_slot), "yz", -27.0, -24.5),                  # 2.5 mm fork slot through the cheek
            _cyl(2.6, -39.0, -17.0, SA), _cyl(1.6, -39.0, -17.0, SB), _cyl(2.5, -36.5, -17.0, SB), _ext(kid, "yz", -29.5, -21.0)]
    # TPU cannot print the ramp's knife toe: keep the 50.1 reach but stand the toe on a 0.85 mm land (2 perimeters),
    # the ramp face running parallel to the measured one from there
    toe = P([(48.6, 1.0), (50.1, 1.0), (50.1, 1.0 + WEDGE_TOE_H), (48.6, 1.0 + 1.5 * 1.187)])
    body = _U(body, _I(_ext(toe, "yz", -38.5, -17.5), _ext(s1.union(cheek).union(tab).buffer(0.01), "yz", -38.5, -17.5)))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # the STEP leaves the fork tine and the mount boss inside the TPU nose; cut their seats (the tine slides into a
    # 1.5 mm slit, the TPU nose tab bears on the mount)
    # the nose tab grazes the chassis lug by 0.1 mm: take the chassis out of it (a printed TPU nose conforms)
    return _S(sh, _fork_slot(s), weapon_mount("l" if s < 0 else "r"), chassis())


# ------------------------------------------------------------------------------------------------------------ side panel
SP_IN = [(-43.5, -41.0), (-43.5, -21.3), (-43.0, -19.6), (-41.2, -17.9), (-37.2, -17.2), (-34.4, -15.7), (-32.3, -13.0), (-31.5, -9.9),
         (-31.5, 11.1), (-31.9, 13.4), (-33.6, 17.5), (-35.5, 20.4), (-37.2, 21.9), (-41.2, 23.3), (-42.7, 26.6)]
# the front swing round the front wheel (inner face X at Y 13, 14, 16, 18, 20, 22, 24, 26.6) at three heights: it leans
# out towards the floor so wheel hits ride up it (STEP RV23: inner face at Y 22 is X -47.6 at the floor, -41.6 at Z 7)
SW_Y = (13.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.6)
SW_X = {1.0: (-32.4, -33.4, -36.6, -44.0, -46.3, -47.6, -48.3, -48.6),
        4.0: (-32.2, -32.7, -34.2, -36.7, -43.0, -45.1, -46.0, -46.6),
        7.5: (-31.7, -32.2, -33.2, -34.4, -36.0, -40.5, -43.0, -43.8),
        9.5: (-31.6, -31.9, -32.8, -33.6, -34.6, -36.4, -39.6, -42.3)}
# wall thickness (normal to the inner face) against height: rear / middle run battered 5 -> 2 mm, the swing ~3.4 mm
SP_W_Z = (1.0, 3.0, 6.0, 9.0, 12.0, 16.0)
SP_FOOT_LAND = 0.85
SP_W_REAR = (5.2, 4.9, 4.3, 3.6, 3.0, 2.1)
SP_W_MID = (5.0, 4.8, 3.4, 3.0, 2.5, 2.1)
SP_W_SWING = (3.3, 3.3, 3.0, 2.6, 2.4, 2.1)


def _interp(x, xs, ys):
    if x <= xs[0]:
        return ys[0]
    for (x0, y0), (x1, y1) in zip(zip(xs, ys), zip(xs[1:], ys[1:])):
        if x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
    return ys[-1]


def _sp_path(z):
    """Inner face path (X, Y) of the side wall at height z."""
    ks = sorted(SW_X)
    sw = [_interp(z, ks, [SW_X[k][i] for k in ks]) for i in range(len(SW_Y))]
    return SP_IN[:9] + list(zip(sw, SW_Y))


def _sp_w(y, z):
    r, m, w = (_interp(z, SP_W_Z, t) for t in (SP_W_REAR, SP_W_MID, SP_W_SWING))
    return _interp(y, (-16.0, -12.0, 11.0, 15.0), (r, m, m, w))


SIDE_WALL_DEBUG = []


def side_panel(s):
    """RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon
    b = _b()
    # the battered, leaning wall is one smooth (non-ruled) loft through six band sections floor -> top: the inner face
    # path leans out in the front swing and the thickness thins with height (outer face battered), all as smooth
    # functions of Z so the outer surface has no steps.
    secs = []
    # the floor section is repeated SP_FOOT_LAND higher: the wall rises straight for that height before it leans, so
    # the leaning outer face meets the floor in a printable 0.85 mm land, not a knife edge
    for zw, z in [(SP_W_Z[0], SP_W_Z[0]), (SP_W_Z[0], SP_W_Z[0] + SP_FOOT_LAND)] + [(q, q) for q in SP_W_Z[1:]]:
        path = _resample(_chaikin_open(_sp_path(zw), 3), 240)
        out = _offset_var(path, [_sp_w(y, zw) for _, y in path])
        ring = path + _end_cap(path[-1], out[-1], path[-2]) + out[::-1] + _end_cap(out[0], path[0], path[1])
        # drop the little loops a variable offset makes inside tight bends, round what is left (r 0.6), then
        # resample the outline to 480 points from the inner rear corner so every section's points correspond
        poly = Polygon(ring).buffer(0)
        poly = max(getattr(poly, "geoms", [poly]), key=lambda g: g.area).buffer(0.6, 16).buffer(-0.6, 16)
        rg = list(poly.exterior.coords)[:-1]
        if not poly.exterior.is_ccw:
            rg = rg[::-1]
        k = min(range(len(rg)), key=lambda i: math.dist(rg[i], path[0]))
        rg = rg[k:] + rg[:k] + [rg[k]]
        pts = _resample(rg, 481)[:-1]
        # (dense polygon sections: one ruling per matched point pair, adjacent facets meet at a fraction of a degree)
        secs.append(b.Wire.make_polygon([b.Vector(x, y, z) for x, y in pts], close=True))
    wall = _U(b.Solid.make_loft(secs[:2], ruled=True), b.Solid.make_loft(secs[1:], ruled=False))
    side = _round(Polygon([(-32.9, 1.0), (-32.9, 16.0), (-4.3, 16.0), (17.0, 12.0), (25.0, 10.0), (42.0, 10.0), (50.1, 1.0)]), r_out=1.5)
    side = side.union(Point(-32.9, 8.5).buffer(7.5, 64))                           # rear end a full round over the wheel
    foot = _ext(_poly([(-31.6, -12.0), (-42.0, -11.9), (-40.6, -2.1), (-40.8, 3.3), (-42.9, 13.3), (-31.6, 13.3)]), "xy", 1.0, 2.0)   # 1 mm wide foot under the chassis lobe
    wall = _I(wall, _ext(side, "yz", -60.0, -20.0))
    SIDE_WALL_DEBUG.append(wall)
    nose_plan = _round(Polygon([(-51.6, 26.5), (-51.2, 39.7), (-50.0, 43.0), (-47.9, 45.7), (-45.1, 47.9), (-41.7, 49.6), (-40.0, 50.1), (-38.5, 50.1),
                                (-38.5, 38.7), (-41.6, 38.7), (-42.4, 37.3), (-42.3, 34.9), (-40.5, 34.5), (-40.5, 26.5)]), r_out=0.5)
    batter = _ext(_poly([(-51.6, 1.0), (-51.6 + 0.79 * 15, 16.0), (0.0, 16.0), (0.0, 1.0), (-51.6, -5.0)]), "xz", 0.0, 60.0)   # outer face leans in 38 deg
    nose = _I(_I(_ext(nose_plan, "xy", 1.0, 10.0), _ext(side, "yz", -60.0, -20.0)), batter)
    # the nose top continues the wedgelet's 50 deg ramp (Z = 1 + 1.187 (50.1 - Y)) so a wedge rides up both as one face
    nose = _one(nose).split(b.Plane(origin=(0.0, 50.1, 1.0), z_dir=(0.0, 1.187, 1.0)), keep=b.Keep.BOTTOM)
    # like the wedgelet, the ramp's knife toe stands on a 0.85 mm land at full reach (printable TPU)
    toe = _poly([(47.0, 1.0), (50.1, 1.0), (50.1, 1.0 + WEDGE_TOE_H), (47.0, 1.0 + 3.1 * 1.187)])
    nose = _U(nose, _I(_I(_ext(nose_plan, "xy", 1.0, 10.0), _ext(toe, "yz", -60.0, -20.0)), batter))
    # the nose's front-outer corner is chamfered back (a plane leaning ~55 deg in and ~57 deg back) so a wedge or
    # spinner tooth coming in from the front quarter glances off instead of catching the corner
    nose = _one(nose).split(b.Plane(origin=(-120.0, 0.0, 0.0), z_dir=(1.0, -1.525, -1.4725)), keep=b.Keep.TOP)
    nose = _S(nose, _box(-42.0, -38.4, 26.5, 39.0, 3.0, 10.5))                     # hollow behind the nose wall
    boss = _I(_cyl(3.0, -42.5, -39.5, SA), _ext(side, "yz", -60.0, -20.0))         # standoff end boss
    body = _U(wall, nose, foot, boss)
    # M3 CSK seats (ISO 10642 head 6.6, +0.1 clearance) with a 12 mm head bore out through the battered outer face, so a
    # driver reaches the head and the screw backs straight out
    cuts = [_csk(3.3, 6.7, (-46.26, SA[0], SA[1]), "x", 1, 8.0, 12.0), _csk(3.3, 6.7, (-41.76, SB[0], SB[1]), "x", 1, 8.0, 12.0),
            _csk(3.3, 6.7, (-35.26, NUT[0], NUT[1]), "x", 1, 8.0, 12.0),
            _cyl(2.55, -42.55, -38.0, SA),
            _box(-45.0, -43.4, -38.7, -24.8, 5.0, 15.0),                          # rear tyre relief on the inner face
            _box(-32.5, -31.4, -16.5, 3.0, 3.9, 13.3)]                           # clears the whole chassis nut lobe (STEP: Y -16..2.5, Z 4..13): the panel does not shave it or leave a 0.25 mm shelf under it
    for y0 in (-11.0, -4.5, 2.0):     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, 5.0), (y0 + 5.0, 11.0)]).buffer(1.0, cap_style=1)
        cuts.append(_ext(sl, "yz", -50.0, -36.5))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # belt channel on the inner face: the O-ring runs inside the panel, covered from outside (W8)
    from shapely.geometry import Point
    band = Point(RY, RZ).buffer(7.5 + 1.25, 64).union(Point(*SA).buffer(3.7 + 1.25, 48)).convex_hull
    band = band.buffer(2.0, 64).difference(band.buffer(-2.6, 64))   # the ring the O-ring runs in (+2 mm so no film is left at the panel top), not the whole hull
    return _S(sh, _ext(band, "yz", *sorted((s * 30.5, s * 32.0))))


def _end_cap(p, q, prev, n=5):
    """Points of a half-round cap from p to q (open ends of a band), bulging away from `prev`."""
    cx, cy = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    r = math.dist(p, q) / 2
    a0 = math.atan2(p[1] - cy, p[0] - cx)
    tx, ty = p[0] - prev[0], p[1] - prev[1]
    sgn = 1 if math.cos(a0 + math.pi / 2) * tx + math.sin(a0 + math.pi / 2) * ty > 0 else -1
    return [(cx + r * math.cos(a0 + sgn * math.pi * k / (n + 1)), cy + r * math.sin(a0 + sgn * math.pi * k / (n + 1))) for k in range(1, n + 1)]


def _offset_var(line, ds):
    """Offset of an open (x, y) polyline to its left by a per-point distance (averaged tangent normals, smoothed)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 2, 0)], line[min(i + 2, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty)
        out.append((x - ds[i] * ty / L, y + ds[i] * tx / L))
    return _chaikin_open(out, 0)


def _offset_open(line, d):
    """Offset of an open (x, y) polyline by d to its left (mitre at the vertices, same point count)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 1, 0)], line[min(i + 1, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty)
        out.append((x - d * ty / L, y + d * tx / L))
    return out


def _chaikin_open(p, n):
    for _ in range(n):
        q = [p[0]]
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        q.append(p[-1])
        p = q
    return p


def _band(path, w):
    """Shapely polygon between an open path and its offset by w to the left (round joins)."""
    from shapely.geometry import LineString, Polygon
    off = LineString(path).offset_curve(w, join_style=1)
    oc = list(off.coords)
    if math.dist(oc[0], path[0]) > math.dist(oc[-1], path[0]):
        oc = oc[::-1]
    return Polygon(list(path) + oc[::-1]).buffer(0)


def _loft_yz(pa, xa, pb, xb, n=160):
    """Ruled loft between two shapely outlines in YZ planes at X xa and xb (both resampled to n points from the point
    nearest +Y, so the rulings do not twist)."""
    b = _b()
    def wire(p, x):
        ring = list(p.exterior.coords)[:-1]
        if Polygon(ring).exterior.is_ccw is False:
            ring = ring[::-1]
        k = max(range(len(ring)), key=lambda i: (ring[i][0], -abs(ring[i][1])))
        ring = ring[k:] + ring[:k] + [ring[k]]
        pts = _resample(ring, n + 1)[:-1]
        return b.Wire.make_polygon([b.Vector(x, u, v) for u, v in pts], close=True)
    from shapely.geometry import Polygon
    return b.Solid.make_loft([wire(pa, xa), wire(pb, xb)], ruled=True)


def _resample(line, n):
    from shapely.geometry import LineString
    ln = LineString(line)
    return [tuple(ln.interpolate(i / (n - 1), normalized=True).coords[0]) for i in range(n)]


def _band_wire(path, w, z, n=160):
    """Closed wire of a wall band: the inner face path and its offset by w to the left (shapely, round joins), both
    resampled to n points so bands of different width loft cleanly."""
    from shapely.geometry import LineString
    b = _b()
    off = LineString(path).offset_curve(w, join_style=1)
    oc = list(off.coords)
    if math.dist(oc[0], path[0]) > math.dist(oc[-1], path[0]):
        oc = oc[::-1]
    pts = _resample(path, n) + _resample(oc, n)[::-1]
    return b.Wire.make_polygon([b.Vector(x, y, z) for x, y in pts], close=True)


# ------------------------------------------------------------------------------------------------------------ chassis
def _wall_pocket(x0, x1, z0, z1, y0, y1, r_vert=0.5, r_floor=0.8):
    """Rectangular front-wall pocket cutter (X x Z, floor at y1): R0.5 corners and an R0.8 floor, as in the STEP."""
    b = _b()
    s = _box(x0, x1, y0, y1, z0, z1)
    s = b.fillet(s.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[-1].edges(), r_floor)


def _lattice_pocket(pts, y0=-36.6, y1=-35.5, r_vert=0.45, r_floor=0.95):
    """Cutter of one triangular rear-wall pocket (X, Z outline `pts`): R0.45 corners and an R0.95 floor (the STEP's R0.98),
    so the pocket has no sharp internal corner in the print."""
    b = _b()
    with b.BuildPart() as bp:
        with b.BuildSketch(b.Plane.XZ.offset(-y1)):
            b.Polygon(*pts, align=None)
        b.extrude(amount=y1 - y0)
    s = b.fillet(bp.part.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[0].edges(), r_floor)


def chassis():
    """RV01 printed chassis: a closed-top box printed deck-down (no supports: the deck is the first layer), open
    underneath for the base panel. X-ribbed deck pockets; 5 insert columns floor to deck; N10 keyhole pockets in the
    side walls; a lobe on each side wall with the captive thin M3 nut; front tabs that key the weapon mounts and
    lugs that carry the standoffs."""
    from shapely.geometry import Point, Polygon
    c = CH
    x, y0, y1, z0, z1, w = c["x"], c["y0"], c["y1"], c["z0"], c["z1"], c["wall"]
    plan = _round(Polygon([(-x, y0), (x, y0), (x, y1), (-x, y1)]), r_out=2.0)
    b = _b()
    outer = _ext(plan, "xy", z0, z1)
    # 2 mm chamfer round the top edges (hits slide over)
    top = _round(Polygon([(-x + 2, y0 + 2), (x - 2, y0 + 2), (x - 2, y1 - 2), (-x + 2, y1 - 2)]), r_out=0.5)
    lo = _face(plan, "xy")[0].outer_wire().moved(b.Location((0, 0, z1 - 2.0)))
    hi = _face(top, "xy")[0].outer_wire().moved(b.Location((0, 0, z1)))
    cap = b.Solid.make_loft([lo, hi], ruled=True)
    outer = _U(_ext(plan, "xy", z0, z1 - 2.0), cap)
    inner = _round(Polygon([(-x + w, y0 + w), (x - w, y0 + w), (x - w, y1 - w), (-x + w, y1 - w)]), r_out=1.0)
    body = _S(outer, _ext(inner, "xy", z0 - 1, c["deck"]))
    add = []
    # insert columns (floor to deck): the rear-centre one a round boss on the rear wall, the corner ones blocks merged
    # into the wall corners with a R2.6 nose (STEP)
    add.append(_cyl(2.75, z0, c["deck"] + 0.1, INS[4], "z"))
    # every column foot flares to R3.7 (56 deg cone, prints deck-down without support) so the base-panel boss recess keeps a 1 mm wall
    for px, py in INS:
        add.append(_cyl(3.7, z0, 5.2, (px, py), "z"))
        add.append(_b().Solid.make_cone(3.7, 2.75, 1.4, _b().Plane(origin=(px, py, 5.2 - 0.001), z_dir=(0, 0, 1))))   # 56 deg: no overhang printed deck-down
    for sg in (1, -1):
        def mx(poly):
            return Polygon([(sg * u, v) for u, v in poly.exterior.coords]).buffer(0)
        def nose(x0, y0, dx, dy, r):   # the corner region at (x0, y0) outside an R r round (dx, dy: directions into the block)
            q = Polygon([(x0, y0), (x0 + dx * r, y0), (x0 + dx * r, y0 + dy * r), (x0, y0 + dy * r)])
            return q.difference(Point(x0 + dx * r, y0 + dy * r).buffer(r, 48))
        front_blk = Polygon([(22.25, 7.65), (27.6, 7.65), (27.6, 13.1), (22.25, 13.1)]).difference(nose(22.25, 7.65, 1, 1, 2.5))
        front_blk = front_blk.union(nose(22.25, 13.0, -1, -1, 0.8)).union(nose(27.5, 7.65, -1, -1, 0.8))      # R0.8 fillets into the walls
        rear_blk = Polygon([(22.21, -23.45), (27.6, -23.45), (27.6, -18.85), (22.21, -18.85)]).difference(nose(22.21, -18.85, 1, -1, 2.6))
        rear_blk = rear_blk.union(nose(22.21, -23.4, -1, 1, 0.9)).union(nose(27.5, -18.85, -1, 1, 0.9))
        add.append(_ext(mx(front_blk), "xy", z0, c["deck"] + 0.1))
        add.append(_ext(mx(rear_blk), "xy", z0, c["deck"] + 0.1))
        # motor front stop wall (load path: the N10 gearbox bears on it, not the base screws)
        add.append(_box(sg * 17.7, sg * (x - w + 0.1), -25.4, -23.4, z0, c["deck"] + 0.1))
        # N10 retention comb off the stop wall (deviation from the STEP, which leaves the motor to the hub and grub):
        # a key tab drops between the last two gearbox plates (|X| 23.4 / 26.3, 0.15 each side) so a hit or a drop
        # cannot walk the motor along its shaft, and a 0.4 mm ledge 0.1 over the gearbox plates stops it lifting off the
        # base-panel preload pad when inverted. Both hang from the deck (printed deck-down: no supports) and clear the
        # rounded can, so the motor still drops straight out downwards once the base panel is off.
        add.append(_box(sg * N10_KEY[0], sg * N10_KEY[1], -26.15, -23.4, 16.0, c["deck"] + 0.1))
        add.append(_box(sg * 20.0, sg * (x - w + 0.1), -27.3, -23.4, N10_TOP + 0.1, c["deck"] + 0.1))
        # side lobe with the thin M3 nut (Y -16.3..2.8)
        lobe = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull
        add.append(_ext(lobe, "yz", sg * (x - 0.1), sg * 32.5))
        R_ = 1.95   # root fillet where the lobe leaves the wall (STEP R1.95): 12 ruled slices of the quarter round
        for k in range(12):
            h0, h1 = R_ * k / 12, R_ * (k + 1) / 12
            d0, d1 = (R_ - math.sqrt(R_ * R_ - (R_ - h) ** 2) for h in (h0, h1))
            add.append(_loft_yz(lobe.buffer(d0, join_style=1), sg * (x - 0.1 + h0), lobe.buffer(d1, join_style=1), sg * (x - 0.1 + h1)))
        # front tabs (key into the weapon-mount notches) and inner tab walls
        add.append(_ext(_poly([(18.5, 6.4), (19.5, 5.4), (25.5, 5.4), (26.5, 6.4), (26.5, 12.5), (25.5, 13.5), (19.5, 13.5), (18.5, 12.5)]), "yz", sg * 13.2, sg * 17.6))
        # inner tab wall, its top-front corner cut back on a R15.9 about the weapon axis: the drisk (swept R ~14.8 at the wall)
        # keeps >= 1 mm, so a bent tooth or a chassis flexed by a hit does not rub
        tabw = _poly([(13.0, 2.5), (25.5, 2.5), (26.5, 3.5), (26.5, 12.35), (25.59, 14.75), (15.0, 19.5), (13.0, 19.5)]).difference(Point(WY, WZ).buffer(WEAPON_CLEAR_R, 128))
        add.append(_ext(tabw, "yz", sg * 10.3, sg * 13.3))
        fil = Polygon([(8.3, 14.9), (10.4, 14.9), (10.4, 17.0), (8.3, 17.0)]).difference(Point(8.3, 17.0).buffer(2.0, 48))   # R2 into the front face
        add.append(_ext(Polygon([(sg * u, v) for u, v in fil.exterior.coords]).buffer(0), "xy", z0, c["deck"]))
        # switch pad under the deck (STEP): the switch ears bear on it
        if sg > 0:
            add.append(_ext(_round(Polygon([(22.0, -15.6), (27.5, -15.6), (27.5, 4.4), (22.0, 4.4)]), r_out=1.0), "xy", 16.5, c["deck"] + 0.1))
        # lugs carrying the standoffs (sloped top so they sit under the mount)
        lug = Polygon([(13.0, z0), (26.0, z0), (30.4, 1.0)] + _arc(SA, 4.5, 250, 300, 6) + [(36.6, 2.5)] + _arc(SB, 3.25, 250, 400, 24) + [(15.0, z1), (13.0, z1)])
        lug = _round(lug.convex_hull.difference(Polygon([(26.0, 0.0), (26.0, 2.5), (30.0, 1.0), (40.0, 0.9), (60, 0)])), r_in=0.0)
        add.append(_ext(lug, "yz", sg * 17.5, sg * 21.5))
    for sg in (1, -1):
        # front corner flanges (STEP): a bottom flange that blends from the side wall into the lug, and a top flange
        # that carries the deck chamfer forward to the lug
        blend = [(29.5, 15.0), (28.7, 16.0), (26.5, 18.5), (24.2, 21.0), (22.8, 22.8), (22.0, 24.6), (21.6, 26.3), (21.5, 27.5)]
        # front face of the corners at Y 15.6 with a R2.7 fillet into the lug, R1 outer corner (STEP)
        face = Polygon([(21.4, 13.0), (29.5, 13.0), (29.5, 14.6), (28.5, 15.6), (21.4, 15.6)]).union(
            Polygon([(21.4, 15.5), (24.2, 15.5), (24.2, 18.3), (21.4, 18.3)]).difference(Point(24.2, 18.3).buffer(2.7, 64)))
        add.append(_ext(Polygon([(sg * x_, y_) for x_, y_ in face.exterior.coords]).buffer(0), "xy", z0, 16.4))
        bot = Polygon([(21.5, 13.0), (29.5, 13.0)] + blend)
        add.append(_ext(Polygon([(sg * x_, y_) for x_, y_ in bot.exterior.coords]).buffer(0), "xy", z0, 5.0))
        # 2 x 2.6 gusset (52 deg) in the corner between the flange top and the lug face: printed deck-down the flange top is a
        # ceiling; the gusset narrows its unsupported span and stiffens the flange root
        gus = _ext(_poly([(sg * 21.45, 4.99), (sg * 23.5, 4.99), (sg * 21.45, 7.6)]), "xz", 13.0, 27.5)
        add.append(_I(gus, _ext(Polygon([(sg * x_, y_) for x_, y_ in bot.exterior.coords]).buffer(0), "xy", z0, 8.0)))
        topf = _ext(_poly([(13.0, 19.5), (15.3, 19.5), (23.0, 15.83), (23.0, 13.47), (15.3, 16.4), (13.0, 16.4)]), "yz", sg * 21.4, sg * 29.5)
        add.append(_I(topf, _ext(Polygon([(sg * x_, y_) for x_, y_ in Polygon([(21.4, 13.0), (29.5, 13.0)] + blend + [(21.4, 27.5)]).buffer(0).exterior.coords]).buffer(0), "xy", 10.0, 20.0)))
    body = _U(body, *add)
    cuts = []
    for sg in (1, -1):
        # lug underside: flat to Y 26, then the ramp; a scallop between the two standoffs (STEP)
        cuts.append(_ext(_poly([(10.0, -5.0), (10.0, 2.5), (26.0, 2.5), (30.4, 1.0), (30.4, -5.0)]), "yz", sg * 17.4, sg * 21.6))
        cuts.append(_ext(Point(36.70, -0.66).buffer(3.16, 96), "yz", sg * 17.4, sg * 21.6))   # R3.16 scallop tangent to the lug arc round the nose standoff (STEP section at X 18.8)
        cuts.append(_box(sg * 13.3, sg * 17.5, 12.0, 15.1, z0 - 0.1, 4.5))   # front wall stops at the rabbet under the tab (STEP)
        # motor stop wall: lower inner edge rounded R4.5 (STEP)
        fil = Polygon([(17.6, 4.4), (22.2, 4.4), (22.2, 9.0), (17.6, 9.0)]).difference(Point(22.2, 9.0).buffer(4.5, 64))
        cuts.append(_ext(Polygon([(sg * x_, z_) for x_, z_ in fil.exterior.coords]).buffer(0), "xz", -25.5, -22.4))   # through the R0.9 corner fillet too: no 0.1 mm skin left under it
    # deck X-pocket lightening (from below, 1 mm skin stays)
    dz0, dz1 = c["deck"] - 0.5, c["deck"] + 1.0
    # deck pockets (STEP RV01 at Z 18): an X of 2 mm ribs, two diagonals at slope 0.64
    k_ = 0.6404
    tri = [Polygon([(0.0, -3.07), (-22.25, -3.07 + k_ * 22.25), (-22.25, 12.4), (22.25, 12.4), (22.25, -3.07 + k_ * 22.25)]),
           Polygon([(0.0, -8.13), (22.25, -8.13 - k_ * 22.25), (22.25, -23.4), (17.5, -23.4), (17.5, -23.6), (-17.5, -23.6), (-17.5, -23.4),
                    (-22.25, -23.4), (-22.25, -8.13 - k_ * 22.25)])]
    for t in tri:
        cuts.append(_ext(_round(t, r_out=0.8), "xy", dz0, dz1))
    for sg in (1, -1):   # side pockets: apex R2 towards the centre
        side = Polygon([(sg * 3.72, -5.59), (sg * 22.0, 4.51 + 0.640 * 2.49), (sg * 22.0, -15.71 - 0.6407 * 2.49)])   # right edge at |X| 22.0 (STEP 22.5): 1.0 mm rib to the 23.0 switch slot, not 0.5
        cuts.append(_ext(_round(side, r_out=1.9), "xy", dz0, dz1))
    for xa, xb in ((-26.5, -16.13), (-14.12, -3.75), (3.75, 14.12), (16.13, 26.5)):   # rear deck pockets
        cuts.append(_ext(_round(Polygon([(xa, -34.5), (xb, -34.5), (xb, -26.5), (xa, -26.5)]), r_out=0.6), "xy", dz0, dz1))
    cuts.append(_ext(_round(Polygon([(-2.75, -30.0), (2.75, -30.0), (2.75, -26.5), (-2.75, -26.5)]), r_out=1.2), "xy", dz0, dz1))
    bb = _b()
    for px, py in INS:
        # 3.0 hole floor to deck top, 0.6 chamfers both ends (STEP); the 3.5 M2 heat-set melts into its bottom
        cuts.append(_cyl(1.5, z0 - 1.0, (z1 + 1) if py == -33.6 else z1 - 4.0, (px, py), "z"))
        cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, 4.5 - 0.001), z_dir=(0, 0, 1))))
        if py == -33.6:
            cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, z1 + 0.001), z_dir=(0, 0, -1))))
        else:   # corner columns: a 1.7 thread-forming pilot in the top 4 mm for the top-panel screw (deviation: STEP 3.0 through),
            # under the STEP 0.6 top chamfer, which takes the tip of the M2 flat head that the 0.9 plate is too thin to hold
            cuts.append(_cyl(0.85, z1 - 4.1, z1 + 1, (px, py), "z"))
            cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, z1 + 0.001), z_dir=(0, 0, -1))))
    # switch slot in the deck beside the top panel, 2 M2 pilot holes
    cuts.append(_ext(_round(Polygon([(23.0, -11.6), (26.6, -11.6), (26.6, 0.4), (23.0, 0.4)]), r_out=0.45), "xy", 16.0, z1 + 1))
    for yy in (1.9, -13.1):
        cuts.append(_cyl(0.85, c["deck"] - 3, z1 + 1, (SWX, yy), "z"))
    for sg in (1, -1):
        # N10 keyhole: round seat for the gearbox shaft boss, narrowing to the floor (motor tilts in)
        kh = Point(RY, RZ).buffer(2.5, 64).union(Point(RY, 5.85).buffer(0.85, 24)).convex_hull   # STEP keyhole
        # opened into a U-slot to the floor (deviation): the gearbox boss (4 dia) and the shaft drop in from below with
        # the base panel off, instead of threading the shaft through a closed hole the motor cannot reach in a straight line
        kh = kh.union(Polygon([(RY - 2.05, z0 - 1.0), (RY + 2.05, z0 - 1.0), (RY + 2.05, RZ), (RY - 2.05, RZ)]))
        cuts.append(_ext(kh, "yz", sg * (x - w - 0.5), sg * (x + 0.5)))
        # nut: M3 clearance through lobe + wall, hex pocket on the inside
        cuts.append(_cyl(1.6, sg * 26.0, sg * 33.0, NUT))
        # hex pocket 0.05 under the nut's 5.5 AF / 6.35 corners: the nut is pressed in and cannot shake loose into the bay
        hexp = Polygon([(NUT[0] + 3.12 * math.cos(math.radians(60 * i + 30)), NUT[1] + 3.13 * math.sin(math.radians(60 * i + 30))) for i in range(6)])
        cuts.append(_ext(hexp, "yz", sg * 27.0, sg * 29.5))
        cuts.append(_ext(_round(Polygon([(-7.14, 6.85), (-3.45, 7.05), (-3.45, 7.95), (-6.9, 8.9)]), r_out=0.25), "yz", sg * 29.0, sg * 33.0))
        # standoff holes in the lugs, square key hole
        cuts.append(_cyl(2.5, sg * 17.0, sg * 22.0, SA))
        cuts.append(_cyl(1.6, sg * 17.0, sg * 22.0, SB))
        cuts.append(_ext(_round(Polygon([(20.0, 6.9), (25.0, 6.9), (25.0, 12.0), (20.0, 12.0)]), r_out=0.9), "yz", sg * 10.0, sg * 22.0))
    # rear wall: 1 mm deep triangle lattice on the inner face (STEP)
    lat = []
    for sg in (1, -1):
        lat += [Polygon([(sg * 4.84, 7.0), (sg * 4.84, 15.0), (sg * 12.4, 11.0)]), Polygon([(sg * 26.42, 7.0), (sg * 26.42, 15.0), (sg * 18.85, 11.0)]),
                Polygon([(sg * 10.6, 5.58), (sg * 20.65, 5.58), (sg * 15.6, 9.7)]), Polygon([(sg * 10.6, 16.42), (sg * 20.65, 16.42), (sg * 15.6, 12.3)])]
    for t in lat:
        cuts.append(_lattice_pocket(list(t.exterior.coords)[:-1]))
    # weapon phase wire hole in the front wall
    cuts.append(_ext(_round(Polygon([(7.25, 5.0), (10.25, 5.0), (10.25, 17.0), (7.25, 17.0)]), r_out=1.45), "xz", 12.0, 16.0))
    for xa, xb in ((-18.25, 4.25), (13.25, 18.2)):
        cuts.append(_wall_pocket(xa, xb, 6.55, 15.55, 12.0, 13.85))
    # rabbet for the base panel (recessed flush with the wall bottom lip) and the mating faces of the mounts and side
    # panels: the parts seat on the chassis, they do not share material with it
    pan = _panel_outline(0.05)
    cuts.append(_ext(pan, "xy", z0 - 1.0, 4.5))
    for px, py in INS:   # recess in each column foot for the base-panel ring boss
        cuts.append(_cyl(BOSS_R + 0.3, 4.4, 4.5 + BOSS_H + 0.05, (px, py), "z"))   # 0.25 base fillet round the boss
    for sg in (1, -1):
        cuts.append(_box(sg * 17.65, sg * 27.35, -35.15, -25.45, 4.4, 4.8))   # pad + 0.25 base fillet   # motor preload pads
        # square the R1 inner rear corner where the N10 gearbox plates sit (their corner would bite 0.14 into the round)
        cuts.append(_box(sg * 25.5, sg * (x - w + 0.05), y0 + w - 0.05, y0 + w + 2.0, z0 + 2.0, c["deck"]))
    cuts += [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)]
    body = _S(body, *cuts)
    # electronics cage hung from the deck (up into the 1 mm deck skin through the lightening pockets; prints as part of the deck-down first layers): ribs 0.1 mm off the Malenki's
    # -x / +x / -y faces and the weapon ESC's -y face, so neither board hammers around when the robot is flipped
    (ex0, ex1), (ey0, ey1), ez0 = RX_X, RX_Y, RX_Z[0]
    G_ = 0.1
    ribs = [_box(ex0 - G_ - 1.28, ex0 - G_, -12.0, 8.0, ez0, c["deck"] + 1.1),          # -x, in the gap to the pack
            _box(ex1 + G_, ex1 + G_ + 1.2, -12.0, 8.0, ez0, c["deck"] + 1.1),           # +x
            _box(0.0, 14.6, ey0 - G_ - 1.0, ey0 - G_, WE_Z[0] + 0.9, c["deck"] + 1.1)]   # -y, down over the ESC's end
    return _U(body, *ribs)


# belt guard (not in the STEP: the RVRN 2.0 O-rings run open in the slot between tub wall and side panel; shielded here
# so a spinner tooth or debris cannot reach them from above or through that slot)
BG = dict(clear=0.6,        # roof underside above the O-ring's top run
          t=1.3,            # roof thickness
          x_in=CH["x"],     # inner face glued on the tub side wall
          x_out=32.0,       # outer edge: covers the 30.8..31.8 O-ring; 1.2 mm over the front tyre top
          x_out_rear=31.5,  # beside the rear tyre (inner face |X| 32.5): 1 mm running clearance
          x_foot=27.9,      # rear foot reaches in over the deck chamfer, 0.2 off the top panel (|X| 27.7)
          z_min=12.0,       # front: 1 mm over the front tyre top (Z 11)
          z_max=20.1,       # rear: over the rear pulley wrap (O-ring top Z 19.5)
          y0=-40.0, y1=36.2)


def _belt_top(y):
    """Z of the O-ring's top at Y (outer belt hull: rear hub R 8.5, front hub R 4.7)."""
    from shapely.geometry import LineString, Point
    hull = Point(RY, RZ).buffer(8.5, 64).union(Point(*SA).buffer(4.7, 48)).convex_hull
    yy = min(max(y, hull.bounds[0] + 0.05), hull.bounds[2] - 0.05)
    seg = hull.intersection(LineString([(yy, -50.0), (yy, 50.0)]))
    return seg.bounds[3]


def belt_guard(s):
    """PLA roof over the O-ring: follows its top run at BG clear, clamped between the front-tyre and rear-pulley
    heights; glued along the tub side wall (and, at the rear, on the deck chamfer). Clears the side panel by 0.2."""
    from shapely.geometry import Polygon
    ys = [BG["y0"] + i * 0.5 for i in range(int((BG["y1"] - BG["y0"]) / 0.5) + 1)]
    zb = [BG["z_max"] if y <= RY else min(max(_belt_top(y) + BG["clear"], BG["z_min"]), BG["z_max"]) for y in ys]   # flat over the rear wrap
    prof = Polygon([(y, z) for y, z in zip(ys, zb)] + [(y, z + BG["t"]) for y, z in reversed(list(zip(ys, zb)))])
    roof = _ext(prof, "yz", BG["x_foot"], BG["x_out"])
    c = CH
    x, y0, y1, z0, z1 = c["x"], c["y0"], c["y1"], c["z0"], c["z1"]
    # glue web/foot under the roof's inner edge: down the tub wall face, and onto the deck chamfer at the rear
    fy = [(y, z) for y, z in zip(ys, zb) if y0 + 3.0 <= y <= y1 - 4.0]
    foot = _ext(Polygon([(y, min(z1 - 2.5, z - 3.0)) for y, z in fy] + [(y, z + 0.5) for y, z in reversed(fy)]), "yz", BG["x_foot"], x + 0.5)
    roof = _U(roof, foot)
    # tub envelope (box + 2 mm top chamfer, as chassis()) and the side panel moved 0.2 inboard come out of it
    b = _b()
    plan = _round(Polygon([(-x, y0), (x, y0), (x, y1), (-x, y1)]), r_out=2.0)
    top = _round(Polygon([(-x + 2, y0 + 2), (x - 2, y0 + 2), (x - 2, y1 - 2), (-x + 2, y1 - 2)]), r_out=0.5)
    lo = _face(plan, "xy")[0].outer_wire().moved(b.Location((0, 0, z1 - 2.0)))
    hi = _face(top, "xy")[0].outer_wire().moved(b.Location((0, 0, z1)))
    tub = _U(_ext(plan, "xy", z0 - 2.0, z1 - 2.0), b.Solid.make_loft([lo, hi], ruled=True))
    sp = side_panel(1).moved(_b().Location((-0.2, 0.0, 0.0)))
    rt = 10.75 + 1.0   # rear tyre radius + running clearance
    g = _S(roof, tub, sp, _box(BG["x_foot"] - 1, x, -22.0, 60.0, 0.0, 30.0),   # inboard foot only where the roof is above the deck
           _box(BG["x_out_rear"], BG["x_out"] + 1, RY - rt, RY + rt, 0.0, 30.0),
           _cyl(8.6, x - 0.1, BG["x_out"] + 1, (RY, RZ)))      # rear hub flange (R 8.0): web stops short of it   # foot only over the tub
    return g if s > 0 else _mirror_x(g)


def esc_tray():
    """TPU tray glued to the base panel under the weapon ESC (not in the STEP, where kapton alone holds it): two rails carry
    the board 0.1 mm off, 1 mm lips 0.1 mm off its -x / +x / +y sides (leads leave above the lips at the board mid-plane).
    The deck cage holds -y and the Malenki above it +z, so the ESC cannot rattle inverted; base panel off, it lifts out."""
    (wx0, wx1), (wy0, wy1), wz0 = WE_X, WE_Y, WE_Z[0]
    z0, top, g, w = 4.5, wz0 + 1.0, 0.1, 1.25   # TPU walls >= 1.2
    parts = [_box(wx0 - g - w, wx1 + g + w, wy0, wy1 + g + w, z0, z0 + w)]
    parts += [_box(xa, xa + w, wy0 + 1.0, wy1 - 1.0, z0 + w - 0.01, wz0 - g) for xa in (wx0 + 1.4, wx1 - 2.6)]
    parts += [_box(wx0 - g - w, wx0 - g, wy0, wy1 + g + w, z0 + w - 0.01, top), _box(wx1 + g, wx1 + g + w, wy0, wy1 + g + w, z0 + w - 0.01, top),
              _box(wx0 - g - w, wx1 + g + w, wy1 + g, wy1 + g + w, z0 + w - 0.01, top)]
    return _U(*parts)


# ------------------------------------------------------------------------------------------------------------ misc
def _lock_yz():
    """World (Y, Z) of the RV00 lock pin axis: the spider window at LOCK_A, radius LOCK_RC, in the drisk's modelled phase."""
    a = math.radians(LOCK_A)
    return _disc_local(LOCK_RC * math.cos(a), LOCK_RC * math.sin(a))


def lock_outer_x():
    """|X| just clear of RV02's battered outer face over the pin's head footprint (face: |X| = 23.48 - 0.185 Z - 0.0168 Y)."""
    y, z = _lock_yz()
    return 23.48 - 0.185 * (z - LOCK_HEAD_R) - 0.0168 * (y - LOCK_HEAD_R) + 0.15


LOCK_HEAD_R, LOCK_HEAD_T = 3.5, 1.6


def weapon_lock():
    """RV00 TPU weapon lock (Build Guide safety rule, not in the STEP), in its own frame: the pin axis is local +Z with
    the tip at the origin (the spec places it at the tip, local Z -> world +X). A d4 shank runs back from the tip
    through the spider window and the RV02 bore; outside RV02 a d7 head with a flag tab (pull grip, lanyard eye) stops
    it going in too far. Pulled out along the axis before a fight; while it is in, the spider's window bears on the shank
    and the drisk cannot turn."""
    b = _b()
    head0 = -(lock_outer_x() + LOCK_TIP_X)          # local z of the head's inner face (tip at local 0 = world LOCK_TIP_X)
    shank = b.Solid.make_cylinder(LOCK_R, -head0, b.Plane(origin=(0, 0, head0), z_dir=(0, 0, 1)))
    # lead-in chamfer: full d4 at local -0.5, d3 at the tip (local 0); the cone's wide end meets the shank flush
    tipc = b.Solid.make_cone(LOCK_R, LOCK_R - 0.5, 0.5, b.Plane(origin=(0, 0, -0.5), z_dir=(0, 0, 1)))
    shank = _S(shank, _cyl(LOCK_R + 1, -0.5, 0.5, (0, 0), "z")).fuse(tipc)
    head = b.Solid.make_cylinder(LOCK_HEAD_R, LOCK_HEAD_T, b.Plane(origin=(0, 0, head0 - LOCK_HEAD_T), z_dir=(0, 0, 1)))
    # flag tab: local -X is world +Z (up), so the grip stands above the head; 2 mm lanyard eye near its end
    from shapely.geometry import Point
    flag = Point(0, 0).buffer(2.5, 32).union(Point(-9.0, 0).buffer(2.5, 32)).convex_hull.difference(Point(-9.0, 0).buffer(1.0, 24))
    tab = _ext(flag, "xy", head0 - LOCK_HEAD_T, head0 - LOCK_HEAD_T + 1.2)
    return _U(shank, head, tab)


PARTS = {
    "base_panel": base_panel, "top_panel": top_panel, "chassis": chassis, "motor_back_spacer": motor_back_spacer,
    "mount_l": lambda: weapon_mount("l"), "mount_r": lambda: weapon_mount("r"),
    "fork_l": lambda: fork(-1), "fork_r": lambda: fork(1),
    "spider": spider, "disc_a": lambda: disc("disc_a"), "disc_b": lambda: disc("disc_b"), "drisk_spacer": drisk_spacer,
    "wedgelet_l": lambda: wedgelet(-1), "wedgelet_r": lambda: wedgelet(1),
    "side_panel_l": lambda: side_panel(-1), "side_panel_r": lambda: side_panel(1),
    "rear_hub_l": lambda: rear_hub(-1), "rear_hub_r": lambda: rear_hub(1),
    "front_hub_l": lambda: front_hub(-1), "front_hub_r": lambda: front_hub(1),
    "rear_tyre_l": lambda: tyre(21.5, 14.0, -42.0, -32.5, (RY, RZ), 1.2), "rear_tyre_r": lambda: tyre(21.5, 14.0, 32.5, 42.0, (RY, RZ), 1.2),
    "front_tyre_l": lambda: tyre(11.0, 7.0, -38.5, -32.5, SA, 0.6), "front_tyre_r": lambda: tyre(11.0, 7.0, 32.5, 38.5, SA, 0.6),
    "so_a_l": lambda: standoff((-SA_X[1], -SA_X[0]), SA), "so_a_r": lambda: standoff(SA_X, SA),
    "so_b_l": lambda: standoff((-SB_X[1], -SB_X[0]), SB), "so_b_r": lambda: standoff(SB_X, SB),
    "weapon_lock": weapon_lock, "esc_tray": esc_tray,
    "belt_guard_l": lambda: belt_guard(-1), "belt_guard_r": lambda: belt_guard(1),
}


def build(part, origin=None):
    """Model-file entry point (robot.shapes `model`): one part in world coordinates, or relative to `origin` (the part's
    `at`, for rotating parts whose frame sits on their spin axis)."""
    s = _solid(PARTS[part]())
    if origin:
        s = s.moved(_b().Location(tuple(-float(v) for v in origin)))
    return s


# ====================================================================================================================
# Spec
# ====================================================================================================================
def make_spec(model_file):
    def M(name, origin=None):
        return {"type": "model", "file": model_file, "params": {"part": name, **({"origin": list(origin)} if origin else {})}}
    WO = (0.0, WY, WZ)   # weapon frame: on the spin axis

    parts, fast, conn = [], [], []
    def P(**k): parts.append(k)
    def F(**k):
        k.setdefault("head", "countersunk"); k.setdefault("tool", "hex2"); k.setdefault("removable", True); fast.append(k)
    def C(a, b, m, r, **k): conn.append(dict(a=a, b=b, method=m, reason=r, **k))
    PLA = dict(material="pla_st", process="fdm")
    SIDES = ((-1, "l"), (1, "r"))

    # ---------------------------------------------------------------- structure
    P(id="tub", kind="structure", print_orientation="-z", rotates_with="fixed", solid_fraction=0.8, color="#2a2c30", shape=M("chassis"), **PLA,
      label="RV01 printed chassis: closed X-ribbed deck (printed deck-down), open floor for the base panel, N10 keyhole side pockets, nut lobes, weapon-mount tabs and standoff lugs")
    P(id="base_panel", kind="structure", print_orientation="+z", rotates_with="fixed", color="#2a2c30", shape=M("base_panel"), **PLA,
      label="RV26 1 mm printed base panel, 5 M2 CSK into the floor heat-sets, 0.45 mm pads preload the N10s")
    P(id="top_panel", kind="armor", material="titanium", process="laser", stock="0.9 mm Ti Gr5 sheet", secondary_ops=["countersink"], rotates_with="fixed", color="#8d939b", shape=M("top_panel"),
      label="0.9 mm Ti top panel: laser outline with 4 countersunk 2.2 corner holes, 4 M2 flat-head thread-forming screws into the column tops (material inferred, see REFERENCE.md)")
    # ---------------------------------------------------------------- weapon module
    P(id="mount_r", kind="structure", print_orientation="+x", rotates_with="fixed", solid_fraction=0.85, color="#2a2c30", shape=M("mount_r"), **PLA,
      label="RV03 XALT HD right weapon mount (8 mm): GR1507 stator on 4 M2 through the back spacer, notch on the chassis tab, 2 M3 CSK into the standoffs")
    P(id="mount_l", kind="structure", parent="mount_r", print_orientation="-x", rotates_with="fixed", solid_fraction=0.85, color="#2a2c30", shape=M("mount_l"), **PLA,
      label="RV02 XALT HD left weapon mount (8 mm): outboard MR85 bearing for the threaded shaft end, notch on the chassis tab, 2 M3 CSK into the standoffs")
    P(id="motor_spacer", kind="other", role="spacer", parent="mount_r", print_orientation="+x", rotates_with="fixed", color="#2a2c30", shape=M("motor_back_spacer"), **PLA,
      label="1.5 mm printed motor back spacer: stator base off the mount, clears the rear bearing boss and the phase leads")
    P(id="weapon_motor", kind="weapon_motor", catalog="gr1507", parent="mount_r", at=[0.0, WY, WZ], rot=[0, 0, 180], rotates_with="fixed", exposed=True,
      exposed_reason="Drisk: the GR1507 bell is the hub of the weapon, inside the spacer bore between the two Hardox discs; the discs shield it radially",
      label="GR1507 outrunner: stator on RV03, bell drives the spider")
    P(id="wbearing", kind="bearing", parent="mount_l", material="steel", process="cots", rotates_with="fixed", stock="MR85ZZ 5 x 8 x 2.5", color="#555555",
      shape=_spec_bearing(), label="MR85ZZ in the RV02 8 mm seat: outboard support of the threaded shaft end (inferred: the STEP shows the 7.9 seat but no bearing)")
    P(id="wshaft", kind="shaft", material="steel", process="cots", stock="GR1507 5 mm shaft (part of the motor): modelled whole, MR85 end X -18.7 through the bell and the rear bearing to its circlip end X 11.4", rotates_with="weapon", shaft_of="weapon_motor", parent="weapon_motor",
      shape={"type": "place", "shape": {"type": "cylinder", "radius": 2.5, "height": 30.1}, "at": [3.65, 0, 0], "rot": [0, 90, 0]}, color="#777777", solid_fraction=0.05,
      label="threaded end of the GR1507 shaft through the MR85 (its mass is in the motor)")
    P(id="spider", kind="weapon", material="aluminium", process="waterjet", stock="3 mm 7075 plate (one 2D profile: water-jet, no milling needed)",
      min_web_mm=0.8, min_web_reason="0.8 mm webs between the dog pockets and the rim are the designer's own (RVRN 2.0 STEP spider_1 measures 0.8 at the same four places)", rotates_with="weapon", parent="mount_r", at=list(WO), shape=M("spider", WO),
      joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [-6.7, WY, WZ], "min": 0, "max": 360, "default": 0}, color="#b8bcc2",
      weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [1, 0, 0], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 1,
              "locking_bar": "weapon_lock"},
      label="3 mm aluminium spider: bolted to the bell (4 M2 on r4.5), carries the disc stack on 4 M2 on r14")
    for nm, lab in (("disc_a", "inner"), ("disc_b", "outer")):
        P(id=nm, kind="other", role="blade", material="hardox", process="laser", stock="3 mm Hardox 450", parent="spider",
          min_web_mm=0.9, min_web_reason="0.9 mm webs beside the balance window are the designer's own (RVRN 2.0 STEP Drisk_floating_3 measures 0.9 at the same four places)", rotates_with="weapon", shape=M(nm, WO), color="#d9dde2",
          label=f"Drisk_floating_3 ({lab}): 3 mm Hardox single-tooth disc, R16.5 rim 0.5 mm eccentric against the R23 tooth, 12 mm bore with 4 ramped dogs, 4 M2 on r14")
    P(id="dspacer", kind="other", role="spacer", parent="spider", rotates_with="weapon", print_orientation="+x", shape=M("drisk_spacer", WO), color="#2a2c30", **PLA,
      label="Drisk_spacer_alt_x: 6 mm printed ring round the bell, 4 arc windows, 4 M2 on r14")
    for s, n in SIDES:
        mnt = f"mount_{n}"
        P(id=f"so_a{n}", kind="pin", role="standoff", material="aluminium", process="cots", rotates_with="fixed", color="#b8bcc2", stock="RV11 M3 x 25 aluminium standoff, 5 OD",
          shape=M(f"so_a_{n}"), label="RV11 25 mm alu standoff: front axle, clamps the mount, the side panel screws to its end")
        P(id=f"so_b{n}", kind="pin", role="standoff", material="aluminium", process="cots", rotates_with="fixed", color="#b8bcc2", stock="RV10 M3 x 15 aluminium standoff, 5 OD",
          shape=M(f"so_b_{n}"), label="RV10 15 mm alu standoff: nose, through the chassis lug, the fork and the wedgelet cheeks")
        P(id=f"fork_{n}", kind="fork", material="titanium", process="laser", stock="1.5 mm Ti Gr5 sheet", min_web_mm=1.05, min_web_reason="1.1 mm web under the 5.3 standoff hole is the designer's own (RVRN 2.0 STEP fork_5 measures 1.1)", parent=f"so_b{n}", rotates_with="fixed", color="#9aa0a6", shape=M(f"fork_{n}"),
          label="fork_5: 1.5 mm Ti fork on the 15 mm standoff, tail pinned in the wedgelet cheek slot")
        P(id=f"wedgelet_{n}", kind="armor", material="tpu", process="fdm", solid_fraction=0.9, print_orientation="-z", parent=f"so_a{n}", rotates_with="fixed", color="#3c4048",
          shape=M(f"wedgelet_{n}"), cover_fasteners_deviation="RVRN 2.0 STEP: the wedgelet is clamped between the side panel nose and the 15 mm standoff end by bolt_s?b (listed in its `through`), and located on both standoffs; bolt_s?a seats the side panel directly on the 25 mm standoff end (the STEP wedgelet stops at |X| 38.5 and never enters that stack). Kept as designed; no extra screw (coordinator decision).",
          label=f"RV1{7 if s < 0 else 8} TPU wedgelet: 50 deg ramp over the nose, cheeks round both standoffs and the fork tail")
        P(id=f"side_{n}", kind="armor", material="tpu", process="fdm", solid_fraction=0.9, print_orientation="+z", parent=f"so_a{n}", rotates_with="fixed", color="#3c4048", shape=M(f"side_panel_{n}"),
          label=f"RV2{3 if s < 0 else 4} TPU side panel: battered S-wall round the wheels, 3 M3x8 CSK (two standoff ends, one chassis nut)")
        P(id=f"belt_guard_{n}", kind="armor", material="pla_st", process="fdm", print_orientation="-x" if s < 0 else "+x", rotates_with="fixed", color="#2a2c30",
          shape=M(f"belt_guard_{n}"),
          label="PLA belt guard (not in the STEP): roof over the O-ring slot between tub wall and side panel, glued to the tub side wall")
        C(f"belt_guard_{n}", "tub", "glue", "PLA guard web/foot CA-glued along the tub side wall and deck chamfer")
        P(id=f"nut_c{n}", kind="nut", catalog="nut_m3_thin", at=[s * 28.6, NUT[0], NUT[1]], rot=[0, 90, 0], rotates_with="fixed")
        # drive
        rot = [0, 0, 0] if s > 0 else [0, 0, 180]
        P(id=f"motor_{n}", kind="motor", catalog="n10_2200rpm_spicy", at=[s * MOTX, RY, RZ], rot=rot, rotates_with="fixed")
        P(id=f"whub_r{n}", kind="pulley", solid_fraction=0.85, rotates_with=f"wheel_r{n}", print_orientation="+x" if s > 0 else "-x", shape=M(f"rear_hub_{n}"), parent="tub",
          joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [s * 41.6, RY, RZ], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
          label="RV21 printed rear hub 16 x 12: blind D-bore on the N10, O-ring groove, crowned F1 tyre seat, M2 grub on the flat")
        P(id=f"wheel_r{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_r{n}", rotates_with=f"wheel_r{n}", parent=f"whub_r{n}", shape=M(f"rear_tyre_{n}"),
          color="#1b1b1b", stock="RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5", label="Scalextric F1 tyre 21.5 x 14 x 9.5")
        P(id=f"whub_f{n}", kind="pulley", solid_fraction=0.85, rotates_with=f"wheel_f{n}", print_orientation="+x" if s > 0 else "-x", shape=M(f"front_hub_{n}"), parent=f"so_a{n}",
          joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [s * 34.5, SA[0], SA[1]], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
          label="RV19 micro hub 9 x 9 greased on the 25 mm standoff, O-ring groove inboard")
        P(id=f"wheel_f{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_f{n}", rotates_with=f"wheel_f{n}", parent=f"whub_f{n}", shape=M(f"front_tyre_{n}"),
          color="#1b1b1b", stock="RV20 Scalextric micro SLX tyre 11 x 7 x 6", label="Scalextric micro tyre 11 x 7 x 6")
    P(id="battery", kind="battery", catalog="lipo_2s_180_turnabot", at=[-11.81, -5.4, 12.0], rot=[0, 0, 90], retained="press_fit")
    P(id="rxesc", kind="esc", catalog="malenki_nano_rvrn2", at=[8.67, -3.0, 15.3], rot=[0, 0, 90], retained="kapton")
    P(id="wesc", kind="esc", catalog="bbb_ant_esc_rvrn2", at=[8.63, -7.25, 10.6], rot=[0, 0, 90], retained="kapton")
    P(id="power_switch", kind="switch", catalog="switch_bbb_ant_rvrn2", at=[SWX, -5.6, 14.25], rot=[0, 0, 90], retained="screws", marked=True, tool_free=True,
      off_dir=[0, -1, 0], label="BBB ant switch hung under the deck beside the top panel: lever flush in the deck slot, 2 M2 into the deck")
    for i, (x, y) in enumerate(INS):
        P(id=f"insert_b{i}", kind="insert", catalog="heatset_m2_4", at=[x, y, (INS_Z[0] + INS_Z[1]) / 2])
    for k in range(4):
        dy, dz = _disc_local(BOLT_R * math.cos(math.radians(90 * k)), BOLT_R * math.sin(math.radians(90 * k)))
        P(id=f"nut_d{k}", kind="nut", catalog="nut_m2", at=[DR_X["disc_b"][1] + 0.8, dy - WY, dz - WZ], rot=[0, 90, 0], rotates_with="weapon", parent="spider")
    P(id="esc_tray", kind="other", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", shape=M("esc_tray"),
      label="TPU weapon-ESC tray (not in the STEP): glued to the base panel, lips hold the ESC when inverted")
    ly, lz = _lock_yz()
    P(id="weapon_lock", kind="locking_bar", role="weapon_lock", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#ff6a00", tethered=True,
      parent="mount_l", at=[LOCK_TIP_X, ly, lz], rot=[0, 90, 0],
      marked=True, tool_free=True, shape=M("weapon_lock"), label="RV00 TPU weapon lock pin (Build Guide rule; not in the STEP): d4 pin pushed through RV02 into a spider window, flag head + lanyard outside")

    # ---------------------------------------------------------------- fasteners
    for i, (x, y) in enumerate(INS):
        F(id=f"bolt_b{i}", designation="M2x6", material="aluminium", at=[x, y, 3.5], dir=[0, 0, 1], through=["base_panel", "tub"], threads_into=f"insert_b{i}", tool="hex1.3",
          hole=_panel_seat("base", i)[1].hole)
    for s, n in SIDES:
        mnt = f"mount_{n}"
        F(id=f"bolt_u{n}a", designation="M3x12", material="aluminium", at=[s * MNT_IN, SA[0], SA[1]], dir=[s, 0, 0], through=[mnt], threads_into=f"so_a{n}", hole=_mount_csk(s, *SA, "M3x12")[1].hole,
          reason="FS9 M3x12 CSK alu, head flush in the mount's inner face")
        F(id=f"bolt_u{n}b", designation="M3x14", reason="M3x14 CSK alu (STEP FS9 M3x12): through mount and lug, 12 mm bites only 3.9 mm of the 15 mm standoff", material="aluminium", at=[s * MNT_IN, SB[0], SB[1]], dir=[s, 0, 0], through=[mnt, "tub"], threads_into=f"so_b{n}", hole=_mount_csk(s, *SB, "M3x14")[1].hole)
        F(id=f"bolt_s{n}a", designation="M3x10", material="aluminium", reason="M3x10 CSK (STEP: M3x8): 8 mm bites only 4.2 mm of the standoff thread; 10 mm gives 6.2 (>= 1.5 d in aluminium)", at=[s * 46.26, SA[0], SA[1]], dir=[-s, 0, 0], through=[f"side_{n}"], threads_into=f"so_a{n}")
        F(id=f"bolt_s{n}b", designation="M3x10", material="aluminium", reason="M3x10 CSK (STEP: M3x8): the head sits 5.3 mm out from the 15 mm standoff end, so 8 mm bites 2.7 mm; 10 mm bites 4.7", at=[s * 41.76, SB[0], SB[1]], dir=[-s, 0, 0], through=[f"side_{n}", f"wedgelet_{n}"], threads_into=f"so_b{n}")
        F(id=f"bolt_s{n}c", designation="M3x8", material="aluminium", reason="alu M3 CSK (Build Guide: aluminium bolts for weight; the STEP draws stainless)", at=[s * 35.26, NUT[0], NUT[1]], dir=[-s, 0, 0], through=[f"side_{n}", "tub"], threads_into=f"nut_c{n}")
    for k, (dy, dz) in enumerate(((6, 0), (-6, 0), (0, 6), (0, -6))):
        F(id=f"bolt_wm{k}", designation="M2x8", head="button", tool="hex1.3", material="titanium", at=[CB_CONE_X[1], WY + dy, WZ + dz], hole=_stator_hole(1, dy, dz)[1].hole, dir=[-1, 0, 0], through=["mount_r", "motor_spacer"],
          threads_into="weapon_motor", reason="button heads (one hex1.3 key for every M2) sunk in the RV03 boss counterbores (inferred: the STEP shows the 4.4 counterbores, not the screws)")
    for k in range(4):
        a = math.radians(90 * k)
        dy, dz = _disc_local(HUB_R * math.cos(a), HUB_R * math.sin(a))
        F(id=f"bolt_p{k}", designation="M2x4", head="button", tool="hex1.3", material="titanium", at=[DR_X["spider"][0], dy, dz], dir=[1, 0, 0], through=["spider"], threads_into="weapon_motor",
          access_before=["weapon_lock", "mount_l", "wbearing"], reason="spider to bell, fitted before the left mount goes on (inferred)")
        dy, dz = _disc_local(BOLT_R * math.cos(a), BOLT_R * math.sin(a))
        F(id=f"bolt_d{k}", designation="M2x18", head="button", tool="hex1.3", material="titanium", at=[DR_X["spider"][0], dy, dz], dir=[1, 0, 0],
          through=["spider", "disc_a", "dspacer", "disc_b"], threads_into=f"nut_d{k}",
          access_before=["weapon_lock", "mount_l", "wbearing", "weapon_motor", "mount_r", "motor_spacer", "tub", "so_al", "so_bl", "so_ar", "so_br"],
          reason="stack bolted up on the bench before it goes on the motor (inferred: the STEP has the 2.2 holes but no screws)")
    for i, (x, y) in enumerate(((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))):
        F(id=f"bolt_t{i}", designation="M2x5", head="button", tool="hex1.3", at=[x, y, 20.4], dir=[0, 0, -1], through=["top_panel"], threads_into="tub",
          reason="M2 flat head in the panel's 90 deg countersink, thread-forming into the 1.7 column-top pilot (inferred: the STEP top panel has the countersunk 2.2 holes but no screws)",
          hole=_panel_seat("top", i)[1].hole)
    for i, yy in enumerate((1.9, -13.1)):
        F(id=f"bolt_sw{i}", designation="M2x3", head="button", tool="hex1.3", at=[SWX, yy, 16.0], dir=[0, 0, 1], through=["power_switch"], threads_into="tub", access_before=["base_panel"], hole=_switch_hole(yy)[1].hole,
          reason="thread-forming into the 1.7 pilot holes either side of the switch flange; heads clamp the flange to the deck underside (inferred)")

    # ---------------------------------------------------------------- connections
    for s, n in SIDES:
        mnt = f"mount_{n}"
        C(f"motor_{n}", "tub", "interlock", "N10 gearbox boss seats in the side-wall keyhole, its front face bears on the stop wall; the base-panel pad preloads it up")
        C(f"whub_r{n}", f"motor_{n}", "press_fit", "Blind D-bore on the 3 mm D-shaft, M2 grub on the flat", interference_mm=0.05, mechanical_key=True)
        C(f"wheel_r{n}", f"whub_r{n}", "press_fit", "F1 tyre (14 ID) stretched over the crowned 14 mm seat", interference_mm=0.3, mechanical_key=True)
        C(f"whub_f{n}", f"so_a{n}", "shaft", "Micro hub runs greased on the 25 mm standoff between the mount face and the side panel")
        C(f"wheel_f{n}", f"whub_f{n}", "press_fit", "Micro tyre stretched into the 7.4 seat between the flanges", interference_mm=0.2, mechanical_key=True)
        for nm in "ab":
            C(f"so_{nm}{n}", mnt, "screw", "M3x12 CSK alu through the mount into the standoff end")
            C(f"so_{nm}{n}", f"side_{n}", "screw", "Side panel screwed to the standoff's outer end (M3x8 CSK)", mechanical_key=True)
        C(f"so_b{n}", "tub", "pin", "Nose standoff clamped between the mount and its chassis lug", mechanical_key=True)
        C(f"so_a{n}", "tub", "pin", "Axle standoff passes through the 5 mm lug hole", mechanical_key=True)
        C(f"fork_{n}", f"so_b{n}", "pin", "Fork hangs on the 15 mm standoff (5.3 hole)", mechanical_key=True)
        C(f"fork_{n}", f"wedgelet_{n}", "interlock", "Fork tail clamped in the wedgelet cheek slot: cannot rotate about the standoff")
        C(f"wedgelet_{n}", f"so_a{n}", "pin", "Wedgelet ring over the axle standoff", mechanical_key=True)
        C(f"wedgelet_{n}", f"so_b{n}", "pin", "Wedgelet cheeks over the nose standoff", mechanical_key=True)
        C(f"wedgelet_{n}", f"side_{n}", "interlock", "Side panel nose holds the wedgelet on the standoffs")
        C(f"side_{n}", "tub", "screw", "Side panel screwed into the captive thin nut in the chassis wall")
        C(f"nut_c{n}", "tub", "press_fit", "Thin M3 nut in the hex pocket inside the wall: cannot turn or fall in", interference_mm=0.05, mechanical_key=True)
        C(mnt, "tub", "interlock", "Mount notch drops over the chassis tab: the tab takes fore/aft and vertical load, the screws only clamp", mechanical_key=True)
        C(f"belt_{n}", f"whub_r{n}", "interlock", "O-ring stretched into the rear hub groove; its tension and the groove flanks keep it on the pulley")
        C(f"belt_{n}", f"whub_f{n}", "interlock", "O-ring in the front hub groove: drives the front wheel")
    C("weapon_motor", "mount_r", "screw", "Stator base on 4 M2 through RV03 and the back spacer")
    C("motor_spacer", "mount_r", "interlock", "Spacer clamped between the stator base and RV03 by the 4 motor screws", mechanical_key=True)
    C("spider", "weapon_motor", "screw", "Spider on the bell, 4 M2 on r4.5; its 5.2 bore centres it on the shaft collar", mechanical_key=True)
    C("disc_a", "spider", "pin", "Disc located and driven by the 4 r14 stack bolts and the spider dogs; the bolts clamp it in shear", mechanical_key=True)
    C("dspacer", "disc_a", "pin", "Spacer on the 4 stack bolts between the discs", mechanical_key=True)
    C("disc_b", "dspacer", "pin", "Outer disc located by the 4 stack bolts through the spacer and clamped by their nuts", mechanical_key=True)
    C("wshaft", "wbearing", "shaft", "Threaded shaft end in the MR85 inner race: second support of the drisk")
    C("wshaft", "weapon_motor", "press_fit", "The shaft is the GR1507 motor's own steel shaft, pressed into the bell at the factory", interference_mm=0.02, mechanical_key=True)
    C("wshaft", "spider", "press_fit", "Spider bore on the shaft collar", interference_mm=0.02, mechanical_key=True)
    C("wbearing", "mount_l", "press_fit", "MR85 pressed into the 7.9 seat", interference_mm=0.05, mechanical_key=True)
    C("mount_l", "mount_r", "interlock", "Both mounts tied by the standoffs and the chassis tabs")
    C("base_panel", "tub", "screw", "Base panel under the open floor, 5 M2 CSK into heat-sets")
    C("top_panel", "tub", "screw", "Ti top panel held by 4 M2 flat-head thread-forming screws through its countersunk corner holes into the column-top pilots (the STEP has the holes, not the screws)")
    C("weapon_lock", "mount_l", "press_fit", "TPU lock pin pressed into the RV02 3.9 bore (0.05 radial grip, pulled by its flag) into a spider window; the head stops it, the lanyard tethers it to the mount", interference_mm=0.05, mechanical_key=True)
    C("battery", "tub", "press_fit", "Pack between the motor wall, the insert columns and the deck", interference_mm=0.1, mechanical_key=True)
    C("rxesc", "tub", "interlock", "Malenki boxed by the deck cage ribs (0.1 mm), the front wall and the deck; the weapon ESC under it")
    C("wesc", "esc_tray", "interlock", "weapon ESC in the TPU tray lips (0.1 mm); the cage rib holds -y, the Malenki +z")
    C("esc_tray", "base_panel", "glue", "TPU tray contact-glued to the base panel top")
    C("power_switch", "tub", "screw", "Switch flange clamped under the deck by 2 M2", mechanical_key=True)

    # O-ring belts (front micro hub <-> rear hub, plane |X| 31.3)
    def belt_shape(s):
        from shapely.geometry import Point
        o = Point(RY, RZ).buffer(7.5 + 1.0, 64).union(Point(*SA).buffer(3.7 + 1.0, 48)).convex_hull
        i = Point(RY, RZ).buffer(7.5, 64).union(Point(*SA).buffer(3.7, 48)).convex_hull
        return {"type": "subtract", "base": _prism_yz(o, s * 30.8, s * 31.8), "cut": [_prism_yz(i, s * 29.0, s * 33.0)]}
    c_ = math.hypot(SA[0] - RY, SA[1] - RZ)
    loop = 2 * math.sqrt(c_ ** 2 - (8.0 - 4.2) ** 2) + math.pi * (8.0 + 4.2) + 2 * (8.0 - 4.2) * math.asin((8.0 - 4.2) / c_)
    ORING = (45, 1.0)
    BELT_L = round(math.pi * ORING[0], 1)
    for s, n in SIDES:
        P(id=f"belt_{n}", kind="belt", material="rubber", process="cots", shape=belt_shape(s), color="#3f7fbf",
          belt={"pulleys": [f"whub_r{n}", f"whub_f{n}"], "kind": "o_ring", "length_mm": BELT_L, "width_mm": ORING[1], "stock": {"id_mm": ORING[0], "cs_mm": ORING[1]}},
          label=f"stock {ORING[0]} x {ORING[1]} nitrile O-ring ({100 * (loop / BELT_L - 1):.0f} % stretch on the 61 mm centres): front wheel drive (not in the STEP; the hub grooves are)")

    wires = [dict(_Wr("w_bat_sw", "battery.jst_rcy", "power_switch.in", 24, "power", 8), connector="jst_rcy"), _Wr("w_sw_wesc", "power_switch.out", "wesc.bat", 24, "power", 8),
             _Wr("w_sw_rx", "power_switch.out", "rxesc.bat", 26, "power", 8), dict(_Wr("w_wesc_m", "wesc.motor", "weapon_motor.phases", 24, "motor", 15), connector="bullet2", count=3,
                 via=[[11.1, 14.5, 16.0], [11.1, 30.0, 14.5]]),   # phases run rearward in the gap behind the drisk (4 mm axial from the stack), into the tub at the deck front
             _Wr("w_rx_wesc", "rxesc.wpn", "wesc.rx", 30, "signal", 6), _Wr("w_m_l", "rxesc.m2", "motor_l.terminals", 28, "motor", 6),
             _Wr("w_m_r", "rxesc.m1", "motor_r.terminals", 28, "motor", 6)]
    return dict(parts=parts, fasteners=fast, connections=conn, wires=wires, intent=intent_checks())


def intent_checks():
    """Functional design-intent probes (robot.checks.intent): each tests what the feature is FOR."""
    out = []
    A = lambda rule, why, **k: out.append(dict(rule=rule, why=why, **k))  # noqa: E731
    for s, n in ((-1, "l"), (1, "r")):
        A("keyed_bore", "the N10 shaft is a 3 mm D; the flat in the blind bore drives the hub (a round printed bore slips at stall)",
          part=f"whub_r{n}", axis="x", at=[s * 35.0, RY, RZ], span=sorted([s * 30.5, s * 40.5]))
        A("tyre_retention", "the F1 tyre (13 mm relaxed ID, assumed; the STEP shows it stretched to 14) is held by stretch over the 45 deg crown, so side hits cannot walk it off",
          hub=f"whub_r{n}", axis=[1, 0, 0], at=[0, RY, RZ], span=sorted([s * 32.5, s * 42.0]), tyre_id=13.0, min_interference=1.0)
        A("captive_nut", "the thin M3 nut sits in a hex pocket inside the wall: with the side panel off it cannot turn or drop into the electronics bay",
          nut=f"nut_c{n}", host="tub", move=0.3)
        A("wheel_clearance", "a tyre rubbing the armour or chassis is a brake on a 2-motor 4WD", wheel=f"wheel_r{n}", exclude=[f"whub_r{n}", f"belt_{n}"], min=1.0)
        A("wheel_clearance", "front tyres run on the standoff axle and must clear the wedgelet and side panel", wheel=f"wheel_f{n}",
          exclude=[f"whub_f{n}", f"so_a{n}", f"belt_{n}"], min=1.0)
        A("flush_head", "side-panel screws sit in TPU countersinks: nothing proud for a spinner to catch", fastener=f"bolt_s{n}a", host=f"side_{n}", out=[s, 0, 0])
        A("flush_head", "mount screws are countersunk in the inner face, the face beside the disc rim", fastener=f"bolt_u{n}a", host=f"mount_{n}", out=[-s, 0, 0])
        A("seat_locates", "the N10 gearbox boss seats in the keyhole and its body bears on the stop walls: shaft concentric, stall torque reacted by the chassis",
          part=f"motor_{n}", host=["tub", "base_panel"], axis=[1, 0, 0], at=[s * MOTX, RY, RZ], play=0.15, turn_deg=2.0)
    for n in ("l", "r"):
        A("notch_bears", "a hit drives the mount back; the notch on the chassis tab bears it in compression, the bolts only clamp",
          part=f"mount_{n}" if n == "l" else "mount_r", lug="tub", bolts=[f"bolt_u{n}a", f"bolt_u{n}b"], dir=[0, -1, 0])
    for pid, up in (("tub", "-z"), ("mount_r", "+x"), ("mount_l", "-x"), ("whub_rr", "+x"), ("whub_rl", "-x"), ("whub_fr", "+x"), ("whub_fl", "-x"),
                    ("wedgelet_r", "-z"), ("wedgelet_l", "-z"), ("side_r", "+z"), ("side_l", "+z"), ("motor_spacer", "+x"), ("weapon_lock", "+z")):
        A("support_free", "every printed part prints without supports in its declared orientation", part=pid, up=up)
    # exceptions (STEP RV01, by design): the rear wall is a triangulated truss - 2 mm ribs round 1 mm deep pockets, the ribs carry
    # the load and the 1 mm web only closes the box; the 1 mm lip below the base-panel rabbet only locates the panel edge
    A("min_wall", "2 mm walls are 4+ perimeters: the box takes wheel-side and clamp loads without delaminating", part="tub", min=1.8, envelope=True,
      **{"except": [[[-29.6, -37.7, 4.6], [29.6, -35.4, 17.5]], [[-33.0, -38.0, 0.0], [33.0, 44.0, 4.6]]]})
    A("insert_column", "printed deck-down, each heat-set insert sits on a solid column back to the deck (the first layers): no hanging boss to pull out",
      part="tub", inserts=[[x, y, CH["deck"]] for x, y in INS], floor_z=INS_Z[0], r=2.2)
    x, w = CH["x"], CH["wall"]
    A("fillet", "inside wall corners are radiused: sharp PLA inside corners crack under impact", part="tub", axis="z", h=10.0,
      at=[[-x + w, CH["y0"] + w], [x - w, CH["y0"] + w], [x - w, CH["y1"] - w], [-x + w, CH["y1"] - w]])
    A("tool_count", "pit kit: one hex key per screw size (1.3 for M2, 2 for M3); the weapon swap needs only the 2 mm key", max=2, module_max=1,
      module=["bolt_ula", "bolt_ulb", "bolt_ura", "bolt_urb"])
    rot = ["spider", "disc_a", "disc_b", "dspacer"] + [f"nut_d{k}" for k in range(4)]
    A("wire_clear_rotor", "phases and power leads stay out of the drisk's swept volume", rotor=rot, axis=[1, 0, 0], at=[0, WY, WZ], min=2.0,
      via={"w_wesc_m": [[11.1, 14.5, 16.0], [11.1, 30.0, 14.5]]})
    return out


def _prism_yz(poly, x0, x1):
    pts = [[round(-z, 4), round(y, 4)] for y, z in list(poly.exterior.coords)[:-1]]
    x0, x1 = min(x0, x1), max(x0, x1)
    return {"type": "place", "shape": {"type": "prism", "points": pts, "height": x1 - x0}, "at": [(x0 + x1) / 2, 0, 0], "rot": [0, 90, 0]}


def _spec_bearing():
    return {"type": "subtract", "base": {"type": "place", "shape": {"type": "cylinder", "radius": 4.0, "height": 2.5}, "at": [-14.75, WY, WZ], "rot": [0, 90, 0]},
            "cut": [{"type": "place", "shape": {"type": "cylinder", "radius": 2.5, "height": 4.0}, "at": [-14.75, WY, WZ], "rot": [0, 90, 0]}]}


def _Wr(i, a, b, awg, kind, sl): return {"id": i, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": sl}


REF_BOM = [   # RVRN 2.0 STEP part list (research/rvrn_step/INDEX.txt); one row per joint or part family
    dict(role="FS8: base panel 5 x M2 CSK into heat-sets", match=["bolt_b*"], count=5, designation="M2x6", head="countersunk", threads_into="insert"),
    dict(role="FS1 M2 heat-sets (floor)", kind="part", match=["insert_b*"], count=5, catalog="heatset_m2_4"),
    dict(role="FS9: mount to standoff 2 x M3x12 CSK alu (axle standoff)", match=["bolt_u?a"], count=2, designation="M3x12", head="countersunk", threads_into="standoff", material="aluminium"),
    dict(role="FS9: mount to nose standoff 2 x M3 CSK alu", match=["bolt_u?b"], count=2, designation="M3x14", head="countersunk", threads_into="standoff", material="aluminium",
         deviation="M3x14 instead of the STEP's M3x12: through mount and lug, 12 mm engages 3.9 mm of the 15 mm standoff (< 1.5 d)"),
    dict(role="top panel: 4 x M2 CSK thread-forming (not in the STEP; its countersunk holes are)", match=["bolt_t*"], count=4, designation="M2x5", threads_into="tub",
         deviation="the STEP top panel has 4 countersunk corner holes but no screws; 4 M2x4 CSK thread-forming screws added so the Ti panel cannot peel off"),
    dict(role="side panel to standoff ends: 4 x M3 CSK (STEP M3x8)", match=["bolt_s?a", "bolt_s?b"], count=4, designation="M3x10", head="countersunk", threads_into="standoff",
         deviation="M3x10 instead of the STEP's M3x8: 8 mm engages 4.2 / 2.7 mm of standoff thread, under 1.5 d in aluminium"),
    dict(role="side panel to chassis: 2 x M3x8 CSK into thin nuts", match=["bolt_s?c"], count=2, designation="M3x8", head="countersunk", threads_into="nut"),
    dict(role="M3 thin nuts (BS EN 24036)", kind="part", match=["nut_c*"], count=2, catalog="nut_m3_thin"),
    dict(role="RV11 25 mm + RV10 15 mm alu standoffs", kind="part", match=["so_*"], count=4, material="aluminium"),
    dict(role="GR1507 weapon motor", kind="part", match=["weapon_motor"], count=1, catalog="gr1507"),
    dict(role="Motor back spacer", kind="part", match=["motor_spacer"], count=1),
    dict(role="spider + 2 Drisk_floating_3 + Drisk_spacer_alt_x", kind="part", match=["spider", "disc_a", "disc_b", "dspacer"], count=4),
    dict(role="fork_5 x 2", kind="part", match=["fork_*"], count=2),
    dict(role="RV17/18 wedgelets", kind="part", match=["wedgelet_*"], count=2, material="tpu"),
    dict(role="RV23/24 side panels", kind="part", match=["side_*"], count=2, material="tpu"),
    dict(role="Top panel 0.9 sheet", kind="part", match=["top_panel"], count=1),
    dict(role="RV15 BBB antweight switch", kind="part", match=["power_switch"], count=1, catalog="switch_bbb_ant_rvrn2"),
    dict(role="RV16 Turnabot 2S 180 mAh", kind="part", match=["battery"], count=1, catalog="lipo_2s_180_turnabot"),
    dict(role="RV13 Malenki nano", kind="part", match=["rxesc"], count=1, catalog="malenki_nano_rvrn2"),
    dict(role="RV14 brushless ESC", kind="part", match=["wesc"], count=1, catalog="bbb_ant_esc_rvrn2"),
    dict(role="RV12 N10 2200 rpm x 2", kind="part", match=["motor_l", "motor_r"], count=2, catalog="n10_2200rpm_spicy"),
    dict(role="drisk stack: 4 x M2 + nuts (not in the STEP, holes are)", match=["bolt_d*"], count=4, designation="M2", threads_into="nut",
         deviation="the STEP leaves the r14 stack holes empty; 4 M2x18 + nuts added so the stack is held (18 mm: the nut is fully engaged)"),
    dict(role="spider to bell: 4 x M2 (not in the STEP)", match=["bolt_p*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the r4.5 holes only"),
    dict(role="stator: 4 x M2 (not in the STEP)", match=["bolt_wm*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the RV03 counterbores only"),
    dict(role="switch: 2 x M2 into the deck pilot holes (not in the STEP)", match=["bolt_sw*"], count=2, designation="M2",
         deviation="the STEP has the two 1.7 pilot holes but no screws"),
    dict(role="weapon lock RV00 (TPU, Build Guide)", kind="part", match=["weapon_lock"], count=1, material="tpu"),
    dict(role="nitrile O-ring belts (not in the STEP; hub grooves are)", kind="part", match=["belt_l", "belt_r"], count=2),
    dict(role="PLA belt guards over the O-ring slots (not in the STEP)", kind="part", match=["belt_guard_*"], count=2),
    dict(role="battery lead: JST RCY", kind="wire", match=["w_bat_sw"], count=1, connector="jst_rcy"),
    dict(role="weapon phases: 3 x 2 mm bullets", kind="wire", match=["w_wesc_m"], count=1, connector="bullet2"),
]

REF_DIR = "/mnt/project-files/robot-cad/research/rvrn_step/parts"
DRISK_T = None


def _drisk_to_world():
    a = math.radians(DR_ROT)
    D = [[math.cos(a), -math.sin(a), 0, -38.5], [math.sin(a), math.cos(a), 0, 23.5], [0, 0, 1, 6.7], [0, 0, 0, 1]]
    import numpy as np
    return (np.array(REF_TO_WORLD, float) @ np.array(D, float)).round(6).tolist()


MICRO_T = {   # STEP Micro_slx_v1_0 instance placements (assembly frame), composed with REF_TO_WORLD
    "l": [[0, -0.33, 0.944, -30.5], [0, 0.944, 0.33, 5.5], [-1, 0, 0, 35.5], [0, 0, 0, 1]],
    "r": [[0, -0.33, -0.944, -30.5], [0, 0.944, -0.33, 5.5], [1, 0, 0, -35.5], [0, 0, 0, 1]],
}


def _micro_to_world(side):
    import numpy as np
    return (np.array(REF_TO_WORLD, float) @ np.array(MICRO_T[side], float)).round(6).tolist()


def _fork_dev(s):
    return [dict(near=[s * 25.5, 66.0, 1.4], r=2.0, reason="laser-cut Ti cannot hold the STEP's knife tip (0.0 mm): the tip ends "
                 "in a 0.45 mm land at full length (laser titanium min web 0.4 mm)")]


def _wedge_dev(s):
    slit = "the STEP draws the Ti fork tine inside the TPU nose (interpenetrating solids); the TPU has the 1.5 mm slit the tine slides into"
    toe = "the STEP ramp ends in a 0 mm knife toe FDM TPU cannot print; the toe stands on a 0.85 mm land at the same reach"
    return ([dict(near=[s * 25.75, y, z], r=2.5, reason=slit) for y, z in ((46.4, 2.2), (44.4, 6.0), (43.1, 6.2), (44.2, 5.9), (48.5, 2.8))]
            + [dict(near=[s * x, 49.3, 1.4], r=4.0, reason=toe) for x in (19.5, 24.0, 28.0, 32.0, 36.5)])


def _side_dev(s):
    return [dict(near=[s * 41.78, SB[0], SB[1]], r=4.0, reason="nose screw seat: ISO 10642 M3 head is 6.6 (catalog max), the STEP's "
                 "6.2 bore would trap it; 6.7 seat with a straight head bore out through the nose for the driver")]


def _GRUB_DEV(s):
    return [{"near": [s * 34.4, RY, RZ + 3.0], "r": 3.5,
             "reason": "grub bore is the catalog M2 tap drill (1.6, robot.cad.holes) 0.2 inboard, not the STEP 2.5 hole at |X| 34.5: "
                       "a 2.5 hole breaks into both 45 deg tyre-seat ramps and leaves knife edges (mfg.thin_wall 0.01 mm); the grub "
                       "threads the 1.6 bore and the captive nut, so it clamps the flat the same"}]


def reference_cad():
    def R(part, file, mode="shape", **k):
        return dict(part=part, file=file, mode=mode, **k)
    dt = _drisk_to_world()
    rows = [
        R("tub", "RV01_Chassis_1.stl", tol_mm=1.0, tol_vol_frac=0.25, note="RV01 chassis",
          deviations=[dict(near=[x, y, 11.0], r=9.0, reason="corner column top: 1.7 thread-forming pilot for the top-panel M2 screw instead of the STEP 3.0 bore (the STEP top panel is bonded; screws make it removable)")
                      for x, y in INS[:4]]
          + [dict(near=[sx * 28.6, -30.6, 4.5], r=4.5, reason="N10 keyhole opened into a U-slot to the floor so the gearbox boss and shaft drop in from below with the base panel off (the STEP closes the keyhole, the shaft cannot be threaded through it)")
             for sx in (1, -1)]
          + [dict(near=[x, y, 5.0], r=4.0, reason="column foot flared to R3.7 with a recess for the base-panel ring boss (1.0 mm base skin cannot seat a 1.2 mm M2 flat head)")
             for x, y in INS]
          + [dict(near=[-10.97, -9.03, 14.13], r=3.0, reason="centroid of one connected extra blob (bbox x -27..-0.4) made of the left cage rib, the left column-foot flares and the left flange gusset, each reasoned above")]
          + [dict(near=list(p_), r=8.0, reason="2 x 2.6 gusset under the front-corner flange: printed deck-down the flange top is an unsupported ceiling")
             for p_ in ((-22.5, 20.0, 5.8), (22.5, 20.0, 5.8))]
          + [dict(near=list(p_), r=6.0, reason="electronics cage ribs hung from the deck (not in the STEP, where kapton alone holds the boards): the Malenki and weapon ESC stay put inverted and under impact")
             for p_ in ((-2.0, -2.0, 15.4), (19.4, -2.0, 15.4), (2.0, -19.6, 13.0), (12.0, -19.6, 13.0), (7.5, -19.6, 13.0), (-2.2, -9.0, 14.0), (19.3, 4.0, 14.0), (-2.2, 4.0, 14.0), (19.3, -9.0, 14.0))]),
        R("base_panel", "RV26_Base_Panel_1.stl", tol_mm=0.3, note="RV26 1 mm panel",
          deviations=[dict(near=[x, y, 4.5], r=3.0, reason="0.4 mm ring boss, R3 edge ears + 4.5 countersink on a 3.4 hole: an ISO 10642 M2 head (4.4 x 1.2) needs 1.6 mm of seat; the STEP's 3.2 x 0.5 seat leaves it proud")
                      for x, y in INS]),
        R("top_panel", "Top_Panel_1.stl", tol_mm=0.3, note="0.9 mm top panel",
          deviations=[dict(near=[x, y, 19.95], r=3.0, reason="4.5 countersink on a 3.5 hole (STEP 3.65 on 2.2) for an ISO M2 flat head, ear R2.7 (STEP 2.5) to keep 0.45 mm of Ti round it")
                      for x, y in INS[:4]]),
        R("mount_l", "RV02_XALT_HD_left_hand_weapon_mount_1.stl", tol_mm=0.5,
          deviations=[{"near": [-17.4, *[round(v, 2) for v in _lock_yz()]], "r": 4.5,
                       "reason": "RV00 weapon-lock pin bore d3.9 through RV02 (Build Guide lock rule; the STEP models no lock)"}]),
        R("mount_r", "RV03_XALT__HD_Right_hand_weapon_mount_1.stl", tol_mm=0.5,
          deviations=[{"near": [16.8, WY + dy, WZ + dz], "r": 2.0,
                       "reason": "STEP 16.4-17.15 lead-in cone under each stator counterbore left out: the d3.5 button head needs a flat seat on the 17.15 floor (fastener_seat.head_bearing)"}
                      for dy, dz in ((6, 0), (-6, 0), (0, 6), (0, -6))]),
        R("motor_spacer", "Motor_back_spacer_1.stl", tol_mm=0.3),
        R("spider", "spider_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("disc_a", "Drisk_floating_3_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("disc_b", "Drisk_floating_3_2.stl", tol_mm=0.5, ref_to_world=dt),
        R("dspacer", "Drisk_spacer_alt_x_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("wedgelet_l", "RV17_Wedgelet_LH_1.stl", tol_mm=0.8, tol_vol_frac=0.25, deviations=_wedge_dev(-1)),
        R("wedgelet_r", "RV18_Wedgelet_RH_1.stl", tol_mm=0.8, tol_vol_frac=0.25, deviations=_wedge_dev(1)),
        R("side_l", "RV23_side_panel_LH_1.stl", tol_mm=1.0, tol_vol_frac=0.25, deviations=_side_dev(-1)),
        R("side_r", "RV24_Mirrorside_panel_RH_1.stl", tol_mm=1.0, tol_vol_frac=0.25, deviations=_side_dev(1)),
        R("fork_l", "fork_5_2.stl", tol_mm=0.5, deviations=_fork_dev(-1)), R("fork_r", "fork_5_1.stl", tol_mm=0.5, deviations=_fork_dev(1)),
        R("whub_rl", "RV21_Rear_Wheel_1.stl", tol_mm=0.5, tol_vol_frac=0.15, deviations=_GRUB_DEV(-1)),
        R("whub_rr", "RV21_Rear_Wheel_2.stl", tol_mm=0.5, tol_vol_frac=0.15, deviations=_GRUB_DEV(1)),
        R("whub_fl", "RV19_Hub_Micro_1.stl", tol_mm=0.5, ref_to_world=_micro_to_world("l")),
        R("whub_fr", "RV19_Hub_Micro_2.stl", tol_mm=0.5, ref_to_world=_micro_to_world("r")),
        R("so_al", "RV11_m3_25mm_aluminium_standoff_1.stl", mode="envelope", tol_mm=0.3, tol_vol_frac=0.2),
        R("so_bl", "RV10_m3_standoff_15mm_1.stl", mode="envelope", tol_mm=0.3, tol_vol_frac=0.2),
        R("wheel_rl", "RV22_Scalextric_F1_Front_tyre_1.stl", mode="envelope", tol_mm=0.3),
        R("wheel_fl", "RV20_11OD_7ID_6W_Micro_slx_1.stl", mode="envelope", tol_mm=0.3, ref_to_world=_micro_to_world("l")),
        R("motor_l", "RV12_N10_2200_RPM_1.stl", mode="envelope", tol_mm=0.6, tol_vol_frac=0.3),
        R("weapon_motor", "GR1507_1.stl", mode="envelope", tol_mm=0.6, tol_vol_frac=0.3),
        R("battery", "RV16_Turnabot_180mah_2s_1.stl", mode="envelope", tol_mm=0.6, tol_vol_frac=0.2),
        R("rxesc", "RV13_Malenki_nano_1.stl", mode="envelope", tol_mm=0.6, tol_vol_frac=0.3),
        R("wesc", "RV14_Brushless_ESC__1.stl", mode="envelope", tol_mm=0.6, tol_vol_frac=0.3),
        R("power_switch", "RV15_BBB_Antweight_Switch_1.stl", mode="envelope", tol_mm=1.0, tol_vol_frac=0.5),
        R("nut_cl", "hex_thin_nut_gradeb_bsi_BS_EN_24036_-_M3_-_N_1.stl", mode="envelope", tol_mm=0.3, tol_vol_frac=0.3),
    ]
    return {"dir": REF_DIR, "ref_to_world": REF_TO_WORLD, "iou_min": 0.9, "placement_tol_mm": 0.5, "parts": rows}


def main():
    spec_dir = os.path.join(HERE, "..")
    out_spec = os.path.join(spec_dir, "spec.json")
    out_tpl = os.path.join(ROOT, "robot/templates/revron.json")
    for out, mf in ((out_spec, "src/build_revron.py"), (out_tpl, "../../robots/revron/src/build_revron.py")):
        body = make_spec(mf)
        spec = dict(name="Revron", profile="aws2025", robot_type="vertical_spinner", locomotion="roller", archetype="vertical_spinner_forks",
                    archetype_params={"blade_lead_mm": [-30, -10], "axle_height_mm": [22, 25], "disc_thickness_mm": [14, 16], "disc_dia_mm": [44, 48], "teeth": [1, 1],
                                      "tub_height_mm": [15, 19], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25],
                                      "disc_floor_gap_mm": [5.0, 9.0]},   # STEP: R16.5 drisk on the 23.5 axle sweeps ~7 mm up; the forks and wedgelets work the floor, not the disc,
                    targets={"length_mm": 107, "width_mm": 104.1, "disc_dia_mm": 46, "wheel_dia_mm": 21.5, "tol_mm": 3,
                             "source": "RVRN 2.0 STEP (research/rvrn_step) measured in its assembly frame",
                             "note": "GR1507 drisk (single tooth, 3+6+3 on a 3 mm spider) on 8 mm XALT mounts; N10 direct to 21.5 rear tyres, O-rings to 11 mm fronts"},
                    weapon_lock={"require_part": True, "note": "RV00 TPU tooth stop (weapon.locking_bar = weapon_lock), fitted whenever the battery is in"},
                    reference_bom=REF_BOM,
                    reference_doc={"path": "REFERENCE.md", "must_mention": ["GR1507", "180 mAh", "Hardox", "JST RCY", "RV00", "XALT", "0.9 mm"],
                                   "must_not_mention": ["through an aluminium spider", "2S ≈350 mAh LiPo"]},
                    electronics=dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2), can_run_inverted=False,
                    allow_overlap=[dict(a="wshaft", b="wbearing", max_depth_mm=0.3, reason="shaft in the MR85 inner race (bearing modelled as one solid)"),
                                   dict(a="wshaft", b="weapon_motor", max_depth_mm=2.6, reason="wshaft is the GR1507's own shaft, already drawn inside the catalog motor envelope"),
                                   dict(a="motor_l", b="whub_rl", max_depth_mm=0.4, reason="the catalog N10 shaft is drawn round; the hub's D-flat sits on its flat"),
                                   dict(a="motor_r", b="whub_rr", max_depth_mm=0.4, reason="the catalog N10 shaft is drawn round; the hub's D-flat sits on its flat"),
                                   *[dict(a=f"insert_b{i}", b="tub", max_depth_mm=0.2, reason="heat-set insert: 3.5 OD melted into a 3.4 bore (interference by design)") for i in range(5)],
                                   *[dict(a=f"nut_c{n}", b="tub", max_depth_mm=0.1, reason="thin M3 nut pressed into a hex pocket 0.05 under its flats (captive)") for n in "lr"],
                                   dict(a="weapon_lock", b="mount_l", max_depth_mm=0.15, reason="RV00 TPU lock pin d4 pressed into the RV02 3.9 bore (0.05 radial grip) so it cannot rattle out"),
                                   dict(a="wbearing", b="mount_l", max_depth_mm=0.1, reason="MR85 8.0 OD pressed into the RV02 7.9 printed seat (0.05 radial interference, the STEP seat size)")],
                    claims=[dict(id="c_mass", text="weighs 150 g or less", metric="mass_total_g", op="<=", value=150),
                            dict(id="c_fit", text="fits the 150 mm square", metric="footprint_mm", op="<=", value=150)],
                    sharp_ok=[dict(part="base_panel", near=[27.9, -21.5, 4.5], r_mm=3.0,
                                   reason="screw boss is 0.3 mm tall (any taller breaks the reference silhouette), so its base fillet is capped at R0.25; the STEP pad base is R0.5")],
                    teardown=TEARDOWN, reference_cad=reference_cad(), **body)
        spec["modules"] = [{"id": "weapon_module", "root": "mount_r", "note": "RVRN quick change: 4 M3 out, both mounts with the drisk lift off the chassis tabs",
                            "parts": [p["id"] for p in spec["parts"] if _root(spec["parts"], p) == "mount_r" and p["id"] != "mount_r"]}]
        json.dump(spec, open(out, "w"), indent=1)
    print("wrote", out_spec, len(spec["parts"]), "parts", len(spec["fasteners"]), "fasteners")


# real service order (Build Guide): side screws out, side panels off, then each wedgelet comes off its standoffs
# outward together with the fork whose tail sits in its cheek slot; then the standoffs slide out of the lugs.
TEARDOWN = [t for s, n in ((-1, "l"), (1, "r")) for t in (
    dict(parts=[f"wedgelet_{n}", f"fork_{n}"], dir=[s, 0, 0], reason="fork tail is pinned in the wedgelet cheek slot: they slide off the standoffs as one"),
    dict(parts=[f"so_b{n}"], dir=[s, 0, 0], reason="nose standoff slides out of the chassis lug once the mount screw is out"),
    dict(parts=[f"so_a{n}"], dir=[s, 0, 0], reason="axle standoff slides out of the lug with the front hub and wheel on it"))] + [
    # weapon module (fix-B): with both standoff pairs out, RV02 slides off the shaft end and its lug (MR85 and lock with it,
    # the two CSK screws captive in it); the spider bolts are then reachable, the drisk slides off the shaft; the motor
    # comes out after its 4 stator screws; RV03 last.
    dict(parts=["mount_l", "bolt_ula", "bolt_ulb"], dir=[-1, 0, 0], reason="RV02 slides outboard off the lug and the shaft end, its CSK screws captive"),
    dict(parts=["spider"], dir=[-1, 0, 0], reason="drisk (spider, discs, spacer, stack bolts) slides off the GR1507 shaft once the 4 bell screws are out"),
    dict(parts=["weapon_motor"], dir=[-1, 0, 0], reason="GR1507 leaves inboard-left once the 4 stator screws are out"),
    dict(parts=["mount_r", "bolt_ura", "bolt_urb"], dir=[1, 0, 0], reason="RV03 slides outboard off its lug with the back spacer, CSK screws captive")]


def _root(parts, q):
    by = {x["id"]: x for x in parts}
    while q.get("parent"):
        q = by[q["parent"]]
    return q["id"]


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    main()
