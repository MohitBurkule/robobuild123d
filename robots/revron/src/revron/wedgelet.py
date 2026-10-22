"""[fix-C-w7] Revron wedgelet RV17/18 (TPU), rebuilt from relations about the shared datums (no measured point tables).

The ramp (WG_RAMP_DEG) and the lines K (cheek top / cap axis, perpendicular to the ramp) and T (rear face, WG_TAPER_DEG off vertical,
WG_FLANK_R from SA) span every outline; the skin is WG_SKIN_T thick and WG_SKIN_RUN long along the ramp, and the same WG_SKIN_RUN fixes
the nose top and the R(run + 1) cap cylinder that carves the skin's top. LH is built once (slabs along X from WG_X0), RH is its mirror."""
import math
from functools import lru_cache

from .params import (ARC_N, GEO_EPS, FK_PIN_ANG, FK_PIN_DIST, FK_X, FLOOR_Z, LUG_SB_R, RAMP_REACH, SA, SB, WG_BAY_Z, WG_BOSS_GAP, WG_BORES, WG_BOSS_R, WG_FAR,
                     WG_CHAMFER_END, WG_FLANK_R, WG_MERGE_EPS, WG_MOUNT_GAP, WG_NOTCH, WG_PIN_SWING, WG_RAMP_DEG, WG_RING_CHAMFER_Y,
                     WG_SA_R, WG_SKIN_RUN, WG_SLIT_W, WG_SKIN_T, WG_SLAB, WG_TAB_FILM, WG_TAPER_DEG, WG_TOE_CHAMFER, WG_TOP_Z, WG_X0)
from .common import _I, _S, _U, _arc, _b, _box, _cyl, _ext, _mirror_x

_DOT = lambda a, c: a[0] * c[0] + a[1] * c[1]   # noqa: E731


def _meet(n1, c1, n2, c2):
    """Intersection of the lines n1.p = c1 and n2.p = c2."""
    d = n1[0] * n2[1] - n1[1] * n2[0]
    return ((c1 * n2[1] - c2 * n1[1]) / d, (n1[0] * c2 - n2[0] * c1) / d)


@lru_cache(maxsize=None)
def _wg():
    """Datum points / lines of the (Y, Z) outline, all derived from the masters in params_side (WG_*)."""
    rd, tau = math.radians(WG_RAMP_DEG), math.radians(WG_TAPER_DEG)
    g = dict(rh=(-math.cos(rd), math.sin(rd)), nr=(math.sin(rd), math.cos(rd)), nt=(math.cos(tau), math.sin(tau)),   # ramp direction up, ramp normal, T normal
             dn=(math.sin(tau), -math.cos(tau)))                                                                      # T's direction, downwards
    g["A"] = (RAMP_REACH - (WG_TOP_Z - FLOOR_Z) / math.tan(rd), WG_TOP_Z)             # cheek top corner: ramp meets K
    g["k"] = _DOT(g["rh"], g["A"])                                                     # K: rh.p = k (K runs along the ramp normal)
    g["t"] = _DOT(g["nt"], SA) + WG_FLANK_R                                            # T: nt.p = t, tangent to the R10 circle about SA
    g["Tk"] = _meet(g["rh"], g["k"], g["nt"], g["t"])
    g["z_nose"] = WG_TOP_Z - WG_SKIN_RUN * math.sin(rd)                                # nose top = the ramp point one skin run below A
    g["toe"] = (RAMP_REACH, FLOOR_Z)                                                   # ramp toe
    g["c_in"] = _DOT(g["nr"], g["toe"]) - WG_SKIN_T                                    # skin inner face: nr.p = c_in
    return g


def _t_at_z(z):
    g = _wg()
    return ((g["t"] - g["nt"][1] * z) / g["nt"][0], z)


def _poly(pts):
    from shapely.geometry import Polygon
    return Polygon(pts).buffer(0)


def _circle(c, r):
    from shapely.geometry import Point
    return Point(*c).buffer(r, ARC_N)


def _nose_polys():
    """(Q, Qz): the wedge between floor, ramp, K and T up to the cheek top (SB's ring joins it), and its part below the nose top."""
    g = _wg()
    off = g["t"] - _DOT(g["nt"], SB)                                                      # signed distance SB -> T
    half = math.sqrt(WG_BOSS_R ** 2 - off ** 2)
    tc = (SB[0] + off * g["nt"][0] - half * g["dn"][0], SB[1] + off * g["nt"][1] - half * g["dn"][1])   # T meets the ring round SB (upper point)
    base = [(SB[0], FLOOR_Z), g["toe"]]
    top = (RAMP_REACH - (g["z_nose"] - FLOOR_Z) / math.tan(math.radians(WG_RAMP_DEG)), g["z_nose"])
    return _poly(base + [g["A"], g["Tk"], tc]), _poly(base + [top, _t_at_z(g["z_nose"]), tc])


