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




# ---------------------------------------------------------------- layout (params.json)
TYRE_OD = pv("tyre_od", 21.5); RT = TYRE_OD / 2
TYRE_W = pv("tyre_width", 9.5)
HUB_R = pv("hub_od_belted", 16.0) / 2 - 0.5      # tyre seat radius under the 16 mm pulley rim
AXZ = pv("axle_z", 8.5)                           # wheel axle above chassis underside
WB = pv("wheelbase", 52.4) - 3.5; YF, YR = pv("wheelbase", 52.4) / 2, pv("wheelbase", 52.4) / 2 - WB   # rear axle 3.5 mm forward of SVRN to match the Revron side photo
FLOOR = AXZ - RT                                  # tyre contact plane (= -2.25)
CH = pv("chassis_height", 17.0)
DECK = 1.0                                        # params chassis_top_deck_t 1.2; 1.0 under the Ti plate to make weight
WALL = 1.0                                        # 2.0 in SVRN; 1.6 to make weight with the bigger weapon
CX = 30.5                                         # chassis half width (SVRN 65 -> 61 so the belted hubs clear the wall)
CY0, CY1 = -29.5, 33.5                       # box 3.5 mm shorter than SVRN (Revron photo)
FWALL = 2.1                                       # front wall (gearbox stop)
BP_T = pv("base_panel_t", 2.5); BP_Z0 = pv("base_panel_z", -0.5)
TP_T = 0.5                                        # Ti top plate (0.8-1.0 in SVRN; 0.5 Ti grade 5 for weight)
TP_X, TP_Y = 27.5, 18.5
PUL_W = 3.5                                       # pulley width (1.5 mm O-ring groove + 1 mm walls)
HUB_X0 = CX + 1.15                                # inner face of every hub (1.15 running gap to the wall)
TYRE_X0 = HUB_X0 + PUL_W + 0.25
HUB_L = PUL_W + 0.25 + TYRE_W                     # hub length
HUB_X1 = HUB_X0 + HUB_L
POD_T = 1.2
POD_X0, POD_X1 = HUB_X1 + 1.1, HUB_X1 + 1.1 + POD_T   # TPU side panel outer wall
MOT_L = 21.1; MOT_SH = 9.0                        # n10 catalog: body 21.1, shaft 9
MOT_CX = CX - WALL - MOT_L / 2                    # gearbox face against the side wall
# weapon (motor-local x: stator face -7, bell to +7, stub 6..14)
DISC_R = pv("weapon_disc_dia", 40.0) / 2
ZW = FLOOR + pv("weapon_axle_z", 23.0)            # axle 23 above the floor
YW = 53.8
BT_C, BT_O = pv("weapon_blade_t", 2.0), 0.0       # single 2 mm tooth plate; the 2 x 1 mm outer rings were dropped to pay for the 350 mAh pack
BLO = (8.2, 8.2 + BT_O)                           # blade stack, motor-local x
BLC = (BLO[1], BLO[1] + BT_C)
BLI = (BLC[1], BLC[1] + BT_O)
SP_H0, SP_F0 = 7.5, BLI[1]                        # spider hub start, flange inner face
SP_H1 = SP_F0 + 1.5                               # flange outer face
HEAD_T = 1.4                                      # ISO7380 M2.5 head
NUT0 = BLO[0] - 1.8                               # round nut on the outer ring
WX0 = -(BLO[0] + BLI[1]) / 2                      # motor centre x: blade stack centred on x = 0
RING_I, RING_O, BOLT_R = 10.0, 17.6, 13.1
SH0 = -8.0                                        # motor shaft extended out of the stator back (local)
UL0L = SP_H1 + HEAD_T + 2.15                      # left upright inner face (local)
SH0, SH1 = 0.5, UL0L + 3.0   # tail runs through the stator into a clearance bore in the right upright                       # motor's own shaft, extended into the F683 in the left upright
# uprights / bosses (world)
UR0, UR1 = WX0 - 12.0, WX0 - 7.0                  # right upright (stator side)
UL0 = round(WX0 + UL0L, 2); UL1 = UL0 + 5.0             # left upright (bearing side)
BOSS_R = (UR0 - 6.5, UR0); BOSS_L = (UL1, UL1 + 6.5)
TAB_R = (BOSS_R[0], UR0); TAB_L = (UL1, BOSS_L[1])
BY0, BY1 = 34.3, 46.0
CHIN_Y1, CHIN_Z1 = 41.0, 4.0
NOSE_Z = 15.3                                     # front of the long sloped deck (TPU wedge cover sits on it)
SL0 = 20.0                                        # deck slope starts just ahead of the Ti plate


def zdeck(y):
    return CH if y <= SL0 else CH - (CH - NOSE_Z) * (y - SL0) / (CY1 - SL0)
TAB_Z0, TAB_Z1 = 14.0, 17.0

parts = []
def P(**k): parts.append(k)

POSTS = [(25.0, 16.0), (-25.0, 16.0), (25.0, -16.0), (-25.0, -16.0), (0.0, -24.9)]
TOP_POSTS = POSTS[:4]
BASE_PTS = [POSTS[0], POSTS[3], POSTS[4]]           # 3 base screws in a triangle
POD_Y = (4.0, 10.0); POD_Z = 8.25; POD_WY = (1.0, 13.0)
SW_Y, SW_Z = -6.6, 8.5
BAT_Y = -12.0
INS_B_Z = BP_Z0 + BP_T + 1.5                      # base inserts 2..5
INS_T_Z = CH - 1.5                         # top inserts 12.8..15.8
INS_U_Z = TAB_Z0 - 1.5
INS_P_X = CX - 1.5                         # pod inserts (axis x) 25.9..28.9
FORK_X = (5.0, 9.5)
FORK_HX = 3.5                                     # fork root screws at x = +-2.5
FORK_TIP = YW + DISC_R + 4.0
SPK_Y = (57.0,); SPK_Z = 1.5                       # spike-fork bolt through the pod front corner                 # spike-fork bolts through the pod front corner


