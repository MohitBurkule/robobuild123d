"""[W1] Tub shell cuts: deck lightening pockets, base-panel seat (rabbet, ring-boss recesses, preload pad recess, squared corner),
motor stop-wall round, and (unchanged, owned by the heat-set worker) the column bores and the switch slot with its pilots."""
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_util import both, rect, sym, cone, inner
from .tub_shell_cols import STOP_X0, STOP_Y, EPS

# ---- deck pockets (STEP RV01 at deck Z): an X of 2 mm ribs, two diagonals; 1 mm skin stays
POCKET_Z = (-0.5, 1.0)                        # cutter Z span relative to the deck underside
X_RIB, X_SLOPE, X_R = 22.25, 0.6404, 0.8      # half width of the X pockets (= the corner block face), diagonal slope, corner R
X_UP = (-3.07, 12.4)                          # front pocket: apex Y on the axis, top edge Y
X_LO = (-8.13, -23.4, -23.6)                  # rear pocket: apex Y, rear edge Y beside the blocks, rear edge Y between the stop walls
X_NOTCH = 17.5                                # |X| where the rear pocket steps back between the motor stop walls
SIDE_X, SIDE_DIAG = 22.5, dict(x=19.51, y_up=4.51, k_up=0.640, y_lo=-15.71, k_lo=0.6407)   # side pocket: right edge |X| (= the switch pad edge), diagonals through (x, y) with slope k
SIDE_TRI = [(3.72, -5.59), (SIDE_X, SIDE_DIAG["y_up"] + SIDE_DIAG["k_up"] * (SIDE_X - SIDE_DIAG["x"])),
            (SIDE_X, SIDE_DIAG["y_lo"] - SIDE_DIAG["k_lo"] * (SIDE_X - SIDE_DIAG["x"]))]
SIDE_R = 1.9                                  # apex R towards the centre
REAR_P = dict(x0=3.75, w=10.37, pitch=12.38, y=(-34.5, -26.5), r=0.6)   # rear deck pockets: first inner X, width, pitch, Y span, corner R
REAR_C = dict(half=2.75, y=(-30.0, -26.5), r=1.2)                       # centre rear pocket
# ---- base-panel seat
SEAT_Z = BASE_Z0 + BASE_T                     # top of the base panel skin = Z of the rabbet floor
RABBET_GROW = 0.05                            # the rabbet is the panel outline grown by this
PAD = dict(c=(22.5, -30.3), s=9.1, margin=0.3, z=(-0.1, 0.3))   # N10 preload pad: centre, side, recess margin (0.25 fillet), Z span about SEAT_Z
SQUARE = dict(x0=25.5, depth=2.0, up=2.0, over=0.05)            # squared rear corner behind the gearbox plates: inner |X|, Y depth, Z over the floor
ROUND_R, ROUND_Y, ROUND_Z = 4.5, (-25.5, -22.4), (4.4, 9.4)   # stop wall lower inner edge R4.5 (STEP): radius, cutter Y span (through the corner fillet too), Z span of the round
# ---- column bores and switch slot (NO-CHANGE: owned by the heat-set worker)
HOLE_R, CH_R, CH_H = 1.5, 2.1, 0.6            # M2 heat-set hole R, chamfer outer R, chamfer height
SW_SLOT = dict(x0=23.0, w=4.0, y0=-11.6, l=12.0, r=0.45, z0=16.0)   # slot beside the top panel: inner edge, width, front Y, length, corner R, floor Z
SW_PILOT = dict(r=0.85, pitch=15.0, down=3.0)   # switch pilot R, Y pitch about the slot centre, depth under the deck


def _pocket(poly, c):
    return _ext(poly, "xy", c["deck"] + POCKET_Z[0], c["deck"] + POCKET_Z[1])


def deck_pockets(c):
    """Lightening pockets seen from below: the two X triangles, two side triangles, four rear boxes, the centre rear box."""
    X, k = X_RIB, X_SLOPE
    up = [(0.0, X_UP[0]), (X, X_UP[0] + k * X), (X, X_UP[1])]
    lo = [(0.0, X_LO[0]), (X, X_LO[0] - k * X), (X, X_LO[1]), (X_NOTCH, X_LO[1]), (X_NOTCH, X_LO[2]), (0.0, X_LO[2])]
    out = [_pocket(_round(sym(p), r_out=X_R), c) for p in (up, lo)]
    R = REAR_P
    boxes = [rect(R["x0"] + i * R["pitch"], R["x0"] + i * R["pitch"] + R["w"], *R["y"]) for i in range(2)]
    side = _pocket(_round(Polygon(SIDE_TRI), r_out=SIDE_R), c)
    rear = [_pocket(_round(p, r_out=R["r"]), c) for p in boxes]
    mid = _pocket(_round(rect(-REAR_C["half"], REAR_C["half"], *REAR_C["y"]), r_out=REAR_C["r"]), c)
    return out + [mid] + both(side, *rear)


def seat_cuts(c):
    """Rabbet for the base panel, N10 preload pad recess, squared rear corner."""
    from .tub import _panel_outline
    z0, (xi, yi0, _) = c["z0"], inner(c)
    out = [_ext(_panel_outline(RABBET_GROW), "xy", z0 - 1, SEAT_Z)]
    (pcx, pcy), h = PAD["c"], PAD["s"] / 2 + PAD["margin"]
    pad = _box(pcx - h, pcx + h, pcy - h, pcy + h, SEAT_Z + PAD["z"][0], SEAT_Z + PAD["z"][1])
    S = SQUARE
    corner = _box(S["x0"], xi + S["over"], yi0 - S["over"], yi0 + S["depth"], z0 + S["up"], c["deck"])
    return out + both(pad, corner)


def stop_wall_round(c):
    """Motor stop wall: lower inner edge rounded (STEP)."""
    x0, z0, z1 = STOP_X0, *ROUND_Z
    x1 = x0 + ROUND_R
    fil = rect(x0, x1, z0, z1).difference(Point(x1, z1).buffer(ROUND_R, SEG))
    return both(_ext(fil, "xz", *ROUND_Y))


def column_bores(c):
    """NO-CHANGE: owned by the heat-set worker. Hole with 0.6 chamfers both ends (STEP: 3.0 bore through, no pilot)."""
    z0, z1, out = c["z0"], c["z1"], []
    for px, py in INS:
        out.append(_cyl(HOLE_R, z0 - 1, z1 + 1, (px, py), "z"))
        out.append(cone(CH_R, HOLE_R, CH_H, (px, py, SEAT_Z - EPS)))
        out.append(cone(CH_R, HOLE_R, CH_H, (px, py, z1 + EPS), up=False))
    return out



def switch_slot(c):
    """NO-CHANGE: owned by the heat-set worker. Switch slot in the deck beside the top panel and its two M2 pilots."""
    S, P = SW_SLOT, SW_PILOT
    slot = rect(S["x0"], S["x0"] + S["w"], S["y0"], S["y0"] + S["l"])
    out = [_ext(_round(slot, r_out=S["r"]), "xy", S["z0"], c["z1"] + 1)]
    yc = S["y0"] + S["l"] / 2
    for yy in (yc + P["pitch"] / 2, yc - P["pitch"] / 2):
        out.append(_cyl(P["r"], c["deck"] - P["down"], c["z1"] + 1, (SWX, yy), "z"))
    return out