def _skin_poly():
    """Ramp skin: ramp, floor, toe chamfer, the inner face WG_SKIN_T below the ramp, the hollow's start line K2 (WG_SKIN_RUN below K), T up to the cheek corner."""
    g = _wg()
    v0 = ((g["c_in"] - g["nr"][1] * FLOOR_Z) / g["nr"][0], FLOOR_Z)                       # inner face meets the floor
    c, k2 = WG_TOE_CHAMFER, g["k"] - WG_SKIN_RUN
    return _poly([g["toe"], (v0[0] + c, FLOOR_Z), (v0[0] + c * g["rh"][0], FLOOR_Z + c * g["rh"][1]), _meet(g["rh"], k2, g["nr"], g["c_in"]),
                  _meet(g["rh"], k2, g["nt"], g["t"]), g["Tk"], g["A"]])


def _flank():
    """Cheek flank: the bulb arc about SA, then the R10 arc tangent to it and to K (its end tangent is the K line)."""
    g = _wg()
    th = math.degrees(math.atan2(g["rh"][1], g["rh"][0]))
    r2 = WG_SA_R + WG_FLANK_R
    phi = th - math.degrees(math.acos((g["k"] + WG_FLANK_R - _DOT(g["rh"], SA)) / r2))   # direction SA -> c2
    c2 = (SA[0] + r2 * math.cos(math.radians(phi)), SA[1] + r2 * math.sin(math.radians(phi)))
    return _arc(SA, WG_SA_R, 180, phi, ARC_N)[:-1] + _arc(c2, WG_FLANK_R, phi - 180, -WG_RAMP_DEG, ARC_N)


def _notch():
    """(P1, P2, N): the tail-entry notch floor corners (width back from T, depth down T from the cheek corner) and where its rear wall meets K."""
    g = _wg()
    p2 = (g["Tk"][0] + WG_NOTCH["depth"] * g["dn"][0], g["Tk"][1] + WG_NOTCH["depth"] * g["dn"][1])
    p1 = (p2[0] - WG_NOTCH["width"], p2[1])
    return p1, p2, _meet(g["rh"], g["k"], g["nt"], _DOT(g["nt"], p1))


def _cheek_poly():
    g = _wg()
    p1, p2, n = _notch()
    return _poly([g["A"], g["toe"], (SA[0] - WG_SA_R, FLOOR_Z), *_flank(), n, p1, p2, g["Tk"]])


def _bay_poly():
    """What the fork bay leaves standing in the cheek: the ramp side of T above the ledge, bounded below by the 45 deg tangent to the lug round SB."""
    g = _wg()
    r = LUG_SB_R + WG_MOUNT_GAP                                                         # the arc round SB stands WG_MOUNT_GAP off the chassis lug
    y45 = SB[0] + SB[1] + r * math.sqrt(2) - WG_BAY_Z                                   # the tangent y + z = const meets the ledge here
    return _poly([g["A"], g["toe"], (SB[0] + r, FLOOR_Z), *_arc(SB, r, 0, 45, ARC_N), (y45, WG_BAY_Z), _t_at_z(WG_BAY_Z), g["Tk"]])


def _slabs():
    x = [WG_X0]
    for w in WG_SLAB:
        x.append(x[-1] + w)
    return x   # block | ring step | skin | cheek | nose tab | end


def _cap_cutter():
    """The skin cap: a cylinder R = run + 1 whose axis (along the ramp normal) stands 1 above K on the block face WG_X0; everything above its
    lower arc (up the ramp) and left of its vertical tangent is carved from the skin."""
    from shapely.geometry import box
    b = _b()
    g = _wg()
    r = WG_SKIN_RUN + 1
    p0 = (g["A"][0] + g["rh"][0], g["A"][1] + g["rh"][1])                                # on the axis line: 1 above A along the ramp
    ax = (0, g["nr"][0], g["nr"][1])
    pl = b.Plane(origin=(WG_X0, p0[0] - RAMP_REACH * ax[1], p0[1] - RAMP_REACH * ax[2]), x_dir=(1, 0, 0), z_dir=ax)
    prof = _circle((0, 0), r).union(box(-r, -r, r, 0))                                      # local v = -(distance up the ramp)
    face = b.Face(b.Wire.make_polygon([pl.from_local_coords((u, v)) for u, v in list(prof.exterior.coords)[:-1]], close=True))
    return b.Solid.extrude(face, b.Vector(*[2 * RAMP_REACH * c for c in ax]))