# ---------------------------------------------------------------- chassis (printed nylon tub, open bottom)
def chassis():
    prof = [(CY0, 0), (CY1, 0), (CY1, NOSE_Z), (SL0, CH), (CY0, CH)]
    inner = [(CY0 + WALL, -1), (CY1 - FWALL, -1), (CY1 - FWALL, zdeck(CY1 - FWALL) - DECK), (SL0, CH - DECK), (CY0 + WALL, CH - DECK)]
    shell = S(yz(prof, -CX, CX), yz(inner, -(CX - WALL), CX - WALL))
    add = []
    for x, y in POSTS:
        add.append(cylz(2.75, BP_Z0 + BP_T, CH - DECK + 0.1, x, y))
        if abs(x) > 1:   # web from the post to the side wall
            s = 1 if x > 0 else -1
            add.append(boxr(*sorted((s * (abs(x) + 1.5), s * (CX - WALL + 0.1))), y - 0.8, y + 0.8, BP_Z0 + BP_T, CH - DECK + 0.1))
        else:
            add.append(boxr(-0.8, 0.8, CY0 + WALL - 0.1, y - 1.5, BP_Z0 + BP_T, CH - DECK + 0.1))
    for s in (1, -1):
        add.append(boxr(*sorted((s * (CX - WALL - 4.6), s * (CX - WALL + 0.1))), POD_Y[0] - 3.0, POD_Y[1] + 3.0, POD_Z - 3.2, POD_Z + 3.2))   # insert boss
        add.append(cylx(3.0, *sorted((s * (CX - WALL - 2.4), s * (CX - WALL + 0.1))), YR, AXZ))     # rear axle boss
        # motor clamp ribs from the deck down to the gearbox top
        add.append(yz([(YF - 6.0, AXZ + 6.0), (YF - 5.0, AXZ + 6.0), (YF - 5.0, zdeck(YF - 5.0) - DECK + 0.1), (YF - 6.0, zdeck(YF - 6.0) - DECK + 0.1)], *sorted((s * (MOT_CX - 8.0), s * (MOT_CX + 8.0)))))
        add.append(yz([(YF - 4.0, AXZ + 6.0), (YF + 4.0, AXZ + 6.0), (YF + 4.0, zdeck(YF + 4.0) - DECK + 0.1), (YF - 4.0, zdeck(YF - 4.0) - DECK + 0.1)], *sorted((s * (MOT_CX - 6.0), s * (MOT_CX + 6.0)))))   # top clamp pad, follows the sloped deck
    add.append(boxr(BOSS_R[0], BOSS_L[1], CY1 - 0.1, CHIN_Y1, 0.0, CHIN_Z1))       # chin
    for b0, b1 in (BOSS_R, BOSS_L):
        add.append(boxr(b0, b1, CY1 - 0.1, BY1, 0.0, TAB_Z0))                       # square upright bosses
    for s_ in (1, -1):   # inner corner fillets behind the top facets
        tri = [(s_ * (CX - WALL + 0.05), CH - DECK + 0.05), (s_ * (CX - WALL - 1.6), CH - DECK + 0.05), (s_ * (CX - WALL + 0.05), CH - DECK - 1.6)]
        add.append(place({"type": "prism", "points": r4(tri if s_ < 0 else list(reversed(tri))), "height": SL0 - CY0 - 1}, (0, (CY0 + 1 + SL0) / 2, 0), (90, 0, 0)))
    add.append(yz([(CY0 + WALL - 0.05, CH - DECK + 0.05), (CY0 + WALL - 0.05, CH - DECK - 1.6), (CY0 + WALL + 1.6, CH - DECK + 0.05)], -CX + 1, CX - 1))
    body = U(shell, *add)
    cut = []
    for s in (1, -1):
        cut.append(cylx(2.1, *sorted((s * (CX - WALL - 0.5), s * (CX + 0.5))), YF, AXZ))              # gearbox-boss keyhole
        cut.append(boxr(*sorted((s * (CX - WALL - 0.5), s * (CX + 0.5))), YF - 2.1, YF + 2.1, -1.0, AXZ))   # open below: the motor drops in from underneath
        cut.append(cylx(1.5, *sorted((s * (CX - WALL - 2.5), s * (CX + 0.5))), YR, AXZ))              # rear axle press hole
        for y in POD_Y:
            cut.append(cylx(1.0, *sorted((s * (CX - WALL - 5.2), s * (CX + 0.5))), y, POD_Z))         # M2 pilot (through)
            cut.append(cylx(1.6, *sorted((s * (INS_P_X - 1.55), s * (CX + 0.5))), y, POD_Z))   # insert bore, pressed in from outside through the wall
            cut.append(cylx(1.15, *sorted((s * (CX - WALL - 0.1), s * (CX + 0.5))), y, POD_Z))        # wall clearance
    for x, y in POSTS:
        cut.append(cylz(1.6, INS_B_Z - 1.5 - 0.01, INS_B_Z + 1.5, x, y)); cut.append(cylz(1.0, INS_B_Z, INS_B_Z + 3.0, x, y))
    for x, y in TOP_POSTS:
        cut.append(cylz(1.6, INS_T_Z - 1.5, CH + 0.5, x, y)); cut.append(cylz(1.0, INS_T_Z - 5.0, INS_T_Z, x, y))
        cut.append(cylz(1.15, CH - DECK - 0.1, CH + 0.5, x, y))
    for (b0, b1) in (BOSS_R, BOSS_L):
        bx = (b0 + b1) / 2
        cut.append(boxr(b0 + 1.4, b1 - 1.4, BY0 + 1.4, BY1 - 1.4, -0.5, UB_Z - 2.5))          # hollow boss, open below
        for y in UB_Y:
            cut.append(cylx(1.1, b0 - 0.5, b1 + 0.5, y, UB_Z))
    cut.append(boxr(-CX - 0.5, -CX + WALL + 0.5, SW_Y - 6.0, SW_Y + 6.0, SW_Z - 2.1, SW_Z + 2.1))   # switch slot, left wall
    cut.append(boxr(-21.5, 21.5, -14, 14, CH - DECK - 0.5, CH + 0.5))
    for s_ in (1, -1):   # chamfered top side edges: printed facets either side of the inset Ti plate
        tri = [(s_ * (CX - CHAMF[0]), CH + 0.01), (s_ * (CX + 0.01), CH + 0.01), (s_ * (CX + 0.01), CH - CHAMF[1])]
        cut.append(place({"type": "prism", "points": r4(tri if s_ > 0 else list(reversed(tri))), "height": TP_Y - CY0 + 1}, (0, (CY0 + TP_Y - 1) / 2, 0), (90, 0, 0)))
    cut.append(yz([(CY0 - 0.01, CH + 0.01), (CY0 + CHAMF[0], CH + 0.01), (CY0 - 0.01, CH - CHAMF[1])], -CX - 1, CX + 1))   # rear facet
    cut.append(yz([(CY1 - 1.0, zdeck(CY1 - 1.0) + 0.2), (CY1 + 0.1, NOSE_Z + 0.2), (CY1 + 0.1, NOSE_Z - 1.0)], -9.0, 9.0))   # nose relief under the disc (1 mm rub gap)
    for s_ in (1, -1):   # side-wall lightening windows, hidden behind the pods
        cut.append(boxr(*sorted((s_ * (CX - WALL - 0.5), s_ * (CX + 0.5))), -12.0, -1.0, 4.5, 13.5))
    cut.append(yz(rrect(-14.0, 14.0, 5.0, 12.0, 2.0), -0.0, 0.0) if False else boxr(-14.0, 14.0, CY0 - 0.5, CY0 + WALL + 0.5, 6.0, 12.0))   # rear-wall window (charge lead / LED view)          # deck window under the Ti plate
    cut.append(boxr(-7.5, -1.0, CY1 - FWALL - 0.5, CY1 + 0.5, 4.5, 9.0))   # weapon phase-wire grommet hole, between the drive gearmotors
    return S(body, *cut)


UB_Y = (38.4, 42.9)
UB_Z = 11.2


