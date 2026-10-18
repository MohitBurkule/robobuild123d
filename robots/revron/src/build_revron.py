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
PM_X = (BL_X[0] - 2.0, BL_X[0])       # prop-mount clamp flange -9.1..-7.1
SH_X = (UR_OUT - 2.0, UL_IN + STATOR_RECESS)   # 5 mm rotor shaft -19.5..15.4
BR_X = (UR_IN - 1.9, UR_IN + 0.6)     # MF85ZZ: body in the plate, 0.6 flange proud of the inner face
DISC_R, TIP_R = 16.5, 21.5
BOLT_R, CAN_R, LIGHT_R = 14.0, 4.5, 9.46
A0 = 73.6                             # bolt-circle phase relative to the tooth tip direction (measured)
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
WG_OUT = 51.8                         # wedglet outer face (|X|)
WM_CB = 0.0                           # motor screw head counterbore depth

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
    for (y, z) in (SA, SB):
        cut.append(cylx(1.6, x0 - 1, x1 + 1, y, z))                             # 3.2 M3 clearance into the standoffs
    cut.append(yz(slot2((24.0, 9.75), (29.4, 5.75), 2.0), x0 - 1, x1 + 1))       # lightening slot over the standoffs
    if side == "l":
        cut.append(yz(chaikin([(20.6, 16.5), (25.9, 16.5), (23.85, 20.1)], 3), x0 - 1, x1 + 1))
        for dy, dz in ((0, 6), (0, -6), (8, 0), (-8, 0)):                       # BE1806 stator pattern 12 / 16
            cut.append(cylx(1.095, x0 - 1, x1 + 1, WY + dy, WZ + dz))
    else:
        cut.append(yz(chaikin([(19.6, 16.85), (25.6, 16.85), (23.5, 21.15)], 3), x0 - 1, x1 + 1))
    return S(body, *cut)


# ---------------------------------------------------------------- drisk
def disc_outline(phase):
    """Disc R16.5 with two tips at R21.5, 180 deg apart (RVRN drisk). Each tip is reached by a flank tangent to the disc
    (leaving it acos(16.5/21.5) ahead of the tip) and drops back by a short hook, filleted into the rim (>= kerf)."""
    pts = []
    g = math.degrees(math.acos(DISC_R / TIP_R))
    P_ = lambda r, a: (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))  # noqa: E731
    for k in (0, 1):
        aT = phase + 180.0 * k
        hook = chaikin_open([P_(TIP_R, aT), P_(19.9, aT - 2.0), P_(DISC_R, aT - 7.0), P_(DISC_R, aT - 9.0)], 6)
        pts += hook[:-1]
        pts += arc((0, 0), DISC_R, aT - 9.0, aT - 180.0 + g, 36)
    return r4(pts[::-1])


def disc_cuts(t, full=True):
    c = []
    for k in range(4):
        a = math.radians(A0 + 90 * k)
        c.append(cyl(1.095, t + 2, (BOLT_R * math.cos(a), BOLT_R * math.sin(a), 0)))
        if full:
            c.append(cyl(1.095, t + 2, (CAN_R * math.cos(a), CAN_R * math.sin(a), 0)))
            b = math.radians(A0 - 45 + 90 * k)
            c.append(cyl(4.13, t + 2, (LIGHT_R * math.cos(b), LIGHT_R * math.sin(b), 0)))
    c.append(cyl(2.99 if full else 11.75, t + 2))
    return c


