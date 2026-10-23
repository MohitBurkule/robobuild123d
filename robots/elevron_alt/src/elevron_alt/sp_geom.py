"""Side_Panel_alt_sm body (TPU, right-hand part, STEP frame) from relations (params_side): a drafted wheel guard round
both tyres (solid at the front, a shell with grip grooves over the rear tyre), the plate on the side boss with its lip,
flanks from the plate to the guard ends, tongue / crossbar / fork root round the outer chassis tab, and the fork."""
import math

import build123d as bd
from shapely.geometry import Point, Polygon, LineString, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _I, _ext as _ext_poly, _face, _mirror_x, _solid


def _ext(poly, plane, a0, a1, arcs=True):
    """Prism of an outline with its polygonised arcs turned back into true arcs (cylinders, not facets)."""
    return _ext_poly(poly, plane, a0, a1, arcs=arcs)
from .chassis import halfspace
from .params_chassis import AXLE_Y, AXLE_Z, HY, TAB_HOLE_DY, TAB_HOLE_Z

from .params_side import *  # noqa: F401,F403

BIG = 1e3
TOOL = BIG / 10                         # cut tools reach this far
SEG = 64                                # arc segments per quarter
EPS = 0.01                              # sliver to keep tool faces off part faces
Z_BELOW = -5.0                          # drafted solids start below the floor
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
    z1 = (GUARD_R0 - off) / math.tan(math.radians(GUARD_DRAFT)) - EPS
    r0, r1 = _r(z0, off), _r(z1, off)
    pl = lambda y, z: bd.Plane(origin=(GUARD_X, y, z), z_dir=(0, 0, 1))
    if len(spine) == 1:
        return bd.Solid.make_cone(r0, max(r1, EPS), z1 - z0, pl(spine[0], z0))
    ya, yb = spine
    s = [bd.Solid.make_cone(r0, max(r1, EPS), z1 - z0, pl(y, z0)) for y in (ya, yb)]
    prof = Polygon([(GUARD_X - r0, z0), (GUARD_X + r0, z0), (GUARD_X + max(r1, EPS), z1), (GUARD_X - max(r1, EPS), z1)])
    s.append(_ext(prof, "xz", 0, yb - ya).moved(bd.Location((0, ya, 0))))
    return _U(*s)


def wells():
    return _U(_cyl(WELL_R, -TOOL, TOOL, (-AXLE_Y, AXLE_Z), "x"), _cyl(WELL_R, *WELL_X, (AXLE_Y, AXLE_Z), "x"))   # front: right across


def guard():
    z0 = Z_BELOW
    off = GUARD_T / math.cos(math.radians(GUARD_DRAFT))
    out = _U(_drafted((GUARD_Y[0],), 0, z0), _drafted(GUARD_Y[1:], 0, z0))
    rear = _I(_drafted(GUARD_Y[1:], 0, z0), _box(WELL_X[0], BIG, -BIG, BIG, -BIG, CROSS_TOP))
    rear = _S(rear, _box(-BIG, WELL_X[1], GUARD_Y[1] - GUARD_FRONT_CLR, CROSS_Y0, -BIG, BIG))          # over the tyre only its outer wall
    xf = WELL_X[1] + GUARD_TIP_R                               # tip round: tangent to the inner face and the drafted face
    a = math.radians(GUARD_DRAFT)
    zc = (GUARD_R0 - (xf - GUARD_X) - GUARD_TIP_R / math.cos(a)) / math.tan(a)
    tip = _S(_box(WELL_X[1], xf + GUARD_TIP_R * math.cos(a), -BIG, BIG, zc, BIG), _cyl(GUARD_TIP_R, -TOOL, TOOL, (xf, zc), "y"))
    rear = _S(rear, _I(tip, _box(-BIG, BIG, GUARD_Y[1] - GUARD_FRONT_CLR, CROSS_Y0, -BIG, BIG)))
    out = _U(_I(_drafted((GUARD_Y[0],), 0, z0), _box(-BIG, BIG, -BIG, BIG, -BIG, CROSS_TOP)), rear)
    hollow = _I(_drafted(GUARD_Y[1:], off, z0), _box(-BIG, BIG, GUARD_Y[1], GUARD_Y[2], -BIG, BIG))
    return _S(out, hollow, grooves())     # the rear guard is a shell over the tyre, closed at the crossbar; the front one solid


