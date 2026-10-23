"""vert_mod body from relations: one ramp plane (front inner wall at deck height up to the top of the upright tail
round the weapon axis) tops the whole module; a planform cut from the chassis inner box; a hollow under the ramp shell;
two uprights whose outline is the hull of the bulkhead foot and the tail circle round the axis. STEP frame."""
import math

import build123d as bd

from shapely.geometry import Point, Polygon, box as sbox, LineString
from shapely.ops import unary_union
from shapely import affinity

from robocad.geom import _box, _cyl, _U, _S, _I, _ext as _ext_poly, _face, _mirror_x, _solid


def _ext(poly, plane, a0, a1, arcs=True):
    """Prism of an outline with its polygonised arcs turned back into true arcs (cylinders, not facets)."""
    return _ext_poly(poly, plane, a0, a1, arcs=arcs)
from .chassis import halfspace
from .params_chassis import IN_X, IN_Y, POSTS, CH_H
from .params_drive import WY, WZ
from .params_vert import *  # noqa: F401,F403

TOOL = BIG / 10                        # cut tools reach this far
MIN_PIPE_ARC = 0.5                     # floor-round arcs shorter than this are left out
OVERLAP = 0.05                         # a filler's reach into the material it joins
HS = BIG / 5                           # half-space cutters: well past the part, small enough for exact booleans
TOOL_S = BIG / 50                      # drafted tools: far enough through the ramp
SEG = 128                              # arc segments per quarter
GEOM_EPS = 1e-6                        # coordinate match on edges

K = (WZ + UP_R - DECK_TOP) / (WY + IN_Y)          # ramp: deck height at the front inner wall -> top of the tail circle
COSK = 1 / math.hypot(1, K)
SECK = math.hypot(1, K)


def ramp_z(y, drop=0.0):
    return DECK_TOP + K * (y + IN_Y) - drop / COSK


def above_ramp(drop=0.0):
    return halfspace((0, -IN_Y, DECK_TOP - drop / COSK), (0, -K, 1), HS)


def _sym(p):
    return unary_union([p, affinity.scale(p, -1, 1, origin=(0, 0))])


def taper_x(y):
    (x0, y0), (x1, y1) = TAPER
    return x0 + (x1 - x0) * (y - y0) / (y1 - y0)


def _tangent_ext(c, r, m, reach):
    """A point `reach` past m on the line from m tangent to circle (c, r), on the +x side: kept in a hull it carries the
    tangent line on past the notch mouth (so a chamfer along it runs out as a plane)."""
    dx, dy = c[0] - m[0], c[1] - m[1]
    d = math.hypot(dx, dy)
    a = math.asin(r / d)
    out = []
    for sg in (1, -1):
        ca, sa = math.cos(sg * a), math.sin(sg * a)
        u = ((dx * ca - dy * sa) / d, (dx * sa + dy * ca) / d)
        out.append((m[0] - reach * u[0], m[1] - reach * u[1]))
    return max(out, key=lambda p: p[0])


def notch(reach=0.0):
    """Side notch in the planform: round rear end, round front corner, tangent lines out to the inner wall line."""
    (cx, cy), r = NOTCH_TOP
    (lx, ly), rl = NOTCH_LOW
    mt, ml = (IN_X, NOTCH_Y[1]), (IN_X, NOTCH_Y[0])
    top = unary_union([Point(cx, cy).buffer(r, SEG), Point(mt)] + ([Point(_tangent_ext((cx, cy), r, mt, reach))] if reach else [])).convex_hull
    low = unary_union([Point(lx, ly).buffer(rl, SEG), Point(ml), Point(IN_X, ly)] + ([Point(_tangent_ext((lx, ly), rl, ml, reach))] if reach else [])).convex_hull
    return _sym(unary_union([top, low, sbox(NOTCH_X, ly, IN_X + 1, cy)]))


def front_opening(full=False):
    """Plan opening between the legs. The arch over it is cut square to the ramp (arch()); the plan cut stops at the
    arch corner centres' deck line. full: the whole opening as seen on the deck (the hollow keeps one wall round it)."""
    (ax, ay), (bx, by) = LEG_IN
    k = (bx - ax) / (by - ay)
    top = ARCH_Y if full else ARCH_Y - ARCH_R * SECK
    xa, xt = ax + k * (-TOOL - ay), ax + k * (top - ay)
    p = Polygon([(-xa, -TOOL), (xa, -TOOL), (xt, top), (-xt, top)])
    return p.buffer(-ARCH_R, SEG).buffer(ARCH_R, SEG) if full else p