# ---------------------------------------------------------------- base panel (printed, X-ribbed, 5 x M2 CSK)
def base_panel():
    x1, y0, y1 = CX - WALL - 0.2, CY0 + WALL + 0.2, CY1 - FWALL - 0.2
    skin = boxr(-x1, x1, y0, y1, BP_Z0, BP_Z0 + 0.9)
    ribs = []
    L = math.hypot(2 * x1, y1 - y0); ang = math.degrees(math.atan2(y1 - y0, 2 * x1))
    for a in (ang, -ang):
        ribs.append(place({"type": "box", "size": [L - 4, 1.6, 1.5]}, (0, (y0 + y1) / 2, BP_Z0 + 1.75), (0, 0, a)))
    rim = S(boxr(-x1, x1, y0, y1, BP_Z0, BP_Z0 + BP_T), boxr(-x1 + 1.4, x1 - 1.4, y0 + 1.4, y1 - 1.4, BP_Z0 - 1, BP_Z0 + BP_T + 1))
    pads = [cylz(3.0, BP_Z0, BP_Z0 + BP_T, x, y) for x, y in POSTS]
    rails = []
    for s in (1, -1):   # gearbox rails: the motor sits on them, the deck ribs clamp it from above
        for ya, yb in ((YF - 6.2, YF - 5.0),):
            rails.append(boxr(*sorted((s * (MOT_CX - 8.0), s * (MOT_CX + 8.0))), ya, yb, BP_Z0 + 1.0, AXZ - 6.0 + 2.0))
    for s in (1, -1):
        rails.append(boxr(*sorted((s * (MOT_CX - 8.0), s * (MOT_CX + 8.0))), YF - 4.0, YF + 4.0, BP_Z0 + 1.0, AXZ - 6.0))   # saddle
        rails.append(boxr(*sorted((s * (MOT_CX - MOT_L / 2 - 1.4), s * (MOT_CX - MOT_L / 2))), YF - 4.0, YF + 4.0, BP_Z0 + 1.0, AXZ - 1.0))   # end stop
    fence = [boxr(-19.0, 19.0, BAT_Y - 8.6 - 1.2, BAT_Y - 8.6, BP_Z0 + 1.0, BP_Z0 + BP_T + 2.0),
             boxr(-19.0, 19.0, BAT_Y + 8.6, BAT_Y + 8.6 + 1.2, BP_Z0 + 1.0, BP_Z0 + BP_T + 2.0)]
    body = U(skin, rim, *ribs, *pads, *rails, *fence)
    cut = [cylz(1.1, BP_Z0 - 1, BP_Z0 + BP_T + 1, x, y) for x, y in POSTS]
    cut += [cylz(2.0, BP_Z0 - 0.1, BP_Z0 + 1.0, x, y) for x, y in POSTS]   # countersink seats
    return S(body, *cut)


# ---------------------------------------------------------------- weapon
TOOTH_A = 90.0
TOOTH = [(-62, RING_O + 0.05), (-48, 17.9), (-34, 18.3), (-22, 18.7), (-12, 19.4), (-5, 19.85), (0.0, 20.0), (1.0, 19.85), (1.8, 18.9), (2.8, 17.6), (5.0, RING_O + 0.03)]   # one hooked tooth, 3.5 mm proud of the rim
BOLT_A = (45, 135, 225, 315)
LOCK_A = 292.5                                    # removable lock-pin hole (blade-local angle)
LOCK_R = 1.6
LIGHT_A = (0, 90, 180, 270)


def blade_outline(o):
    cx, cy = o
    def circ(a):
        t = math.radians(a); ux, uy = math.cos(t), math.sin(t)
        b = -2 * (cx * ux + cy * uy); c = cx * cx + cy * cy - RING_O * RING_O
        r = (-b + math.sqrt(b * b - 4 * c)) / 2
        return (r * ux, r * uy)
    pts = []; a = TOOTH_A + 8.0
    while a < TOOTH_A + 8.0 + 286 - 0.1:
        pts.append(circ(a)); a += 8.0
    for da, r in TOOTH:
        t = math.radians(TOOTH_A + da); pts.append((r * math.cos(t), r * math.sin(t)))
    return r4(pts)


def lock_hole(t):
    return cyl(LOCK_R, t + 2, (BOLT_R * math.cos(math.radians(LOCK_A)), BOLT_R * math.sin(math.radians(LOCK_A)), 0))


def blade_holes(t):
    h = [cyl(1.4, t + 2, (BOLT_R * math.cos(math.radians(a)), BOLT_R * math.sin(math.radians(a)), 0)) for a in BOLT_A]
    h += [cyl(1.8, t + 2, (BOLT_R * math.cos(math.radians(a)), BOLT_R * math.sin(math.radians(a)), 0)) for a in LIGHT_A]
    h.append(lock_hole(t))
    return h


def kidney(ac, t):
    pts = []
    for k in range(9):
        a = math.radians(ac - 32 + 64 * k / 8); pts.append((9.2 * math.cos(a), 9.2 * math.sin(a)))
    for k in range(9):
        a = math.radians(ac + 22 - 44 * k / 8); pts.append((5.2 * math.cos(a), 5.2 * math.sin(a)))
    return {"type": "spline_prism", "points": r4(pts), "height": t + 2}


def tooth_blade(o):
    """2 mm tooth plate: rim + 4 spokes + hub drawn solid over the motor shaft (pivot of the weapon joint)."""
    return S({"type": "spline_prism", "points": blade_outline(o), "height": BT_C}, *[kidney(a, BT_C) for a in (0, 90, 180, 270)],
             *[cyl(1.4, BT_C + 2, (BOLT_R * math.cos(math.radians(a)), BOLT_R * math.sin(math.radians(a)), 0)) for a in BOLT_A], lock_hole(BT_C))


def ring_blade():
    return S(cyl(RING_O, BT_O), cyl(RING_I, BT_O + 2), *blade_holes(BT_O))


def solve_balance():
    from robot import shapes
    import numpy as np
    def c(o):
        q = shapes.to_solid(tooth_blade(tuple(o))).center(); return np.array([q.X, q.Y])
    o = np.array([0.0, -0.05]); h = 0.02
    for _ in range(8):
        f = c(o)
        if np.abs(f).max() < 1e-4: break
        J = np.column_stack([(c(o + [h, 0]) - f) / h, (c(o + [0, h]) - f) / h]); o = o - np.linalg.solve(J, f)
    f = c(o); print("blade balance o=(%.4f,%.4f) centroid %.5f %.5f" % (o[0], o[1], f[0], f[1]))
    return (float(o[0]), float(o[1]))


BAL = solve_balance()


def yzr(a):
    """Blade-local angle -> (y, z) offset from the spin axis (blades are placed with rot [0, 90, 0])."""
    return BOLT_R * math.sin(math.radians(a)), -BOLT_R * math.cos(math.radians(a))


def spider():
    hub = cylx(4.5, SP_F0, SP_H1 + 1.0, 0, 0)
    # 8-lobe flange: a 15.9 disc with 8 R4 scallops milled between the lobes (bolts and lightening holes on the lobes)
    flange = S(cylx(15.9, SP_F0, SP_H1, 0, 0), *[cylx(4.0, SP_F0 - 1, SP_H1 + 1, 16.6 * math.sin(math.radians(22.5 + 45 * k)), -16.6 * math.cos(math.radians(22.5 + 45 * k))) for k in range(8)])
    cut = []
    for a in BOLT_A:
        y, z = yzr(a); cut.append(cylx(1.4, SP_F0 - 1, SP_H1 + 1, y, z))
    for a in LIGHT_A:
        y, z = 9.0 * math.sin(math.radians(a)), -9.0 * math.cos(math.radians(a))
        cut.append(cylx(2.2, SP_F0 - 1, SP_H1 + 1, y, z))
    cut.append(cylx(1.5, SP_F0 - 1, SP_H1 + 2, 0, 0))   # shaft bore
    return S(U(hub, flange), *cut)


