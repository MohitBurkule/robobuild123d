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
ROOT = "/home/user/robobuild123d"
HERE = os.path.dirname(os.path.abspath(__file__))

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
RY, RZ = -30.5, 11.0                 # N10 shaft (rear axle)
MOTX = 19.6                          # N10 catalog origin |X| (body 3.7..27.5, shaft to 37.5)
# chassis RV01
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


def _csk(d_hole, d_head, at, axis, sign, depth=8.0):
    """Countersink + clearance for a flat head screw whose head is flush at `at` (face point), shank going `sign`
    along `axis`: a 90 deg cone from d_head at the face down to d_hole, the clearance hole, and a head bore outward."""
    b = _b()
    d = [0.0, 0.0, 0.0]
    d[{"x": 0, "y": 1, "z": 2}[axis]] = float(sign)
    h = (d_head - d_hole) / 2
    cone = b.Solid.make_cone(d_head / 2, d_hole / 2, h, b.Plane(origin=at, z_dir=d))
    hole = b.Solid.make_cylinder(d_hole / 2, depth, b.Plane(origin=at, z_dir=d))
    head = b.Solid.make_cylinder(d_head / 2, 3.0, b.Plane(origin=at, z_dir=[-c for c in d]))
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
def base_panel():
    """RV26: 1 mm printed panel under the open chassis, 5 M2 CSK into the floor heat-sets; two 0.25 mm pads under the
    N10 gearboxes preload the motors up into their keyhole pockets."""
    z0, t = 3.5, 1.0
    out = _round(_poly([(-28.1, -36.2), (28.1, -36.2), (28.1, 13.0), (-28.1, 13.0)]), r_out=0.8)
    body = _ext(out, "xy", z0, z0 + t)
    for s in (1, -1):
        pad = _round(_poly([(s * 17.95, -34.85), (s * 27.05, -34.85), (s * 27.05, -25.75), (s * 17.95, -25.75)]), r_out=0.6)
        body = _U(body, _ext(pad, "xy", z0 + t - 0.01, z0 + t + 0.25))
    cuts = [_csk(2.2, 4.0, (x, y, z0), "z", 1, 4.0) for x, y in INS]   # 4.0 countersink (STEP RV26 has 3.2 x 0.5; an ISO 10642 M2 head is 3.8, so it would stand proud and bind) then the 2.2 hole
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
    ears = [Point(x, y).buffer(2.5, 64) for x, y in ((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))]
    blocks = [_poly([(s * 21.0, 8.6), (s * 25.0, 8.6), (s * 25.0, 12.9), (s * 21.0, 12.9)]) for s in (1, -1)] + \
             [_poly([(s * 21.0, -24.1), (s * 25.0, -24.1), (s * 25.0, -19.0), (s * 21.0, -19.0)]) for s in (1, -1)]
    # the ears run into the side edges along concave arcs (STEP): each arc is tangent to the |X| 23 edge and to its ear
    fills = []
    for sx in (1, -1):
        for ey, yt in ((10.4, 1.0), (-21.6, -12.5)):
            d = abs(ey - yt)
            R = (4.0 + d * d - 6.25) / 9.0                       # (2 - R)^2 + d^2 = (R + 2.5)^2
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
    # 2.2 holes countersunk (90 deg, 3.65 at the top face) for M2 flat heads into the column-top pilots (STEP)
    return _S(body, *[_csk(2.2, 4.0, (x, y, z0 + t), "z", -1, 2.0) for x, y in ((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))])


