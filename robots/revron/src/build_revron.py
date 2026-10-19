"""Revron 2.1 generator (rebuild from scratch, 2026-10-18).

Every measured number comes from robots/revron/params.json (SVRN STEP files, the builder's forum diary and the photos);
the derived layout follows from those numbers. Frame: X right, Y forward, Z up, chassis underside at Z = 0.

Architecture (forum diary): BE1806 outrunner is the weapon hub. Its stator is bolted to the right upright; an aluminium
spider is clamped on the motor shaft stub and carries three 2 mm Hardox plates (one hooked, balanced tooth plate between
two plain rings) with 4 countersunk M3 bolts and nuts. A 3 mm spigot on the spider runs in an F683ZZ flanged bearing in
the left upright, so the rotor is supported both sides. Uprights sit on square printed bosses on the chassis nose.
Drive: two N10 gearmotors at the front axle, O-ring belts to rear stub-axle wheels. TPU side panels, TPU sprung forks,
Ti top plate, printed base panel on heat-set inserts.
"""
import json, math, os, sys
ROOT = "/home/user/robobuild123d"
sys.path.insert(0, ROOT)
HERE = os.path.dirname(os.path.abspath(__file__))
PRM = json.load(open(os.path.join(HERE, "..", "params.json")))
OUT = os.path.join(ROOT, "robot/templates/revron.json")


def pv(k, default=None):
    v = PRM.get(k, {})
    v = v.get("value") if isinstance(v, dict) else v
    return float(v) if isinstance(v, (int, float)) else default


# ---------------------------------------------------------------- shape helpers
def place(s, at, rot=(0, 0, 0)): return {"type": "place", "shape": s, "at": [round(a, 4) for a in at], "rot": list(rot)}
def box(sx, sy, sz, at=(0, 0, 0)): return place({"type": "box", "size": [sx, sy, sz]}, at)
def boxr(x0, x1, y0, y1, z0, z1): return box(x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
def cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0)): return place({"type": "cylinder", "radius": r, "height": h}, at, rot)
def cylx(r, x0, x1, y, z): return cyl(r, x1 - x0, ((x0 + x1) / 2, y, z), (0, 90, 0))
def cylz(r, z0, z1, x, y): return cyl(r, z1 - z0, (x, y, (z0 + z1) / 2))
def U(*a): return {"type": "union", "items": list(a)}
def S(b, *c): return {"type": "subtract", "base": b, "cut": list(c)}
def fillet(s, r): return {"type": "fillet", "shape": s, "radius": r}
def r4(p): return [[round(a, 4), round(b, 4)] for a, b in p]


def yz(pts, x0, x1, spline=False):
    """Prism of a (y, z) outline extruded over x0..x1."""
    x0, x1 = min(x0, x1), max(x0, x1)
    loc = [[-z, y] for y, z in pts]
    return place({"type": "spline_prism" if spline else "prism", "points": r4(loc), "height": x1 - x0}, ((x0 + x1) / 2, 0, 0), (0, 90, 0))


def hull(pts):
    pts = sorted(set((round(a, 4), round(b, 4)) for a, b in pts))
    def cr(o, a, b): return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def circ_pts(c, r, n=40): return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
def rrect(y0, y1, z0, z1, r, n=6):
    pts = []
    for cy, cz, a0 in ((y1 - r, z1 - r, 0), (y0 + r, z1 - r, 90), (y0 + r, z0 + r, 180), (y1 - r, z0 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cy + r * math.cos(a), cz + r * math.sin(a)))
    return pts
def hexp(af, t, at, axis="x"):
    pts = [[af / 2 / math.cos(math.radians(30)) * math.cos(math.radians(60 * i + 30)), af / 2 / math.cos(math.radians(30)) * math.sin(math.radians(60 * i + 30))] for i in range(6)]
    rot = {"x": (0, 90, 0), "y": (90, 0, 0), "z": (0, 0, 0)}[axis]
    return place({"type": "prism", "points": r4(pts), "height": t}, at, rot)


def chaikin_open(p, n):
    """Chaikin smoothing of an open polyline, end points kept."""
    for _ in range(n):
        q = [p[0]]
        for (x0, y0), (x1, y1) in zip(p, p[1:]):
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        q.append(p[-1]); p = q
    return p


def chaikin(p, n):
    """Corner-cutting (quadratic B-spline) smoothing of a closed outline."""
    for _ in range(n):
        q = []
        for i in range(len(p)):
            (x0, y0), (x1, y1) = p[i], p[(i + 1) % len(p)]
            q += [(0.75 * x0 + 0.25 * x1, 0.75 * y0 + 0.25 * y1), (0.25 * x0 + 0.75 * x1, 0.25 * y0 + 0.75 * y1)]
        p = q
    return p




# ======================================================================================================================
# RVRN layout. Every number below is a measured feature of the RVRN reference CAD (research/rvrn_drive, measured with
# robot.checks.reference_cad.fingerprint / mid-plane sections; never imported) or the RVRN Build Guide BOM.
# Frame: X left(+)/right(-), Y forward, Z up, floor at Z = 0. Reference assembly frame -> ours: Y = 60 - x_ref,
# Z = y_ref - 4.25, X = 52.57 - z_ref.
# ======================================================================================================================
WY, WZ = 31.15, 22.35                 # weapon axis (axle 22.35 above the floor)
# weapon stack along X (motor base on the left upright's inner face)
UL_IN, UL_OUT = 13.5, 17.5            # upright_l (stator side), 4 mm
UR_IN, UR_OUT = -13.5, -17.5          # upright_r (bearing side), 4 mm
STATOR_RECESS = 0.0                   # RVRN CAD: stator base flat on the left upright's inner face (motor X -7.0..13.5)
MOT_X = UL_IN + STATOR_RECESS - 10.25  # be1806_bbb origin: base 10..13.5, bell -5..10, shaft collar -7..-5
CAN_TOP = MOT_X - 8.25                # -5.0 (RVRN: motor-side disc X -8..-5, spacer -5..3)
DT = 3.0                              # Hardox disc thickness
BL_X = (CAN_TOP - DT, CAN_TOP)        # blade_c (motor side disc) -8..-5
SP_X = (CAN_TOP, CAN_TOP + 8.0)       # printed spacer -5..3
DF_X = (SP_X[1], SP_X[1] + DT)        # floating disc 3..6
PM_X = (BL_X[0] - 3.0, BL_X[0])       # prop-mount clamp flange -11..-8 (RVRN C4: 15 OD x 3)
PM_SP = -22.0                          # prop-mount 5 mm spigot runs out to -22 through the MF85ZZ
SH_X = (PM_SP, UL_IN + STATOR_RECESS)   # BE1806 5 mm shaft + prop-mount spigot -22..13.5: stator bearings, bell, flange, MF85ZZ
BR_X = (UR_OUT - 0.6, UR_OUT + 1.9)   # MF85ZZ -18.1..-15.6: pressed in from the outer (countersunk) face, flange outside
PM_CB = 0.0                           # M2 heads stand on the prop-mount flange (a 1 mm counterbore left 0.05 mm to the bore)
BS_X = (BR_X[1], PM_X[0] + PM_CB - 1.2)   # RV09 bearing spacer on the spigot: inner race to the 4 M2 heads
DISC_R, TIP_R = 16.5, 21.5
BOLT_R, CAN_R, LIGHT_R = 14.0, 4.5, 9.46
A0 = 106.4                            # disc-local angle of tip 1, the bolt circles (on the tip radii) and, 45 deg on, the pockets
# standoffs (front pair) and the front wheel
SA = (33.15, 4.35)                    # 15 mm standoff (wedglet / side panel)
SB = (23.15, 5.5)                     # 25 mm standoff = front axle
SO_R = 2.5
SA_LEN, SB_LEN = 20.0, 25.0           # RVRN CAD: wedglet bore over the nose standoff runs to X 37 (20 mm part in the Drive BOM), the axle standoff to 42.5
SA_END, SB_END = UL_OUT + SA_LEN, UL_OUT + SB_LEN
FW_OD, FW_ID, FW_W = 11.0, 7.0, 6.0   # Scalextric micro tyre
FH_X = (30.0, 39.0)                   # micro hub (9 x 9)
FT_X = (32.5, 38.5)
# rear drive
RY, RZ = -37.85, 10.75                # N10 shaft (rear wheel axle), 21.5 tyre touches the floor
MOTX = 19.6                           # N10 origin |X|: body 3.7..27.5, shaft to 37.5
RH_X = (30.0, 42.0)                   # printed rear hub 16 x 12
RT_X = (32.5, 42.0)                   # F1 tyre 21.5 x 12 x 9.5
# chassis
CX, CW = 29.0, 1.3                    # outer half width, wall
CY0, CY1 = -44.4, 6.6                 # box
CZ0, CZ1 = 4.37, 19.37
FL_T = 1.0                            # floor (X-ribbed)
BP = dict(x=27.6, y0=-43.05, y1=5.15, z0=3.37, t=1.0)  # RVRN CAD panel 54.4 x 47.4 x 1 at Z 3.37, +0.4 a side: the CAD's M2 holes leave 0.6 mm edge (ORIGINAL_ISSUES)
FLOOR_Z0 = BP["z0"] + BP["t"]          # 3.4
FLOOR_Z1 = FLOOR_Z0 + FL_T            # 4.4
INS = [(25.0, 2.65), (-25.0, 2.65), (25.0, -28.94), (-25.0, -28.94), (0.0, -40.55)]   # RVRN CAD panel holes, edge ones 0.4 in
NUT_Y, NUT_Z = -18.85, 8.37           # RVRN CAD: wedglet rear M3 clearance hole -> alu nut in the chassis side wall
NUT_X0, NUT_XC = 23.3, 25.65          # nut boss inner face, nut centre (2.4 thick, 2.1 mm wall outboard)
SW_Z = 11.5                           # switch on the rear insert boss, slide along Y (pull rearward = off)
HOOD_Z = 23.37
LOCK = (16.5, 10.7)                   # weapon-lock pin (Y, Z): r 18.7 from the axle, between the R16.5 rim and the R21.5 tips, through both chassis lugs
WG_OUT = 51.8                         # wedglet outer face (|X|)
WM_CB = 0.0                           # motor screw head counterbore depth
UB_CB = 0.0                           # upright-to-standoff screw heads on the inner faces (RVRN fl/fr have plain 3.2 holes)
SLC_X = 34.9                          # countersink face of the wedglet-to-chassis screw (on the battered wall)
CSK_A, CSK_B = 48.7, 47.8              # countersink faces of the standoff-end screws on the nose ramp