def _ramp_plane(z):
    """Plane square to the ramp (its normal), origin on the centre line at height z above the deck line y 0."""
    import build123d as bd
    return bd.Plane(origin=(0, 0, z), x_dir=(1, 0, 0), z_dir=(0, -K / SECK, 1 / SECK))


def inside_round(p1, p2, r):
    """Material an inside round of radius r adds where two faces meet (each an outward plane (n, d), n.p = d): the corner
    wedge between the tangent lines minus the cylinder, along the planes' common line (exact)."""
    import build123d as bd
    import numpy as np
    (n1, d1), (n2, d2) = [(np.array(n, float) / np.linalg.norm(n), d / np.linalg.norm(n)) for n, d in (p1, p2)]
    u = np.cross(n1, n2)
    u /= np.linalg.norm(u)
    A = np.array([n1, n2, u])
    v, c = np.linalg.solve(A, [d1, d2, 0.0]), np.linalg.solve(A, [d1 + r, d2 + r, 0.0])
    e = OVERLAP                                             # reach into both faces' material so the fuse merges cleanly
    quad = (v - e * (n1 + n2), c - (r + e) * n1, c, c - (r + e) * n2)
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(*(q - u * TOOL_S)) for q in quad], close=True))
    wedge = bd.Solid.extrude(face, bd.Vector(*(u * 2 * TOOL_S)))
    return _S(wedge, bd.Solid.make_cylinder(r, 2 * TOOL_S, bd.Plane(origin=tuple(c - u * TOOL_S), z_dir=tuple(u))))


def hollow_front_round():
    """R HOLLOW_EDGE_R round where the hollow's ceiling meets the lip's back face, over the arch's straight run (STEP)."""
    ceil = ((0, K, -1), -(ramp_z(0) - VM_T * SECK))
    back = ((0, 1, 0), ARCH_Y + LIP_W)
    return _I(inside_round(back, ceil, HOLLOW_EDGE_R), _box(-ARCH_X, ARCH_X, -BIG, BIG, -BIG, BIG))


def hollow_rear_round():
    """R HOLLOW_EDGE_R round where the hollow's ceiling (one wall under the ramp) meets the bulkhead face (STEP)."""
    y0, r = BULK_Y[0], HOLLOW_EDGE_R
    ceil = lambda y: ramp_z(y) - VM_T * SECK
    c = (y0 - r, ceil(y0 - r) - r * SECK)                   # r off the wall and r under the ceiling
    tw = (y0, c[1])
    tc = (c[0] - r * K / SECK, c[1] + r / SECK)              # tangent point on the ceiling (along its normal)
    corner = (y0, ceil(y0))
    e = OVERLAP                                             # reach into the wall and the ceiling so the fuse merges it
    up = (-K / SECK, 1 / SECK)
    prof = Polygon([(corner[0] + e, corner[1] + e), (tc[0] + e * up[0], tc[1] + e * up[1]), tc, c, tw, (tw[0] + e, tw[1])])
    prof = prof.buffer(0).difference(Point(c).buffer(r, SEG))
    xh = max(abs(x) for x, y in hollow_plan().exterior.coords if abs(y - y0) < GEOM_EPS)   # the rear edge's straight run
    return _ext(prof, "yz", -xh, xh)