def spacer_shape():
    lobes = []
    for k in range(4):
        a = math.radians(A0 + 90 * k)
        lobes.append(cyl(2.4, 8.0, (BOLT_R * math.cos(a), BOLT_R * math.sin(a), 0)))
        lobes.append(place({"type": "box", "size": [3.6, 4.8, 8.0]}, (12.5 * math.cos(a), 12.5 * math.sin(a), 0), (0, 0, math.degrees(a))))
    ring = cyl(13.13, 8.0)
    holes = [cyl(1.095, 10.0, (BOLT_R * math.cos(math.radians(A0 + 90 * k)), BOLT_R * math.sin(math.radians(A0 + 90 * k)), 0)) for k in range(4)]
    return S(U(ring, *lobes), cyl(11.635, 10.0), *holes)


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
        add.append(boxr(*sorted((s * (xi - 3.0), s * (xi - 0.05))), CY1 - 0.1, 18.0, 3.4, 15.0))        # inner cheek
        add.append(boxr(*sorted((s * (xi - 3.0), s * (xi - 0.05))), 9.6, 16.4, 14.9, 19.5))             # lock-pin ear
        add.append(boxr(*sorted((s * (xo + 0.05), s * (xo + 2.5))), CY1 - 0.1, 18.0, 3.4, 15.0))       # outer cheek
    # motor pockets (rear): front and rear stop walls either side of each N10
    for s in (1, -1):
        add.append(boxr(*sorted((s * 3.0, s * (CX - CW + 0.1))), RY + 5.25, RY + 6.45, FLOOR_Z1 - 0.1, RZ + 6.0))
        add.append(boxr(*sorted((s * 2.6, s * 3.6)), CY0 + CW - 0.1, RY + 6.4, FLOOR_Z1 - 0.1, RZ + 6.0))   # inner end stop
    # X rib + insert bosses
    L = math.hypot(2 * (CX - CW), RY + 6.4 - (CY1 - CW)); ang = math.degrees(math.atan2(RY + 6.4 - (CY1 - CW), 2 * (CX - CW)))
    for a in (ang, -ang):
        add.append(place({"type": "box", "size": [L - 1.0, 1.6, 2.0]}, (0, (RY + 6.4 + CY1 - CW) / 2, FLOOR_Z1), (0, 0, a)))
    for px, py in INS:
        add.append(cylz(2.6, FLOOR_Z0, FLOOR_Z1 + 3.5, px, py))
    for s in (1, -1):   # alu nut pockets
        add.append(boxr(*sorted((s * NUT_X0, s * (CX - CW + 0.1))), NUT_Y - 4.0, NUT_Y + 4.0, NUT_Z - 4.0, NUT_Z + 4.0))
    body = U(body, *add)
    body = S(body, cylx(1.6, -CX, CX, 13.0, 16.3))   # weapon-lock pin bore through both ears
    cut = []
    # floor: triangular pockets between the X ribs
    yc = (RY + 5 + CY1 - CW) / 2
    for tri in ([(-22, CY1 - CW - 3), (22, CY1 - CW - 3), (0, yc + 3)], [(-22, RY + 8.0), (22, RY + 8.0), (0, yc - 3)],
                [(-CX + CW + 2.5, CY1 - CW - 6), (-CX + CW + 2.5, RY + 11), (-4.0, yc)], [(CX - CW - 2.5, CY1 - CW - 6), (4.0, yc), (CX - CW - 2.5, RY + 11)]):
        cut.append(place({"type": "prism", "points": r4(chaikin(tri, 3)), "height": 3.0}, (0, 0, FLOOR_Z1 - 0.5)))
    for s in (1, -1):
        cut.append(boxr(*sorted((s * 3.6, s * (CX - CW + 0.05))), CY0 + CW - 0.05, RY + 5.0, FLOOR_Z0 - 2, FLOOR_Z1 + 0.05))   # motor bays open to the panel
        cut.append(cylx(1.7, *sorted((s * (CX - CW - 0.5), s * (CX + 0.5))), RY, RZ))                     # N10 shaft bushing hole
        cut.append(boxr(*sorted((s * (CX - CW - 0.5), s * (CX + 0.5))), RY - 1.7, RY + 1.7, FLOOR_Z0 - 2, RZ))   # keyhole slot down to the base panel
        cut.append(cylx(1.6, *sorted((s * (NUT_X0 - 0.5), s * (CX + 0.5))), NUT_Y, NUT_Z))               # M3 clearance
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
    t = 1.2
    top = boxr(-CX, CX, CY0, CY1, HOOD_Z - t, HOOD_Z)
    posts = [boxr(-CX, CX, y - 1.5, y + 1.5, CZ1, HOOD_Z - t + 0.01) for y in (CY0 + 0.75, CY1 - 0.75)]
    li = CX - CW - 0.1
    skirt = S(boxr(-li, li, CY0 + CW + 0.1, CY1 - CW - 0.1, CZ1 - 1.3, HOOD_Z - t + 0.01),
              boxr(-li + 1.2, li - 1.2, CY0 + CW + 1.3, CY1 - CW - 1.3, CZ1 - 3.0, HOOD_Z))
    body = U(top, skirt, *posts)
    cut = []
    for s in (1, -1):
        for tri in ([(4, -6), (22, -6), (4, -24)], [(22, -10), (22, -28), (6, -28)], [(4, 2), (22, 2), (22, -3)]):
            q = [(s * a, b) for a, b in tri]
            q = q if s > 0 else q[::-1]
            cut.append(place({"type": "prism", "points": r4(chaikin(q, 2)), "height": 4.0}, (0, 0, HOOD_Z - t / 2)))
    return S(body, *cut)