# ---------------------------------------------------------------- uprights
def upright(side):
    if side == "r":
        x0, x1, tab = UR0, UR1, TAB_R
        extra = circ_pts((YW, ZW), 6.0) + circ_pts((YW, ZW + 8.0), 3.2) + circ_pts((YW, ZW - 8.0), 3.2)
    else:
        x0, x1, tab = UL0, UL1, TAB_L
        extra = circ_pts((YW, ZW), 6.0)
    extra += circ_pts((YW + yzr(LOCK_A)[0], ZW + yzr(LOCK_A)[1]), 3.4)   # material ring round the lock-pin hole
    prof = hull([(BY0, CHIN_Z1), (BY1, CHIN_Z1), (BY1, TAB_Z1), (BY0, TAB_Z1), (BY0 + 3.0, 20.5)] + extra)
    body = yz(prof, x0, x1)
    cut = []
    bx = (tab[0] + tab[1]) / 2 if side == "l" else (BOSS_R[0] + BOSS_R[1]) / 2
    if side == "l":
        bx = (BOSS_L[0] + BOSS_L[1]) / 2
    for y in UB_Y:   # heat-set insert bores (screws come in through the boss, normal to the contact face)
        cut.append(cylx(1.6, *((x0 - 0.01, x0 + 3.0) if side == 'r' else (x1 - 3.0, x1 + 0.01)), y, UB_Z))
        cut.append(cylx(1.0, x0 - 0.1, x1 + 0.1, y, UB_Z))
    ly, lz = yzr(LOCK_A)
    cut.append(cylx(LOCK_R, x0 - 1, x1 + 1, YW + ly, ZW + lz))   # lock-pin hole
    if side == "r":
        for dz in (-8.0, 8.0):
            cut.append(cylx(1.1, x0 - 1, x1 + 1, YW, ZW + dz))
        cut.append(boxr(x1 - 2.2, x1 + 0.1, YW - 5.1, YW - 2.3, ZW - 10.5, ZW + 2.5))   # phase-wire channel down the motor-side face
        pass
    else:
        cut.append(cylx(3.5, x0 - 0.1, x0 + 3.0, YW, ZW))       # F683 seat on the inner face
        cut.append(cylx(2.6, x0 + 2.9, x1 + 1, YW, ZW))         # push-out hole
    return S(body, *cut)


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


CHAMF = (2.6, 0.9)                                 # tub top-edge chamfer (x, z) under the bent Ti facets


def top_armour():
    """0.4 mm Ti: flat centre panel, side and rear facets bent down over the tub's chamfered top edges."""
    flat = boxr(-TP_X, TP_X, -TP_Y, TP_Y, CH, CH + TP_T)
    fac = []
    for s_ in (1, -1):
        xa, xb = s_ * TP_X, s_ * CX
        poly = [(xa, CH), (xb, CH - CHAMF[1]), (xb, CH - CHAMF[1] + TP_T + 0.1), (xa, CH + TP_T)]
        fac.append(place({"type": "prism", "points": r4(poly if s_ > 0 else list(reversed(poly))), "height": 2 * TP_Y}, (0, 0, 0), (90, 0, 0)))
    rear = [(-TP_Y, CH), (-TP_Y, CH + TP_T), (CY0, CH - CHAMF[1] + TP_T + 0.1), (CY0, CH - CHAMF[1])]
    fac.append(yz(rear, -TP_X, TP_X))
    return S(U(flat, *fac), *[cylz(1.1, CH - 3, CH + 2, x, y) for x, y in TOP_POSTS])


COV_Y1 = 30.47


def top_cover():
    """Printed TPU wedge: 1.2 mm skin on the sloped deck from the Ti plate's front edge to just short of the nose,
    top surface tapering forward; a rear step stands 0.4 proud of the inset Ti plate, side wings wrap the chamfers."""
    n = 8
    th = math.atan((CH - NOSE_Z) / (CY1 - SL0)); t = 1.23
    bot = [(TP_Y + 0.13, CH), (SL0, CH), (COV_Y1, zdeck(COV_Y1))]
    top = [(TP_Y + 0.13, CH + t), (SL0 + t * math.tan(th / 2), CH + t), (COV_Y1 + t * math.sin(th), zdeck(COV_Y1) + t * math.cos(th))]
    return yz(bot + list(reversed(top)), -(CX - CHAMF[0]), CX - CHAMF[0])



# ---------------------------------------------------------------- forks (TPU, sprung)
def forks():
    root = boxr(-12.0, 12.0, BY0, CHIN_Y1, -2.0, 0.6)   # thick root, sunk 0.6 into a chin pocket
    tines = []
    for s in (1, -1):   # B-spline tines: wide sprung root tapering to a rounded scoop tip, thinning towards the tip
        prof = [(BY0, -2.0), (CHIN_Y1 + 4, -2.0), (FORK_TIP - 6, -2.0), (FORK_TIP, -2.0), (FORK_TIP, -0.6), (FORK_TIP - 8, 0.2),
                (CHIN_Y1 + 3, 0.6), (CHIN_Y1 + 0.5, 0.6), (BY0, 0.6)]
        plan = [(3.0, BY0 + 0.3), (11.2, BY0), (11.2, CHIN_Y1 + 2), (11.0, CHIN_Y1 + 12), (10.2, FORK_TIP - 6), (9.6, FORK_TIP - 1.0), (8.9, FORK_TIP), (6.6, FORK_TIP),
                (5.9, FORK_TIP - 1.0), (5.4, FORK_TIP - 6), (4.4, CHIN_Y1 + 12), (3.0, CHIN_Y1 + 2)]
        plan = [(s * x, y) for x, y in plan] if s > 0 else [(s * x, y) for x, y in reversed(plan)]
        tines.append({"type": "intersect", "items": [yz(prof, -13.0, 13.0, spline=False),
                      place({"type": "prism", "points": r4(chaikin(plan, 3)), "height": 4.0}, (0, 0, -0.7))]})
    cut = [cylz(1.1, -3, 1, s * FORK_HX, 37.7) for s in (1, -1)]
    cut += [cylz(2.0, -2.1, -0.6, s * FORK_HX, 37.7) for s in (1, -1)]
    return S(U(root, *tines), *cut)


