"""[W1] Tub shell cuts: deck lightening pockets, base-panel seat (rabbet, ring-boss recesses, preload pad recess, squared corner),
motor stop-wall round, and (unchanged, owned by the heat-set worker) the column bores and the switch slot with its pilots."""
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_util import both, rect, sym, cone, inner
from .tub_shell_cols import STOP_X0, STOP_Y, CORNER_BLOCKS, EPS, OVER

# ---- deck pockets (STEP RV01 at deck Z): an X of 2 mm ribs, two diagonals; 1 mm skin stays
POCKET_Z = (-0.5, 1.0)                        # cutter Z span relative to the deck underside
X_RIB, X_SLOPE, X_R = CORNER_BLOCKS[0][0], 0.6404, 0.8      # half width of the X pockets (= the corner block face), diagonal slope, corner R
X_UP = (-3.07, WALL_IN_FRONT - 0.6)                          # front pocket: apex Y on the axis, top edge Y
X_LO = (-8.13, STOP_Y[1], STOP_Y[1] - 0.2)                  # rear pocket: apex Y, rear edge Y beside the blocks, rear edge Y between the stop walls
X_NOTCH = STOP_X0                                # |X| where the rear pocket steps back between the motor stop walls
SIDE_X, SIDE_DIAG = TOP_X - 0.5, dict(x=19.51, y_up=4.51, k_up=0.640, y_lo=-15.71, k_lo=0.6407)   # side pocket: right edge |X| (= the switch pad edge), diagonals through (x, y) with slope k
SIDE_TRI = [(3.72, -5.59), (SIDE_X, SIDE_DIAG["y_up"] + SIDE_DIAG["k_up"] * (SIDE_X - SIDE_DIAG["x"])),
            (SIDE_X, SIDE_DIAG["y_lo"] - SIDE_DIAG["k_lo"] * (SIDE_X - SIDE_DIAG["x"]))]
X_APEX_R, X_APEX_REACH = 2.0, 4.0              # RV01 R2 round at the pocket apex on the axis (the other corners stay X_R), and the radius round the apex it replaces
SIDE_R = 1.9                                  # apex R towards the centre
REAR_Y1 = -26.5                               # front edge of the rear pockets (shared)
RIB, WEB, REAR_W = 1.0, 2.01, 10.37          # rib to the centre pocket, web between the two side pockets, width of each (STEP; they end 1.0 off the inner wall)
REAR_C = dict(half=COL_R, y=(-30.0, REAR_Y1), r=1.2)                    # centre rear pocket: as wide as the rear boss
REAR_P = dict(x0=REAR_C["half"] + RIB, w=REAR_W, pitch=REAR_W + WEB, y=(WALL_IN_REAR + 1.1, REAR_Y1), r=1.5)   # rear deck pockets: first inner X, width, pitch, Y span (1.1 skin off the rear wall), corner R
# ---- base-panel seat
SEAT_Z = BASE_Z0 + BASE_T                     # top of the base panel skin = Z of the rabbet floor
RABBET_GROW = 0.05                            # the rabbet is the panel outline grown by this
PAD = dict(c=PRELOAD_PAD["c"], s=PRELOAD_PAD["s"], margin=0.3, z=(-0.1, 0.3))   # N10 preload pad: centre, side, recess margin (0.25 fillet), Z span about SEAT_Z
SQUARE = dict(x0=25.5, depth=CH_WALL, up=SEAT_Z - CH_Z0, over=0.05)            # squared rear corner behind the gearbox plates: inner |X|, Y depth, Z over the floor
ROUND_R, ROUND_Y, ROUND_Z = 4.5, (STOP_Y[0] - OVER, STOP_Y[1] + 1.0), (SEAT_Z - OVER, 9.4)   # stop wall lower inner edge R4.5 (STEP): radius, cutter Y span (through the corner fillet too), Z span of the round
# ---- column bores and switch slot (NO-CHANGE: owned by the heat-set worker)
HOLE_R, CH_H = 1.5, 0.6; CH_R = HOLE_R + CH_H            # M2 heat-set hole R, chamfer outer R, chamfer height
_SW_L = 12.0                                  # switch slot length, centred on the switch catalog Y
SW_SLOT = dict(x0=TOP_X, w=4.0, y0=ELEC["switch_yz"][0] - _SW_L / 2, l=_SW_L, r=0.45, z0=SW_BOLT_Z)   # slot beside the top panel: inner edge, width, front Y, length, corner R, floor Z
SW_PILOT = dict(r=0.85, pitch=SW_SCREW_Y[0] - SW_SCREW_Y[1], down=3.0)   # switch pilot R, Y pitch about the slot centre, depth under the deck


def _pocket(poly, c):
    return _ext(poly, "xy", c["deck"] + POCKET_Z[0], c["deck"] + POCKET_Z[1])


def _apex_round(poly, apex):
    """`poly` with its corners rounded X_R except the one at `apex` (on the axis), rounded X_APEX_R."""
    zone = Point(apex).buffer(X_APEX_REACH, SEG)
    return _round(poly, r_out=X_R).difference(zone).union(_round(poly, r_out=X_APEX_R).intersection(zone)).buffer(0)


def deck_pockets(c):
    """Lightening pockets seen from below: the two X triangles, two side triangles, four rear boxes, the centre rear box."""
    X, k = X_RIB, X_SLOPE
    up = [(0.0, X_UP[0]), (X, X_UP[0] + k * X), (X, X_UP[1])]
    lo = [(0.0, X_LO[0]), (X, X_LO[0] - k * X), (X, X_LO[1]), (X_NOTCH, X_LO[1]), (X_NOTCH, X_LO[2]), (0.0, X_LO[2])]
    out = [_pocket(_apex_round(sym(p), p[0]), c) for p in (up, lo)]
    R = REAR_P
    boxes = [rect(R["x0"] + i * R["pitch"], R["x0"] + i * R["pitch"] + R["w"], *R["y"]) for i in range(2)]
    side = _pocket(_round(Polygon(SIDE_TRI), r_out=SIDE_R), c)
    rear = [_pocket(_round(p, r_out=R["r"]), c) for p in boxes]
    mid = _pocket(_round(rect(-REAR_C["half"], REAR_C["half"], *REAR_C["y"]), r_out=REAR_C["r"]), c)
    return out + [mid] + both(side, *rear)


def seat_cuts(c):
    """Rabbet for the base panel, N10 preload pad recess, squared rear corner."""
    from .panel_base import rabbet
    z0, (xi, yi0, _) = c["z0"], inner(c)
    out = [rabbet(RABBET_GROW, z0 - 1, SEAT_Z)]
    (pcx, pcy), h = PAD["c"], PAD["s"] / 2 + PAD["margin"]
    pad = _box(pcx - h, pcx + h, pcy - h, pcy + h, SEAT_Z + PAD["z"][0], SEAT_Z + PAD["z"][1])
    S = SQUARE
    corner = _box(S["x0"], xi + S["over"], yi0, yi0 + S["depth"], z0 + S["up"], c["deck"])
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