# ---------------------------------------------------------------- wedglet + side panel (TPU, one piece per side)
def wedglet(s):
    """RVRN low-profile TPU wedglet (one piece per side, 90 long): a full-width nose ramp, a split block that slides over
    both front standoffs, an open bay for the front wheel, an outer block that takes the axle-standoff screw, a tall side
    rail beside the chassis with a low skirt, a transverse wall ahead of the rear wheel and a rear rail outboard of it
    with a window. Outline and heights measured from the RVRN CAD (never imported). Built for the left side, mirrored."""
    Z0 = 0.87
    def bx(x0, x1, y0, y1, z1, z0=Z0): return boxr(x0, x1, y0, y1, z0, z1)
    parts_ = [
        yz([(30.4, Z0), (42.75, Z0), (42.75, 1.5), (31.0, 14.5), (30.4, 14.5)], 17.5, 33.5),           # nose, inner (tall) half
        yz([(29.65, Z0), (42.75, Z0), (42.75, 1.5), (36.0, 9.87), (29.65, 9.87)], 33.5, 44.5),         # nose, outer half
        bx(44.5, 51.5, 12.0, 30.0, 2.4),                                                                # outer lip
        yz([(19.2, Z0), (30.5, Z0), (30.5, 15.2), (19.2, 8.0)], 21.0, 24.5),                            # standoff block, inner cheek
        yz([(19.2, Z0), (30.5, Z0), (30.5, 15.2), (19.2, 8.0)], 25.5, 29.0),                            # standoff block, outer cheek
        bx(24.4, 25.6, 19.2, 30.5, 3.0),                                                                # web under the split
        bx(42.0, 47.5, 6.5, 29.65, 9.87),                                                               # outer block (axle screw)
        cylx(4.0, 40.0, 42.1, SB[0], SB[1]),                                                            # boss bearing on the axle-standoff end
        bx(36.0, 42.1, 6.5, 15.0, 9.87),                                                                # rail-to-outer-block knee
        yz([(-21.5, Z0), (10.4, Z0), (10.4, 12.0), (-21.5, 15.87)], 33.0, 36.0),                        # side rail (beside the chassis)
        bx(36.0, 44.0, -21.0, 6.5, 2.4),                                                                # skirt
        bx(33.0, 48.0, -25.0, -22.0, 15.87),                                                            # transverse wall ahead of the rear wheel
        bx(44.5, 47.0, -47.7, -25.0, 15.87),                                                            # rear rail
        bx(47.0, 50.5, -47.7, -25.0, 8.86),                                                             # rear rail step
    ]
    body = U(*parts_)
    cut = []
    cut.append(cylx(2.6, 17.0, SA_END, SA[0], SA[1]))                       # bore over the nose standoff (0.1 a side)
    cut.append(cylx(1.6, SA_END - 0.5, 45.0, SA[0], SA[1]))                  # M3 clearance (head on the nose's outer face)
    cut.append(cylx(2.6, 17.0, SB_END, SB[0], SB[1]))                       # bore over the axle standoff
    cut.append(cylx(1.6, SB_END - 0.5, 48.0, SB[0], SB[1]))
    cut.append(cylx(3.1, SB_END + 1.5, 48.0, SB[0], SB[1]))                  # head seat in the outer block
    cut.append(yz(rrect(27.72, 30.71, 4.15, 8.26, 1.0), 20.0, 30.0))         # lightening hole between the bores
    cut.append(cylx(1.6, 32.0, 37.0, NUT_Y, NUT_Z))                          # rear screw into the chassis nut
    cut.append(yz(rrect(-46.6, -31.8, 4.95, 14.78, 2.5), 44.0, 48.0))        # window over the rear wheel
    sh = S(body, *cut)
    return sh if s > 0 else {"type": "mirror", "shape": sh, "axis": "x"}