def arch():
    """Arch over the front opening, cut along the ramp normal: a straight top on the lip line, R ARCH_R corners
    ARCH_X off the middle, the opening below them; its edge on the ramp chamfered TOP_CH at 45 deg (STEP)."""
    import build123d as bd
    vt = ARCH_Y / SECK                                      # lip line, along the ramp from the deck origin
    vc = vt - ARCH_R
    prof = unary_union([sbox(-ARCH_X, -TOOL_S, ARCH_X, vt), sbox(-ARCH_X - ARCH_R, -TOOL_S, ARCH_X + ARCH_R, vc),
                        Point(-ARCH_X, vc).buffer(ARCH_R, SEG), Point(ARCH_X, vc).buffer(ARCH_R, SEG)])
    h = (ramp_z(0) - DECK_TOP) / SECK                       # ramp surface over the deck origin, along the normal
    pl = _ramp_plane(DECK_TOP)
    f = _face(prof, "xy", arcs=True)[0]
    body = bd.extrude(f.moved(bd.Location(pl.offset(-TOOL_S))), amount=TOOL_S + h - TOP_CH, dir=pl.z_dir)
    w0, w1 = h - TOP_CH, h + 1                              # the chamfer starts TOP_CH under the ramp surface and runs out past it
    g = (w1 - w0) * math.tan(math.radians(ARCH_CH_ANG))     # how far the profile has grown at w1
    yz = lambda pts: bd.Face(bd.Wire.make_polygon([bd.Vector(0, v, w) for v, w in pts], close=True))
    xw = lambda pts: bd.Face(bd.Wire.make_polygon([bd.Vector(x, 0, w) for x, w in pts], close=True))
    top = bd.Solid.extrude(yz([(-TOOL_S, w0), (vt, w0), (vt + g, w1), (-TOOL_S, w1)]), bd.Vector(2 * ARCH_X, 0, 0)).moved(bd.Location((-ARCH_X, 0, 0)))
    side = bd.Solid.extrude(xw([(0, w0), (ARCH_X + ARCH_R, w0), (ARCH_X + ARCH_R + g, w1), (0, w1)]), bd.Vector(0, vc + TOOL_S, 0)).moved(bd.Location((0, -TOOL_S, 0)))
    cones = [bd.Solid.make_cone(ARCH_R, ARCH_R + g, w1 - w0, bd.Plane(origin=(sx * ARCH_X, vc, w0))) for sx in (-1, 1)]
    ch = _U(top, side, _mirror_x(side), *cones).moved(bd.Location(pl))   # exact planes and cones (an offset profile, not a loft)
    return _U(body, ch)


def plan():
    """Whole planform: chassis inner box from the front clearance to the tail, cut by the upright tapers, the leg
    opening, the side notches and the slot between the uprights."""
    y1 = WY + UP_R
    half = Polygon([(0, FRONT_Y), (IN_X, FRONT_Y), (IN_X, TAPER[0][1]), (taper_x(y1), y1), (0, y1)])
    return _sym(half).difference(front_opening()).difference(notch())


def slot_plan():
    """Slot between the uprights behind the bulkhead, its corners rounded SLOT_R."""
    return sbox(-UP_X0, BULK_Y[1], UP_X0, TOOL).buffer(-SLOT_R, SEG).buffer(SLOT_R, SEG)


def hollow_plan():
    """Under-shell hollow: the planform in by one wall, from the lip to the bulkhead, round the rear column pads."""
    p = plan().buffer(-VM_T, join_style=2).intersection(sbox(-BIG, HOLLOW_FRONT, BIG, BULK_Y[0]))
    p = p.difference(front_opening(full=True).buffer(LIP_W, SEG))   # the front lip round the arch (STEP: its back face at y ARCH_Y + LIP_W)
    p = p.difference(unary_union([Point(q).buffer(POST_PAD_R, SEG) for q in POSTS if q[1] > 0])).difference(slot_plan())
    return p.buffer(-HOLLOW_R, SEG).buffer(HOLLOW_R, SEG).buffer(HOLLOW_R, SEG).buffer(-HOLLOW_R, SEG)


def upright_prof():
    """(y, z) outline: hull of the bulkhead foot and the tail circle round the weapon axis."""
    tail = Point(WY, WZ).buffer(UP_R, SEG)
    hull = unary_union([tail, Point(IN_Y, DECK_TOP), Point(BULK_Y[0], ramp_z(BULK_Y[0]))]).convex_hull
    under = Polygon([(-BIG, -BIG), (BIG, -BIG), (BIG, ramp_z(BIG)), (-BIG, ramp_z(-BIG))])   # the ramp plane runs on over the uprights (STEP)
    top = hull.intersection(under).union(tail).buffer(UP_TOP_R, SEG).buffer(-UP_TOP_R, SEG)   # rounded into the tail circle
    return top.union(sbox(BULK_Y[0], DECK_TOP, IN_Y, ramp_z(IN_Y)))   # flat foot to the chassis inner wall line


