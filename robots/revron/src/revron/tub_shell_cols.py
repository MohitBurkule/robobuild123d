"""[W1] Insert columns and what hangs off them: round rear boss, flared feet, corner blocks, motor stop wall, N10 key tab and ledge."""
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
import math
from .tub_util import both, rect, cone, inner

OVER = OVERLAP                   # solids reach this far into the deck / walls so they fuse
EPS = 0.001                      # cones start this far inside the column so they fuse
FOOT_R, FOOT_Z, FOOT_H = 3.7, 5.2, 1.4   # (COL_R in params) foot R (56 deg flare, prints deck-down), foot cylinder top Z, flare height
BOSS_FILLET_R = 1.0              # concave fillet (RV01 Fillet4 R1) where the rear-centre boss meets the rear wall: the boss runs straight (|x| = COL_R) from its round to the wall
NOSE_SEG = 48                    # buffer resolution of the corner-block rounds
REAR_BLOCK_WALL_R = 1.0          # rear corner block: nose-end fillet into the side wall (RV01 R1)
# measured corner blocks (STEP), per block: inner face X, nose-end Y, wall-end Y, fillet-end Y, nose R, wall-fillet R
# Each block's face and nose are tangent to the insert column boss of its corner (face X = column X - COL_R, nose Y = column Y -/+ COL_R);
# the wall end overshoots the inner wall by OVER and the fillet ends on the inner wall / stop-wall face.
STOP_X0, STOP_Y = SA_X0, (-25.4, KEY_SPAN[1])   # motor stop wall: inner end |X| (independent: gearbox-rear bearing), Y span (the N10 gearbox bears on its rear face)
CORNER_BLOCKS = ((INS[1][0] - COL_R, INS[1][1] - COL_R, WALL_IN_FRONT + OVER, WALL_IN_FRONT, 2.5, 0.8),
                 (22.21, INS[3][1] + COL_R, STOP_Y[1] - 0.05, STOP_Y[1], 2.6, REAR_BLOCK_WALL_R))   # rear block face 22.21: STEP measure, 0.04 off the column tangent
KEY_DROP = 1.0                              # the key tab reaches this far below the plate top so it really keys between the N10 gearbox plates (STEP: flush, 0.1 would not stop the motor)
KEY_Y0, KEY_Z0 = KEY_SPAN[0], N10_TOP - KEY_DROP   # key tab between the gearbox plates: front Y, bottom Z
LEDGE_X0, LEDGE_Y0 = 20.0, -27.3             # 0.4 ledge over the gearbox plates: inner |X|, front Y
LEDGE_FILLET_R = 1.5                         # RV01 R1.5 vertical fillets of the ledge: its inner end into the stop wall's front face, its front face into the side wall


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
    """Rear-centre boss (a round at the column with straight flanks to the rear wall) plus a flared foot under every insert column."""
    top = c["deck"] + OVER
    bx, by = INS[-1]
    out = [_cyl(COL_R, c["z0"], top, INS[-1], "z"), _ext(rect(bx - COL_R, bx + COL_R, inner(c)[1] - OVER, by), "xy", c["z0"], top)]
    for px, py in INS:
        out.append(_cyl(FOOT_R, c["z0"], FOOT_Z, (px, py), "z"))
        out.append(cone(FOOT_R, COL_R, FOOT_H, (px, py, FOOT_Z - EPS)))
    return out


def boss_fillet(c):
    """+X side R BOSS_FILLET_R fillet between the boss's straight flank and the rear wall, as a plan region extruded over the column height."""
    bx, _ = INS[-1]
    yw, rf = inner(c)[1], BOSS_FILLET_R
    fx = bx + COL_R + rf                                              # fillet circle: tangent to the flank (x = bx + COL_R) and the wall
    region = rect(bx + COL_R, fx, yw - OVER, yw + rf).difference(Point(fx, yw + rf).buffer(rf, NOSE_SEG))
    return _ext(region, "xy", c["z0"], c["deck"] + OVER)


def ledge_fillets(c):
    """Two R LEDGE_FILLET_R vertical fillets of the ledge (plan regions over the ledge's Z span): inner end x = LEDGE_X0 into the stop wall's front face
    (y = STOP_Y[0]), and front face y = LEDGE_Y0 into the inner side wall."""
    xi, r = inner(c)[0], LEDGE_FILLET_R
    z0, z1 = N10_TOP + OVER, c["deck"] + OVER
    out = []
    for cx, cy in ((LEDGE_X0, STOP_Y[0]), (xi, LEDGE_Y0)):
        reg = rect(cx - r, cx + OVER, cy - r, cy + OVER).difference(Point(cx - r, cy - r).buffer(r, NOSE_SEG))
        out.append(_ext(reg, "xy", z0, z1))
    return out


def half_adds(c):
    """+X half: corner blocks, motor stop wall, N10 key tab and ledge (all hang from the deck: printed deck-down)."""
    xo, top = inner(c)[0] + OVER, c["deck"] + OVER
    blocks = [_ext(_corner_block(c, *blk), "xy", c["z0"], top) for blk in CORNER_BLOCKS]
    stop = _box(STOP_X0, xo, *STOP_Y, c["z0"], top)
    key = _box(N10_KEY[0], N10_KEY[1], KEY_Y0, STOP_Y[1], KEY_Z0, top)
    ledge = _box(LEDGE_X0, xo, LEDGE_Y0, STOP_Y[1], N10_TOP + OVER, top)
    return blocks + [stop, key, ledge, boss_fillet(c)] + ledge_fillets(c)


def column_adds(c):
    return feet(c) + both(*half_adds(c))