def grooves():
    """Diagonal grip grooves pressed GROOVE[3] into the rear guard's outer face."""
    y0, pitch, w, depth, (za, zb), dydz, n, zr = GROOVE
    skin = _S(_drafted(GUARD_Y[1:], 0, Z_BELOW), _drafted(GUARD_Y[1:], depth / math.cos(math.radians(GUARD_DRAFT)), Z_BELOW))
    bands = []
    for k in range(n):
        c = y0 + k * pitch
        bands.append(Polygon([(c - w / 2 + dydz * (za - zr), za), (c + w / 2 + dydz * (za - zr), za), (c + w / 2 + dydz * (zb - zr), zb), (c - w / 2 + dydz * (zb - zr), zb)]))
    g = _ext(unary_union(bands).intersection(sbox(GUARD_Y[1] - pitch, -BIG, GUARD_Y[2], BIG)), "yz", GUARD_X, TOOL)
    return _I(skin, g)


def plate():
    cy, r, top, flat = PLATE_OB[0], PLATE_OB[1], PLATE_OB[2], PLATE_OB[3]
    ob = unary_union([Point(-cy, AXLE_Z).buffer(r, SEG), Point(cy, AXLE_Z).buffer(r, SEG), Point(-flat, top), Point(flat, top)]).convex_hull
    p = _S(_ext(ob, "yz", PLATE_X0, TOOL), halfspace((PLATE_OUT[2] / PLATE_OUT[0], 0, 0), (PLATE_OUT[0], 0, PLATE_OUT[1]), BIG))
    boss = unary_union([LineString([(-cy, AXLE_Z), (cy, AXLE_Z)]).buffer(LIP_IN_R, SEG)])
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
    tongue = _S(_box(*TONGUE_X, HY + EPS, TOOL, -1, TOOL), ttop, slope, front)   # its raked front stops at the chassis rear face
    x0, x1, yr, ch = TAB_POCKET
    rc = POCKET_R
    plan = sbox(x1, CROSS_Y0, FORK_X[1], TOOL).union(sbox(x0, yr, FORK_X[1], TOOL)).union(sbox(x1, CROSS_Y0 + rc, FORK_X[1], TOOL))
    plan = plan.difference(sbox(x1, CROSS_Y0, x1 + rc, CROSS_Y0 + rc)).union(Point(x1 + rc, CROSS_Y0 + rc).buffer(rc, SEG))
    low = _ext(plan, "xy", -1, CROSS_TOP)
    hi = _S(_box(x0, FORK_X[1], CROSS_Y0, TOOL, -1, CROSS_TOP), halfspace((0, ch, 0), (0, -1, -1), BIG))   # above the pocket's underside chamfer
    cross = _S(_U(low, hi), slope)
    nx, ny, nz, d = ROOT_EDGE
    side = halfspace((d / nx, 0, 0), (nx, ny, nz), BIG)      # beyond the root's inner face (the fork side)
    root = _S(_I(_box(x0, FORK_X[1], yr - 1, TOOL, -1, CROSS_TOP), _box(-BIG, BIG, -BIG, BIG, -BIG, BIG).cut(side)), _I(slope, top1))
    return _U(tongue, cross, root)


def pocket():
    """Void round the outer chassis tab: open in front and below, its rear wall at the tab end, its outer wall rounding
    into the crossbar's front face, its roof the underside chamfer."""
    x0, x1, yr, ch = TAB_POCKET
    rc = POCKET_R
    plan = sbox(x0, HY - 1, x1, yr).union(sbox(x1, HY - 1, x1 + rc, CROSS_Y0 + rc).difference(Point(x1 + rc, CROSS_Y0 + rc).buffer(rc, SEG)))
    return _S(_ext(plan, "xy", -TOOL, TOOL), halfspace((0, ch, 0), (0, 1, 1), BIG))