def body():
    pl = plan()
    shell = _ext(pl.intersection(sbox(-BIG, -BIG, BIG, BULK_Y[1])), "xy", DECK_TOP, DECK_TOP + TOOL_S)   # tall enough for the ramp, short enough for exact booleans
    side = pl.intersection(sbox(-BIG, BULK_Y[0], BIG, BIG))  # the bulkhead and the slot corners hang with the uprights (underside on the hull)
    slot = _ext(slot_plan(), "xy", -TOOL, TOOL, arcs=True)
    ups = _I(_ext(side, "xy", -1, TOOL), _ext(upright_prof(), "yz", -TOOL, TOOL))
    ar = above_ramp()
    s = _S(_U(_S(shell, ar), _S(ups, ar)), slot)        # the ramp cut before the union (OCC drops it from the fused arcs)
    hollow = _ext(hollow_plan(), "xy", DECK_TOP - 1, TOOL)
    s = _S(s, _S(hollow, above_ramp(VM_T)), leg_drafts(), arch())
    s = _U(s, hollow_rear_round(), hollow_front_round())
    return top_chamfer(s)


def leg_drafts():
    """Leg inner faces lean back LEG_DRAFT from their deck line up to where the arch round starts."""
    (ax, ay), (bx, by) = LEG_IN
    L = math.hypot(bx - ax, by - ay)
    m = ((by - ay) / L, (ax - bx) / L)                      # plan normal of the right leg's inner face, into the opening
    m = (-m[0], -m[1]) if m[0] > 0 else m
    a = math.radians(LEG_DRAFT)
    n = (m[0] * math.sin(a), m[1] * math.sin(a), math.cos(a))
    c = _I(halfspace((ax, ay, DECK_TOP), n, HS), _box(0, IN_X + 1, -TOOL, ARCH_Y - ARCH_R, DECK_TOP, TOOL))
    return _U(c, _mirror_x(c))


def top_chamfer(s):
    """TOP_CH equal-distance chamfer on the ramp edges over the side notches: chamfered on a flat-topped block round each
    notch (the ramp flattened), the removed sliver sheared back onto the ramp and cut from the body."""
    import build123d as bd
    (cx, cy), r = NOTCH_TOP
    ly = NOTCH_LOW[0][1]
    area = sbox(NOTCH_X - 2 * TOP_CH, NOTCH_Y[0] - 2 * TOP_CH, IN_X, NOTCH_Y[1] + 2 * TOP_CH)
    ring = area.difference(notch(reach=2 * TOP_CH))
    z0, z1 = DECK_TOP - 2 * TOP_CH, DECK_TOP
    blk = _ext(ring, "xy", z0, z1, arcs=True)
    top = [f for f in blk.faces() if f.geom_type.name == "PLANE" and abs(f.normal_at().Z - 1) < 1e-9]
    inner = lambda e: NOTCH_X - GEOM_EPS <= e.center().X <= IN_X - GEOM_EPS and NOTCH_Y[0] - TOP_CH < e.center().Y < NOTCH_Y[1] + TOP_CH \
        and not (abs(e.center().X - (NOTCH_X - 2 * TOP_CH)) < GEOM_EPS)
    E = [e for f in top for e in f.edges() if inner(e)]
    sliver = _S(_S(blk, blk.chamfer(TOP_CH, None, E)), _box(-BIG, BIG, NOTCH_LOW[0][1], BIG, -BIG, BIG))   # the mouth's front run only
    shear = bd.Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, K, 1, K * IN_Y], [0, 0, 0, 1]])
    cut = sliver.transform_geometry(shear)
    # ahead of it the chamfer runs out to nothing at the notch's front corner: a plane through the corner's top edge
    y0, y1 = NOTCH_LOW[0][1], NOTCH_CH_Y0
    p0 = (NOTCH_X, y0, ramp_z(y0))
    p1 = (NOTCH_X - TOP_CH, y1, ramp_z(y1))
    p2 = (NOTCH_X, y1, ramp_z(y1) - TOP_CH / COSK)
    u = [p1[i] - p0[i] for i in range(3)]
    v = [p2[i] - p0[i] for i in range(3)]
    n = (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])
    n = n if n[2] > 0 else tuple(-c for c in n)
    taper = _I(halfspace(p0, n, BIG), _box(NOTCH_X - TOP_CH - 1, NOTCH_X + 1, y0, y1, -BIG, HS))
    cut = _U(cut, taper)
    return _S(s, cut, _mirror_x(cut), *[notch_rear_chamfer(sx) for sx in (-1, 1)])