# ---------------------------------------------------------------- side pods (TPU)
def pod(s):
    x0, x1 = sorted((s * POD_X0, s * POD_X1))
    tip = pv("side_panel_front_wedge_tip_y", 70.2)
    # B-spline (Chaikin) side profile: fenders swell over both wheels, waist dips between them, long ramp to the wedge tip
    top = [(44.0, 10.0), (37.0, 17.0), (YF + 6.0, 21.7), (YF - 3.0, 21.7), (YF - 12.0, 16.0), (0.0, 14.5), (YR + 12.0, 16.0),
           (YR + 3.0, 21.7), (YR - 6.0, 21.7), (CY0 - 1.0, 15.0)]
    bot = [(CY0 - 1.0, 4.0), (CY0 + 3.0, -1.0), (YF + 14, -1.25)]
    prof = bot + [(tip, -1.75)] + chaikin_open([(tip, -0.5)] + top, 3)
    outer = yz(prof, x0, x1)
    wx0, wx1 = sorted((s * CX, s * (CX + 2.0)))
    inner = boxr(wx0, wx1, POD_WY[0], POD_WY[1], 3.0, 13.5)
    fx0, fx1 = sorted((s * (CX + 2.0), s * POD_X0 + s * 0.1))
    fl = [boxr(fx0, fx1, POD_WY[0], POD_WY[1], 3.0, 5.0), boxr(fx0, fx1, POD_WY[0], POD_WY[1], 11.5, 13.5)]
    tcf = chaikin_open([(tip, -0.5)] + top, 3)
    yr_ = max((p for p in tcf if p[0] < 0), key=lambda p: p[1])[0]; yf_ = max((p for p in tcf if p[0] > 0), key=lambda p: p[1])[0]
    tc = [p for p in tcf if yr_ <= p[0] <= yf_]   # lip runs crest to crest
    # one prism 6.5 mm wider than the wall, carved back so only a 1.4 mm lip follows the top edge over the wheels
    ix0, ix1 = sorted((s * (POD_X0 - 6.5), s * POD_X0))
    outer = yz(prof, *sorted((s * (POD_X0 - 6.5), s * POD_X1)))
    under = [(y, z - 1.5) for y, z in tc] + [(tc[-1][0], -10.0), (tc[0][0], -10.0)]
    carve = [yz(under, ix0 - 0.01 * s, ix1), boxr(ix0 - 0.01, ix1, tc[0][0] - 0.01, 200.0, -10.0, 40.0), boxr(ix0 - 0.01, ix1, -200.0, tc[-1][0] + 0.01, -10.0, 40.0)]
    lx = sorted((s * (POD_X0 - 1.6), s * POD_X0 + s * 0.05))
    ledge = yz([(53.07, 4.85), (65.93, 1.73), (66.21, 2.9), (53.35, 6.02)], *lx)   # keys the spike's top edge
    body = U(S(outer, *carve), inner, *fl, ledge)
    cut = []
    for y in POD_Y:
        cut.append(cylx(1.1, wx0 - 1, wx1 + 1, y, POD_Z))
    cut.append(yz(rrect(POD_Y[0] - 2.8, POD_Y[1] + 2.8, POD_Z - 2.8, POD_Z + 2.8, 2.7), x0 - 1, x1 + 1))   # driver access slot
    for y in SPK_Y:
        cut.append(cylx(1.1, x0 - 1, x1 + 1, y, SPK_Z))
    for y0 in (-29.0, -24.0, -19.0, 17.0, 22.0, 27.0, 34.5, 39.5) + ((-14.0, -9.5) if s > 0 else ()):   # angled slash vents (raked back 25 deg)
        ztop = 13.0 if y0 < 33 else 11.0
        cut.append(yz(chaikin([(y0, 3.5), (y0 + 2.4, 3.5), (y0 + 2.4 + 0.47 * (ztop - 3.5), ztop), (y0 + 0.47 * (ztop - 3.5), ztop)], 2), x0 - 1, x1 + 1))
    cut.append(yz(rrect(-3.0, 3.0, 14.8, 17.3, 1.0), x0 - 1, x1 + 1))
    if s < 0:
        cut.append(cylx(3.0, x0 - 1, x1 + 1, SW_Y, SW_Z))     # switch access
    return S(body, *cut)


# ---------------------------------------------------------------- drive
def hub_front():   # hub-local: x 0 = inner face
    spig = cylx(4.5, 0.0, PUL_W, 0, 0)
    body = cylx(HUB_R, PUL_W, HUB_L, 0, 0)
    lip = cylx(HUB_R + 0.6, HUB_L - 1.0, HUB_L, 0, 0)
    return S(U(spig, body, lip), S(cylx(HUB_R - 1.2, PUL_W + 1.5, HUB_L - 1.0, 0, 0), cylx(2.6, 0, HUB_L + 1, 0, 0)))


def hub_rear():
    spig = cylx(4.5, 0.0, PUL_W, 0, 0)
    body = cylx(HUB_R, PUL_W, HUB_L, 0, 0)
    lip = cylx(HUB_R + 0.6, HUB_L - 1.0, HUB_L, 0, 0)
    cut = [cylx(3.0, -0.1, 2.5, 0, 0), cylx(3.0, HUB_L - 2.5, HUB_L + 0.1, 0, 0), cylx(2.6, 2.4, HUB_L - 2.4, 0, 0),
           S(cylx(HUB_R - 1.2, PUL_W + 1.0, HUB_L - 1.0, 0, 0), cylx(4.4, 0, HUB_L + 1, 0, 0))]
    return S(U(spig, body, lip), *cut)


def tyre():   # printed TPU tyre with 10 axial cells (softer, lighter)
    rc = (RT + HUB_R) / 2
    cells = [cylx(0.8, PUL_W - 1, HUB_L + 1, rc * math.cos(2 * math.pi * k / 10), rc * math.sin(2 * math.pi * k / 10)) for k in range(10)]
    return S(cylx(RT, PUL_W + 0.25, HUB_L, 0, 0), cylx(HUB_R, 0, HUB_L + 1, 0, 0))
def pulley(): return S(cylx(8.0, 0.0, PUL_W, 0, 0), cylx(4.5, -1, PUL_W + 1, 0, 0), S(cylx(8.2, 1.0, 2.5, 0, 0), cylx(7.5, 0.9, 2.6, 0, 0)))


def belt(s):
    xa, xb = sorted((s * (HUB_X0 + 1.0), s * (HUB_X0 + 2.5)))
    o = hull(circ_pts((YF, AXZ), 9.0) + circ_pts((YR, AXZ), 9.0)); i = hull(circ_pts((YF, AXZ), 7.5) + circ_pts((YR, AXZ), 7.5))
    return S(yz(o, xa, xb), yz(i, xa - 1, xb + 1))


BELT_L = round((2 * WB + 2 * math.pi * 8.25) * 0.95, 1)

# ---------------------------------------------------------------- parts
P(id="tub", kind="structure", material="nylon", process="fdm", print_orientation="-z", rotates_with="fixed", solid_fraction=0.85, color="#2a2c30",
  shape=chassis(), label="printed nylon chassis: 1.6 mm walls, open bottom, sloped nose, square upright bosses, insert posts")
P(id="base_panel", kind="structure", material="nylon", process="fdm", print_orientation="+z", rotates_with="fixed", color="#2a2c30",
  shape=base_panel(), label="printed X-ribbed base panel, 5 countersunk M2 into heat-set inserts; gearbox rails and battery fence")
SPK = [(53.0, -1.95), (FORK_TIP + 1.0, -1.95), (FORK_TIP + 1.0, -1.45), (53.0, 4.8)]
for s, n in ((1, "l"), (-1, "r")):
    xa, xb = sorted((s * (POD_X0 - 1.0), s * POD_X0))
    P(id=f"spike_{n}", kind="fork", material="steel", process="laser", rotates_with="fixed", color="#3a3d42", stock="1.0 mm spring steel",
      shape=S(yz(SPK, xa, xb), *[cylx(1.1, xa - 1, xb + 1, y, SPK_Z) for y in SPK_Y]),
      label="1 mm hardened spring-steel spike fork bolted inside the pod's front corner, tip 0.3 mm off the floor")
    for k, y in enumerate(SPK_Y):
        P(id=f"nut_s{n}{k}", kind="nut", material="steel", process="turned", secondary_ops=["flat"], rotates_with="fixed", color="#aaaaaa", stock="M2 x 3 hex coupling nut",
          shape=S(hexp(4.0, 3.0, (s * (POD_X0 - 2.5), y, SPK_Z)), cylx(1.0, *sorted((s * (POD_X0 - 4.5), s * (POD_X0 - 0.5))), y, SPK_Z)), label="M2 x 3 long hex nut inside the spike, Loctite 243")
P(id="top_cover", kind="skirt", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", color="#b9bec6",
  shape=top_cover(), label="printed TPU wedge cover on the sloped deck: tapers forward from 1.9 mm proud at the Ti plate edge to 1.2 mm; the Ti plate sits inset behind its step")
P(id="top_armour", kind="armor", material="titanium", process="laser", rotates_with="fixed", color="#c9ccd1",
  shape=S(boxr(-TP_X, TP_X, -TP_Y, TP_Y, CH, CH + TP_T), *[cylz(1.1, CH - 1, CH + 2, x, y) for x, y in TOP_POSTS]),
  label=f"{TP_T} mm Ti-6Al-4V top plate 55 x 37, laser-cut, inset between the tub's chamfered top facets, 4 M2", stock=f"{TP_T} mm Ti sheet")
