"""[W1] Insert columns and what hangs off them: round rear boss, flared feet, corner blocks, motor stop wall, N10 key tab and ledge."""
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
import math
from .tub_util import both, rect, cone, inner

OVER = 0.1                       # solids reach this far into the deck / walls so they fuse
EPS = 0.001                      # cones start this far inside the column so they fuse
COL_R, FOOT_R, FOOT_Z, FOOT_H = 2.75, 3.7, 5.2, 1.4   # column boss R; foot R (56 deg flare, prints deck-down), foot cylinder top Z, flare height
BOSS_FILLET_R = 1.0              # concave fillet where the rear-centre boss meets the rear wall (STEP RV01: boss half width 3.0 at 0.2 mm off the wall)
NOSE_SEG = 48                    # buffer resolution of the corner-block rounds
# measured corner blocks (STEP), per block: inner face X, nose-end Y, wall-end Y, fillet-end Y, nose R, wall-fillet R
CORNER_BLOCKS = ((22.25, 7.65, 13.1, 13.0, 2.5, 0.8), (22.21, -18.85, -23.45, -23.4, 2.6, 0.9))
STOP_X0, STOP_Y = 17.7, (-25.4, -23.4)       # motor stop wall: inner end |X|, Y span (the N10 gearbox bears on its rear face)
KEY_Y0, KEY_Z0 = -26.15, N10_TOP - 1.0       # key tab between the gearbox plates: front Y, bottom Z
LEDGE_X0, LEDGE_Y0 = 20.0, -27.3             # 0.4 ledge over the gearbox plates: inner |X|, front Y


def _nose(x0, y0, dx, dy, r):
    """The corner region at (x0, y0) outside an R r round (dx, dy: directions into the block)."""
    q = rect(x0, x0 + dx * r, y0, y0 + dy * r)
    return q.difference(Point(x0 + dx * r, y0 + dy * r).buffer(r, NOSE_SEG))


def _corner_block(c, x0, yn, yw, yf, rn, rf):
    """Plan of a corner block between the inner wall (+X) and x0: a nose round at (x0, yn), small fillets into the walls."""
    xi = inner(c)[0]
    dy = 1 if yw > yn else -1
    blk = rect(x0, xi + OVER, yn, yw).difference(_nose(x0, yn, 1, dy, rn))
    return blk.union(_nose(x0, yf, -1, -dy, rf)).union(_nose(xi, yn, -1, -dy, rf))


def feet(c):
    """Round rear-centre boss plus a flared foot under every insert column."""
    top = c["deck"] + OVER
    out = [_cyl(COL_R, c["z0"], top, INS[-1], "z")]
    for px, py in INS:
        out.append(_cyl(FOOT_R, c["z0"], FOOT_Z, (px, py), "z"))
        out.append(cone(FOOT_R, COL_R, FOOT_H, (px, py, FOOT_Z - EPS)))
    return out


def boss_fillet(c):
    """+X side fillet between the rear-centre boss and the rear wall, as a plan region extruded over the column height."""
    bx, by = INS[-1]
    yw, rf = inner(c)[1], BOSS_FILLET_R
    fy = yw + rf
    fx = bx + math.sqrt((COL_R + rf) ** 2 - (fy - by) ** 2)          # fillet circle tangent to the wall and to the boss
    d = math.hypot(fx - bx, fy - by)
    tb = (bx + COL_R * (fx - bx) / d, by + COL_R * (fy - by) / d)    # tangent point on the boss
    region = Polygon([(bx, yw), (fx, yw), (fx, fy), tb, (bx, by)]).difference(Point(fx, fy).buffer(rf, NOSE_SEG)).difference(
        Point(bx, by).buffer(COL_R, NOSE_SEG))
    return _ext(region, "xy", c["z0"], c["deck"] + OVER)


def half_adds(c):
    """+X half: corner blocks, motor stop wall, N10 key tab and ledge (all hang from the deck: printed deck-down)."""
    xo, top = inner(c)[0] + OVER, c["deck"] + OVER
    blocks = [_ext(_corner_block(c, *blk), "xy", c["z0"], top) for blk in CORNER_BLOCKS]
    stop = _box(STOP_X0, xo, *STOP_Y, c["z0"], top)
    key = _box(N10_KEY[0], N10_KEY[1], KEY_Y0, STOP_Y[1], KEY_Z0, top)
    ledge = _box(LEDGE_X0, xo, LEDGE_Y0, STOP_Y[1], N10_TOP + OVER, top)
    return blocks + [stop, key, ledge, boss_fillet(c)]


def column_adds(c):
    return feet(c) + both(*half_adds(c))