# ---------------------------------------------------------------- wheels
def rear_hub():   # RV21, local x 0 = inner face: O-ring groove (1.0 flanges), then the 12 mm F1 tyre seat with a retaining ridge
    prof = [(1.5, 0.0), (8.0, 0.0), (8.0, 1.0), (7.0, 1.0), (7.0, 2.2), (8.0, 2.2), (8.0, 3.2), (6.0, 3.2), (6.0, 6.2), (6.15, 6.5), (6.15, 9.2),
            (6.0, 9.5), (6.0, 12.7), (1.5, 12.7)]
    sh = place({"type": "revolve", "profile": r4(prof)}, (0, 0, 0), (0, 90, 0))
    return S(sh, place({"type": "cylinder", "radius": 1.0, "height": 10.0}, (7.5, 0, 3.5), (0, 0, 0)))   # M2 grub-screw hole


RH_TYRE = 2.5     # tyre inner face (hub-local)
FH_TYRE = 3.2


def front_hub():  # RV19 9 mm micro hub on the 5 mm standoff: O-ring groove inboard, 7 mm tyre seat
    prof = [(2.6, 0.0), (4.5, 0.0), (4.5, 1.0), (3.5, 1.0), (3.5, 2.2), (4.5, 2.2), (4.5, 3.2), (3.6, 3.2), (3.6, 9.2), (2.6, 9.2)]
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
P(id="top_armour", kind="armor", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#c8ccd2", shape=hood(),
  label="raised TPU hood with triangle cut-outs, snaps over the tub rim")

# weapon module: both uprights, the 4 standoffs, motor and drisk lift out together once the 2 wedglet screws per side are out
P(id="upright_l", kind="structure", print_orientation="+x", rotates_with="fixed", solid_fraction=1.0, color="#2a2c30", shape=upright("l"), **PLA,
  label="RV02 4 mm printed plate: BE1806 stator bolted to it (4 M2, 12/16 pattern), notch seats on the chassis lug, 2 M3 into the standoffs")
P(id="upright_r", kind="structure", parent="upright_l", print_orientation="+x", rotates_with="fixed", solid_fraction=1.0, color="#2a2c30", shape=upright("r"), **PLA,
  label="RV03 4 mm printed plate: MF85ZZ seat for the prop-mount spigot, notch on the chassis lug, 2 M3 into the standoffs")
for s, n in ((1, "l"), (-1, "r")):
    xi = UL_OUT if s > 0 else UR_OUT
    for nm, (y, z), L in (("a", SA, SA_LEN), ("b", SB, SB_LEN)):
        P(id=f"so_{nm}{n}", kind="pin", role="standoff", material="aluminium", process="cots", parent="upright_l", rotates_with="fixed", color="#b8bcc2",
          stock=f"M3 x {L:g} mm aluminium standoff, 5 mm OD", shape=S(cylx(SO_R, *sorted((xi, s * (abs(xi) + L))), y, z), cylx(1.25, *sorted((s * (abs(xi) - 1), s * (abs(xi) + L + 1))), y, z)),
          label=f"{L:g} mm M3 alu standoff (5 OD): clamps the upright" + (" and is the greased front axle" if nm == "b" else "") + "; the wedglet slides over it")