for s, n in ((1, "l"), (-1, "r")):
    P(id=f"pod_{n}", kind="skirt", material="tpu", process="fdm", print_orientation="+x" if s > 0 else "-x", rotates_with="fixed", color="#c8102e",
      shape=pod(s), label="red TPU side panel (bumper): wedge-nosed outer wall over both wheels, boxed web screwed to the chassis wall by 2 M2")
for n in "rl":   # quick-change weapon module: both uprights, motor and rotor lift out together once the 4 boss screws are out
    P(id=f"upright_{n}", kind="structure", material="nylon", process="fdm", print_orientation="+x", rotates_with="fixed", solid_fraction=0.9, color="#2a2c30",
      **({"parent": "upright_r"} if n == "l" else {}),
      shape=upright(n), label="5 mm printed nylon weapon upright (spin axis = build direction), foot slides down over a square chassis boss, 2 M2 through the boss into inserts" + ("; F683 seat" if n == "l" else "; motor mount"))
P(id="weapon_motor", kind="weapon_motor", catalog="bl_1806_2300kv", parent="upright_r", at=[WX0, YW, ZW], rot=[0, 0, 0], rotates_with="fixed", motor_shaft_extended=True,
  ports={"phases": [-6.5, 0, -9.0]}, label="BE1806 2300 kV outrunner = weapon hub: stator bolted to the right upright, its own (lengthened) 3 mm shaft runs on into an F683 in the left upright")
MF_AT, MF_ROT = [0, 0, -sum(BLC) / 2], [0, -90, 0]   # children of blade_c drawn in the motor frame
P(id="blade_c", kind="weapon", material="steel", process="laser", organic=True, rotates_with="weapon", shape=tooth_blade(BAL), at=[sum(BLC) / 2, 0, 0], rot=[0, 90, 0],
  parent="weapon_motor", joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [sum(BLC) / 2, 0, 0], "min": 0, "max": 360, "default": 0}, color="#d9dde2",
  weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 1},
  label="2 mm Hardox 450 (cold-rolled) tooth plate: one hooked tooth (R 20, ~5 deg rake), 4 spokes, hub bored to the bell boss; ring offset balances the tooth")
P(id="wshaft", kind="shaft", material="titanium", process="cots", rotates_with="weapon", shaft_of="weapon_motor", stock="3 mm Ti-6Al-4V rod",
  shape=cylx(1.5, SH0, SH1, 0, 0), parent="blade_c", at=MF_AT, rot=MF_ROT, color="#777777",
  label="BE1806 rotor shaft replaced by a 3 mm Ti-6Al-4V shaft, lengthened through the blade stack into the F683 (circlip at the stator)")
P(id="spider", kind="other", role="spider", material="aluminium", process="milled", secondary_ops=["turned", "drilled"], rotates_with="weapon",
  shape=spider(), parent="blade_c", at=MF_AT, rot=MF_ROT, color="#3a3d42",
  label="6061 spider: hub on the bell/shaft (2 M3 grub screws on the flat), 1.5 mm flange with 4 M2.5 holes on a 29.5 mm circle, 4 lightening holes")
for i, a in enumerate(BOLT_A):
    y, z = yzr(a)
    P(id=f"wpin{i}", kind="other", role="bolt", material="steel", process="turned", rotates_with="weapon", parent="blade_c", at=MF_AT, rot=MF_ROT, color="#9a9a9a",
      shape=U(cylx(1.25, NUT0, SP_H1, y, z), cylx(2.35, SP_H1, SP_H1 + HEAD_T, y, z)),
      label="M2.5x8 ISO7380 button-head screw (drawn as a part so it turns with the rotor), Loctite 243")
    P(id=f"wnut{i}", kind="nut", material="steel", process="turned", rotates_with="weapon", parent="blade_c", at=MF_AT, rot=MF_ROT, color="#aaaaaa",
      shape=S(cylx(2.35, NUT0, BLO[0], y, z), cylx(1.25, NUT0 - 1, BLO[0] + 1, y, z)), label="M2.5 round (barrel) nut 4.7 x 1.8, turned steel")
P(id="wbearing", kind="bearing", parent="upright_l", material="steel", process="cots", rotates_with="fixed", color="#555555", stock="683ZZ",
  shape=S(cylx(3.5, UL0, UL0 + 3.0, YW, ZW), cylx(1.5, UL0 - 1, UL0 + 4.0, YW, ZW)), label="F683ZZ 3x7x3 flanged bearing in the left upright, flange on the inner face (flange not drawn)")

for s, n in ((1, "l"), (-1, "r")):
    rot = [0, 0, 0] if s > 0 else [0, 0, 180]
    P(id=f"motor_{n}", kind="motor", catalog="n10_2200rpm_6v", at=[s * MOT_CX, YF, AXZ], rot=rot, rotates_with="fixed")
    hub_local = HUB_X0 - MOT_CX
    P(id=f"whub_f{n}", kind="other", material="nylon", process="fdm", print_orientation="+x", rotates_with=f"wheel_f{n}", shape=hub_front(), at=[hub_local, 0, 0],
      parent=f"motor_{n}", joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [hub_local + 2.0, 0, 0], "min": 0, "max": 360, "default": 0},
      color="#333333", label="printed nylon hub on the N10 D-shaft")
    P(id=f"wheel_f{n}", kind="wheel", material="tpu", process="fdm", print_orientation="+x", tyre_of=f"whub_f{n}", rotates_with=f"wheel_f{n}", shape=tyre(),
      parent=f"whub_f{n}", color="#1b1b1b", label="printed TPU 85A tyre, Scalextric F1 profile 21.5 x 9.5")
    P(id=f"pulley_f{n}", kind="pulley", material="nylon", process="fdm", print_orientation="+x", rotates_with=f"wheel_f{n}", shape=pulley(), parent=f"whub_f{n}", color="#444444")
    P(id=f"axle_{n}", kind="pin", material="steel", process="cots", rotates_with="fixed", color="#777777", stock="3 mm silver steel rod",
      shape=cylx(1.5, *sorted((s * (CX - WALL - 2.4), s * (HUB_X1 + 0.5))), YR, AXZ), label="3 mm silver-steel stub axle pressed into the wall boss, e-clip outboard")
    P(id=f"wbrg_{n}0", kind="bearing", material="steel", process="cots", rotates_with=f"wheel_r{n}", color="#555555", stock="MR63ZZ",
      shape=cylx(3.0, 0.0, 2.5, 0, 0), at=[s * HUB_X0, YR, AXZ], rot=rot, parent=f"axle_{n}",
      joint={"kind": "revolute", "axis": [s, 0, 0], "pivot": [s * (HUB_X0 + 1.2), YR, AXZ], "min": 0, "max": 360, "default": 0},
      label="MR63ZZ 3x6x2.5 (drawn solid)")
    P(id=f"whub_r{n}", kind="other", material="nylon", process="fdm", print_orientation="+x", rotates_with=f"wheel_r{n}", shape=hub_rear(), at=[0, 0, 0],
      parent=f"wbrg_{n}0", color="#333333", label="printed nylon rear hub on two MR63ZZ")
    P(id=f"wbrg_{n}1", kind="bearing", material="steel", process="cots", rotates_with=f"wheel_r{n}", color="#555555", stock="MR63ZZ",
      shape=S(cylx(3.0, HUB_L - 2.5, HUB_L, 0, 0), cylx(1.5, HUB_L - 3.5, HUB_L + 1.0, 0, 0)), parent=f"whub_r{n}", label="MR63ZZ 3x6x2.5")
    P(id=f"wheel_r{n}", kind="wheel", material="tpu", process="fdm", print_orientation="+x", tyre_of=f"whub_r{n}", rotates_with=f"wheel_r{n}", shape=tyre(),
      parent=f"whub_r{n}", color="#1b1b1b", label="printed TPU 85A tyre, Scalextric F1 profile 21.5 x 9.5")
    P(id=f"pulley_r{n}", kind="pulley", material="nylon", process="fdm", print_orientation="+x", rotates_with=f"wheel_r{n}", shape=pulley(), parent=f"whub_r{n}", color="#444444")
    P(id=f"belt_{n}", kind="belt", material="rubber", process="cots", shape=belt(s), color="#111111",
      belt={"pulleys": [f"pulley_f{n}", f"pulley_r{n}"], "kind": "o_ring", "length_mm": BELT_L, "width_mm": 1.5}, label=f"1.5 mm nitrile O-ring, {BELT_L} mm")

