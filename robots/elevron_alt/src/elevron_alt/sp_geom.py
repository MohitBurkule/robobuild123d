"""Side_Panel_alt_sm body (TPU, right-hand part, STEP frame) from relations, measured off the RVRN_revdev STEP faces.
Work in progress: pieces are named after the features they reproduce."""
import math

import build123d as bd
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _I, _ext, _mirror_x, _solid
from .chassis import halfspace
from .params_chassis import AXLE_Y, AXLE_Z, HY, TAB_HOLE_DY, TAB_HOLE_Z

BIG = 1e3
B_Y0, B_K = 46.16, 0.0853               # underside plane: z 0 at y B_Y0, rising forward at B_K
GUARD_X, GUARD_Y = 39.5, (-16.8, 16.8, 35.8)   # wheel-guard spine: front point, rear segment
GUARD_R0, GUARD_DRAFT, GUARD_T = 12.814, 35.03, 3.28
GROOVE = (16.98, 6.0, 3.0, 0.5, (2.62, 10.81), -0.857, 4)   # first centre y at z 3, pitch, width, depth, z span, dy/dz, count
WELL_R, WELL_X = 12.0, (31.5, 42.5)     # wheel wells round both axles: rear one from the boss lip out to the guard's inner face
PLATE_X0, PLATE_OUT = 32.5, (0.966, 0.259, 35.53)   # plate on the boss face; slanted outer plane n.x = d
PLATE_OB = (7.0, 7.0, 16.0, 3.0)        # plate outline: obround centres +-y, radius, top z over |y| <= ...
LIP_X0, LIP_IN_R = 31.5, 5.3
TONGUE_X = (20.75, 23.25)
TONGUE_FRONT = (0.997, 0.078, 33.51)    # -n.(y,z) = -d
TONGUE_TOP = (0.217, 0.976, 21.86)
REAR_SLOPE = (0.819, 0.574, 39.82)      # crossbar / tongue rear face (y, z)
ROOT_TOP = (0.340, 0.940, 24.10)        # fork root top (y, z)
CROSS_Y0, CROSS_TOP = 37.8, 14.0
TAB_POCKET = (23.25, 32.25, 41.5, 48.58)   # pocket round the chassis outer tab: x span, rear face y, underside chamfer y + z
ROOT_EDGE = (-0.707, 0.579, 0.406, 7.11)   # fork-root inner face n.(x, y, z) = d
FORK_X = (35.76, 41.5)
FORK_T = 4.0
FORK_TIP = (98.61, (0.499, 0.867, 45.26), 83.22, 84.74)   # tip y, tip top plane, tooth riser y span
FORK_RISER = (0.867, 0.499)            # tooth riser face normal (-y, +z)


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
    rear = _S(rear, _box(-BIG, WELL_X[1], GUARD_Y[1], GUARD_Y[2], -BIG, BIG))          # over the tyre only its outer wall
    out = _U(_drafted((GUARD_Y[0],), 0, z0), rear)
    hollow = _I(_drafted(GUARD_Y[1:], off, z0), _box(-BIG, BIG, GUARD_Y[1], CROSS_Y0, -BIG, BIG))
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
    rc = 3.0
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


def sp():
    s = _U(guard(), plate(), rear(), fork())
    s = _S(s, wells())
    nonfork = _S(_box(-BIG, BIG, -BIG, BIG, -BIG, 0), _box(*FORK_X, 40, BIG, -BIG, BIG))
    s = _S(s, under_b(), nonfork)
    return _solid(s)


def sp_l():
    return _solid(_mirror_x(sp()))


def sp_ref_frame():
    """Ours in the right STEP solid's frame (that solid sits 0.25 inboard of the mirror of the left one)."""
    return sp().moved(bd.Location((-0.25, 0, 0)))