P(id="weapon_motor", kind="weapon_motor", catalog="be1806_bbb", exposed=True,
  exposed_reason="Drisk: the BE1806 bell is the hub of the weapon and turns inside the spacer between the two Hardox discs, as on the real RVRN; the discs (R16.5-21.5) shield it radially", parent="upright_l", at=[MOT_X, WY, WZ], rot=[90, 0, 180], rotates_with="fixed",
  label="BBB BE1806 2300 kV: stator bolted to the left upright, the bell turns with the drisk")
P(id="blade_c", kind="weapon", material="hardox", process="laser", stock="3 mm Hardox 450", secondary_ops=["drilled"], organic=True, rotates_with="weapon",
  shape=S(place({"type": "prism", "points": disc_outline(PHASE), "height": DT}, (0, 0, 0)), *disc_cuts(DT)),
  at=[BLM, WY, WZ], rot=[0, 90, 0], parent="upright_l",
  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [CAN_TOP - 0.5, WY, WZ], "min": 0, "max": 360, "default": 0}, color="#d9dde2",
  weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2},
  label="RV10 drisk disc, motor side: 3 mm Hardox, R16.5 with two tips at R21.5, 6 mm bore, 4 M2 on r4.5 (bell), 4 M2 on r14 (stack), 4 x 8.3 lightening")
P(id="disc_f", kind="other", role="blade", material="hardox", process="laser", stock="3 mm Hardox 450", secondary_ops=["drilled"], rotates_with="weapon",
  shape=S(place({"type": "prism", "points": disc_outline(PHASE), "height": DT}, (0, 0, 0)), *disc_cuts(DT, full=False)),
  parent="blade_c", at=[0, 0, (DF_X[0] + DF_X[1]) / 2 - BLM], rot=[0, 0, 0], color="#d9dde2",
  label="RV11 floating drisk disc: same 3 mm Hardox profile, 23.5 bore clears the bell, held by the 4 long M2")
P(id="spacer", kind="other", role="spacer", rotates_with="weapon", print_orientation="+z", parent="blade_c", at=[0, 0, (SP_X[0] + SP_X[1]) / 2 - BLM], rot=[0, 0, 0],
  shape=spacer_shape(), color="#2a2c30", **PLA, label="RV04 8 mm printed drisk spacer round the bell (ID 23.27), 4 lobes for the long M2")
P(id="prop_mount", kind="other", role="hub", material="aluminium", process="turned", rotates_with="weapon", parent="blade_c", at=MF_AT, rot=MF_ROT,
  shape=S(cylx(7.5, PM_X[0], PM_X[1], WY, WZ), cylx(2.5, PM_X[0] - 1, PM_X[1] + 1, WY, WZ),
          *[cylx(1.095, PM_X[0] - 1, PM_X[1] + 1, *wyz(A0 + 90 * k, CAN_R)) for k in range(4)]),
  secondary_ops=["drilled"], color="#9aa0a6", label="RV07 BE1806 prop-mount flange (15 mm): clamps the motor-side disc to the bell with 4 M2, collet on the 5 mm shaft")
P(id="wshaft", kind="shaft", material="steel", process="cots", stock="5 mm silver steel rod", rotates_with="weapon", shaft_of="weapon_motor", parent="blade_c",
  at=MF_AT, rot=MF_ROT, shape=cylx(2.49, SH_X[0], SH_X[1], WY, WZ), color="#777777",
  label="BE1806 5 mm rotor shaft, run through the bell into the MF85ZZ in the right upright (circlip at the stator back)")