P(id="battery", kind="battery", catalog="lipo_2s_350", at=[0, BAT_Y, BP_Z0 + BP_T + 5.5], retained="press_fit")
P(id="rxesc", kind="esc", catalog="c_malenki_nano_antweight_esc_receiver", at=[0, BAT_Y, CH - DECK - 1.25], retained="velcro",
  ports={"bat": [-16, -4, 0], "m1": [16, 4, 0], "m2": [-16, 4, 0], "wpn": [16, -4, 0]}, label="Malenki-Nano drive ESC + receiver")
P(id="wesc", kind="esc", catalog="c_bbb_antweight_spinner_brushless_esc", at=[0, 7.0, BP_Z0 + BP_T + 2.0], retained="press_fit",
  ports={"bat": [11.5, -3, 0], "motor": [11.5, 3, 0], "rx": [-11.5, 0, 0]})
P(id="power_switch", kind="switch", catalog="switch_slide_12x4", at=[-CX + 2.0, SW_Y, SW_Z], rot=[0, 0, 90], retained="press_fit", label="ON/OFF", marked=True, tool_free=True)

for i, (x, y) in enumerate(BASE_PTS):
    P(id=f"insert_b{i}", kind="insert", catalog="heatset_m2", at=[x, y, INS_B_Z])
for i, (x, y) in enumerate(TOP_POSTS):
    P(id=f"insert_t{i}", kind="insert", catalog="heatset_m2", at=[x, y, INS_T_Z])
for n, xi in (("r", UR0 + 1.5), ("l", UL1 - 1.5)):
    for k, y in enumerate(UB_Y):
        P(id=f"insert_u{n}{k}", kind="insert", parent=f"upright_{n}", catalog="heatset_m2", at=[xi, y, UB_Z], rot=[0, 90, 0])
for s, n in ((1, "l"), (-1, "r")):
    for k, y in enumerate(POD_Y):
        P(id=f"insert_p{n}{k}", kind="insert", catalog="heatset_m2", at=[s * INS_P_X, y, POD_Z], rot=[0, 90, 0])

fast = []
def F(**k):
    k.setdefault("head", "socket"); k.setdefault("tool", "hex1.5"); k.setdefault("removable", True); fast.append(k)
for i, (x, y) in enumerate(BASE_PTS):
    F(id=f"bolt_b{i}", designation="M2x6", at=[x, y, BP_Z0], dir=[0, 0, 1], through=["base_panel", "tub"], threads_into=f"insert_b{i}", head="countersunk",
      reason="Panel drops into the wall rim (sides only locate it, 0.2 mm clear); the screws clamp it up against the post end faces, which are normal to them")
for i, (x, y) in enumerate(TOP_POSTS):
    F(id=f"bolt_t{i}", designation="M2x6", at=[x, y, CH + TP_T], dir=[0, 0, -1], through=["top_armour", "tub"], threads_into=f"insert_t{i}")
for n, x0, d in (("r", BOSS_R[0], 1), ("l", BOSS_L[1], -1)):
    for k, y in enumerate(UB_Y):
        F(id=f"bolt_u{n}{k}", designation="M2x10", at=[x0, y, UB_Z], dir=[d, 0, 0], through=["tub", f"upright_{n}"], threads_into=f"insert_u{n}{k}")
for k, dz in enumerate((-8.0, 8.0)):
    F(id=f"bolt_wm{k}", designation="M2x8", at=[UR0, YW, ZW + dz], dir=[1, 0, 0], through=["upright_r"], threads_into="weapon_motor")
for s, n in ((1, "l"), (-1, "r")):
    for k, y in enumerate(POD_Y):
        F(id=f"bolt_p{n}{k}", designation="M2x8", at=[s * (CX + 2.0), y, POD_Z], dir=[-s, 0, 0], through=[f"pod_{n}", "tub"], threads_into=f"insert_p{n}{k}")
for s, n in ((1, "l"), (-1, "r")):
    for k, y in enumerate(SPK_Y):
        F(id=f"bolt_s{n}{k}", designation="M2x6", at=[s * POD_X1, y, SPK_Z], dir=[-s, 0, 0], through=[f"pod_{n}", f"spike_{n}"], threads_into=f"nut_s{n}{k}")


