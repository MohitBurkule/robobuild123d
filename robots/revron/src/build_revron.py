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
    cuts = [_csk(2.1, 3.1, (x, y, z0), "z", 1, 4.0) for x, y in INS]
    return _S(body, *cuts)


def top_panel():
    """0.9 mm Ti top panel (no holes: bonded on the deck with VHB). Four corner ears cover the insert columns; the
    front notches clear the weapon-mount tabs; it stops at |X| 23 beside the switch so the switch stays reachable."""
    z0, t = 19.5, 0.9
    core = _poly([(-23.0, -24.1), (23.0, -24.1), (23.0, 7.9), (21.0, 7.9), (21.0, 12.9), (-21.0, 12.9), (-21.0, 7.9), (-23.0, 7.9)])
    tab = _poly([(-13.0, 7.0), (13.0, 7.0), (13.0, 11.9), (-13.0, 11.9)])
    notch = [_poly([(s * 13.0, 7.9), (s * 21.0, 7.9), (s * 21.0, 13.5), (s * 13.0, 13.5)]) for s in (1, -1)]
    from shapely.geometry import Point
    ears = [Point(x, y).buffer(2.5, 64) for x, y in ((25.0, 10.4), (-25.0, 10.4), (25.0, -21.6), (-25.0, -21.6))]
    blocks = [_poly([(s * 21.0, 8.6), (s * 25.0, 8.6), (s * 25.0, 12.9), (s * 21.0, 12.9)]) for s in (1, -1)] + \
             [_poly([(s * 21.0, -24.1), (s * 25.0, -24.1), (s * 25.0, -19.0), (s * 21.0, -19.0)]) for s in (1, -1)]
    p = core
    for q in ears + blocks:
        p = p.union(q)
    for q in notch:
        p = p.difference(q)
    p = p.union(tab)
    p = _round(p, r_out=0.4, r_in=1.2)
    return _ext(p, "xy", z0, z0 + t)