P(id="wbearing", kind="bearing", parent="upright_r", material="steel", process="cots", rotates_with="fixed", stock="MF85ZZ", color="#555555",
  shape=S(U(cylx(4.0, BR_X[0], UR_IN, WY, WZ), cylx(4.6, UR_IN, BR_X[1], WY, WZ)), cylx(2.5, BR_X[0] - 1, BR_X[1] + 1, WY, WZ)),
  label="MF85ZZ 5 x 8 x 2.5 flanged, pressed into the right upright from the inside")
for k in range(4):
    dy, dz = yz_of(A0 + 90 * k, BOLT_R)
    px = BL_X[0] - 0.8
    P(id=f"nut_w{k}", kind="nut", catalog="nut_m2", parent="blade_c", at=[-dz, dy, px - BLM], rot=[0, 0, 0], rotates_with="weapon",
      label="M2 nut on the fixed-disc side, Loctite 243")

for s, n in ((1, "l"), (-1, "r")):
    rot = [0, 0, 0] if s > 0 else [0, 0, 180]
    P(id=f"motor_{n}", kind="motor", catalog="n10_2200rpm_spicy", at=[s * MOTX, RY, RZ], rot=rot, rotates_with="fixed")
    hl = RH_X[0] - MOTX
    P(id=f"whub_r{n}", kind="pulley", rotates_with=f"wheel_r{n}", print_orientation="+x", shape=rear_hub(), at=[hl, 0, 0], parent=f"motor_{n}",
      joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [hl + 6.0, 0, 0], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
      label="RV21 printed rear hub 16 x 12 pressed on the N10 D-shaft, O-ring groove inboard, M2 grub screw")
    P(id=f"wheel_r{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_r{n}", rotates_with=f"wheel_r{n}", parent=f"whub_r{n}", at=[FH_TYRE, 0, 0],
      shape=tyre(21.5, 12.0, 9.5), color="#1b1b1b", stock="Scalextric F1 front tyre 21.5 x 12 x 9.5", label="Scalextric F1 tyre 21.5 x 12 x 9.5")
    so = f"so_b{n}"
    P(id=f"whub_f{n}", kind="pulley", rotates_with=f"wheel_f{n}", print_orientation="+x", shape=front_hub(), at=[s * FH_X[0], SB[0], SB[1]], rot=rot, parent=so,
      joint={"kind": "revolute", "axis": [s, 0, 0], "pivot": [s * (FH_X[0] + 4.5), SB[0], SB[1]], "min": 0, "max": 360, "default": 0}, color="#333333", **PLA,
      label="RV19 printed front hub 9 x 9 with O-ring groove, runs greased on the 5 mm standoff (no bearing)")
    P(id=f"wheel_f{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_f{n}", rotates_with=f"wheel_f{n}", parent=f"whub_f{n}", at=[FH_TYRE, 0, 0],
      shape=tyre(FW_OD, FW_ID, FW_W), color="#1b1b1b", stock="Scalextric Micro SLX tyre 11 x 7 x 6", label="Scalextric micro tyre 11 x 7 x 6")
    P(id=f"spike_{n}", kind="fork", parent=f"so_a{n}", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#c8102e", shape=wedglet(s),
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
    F(id=f"bolt_b{i}", designation="M2x6", at=[x, y, BP["z0"]], dir=[0, 0, 1], through=["base_panel", "tub"], threads_into=f"insert_b{i}", head="countersunk")
for k, (dy, dz) in enumerate(((8, 0), (-8, 0), (0, 6), (0, -6))):
    F(id=f"bolt_wm{k}", designation="M2x6", at=[UL_OUT - WM_CB, WY + dy, WZ + dz], dir=[-1, 0, 0], through=["upright_l"], threads_into="weapon_motor")
for s, n in ((1, "l"), (-1, "r")):
    xi = UL_IN if s > 0 else UR_IN
    up = "upright_l" if s > 0 else "upright_r"
    for nm, (y, z), e in (("a", SA, SA_END), ("b", SB, SB_END)):
        F(id=f"bolt_u{n}{nm}", designation="M3x10", material="aluminium", at=[xi, y, z], dir=[s, 0, 0], through=[up], threads_into=f"so_{nm}{n}", tool="hex2.5",
          **({} if s > 0 else dict(access_before=["blade_c", "disc_f", "spacer"], reason="Right upright and its two standoffs are screwed together on the bench before the plate goes onto the shaft")))
        F(id=f"bolt_s{n}{nm}", designation="M3x10" if nm == "a" else "M3x8", material="aluminium", at=[s * (44.5 if nm == "a" else e + 1.5), y, z], dir=[-s, 0, 0], through=[f"spike_{n}"], threads_into=f"so_{nm}{n}", tool="hex2.5",
          reason="Wedglet bore slides over the standoff (takes the shear); the CSK screw along the standoff axis clamps it to the end face")
    F(id=f"bolt_s{n}c", designation="M3x12", material="aluminium", at=[s * 36.0, NUT_Y, NUT_Z], dir=[-s, 0, 0], through=[f"spike_{n}", "tub"], threads_into=f"nut_c{n}", tool="hex2.5")
for k in range(4):
    dy, dz = yz_of(A0 + 90 * k, BOLT_R)
    F(id=f"bolt_d{k}", designation="M2x16", at=[DF_X[1], WY + dy, WZ + dz], dir=[-1, 0, 0], through=["disc_f", "spacer", "blade_c"], threads_into=f"nut_w{k}",
      access_before=["upright_l", "weapon_motor", "spike_l", "so_al", "so_bl"], reason="The drisk stack is bolted up on the bench before it goes onto the motor bell (guide step 1)")
    dy, dz = yz_of(A0 + 90 * k, CAN_R)
    F(id=f"bolt_p{k}", designation="M2x8", at=[PM_X[0], WY + dy, WZ + dz], dir=[1, 0, 0], through=["prop_mount", "blade_c"], threads_into="weapon_motor",
      access_before=["upright_r", "wbearing"],
      reason="Driven on the bench when the drisk is built onto the motor (guide step 2), before the right upright and its bearing go on")

# O-ring belts: rear hub groove -> front hub groove, one per side
BX = (31.0, 32.2)
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
        C(f"so_{nm}{n}", f"spike_{n}", "screw", "Wedglet slides over the standoff and is screwed to its outer end (M3 CSK alu)", mechanical_key=True)
    C(f"belt_{n}", f"whub_r{n}", "interlock", "O-ring in the rear hub groove under 10 % stretch")
    C(f"belt_{n}", f"whub_f{n}", "interlock", "O-ring in the front hub groove; drives the front wheel")
    C(f"spike_{n}", "tub", "screw", "Wedglet / side panel screwed to the chassis side wall into a press-fit alu M3 nut")
    C(f"nut_c{n}", "tub", "press_fit", "Alu M3 nut pressed into the hex pocket inside the side wall", interference_mm=0.1, mechanical_key=True)
    C(up, "tub", "interlock", "Upright notch seats over the chassis lug between two cheeks; the standoffs and wedglet screws lock it", mechanical_key=True)
C("weapon_motor", "upright_l", "screw", "Stator base bolted to the left upright with 4 M2 (12 / 16 mm pattern)")
C("blade_c", "weapon_motor", "screw", "Motor-side disc clamped to the bell by the prop-mount flange and 4 M2 into the bell: the bell drives the drisk", mechanical_key=True)
C("prop_mount", "blade_c", "screw", "Prop-mount flange clamps the disc to the bell, 4 M2", mechanical_key=True)
C("wshaft", "wbearing", "shaft", "5 mm shaft in the MF85ZZ inner race: the second support of the drisk")
C("wshaft", "weapon_motor", "press_fit", "The motor's own rotor shaft, pressed in the bell and held by its circlip behind the stator", interference_mm=0.02, mechanical_key=True)
C("prop_mount", "wshaft", "press_fit", "Prop-mount collet clamped on the 5 mm shaft", interference_mm=0.02, mechanical_key=True)
C("wbearing", "upright_r", "press_fit", "MF85ZZ pressed into the 7.98 seat, flange on the inner face", interference_mm=0.02, mechanical_key=True)
C("spacer", "blade_c", "pin", "Spacer lobes ride on the 4 long M2 bolts and are clamped between both Hardox discs", mechanical_key=True)
C("disc_f", "spacer", "pin", "Floating disc on the 4 long M2 through the spacer", mechanical_key=True)
for k in range(4):
    C(f"nut_w{k}", "blade_c", "interlock", "M2 nut on the long bolt against the fixed disc, Loctite 243")
C("base_panel", "tub", "screw", "Base panel in the floor recess, 5 M2 CSK into heat-set inserts")
C("top_armour", "tub", "snap", "TPU hood skirt snaps over the tub rim")
C("battery", "tub", "press_fit", "Pack between the side wall, the motor-bay wall and the front wall, hood above", interference_mm=0.1, mechanical_key=True)
C("rxesc", "tub", "interlock", "Malenki + BBB stack kapton-wrapped beside the pack, boxed by the walls and the hood")
C("wesc", "rxesc", "interlock", "BBB ESC kapton-wrapped onto the Malenki as one stacked brick")
C("wesc", "tub", "interlock", "ESC brick boxed in by the tub side wall, the battery, the front wall and the hood lip above")
C("power_switch", "tub", "press_fit", "Switch pressed into the rear-wall slot, 2 M2 on the housing", interference_mm=0.1)

ov = [dict(a="wshaft", b="wbearing", max_depth_mm=0.3, reason="5 mm shaft runs in the MF85ZZ inner race (bearing modelled as one solid)")]
spec = dict(name="Revron", profile="aws2025", robot_type="vertical_spinner", locomotion="roller", archetype="vertical_spinner_forks",
            archetype_params={"blade_lead_mm": [-12, -5], "axle_height_mm": [21, 24], "disc_thickness_mm": [13, 15], "disc_dia_mm": [41, 45], "teeth": [2, 2],
                              "tub_height_mm": [13, 17], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25]},
            targets={"length_mm": 101, "width_mm": 104, "disc_dia_mm": 43, "wheel_dia_mm": 21.5, "tol_mm": 4,
                     "source": "RVRN reference CAD (research/rvrn_drive) measured in its assembly frame", "note": "drisk 3+8+3 on a BE1806; N10 direct to 21.5 rear wheels, O-rings to 11 mm fronts"},
            weapon_lock={"type": "removable_pin", "mode": "tooth_stop", "dia_mm": 3.0, "axis": [1, 0, 0], "holes": ["tub"], "at": [0.0, 13.0, 16.3],
                         "note": "M3 pin through both tub cheeks inside the tip circle; stops the teeth (RVRN has no lock model)"},
            parts=parts, fasteners=fast, wires=wires,
            electronics=dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2), can_run_inverted=False,
            allow_overlap=ov, connections=conn,
            claims=[dict(id="c_mass", text="weighs 150 g or less", metric="mass_total_g", op="<=", value=150),
                    dict(id="c_fit", text="fits the 150 mm square", metric="footprint_mm", op="<=", value=150)])
for k in ("reference_ratios", "reference_cad"):
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
    "pod_h_over_tub_h": dict(num="part:spike_l.H", value=1.0, tol=0.15, source="RVRN CAD: low-profile wedglet / side panel 15 tall, chassis ~15"),
}
for e in spec["reference_ratios"]:
    if e["name"] in CAD_FIX:
        e.update(CAD_FIX[e["name"]])
for e in spec["reference_cad"]["parts"]:
    if e["part"] == "wheel_fl": e["file"] = "Micro_slx_v1.0-2_11OD_7ID_6W_Micro_slx-1.STL"
    elif e["part"] == "wheel_rl": e["file"] = "RVRN_1.7_C5_Scalextric_F1_Front_tyre-1.STL"
json.dump(spec, open(OUT, "w"), indent=1)
json.dump(spec, open(os.path.join(HERE, "..", "spec.json"), "w"), indent=1)
print("wrote", OUT, len(parts), "parts", len(fast), "fasteners")