parts = []
def P(**k): parts.append(k)


def arc(c, r, a0, a1, n=24):
    return [(c[0] + r * math.cos(math.radians(a0 + (a1 - a0) * k / n)), c[1] + r * math.sin(math.radians(a0 + (a1 - a0) * k / n))) for k in range(n + 1)]


def slot2(a, b, w, n=10):
    (ya, za), (yb, zb) = a, b
    ang = math.degrees(math.atan2(zb - za, yb - ya))
    return arc(b, w / 2, ang - 90, ang + 90, n) + arc(a, w / 2, ang + 90, ang + 270, n)


# ---------------------------------------------------------------- uprights (4 mm printed plates, RVRN fl / fr)
def upright_poly(R):
    px, pz = 11.05 - WY, 15.42 - WZ
    d = math.hypot(px, pz); base = math.degrees(math.atan2(pz, px)); off = math.degrees(math.acos(R / d))
    a_t = base - off                       # tangent point on the upper side
    if a_t < 0: a_t += 360
    a_n = -79.0 if R > 8 else -48.0        # neck
    pts = [(11.05, 15.42)]
    pts += arc((WY, WZ), R, a_t, a_n, 48)  # clockwise over the top
    pts += [(32.4, 11.6), (32.3, 10.6)] if R > 8 else [(31.0, 12.4), (31.1, 11.0)]
    pts += arc(SA, 3.23, 44.0, -90.0, 18)
    pts += [(8.05, 1.12), (8.05, 2.12), (11.05, 2.12), (11.05, 5.22), (18.25, 5.22), (19.25, 6.22), (19.25, 12.42), (18.25, 13.42), (11.05, 13.42)]
    return pts


def upright(side):
    R = 10.5 if side == "l" else 7.0
    x0, x1 = (UL_IN, UL_OUT) if side == "l" else (UR_OUT, UR_IN)
    body = yz(upright_poly(R), x0, x1)
    cut = [cylx(3.99, x0 - 1, x1 + 1, WY, WZ)]                                  # 7.98: motor base spigot (l) / MF85ZZ seat (r)
    xin = x0 if side == "l" else x1                                             # inner face (towards the drisk)
    for (y, z) in (SA, SB):
        cut.append(cylx(1.6, x0 - 1, x1 + 1, y, z))                             # 3.2 M3 clearance into the standoffs
    if side == "r":
        cut.append(cylx(4.6, BR_X[1] - 1.0, x1 + 1, WY, WZ))                          # clearance round the bearing spacer, inboard of the seat
    cut.append(yz(slot2((24.0, 9.75), (29.4, 5.75), 2.0), x0 - 1, x1 + 1))       # lightening slot over the standoffs
    if side == "l":
        cut.append(yz(chaikin([(20.6, 16.5), (25.9, 16.5), (23.85, 20.1)], 3), x0 - 1, x1 + 1))
        for dy, dz in ((0, 6), (0, -6), (8, 0), (-8, 0)):                       # BE1806 stator pattern 12 / 16
            cut.append(cylx(1.095, x0 - 1, x1 + 1, WY + dy, WZ + dz))
    else:
        cut.append(yz(chaikin([(19.6, 16.85), (25.6, 16.85), (23.5, 21.15)], 3), x0 - 1, x1 + 1))
    return S(body, *cut)


# ---------------------------------------------------------------- drisk
def disc_outline(tip_a):
    """RVRN drisk disc (PT_10): R16.5 with two tips at R21.5, 180 deg apart. The leading flank is tangent to the disc
    (it leaves the rim acos(16.5/21.5) = 39.9 deg ahead of the tip), the back of each tip drops radially to R17.7 and
    is filleted into the rim. Disc-local polar angles, counter-clockwise."""
    g = math.degrees(math.acos(DISC_R / TIP_R))
    P_ = lambda r, a: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))  # noqa: E731
    pts = []
    for k in (0, 1):
        aT = tip_a + 180.0 * k
        tip, tan_ = P_(TIP_R, aT), P_(DISC_R, aT - g)
        L = math.dist(tip, tan_)
        fl = (tip[0] + (tan_[0] - tip[0]) * 1.2 / L, tip[1] + (tan_[1] - tip[1]) * 1.2 / L)
        pts += chaikin_open([fl, tip, P_(17.7, aT + 0.1), P_(16.5, aT + 3.9), P_(DISC_R, aT + 6.0)], 3)[:-1]   # tip radiused, back edge filleted (> kerf)
        pts += arc((0, 0), DISC_R, aT + 6.0, aT + 180.0 - g, 40)
    return r4(pts)


# RVRN lightening pocket: a three-lobed window symmetric about its radius (u radial, v tangential, mm), centroid on r9.46
BLOB_HALF = [(4.03, 0.0), (3.86, 0.71), (2.59, 1.8), (1.36, 5.03), (0.76, 5.44), (0.03, 5.52), (-0.83, 5.1), (-3.15, 2.57), (-3.22, 1.9), (-2.96, 0.0)]


def blob(at_a):
    c, sn = math.cos(math.radians(at_a)), math.sin(math.radians(at_a))
    half = BLOB_HALF + [(u, -v) for u, v in reversed(BLOB_HALF[1:-1])]
    half = chaikin(half, 3)   # every corner filleted (> 0.1 kerf)
    pts = [(LIGHT_R * c + u * c - v * sn, LIGHT_R * sn + u * sn + v * c) for u, v in half]
    return r4(pts[::-1] if Polygon_area(pts) < 0 else pts)


def Polygon_area(p): return 0.5 * sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(p, p[1:] + p[:1]))


def disc_cuts(t, full=True):
    c = []
    for k in range(4):
        a = math.radians(A0 + 90 * k)
        c.append(cyl(1.095, t + 2, (BOLT_R * math.cos(a), BOLT_R * math.sin(a), 0)))
        if full:
            c.append(cyl(1.095, t + 2, (CAN_R * math.cos(a), CAN_R * math.sin(a), 0)))
            c.append(place({"type": "prism", "points": blob(A0 - 45 + 90 * k), "height": t + 2}, (0, 0, 0)))
    c.append(cyl(2.99 if full else 11.75, t + 2))
    return c


def spacer_shape():
    """RVRN drisk spacer (PT_9): ring R13.15 round the bell (bore 23.27), a lobe R2.45 round each long M2, blended into
    the ring over +-17 deg."""
    lobes = []
    for k in range(4):
        a = A0 + 90 * k
        c = (BOLT_R * math.cos(math.radians(a)), BOLT_R * math.sin(math.radians(a)))
        q = circ_pts(c, 2.45, 24) + [(13.0 * math.cos(math.radians(a + d)), 13.0 * math.sin(math.radians(a + d))) for d in (-17, -9, 9, 17)]
        lobes.append(place({"type": "prism", "points": r4(hull(q)), "height": 8.0}, (0, 0, 0)))
    ring = cyl(13.15, 8.0)
    holes = [cyl(1.095, 10.0, (BOLT_R * math.cos(math.radians(A0 + 90 * k)), BOLT_R * math.sin(math.radians(A0 + 90 * k)), 0)) for k in range(4)]
    return S(U(ring, *lobes), cyl(11.70, 10.0), *holes)   # 23.4 bore: 0.2 a side round the 23 bell (printed fit band)


PHASE = 90.0           # tips straight up/down in disc-local -> with rot [0,90,0] they point fore/aft
MF_AT = None


def prop_mount():
    fl = cylx(7.5, PM_X[1] - 2.0, PM_X[1], 0, 0)
    sh = cylx(2.49, PM_X[0], PM_X[1] - 2.0, 0, 0)
    cut = [cylx(1.095, PM_X[1] - 3, PM_X[1] + 1, CAN_R * math.sin(math.radians(A0 + 90 * k + PHASE_ROT)), -CAN_R * math.cos(math.radians(A0 + 90 * k + PHASE_ROT))) for k in range(4)]
    return S(U(fl, sh), *cut)


PHASE_ROT = 0.0


def wyz(a, r):
    dy, dz = yz_of(a, r)
    return WY + dy, WZ + dz


def yz_of(a, r):
    """disc-local polar (deg, mm) -> world (dy, dz) for discs placed with rot [0, 90, 0] (local x -> world -z, local y -> world y)."""
    t = math.radians(a)
    return r * math.sin(t), -r * math.cos(t)


