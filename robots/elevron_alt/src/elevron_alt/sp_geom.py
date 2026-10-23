"""Side_Panel_alt_sm body (TPU, right-hand part, STEP frame) from relations (params_side): a drafted wheel guard round
both tyres (solid at the front, a shell with grip grooves over the rear tyre), the plate on the side boss with its lip,
flanks from the plate to the guard ends, tongue / crossbar / fork root round the outer chassis tab, and the fork."""
import math

import build123d as bd
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _I, _ext, _mirror_x, _solid
from .chassis import halfspace
from .params_chassis import AXLE_Y, AXLE_Z, HY, TAB_HOLE_DY, TAB_HOLE_Z

from .params_side import *  # noqa: F401,F403

BIG = 1e3
B_Y0, B_K = UNDER


def bottom_z(y):
    return B_K * (B_Y0 - y)


def under_b():
    """Everything below the underside plane."""
    return halfspace((0, B_Y0, 0), (0, -B_K, -1), BIG)


def _r(z, off=0.0):
    return GUARD_R0 - off - z * math.tan(math.radians(GUARD_DRAFT))


def _drafted(spine, off, z0):
    """Solid of the points within _r(z, off) of a spine (point or y segment at GUARD_X) from z0 up to its apex."""
    z1 = (GUARD_R0 - off) / math.tan(math.radians(GUARD_DRAFT)) - 0.01
    r0, r1 = _r(z0, off), _r(z1, off)
    pl = lambda y, z: bd.Plane(origin=(GUARD_X, y, z), z_dir=(0, 0, 1))
    if len(spine) == 1:
        return bd.Solid.make_cone(r0, max(r1, 0.01), z1 - z0, pl(spine[0], z0))
    ya, yb = spine
    s = [bd.Solid.make_cone(r0, max(r1, 0.01), z1 - z0, pl(y, z0)) for y in (ya, yb)]
    prof = Polygon([(GUARD_X - r0, z0), (GUARD_X + r0, z0), (GUARD_X + max(r1, 0.01), z1), (GUARD_X - max(r1, 0.01), z1)])
    s.append(_ext(prof, "xz", 0, yb - ya).moved(bd.Location((0, ya, 0))))
    return _U(*s)


def wells():
    return _U(_cyl(WELL_R, -BIG / 10, BIG / 10, (-AXLE_Y, AXLE_Z), "x"), _cyl(WELL_R, *WELL_X, (AXLE_Y, AXLE_Z), "x"))   # front: right across


def guard():
    z0 = -5.0
    off = GUARD_T / math.cos(math.radians(GUARD_DRAFT))
    out = _U(_drafted((GUARD_Y[0],), 0, z0), _drafted(GUARD_Y[1:], 0, z0))
    rear = _I(_drafted(GUARD_Y[1:], 0, z0), _box(WELL_X[0], BIG, -BIG, BIG, -BIG, CROSS_TOP))
    rear = _S(rear, _box(-BIG, WELL_X[1], GUARD_Y[1] - 0.8, CROSS_Y0, -BIG, BIG))          # over the tyre only its outer wall
    out = _U(_I(_drafted((GUARD_Y[0],), 0, z0), _box(-BIG, BIG, -BIG, BIG, -BIG, CROSS_TOP)), rear)
    hollow = _I(_drafted(GUARD_Y[1:], off, z0), _box(-BIG, BIG, GUARD_Y[1], GUARD_Y[2], -BIG, BIG))
    return _S(out, hollow, grooves())     # the rear guard is a shell over the tyre, closed at the crossbar; the front one solid


def grooves():
    """Diagonal grip grooves pressed GROOVE[3] into the rear guard's outer face."""
    y0, pitch, w, depth, (za, zb), dydz, n = GROOVE
    skin = _S(_drafted(GUARD_Y[1:], 0, -5.0), _drafted(GUARD_Y[1:], depth / math.cos(math.radians(GUARD_DRAFT)), -5.0))
    bands = []
    for k in range(n):
        c = y0 + k * pitch
        bands.append(Polygon([(c - w / 2 + dydz * (za - 3), za), (c + w / 2 + dydz * (za - 3), za), (c + w / 2 + dydz * (zb - 3), zb), (c - w / 2 + dydz * (zb - 3), zb)]))
    g = _ext(unary_union(bands).intersection(sbox(GUARD_Y[1], -BIG, GUARD_Y[2], BIG)), "yz", GUARD_X, BIG / 10)
    return _I(skin, g)