def notch_rear_chamfer(sx):
    """Ramp edge over the notch's floor, rear round and rear wall (STEP): the floor edge an equal-distance TOP_CH chamfer,
    the wall edge the STEP's own plane per side, the round between them a cylinder of NOTCH_R along their common line."""
    import build123d as bd
    import numpy as np
    nr = np.array([0.0, -K, 1.0]) / SECK                      # ramp normal
    nf = np.array([sx, 0.0, 0.0]) + nr
    nf /= np.linalg.norm(nf)
    df = nf @ np.array([sx * NOTCH_X, 0.0, ramp_z(0.0)]) - TOP_CH * math.sin(math.radians(45))
    nw, dw = NOTCH_WALL_CH[sx]
    nw = np.array(nw)
    H = lambda n, d: halfspace(tuple(n * d), tuple(n), HS)  # the void side (n.p > d)
    u = np.cross(nf, nw)
    u /= np.linalg.norm(u)
    axis = np.linalg.solve(np.array([nf, nw, u]), np.array([df + NOTCH_R, dw + NOTCH_R, 0.0]))
    cyl = bd.Solid.make_cylinder(NOTCH_R, 2 * TOOL_S, bd.Plane(origin=tuple(axis - u * TOOL_S), z_dir=tuple(u)))
    wedge = _I(H(nf, df), H(nw, dw))
    v = np.linalg.solve(np.array([nf, nw, u]), np.array([df, dw, 0.0]))   # the sharp corner line
    quad = [v, axis - NOTCH_R * nf, axis, axis - NOTCH_R * nw]           # corner, tangent points, round centre
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(*(q - u * TOOL_S)) for q in quad], close=True))
    corner = bd.Solid.extrude(face, bd.Vector(*(u * 2 * TOOL_S)))         # only between the tangent lines
    void = _S(wedge, _S(corner, cyl))
    x0, x1 = sorted((sx * (NOTCH_X - TOP_CH - 1), sx * (IN_X + 1)))
    return _I(void, _box(x0, x1, NOTCH_CH_Y0, NOTCH_Y[1] + 2 * TOP_CH, DECK_TOP, TOOL))


def edge_chamfer(m, p, dh, dv, region):
    """Chamfer cut along a ramp-top edge over a vertical wall whose outward plan normal is m, through point p of that
    edge: the plane dh in from the edge on the ramp and dv down the wall. Kept in region."""
    t = (-m[1], m[0])
    e = (t[0], t[1], K * t[1])
    a = (p[0] - dh * m[0], p[1] - dh * m[1], ramp_z(p[1] - dh * m[1]))
    b = (p[0], p[1], ramp_z(p[1]) - dv)
    w = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    n = (e[1] * w[2] - e[2] * w[1], e[2] * w[0] - e[0] * w[2], e[0] * w[1] - e[1] * w[0])
    n = n if n[2] > 0 else tuple(-c for c in n)
    return _I(halfspace(a, n, HS), region)


def bulk_chamfer():
    """Bulkhead rear top edge round the slot: a 45 deg plane, coned round the slot corners."""
    import build123d as bd
    x0 = UP_X0 - SLOT_R
    z0 = ramp_z(BULK_Y[1]) - TOP_CH                         # chamfer foot on the rear face
    flat = _I(halfspace((0, BULK_Y[1], z0), (0, 1, 1), HS), _box(-x0, x0, -TOOL, BULK_Y[1] + SLOT_R, DECK_TOP, TOOL))
    c = []
    for sx in (-1, 1):
        cone = bd.Solid.make_cone(0, TOOL, TOOL, bd.Plane(origin=(sx * x0, BULK_Y[1] + SLOT_R, z0 - SLOT_R), z_dir=(0, 0, 1)))
        c.append(_I(cone, _box(sx * x0, sx * UP_X0, -TOOL, BULK_Y[1] + SLOT_R, DECK_TOP, TOOL)))
    return _U(flat, *c)