# ---------------------------------------------------------------- base panel (1 mm, 5 x M2 CSK, 6 lightening holes)
def base_panel():
    x, y0, y1, z0, t = BP["x"], BP["y0"], BP["y1"], BP["z0"], BP["t"]
    body = place({"type": "prism", "points": r4(rrect_xy(-x, x, y0, y1, 1.5)), "height": t}, (0, 0, z0 + t / 2))
    cut = [cylz(1.095, z0 - 1, z0 + t + 1, px, py) for px, py in INS]

    for s in (1, -1):
        for tri in ([(25.0, -39.0), (25.0, -31.9), (16.6, -34.9)], [(1.25, -31.9), (1.25, -38.4), (8.4, -34.9)], [(6.2, -41.05), (18.8, -41.05), (12.5, -36.4)]):
            q = [(s * a, b) for a, b in tri]
            q = q if s > 0 else q[::-1]
            cut.append(place({"type": "prism", "points": r4(chaikin(q, 3)), "height": t + 2}, (0, 0, z0 + t / 2)))
    return S(body, *cut)


def shrink_yz(pts, d):
    """Inset an axis-aligned-ish (y, z) outline by d (shapely buffer, mitred)."""
    from shapely.geometry import Polygon
    q = Polygon(pts).buffer(-d, join_style=2)
    return [(round(a, 4), round(b, 4)) for a, b in list(q.exterior.coords)[:-1]]


def hexagon_pts(af):
    r = af / math.sqrt(3)
    return r4([(r * math.cos(math.radians(60 * i)), r * math.sin(math.radians(60 * i))) for i in range(6)])