def plate():
    cy, r, top, flat = PLATE_OB[0], PLATE_OB[1], PLATE_OB[2], PLATE_OB[3]
    ob = unary_union([Point(-cy, AXLE_Z).buffer(r, 64), Point(cy, AXLE_Z).buffer(r, 64), Point(-flat, top), Point(flat, top)]).convex_hull
    p = _S(_ext(ob, "yz", PLATE_X0, 50), halfspace((PLATE_OUT[2] / PLATE_OUT[0], 0, 0), (PLATE_OUT[0], 0, PLATE_OUT[1]), BIG))
    boss = unary_union([LineString([(-cy, AXLE_Z), (cy, AXLE_Z)]).buffer(LIP_IN_R, 64)])
    lip = _ext(ob.difference(boss), "yz", LIP_X0, PLATE_X0)
    return _U(p, lip)


def _above(n, d):
    """Cut tool: the part with n.(y, z) > d."""
    ny, nz = n
    return halfspace((0, 0, d / nz), (0, ny, nz), BIG)


def rear():
    """Tongue in the tab gap, crossbar round the outer chassis tab, fork root out to the fork."""
    slope, top1, ttop = _above(REAR_SLOPE[:2], REAR_SLOPE[2]), _above(ROOT_TOP[:2], ROOT_TOP[2]), _above(TONGUE_TOP[:2], TONGUE_TOP[2])
    front = halfspace((0, TONGUE_FRONT[2] / TONGUE_FRONT[0], 0), (0, -TONGUE_FRONT[0], -TONGUE_FRONT[1]), BIG)
    tongue = _S(_box(*TONGUE_X, 20, 70, -1, 20), ttop, slope, front)
    x0, x1, yr, ch = TAB_POCKET
    rc = POCKET_R
    plan = sbox(x1, CROSS_Y0, FORK_X[1], 70).union(sbox(x0, yr, FORK_X[1], 70)).union(sbox(x1, CROSS_Y0 + rc, FORK_X[1], 70))
    plan = plan.difference(sbox(x1, CROSS_Y0, x1 + rc, CROSS_Y0 + rc)).union(Point(x1 + rc, CROSS_Y0 + rc).buffer(rc, 64))
    low = _ext(plan, "xy", -1, CROSS_TOP)
    hi = _S(_box(x0, FORK_X[1], CROSS_Y0, 70, -1, CROSS_TOP), halfspace((0, ch, 0), (0, -1, -1), BIG))   # above the pocket's underside chamfer
    cross = _S(_U(low, hi), slope)
    nx, ny, nz, d = ROOT_EDGE
    side = halfspace((d / nx, 0, 0), (nx, ny, nz), BIG)      # beyond the root's inner face (the fork side)
    root = _S(_I(_box(x0, FORK_X[1], yr - 1, 70, -1, CROSS_TOP), _box(-BIG, BIG, -BIG, BIG, -BIG, BIG).cut(side)), _I(slope, top1))
    return _U(tongue, cross, root)


def fork():
    """Fork prong: FORK_T over the underside, the root top plane carried on until it drops under that, a tooth riser
    near the tip and the tip's top plane down to the underside."""
    y_tip, tp, ya, yb = FORK_TIP
    f = _box(*FORK_X, CROSS_Y0, y_tip, -10, CROSS_TOP)
    thick = halfspace((0, B_Y0, FORK_T / math.cos(math.atan(B_K))), (0, B_K, 1), BIG)       # above FORK_T over the underside
    body = _I(_I(thick, _above(ROOT_TOP[:2], ROOT_TOP[2])), _box(-BIG, BIG, -BIG, ya, -BIG, BIG))
    tooth = _I(halfspace((0, ya, bottom_z(ya) + FORK_T), (0, -FORK_RISER[0], FORK_RISER[1]), BIG), _box(-BIG, BIG, ya, BIG, -BIG, BIG))
    return _S(f, body, tooth, _above(tp[:2], tp[2]))


def struts():
    """Flanks between the plate's top and each wheel guard's end: under a plane falling outwards from the plate top."""
    xs, zs, k = STRUT_TOP
    blk = _U(*[_box(PLATE_X0, BIG / 10, *sorted((sy * STRUT_Y0, sy * STRUT_Y1)), -5, zs) for sy in (-1, 1)])
    cy, r, top, flat = PLATE_OB
    ob = unary_union([Point(-cy, AXLE_Z).buffer(r, 64), Point(cy, AXLE_Z).buffer(r, 64), Point(-flat, top), Point(flat, top)]).convex_hull
    blk = _I(blk, _U(_ext(ob, "yz", PLATE_X0 - 1, xs), _box(xs, BIG, -BIG, BIG, -BIG, BIG)))   # inside the plate outline until the flank leaves it
    return _S(blk, halfspace((xs, 0, zs), (k, 0, 1), BIG))


def sp():
    s = _U(guard(), plate(), rear(), fork(), struts())
    s = _S(s, wells())
    nonfork = _S(_box(-BIG, BIG, -BIG, BIG, -BIG, 0), _box(*FORK_X, 40, BIG, -BIG, BIG))
    s = _S(s, under_b(), nonfork)
    return _solid(s)