def fork():
    """Fork prong: FORK_T over the underside, the root top plane carried on until it drops under that, a tooth riser
    near the tip and the tip's top plane down to the underside."""
    y_tip, tp, ya, yb = FORK_TIP
    f = _box(*FORK_X, CROSS_Y0, y_tip, -TOOL, CROSS_TOP)
    thick = halfspace((0, B_Y0, FORK_T / math.cos(math.atan(B_K))), (0, B_K, 1), BIG)       # above FORK_T over the underside
    body = _I(_I(thick, _above(ROOT_TOP[:2], ROOT_TOP[2])), _box(-BIG, BIG, -BIG, ya, -BIG, BIG))
    tooth = _I(halfspace((0, ya, bottom_z(ya) + FORK_T), (0, -FORK_RISER[0], FORK_RISER[1]), BIG), _box(-BIG, BIG, ya, BIG, -BIG, BIG))
    return _S(f, body, tooth, _above(tp[:2], tp[2]))


def struts():
    """Flanks between the plate's top and each wheel guard's end: under a plane falling outwards from the plate top."""
    xs, zs, k = STRUT_TOP
    blk = _U(*[_box(PLATE_X0, TOOL, *sorted((sy * STRUT_Y0, sy * STRUT_Y1)), Z_BELOW, zs) for sy in (-1, 1)])
    cy, r, top, flat = PLATE_OB
    ob = unary_union([Point(-cy, AXLE_Z).buffer(r, SEG), Point(cy, AXLE_Z).buffer(r, SEG), Point(-flat, top), Point(flat, top)]).convex_hull
    blk = _I(blk, _U(_ext(ob, "yz", PLATE_X0 - 1, xs), _box(xs, BIG, -BIG, BIG, -BIG, BIG)))   # inside the plate outline until the flank leaves it
    return _S(blk, halfspace((xs, 0, zs), (k, 0, 1), BIG))


def rear_flare(n=10, k=8):
    """Concave blend from the fork's outer face down to the rear guard's end at the floor, lofted through sections."""
    r0, gy = GUARD_R0, GUARD_Y[2]
    y1 = gy + math.sqrt(r0 ** 2 - (FLARE_MIN + FORK_X[1] - GUARD_X) ** 2)
    secs = []
    for i in range(n + 1):
        y = CROSS_Y0 + (y1 - CROSS_Y0) * i / n
        xb = GUARD_X + math.sqrt(max(r0 ** 2 - (y - gy) ** 2, 0.0))
        zt = min(CROSS_TOP, max((ROOT_TOP[2] - ROOT_TOP[0] * y) / ROOT_TOP[1], (REAR_SLOPE[2] - REAR_SLOPE[0] * y) / REAR_SLOPE[1]))
        a = xb - FORK_X[1]
        pts = [(FORK_X[1] - EPS, -1.0), (xb, -1.0)] + [(xb - a * math.sin(t), zt - zt * math.cos(t)) for t in [j * math.pi / 2 / k for j in range(k + 1)]]
        pts[-1] = (FORK_X[1] - EPS, zt)
        secs.append(bd.Face(bd.Wire.make_polygon([bd.Vector(x, y, z) for x, z in pts], close=True)))
    return bd.Solid.make_loft([f.outer_wire() for f in secs], ruled=True)


def sp():
    s = _U(guard(), plate(), rear(), fork(), struts(), rear_flare())
    s = _S(s, wells(), pocket())
    nonfork = _S(_box(-BIG, BIG, -BIG, BIG, -BIG, 0), _box(*FORK_X, CROSS_Y0, BIG, -BIG, BIG))
    s = _S(s, under_b(), nonfork)
    from .variants import variant
    if variant("clip_forks"):
        s = _S(s, _box(-BIG, BIG, -BIG, BIG, -BIG, FORK_FLOOR_CLR - FLOOR_LIFT))   # forks stop over the floor (departure)
    return _solid(s)