def upright_chamfers():
    (x0, y0), (x1, y1) = TAPER
    L = math.hypot(x1 - x0, y1 - y0)
    m = ((y1 - y0) / L, (x0 - x1) / L)
    yc = BULK_Y[1]
    dh, dv = UP_IN_CH
    out = lambda ch: edge_chamfer(m, (taper_x(yc), yc), ch[0], ch[1], _box(0, TOOL, y0 - 1, UP_CH_Y[1], DECK_TOP, TOOL))
    inner = edge_chamfer((-1, 0), (UP_X0, yc), dh, dv, _box(UP_X0 - 1, UP_X0 + dh + 1, UP_CH_Y[0], UP_CH_Y[1], DECK_TOP, TOOL))
    return _U(out(UP_OUT_CH[1]), _mirror_x(out(UP_OUT_CH[0])), inner, _mirror_x(inner), bulk_chamfer())


def side_pockets():
    """Upright outer pockets: drawn on the floor plane SIDE_POCKET depth in from the taper face and cut outwards along
    its normal; a round end on the axis, a flat floor at the front running into the hollow."""
    import build123d as bd
    (c, r, (z0, z1), depth) = SIDE_POCKET
    (x0, y0), (x1, y1) = TAPER
    L = math.hypot(x1 - x0, y1 - y0)
    t = ((x1 - x0) / L, (y1 - y0) / L)                      # along the right taper face, rearwards
    n = (-t[1], t[0]) if -t[1] > 0 else (t[1], -t[0])       # outward
    o = (x0 - depth * n[0], y0 - depth * n[1])              # floor plane origin
    u = lambda y: (y - o[1]) / t[1]                          # along-face coordinate of a point of the floor at y
    cu = u(c[0])
    yf = BULK_Y[0] - SIDE_POCKET_FRONT
    prof = unary_union([Point(cu, c[1]).buffer(r, SEG), Point(u(BULK_Y[0] + POCKET_STEP), z0), Point(u(BULK_Y[0]), z1)]).convex_hull
    prof = prof.union(sbox(u(yf), z0, u(BULK_Y[0] + POCKET_STEP) + OVERLAP, z1 - K * SIDE_POCKET_FRONT))   # runs a hair under the slope: no coincident corner
    pl = bd.Plane(origin=(o[0], o[1], 0), x_dir=(t[0], t[1], 0), z_dir=(n[0], n[1], 0))
    p = _floor_rounded(prof, SIDE_POCKET_FLOOR_R).moved(bd.Location(pl))   # its floor edges rounded (STEP)
    return _U(p, _mirror_x(p))


def _floor_rounded(prof, r):
    """Pocket of outline `prof` (local XY) cut along +Z from its floor at z 0, every floor edge rounded r: the outline
    from r up, the outline shrunk by r from the floor, and a circle of r swept round the shrunk outline at height r."""
    import build123d as bd
    inner = prof.buffer(-r, SEG)
    up = _U(*[bd.Solid.extrude(f.moved(bd.Location((0, 0, r))), bd.Vector(0, 0, TOOL)) for f in _faces(prof)])
    low = _U(*[bd.Solid.extrude(f, bd.Vector(0, 0, TOOL)) for f in _faces(inner)])
    pipes = []
    for f in _faces(inner):                                 # the ball's path: a cylinder per line, a torus per arc
        for e in f.outer_wire().moved(bd.Location((0, 0, r))).edges():
            p0, p1 = e.position_at(0), e.position_at(1)
            if e.geom_type.name == "LINE":
                pipes.append(bd.Solid.make_cylinder(r, (p1 - p0).length, bd.Plane(origin=p0, z_dir=p1 - p0)))
            elif e.length > MIN_PIPE_ARC:                       # a corner's sliver of arc tessellates badly against its neighbours
                c = e.arc_center
                ang = lambda q: math.degrees(math.atan2(q.Y - c.Y, q.X - c.X))
                a0, am, a1 = ang(p0), ang(e.position_at(0.5)), ang(p1)
                ccw = (am - a0) % 360 < (a1 - a0) % 360                         # the mid point decides the arc's sense
                a0, sweep = (a0, (a1 - a0) % 360) if ccw else (a1, (a0 - a1) % 360)
                xd = (math.cos(math.radians(a0)), math.sin(math.radians(a0)), 0)
                pipes.append(bd.Solid.make_torus(e.radius, r, bd.Plane(origin=c, x_dir=xd, z_dir=(0, 0, 1)), major_angle=sweep))   # exact torus, not a swept B-spline
    s = _U(up, low)
    for q in pipes:                                         # one at a time: a single many-tool fuse drops the tori
        s = _U(s, q)
    return s