def _ring_cone(x0, x1):
    """Ring step round SB: a 45 deg cone chamfering the far edge (left half only: the right half merges into the wedge)."""
    b = _b()
    cone = b.Solid.make_cone(WG_BOSS_R, WG_BOSS_R - 1, x1 - x0, b.Plane(origin=(x0, *SB), z_dir=(1, 0, 0)))
    return _I(cone, _box(x0, x1, SB[0] - 2 * WG_BOSS_R, SB[0], SB[1] - 2 * WG_BOSS_R, SB[1] + 2 * WG_BOSS_R))


def _floor_chamfer(body, x1):
    """Chamfer7 on the ring step's far floor edge: 1 mm x 45 deg plane to WG_RING_CHAMFER_Y, ending in a vertex blend with Fillet1."""
    from shapely.geometry import Polygon
    b = _b()
    y0, a, c = WG_RING_CHAMFER_Y, WG_CHAMFER_END["a"], WG_CHAMFER_END["b"]
    wedge = _ext(Polygon([(x1 - 1, FLOOR_Z), (x1, FLOOR_Z + 1), (x1, FLOOR_Z - 1), (x1 - 1, FLOOR_Z - 1)]), "xz", SB[0], y0)
    secs = []
    for i in range(1, 8):
        h = (i / 7) ** 2                                                                # chamfer height at this X (denser where the end curve is steep)
        ye = y0 + math.sqrt(a * h - c * h * h)
        pts = [(y0 - 0.5, FLOOR_Z - 0.5), (y0 - 0.5, FLOOR_Z + h), (y0, FLOOR_Z + h), (ye, FLOOR_Z), (ye, FLOOR_Z - 0.5)]
        secs.append(b.Wire([b.Edge.make_line(b.Vector(x1 - 1 + h, *p), b.Vector(x1 - 1 + h, *q)) for p, q in zip(pts, pts[1:] + pts[:1])]))
    return _S(body, wedge, b.Solid.make_loft(secs))


def _round_step(body, x):
    """Fillet1: the concave R1 where the skin's inner face (parallel to the ramp) leaves the ring step's face (plane X x): one bar along the
    inner face, square minus quarter disc in section, clipped to the nose wedge."""
    b = _b()
    g = _wg()
    on_face = [c for c in _skin_poly().exterior.coords if abs(_DOT(g["nr"], c) - g["c_in"]) < 1e-6]
    p, q = sorted(on_face[:2], key=lambda c: c[1])
    ln = math.dist(p, q)
    n = (-g["nr"][0], -g["nr"][1])                                                    # away from the skin, into the hollow
    P = lambda u, t: b.Vector(x + t, p[0] + u * n[0], p[1] + u * n[1])               # noqa: E731
    k = 1 - math.sqrt(0.5)
    prof = b.Wire([b.Edge.make_line(P(0, 0), P(1, 0)), b.Edge.make_three_point_arc(P(1, 0), P(k, k), P(0, 1)), b.Edge.make_line(P(0, 1), P(0, 0))])
    bar = b.Solid.extrude(b.Face(prof), b.Vector(0, q[0] - p[0], q[1] - p[1]))
    return _U(body, _I(bar, _ext(_nose_polys()[1], "yz", x, x + 1)))


def _prism(items, x0, x1):
    """Prism over X x0..x1 of a closed (Y, Z) outline of lines ('l', p, q) and arcs ('a', centre, r, a0, a1 deg, through the mid angle)."""
    b = _b()
    pt = lambda p: b.Vector(0, p[0], p[1])   # noqa: E731
    on = lambda rr, a, c: (c[0] + rr * math.cos(math.radians(a)), c[1] + rr * math.sin(math.radians(a)))   # noqa: E731
    edges = [b.Edge.make_line(pt(it[1]), pt(it[2])) if it[0] == "l" else
             b.Edge.make_three_point_arc(pt(on(it[2], it[3], it[1])), pt(on(it[2], (it[3] + it[4]) / 2, it[1])), pt(on(it[2], it[4], it[1])))
             for it in items]
    return b.Solid.extrude(b.Face(b.Wire(edges)), b.Vector(x1 - x0, 0, 0)).moved(b.Location((x0, 0, 0)))