def rrect_xy(x0, x1, y0, y1, r, n=6):
    pts = []
    for cx, cy, a0 in ((x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180), (x1 - r, y0 + r, 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


# ---------------------------------------------------------------- chassis (printed PLA-ST open box, X-ribbed floor)
def chassis():
    outer = boxr(-CX, CX, CY0, CY1, FLOOR_Z0 - 1.0, CZ1)
    inner = boxr(-CX + CW, CX - CW, CY0 + CW, CY1 - CW, FLOOR_Z1, CZ1 + 1)
    skirt = boxr(-CX + CW, CX - CW, CY0 + CW, CY1 - CW, FLOOR_Z0 - 1.1, FLOOR_Z0)   # base panel recess
    body = S(outer, inner, skirt)
    add = []
    # front lugs: tab filling each upright's notch, cheeks either side of the plate (the plate slides back between them)
    for s in (1, -1):
        xi, xo = (UL_IN, UL_OUT) if s > 0 else (-UR_IN, -UR_OUT)
        add.append(yz([(CY1 - 0.1, 5.3), (18.2, 5.3), (19.15, 6.25), (19.15, 12.4), (18.2, 13.35), (CY1 - 0.1, 13.35)], *sorted((s * (xi - 0.05), s * (xo + 0.05)))))   # tab (in the notch)
        add.append(boxr(*sorted((s * (xi - 3.0), s * (xi - 0.05))), CY1 - 0.1, 19.15, 3.4, 15.0))       # inner cheek
        # box section (RV01 front): a hollow rectangular tube outboard of the upright, the two standoffs pass through its
        # 5 mm holes; open at the back into the tub (phase wires run through it), the wedglet clip bears on its outer face
        bx = S(box_section(0.0, s), yz([(y, z) for y, z in shrink_yz(BOX_YZ, 1.2)], *sorted((s * (BOX_X[0] + 1.2), s * (BOX_X[1] - 1.2)))),
               boxr(*sorted((s * (BOX_X[0] + 1.2), s * (BOX_X[1] - 1.2))), CY1 - CW - 0.5, CY1 + 1.3, WG_Z0 + 1.2, 11.8))
        add.append(bx)
        for (y, z) in (SA, SB):
            add.append({"type": "intersect", "items": [cylx(3.75, *sorted((s * BOX_X[0], s * BOX_X[1])), y, z), box_section(0.0, s),
                                                       boxr(-CX - 10, CX + 10, CY1 - 1.0, SB[0], -1.0, 20.0)]})   # rear half only (the key-slot runs forward)   # boss round each standoff hole
        pad = boxr(*sorted((s * (CX - 0.1), s * 33.0)), NUT_Y - 3.4, NUT_Y + 3.4, NUT_Z - 3.4, NUT_Z + 3.4)   # clamp pad: takes the wedglet's inner face
        add.append(S(pad, wedglet(s)))
    # motor pockets (rear): front and rear stop walls either side of each N10
    for s in (1, -1):
        add.append(boxr(*sorted((s * 3.0, s * (CX - CW + 0.1))), RY + 5.25, RY + 6.45, FLOOR_Z1 - 0.1, RZ + 6.0))
        add.append(boxr(*sorted((s * 2.6, s * 3.6)), RY - 2.0, RY + 6.4, FLOOR_Z1 - 0.1, RZ + 2.0))   # inner end stop (low and short: the switch wires pass behind it)
    # X rib + insert bosses
    L = math.hypot(2 * (CX - CW), RY + 6.4 - (CY1 - CW)); ang = math.degrees(math.atan2(RY + 6.4 - (CY1 - CW), 2 * (CX - CW)))
    for a in (ang, -ang):
        add.append(place({"type": "box", "size": [L - 1.0, 1.6, 2.0]}, (0, (RY + 6.4 + CY1 - CW) / 2, FLOOR_Z1), (0, 0, a)))
    for px, py in INS:
        add.append(cylz(2.6, FLOOR_Z0, FLOOR_Z1 + 3.5, px, py))
    for s in (1, -1):   # alu nut pockets
        add.append(boxr(*sorted((s * NUT_X0, s * (CX - CW + 0.1))), NUT_Y - 4.6, NUT_Y + 4.6, FLOOR_Z1 - 0.1, NUT_Z + 4.0))
    body = U(body, *add)
    body = S(body, cylx(1.6, -CX, CX, LOCK[0], LOCK[1]))   # weapon-lock pin bore through both lugs
    cut = []
    # floor: triangular pockets between the X ribs
    yc = (RY + 5 + CY1 - CW) / 2
    for tri in ([(-22, CY1 - CW - 3), (22, CY1 - CW - 3), (0, yc + 3)], [(-22, RY + 8.0), (22, RY + 8.0), (0, yc - 3)],
                [(-CX + CW + 2.5, CY1 - CW - 6), (-CX + CW + 2.5, RY + 11), (-4.0, yc)], [(CX - CW - 2.5, CY1 - CW - 6), (4.0, yc), (CX - CW - 2.5, RY + 11)]):
        cut.append(S(place({"type": "prism", "points": r4(chaikin(tri, 3)), "height": 3.0}, (0, 0, FLOOR_Z1 - 0.5)),
                     *[boxr(*sorted((s_ * (NUT_X0 - 1.0), s_ * CX)), NUT_Y - 5.6, NUT_Y + 5.6, FLOOR_Z0 - 3, NUT_Z + 5) for s_ in (1, -1)]))   # pockets stop short of the nut bosses
    for s in (1, -1):
        cut.append(boxr(*sorted((s * 3.6, s * (CX - CW + 0.05))), CY0 + CW - 0.05, RY + 5.0, FLOOR_Z0 - 2, FLOOR_Z1 + 0.05))   # motor bays open to the panel
        cut.append(cylx(1.7, *sorted((s * (CX - CW - 0.5), s * (CX + 0.5))), RY, RZ))                     # N10 shaft bushing hole
        cut.append(boxr(*sorted((s * (CX - CW - 0.5), s * (CX + 0.5))), RY - 1.7, RY + 1.7, FLOOR_Z0 - 2, RZ))   # keyhole slot down to the base panel
        cut.append(cylx(1.6, *sorted((s * (NUT_X0 - 0.5), s * 34.0)), NUT_Y, NUT_Z))                     # M3 clearance (wall and pad)
        cut.append(csk_x(3, SLC_X, s, NUT_Y, NUT_Z))                                                       # the CSK head cone dips into the clamp pad
        for (y, z) in (SA, SB):
            cut.append(cylx(2.55, *sorted((s * (BOX_X[0] - 0.5), s * (BOX_X[1] + 0.5))), y, z))          # 5.1 standoff holes
            # 3.3 key-slot forward from each hole through the inner part of the box: the upright screws, backed out of the
            # standoffs, stay captive in the uprights and their shanks slide forward out of the box with the weapon module
        cut.append(boxr(*sorted((s * (BOX_X[0] - 0.5), s * SLOT_X)), SB[0], BOX_YZ[1][0] + 1.0, 1.5, SB[1] + 1.65))
        cut.append(boxr(*sorted((s * (NUT_XC - 1.3), s * (NUT_XC + 1.3))), NUT_Y - 2.8, NUT_Y + 2.8, NUT_Z, NUT_Z + 4.5))   # nut drops in from above
        cut.append(place({"type": "prism", "points": hexagon_pts(5.6), "height": NUT_XC + 1.25 - NUT_X0 + 0.5}, (s * (NUT_XC + 1.25 + NUT_X0 - 0.5) / 2, NUT_Y, NUT_Z), (0, 90, 0)))   # alu nut pocket (5.5 AF + 0.1), open to the inside
    for px, py in INS:
        cut.append(cylz(1.6, FLOOR_Z0 - 2, FLOOR_Z0 + 3.0, px, py))                                        # heat-set bore
        cut.append(cylz(1.05, FLOOR_Z0, FLOOR_Z1 + 3.6, px, py))                                             # screw run-out
    cut.append(boxr(-2.1, 2.1, CY0 - 0.5, CY0 + CW + 0.5, SW_Z - 2.15, SW_Z + 2.15))                # switch slot (rear wall)
    cut.append(boxr(5.5, 10.0, CY1 - CW - 0.5, CY1 + 0.5, 6.0, 10.5))                                       # weapon phase-wire hole
    return S(body, *cut)


# ---------------------------------------------------------------- hood (raised TPU, triangle cut-outs)
def hood():
    """Raised TPU hood (RVRN / revron21 photos): a shallow truncated pyramid over the tub, 1.2 mm skin, sides battered
    inwards 30 deg so hits glance off; a lip drops inside the tub rim and snaps under it. Two vent slots over the ESC."""
    t, rise, inset = 1.2, HOOD_Z - CZ1, 5.0
    def frustum(d):   # d = inward offset of the whole shell
        x0, y0, y1 = CX - d, CY0 + d, CY1 - d
        lo = r4(rrect_xy(-x0, x0, y0, y1, 3.0))
        hi = r4(rrect_xy(-(x0 - inset), x0 - inset, y0 + inset, y1 - inset, 3.0))
        return {"type": "loft", "ruled": True, "sections": [{"z": CZ1 + 1.0 - (0.01 if d else 0.0), "spline": False, "points": lo}, {"z": HOOD_Z - (t if d else 0.0), "spline": False, "points": hi}]}
    li = CX - CW - 0.1
    band = S(xy(rrect_xy(-CX, CX, CY0, CY1, 3.0), CZ1, CZ1 + 1.01), boxr(-li + 1.2, li - 1.2, CY0 + CW + 1.3, CY1 - CW - 1.3, CZ1 - 1, CZ1 + 2))   # deck ring joins skin and lip
    # inner face: the outer frustum dropped by t / cos(slope) so the battered skin is t thick normal to its face
    drop = t * math.hypot(rise - 1.0, inset) / inset
    outer = frustum(0.0)
    inner = {"type": "intersect", "items": [{"type": "loft", "ruled": True, "sections": [dict(sec, z=sec["z"] - drop) for sec in outer["sections"]]},
                                            boxr(-CX - 1, CX + 1, CY0 - 1, CY1 + 1, CZ1 + 0.99, HOOD_Z + 1)]}
    shell = U(band, S(outer, inner))
    lip = S(boxr(-li, li, CY0 + CW + 0.1, CY1 - CW - 0.1, CZ1 - 2.0, CZ1 + 0.01),
            boxr(-li + 1.2, li - 1.2, CY0 + CW + 1.3, CY1 - CW - 1.3, CZ1 - 3.0, CZ1 + 1.0))
    body = U(shell, lip)
    cut = []
    for s_ in (1, -1):
        cut.append(xy(slot2((s_ * 14.0, -26.0), (s_ * 14.0, -10.0), 3.0), HOOD_Z - 3.0, HOOD_Z + 1.0))   # vents over the ESC / battery
    return S(body, *cut)


# ---------------------------------------------------------------- wedglet + side panel (TPU, one piece per side)
def xz(pts, y0, y1):
    """Prism of an (x, z) outline extruded over y0..y1."""
    y0, y1 = min(y0, y1), max(y0, y1)
    return place({"type": "prism", "points": r4(pts), "height": y1 - y0}, (0, (y0 + y1) / 2, 0), (90, 0, 0))


def xy(pts, z0, z1):
    """Prism of an (x, y) outline extruded over z0..z1."""
    return place({"type": "prism", "points": r4(pts), "height": z1 - z0}, (0, 0, (z0 + z1) / 2))


def offset_open(line, d):
    """Offset of an open (x, y) polyline by d to its right (miter at the vertices, same point count)."""
    out = []
    for i, (x, y) in enumerate(line):
        a, b = line[max(i - 1, 0)], line[min(i + 1, len(line) - 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        L = math.hypot(tx, ty); tx, ty = tx / L, ty / L
        out.append((x + d * ty, y - d * tx))
    return out


# RVRN low-profile wedglet + side panel (TPU, one per side, mirrored). Measured from the RVRN CAD, never imported.
WG_Z0, WG_Z1 = 0.72, 15.87          # RVRN 0.87; 0.15 lower so the nose-standoff bore keeps a 1 mm floor (ORIGINAL_ISSUES)
WG_INNER = [(43.5, -47.7), (43.5, -28.8), (43.0, -26.8), (40.9, -25.1), (37.4, -24.6), (34.9, -23.4), (32.9, -21.3), (31.6, -17.8),
            (31.5, 3.2), (31.6, 6.0)]                                   # inner (chassis-side) face of the wall
WG_SIDE = [(-47.7, 10.3), (-47.2, 12.3), (-46.1, 13.9), (-43.7, 15.5), (-41.7, 15.87), (-14.7, 15.87), (-1.7, 13.3), (7.1, 12.4),
           (16.2, 9.9), (23.8, 9.9), (29.3, 14.0), (30.4, 15.0), (30.7, 15.2), (42.8, WG_Z0 + 1.3), (42.8, WG_Z0),
           (-39.5, WG_Z0), (-42.6, 2.1), (-45.2, 4.1), (-47.0, 6.8), (-47.5, 8.4)]  # side elevation (y, z): high rear rail, nose ramp
WG_FRONT = [(17.5, WG_Z0), (52.0, WG_Z0), (52.0, WG_Z0 + 1.3), (44.5, 9.9), (38.5, 9.9), (36.7, 10.2),
            (34.9, 11.4), (33.6, 12.7), (31.7, 12.7), (30.6, 15.2), (21.0, 15.2), (20.2, 14.9), (17.9, 13.2), (17.5, 12.3)]   # nose, seen from the front (x, z)
WG_NOSE = [(17.5, 42.8), (17.5, 31.2), (18.0, 30.8), (21.6, 30.4), (21.6, 19.2),
           (29.0, 19.2), (29.0, 29.2), (36.5, 29.2), (41.5, 29.6),
           (41.5, 27.1), (39.5, 27.1), (39.5, 19.2), (41.5, 19.2), (41.3, 18.2),
           (40.0, 16.6), (36.6, 15.6), (34.5, 13.4), (32.6, 9.3), (31.6, 5.0), (42.6, 5.0), (43.5, 6.4), (46.5, 8.2), (49.5, 11.2),
           (50.6, 13.0), (51.9, 17.1), (51.9, 31.3), (51.4, 33.4), (49.5, 37.2), (46.5, 40.2), (44.6, 41.3), (40.6, 42.6), (38.5, 42.8),
           (27.0, 42.8), (27.0, 37.2), (24.5, 37.2), (24.5, 42.8)]                     # nose plan (x, y): bay for the front wheel
WG_FLANGE = [(31.5, -19.0), (42.1, -19.5), (40.6, -8.0), (41.0, -2.9), (42.9, 6.0), (31.6, 5.0)]


def csk_x(d, x_face, s, y, z):
    """Countersink for an ISO 10642 M`d` screw whose head is flush at x = s*x_face, shank towards the chassis
    (-s): a 90 deg cone plus a clear bore outward for the head to enter. Matches robot.world.csk_dims (+0.1)."""
    dk, k = 2.2 * d + 0.2, 0.6 * d + 0.1
    prof = [[0.0, -k], [d / 2 + 0.1, -k], [dk / 2, 0.0], [dk / 2, 8.0], [0.0, 8.0]]
    return place({"type": "revolve", "profile": r4(prof)}, (s * x_face, y, z), (0, 90 * s, 0))


def belt_env(grow):
    rr, rf = 7.0, 3.5
    return hull(circ_pts((RY, RZ), rr + 1.2 + grow) + circ_pts(SB, rf + 1.2 + grow))


BOX_X = (18.1, 21.5)                    # chassis box section (|X|): outboard of the upright, inboard of the wedglet clip
SLOT_X = 20.5                          # key-slots in the box section run out to here (|X|)
BOX_YZ = [(CY1 - 0.1, 0.3), (38.0, 0.3), (38.0, 7.9), (33.0, 8.6), (30.5, 14.0), (CY1 - 0.1, 14.0)]


def box_section(grow=0.0, s=1):
    """Envelope of one chassis box section (+X side), grown by `grow` (clearance cut for the wedglet)."""
    pts = BOX_YZ if not grow else [(y + (grow if y > 30 else -grow), z + (grow if z > 1 else -grow)) for y, z in BOX_YZ]
    return yz(pts, s * (BOX_X[0] - grow), s * (BOX_X[1] + grow))


WG_SCREW_PAD = boxr(31.5, 33.5, NUT_Y - 3.4, NUT_Y + 3.4, NUT_Z - 3.4, NUT_Z + 3.4)   # wedglet inner face under the chassis-screw CSK (same footprint as the chassis clamp pad)


def wedglet(s):
    """RVRN low-profile TPU wedglet / side panel, one piece per side (built for the left, mirrored for the right).
    Side wall: its inner face follows the chassis and S-bends out round the rear wheel; the outer face is battered
    from 5 mm at the floor to 2 mm at the top (a ramp against side hits). Nose: a wedge ramp, a block that slides over
    both front standoffs, an open bay for the front wheel. A 1 mm skirt under the mid wall. Side elevation trims the
    top (high rail at the rear, dropping to the nose ramp)."""
    zb, zt = WG_Z0, WG_Z1
    inner = chaikin_open(WG_INNER, 2)
    bot = inner + offset_open(inner, 5.0)[::-1]
    top = inner + offset_open(inner, 2.0)[::-1]
    wall = {"type": "loft", "ruled": True, "sections": [{"z": zb, "spline": False, "points": r4(bot)}, {"z": zt, "spline": False, "points": r4(top)}]}
    side = yz(WG_SIDE, 16.0, 54.0)
    nose = {"type": "intersect", "items": [xy(WG_NOSE, zb, zt), xz(WG_FRONT, 4.9, 43.0), side]}
    body = U({"type": "intersect", "items": [wall, side]}, nose, xy(WG_FLANGE, zb, zb + 1.0))
    body = U(body, WG_SCREW_PAD,   # squares off the S-bend under the countersink (the chassis clamp pad meets it flat)
             boxr(33.0, 35.2, -24.4, -21.5, NUT_Z - 3.6, NUT_Z + 3.6))   # and 1.2+ of TPU between the CSK head and the S-bend face
    cut = [
        {"type": "intersect", "items": [cylx(2.6, 17.0, SA_END, SA[0], SA[1]), boxr(16.0, 60.0, 20.0, 45.0, -1.0, 20.0)]},   # inboard the standoff runs in an open channel (the wall wraps it only partly)
        cylx(1.6, SA_END - 0.5, CSK_A - 1.0, SA[0], SA[1]),   # M3 clearance up to the countersink cone
        cylx(2.6, 17.0, SB_END, SB[0], SB[1]),            # bore over the axle standoff
        cylx(1.6, SB_END - 0.5, CSK_B - 1.0, SB[0], SB[1]),
        cylx(1.6, 30.0, 50.0, NUT_Y, NUT_Z),               # chassis screw into the alu nut
        {"type": "intersect", "items": [yz(rrect(-44.0, -32.0, 4.9, 14.1, 1.5), 43.3, 45.0),
                                         xz([(43.3, 4.0), (45.0, 4.0), (45.0, 11.5), (44.5, 14.1), (43.3, 14.1)], -45.0, -31.0)]},   # rear-wheel relief on the inner face, its top eased to keep 1.2 behind it under the battered face
        boxr(24.5, 27.0, 27.0, 29.3, 0.0, 16.0),           # slot between the clip cheeks
        boxr(21.0, 29.5, 25.5, 27.01, 11.2, 16.0),         # flat top ahead of the clip (no knife edge at the slope)
        boxr(23.0, 27.0, 27.0, 29.3, 7.0, 16.0),           # H clip: two cheeks joined by a web
        boxr(23.0, 27.0, 27.0, 29.3, 0.0, 5.0),
        csk_x(3, CSK_A, 1, SA[0], SA[1]),                  # M3 countersinks on the nose ramp (CSK alu screws, flush)
        csk_x(3, CSK_B, 1, SB[0], SB[1]),
        csk_x(3, SLC_X, 1, NUT_Y, NUT_Z),                  # and on the battered side wall
        S(yz(belt_env(0.7), 30.4, 32.6), WG_SCREW_PAD, boxr(29.0, 34.0, -60.0, -19.5, -1.0, 20.0)),   # belt channel on the inner face, a pad kept between the belt runs under the chassis-screw countersink
        boxr(30.4, 32.6, -19.5, SB[0], -1.0, 1.95),        # where the belt runs low the channel opens through the floor (no skin)
        boxr(47.7, 53.0, SA[0] - 3.0, SA[0] + 3.0, -1.0, SA[1]),
        boxr(CSK_A, 53.0, SA[0] + 2.5, 39.0, -1.0, 20.0),   # no sliver between the head bore and the rounded nose corner   # the CSK head bore leaves a 0.2 mm floor: open it (head seats on the cone)
        boxr(17.0, 21.7, 35.6, 38.3, 7.5, 12.0),          # no tapering tongue over the front of the box section
        yz([(22.1, 2.7), (36.27, 15.7), (36.27, 20.0), (10.0, 20.0), (10.0, 2.7)], 17.0, 21.7),   # the skin over the box-section slope ends square to the ramp, 1.6 thick
        boxr(17.0, 21.7, 38.0, 40.0, 5.8, 12.0),          # and no knife edge on the block ahead of it
        box_section(0.1),                                  # clears the chassis box section (the nose clip sits on its outer face)
        boxr(0.0, BOX_X[0] - 0.1, -60.0, 60.0, -1.0, 30.0),   # nothing inboard of the box section (slides off outward)
        S(boxr(29.5, 44.0, 31.9, 36.5, 0.0, 6.5), cylx(3.8, 29.0, 45.0, SA[0], SA[1])),   # hollow under the nose plate, a 1.2 tube kept round the nose standoff
        boxr(28.0, 35.0, 36.4, 40.0, 0.0, 3.0),
        xz([(29.0, 0.0), (29.0, 8.7), (43.5, 8.7), (49.0, 2.6), (49.0, 0.0)], 12.5, 19.1),   # hollow under the wedge ramp (1.2 roof under the ramp, 1.5 tip wall)
        xz([(29.0, 0.0), (29.0, 11.0), (32.5, 11.5), (35.6, 4.2), (38.0, 2.3), (43.0, 0.5), (43.0, 0.0)], 6.2, 12.5),
        xz([(35.3, 16.0), (35.3, 11.3), (38.0, 6.2), (44.0, 4.2), (49.0, 1.95), (55.0, 1.95), (55.0, 16.0)], 4.9, 12.5),   # ramp top face
        boxr(29.0, 34.5, 12.5, 19.1, 9.6, 16.0),
    ]
    sh = S(body, *cut)
    return sh if s > 0 else {"type": "mirror", "shape": sh, "axis": "x"}


# ---------------------------------------------------------------- wheels
def rear_hub():   # RV21, local x 0 = inner face: O-ring groove (1.0 flanges), then the 12 mm F1 tyre seat with a retaining ridge
    prof = [(1.5, 0.0), (8.0, 0.0), (8.0, 0.9), (7.0, 0.9), (7.0, 2.1), (8.0, 2.1), (8.0, 3.0), (6.0, 3.0), (6.0, 6.0), (6.15, 6.3), (6.15, 9.0),
            (6.0, 9.3), (6.0, 12.0), (1.5, 12.0)]
    sh = place({"type": "revolve", "profile": r4(prof)}, (0, 0, 0), (0, 90, 0))
    return S(sh, place({"type": "cylinder", "radius": 1.0, "height": 10.0}, (7.5, 0, 3.5), (0, 0, 0)))   # M2 grub-screw hole


RH_TYRE = 3.0     # tyre inner face (hub-local)
FH_TYRE = 3.0


def front_hub():  # RV19 9 mm micro hub on the 5 mm standoff: O-ring groove inboard, 7 mm tyre seat
    prof = [(2.6, 0.0), (4.5, 0.0), (4.5, 0.9), (3.5, 0.9), (3.5, 2.1), (4.5, 2.1), (4.5, 3.0), (3.6, 3.0), (3.6, 9.2), (2.6, 9.2)]
    return place({"type": "revolve", "profile": r4(prof)}, (0, 0, 0), (0, 90, 0))


def tyre(od, idd, w):
    return S(cylx(od / 2, 0.0, w, 0, 0), cylx(idd / 2, -1.0, w + 1.0, 0, 0))


# ======================================================================================================================
# parts
# ======================================================================================================================
def mf(x): return x                               # drisk parts are drawn in world coordinates
BLM = (BL_X[0] + BL_X[1]) / 2
MF_AT, MF_ROT = [WZ, -WY, -BLM], [0, -90, 0]       # children of blade_c drawn in world coordinates
PLA = dict(material="pla_st", process="fdm")

P(id="tub", kind="structure", print_orientation="-z", rotates_with="fixed", solid_fraction=0.9, color="#2a2c30", shape=chassis(), **PLA,
  label="RV01 printed PLA-ST open box: X-ribbed floor, rear N10 pockets, front lugs that seat the weapon uprights, 2 alu-nut pockets, 5 insert bosses")
P(id="base_panel", kind="structure", print_orientation="+z", rotates_with="fixed", color="#2a2c30", shape=base_panel(), **PLA,
  label="RV26 1 mm printed base panel 47.4 x 54.4, 5 M2 CSK into the floor inserts, 6 lightening holes")
P(id="top_armour", kind="armor", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#5a5f68", shape=hood(),
  label="raised TPU hood: shallow battered pyramid, two vent slots, lip snaps under the tub rim")

# weapon module (guide: quick change = unbolt 4 M3): both uprights, motor, bearing and drisk lift forward off the chassis
# lugs once the 4 upright-to-standoff screws are out; the standoffs stay in the chassis box sections with the wedglets
P(id="upright_l", kind="structure", print_orientation="+x", rotates_with="fixed", solid_fraction=1.0, color="#2a2c30", shape=upright("l"), **PLA,
  label="RV02 4 mm printed plate: BE1806 stator bolted to it (4 M2, 12/16 pattern), notch seats on the chassis lug, 2 M3 into the standoffs")
P(id="upright_r", kind="structure", parent="upright_l", print_orientation="+x", rotates_with="fixed", solid_fraction=1.0, color="#2a2c30", shape=upright("r"), **PLA,
  label="RV03 4 mm printed plate: MF85ZZ seat for the prop-mount spigot, notch on the chassis lug, 2 M3 into the standoffs")
for s, n in ((1, "l"), (-1, "r")):
    xi = UL_OUT if s > 0 else UR_OUT
    for nm, (y, z), L in (("a", SA, SA_LEN), ("b", SB, SB_LEN)):
        P(id=f"so_{nm}{n}", **({"parent": f"so_a{n}"} if nm == "b" else {}), kind="pin", role="standoff", material="aluminium", process="cots", rotates_with="fixed", color="#b8bcc2",
          stock=f"M3 x {L:g} mm aluminium standoff, 5 mm OD", shape=S(cylx(SO_R, *sorted((xi, s * (abs(xi) + L))), y, z), cylx(1.25, *sorted((s * (abs(xi) - 1), s * (abs(xi) + L + 1))), y, z)),
          label=f"{L:g} mm M3 alu standoff (5 OD): clamps the upright" + (" and is the greased front axle" if nm == "b" else "") + "; the wedglet slides over it")
P(id="weapon_motor", kind="weapon_motor", catalog="be1806_bbb", exposed=True,
  exposed_reason="Drisk: the BE1806 bell is the hub of the weapon and turns inside the spacer between the two Hardox discs, as on the real RVRN; the discs (R16.5-21.5) shield it radially", parent="upright_l", at=[MOT_X, WY, WZ], rot=[90, 0, 180], rotates_with="fixed",
  label="BBB BE1806 2300 kV: stator bolted to the left upright, the bell turns with the drisk")
P(id="blade_c", kind="weapon", material="hardox", process="laser", stock="3 mm Hardox 450", secondary_ops=["drilled", "tapped"], organic=True, rotates_with="weapon",
  shape=S(place({"type": "prism", "points": disc_outline(A0), "height": DT}, (0, 0, 0)), *disc_cuts(DT)),
  at=[BLM, WY, WZ], rot=[0, 90, 0], parent="upright_l",
  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [CAN_TOP - 0.5, WY, WZ], "min": 0, "max": 360, "default": 0}, color="#d9dde2",
  weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2},
  label="RV10 drisk disc, motor side: 3 mm Hardox, R16.5 with two tips at R21.5, 6 mm bore, 4 M2 on r4.5 (bell), 4 M2 on r14 (stack), 4 x 8.3 lightening")
P(id="disc_f", kind="other", role="blade", material="hardox", process="laser", stock="3 mm Hardox 450", secondary_ops=["drilled"], rotates_with="weapon",
  shape=S(place({"type": "prism", "points": disc_outline(A0), "height": DT}, (0, 0, 0)), *disc_cuts(DT, full=False)),
  parent="blade_c", at=[0, 0, (DF_X[0] + DF_X[1]) / 2 - BLM], rot=[0, 0, 0], color="#d9dde2",
  label="RV11 floating drisk disc: same 3 mm Hardox profile, 23.5 bore clears the bell, held by the 4 long M2")
P(id="spacer", kind="other", role="spacer", rotates_with="weapon", print_orientation="+z", parent="blade_c", at=[0, 0, (SP_X[0] + SP_X[1]) / 2 - BLM], rot=[0, 0, 0],
  shape=spacer_shape(), color="#2a2c30", **PLA, label="RV04 8 mm printed drisk spacer round the bell (ID 23.27), 4 lobes for the long M2")
P(id="prop_mount", kind="other", role="hub", material="aluminium", process="turned", rotates_with="weapon", parent="blade_c", at=MF_AT, rot=MF_ROT,
  shape=S(cylx(7.5, PM_X[0], PM_X[1], WY, WZ), cylx(2.5, PM_X[0] - 1, PM_X[1] + 1, WY, WZ),
          *[cylx(1.095, PM_X[0] - 1, PM_X[1] + 1, *wyz(A0 + 90 * k, CAN_R)) for k in range(4)],
          *[cylx(1.95, PM_X[0] - 1, PM_X[0] + PM_CB, *wyz(A0 + 90 * k, CAN_R)) for k in range(4)]),
  secondary_ops=["drilled"], color="#9aa0a6", label="RV07 BE1806 prop-mount flange (15 mm): clamps the motor-side disc to the bell with 4 M2, collet on the 5 mm shaft")
P(id="wshaft", kind="shaft", material="steel", process="cots", stock="BE1806 shaft + prop-mount spigot (bought in)", rotates_with="weapon", shaft_of="weapon_motor", parent="blade_c",
  at=MF_AT, rot=MF_ROT, shape=cylx(2.49, SH_X[0], SH_X[1], WY, WZ), color="#777777", solid_fraction=0.11,
  label="BE1806 5 mm shaft and the prop-mount spigot it carries out through the MF85ZZ (solid_fraction 0.11: only the ~0.6 g spigot counts, the rotor shaft is already in the 18.5 g motor)")
P(id="wbearing", kind="bearing", parent="upright_r", material="steel", process="cots", rotates_with="fixed", stock="MF85ZZ", color="#555555",
  shape=S(U(cylx(4.6, BR_X[0], UR_OUT, WY, WZ), cylx(4.0, UR_OUT, BR_X[1], WY, WZ)), cylx(2.5, BR_X[0] - 1, BR_X[1] + 1, WY, WZ)),
  label="MF85ZZ 5 x 8 x 2.5 flanged, pressed into the right upright from the outer face, flange outside")
P(id="bspacer", kind="other", role="spacer", parent="blade_c", rotates_with="weapon", print_orientation="+x", at=MF_AT, rot=MF_ROT, color="#2a2c30",
  shape=S(cylx(3.45, BS_X[0], BS_X[1], WY, WZ), cylx(2.52, BS_X[0] - 1, BS_X[1] + 1, WY, WZ)), **PLA,
  label="RV09 printed bearing spacer on the prop-mount spigot: clamps the MF85ZZ inner race against the flange, clears the upright bore")
# drisk stack bolts thread straight into the tapped 3 mm Hardox motor-side disc (no nuts: the nuts on the fixed side
# stood 0.6 mm from the RH upright screw heads, see ORIGINAL_ISSUES)

for s, n in ((1, "l"), (-1, "r")):
    rot = [0, 0, 0] if s > 0 else [0, 0, 180]
    P(id=f"motor_{n}", kind="motor", catalog="n10_2200rpm_spicy", at=[s * MOTX, RY, RZ], rot=rot, rotates_with="fixed")
    hl = RH_X[0] - MOTX
    P(id=f"whub_r{n}", kind="pulley", rotates_with=f"wheel_r{n}", print_orientation="+x", shape=rear_hub(), at=[hl, 0, 0], parent=f"motor_{n}",
      joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [hl + 6.0, 0, 0], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
      label="RV21 printed rear hub 16 x 12 pressed on the N10 D-shaft, O-ring groove inboard, M2 grub screw")
    P(id=f"wheel_r{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_r{n}", rotates_with=f"wheel_r{n}", parent=f"whub_r{n}", at=[RH_TYRE, 0, 0],
      shape=tyre(21.5, 12.0, 9.5), color="#1b1b1b", stock="Scalextric F1 front tyre 21.5 x 12 x 9.5", label="Scalextric F1 tyre 21.5 x 12 x 9.5")
    so = f"so_b{n}"
    P(id=f"whub_f{n}", kind="pulley", rotates_with=f"wheel_f{n}", print_orientation="+x", shape=front_hub(), at=[s * FH_X[0], SB[0], SB[1]], rot=rot, parent=so,
      joint={"kind": "revolute", "axis": [s, 0, 0], "pivot": [s * (FH_X[0] + 4.5), SB[0], SB[1]], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
      label="RV19 printed front hub 9 x 9 with O-ring groove, runs greased on the 5 mm standoff (no bearing)")
    P(id=f"wheel_f{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_f{n}", rotates_with=f"wheel_f{n}", parent=f"whub_f{n}", at=[FH_TYRE, 0, 0],
      shape=tyre(FW_OD, FW_ID, FW_W), color="#1b1b1b", stock="Scalextric Micro SLX tyre 11 x 7 x 6", label="Scalextric micro tyre 11 x 7 x 6")
    P(id=f"wedglet_{n}", kind="fork", parent=f"so_a{n}", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#3c4048", shape=wedglet(s),
      label="RV17/18 + RV23/24 low-profile TPU wedglet / side panel: slides over both front standoffs, 3 M3 (two standoff ends, one chassis nut)")
    P(id=f"nut_c{n}", kind="nut", catalog="nut_m3_alu", at=[s * NUT_XC, NUT_Y, NUT_Z], rot=[0, 90, 0], rotates_with="fixed")

P(id="battery", kind="battery", catalog="lipo_2s_180_turnabot", at=[-13.3, -12.75, FLOOR_Z1 + 1.0 + 5.5], rot=[0, 0, 90], retained="press_fit")
P(id="rxesc", kind="esc", catalog="malenki_nano", at=[14.0, -12.0, FLOOR_Z1 + 1.0 + 2.5], rot=[0, 0, 90], retained="kapton")
P(id="wesc", kind="esc", catalog="bbb_ant_esc", at=[14.0, -12.0, FLOOR_Z1 + 1.0 + 5.0 + 2.0], rot=[0, 0, 90], retained="kapton")
P(id="power_switch", kind="switch", catalog="switch_slide_12x4", at=[0.0, CY0 + 5.0, SW_Z], rot=[0, 0, 90], retained="press_fit", label="BBB ant switch: pull rearward = off",
  marked=True, tool_free=True)
for i, (x, y) in enumerate(INS):
    P(id=f"insert_b{i}", kind="insert", catalog="heatset_m2", at=[x, y, FLOOR_Z0 + 1.5])

fast = []
def F(**k):
    k.setdefault("head", "socket"); k.setdefault("tool", "hex1.5"); k.setdefault("removable", True); fast.append(k)
for i, (x, y) in enumerate(INS):
    F(id=f"bolt_b{i}", designation="M2x6", at=[x, y, BP["z0"]], dir=[0, 0, 1], through=["base_panel", "tub"], threads_into=f"insert_b{i}", head="button", tool="hex1.3",
      reason="ISO 7380 button heads under the 1 mm panel: an M2 countersink (1.2 deep) would knife-edge right through it")
for k, (dy, dz) in enumerate(((8, 0), (-8, 0), (0, 6), (0, -6))):
    F(id=f"bolt_wm{k}", designation="M2x6", at=[UL_OUT - WM_CB, WY + dy, WZ + dz], dir=[-1, 0, 0], through=["upright_l"], threads_into="weapon_motor")
for s, n in ((1, "l"), (-1, "r")):
    xi = UL_IN if s > 0 else UR_IN
    up = "upright_l" if s > 0 else "upright_r"
    for nm, (y, z), e in (("a", SA, SA_END), ("b", SB, SB_END)):
        F(id=f"bolt_u{n}{nm}", designation="M3x10", material="aluminium", at=[xi + s * UB_CB, y, z], dir=[s, 0, 0], head="button", through=[up], threads_into=f"so_{nm}{n}", tool="hex2",
          reason="Quick-change: ISO 7380 button heads (2 mm key, 1.65 mm head) so the key clears the R16.5 drisk rim; backed out they stay captive in the upright between plate and disc and leave with the module")
        F(id=f"bolt_s{n}{nm}", designation="M3x16" if nm == "a" else "M3x10", material="aluminium", at=[s * (CSK_A if nm == "a" else CSK_B), y, z], dir=[-s, 0, 0], head="countersunk", through=[f"wedglet_{n}"], threads_into=f"so_{nm}{n}", tool="hex2.5",
          reason="Wedglet bore slides over the standoff (takes the shear); the CSK screw along the standoff axis clamps it to the end face")
    F(id=f"bolt_s{n}c", designation="M3x12", material="aluminium", at=[s * SLC_X, NUT_Y, NUT_Z], dir=[-s, 0, 0], head="countersunk", through=[f"wedglet_{n}", "tub"], threads_into=f"nut_c{n}", tool="hex2.5")
for k in range(4):
    dy, dz = yz_of(A0 + 90 * k, BOLT_R)
    F(id=f"bolt_d{k}", designation="M2x14", at=[DF_X[1], WY + dy, WZ + dz], dir=[-1, 0, 0], through=["disc_f", "spacer"], threads_into="blade_c",
      access_before=["upright_l", "weapon_motor", "wedglet_l", "so_al", "so_bl", "tub", "upright_r", "wbearing", "bspacer"], reason="The drisk stack is bolted up on the bench before it goes onto the motor bell (guide step 1)")
    dy, dz = yz_of(A0 + 90 * k, CAN_R)
    F(id=f"bolt_p{k}", designation="M2x8", at=[PM_X[0] + PM_CB, WY + dy, WZ + dz], dir=[1, 0, 0], head="button", through=["prop_mount", "blade_c"], threads_into="weapon_motor",
      access_before=["upright_r", "wbearing", "bspacer"],
      reason="Driven on the bench when the drisk is built onto the motor (guide step 2), before the right upright and its bearing go on")

# O-ring belts: rear hub groove -> front hub groove, one per side
BX = (RH_X[0] + 0.9, RH_X[0] + 2.1)   # O-ring in the inboard hub grooves
def belt_shape(s):
    rr, rf = 7.0, 3.5
    o = hull(circ_pts((RY, RZ), rr + 1.2) + circ_pts(SB, rf + 1.2)); i = hull(circ_pts((RY, RZ), rr) + circ_pts(SB, rf))
    return S(yz(o, *sorted((s * BX[0], s * BX[1]))), yz(i, *sorted((s * BX[0] - s, s * BX[1] + s))))
c_ = math.hypot(SB[0] - RY, SB[1] - RZ)
LOOP = 2 * math.sqrt(c_ ** 2 - (7.6 - 4.1) ** 2) + math.pi * (7.6 + 4.1) + 2 * (7.6 - 4.1) * math.asin((7.6 - 4.1) / c_)
BELT_L = round(LOOP / 1.10, 1)
for s, n in ((1, "l"), (-1, "r")):
    P(id=f"belt_{n}", kind="belt", material="rubber", process="cots", shape=belt_shape(s), color="#111111",
      belt={"pulleys": [f"whub_r{n}", f"whub_f{n}"], "kind": "o_ring", "length_mm": BELT_L, "width_mm": 1.2},
      label=f"1.2 mm nitrile O-ring, {BELT_L} mm inside circumference, 10 % stretch: drives the front wheel off the rear hub")


def chain_root(q):
    by = {x["id"]: x for x in parts}
    while q.get("parent"):
        q = by[q["parent"]]
    return q["id"]


def Wr(i, a, b, awg, kind, sl): return {"id": i, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": sl}
wires = [Wr("w_bat_sw", "battery.xt30", "power_switch.in", 24, "power", 8), Wr("w_sw_wesc", "power_switch.out", "wesc.bat", 24, "power", 8),
         Wr("w_sw_rx", "power_switch.out", "rxesc.bat", 26, "power", 8), Wr("w_wesc_m", "wesc.motor", "weapon_motor.phases", 24, "motor", 15),
         Wr("w_rx_wesc", "rxesc.wpn", "wesc.rx", 30, "signal", 6), Wr("w_m_l", "rxesc.m1", "motor_l.terminals", 28, "motor", 6),
         Wr("w_m_r", "rxesc.m2", "motor_r.terminals", 28, "motor", 6)]
conn = []
def C(a, b, m, r, **k): conn.append(dict(a=a, b=b, method=m, reason=r, **k))
for s, n in ((1, "l"), (-1, "r")):
    up = "upright_l" if s > 0 else "upright_r"
    C(f"motor_{n}", "tub", "interlock", "N10 drops into its rear pocket from below: front/rear stop walls, inner end stop and the gearbox face on the side wall; the base panel closes the bay")
    C(f"whub_r{n}", f"motor_{n}", "press_fit", "Printed hub pressed on the 3 mm D-shaft, M2 grub screw on the flat", interference_mm=0.1, mechanical_key=True)
    C(f"wheel_r{n}", f"whub_r{n}", "press_fit", "F1 tyre stretched over the 12 mm hub seat, ridge keeps it on", interference_mm=0.3, mechanical_key=True)
    C(f"whub_f{n}", f"so_b{n}", "shaft", "Front hub runs greased on the 5 mm alu standoff, held between the wedglet block and the standoff screw head")
    C(f"wheel_f{n}", f"whub_f{n}", "press_fit", "Micro tyre stretched into the 7 mm hub seat between the flanges", interference_mm=0.2, mechanical_key=True)
    for nm in "ab":
        C(f"so_{nm}{n}", up, "screw", "M3 CSK alu screw through the upright into the standoff end; standoff end face clamps the plate")
        C(f"so_{nm}{n}", "tub", "pin", "Standoff passes through the 5 mm hole in the chassis box section", mechanical_key=True)
        C(f"so_{nm}{n}", f"wedglet_{n}", "screw", "Wedglet slides over the standoff and is screwed to its outer end (M3 CSK alu)", mechanical_key=True)
    C(f"belt_{n}", f"whub_r{n}", "interlock", "O-ring in the rear hub groove under 10 % stretch")
    C(f"belt_{n}", f"whub_f{n}", "interlock", "O-ring in the front hub groove; drives the front wheel")
    C(f"wedglet_{n}", "tub", "screw", "Wedglet / side panel screwed to the chassis side wall into a press-fit alu M3 nut")
    C(f"nut_c{n}", "tub", "press_fit", "Alu M3 nut pressed into the hex pocket inside the side wall", interference_mm=0.1, mechanical_key=True)
    C(up, "tub", "interlock", "Upright notch seats over the chassis lug between two cheeks; the standoffs and wedglet screws lock it", mechanical_key=True)
C("weapon_motor", "upright_l", "screw", "Stator base bolted to the left upright with 4 M2 (12 / 16 mm pattern)")
C("blade_c", "weapon_motor", "screw", "Motor-side disc clamped to the bell by the prop-mount flange and 4 M2 into the bell: the bell drives the drisk", mechanical_key=True)
C("prop_mount", "blade_c", "screw", "Prop-mount flange clamps the disc to the bell, 4 M2", mechanical_key=True)
C("wshaft", "wbearing", "shaft", "5 mm prop-mount spigot in the MF85ZZ inner race: the second support of the drisk")
C("bspacer", "wshaft", "pin", "RV09 spacer slid on the spigot, clamped between the M2 heads on the flange and the inner race", mechanical_key=True)
C("wshaft", "weapon_motor", "press_fit", "The motor's own rotor shaft, pressed in the bell and held by its circlip behind the stator", interference_mm=0.02, mechanical_key=True)
C("prop_mount", "wshaft", "press_fit", "Prop-mount collet clamped on the 5 mm shaft", interference_mm=0.02, mechanical_key=True)
C("wbearing", "upright_r", "press_fit", "MF85ZZ pressed into the 7.98 seat, flange on the inner face", interference_mm=0.02, mechanical_key=True)
C("spacer", "blade_c", "pin", "Spacer lobes ride on the 4 long M2 bolts and are clamped between both Hardox discs", mechanical_key=True)
C("disc_f", "spacer", "pin", "Floating disc on the 4 long M2 through the spacer", mechanical_key=True)
C("base_panel", "tub", "screw", "Base panel in the floor recess, 5 M2 CSK into heat-set inserts")
C("top_armour", "tub", "snap", "TPU hood skirt snaps over the tub rim")
C("battery", "tub", "press_fit", "Pack between the side wall, the motor-bay wall and the front wall, hood above", interference_mm=0.1, mechanical_key=True)
C("rxesc", "tub", "interlock", "Malenki + BBB stack kapton-wrapped beside the pack, boxed by the walls and the hood")
C("wesc", "rxesc", "interlock", "BBB ESC kapton-wrapped onto the Malenki as one stacked brick")
C("wesc", "tub", "interlock", "ESC brick boxed in by the tub side wall, the battery, the front wall and the hood lip above")
C("power_switch", "tub", "press_fit", "Switch pressed into the rear-wall slot, 2 M2 on the housing", interference_mm=0.1)

ov = [dict(a="wshaft", b="wbearing", max_depth_mm=0.3, reason="5 mm prop-mount spigot runs in the MF85ZZ inner race (bearing modelled as one solid)")]
spec = dict(name="Revron", profile="aws2025", robot_type="vertical_spinner", locomotion="roller", archetype="vertical_spinner_forks",
            archetype_params={"blade_lead_mm": [-12, -5], "axle_height_mm": [21, 24], "disc_thickness_mm": [13, 15], "disc_dia_mm": [41, 45], "teeth": [2, 2],
                              "tub_height_mm": [13, 17], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25]},
            targets={"length_mm": 101, "width_mm": 104, "disc_dia_mm": 43, "wheel_dia_mm": 21.5, "tol_mm": 4,
                     "source": "RVRN reference CAD (research/rvrn_drive) measured in its assembly frame", "note": "drisk 3+8+3 on a BE1806; N10 direct to 21.5 rear wheels, O-rings to 11 mm fronts"},
            weapon_lock={"type": "removable_pin", "mode": "tooth_stop", "dia_mm": 3.0, "axis": [1, 0, 0], "holes": ["tub"], "at": [0.0, LOCK[0], LOCK[1]],
                         "note": "M3 pin through both chassis lugs at r19.1, inside the tip circle and outside the R16.5 rim: stops the teeth (RVRN has no lock model)"},
            parts=parts, fasteners=fast, wires=wires,
            modules=[{"id": "weapon_module", "root": "upright_l", "note": "RVRN quick-change weapon module: 4 M3 out, lifts forward off the chassis lugs",
                      "parts": [q["id"] for q in parts if chain_root(q) == "upright_l" and q["id"] != "upright_l"]}],
            electronics=dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2), can_run_inverted=False,
            allow_overlap=ov, connections=conn,
            claims=[dict(id="c_mass", text="weighs 150 g or less", metric="mass_total_g", op="<=", value=150),
                    dict(id="c_fit", text="fits the 150 mm square", metric="footprint_mm", op="<=", value=150)])
for k in ("reference_ratios",):
    spec[k] = json.load(open(f"/mnt/project-files/robot-cad/b123d/audit/revron_{k}.json"))
# Corrections from the reference CAD assembly frame (coordinator-approved 2026-10-18): the 21.5 mm F1 tyre is on the
# N10 shaft at the REAR (x_ref 97.85), the 11 mm micro tyre on the front standoff (x_ref 36.85); Scalextric "micro rear"
# / "F1 front" are tyre names, not positions. Photo-derived ratios that the CAD contradicts are re-measured from the CAD.
CAD_FIX = {
    "width_over_length": dict(value=1.03, tol=0.04, source="RVRN CAD: wedglet outer faces 104.1 (z_ref 0.52 mirrored) / 100.4 (disc tip x 8.22 to tyre x 108.59)"),
    "disc_dia_over_length": dict(value=0.425, tol=0.03, source="RVRN CAD: tips at R21.5 -> 43 / 101"),
    "axle_z_over_disc_dia": dict(value=0.52, tol=0.04, source="RVRN CAD: axle y_ref 26.6 - floor 4.25 = 22.35 / 43"),
    "rear_over_front_wheel_dia": dict(value=1.95, tol=0.1, source="RVRN CAD: F1 21.5 on the N10 at the rear, micro 11 on the front standoff"),
    "rotor_mass_fraction": dict(value=0.28, tol=0.03, source="RVRN CAD + BOM: 2 x 14.7 g Hardox discs, 1.7 g spacer, prop mount, 4 long M2 + nuts and half the 18.5 g BE1806 (its bell turns with the drisk) of 150 g; the 31 g photo figure counted the plates only"),
    "pod_h_over_tub_h": dict(num="part:wedglet_l.H", value=1.0, tol=0.15, source="RVRN CAD: low-profile wedglet / side panel 15 tall, chassis ~15"),
    "fork_span_over_width": dict(num="part:wedglet_*.W", value=1.0, tol=0.05, source="RVRN CAD: the two low-profile wedglets are the outermost parts (outer faces z_ref 0.52 and its mirror)"),
    "upright_symmetry": dict(value=1.106, tol=0.05, source="RVRN CAD: fl 31.23 tall vs fr 28.24 (the bearing-side plate is smaller)"),
}
for e in spec["reference_ratios"]:
    if e["name"] in CAD_FIX:
        e.update(CAD_FIX[e["name"]])
# Reference CAD comparison. All RVRN STLs share the RVRN assembly frame; REF_TO_WORLD maps it to ours, so each part is
# compared in place (silhouette IoU along X, Y and Z) as well as by its pose-free fingerprint. mirror_x: opposite hand.
REF_TO_WORLD = [[0, 0, -1, 52.57], [-1, 0, 0, 60.0], [0, 1, 0, -4.25], [0, 0, 0, 1]]
def RCE(part, file, mode="shape", **k): return dict(part=part, file=file, mode=mode, **k)
spec["reference_cad"] = {"dir": "/mnt/project-files/robot-cad/research/rvrn_drive", "ref_to_world": REF_TO_WORLD, "iou_min": 0.9, "parts": [
    RCE("blade_c", "RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL", tol_mm=0.5, tol_vol_frac=0.1, note="motor-side drisk disc 41.25 x 33 x 3"),
    RCE("disc_f", "RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL", mode="envelope", tol_mm=0.5, tol_vol_frac=0.35, ref_shift=[DF_X[0] - BL_X[0], 0, 0],
        outline_only=True, note="floating disc: the PT_10 outline one spacer along the axle, 23.5 bore clears the bell (no can-mount holes or pockets)"),
    RCE("spacer", "RVRN_1.7_PT_9_Drisk_Spacer-1.STL", tol_mm=0.5, note="printed drisk spacer 31.85 x 8"),
    RCE("upright_l", "fl-1.STL", tol_mm=0.8, tol_vol_frac=0.15, note="LH upright, 4 mm plate"),
    RCE("upright_r", "fr-1.STL", tol_mm=0.8, tol_vol_frac=0.15, note="RH upright, 4 mm plate"),
    RCE("base_panel", "RVRN_1.7_PT_8_Bottom_Panel-1.STL", tol_mm=0.8, tol_vol_frac=0.15, note="47.4 x 54.4 x 1 panel, 5 M2 CSK"),
    RCE("wedglet_l", "MirrorLow_profile_wedglet-2.STL", tol_mm=1.0, tol_vol_frac=0.15, note="TPU low-profile wedglet, left hand"),
    RCE("wedglet_r", "MirrorLow_profile_wedglet-2.STL", tol_mm=1.0, tol_vol_frac=0.15, mirror_x=True, note="TPU low-profile wedglet, right hand (mirror)"),
    RCE("whub_rl", "RVRN_1.7_PT_13_Rear_Wheel-2.STL", tol_mm=0.8, tol_vol_frac=0.25, note="printed rear wheel hub 16 x 12"),
    RCE("whub_fl", "Micro_slx_v1.0-2_Hub_Micro-1.STL", tol_mm=0.8, tol_vol_frac=0.3, note="micro hub 9 x 9"),
    RCE("prop_mount", "RVRN_1.7_C4_BE1806_Prop_Mount_Unmodified-1.STL", mode="envelope", tol_mm=0.5, tol_vol_frac=0.3, with_parts=["wshaft"], clip_to_ref=True,
        note="bought-in BE1806 prop mount: the 15 x 3 flange (prop_mount) plus its 5 mm spigot (modelled in wshaft, clipped to the reference span)"),
    RCE("battery", "RVRN_1.7_C7_Turnabot_180mah_2s-1.STL", mode="envelope", tol_mm=1.0, tol_vol_frac=0.15),
    RCE("wheel_fl", "Micro_slx_v1.0-2_11OD_7ID_6W_Micro_slx-1.STL", mode="envelope", tol_mm=0.5, tol_vol_frac=0.25),
    RCE("wheel_rr", "RVRN_1.7_C5_Scalextric_F1_Front_tyre-1.STL", mode="envelope", tol_mm=0.5, tol_vol_frac=0.25),
    RCE("motor_r", "RVRN_1.7_C1_Turnabot_Spicy_N10_2200_RPM-1.STL", mode="envelope", tol_mm=0.5, tol_vol_frac=0.3),
    RCE("weapon_motor", "RVRN_1.7_C2_BBB_BE1806_Rough_Motor_Model-1.STL", mode="envelope", tol_mm=1.0, tol_vol_frac=0.3),
    RCE("wbearing", "MF85ZZ_Budget_Metal_Shielded_Flanged_Deep_Groove_Ball_Bearing_5x8x2.5mm-1.STL", mode="envelope", tol_mm=0.3, tol_vol_frac=0.3),
]}
json.dump(spec, open(OUT, "w"), indent=1)
json.dump(spec, open(os.path.join(HERE, "..", "spec.json"), "w"), indent=1)
print("wrote", OUT, len(parts), "parts", len(fast), "fasteners")