def fork(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = (24.5, 26.0) if s > 0 else (-26.5, -25.0)
    outline = Point(36.3, 6.3).buffer(1.95, 48).union(Polygon([(35.0, 4.9), (36.1, 8.2), (41.0, 8.25), (66.68, 1.49), (51.75, 0.75), (39.0, 0.75), (38.0, 1.5)]))
    outline = _round(outline, r_out=0.3, r_in=0.5).union(Polygon([(60.0, 1.27), (66.68, 1.49), (60.0, 2.5)])).buffer(0.15, 8).buffer(-0.15, 8)   # sharp tip, r0.15 (> kerf) where it joins
    p = outline.difference(Point(SB[0], SB[1]).buffer(2.65, 48)).difference(Point(36.3, 6.3).buffer(0.8, 24))
    p = p.difference(_round(Polygon([(44.2, 2.75), (52.6, 2.85), (44.4, 5.3)]), r_out=0.25))
    if s < 0:   # the STEP hangs the left fork 1.1 deg nose-down about its standoff (pin-hole play in the cheek)
        from shapely import affinity
        p = affinity.rotate(p, -1.1, origin=SB)
    return _ext(p, "yz", x0, x1)


def _mount_profile(r_top):
    """Weapon mount side profile (Y, Z): a teardrop round the weapon axis (R r_top) running down to the standoffs,
    with the notch that drops over the chassis tab (open to the rear)."""
    c = (WY, WZ)
    t0 = _tangent_line_circle((10.17 if r_top > 8 else 9.0, 19.5), c, r_top, upper=True)
    a0 = math.degrees(math.atan2(t0[1] - c[1], t0[0] - c[0]))
    rim = _arc(c, r_top, a0, -14.5 if r_top > 8 else -5.0, 40)
    pts = rim + [(43.6, 3.6)] + _arc(SB, 3.25, -16.0, -90.0, 12)[1:] + [(15.4, 1.25), (13.2, 2.5), (13.2, 4.5), (15.0, 4.5), (15.0, 5.35), (25.6, 5.35), (26.6, 6.35),
                 (26.6, 12.55), (25.6, 13.55), (15.0, 13.55), (15.0, 17.5), (13.0, 19.5), ((10.17 if r_top > 8 else 9.0), 19.5)]
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
    slab = _ext(prof, "yz", xi, xm - s * 0.02)    # slab face 0.02 inside the boss start (no coplanar section face)
    # boss: the part of the profile above the line from the notch top to the nose, battered on its outer face
    line_lo = Polygon([(15.0, 19.5), (44.34, 6.34), (60, 6.34), (60, 60), (0, 60), (0, 19.5)])
    bp = prof.intersection(line_lo)
    boss = _ext(bp, "yz", xm - s * 0.02, xo + s * 0.01)
    # outer battered face (STEP): one plane leaning in with height and towards the nose,
    # |X| = a - kz * Z - ky * Y  (RV02: a 23.48, kz 0.185, ky 0.0168; RV03: 23.88, 0.144, 0.0379)
    a_, kz, ky = (23.88, 0.144, 0.0379) if side == "r" else (23.48, 0.185, 0.0168)
    bb = _b()
    boss = _one(boss).split(bb.Plane(origin=(s * a_, 0.0, 0.0), z_dir=(s * 1.0, ky, kz)), keep=bb.Keep.BOTTOM)
    body = _U(slab, boss)
    cuts = []
    if side == "r":
        cuts.append(_cyl(2.47, -30, 30, (WY, WZ)))                                   # shaft / bearing boss clearance
        bb_ = _b()
        for dy, dz in ((6, 0), (-6, 0), (0, 6), (0, -6)):                           # GR1507 stator M2 on 12 mm (STEP d2.2 clearance)
            cuts.append(_cyl(STAT_HOLE_R, xi - s, xm + s, (WY + dy, WZ + dz)))
            # STEP: d4.5 head counterbore from X 17.15, reached by a cone from the d2.2 hole at X 16.4
            x_c0, x_c1 = s * CB_CONE_X[0], s * CB_CONE_X[1]
            cuts.append(bb_.Solid.make_cone(STAT_HOLE_R, CB_R, abs(x_c1 - x_c0), bb_.Plane(origin=(x_c0, WY + dy, WZ + dz), z_dir=(s, 0, 0))))
            cuts.append(_cyl(CB_R, x_c1, xo + s, (WY + dy, WZ + dz)))
    else:
        cuts.append(_cyl(3.95, -30, 30, (WY, WZ)))                                   # outboard bearing seat (8 mm)
        cuts.append(_cyl(6.0, xm, xo + s, (WY, WZ)))                                 # shaft nut recess
        cuts.append(_cyl(LOCK_R + 0.1, xi - s, xo + 3 * s, _lock_yz()))              # RV00 lock pin bore (0.1 radial slip)
    for (y, z) in (SA, SB):                                                          # M3 CSK into the standoffs, flush inside
        cuts.append(_csk(3.3, 6.2, (xi, y, z), "x", s, 6.0))
    return _S(body, *cuts)


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
    prof = [(0.0, 0.0), (0.0, 8.0), (0.5, 8.0), (0.8, 7.55), (1.7, 7.55), (2.0, 8.0), (2.5, 8.0), (2.55, 6.9), (2.75, 6.35), (3.35, 6.0),
            (5.25, 6.0), (6.25, 7.0), (8.25, 7.0), (9.25, 6.0), (11.29, 6.0), (12.0, 6.5), (12.0, 2.88), (11.8, 2.88), (11.8, 0.0)]   # STEP RV21
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    body = _revolve_x(prof, s * 30.0, (RY, RZ))
    d = Point(RY, RZ).buffer(1.6, 48).intersection(Polygon([(RY - 3, RZ - 3), (RY + 3, RZ - 3), (RY + 3, RZ + 0.9), (RY - 3, RZ + 0.9)]))
    # blind D-bore (flat 0.9 above the axis), an M2 nut slot open at the inner face, the grub hole down to the flat (STEP)
    return _S(body, _ext(d, "yz", s * 29.0, s * 41.0), _box(s * 29.0, s * 41.0, RY - 2.05, RY + 2.05, RZ + 2.4, RZ + 4.4),
              _cyl(1.25, RZ + 0.5, RZ + 9.0, (s * 34.5, RY), "z"))


def front_hub(s):
    """RV19 micro hub (9 x 9) running on the 25 mm standoff: 6 mm tyre seat between two 9 mm flanges, an O-ring
    groove inboard."""
    prof = [(0.0, 2.7), (0.0, 4.5), (0.5, 4.5), (0.56, 3.96), (0.93, 3.7), (1.74, 3.76), (1.94, 3.96), (2.0, 4.5), (2.5, 4.5), (2.5, 4.1), (2.9, 3.7),
            (8.1, 3.7), (8.5, 4.1), (8.5, 4.5), (9.0, 4.5), (9.0, 2.7)]   # STEP RV19
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    return _revolve_x(prof, s * 30.0, SA)


def tyre(od, idd, x0, x1, c):
    return _S(_cyl(od / 2, x0, x1, c), _cyl(idd / 2, x0 - 1, x1 + 1, c))


def standoff(L_x, c):
    return _S(_cyl(SO_R, *L_x, c), _cyl(1.25, L_x[0] - 1, L_x[1] + 1, c))


# ------------------------------------------------------------------------------------------------------------ wedgelet
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
    bb = _b()
    sk = _one(_ext(skin, "yz", -35.5, -29.0)).split(bb.Plane(origin=(-34.0, 41.66, 11.06), z_dir=(-1.24, -0.75, 1.0)), keep=bb.Keep.BOTTOM)
    body = _U(_ext(s1, "yz", -38.5, -36.5), _ext(s2, "yz", -36.5, -35.5), sk, _ext(cheek, "yz", -29.0, -21.5), _ext(tab, "yz", -21.5, -17.5))
    kid = LineString([(36.05, 5.15), (36.95, 7.45)]).buffer(0.95, 24)
    cuts = [_ext(cheek.difference(in_slot), "yz", -27.0, -24.5),                  # 2.5 mm fork slot through the cheek
            _cyl(2.6, -39.0, -17.0, SA), _cyl(1.6, -39.0, -17.0, SB), _cyl(2.5, -36.5, -17.0, SB), _ext(kid, "yz", -29.5, -21.0)]
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # the STEP leaves the fork tine and the mount boss inside the TPU nose; cut their seats (the tine slides into a
    # 1.5 mm slit, the TPU nose tab bears on the mount)
    return _S(sh, fork(s), weapon_mount("l" if s < 0 else "r"))


# ------------------------------------------------------------------------------------------------------------ side panel
SP_IN = [(-43.5, -40.0), (-43.5, -21.3), (-43.0, -19.6), (-41.2, -17.9), (-37.2, -17.2), (-34.4, -15.7), (-32.3, -13.0), (-31.5, -9.9),
         (-31.5, 11.1), (-31.9, 13.4), (-33.6, 17.5), (-35.5, 20.4), (-37.2, 21.9), (-41.2, 23.3), (-42.7, 26.6)]
SP_IN_BOT = SP_IN[:9] + [(-31.9, 12.2), (-35.5, 15.6), (-41.8, 17.0), (-44.9, 18.7), (-47.4, 21.8), (-48.6, 25.6), (-48.6, 26.6)]   # the swing leans: its foot sits 4 mm further out and back   # inner face (Y, |X|) path


def side_panel(s):
    """RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon
    b = _b()
    K, z0, z1 = 10, 1.0, 16.0    # the battered, leaning wall as K stacked layers (path and width interpolated floor -> top)
    layers = []
    for i in range(K):
        t = (i + 0.5) / K
        tp = min(1.0, 2.5 * t)   # the swing's lean is all in its foot
        path = _chaikin_open([(xb + (xt - xb) * tp, yb + (yt - yb) * tp) for (xb, yb), (xt, yt) in zip(SP_IN_BOT, SP_IN)], 2)
        band = _band(path, 5.0 + (2.0 - 5.0) * t)
        layers.append(_ext(band, "xy", z0 + (z1 - z0) * i / K, z0 + (z1 - z0) * (i + 1) / K + 0.01))
    wall = _U(*layers)
    side = _round(Polygon([(-32.9, 1.0), (-32.9, 16.0), (-4.3, 16.0), (17.0, 12.0), (25.0, 10.0), (42.0, 10.0), (50.1, 1.0)]), r_out=1.5)
    side = side.union(Point(-32.9, 8.5).buffer(7.5, 64))                           # rear end a full round over the wheel
    foot = _ext(_poly([(-31.6, -12.0), (-42.0, -11.9), (-40.6, -2.1), (-40.8, 3.3), (-42.9, 13.3), (-31.6, 13.3)]), "xy", 1.0, 2.6)   # wide foot under the chassis lobe
    wall = _I(wall, _ext(side, "yz", -60.0, -20.0))
    nose_plan = _round(Polygon([(-51.6, 26.5), (-51.2, 39.7), (-50.0, 43.0), (-47.9, 45.7), (-45.1, 47.9), (-41.7, 49.3), (-38.5, 49.7),
                                (-38.5, 38.7), (-41.6, 38.7), (-42.4, 37.3), (-42.3, 34.9), (-40.5, 34.5), (-40.5, 26.5)]), r_out=0.5)
    batter = _ext(_poly([(-51.6, 1.0), (-51.6 + 0.79 * 15, 16.0), (0.0, 16.0), (0.0, 1.0), (-51.6, -5.0)]), "xz", 0.0, 60.0)   # outer face leans in 38 deg
    nose = _I(_I(_ext(nose_plan, "xy", 1.0, 10.0), _ext(side, "yz", -60.0, -20.0)), batter)
    wall = _S(wall, _box(-60.0, -30.0, 12.5, 60.0, 10.0, 20.0))                    # above the front wheel the wall runs straight on
    straight = _I(_box(-34.0, -31.5, 9.0, 17.2, 1.0, 16.0), _ext(side, "yz", -60.0, -20.0))
    nose = _S(nose, _box(-42.0, -38.4, 26.5, 39.0, 3.0, 10.5))                     # hollow behind the nose wall
    boss = _I(_cyl(3.0, -42.5, -39.5, SA), _ext(side, "yz", -60.0, -20.0))         # standoff end boss
    body = _U(wall, nose, foot, straight, boss)
    cuts = [_csk(3.3, 6.2, (-46.26, SA[0], SA[1]), "x", 1, 8.0), _csk(3.3, 6.6, (-41.76, SB[0], SB[1]), "x", 1, 8.0), _cyl(3.1, -50.0, -41.5, SB),
            _csk(3.3, 6.2, (-35.26, NUT[0], NUT[1]), "x", 1, 8.0), _cyl(2.55, -42.55, -38.0, SA),
            _box(-45.0, -43.4, -38.7, -24.8, 5.0, 15.0),                          # rear tyre relief on the inner face
            _box(-32.6, -31.4, -13.1, 2.6, 3.7, 13.3)]                            # clears the chassis nut lobe
    for y0 in (-11.0, -4.5, 2.0):     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, 5.0), (y0 + 5.0, 11.0)]).buffer(1.0, cap_style=1)
        cuts.append(_ext(sl, "yz", -50.0, -36.5))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # belt channel on the inner face: the O-ring runs inside the panel, covered from outside (W8)
    from shapely.geometry import Point
    band = Point(RY, RZ).buffer(7.5 + 1.25, 64).union(Point(*SA).buffer(3.7 + 1.25, 48)).convex_hull
    return _S(sh, _ext(band, "yz", *sorted((s * 30.5, s * 32.0))))


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
        # side lobe with the thin M3 nut (Y -16.3..2.8)
        lobe = Point(NUT[0], NUT[1]).buffer(4.55, 64).union(Point(1.35, 6.9).buffer(1.2, 32)).convex_hull
        add.append(_ext(lobe, "yz", sg * (x - 0.1), sg * 32.5))
        add.append(_loft_yz(lobe.buffer(1.2, join_style=1), sg * (x - 0.1), lobe, sg * (x + 1.2)))   # R1.2 root fillet (as a 45 deg blend)
        # front tabs (key into the weapon-mount notches) and inner tab walls
        add.append(_ext(_poly([(18.5, 6.4), (19.5, 5.4), (25.5, 5.4), (26.5, 6.4), (26.5, 12.5), (25.5, 13.5), (19.5, 13.5), (18.5, 12.5)]), "yz", sg * 13.2, sg * 17.6))
        add.append(_ext(_poly([(13.0, 2.5), (25.5, 2.5), (26.5, 3.5), (26.5, 12.35), (25.59, 14.75), (15.0, 19.5), (13.0, 19.5)]), "yz", sg * 10.3, sg * 13.3))
        fil = Polygon([(8.3, 14.9), (10.4, 14.9), (10.4, 17.0), (8.3, 17.0)]).difference(Point(8.3, 17.0).buffer(2.0, 48))   # R2 into the front face
        add.append(_ext(Polygon([(sg * u, v) for u, v in fil.exterior.coords]).buffer(0), "xy", z0, c["deck"]))
        # switch pad under the deck (STEP): the switch ears bear on it
        if sg > 0:
            add.append(_ext(_round(Polygon([(22.5, -15.6), (27.5, -15.6), (27.5, 4.4), (22.5, 4.4)]), r_out=1.0), "xy", 16.5, c["deck"] + 0.1))
        # lugs carrying the standoffs (sloped top so they sit under the mount)
        lug = Polygon([(13.0, z0), (26.0, z0), (30.4, 1.0)] + _arc(SA, 4.5, 250, 300, 6) + [(36.6, 2.5)] + _arc(SB, 3.2, 250, 400, 16) + [(15.0, z1), (13.0, z1)])
        lug = _round(lug.convex_hull.difference(Polygon([(26.0, 0.0), (26.0, 2.5), (30.0, 1.0), (40.0, 1.3), (60, 0)])), r_in=0.0)
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
        topf = _ext(_poly([(13.0, 19.5), (15.3, 19.5), (23.0, 15.83), (23.0, 13.47), (15.3, 16.4), (13.0, 16.4)]), "yz", sg * 21.4, sg * 29.5)
        add.append(_I(topf, _ext(Polygon([(sg * x_, y_) for x_, y_ in Polygon([(21.4, 13.0), (29.5, 13.0)] + blend + [(21.4, 27.5)]).buffer(0).exterior.coords]).buffer(0), "xy", 10.0, 20.0)))
    body = _U(body, *add)
    cuts = []
    for sg in (1, -1):
        # lug underside: flat to Y 26, then the ramp; a scallop between the two standoffs (STEP)
        cuts.append(_ext(_poly([(10.0, -5.0), (10.0, 2.5), (26.0, 2.5), (30.4, 1.0), (30.4, -5.0)]), "yz", sg * 17.4, sg * 21.6))
        cuts.append(_ext(Point(36.34, -1.67).buffer(4.12, 64), "yz", sg * 17.4, sg * 21.6))
        cuts.append(_box(sg * 13.3, sg * 17.5, 12.0, 15.1, z0 - 0.1, 4.5))   # front wall stops at the rabbet under the tab (STEP)
        # motor stop wall: lower inner edge rounded R4.5 (STEP)
        fil = Polygon([(17.6, 4.4), (22.2, 4.4), (22.2, 9.0), (17.6, 9.0)]).difference(Point(22.2, 9.0).buffer(4.5, 64))
        cuts.append(_ext(Polygon([(sg * x_, z_) for x_, z_ in fil.exterior.coords]).buffer(0), "xz", -25.5, -23.3))
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
        side = Polygon([(sg * 3.72, -5.59), (sg * 22.5, 4.51 + 0.640 * 2.99), (sg * 22.5, -15.71 - 0.6407 * 2.99)])
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
        else:   # corner columns: a 1.7 thread-forming pilot in the top 4 mm for the top-panel screw (deviation: STEP 3.0 through)
            cuts.append(_cyl(0.85, z1 - 4.1, z1 + 1, (px, py), "z"))
    # switch slot in the deck beside the top panel, 2 M2 pilot holes
    cuts.append(_ext(_round(Polygon([(23.0, -11.6), (27.0, -11.6), (27.0, 0.4), (23.0, 0.4)]), r_out=0.45), "xy", 16.0, z1 + 1))
    for yy in (1.9, -13.1):
        cuts.append(_cyl(0.85, c["deck"] - 3, z1 + 1, (25.0, yy), "z"))
    for sg in (1, -1):
        # N10 keyhole: round seat for the gearbox shaft boss, narrowing to the floor (motor tilts in)
        kh = Point(RY, RZ).buffer(2.5, 64).union(Point(RY, 5.85).buffer(0.85, 24)).convex_hull   # STEP keyhole
        cuts.append(_ext(kh, "yz", sg * (x - w - 0.5), sg * (x + 0.5)))
        # nut: M3 clearance through lobe + wall, hex pocket on the inside
        cuts.append(_cyl(1.6, sg * 26.0, sg * 33.0, NUT))
        hexp = Polygon([(NUT[0] + 3.29 * math.cos(math.radians(60 * i + 30)), NUT[1] + 3.2 * math.sin(math.radians(60 * i + 30))) for i in range(6)])
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
        cuts.append(_ext(_round(t.buffer(0), r_out=0.45), "xz", -36.6, -35.5))
    # weapon phase wire hole in the front wall
    cuts.append(_ext(_round(Polygon([(7.25, 5.0), (10.25, 5.0), (10.25, 17.0), (7.25, 17.0)]), r_out=1.45), "xz", 12.0, 16.0))
    for xa, xb in ((-18.25, 4.25), (13.25, 18.2)):
        cuts.append(_ext(_round(Polygon([(xa, 6.55), (xb, 6.55), (xb, 15.55), (xa, 15.55)]), r_out=0.5), "xz", 12.0, 13.85))
    # rabbet for the base panel (recessed flush with the wall bottom lip) and the mating faces of the mounts and side
    # panels: the parts seat on the chassis, they do not share material with it
    pan = _round(_poly([(-28.15, -36.25), (28.15, -36.25), (28.15, 13.05), (-28.15, 13.05)]), r_out=0.8)
    cuts.append(_ext(pan, "xy", z0 - 1.0, 4.5))
    for sg in (1, -1):
        cuts.append(_box(sg * 17.95, sg * 27.05, -34.85, -25.75, 4.4, 4.8))   # motor preload pads
    cuts += [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)]
    return _S(body, *cuts)


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
    tipc = b.Solid.make_cone(LOCK_R - 0.5, LOCK_R, 0.5, b.Plane(origin=(0, 0, -0.5), z_dir=(0, 0, 1)))   # lead-in chamfer
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
    "rear_tyre_l": lambda: tyre(21.5, 14.0, -42.0, -32.5, (RY, RZ)), "rear_tyre_r": lambda: tyre(21.5, 14.0, 32.5, 42.0, (RY, RZ)),
    "front_tyre_l": lambda: tyre(11.0, 7.0, -38.5, -32.5, SA), "front_tyre_r": lambda: tyre(11.0, 7.0, 32.5, 38.5, SA),
    "so_a_l": lambda: standoff((-SA_X[1], -SA_X[0]), SA), "so_a_r": lambda: standoff(SA_X, SA),
    "so_b_l": lambda: standoff((-SB_X[1], -SB_X[0]), SB), "so_b_r": lambda: standoff(SB_X, SB),
    "weapon_lock": weapon_lock,
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
      label="RV26 1 mm printed base panel, 5 M2 CSK into the floor heat-sets, 0.25 mm pads preload the N10s")
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
    P(id="wshaft", kind="shaft", material="steel", process="cots", stock="GR1507 5 mm shaft (part of the motor)", rotates_with="weapon", shaft_of="weapon_motor", parent="spider",
      shape={"type": "place", "shape": {"type": "cylinder", "radius": 2.5, "height": 12.2}, "at": [-12.6, 0, 0], "rot": [0, 90, 0]}, color="#777777", solid_fraction=0.05,
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
          shape=M(f"wedgelet_{n}"), label=f"RV1{7 if s < 0 else 8} TPU wedgelet: 50 deg ramp over the nose, cheeks round both standoffs and the fork tail")
        P(id=f"side_{n}", kind="armor", material="tpu", process="fdm", solid_fraction=0.9, print_orientation="+z", parent=f"so_a{n}", rotates_with="fixed", color="#3c4048", shape=M(f"side_panel_{n}"),
          label=f"RV2{3 if s < 0 else 4} TPU side panel: battered S-wall round the wheels, 3 M3x8 CSK (two standoff ends, one chassis nut)")
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
    P(id="power_switch", kind="switch", catalog="switch_bbb_ant_rvrn2", at=[25.0, -5.6, 14.25], rot=[0, 0, 90], retained="screws", marked=True, tool_free=True,
      off_dir=[0, -1, 0], label="BBB ant switch hung under the deck beside the top panel: lever flush in the deck slot, 2 M2 into the deck")
    for i, (x, y) in enumerate(INS):
        P(id=f"insert_b{i}", kind="insert", catalog="heatset_m2_4", at=[x, y, (INS_Z[0] + INS_Z[1]) / 2])
    for k in range(4):
        dy, dz = _disc_local(BOLT_R * math.cos(math.radians(90 * k)), BOLT_R * math.sin(math.radians(90 * k)))
        P(id=f"nut_d{k}", kind="nut", catalog="nut_m2", at=[DR_X["disc_b"][1] + 0.8, dy - WY, dz - WZ], rot=[0, 90, 0], rotates_with="weapon", parent="spider")
    ly, lz = _lock_yz()
    P(id="weapon_lock", kind="locking_bar", role="weapon_lock", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#ff6a00", tethered=True,
      parent="mount_l", at=[LOCK_TIP_X, ly, lz], rot=[0, 90, 0],
      marked=True, tool_free=True, shape=M("weapon_lock"), label="RV00 TPU weapon lock pin (Build Guide rule; not in the STEP): d4 pin pushed through RV02 into a spider window, flag head + lanyard outside")

    # ---------------------------------------------------------------- fasteners
    for i, (x, y) in enumerate(INS):
        F(id=f"bolt_b{i}", designation="M2x6", material="aluminium", at=[x, y, 3.5], dir=[0, 0, 1], through=["base_panel", "tub"], threads_into=f"insert_b{i}", tool="hex1.3")
    for s, n in SIDES:
        mnt = f"mount_{n}"
        F(id=f"bolt_u{n}a", designation="M3x12", material="aluminium", at=[s * MNT_IN, SA[0], SA[1]], dir=[s, 0, 0], through=[mnt], threads_into=f"so_a{n}",
          reason="FS9 M3x12 CSK alu, head flush in the mount's inner face")
        F(id=f"bolt_u{n}b", designation="M3x14", reason="M3x14 CSK alu (STEP FS9 M3x12): through mount and lug, 12 mm bites only 3.9 mm of the 15 mm standoff", material="aluminium", at=[s * MNT_IN, SB[0], SB[1]], dir=[s, 0, 0], through=[mnt, "tub"], threads_into=f"so_b{n}",
          )
        F(id=f"bolt_s{n}a", designation="M3x10", material="aluminium", reason="M3x10 CSK (STEP: M3x8): 8 mm bites only 4.2 mm of the standoff thread; 10 mm gives 6.2 (>= 1.5 d in aluminium)", at=[s * 46.26, SA[0], SA[1]], dir=[-s, 0, 0], through=[f"side_{n}"], threads_into=f"so_a{n}")
        F(id=f"bolt_s{n}b", designation="M3x10", material="aluminium", reason="M3x10 CSK (STEP: M3x8): the head sits 5.3 mm out from the 15 mm standoff end, so 8 mm bites 2.7 mm; 10 mm bites 4.7", at=[s * 41.76, SB[0], SB[1]], dir=[-s, 0, 0], through=[f"side_{n}"], threads_into=f"so_b{n}")
        F(id=f"bolt_s{n}c", designation="M3x8", material="aluminium", reason="alu M3 CSK (Build Guide: aluminium bolts for weight; the STEP draws stainless)", at=[s * 35.26, NUT[0], NUT[1]], dir=[-s, 0, 0], through=[f"side_{n}", "tub"], threads_into=f"nut_c{n}")
    for k, (dy, dz) in enumerate(((6, 0), (-6, 0), (0, 6), (0, -6))):
        F(id=f"bolt_wm{k}", designation="M2x8", head="button", tool="hex1.3", material="titanium", at=[MNT_SLAB, WY + dy, WZ + dz], dir=[-1, 0, 0], through=["mount_r", "motor_spacer"],
          threads_into="weapon_motor", reason="button heads (one hex1.3 key for every M2) sunk in the RV03 boss counterbores (inferred: the STEP shows the 4.4 counterbores, not the screws)")
    for k in range(4):
        a = math.radians(90 * k)
        dy, dz = _disc_local(HUB_R * math.cos(a), HUB_R * math.sin(a))
        F(id=f"bolt_p{k}", designation="M2x4", head="button", tool="hex1.3", material="titanium", at=[DR_X["spider"][0], dy, dz], dir=[1, 0, 0], through=["spider"], threads_into="weapon_motor",
          access_before=["mount_l", "wbearing"], reason="spider to bell, fitted before the left mount goes on (inferred)")
        dy, dz = _disc_local(BOLT_R * math.cos(a), BOLT_R * math.sin(a))
        F(id=f"bolt_d{k}", designation="M2x18", head="button", tool="hex1.3", material="titanium", at=[DR_X["spider"][0], dy, dz], dir=[1, 0, 0],
          through=["spider", "disc_a", "dspacer", "disc_b"], threads_into=f"nut_d{k}",
          access_before=["mount_l", "wbearing", "weapon_motor", "mount_r", "motor_spacer", "tub", "so_al", "so_bl", "so_ar", "so_br"],
          reason="stack bolted up on the bench before it goes on the motor (inferred: the STEP has the 2.2 holes but no screws)")
    for i, (x, y) in enumerate(((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))):
        F(id=f"bolt_t{i}", designation="M2x4", head="countersunk", tool="hex1.3", at=[x, y, 20.4], dir=[0, 0, -1], through=["top_panel"], threads_into="tub",
          reason="M2 flat head in the panel's 90 deg countersink, thread-forming into the 1.7 column-top pilot (inferred: the STEP top panel has the countersunk 2.2 holes but no screws)")
    for i, yy in enumerate((1.9, -13.1)):
        F(id=f"bolt_sw{i}", designation="M2x3", head="button", tool="hex1.3", at=[25.0, yy, 16.0], dir=[0, 0, 1], through=["power_switch"], threads_into="tub",
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
    C("weapon_lock", "mount_l", "pin", "TPU lock pin slides in the RV02 4.2 bore (0.1 slip) into a spider window; the head stops it, the lanyard tethers it to the mount", mechanical_key=True)
    C("battery", "tub", "press_fit", "Pack between the motor wall, the insert columns and the deck", interference_mm=0.1, mechanical_key=True)
    C("rxesc", "tub", "interlock", "Malenki under the deck beside the pack, kapton")
    C("wesc", "rxesc", "interlock", "ESC kapton-wrapped against the Malenki; both boxed in by the walls, the deck and the base panel")
    C("wesc", "tub", "interlock", "ESC boxed by the walls, the deck and the base panel")
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
        P(id=f"belt_{n}", kind="belt", material="rubber", process="cots", shape=belt_shape(s), color="#111111",
          belt={"pulleys": [f"whub_r{n}", f"whub_f{n}"], "kind": "o_ring", "length_mm": BELT_L, "width_mm": ORING[1], "stock": {"id_mm": ORING[0], "cs_mm": ORING[1]}},
          label=f"stock {ORING[0]} x {ORING[1]} nitrile O-ring ({100 * (loop / BELT_L - 1):.0f} % stretch on the 61 mm centres): front wheel drive (not in the STEP; the hub grooves are)")

    wires = [dict(_Wr("w_bat_sw", "battery.jst_rcy", "power_switch.in", 24, "power", 8), connector="jst_rcy"), _Wr("w_sw_wesc", "power_switch.out", "wesc.bat", 24, "power", 8),
             _Wr("w_sw_rx", "power_switch.out", "rxesc.bat", 26, "power", 8), dict(_Wr("w_wesc_m", "wesc.motor", "weapon_motor.phases", 24, "motor", 15), connector="bullet2", count=3),
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
    A("min_wall", "2 mm walls are 4+ perimeters: the box takes wheel-side and clamp loads without delaminating", part="tub", min=1.8, envelope=True)
    A("insert_column", "printed deck-down, each heat-set insert sits on a solid column back to the deck (the first layers): no hanging boss to pull out",
      part="tub", inserts=[[x, y, CH["deck"]] for x, y in INS], floor_z=INS_Z[0], r=2.2)
    x, w = CH["x"], CH["wall"]
    A("fillet", "inside wall corners are radiused: sharp PLA inside corners crack under impact", part="tub", axis="z", h=10.0,
      at=[[-x + w, CH["y0"] + w], [x - w, CH["y0"] + w], [x - w, CH["y1"] - w], [-x + w, CH["y1"] - w]])
    A("tool_count", "pit kit: one hex key per screw size (1.3 for M2, 2 for M3); the weapon swap needs only the 2 mm key", max=2, module_max=1,
      module=["bolt_ula", "bolt_ulb", "bolt_ura", "bolt_urb"])
    rot = ["spider", "disc_a", "disc_b", "dspacer"] + [f"nut_d{k}" for k in range(4)]
    A("wire_clear_rotor", "phases and power leads stay out of the drisk's swept volume", rotor=rot, axis=[1, 0, 0], at=[0, WY, WZ], min=2.0,
      via={"w_wesc_m": [[6.5, 14.5, 16.0], [11.5, 14.5, 16.0]]})
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
    dict(role="top panel: 4 x M2 CSK thread-forming (not in the STEP; its countersunk holes are)", match=["bolt_t*"], count=4, designation="M2x4", threads_into="tub",
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
    dict(role="RV12 N10 2200 rpm x 2", kind="part", match=["motor_*"], count=2, catalog="n10_2200rpm_spicy"),
    dict(role="drisk stack: 4 x M2 + nuts (not in the STEP, holes are)", match=["bolt_d*"], count=4, designation="M2", threads_into="nut",
         deviation="the STEP leaves the r14 stack holes empty; 4 M2x18 + nuts added so the stack is held (18 mm: the nut is fully engaged)"),
    dict(role="spider to bell: 4 x M2 (not in the STEP)", match=["bolt_p*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the r4.5 holes only"),
    dict(role="stator: 4 x M2 (not in the STEP)", match=["bolt_wm*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the RV03 counterbores only"),
    dict(role="switch: 2 x M2 into the deck pilot holes (not in the STEP)", match=["bolt_sw*"], count=2, designation="M2",
         deviation="the STEP has the two 1.7 pilot holes but no screws"),
    dict(role="weapon lock RV00 (TPU, Build Guide)", kind="part", match=["weapon_lock"], count=1, material="tpu"),
    dict(role="nitrile O-ring belts (not in the STEP; hub grooves are)", kind="part", match=["belt_*"], count=2),
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


def reference_cad():
    def R(part, file, mode="shape", **k):
        return dict(part=part, file=file, mode=mode, **k)
    dt = _drisk_to_world()
    rows = [
        R("tub", "RV01_Chassis_1.stl", tol_mm=1.0, tol_vol_frac=0.25, note="RV01 chassis"),
        R("base_panel", "RV26_Base_Panel_1.stl", tol_mm=0.3, note="RV26 1 mm panel"),
        R("top_panel", "Top_Panel_1.stl", tol_mm=0.3, note="0.9 mm top panel"),
        R("mount_l", "RV02_XALT_HD_left_hand_weapon_mount_1.stl", tol_mm=0.5,
          deviations=[{"near": [-17.4, *[round(v, 2) for v in _lock_yz()]], "r": 4.5,
                       "reason": "RV00 weapon-lock pin bore d4.2 through RV02 (Build Guide lock rule; the STEP models no lock)"}]),
        R("mount_r", "RV03_XALT__HD_Right_hand_weapon_mount_1.stl", tol_mm=0.5),
        R("motor_spacer", "Motor_back_spacer_1.stl", tol_mm=0.3),
        R("spider", "spider_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("disc_a", "Drisk_floating_3_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("disc_b", "Drisk_floating_3_2.stl", tol_mm=0.5, ref_to_world=dt),
        R("dspacer", "Drisk_spacer_alt_x_1.stl", tol_mm=0.5, ref_to_world=dt),
        R("wedgelet_l", "RV17_Wedgelet_LH_1.stl", tol_mm=0.8, tol_vol_frac=0.25),
        R("wedgelet_r", "RV18_Wedgelet_RH_1.stl", tol_mm=0.8, tol_vol_frac=0.25),
        R("side_l", "RV23_side_panel_LH_1.stl", tol_mm=1.0, tol_vol_frac=0.25),
        R("side_r", "RV24_Mirrorside_panel_RH_1.stl", tol_mm=1.0, tol_vol_frac=0.25),
        R("fork_l", "fork_5_2.stl", tol_mm=0.5), R("fork_r", "fork_5_1.stl", tol_mm=0.5),
        R("whub_rl", "RV21_Rear_Wheel_1.stl", tol_mm=0.5, tol_vol_frac=0.15), R("whub_rr", "RV21_Rear_Wheel_2.stl", tol_mm=0.5, tol_vol_frac=0.15),
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
                                      "tub_height_mm": [15, 19], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25]},
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
                                   dict(a="wbearing", b="mount_l", max_depth_mm=0.1, reason="MR85 8.0 OD pressed into the RV02 7.9 printed seat (0.05 radial interference, the STEP seat size)")],
                    claims=[dict(id="c_mass", text="weighs 150 g or less", metric="mass_total_g", op="<=", value=150),
                            dict(id="c_fit", text="fits the 150 mm square", metric="footprint_mm", op="<=", value=150)],
                    reference_cad=reference_cad(), **body)
        spec["modules"] = [{"id": "weapon_module", "root": "mount_r", "note": "RVRN quick change: 4 M3 out, both mounts with the drisk lift off the chassis tabs",
                            "parts": [p["id"] for p in spec["parts"] if _root(spec["parts"], p) == "mount_r" and p["id"] != "mount_r"]}]
        json.dump(spec, open(out, "w"), indent=1)
    print("wrote", out_spec, len(spec["parts"]), "parts", len(spec["fasteners"]), "fasteners")


def _root(parts, q):
    by = {x["id"]: x for x in parts}
    while q.get("parent"):
        q = by[q["parent"]]
    return q["id"]


if __name__ == "__main__":
    sys.path.insert(0, ROOT)
    main()