def _kidney_entry(xc, xt):
    """(kidney slot, entry channel): the fork pin's arc slot round SB (r = FK_PIN_DIST, centred on the pin's rest angle, +-WG_PIN_SWING,
    half width 1) through the cheek, and the 1 mm deep channel from the notch to its upper cap, bounded by the slot's outer wall, a rear edge
    from the notch floor and a front edge tangent to the cap. The channel's wall floors are rounded 0.5 on the cutter."""
    b = _b()
    r = FK_PIN_DIST
    a_hi, a_lo = 90 + FK_PIN_ANG - WG_PIN_SWING, 90 + FK_PIN_ANG + WG_PIN_SWING
    on = lambda rr, a, c=SB: (c[0] + rr * math.cos(math.radians(a)), c[1] + rr * math.sin(math.radians(a)))   # noqa: E731
    ch, cl = on(r, a_hi), on(r, a_lo)

    kid = _prism([("a", SB, r + 1, a_lo, a_hi), ("a", ch, 1, a_hi, a_hi - 180), ("a", SB, r - 1, a_hi, a_lo), ("a", cl, 1, a_lo + 180, a_lo)],
                xc - 0.5, xt + 0.5)
    p1, p2, _n = _notch()
    d = math.dist(p2, ch)
    a_t = math.degrees(math.atan2(p2[1] - ch[1], p2[0] - ch[0]) - math.acos(1 / d))   # tangent from the notch floor to the upper cap (half width 1)
    q, t_pt, mid = on(r + 1, a_lo), on(1, a_t, ch), on(r, (a_lo + a_hi) / 2)
    ent = _prism([("l", p1, q), ("l", q, mid), ("l", mid, ch), ("l", ch, t_pt), ("l", t_pt, p2), ("l", p2, p1)], xt - 1, xt)
    near = lambda p, v: abs(p.Y - v[0]) < GEO_EPS and abs(p.Z - v[1]) < GEO_EPS   # noqa: E731
    walls = [(p1, q), (t_pt, p2)]
    edges = [e for f in ent.faces() if abs(f.center().X - (xt - 1)) < GEO_EPS and f.geom_type == b.GeomType.PLANE for e in f.edges()
             if any((near(e.start_point(), u) and near(e.end_point(), v)) or (near(e.start_point(), v) and near(e.end_point(), u)) for u, v in walls)]
    try:
        ent = ent.fillet(0.5, edges)
    except Exception:  # noqa: BLE001 - a failed blend keeps the sharp channel
        pass
    return kid, ent


def _tab_poly(mount):
    """Nose tab: the bay's ramp side with the weapon mount's boss (plus the WG_MOUNT_GAP clearance) taken out; films thinner than a TPU wall are
    dropped by reconstruction (the surviving body keeps its own sharp tips)."""
    from .mount import _mount_clip, _mount_profile
    cut = _bay_poly().difference(_mount_profile(mount).intersection(_mount_clip()).buffer(WG_BOSS_GAP, join_style=2))
    return cut.intersection(cut.buffer(-WG_TAB_FILM, join_style=2).buffer(WG_TAB_FILM + WG_MERGE_EPS, join_style=2)) if WG_TAB_FILM else cut


def _wedgelet_lh(mount):
    """The left wedgelet before the side-specific seats: nose block + ring step, skin, cheek with its fork bay, kidney and entry, nose tab."""
    xb, xr, xs, xc, xt, xe = _slabs()
    q, qz = _nose_polys()
    cap = _cap_cutter()
    nose = _U(_S(_ext(q, "yz", xb, xs), cap), _ext(qz, "yz", xb, xs), _cyl(WG_BOSS_R, xb, xr, SB), _ring_cone(xr, xs))
    nose = _floor_chamfer(nose, xs)
    skin = _S(_ext(_skin_poly(), "yz", xs, xc), cap)
    gusset = _I(_ext(qz, "yz", xs, xc), cap)                  # past the ring step the nose top stays above the cap arc until the arc leaves it
    cheek, tab = _cheek_poly(), _tab_poly(mount)
    body = _U(nose, skin, gusset, _ext(cheek, "yz", xc, xt), _ext(tab, "yz", xt, xe) if not tab.is_empty else None)
    body = _round_step(body, xs)
    kidney, entry = _kidney_entry(xc, xt)
    bay = cheek.difference(_bay_poly().union(_circle(SA, WG_BOSS_R)))
    clr = 0.5                                                 # fork sheet clearance each side
    f0, f1 = FK_X[-1][0] - clr, FK_X[-1][1] + clr
    bx0, bx1 = xb - clr, xe + clr
    return _S(body, _ext(bay, "yz", f0, f1), _cyl(WG_BORES["sa"], bx0, bx1, SA), _cyl(WG_BORES["sb"], bx0, bx1, SB),
              _cyl(WG_BORES["sb_head"], xr, bx1, SB), kidney, entry)


def wedgelet(s):
    """RV17 (s = -1, built) / RV18 (s = +1, its mirror): the TPU wedgelet, with the side's fork tine and weapon-mount seats cut out."""
    from .fork import _fork_slot
    from .mount import weapon_mount
    mount = "l" if s < 0 else "r"
    sh = _wedgelet_lh(mount)
    sh = sh if s < 0 else _mirror_x(sh)
    c = sum(FK_X[s]) / 2                                   # the slit (printable variant) is centred on the tine
    slit = [_I(_fork_slot(s), _box(c - WG_SLIT_W / 2, c + WG_SLIT_W / 2, *WG_FAR))] if WG_SLIT_W else []
    return _S(sh, *slit, weapon_mount(mount))