def _faces(poly):
    return _face(poly, "xy", arcs=True)


def side_holes():
    """Hole through each side wall of the hollow, square to the upright's taper face, ahead of the side pocket."""
    import build123d as bd
    hy, hz, hr = SIDE_HOLE
    (x0, y0), (x1, y1) = TAPER
    L = math.hypot(x1 - x0, y1 - y0)
    n = ((y1 - y0) / L, (x0 - x1) / L)
    n = n if n[0] > 0 else (-n[0], -n[1])
    c = (taper_x(hy), hy, hz)
    h = bd.Solid.make_cylinder(hr, 4 * VM_T, bd.Plane(origin=(c[0] - 2 * VM_T * n[0], c[1] - 2 * VM_T * n[1], hz), z_dir=(n[0], n[1], 0)))
    return _U(h, _mirror_x(h))


def axis_cuts():
    """Axis hole through both uprights, the bearing-side recess, the motor screws (counterbored on the motor side)."""
    c = []
    c.append(_cyl(AXIS_HOLE_R, -TOOL, TOOL, (WY, WZ), "x"))
    c.append(_cyl(UP_RECESS_R, UP_RECESS_X, TOOL, (WY, WZ), "x"))
    for dy, dz in MOTOR_HOLES:
        q = (WY + dy, WZ + dz)
        c.append(_cyl(MOTOR_HOLE_R, -TOOL, TOOL, q, "x"))
        c.append(_cyl(MOTOR_CB_R, -TOOL, -MOTOR_CB_X, q, "x"))
    return _U(*c)


def shroud():
    """Motor-side shroud: a conical flare off the left upright's tail circle round the rear-lower quarter of the can,
    from straight down round to 45 deg up."""
    import build123d as bd
    r_out, x_r, x_end, r_in = SHROUD
    x_tail = -TAPER[1][0]
    k = (r_out - UP_R) / (x_r - x_tail)
    pl = lambda x: bd.Plane(origin=(x, WY, WZ), z_dir=(1, 0, 0))
    outer = _U(bd.Solid.make_cone(UP_R, r_out, x_r - x_tail, pl(x_tail)), _cyl(r_out, x_r, x_end, (WY, WZ), "x"))
    inner = bd.Solid.make_cone(r_in - k * (x_end - x_tail), r_in, x_end - x_tail, pl(x_tail))
    sector = _I(_box(-TOOL, TOOL, WY, TOOL, -TOOL, TOOL),
                halfspace((0, WY, WZ), (0, 1, -1), HS))
    return _I(_S(outer, inner), sector)


def _floor_pipe(x0, x1, zc, rr, y, rb):
    """A circle of radius rb swept round the stadium (centres x0, x1 at height zc, radius rr) in the plane at y."""
    with bd.BuildPart() as bp:
        with bd.BuildLine() as ln:                          # drawn in XY as (x, z), turned onto XZ below
            bd.Line((x0, zc - rr), (x1, zc - rr))
            bd.ThreePointArc((x1, zc - rr), (x1 + rr, zc), (x1, zc + rr))
            bd.Line((x1, zc + rr), (x0, zc + rr))
            bd.ThreePointArc((x0, zc + rr), (x0 - rr, zc), (x0, zc - rr))
        with bd.BuildSketch(bd.Plane(origin=(x0, zc - rr, 0), z_dir=(1, 0, 0))):
            bd.Circle(rb)
        bd.sweep(path=ln.wires()[0])
    return bp.part.solids()[0].rotate(bd.Axis.X, 90).moved(bd.Location((0, y, 0)))