def fork(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = (24.5, 26.0) if s > 0 else (-26.5, -25.0)
    outline = Point(36.3, 6.3).buffer(1.95, 48).union(Polygon([(35.0, 4.9), (36.1, 8.2), (41.0, 8.25), (66.68, 1.49), (51.75, 0.75), (40.5, 0.75), (38.3, 1.5)]))
    outline = _round(outline, r_out=0.3, r_in=0.5)
    p = outline.difference(Point(SB[0], SB[1]).buffer(2.65, 48)).difference(Point(36.3, 6.3).buffer(0.8, 24))
    p = p.difference(_round(Polygon([(44.2, 2.0), (52.3, 2.0), (44.2, 5.3)]), r_out=0.4))
    return _ext(p, "yz", x0, x1)


def _mount_profile(r_top):
    """Weapon mount side profile (Y, Z): a teardrop round the weapon axis (R r_top) running down to the standoffs,
    with the notch that drops over the chassis tab (open to the rear)."""
    c = (WY, WZ)
    t0 = _tangent_line_circle((10.17 if r_top > 8 else 9.0, 19.5), c, r_top, upper=True)
    a0 = math.degrees(math.atan2(t0[1] - c[1], t0[0] - c[0]))
    rim = _arc(c, r_top, a0, -14.5 if r_top > 8 else -5.0, 40)
    pts = rim + [(43.6, 3.6), (40.5, 1.25), (15.4, 1.25), (13.2, 2.5), (13.2, 4.5), (15.0, 4.5), (15.0, 5.35), (25.6, 5.35), (26.6, 6.35),
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
    slab = _ext(prof, "yz", xi, xm)
    # boss: the part of the profile above the line from the notch top to the nose, battered on its outer face
    line_lo = Polygon([(15.0, 19.5), (44.34, 6.34), (60, 6.34), (60, 60), (0, 60), (0, 19.5)])
    bp = prof.intersection(line_lo)
    boss = _ext(bp, "yz", xm, xo + s * 0.01)
    k = math.tan(math.radians(7.7))
    # outer battered face: |X| <= MNT_OUT - k * (Z - 8.5)  (a half-space as a big prism in the XZ plane)
    xz = [(0.0, -10.0), (MNT_OUT + 18.5 * k, -10.0), (MNT_OUT - 40 * k, 48.5), (0.0, 48.5)]
    if s < 0:
        xz = [(-x, z) for x, z in xz]
    half = _ext(_poly(xz), "xz", 0.0, 70.0)
    boss = _I(boss, half)
    body = _U(slab, boss)
    cuts = []
    if side == "r":
        cuts.append(_cyl(2.47, -30, 30, (WY, WZ)))                                   # shaft / bearing boss clearance
        for dy, dz in ((6, 0), (-6, 0), (0, 6), (0, -6)):                           # GR1507 stator M2 on 12 mm
            cuts.append(_cyl(1.05, xi - s, xm + s, (WY + dy, WZ + dz)))
            cuts.append(_cyl(2.22, xm - s * 0.01, xo + s, (WY + dy, WZ + dz)))      # head counterbores in the boss
    else:
        cuts.append(_cyl(3.95, -30, 30, (WY, WZ)))                                   # outboard bearing seat (8 mm)
        cuts.append(_cyl(6.0, xm, xo + s, (WY, WZ)))                                 # shaft nut recess
    for (y, z) in (SA, SB):                                                          # M3 CSK into the standoffs, flush inside
        cuts.append(_csk(3.3, 6.2, (xi, y, z), "x", s, 6.0))
    return _S(body, *cuts)


def motor_back_spacer():
    """1.5 mm printed spacer between the GR1507 stator base and RV03: clears the motor's rear bearing boss and wires."""
    from shapely.geometry import Point
    p = Point(WY, WZ).buffer(10.0, 64).difference(Point(WY, WZ).buffer(3.95, 48))
    for k in range(4):
        a = math.radians(45 + 90 * k)
        p = p.difference(Point(WY + 6.9 * math.cos(a), WZ + 6.9 * math.sin(a)).buffer(2.25, 32))
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
    return _round(rim.union(tooth), r_out=0.0, r_in=0.7)


def floating_disc():
    from shapely.geometry import Point, Polygon
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
    p = p.difference(_round(Polygon([(-13.45, 4.65), (-13.45, 9.4), (-11.3, 7.7)]), r_out=0.45))   # balance window by the tooth
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
    prof = [(0.0, 1.6), (0.0, 8.0), (0.6, 8.0), (0.8, 7.55), (1.5, 7.55), (1.7, 8.0), (2.3, 8.0), (3.3, 6.0), (6.3, 6.0), (7.0, 7.0),
            (8.6, 7.0), (9.3, 6.0), (11.5, 6.0), (12.0, 6.5), (12.0, 0.0), (11.2, 0.0), (11.2, 1.6)]
    prof = [(0.0, 0.0)] + prof[1:-3] + [(12.0, 6.5), (12.0, 0.0)]
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    body = _revolve_x(prof, s * 30.0, (RY, RZ))
    d = Point(RY, RZ).buffer(1.55, 48).intersection(Polygon([(RY - 3, RZ - 3), (RY + 3, RZ - 3), (RY + 3, RZ + 1.2), (RY - 3, RZ + 1.2)]))
    return _S(body, _ext(d, "yz", s * 29.0, s * 41.2), _box(s * 35.8, s * 41.0, RY - 2.05, RY + 2.05, RZ + 2.4, RZ + 4.4),
              _cyl(1.0, RZ + 1.0, RZ + 9.0, (s * 34.5, RY), "z"))


def front_hub(s):
    """RV19 micro hub (9 x 9) running on the 25 mm standoff: 6 mm tyre seat between two 9 mm flanges, an O-ring
    groove inboard."""
    prof = [(0.0, 2.7), (0.0, 4.5), (0.4, 4.5), (0.6, 3.7), (1.8, 3.7), (2.0, 4.5), (2.5, 4.5), (2.5, 3.7), (8.5, 3.7), (8.5, 4.5), (9.0, 4.5), (9.0, 2.7)]
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    return _revolve_x(prof, s * 30.0, SA)


def tyre(od, idd, x0, x1, c):
    return _S(_cyl(od / 2, x0, x1, c), _cyl(idd / 2, x0 - 1, x1 + 1, c))


def standoff(L_x, c):
    return _S(_cyl(SO_R, *L_x, c), _cyl(1.25, L_x[0] - 1, L_x[1] + 1, c))


# ------------------------------------------------------------------------------------------------------------ wedgelet
def wedgelet(s):
    """RV17/18 TPU wedgelet: one ramp face (Z = 1 + 1.187 (50.1 - Y), 50 deg) over the nose. Two cheeks either side of
    the fork slot carry both standoffs (bores) and clamp the fork tail; the 25 mm axle standoff runs through a ring
    at the back; outboard a block round the 15 mm standoff end and a 1.7 mm ramp skin over a hollow (TPU flexes and
    soaks hits, and the hollow saves mass)."""
    from shapely.geometry import Point, Polygon, LineString
    k = 1.187
    def zr(y):
        return 1.0 + k * (50.1 - y)
    ramp = _ext(Polygon([(10.0, 0.0), (50.1, 0.0), (50.1, 1.0), (10.0, zr(10.0))]), "yz", -40.0, -16.0)
    under = _ext(Polygon([(10.0, -5.0), (50.1 - 1.7 / k, -5.0), (50.1 - 1.7 / k, 1.0), (10.0, zr(10.0) - 1.7)]), "yz", -40.0, -16.0)
    ring = Point(*SA).buffer(3.5, 64)
    cheek = _round(ring.union(Polygon([(26.5, 1.0), (26.5, 5.5), (29.5, 9.0), (33.5, 10.6), (38.0, 15.36), (50.1, 1.0)])), r_in=1.5)
    parts = [_ext(cheek, "yz", -29.0, -21.5)]
    blk = Point(*SB).buffer(3.6, 64).union(Polygon([(37.6, 2.5), (40.2, 8.0), (39.5, 10.0), (50.1, 10.0), (50.1, 1.0), (40.0, 1.0)]))
    parts.append(_ext(blk, "yz", -38.5, -35.8))
    parts.append(_box(-35.8, -29.0, 46.1, 50.1, 1.0, 12.0))                           # nose lip
    parts.append(_box(-21.5, -17.5, 43.8, 50.1, 1.0, 7.5))                            # inner nose tab
    parts.append(_S(_box(-38.5, -21.5, 38.0, 50.1, 1.0, 16.0), under))                # ramp skin
    body = _I(_U(*parts), ramp)
    body = _S(body, _box(-39.0, -29.0, 20.0, 52.0, 10.0, 17.0), _box(-21.5, -17.0, 20.0, 52.0, 7.5, 17.0))
    slot = _S(_box(-27.0, -24.5, 20.0, 43.8, 0.0, 17.0), ramp.cut(under))             # fork slot under the ramp skin
    body = _U(_S(body, slot), _I(_ext(ring, "yz", -27.0, -24.5), ramp))
    kid = LineString([(36.3, 4.6), (37.6, 7.6)]).buffer(1.0, 24)
    cuts = [_cyl(2.6, -39.0, -17.0, SA), _cyl(2.6, -36.5, -17.0, SB), _cyl(1.6, -39.0, -17.0, SB), _ext(kid, "yz", -29.5, -21.0)]
    sh = _S(body, *cuts)
    return sh if s < 0 else _mirror_x(sh)


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
    cuts = [_csk(3.3, 6.2, (-46.26, SA[0], SA[1]), "x", 1, 8.0), _csk(3.3, 6.2, (-41.76, SB[0], SB[1]), "x", 1, 8.0),
            _csk(3.3, 6.2, (-35.26, NUT[0], NUT[1]), "x", 1, 8.0), _cyl(2.6, -40.6, -38.0, SA),
            _box(-45.0, -43.4, -38.7, -24.8, 5.0, 15.0),                          # rear tyre relief on the inner face
            _box(-32.6, -31.4, -13.1, 2.6, 3.7, 13.3)]                            # clears the chassis nut lobe
    for y0 in (-11.0, -4.5, 2.0):     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, 5.0), (y0 + 5.0, 11.0)]).buffer(1.0, cap_style=1)
        cuts.append(_ext(sl, "yz", -50.0, -36.5))
    sh = _S(body, *cuts)
    return sh if s < 0 else _mirror_x(sh)


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
    inner = _round(Polygon([(-x + w, y0 + w), (x - w, y0 + w), (x - w, y1 - 1.6), (-x + w, y1 - 1.6)]), r_out=1.0)
    body = _S(outer, _ext(inner, "xy", z0 - 1, c["deck"]))
    add = []
    for px, py in INS:   # insert columns (floor to deck)
        add.append(_cyl(2.6, z0, c["deck"] + 0.1, (px, py), "z"))
    for sg in (1, -1):
        # motor front stop wall (load path: the N10 gearbox bears on it, not the base screws)
        add.append(_box(sg * 17.7, sg * (x - w + 0.1), -25.4, -23.4, z0, c["deck"] + 0.1))
        add.append(_box(sg * 21.7, sg * (x - w + 0.1), -23.4, -18.5, z0, c["deck"] + 0.1))
        # side lobe with the thin M3 nut (Y -16.3..2.8)
        lobe = Point(NUT[0], NUT[1]).buffer(4.7, 64).union(Point(1.5, 7.0).buffer(1.6, 32)).convex_hull
        add.append(_ext(lobe, "yz", sg * (x - 0.1), sg * 32.5))
        # front tabs (key into the weapon-mount notches) and inner tab walls
        add.append(_box(sg * 10.3, sg * 17.5, 13.0, 26.5, 5.35, 13.55))
        add.append(_box(sg * 10.3, sg * 13.3, 13.0, 26.5, z0, c["deck"]))
        # lugs carrying the standoffs (sloped top so they sit under the mount)
        lug = Polygon([(13.0, z0), (26.0, z0), (30.4, 1.0)] + _arc(SA, 4.5, 250, 300, 6) + [(36.6, 2.5)] + _arc(SB, 3.2, 250, 400, 16) + [(15.0, z1), (13.0, z1)])
        lug = _round(lug.convex_hull.difference(Polygon([(26.0, 0.0), (26.0, 2.5), (30.0, 1.0), (40.0, 1.3), (60, 0)])), r_in=0.0)
        add.append(_ext(lug, "yz", sg * 17.5, sg * 21.5))
    body = _U(body, *add)
    cuts = []
    # deck X-pocket lightening (from below, 1 mm skin stays)
    dz0, dz1 = c["deck"] - 0.5, c["deck"] + 1.0
    tri = [Polygon([(-21.5, 12.2), (21.5, 12.2), (0, -2.8)]), Polygon([(-21.5, -23.0), (21.5, -23.0), (0, -8.0)]),
           Polygon([(-22.5, 10.0), (-22.5, -20.5), (-6.5, -5.6)]), Polygon([(22.5, 10.0), (22.5, -20.5), (6.5, -5.6)])]
    for t in tri:
        cuts.append(_ext(_round(t, r_out=1.5), "xy", dz0, dz1))
    for xc in (-21.3, -8.9, 8.9, 21.3):
        cuts.append(_ext(_round(Polygon([(xc - 5, -35.5), (xc + 5, -35.5), (xc + 5, -25.5), (xc - 5, -25.5)]), r_out=1.2), "xy", dz0, dz1))
    for px, py in INS:
        cuts.append(_cyl(1.7, INS_Z[0] - 3, INS_Z[1], (px, py), "z"))           # heat-set bore
        cuts.append(_cyl(1.9, c["deck"] + 1.0, z1 + 1, (px, py), "z"))          # through the deck (screw run-out, vents)
        cuts.append(_cyl(1.2, INS_Z[1] - 0.1, z1 + 1, (px, py), "z"))
    # switch slot in the deck beside the top panel, 2 M2 pilot holes
    cuts.append(_ext(_round(Polygon([(23.9, -11.4), (26.1, -11.4), (26.1, 0.2), (23.9, 0.2)]), r_out=0.5), "xy", c["deck"] - 1, z1 + 1))
    for yy in (1.9, -13.1):
        cuts.append(_cyl(0.85, c["deck"] - 3, z1 + 1, (25.0, yy), "z"))
    for sg in (1, -1):
        # N10 keyhole: round seat for the gearbox shaft boss, narrowing to the floor (motor tilts in)
        kh = Point(RY, 11.6).buffer(2.0, 48).union(Polygon([(RY - 2.0, 11.6), (RY + 2.0, 11.6), (RY + 0.6, 5.3), (RY - 0.6, 5.3)])).union(Point(RY, 5.3).buffer(0.6, 16))
        cuts.append(_ext(kh, "yz", sg * (x - w - 0.5), sg * (x + 0.5)))
        # nut: M3 clearance through lobe + wall, hex pocket on the inside
        cuts.append(_cyl(1.6, sg * 26.0, sg * 33.0, NUT))
        hexp = Polygon([(NUT[0] + 3.2 * math.cos(math.radians(60 * i + 30)), NUT[1] + 3.2 * math.sin(math.radians(60 * i + 30))) for i in range(6)])
        cuts.append(_ext(hexp, "yz", sg * 27.6, sg * 29.6))
        cuts.append(_ext(_round(Polygon([(-7.1, 7.0), (-3.6, 7.6), (-6.6, 9.0)]), r_out=0.3), "yz", sg * 29.0, sg * 33.0))
        # standoff holes in the lugs, square key hole
        cuts.append(_cyl(2.5, sg * 17.0, sg * 22.0, SA))
        cuts.append(_cyl(1.6, sg * 17.0, sg * 22.0, SB))
        cuts.append(_ext(_round(Polygon([(20.8, 7.8), (24.2, 7.8), (24.2, 11.1), (20.8, 11.1)]), r_out=0.6), "yz", sg * 13.0, sg * 22.0))
    # weapon phase wire hole in the front wall
    cuts.append(_box(-7.3, 7.3, 13.0, 16.0, 15.0, c["deck"]))
    return _S(body, *cuts)


# ------------------------------------------------------------------------------------------------------------ misc
def weapon_lock():
    """RV00 TPU lock (Build Guide safety rule, not in the STEP): a block on the chassis nose deck under the tooth;
    with the tooth parked on it the drisk cannot turn."""
    return _box(-4.0, 4.0, 15.4, 19.0, 19.5, 22.0)


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


def build(part):
    """Model-file entry point (robot.shapes `model`): one part, world coordinates."""
    return _solid(PARTS[part]())
