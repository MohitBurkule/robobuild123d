"""[fix-C] Revron wedgelet group (split out of side.py; geometry unchanged)."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _wg_yz_prism(items, x0, x1):
    """Prism over X x0..x1 of a closed (Y, Z) outline of exact lines ('l', p, q) and arcs ('a', centre, r, a0, a1 deg, taken through
    the mid angle), so every wall is a true plane or cylinder."""
    b = _b()
    pt = lambda p: b.Vector(0, p[0], p[1])   # noqa: E731
    on = lambda c, r, a: (c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))   # noqa: E731
    edges = []
    for it in items:
        if it[0] == "l":
            edges.append(b.Edge.make_line(pt(it[1]), pt(it[2])))
        else:
            _, c, r, a0, a1 = it
            edges.append(b.Edge.make_three_point_arc(pt(on(c, r, a0)), pt(on(c, r, (a0 + a1) / 2)), pt(on(c, r, a1))))
    sol = b.Solid.extrude(b.Face(b.Wire(edges)), b.Vector(abs(x1 - x0), 0, 0))
    return sol.moved(b.Location((min(x0, x1), 0, 0)))


def _wg_kidney_entry(xt):
    """(kidney prism, entry prism): the kidney is an arc slot (WG_KIDNEY) round SB; the entry (WG_ENTRY) is the
    channel over its upper cap, bounded by the slot's own outer wall and cap, a rear edge from the wall (at `ring_end` deg) up to
    the notch floor and a front edge tangent to the cap. All from relations about SB, so the walls are shared exactly."""
    k, e = WG_KIDNEY, WG_ENTRY
    on = lambda r, a, c=(0.0, 0.0): (SB[0] + c[0] + r * math.cos(math.radians(a)), SB[1] + c[1] + r * math.sin(math.radians(a)))   # noqa: E731
    hw, ro, ri = k["hw"], k["r"] + k["hw"], k["r"] - k["hw"]
    c_hi = (k["r"] * math.cos(math.radians(k["a_hi"])), k["r"] * math.sin(math.radians(k["a_hi"])))
    c_lo = (k["r"] * math.cos(math.radians(k["a_lo"])), k["r"] * math.sin(math.radians(k["a_lo"])))
    p2 = (e["rear_dy"], e["top"])
    d = math.hypot(p2[0] - c_hi[0], p2[1] - c_hi[1])            # right-hand tangent from the notch-floor corner to the upper cap
    a_t = math.degrees(math.atan2(p2[1] - c_hi[1], p2[0] - c_hi[0]) - math.acos(hw / d))
    S = SB
    kid = _wg_yz_prism([("a", S, ro, k["a_lo"], k["a_hi"]), ("a", (S[0] + c_hi[0], S[1] + c_hi[1]), hw, k["a_hi"], k["a_hi"] - 180),
                     ("a", S, ri, k["a_hi"], k["a_lo"]), ("a", (S[0] + c_lo[0], S[1] + c_lo[1]), hw, k["a_lo"] + 180, k["a_lo"])], *WG_KIDNEY["x"])
    q = on(ro, e["ring_end"])
    t_pt = on(hw, a_t, c_hi)
    P2 = (S[0] + p2[0], S[1] + p2[1])
    P1 = (P2[0] - e["width"], P2[1])
    # the outline closes through the slot's centre line (inside the slot, which is cut anyway): only the two straight walls
    # remain pocket walls, and their floor edges are rounded Fillet9 on the cutter (a convex blend on the cutter = the concave blend on the part)
    mid = on(k["r"], (e["ring_end"] + k["a_hi"]) / 2)
    ch = (S[0] + c_hi[0], S[1] + c_hi[1])
    ent = _wg_yz_prism([("l", P1, q), ("l", q, mid), ("l", mid, ch), ("l", ch, t_pt), ("l", t_pt, P2), ("l", P2, P1)], xt - e["depth"], xt)
    near = lambda p, v: abs(p.Y - v[0]) < 1e-5 and abs(p.Z - v[1]) < 1e-5   # noqa: E731
    walls = [(P1, q), (t_pt, P2)]
    edges = [ed for f in ent.faces() if abs(f.center().X - (xt - e["depth"])) < 1e-6 and f.geom_type == _b().GeomType.PLANE for ed in f.edges()
             if any((near(ed.start_point(), u) and near(ed.end_point(), v)) or (near(ed.start_point(), v) and near(ed.end_point(), u)) for u, v in walls)]
    try:
        ent = ent.fillet(e["fillet"], edges)
    except Exception:  # noqa: BLE001 - a failed blend keeps the sharp pocket
        pass
    return kid, ent


def _wg_round_step(body, skin, ring, x):
    """Fillet1: a concave round (WG_STEP_FILLET) where the ramp skin leaves the ring step's face (plane X x, facing the skin): one
    bar per straight skin outline line that lies inside the ring outline, square minus quarter disc in section, clipped to the ring."""
    from shapely.geometry import LineString, Point
    b = _b()
    r = WG_STEP_FILLET
    floor = min(p[1] for p in skin.exterior.coords)
    bars = []
    cs = list(skin.exterior.coords)
    for p, q in zip(cs[:-1], cs[1:]):
        par = abs((q[0] - p[0]) * RAMP_SLOPE + (q[1] - p[1])) < 1e-2 * math.dist(p, q)   # direction (1, -RAMP_SLOPE): parallel to the ramp
        if min(p[1], q[1]) <= floor + 1e-6 or not par:
            continue                                   # Fillet1 runs only on the skin's inner face (parallel to the ramp); floor, toe chamfer, stubs carry none
        for seg in getattr(LineString([p, q]).intersection(ring), "geoms", [LineString([p, q]).intersection(ring)]):
            if seg.length < 1e-3 or seg.geom_type != "LineString":
                continue
            snap = lambda u: min(cs[:-1] + list(ring.exterior.coords), key=lambda c: math.dist(c, u))   # noqa: E731 - ends on the shared outline vertices
            (y0, z0), (y1, z1) = [snap(u) if math.dist(snap(u), u) < 1e-3 else u for u in (seg.coords[0], seg.coords[-1])]
            ln = math.hypot(y1 - y0, z1 - z0)
            dy, dz = (y1 - y0) / ln, (z1 - z0) / ln
            ny, nz = -dz, dy
            if skin.contains(Point((y0 + y1) / 2 + ny * 1e-3, (z0 + z1) / 2 + nz * 1e-3)):
                ny, nz = -ny, -nz                      # outward: away from the skin
            P = lambda u, t: b.Vector(x + t, y0 + u * ny, z0 + u * nz)   # noqa: E731
            k = r * (1 - math.sqrt(0.5))
            prof = b.Wire([b.Edge.make_line(P(0, 0), P(r, 0)), b.Edge.make_three_point_arc(P(r, 0), P(k, k), P(0, r)), b.Edge.make_line(P(0, r), P(0, 0))])
            bars.append(b.Solid.extrude(b.Face(prof), b.Vector(0, dy * ln, dz * ln)))
    if not bars:
        return body
    clip = _ext(ring, "yz", x, x + r)
    return _U(body, *[_I(bar, clip) for bar in bars])


def _wg_ring(r, tail, x0, x1):
    """Ring step x0..x1: boss round SB with its tail, the far edge (x1) chamfered WG_RING_CHAMFER at 45 deg on the SB side (cone, left half
    of the boss) and along the floor up to WG_RING_CHAMFER_Y (plane); the boss right half merges into the tail."""
    from shapely.geometry import Polygon
    b = _b()
    c = WG_RING_CHAMFER
    cone = b.Solid.make_cone(r, r - c, x1 - x0, b.Plane(origin=(x0, SB[0], SB[1]), z_dir=(1, 0, 0)))
    left = _I(cone, _box(x0, x1, SB[0] - 2 * r, SB[0], SB[1] - 2 * r, SB[1] + 2 * r))
    floor = tail[-1][1]
    wedge = _ext(Polygon([(x1 - c, floor), (x1, floor + c), (x1, floor - 1.0), (x1 - c, floor - 1.0)]), "xz", SB[0], WG_RING_CHAMFER_Y)
    body = _S(_U(left, _ext(Polygon(tail).buffer(0), "yz", x0, x1)), wedge)
    # the floor chamfer ends in a vertex blend with Fillet1: along the floor it runs on to y0 + sqrt(A h - B h^2), h = height of the chamfer at that X
    y0, A, B = WG_RING_CHAMFER_Y, WG_CHAMFER_END["a"], WG_CHAMFER_END["b"]
    secs = []
    for h in (0.05, 0.2, 0.4, 0.6, 0.8, 0.95, 1.0):
        ye = y0 + math.sqrt(A * h - B * h * h)
        secs.append(b.Wire([b.Edge.make_line(b.Vector(x1 - c + h, *p), b.Vector(x1 - c + h, *q)) for p, q in zip(
            [(y0 - 0.5, floor - 0.5), (y0 - 0.5, floor + h), (y0, floor + h), (ye, floor), (ye, floor - 0.5)],
            [(y0 - 0.5, floor + h), (y0, floor + h), (ye, floor), (ye, floor - 0.5), (y0 - 0.5, floor - 0.5)])]))
    return _S(body, b.Solid.make_loft(secs))


def wedgelet(s):
    """RV17/18 TPU wedgelet (left built, right mirrored), slabs along X (WG_X) measured on the STEP sections:
    an outer block round the 15 mm standoff end, a ring step, a 2.3 mm ramp skin over a hollow whose top edge is
    capped by an arc swept along the ramp (WG_SKIN_CAP), the cheek round both standoffs with the fork-tail kidney slot and the 2.5 mm fork slot
    through it, and a nose tab. Ramp face 50 deg: Z = FLOOR_Z + RAMP_SLOPE (RAMP_REACH - Y)."""
    from shapely.geometry import LineString, Point, Polygon, box
    P = lambda pts: Polygon(pts).buffer(0)  # noqa: E731
    (r1, tail1), (r2, tail2) = WG_S1, WG_S2
    s1 = Point(*SB).buffer(r1, ARC_N).union(P(tail1))
    s2 = Point(*SB).buffer(r2, ARC_N).union(P(tail2))
    skin, cheek, tab = P(WG_SKIN), P(WG_CHEEK), P(WG_TAB)
    in_slot = P(WG_IN_SLOT).union(Point(*SA).buffer(r1, ARC_N))
    # the nose tab bears on the weapon mount's nose: take the mount's boss outline (its side profile above the
    # notch-to-nose line) out of the tab in 2D and drop any sliver thinner than a TPU wall, so no film is left
    mprof = _mount_profile("l" if s < 0 else "r").intersection(_mount_clip())
    cut = tab.difference(mprof.buffer(WG_MOUNT_GAP, ARC_MOUNT))
    # opening by reconstruction: films thinner than a TPU wall go, but the surviving body keeps its own sharp tips and edges
    # (a plain open rounds every corner of the tab, which moved the tab by ~1 mm when the mount profile changed)
    tab = cut.intersection(cut.buffer(-WG_TAB_FILM, join_style=2).buffer(WG_TAB_FILM + WG_MERGE_EPS, join_style=2))
    bb = _b()
    xb, xr, xs, xc, xt, xe = WG_X
    # skin cap: arc in (X, W = Z - k Y) drawn on the XZ plane (Y = 0) and swept along (0, 1, k) over the skin
    k, (cx, cw), rc = WG_SKIN_CAP["k"], WG_SKIN_CAP["c"], WG_SKIN_CAP["r"]
    xcap = min(cx + rc, xc)
    cap = Point(cx, cw).buffer(rc, ARC_N).union(box(xs, cw, xcap, cw + rc)).intersection(box(xs, cw - rc, xcap, cw + rc))
    reach = RAMP_REACH + rc
    cutter = bb.Solid.extrude(_face(cap, "xz")[0], bb.Vector(0, reach, k * reach))
    sk = _S(_ext(skin, "yz", xs, xc), cutter)
    # gusset: past the ring step the reference keeps the ring outline above the skin cap arc (the cap cutter's own volume inside the
    # ring outline) until the arc climbs out of the ring top; same arc, no new number
    gusset = _I(_ext(P(tail2), "yz", xs, xcap), cutter)
    body = _U(_U(_cyl(r1, xb, xr, SB), _ext(P(tail1), "yz", xb, xr)), _wg_ring(r2, tail2, xr, xs), sk, gusset, _ext(cheek, "yz", xc, xt), _ext(tab, "yz", xt, xe) if not tab.is_empty else None)
    body = _wg_round_step(body, skin, s2, xs)
    kidney, entry = _wg_kidney_entry(xt)
    bx0, bx1 = WG_BORE_X
    cuts = [_ext(cheek.difference(in_slot), "yz", *WG_FORK_SLOT_X),               # 2.5 mm fork slot through the cheek
            _cyl(WG_BORES["sa"], bx0, bx1, SA), _cyl(WG_BORES["sb"], bx0, bx1, SB), _cyl(WG_BORES["sb_head"], xr, bx1, SB),
            kidney,
            entry]   # tail entry from the notch
    # TPU cannot print the ramp's knife toe: keep the full reach but stand the toe on a printable land,
    # the ramp face running parallel to the measured one from there
    body = _U(body, _I(_ext(P(WG_TOE), "yz", xb, xe), _ext(s1.union(cheek).union(tab).buffer(WG_MERGE_EPS), "yz", xb, xe)))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # the STEP leaves the fork tine and the mount boss inside the TPU nose; cut their seats (the tine slides into a
    # 1.5 mm slit, the TPU nose tab bears on the mount)
    # the nose tab grazes the chassis lug by 0.1 mm: take the chassis out of it (a printed TPU nose conforms)
    sh = _S(sh, _fork_slot(s), weapon_mount("l" if s < 0 else "r"))
    return _S(sh, chassis())   # chassis cut on its own: with the fork / mount cutters in one multi-tool cut the result is invalid (BRepCheck)