def bulk_cuts():
    (xa, xb), (za, zb), back = TUNNEL
    y1 = BULK_Y[1] - back
    r = (zb - za) / 2
    rb = TUNNEL_FLOOR_R                                     # its blind end rounded into the walls: an exact pipe round the bore
    stad = lambda k: LineString([(xa + r, za + r), (xb - r, za + r)]).buffer(r - k, SEG)
    t = _U(_ext(stad(0), "xz", BULK_Y[0] - 1, y1 - rb, arcs=True), _ext(stad(rb), "xz", BULK_Y[0] - 1, y1, arcs=True),
           _floor_pipe(xa + r, xb - r, za + r, r - rb, y1 - rb, rb))
    x, r2, (z0, z1) = LEAD_SLOT
    s = _ext(LineString([(x, z0), (x, z1)]).buffer(r2, SEG), "xz", BULK_Y[0] - 1, SLOT_R + BULK_Y[1])
    return _U(t, s)


def prongs():
    """Prongs down between the chassis tabs onto the cross bolt: front face just off the chassis rear face, a round toe,
    a sloped heel filleted into the upright underside, a window above the cross-bolt boss."""
    from .params_chassis import HY, TAB_HOLE_DY, TAB_HOLE_Z
    x0, t, zb = PRONG
    (ty, tr), (hn, hr) = PRONG_TOE, PRONG_HEEL
    tc = (ty, zb + tr)
    y0 = HY + PRONG_CLR
    d = hn[0] * tc[0] + hn[1] * tc[1] + tr                 # heel line: tangent to the toe round
    yz = lambda z: (d - hn[1] * z) / hn[0]
    up = upright_prof()
    base = Polygon([(y0, zb), (yz(zb), zb), (yz(DECK_TOP + 1), DECK_TOP + 1), (y0, DECK_TOP + 1)])
    toe = sbox(tc[0], zb, BIG, tc[1]).difference(Point(tc).buffer(tr, SEG))
    outline = base.difference(toe).union(up).buffer(hr, SEG).buffer(-hr, SEG)   # heel fillet into the upright underside
    outline = outline.intersection(sbox(y0, zb, yz(DECK_TOP), DECK_TOP))   # overlaps the upright above its underside
    hole = (HY + TAB_HOLE_DY, TAB_HOLE_Z)
    tall = Polygon([(y0, zb), (yz(zb), zb), (yz(TOOL_S), TOOL_S), (y0, TOOL_S)])   # the window's top is the upright underside itself (STEP)
    win = tall.buffer(-PRONG_FRONT, SEG).intersection(sbox(y0 + PRONG_FRONT, zb, BIG, TOOL_S)).difference(up)   # webs PRONG_FRONT thick
    win = win.difference(Point(hole).buffer(PRONG_BOSS, SEG)).buffer(-PRONG_WEB, SEG).buffer(PRONG_WEB, SEG)
    p = _ext(outline.difference(win), "yz", x0, x0 + t)
    p = _S(p, _cyl(TAB_HOLE_R, x0 - 1, x0 + t + 1, hole, "x"))
    return _U(p, _mirror_x(p))


def post_holes():
    from .params_vert import POST_HOLE_D
    return _U(*[_U(_cyl(POST_HOLE_D / 2, -1, TOOL, p, "z"), _cyl(POST_CB_R, POST_CB_Z, TOOL, p, "z")) for p in POSTS])


def grooves():
    n, (x0, x1), (cx, cy), ang, w, pitch, depth = GROOVES
    a = math.radians(ang)
    d, u = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))     # along the groove, across it
    g = []
    for i in range(n):
        c = (cx + u[0] * pitch * i, cy + u[1] * pitch * i)
        L = LineString([(c[0] - d[0] * TOOL, c[1] - d[1] * TOOL), (c[0] + d[0] * TOOL, c[1] + d[1] * TOOL)])
        g.append(L.buffer(w / 2, cap_style=2).intersection(sbox(x0, -BIG, x1, BIG)))
    p = _sym(unary_union(g))
    return _S(_ext(p, "xy", DECK_TOP, TOOL), above_ramp(-1), _S(_box(-BIG, BIG, -BIG, BIG, -BIG, BIG), above_ramp(depth)))


def vm():
    s = _U(body(), shroud(), prongs())
    return _solid(_S(s, side_pockets(), axis_cuts(), bulk_cuts(), post_holes(), grooves(), upright_chamfers()))