def Wr(i, a, b, awg, kind, sl): return {"id": i, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": sl}
wires = [Wr("w_bat_sw", "battery.xt30", "power_switch.in", 22, "power", 8), Wr("w_sw_wesc", "power_switch.out", "wesc.bat", 22, "power", 8),
         Wr("w_sw_rx", "power_switch.out", "rxesc.bat", 26, "power", 8), Wr("w_wesc_m", "wesc.motor", "weapon_motor.phases", 24, "motor", 12),
         Wr("w_rx_wesc", "rxesc.wpn", "wesc.rx", 30, "signal", 6), Wr("w_m_l", "rxesc.m1", "motor_l.terminals", 28, "motor", 6),
         Wr("w_m_r", "rxesc.m2", "motor_r.terminals", 28, "motor", 6)]
conn = []
def C(a, b, m, r, **k): conn.append(dict(a=a, b=b, method=m, reason=r, **k))
for n in "lr":
    C(f"motor_{n}", f"whub_f{n}", "press_fit", "Printed hub pressed onto the 3 mm D-shaft of the N10; the flat carries the torque", interference_mm=0.1, mechanical_key=True)
    C(f"motor_{n}", "tub", "interlock", "Gearbox boss sits in the keyhole in the side wall; gearbox clamped between the deck ribs and the base-panel rails, the flats stop it turning")
    C(f"motor_{n}", "base_panel", "interlock", "Base-panel rails either side of the gearbox; the 5 base screws clamp the motor against the deck ribs")
    C(f"axle_{n}", "tub", "press_fit", "Stub axle pressed through the wall into a 4 mm deep printed boss", interference_mm=0.05, mechanical_key=True)
    C(f"wbrg_{n}0", f"axle_{n}", "shaft", "Bearing inner race on the 3 mm stub axle; e-clip outboard")
    C(f"whub_r{n}", f"wbrg_{n}0", "press_fit", "MR63 pressed into the hub bore", interference_mm=0.05, mechanical_key=True)
    C(f"wbrg_{n}1", f"whub_r{n}", "press_fit", "MR63 pressed into the hub bore", interference_mm=0.05, mechanical_key=True)
    C(f"wbrg_{n}1", f"axle_{n}", "shaft", "Bearing inner race on the 3 mm stub axle")
    for k in "fr":
        C(f"pulley_{k}{n}", f"whub_{k}{n}", "press_fit", "Printed O-ring pulley pressed on the hub spigot", interference_mm=0.1, mechanical_key=True)
        C(f"wheel_{k}{n}", f"whub_{k}{n}", "press_fit", "TPU tyre stretched over the hub between the pulley and the lip", interference_mm=0.3, mechanical_key=True)
    C(f"belt_{n}", f"pulley_f{n}", "interlock", "O-ring in the pulley grooves under 5 % stretch; drives the rear wheel")
    C(f"upright_{n}", "tub", "screw", "Upright plate flat against the square boss side; 2 M2 through the boss, normal to that face, into inserts in the upright")
    C(f"upright_{n}", "tub", "interlock", "Upright foot drops over the square boss (slides on, located on three faces) so hits load the boss, not the screws",
      mechanical_key=True)
    C(f"pod_{n}", "tub", "screw", "Side panel web flat on the chassis wall, 2 M2 normal to the wall into heat-set inserts")
C("weapon_motor", "upright_r", "screw", "Stator face bolted to the right upright with 2 M2 along the motor axis")
C("spider", "blade_c", "pin", "Spider flange clamps the blade stack through the 4 M2.5 screws", mechanical_key=True)
C("blade_c", "weapon_motor", "press_fit", "Spider and tooth-plate hub keyed to the bell by 2 M3 grub screws on the shaft flat; the bell drives the stack",
  interference_mm=0.05, mechanical_key=True)
C("wshaft", "weapon_motor", "press_fit", "The motor's own rotor shaft (lengthened), pressed in the bell and held by its circlip", interference_mm=0.05, mechanical_key=True)
C("wshaft", "blade_c", "press_fit", "Tooth-plate hub on the shaft, keyed by the grub screws", interference_mm=0.05, mechanical_key=True)
C("wbearing", "upright_l", "press_fit", "F683ZZ pressed into the left upright, flange against the inner face", interference_mm=0.05, mechanical_key=True)
C("wbearing", "wshaft", "shaft", "F683ZZ inner race on the shaft end: the second support of the rotor")
for b in ("blade_c",):
    C(b, "spider", "pin", "Tooth plate clamped to the spider flange by 4 M2.5 button-head screws and round nuts", mechanical_key=True)
for i in range(4):
    C(f"wpin{i}", "spider", "pin", "M2.5 screw through the spider flange and the blade stack", mechanical_key=True)
    C(f"wnut{i}", f"wpin{i}", "interlock", "Round nut on the screw thread, Loctite 243")
C("base_panel", "tub", "screw", "Base panel inside the wall rim, 3 CSK M2 into the post inserts")
for s, n in ((1, "l"), (-1, "r")):
    C(f"spike_{n}", f"pod_{n}", "screw", "Spike fork bolted flat inside the pod's front corner, M2 into a long nut")
    C(f"spike_{n}", f"pod_{n}", "interlock", "Spike top edge tucked under a moulded TPU ledge on the pod's inner face: keys it against turning about the bolt", mechanical_key=True)
    for k in range(1):
        C(f"nut_s{n}{k}", f"pod_{n}", "interlock", "Nut seated on the pod's outer face, Loctite 243")
C("top_cover", "tub", "snap", "TPU wedge clips over the deck: its rear step is trapped by the Ti plate front edge and its side lips grip the chamfered deck edges")
C("top_armour", "tub", "screw", "Ti plate on the deck, 4 M2 into the post inserts")
C("battery", "base_panel", "press_fit", "Pack boxed by the base-panel fence and the insert posts, trapped from above by the Malenki and the deck", interference_mm=0.1, mechanical_key=True)
C("wesc", "base_panel", "press_fit", "ESC between the gearbox rails and the battery fence, deck above", interference_mm=0.1, mechanical_key=True)
C("rxesc", "tub", "velcro", "Malenki board on hook-and-loop under the deck, behind the deck window; the pack sits 0.5 mm below it")
C("power_switch", "tub", "press_fit", "Switch pressed into a slot in the left wall", interference_mm=0.1)

ov = [dict(a="weapon_motor", b="spider", max_depth_mm=0.6, reason="spider bore seats over the bell's shaft boss (catalog motor drawn with a solid boss)"),
      dict(a="weapon_motor", b="wshaft", max_depth_mm=1.5, reason="the motor's own shaft inside its stator bore (catalog motor drawn solid)"),
      dict(a="blade_c", b="wshaft", max_depth_mm=1.6, reason="tooth-plate hub drawn solid over the 3 mm shaft (holds the joint pivot)"),
      dict(a="blade_c", b="weapon_motor", max_depth_mm=0.7, reason="tooth-plate bore seats over the bell's shaft boss (catalog motor drawn with a solid boss)")]
for i in range(4):
    pass
for n in "lr":
    ov.append(dict(a=f"motor_{n}", b=f"whub_f{n}", max_depth_mm=1.5, reason="hub D-bore on the N10 shaft (catalog motor shaft drawn round)"))
    ov.append(dict(a=f"axle_{n}", b=f"wbrg_{n}0", max_depth_mm=1.6, reason="inner bearing drawn solid over the 3 mm axle (holds the joint pivot)"))

spec = dict(name="Revron", profile="aws2025", robot_type="vertical_spinner", locomotion="roller",
            archetype="vertical_spinner_forks",
            archetype_params={"blade_lead_mm": [5, 15], "axle_height_mm": [21, 25], "disc_thickness_mm": [4.5, 7], "disc_dia_mm": [37, 43], "teeth": [1, 1],
                              "tub_height_mm": [16, 19], "wheels": [4, 4], "wheel_dia_mm": [20, 23], "weapon_mass_fraction": [0.20, 0.5], "top_slope_deg": [0, 25]},
            targets={"length_mm": 110, "width_mm": round(2 * POD_X1), "disc_dia_mm": 40, "wheel_dia_mm": TYRE_OD, "tol_mm": 6,
                     "source": "robots/revron/params.json", "note": "axle 23 above floor; single 2 mm Hardox tooth plate on a BE1806 hub; belted 4WD"},
            reference=[{"image": "../../robots/revron/photos/ref3.png", "view": "side", "mask": "../../robots/revron/reference/side_mask.png", "scale_hint": 0.162},
                       {"image": "../../robots/revron/photos/ref2.jpg", "view": "iso", "mask": "../../robots/revron/reference/iso_mask.png", "approximate": True}],
            weapon_lock={"type": "removable_pin", "dia_mm": 3.0, "axis": [1, 0, 0],
                         "at": [0.0, round(YW + yzr(LOCK_A)[0], 3), round(ZW + yzr(LOCK_A)[1], 3)],
                         "holes": ["upright_r", "blade_c", "upright_l"],
                         "note": "red 3 mm REMOVE-BEFORE-FIGHT pin (not modelled): slides in from the right through both uprights, the blade stack and the spider flange"},
            parts=parts, fasteners=fast, wires=wires,
            electronics=dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2), can_run_inverted=False,
            allow_overlap=ov, connections=conn,
            claims=[dict(id="c_mass", text="weighs 147 g or less", metric="mass_total_g", op="<=", value=147),
                    dict(id="c_fit", text="fits the 150 mm square", metric="footprint_mm", op="<=", value=150)])
json.dump(spec, open(OUT, "w"), indent=1)
json.dump(spec, open(os.path.join(HERE, "..", "spec.json"), "w"), indent=1)
print("wrote", OUT, len(parts), "parts", len(fast), "fasteners; belt", BELT_L, "front", FORK_TIP, "WX0", WX0, "UL0", UL0)
