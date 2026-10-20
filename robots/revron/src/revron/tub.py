"""[fix-S] Chassis tub and its panels: chassis, base_panel, top_panel, esc_tray, inserts / panel seats."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from shapely.geometry import Point, Polygon


def _panel_seat(which, i):
    """(cutter, FastenerRecord) of the M2 flat-head seat in the base / top panel (robot.cad.holes, head side only): the
    90 deg seat is 4.5 at the face (ISO 10642 dk 3.8 + 0.7: also clears the verifier's 4.4 head); the panels add a wider
    relief hole (BASE_HOLE / TOP_HOLE) so the seat stops short of the far face."""
    sys.path.insert(0, ROOT)
    from robot.cad.holes import hole_tool
    if which == "base":
        x, y = INS[i]
        return hole_tool((x, y, BASE_Z0), (0, 0, 1), "M2x6", head="csk", into="through", side="head", grip=BASE_T + BOSS_H, csk_clear=CSK_CLEAR)
    x, y = TOP_XY[i]
    return hole_tool((x, y, TOP_Z0 + TOP_T), (0, 0, -1), "M2x5", head="button", into="through", side="head", grip=TOP_T, cbore=0)   # 0.9 Ti is too thin for an M2 flat-head seat (1.2 tall): a button head bears flat on the face, plain 2.2 clearance hole


def _panel_outline(grow):
    """RV26 outline (56.2 x 49.2, R0.8) plus R3.0 ears round the screws that sit 2.6 mm from its edge, so the 4.5
    countersink keeps a rim; `grow` > 0 gives the matching chassis rabbet."""
    from shapely.geometry import Point
    o = BASE_OUT
    x, y0, y1 = o["x"] + grow, o["y0"] - grow, o["y1"] + grow
    p = _round(_poly([(-x, y0), (x, y0), (x, y1), (-x, y1)]), r_out=o["r"])
    for x, y in INS:
        if min(o["y1"] - y, y - o["y0"]) < PANEL_EAR_EDGE:
            p = p.union(Point(x, y).buffer(PANEL_EAR_R + grow, SEG))
    return _round(p, r_in=PANEL_R_IN)


def base_panel():
    """RV26: 1 mm printed panel under the open chassis, 5 M2 CSK into the floor heat-sets; two 0.45 mm pads under the
    N10 gearboxes preload the motors up into their keyhole pockets."""
    z0, t = BASE_Z0, BASE_T
    out = _panel_outline(0.0)
    b = _b()
    body = _solid(_ext(out, "xy", z0, z0 + t))
    px, py, side, ph, pr = TB_PAD
    for s in (1, -1):   # [fix-D] 0.45: top 4.95, 0.05 under the N10; plain boxes (not shapely polylines) so the base can take a fillet
        pad = b.Pos(s * px, py, z0 + t - TB_SINK + ph / 2) * b.Box(side, side, ph)
        body = body + b.fillet(pad.edges().filter_by(b.Axis.Z), pr)
    # the 1 mm skin is thinner than the 1.2 mm M2 flat head: a 0.3 mm ring boss over each screw gives the seat 1.3 mm of
    # material (no knife edge under the head) and keys the panel into the column feet, so side hits shear the bosses, not the screws
    for x, y in INS:
        body = body + b.Pos(x, y, z0 + t - TB_SINK + (BOSS_H + TB_SINK) / 2) * b.Cylinder(BOSS_R, BOSS_H + TB_SINK)
    # R0.25 where pads and bosses meet the skin: no sharp internal corner in the print (the STEP has r 0.5 at the pads)
    skin_top = z0 + t
    def _base_edge(e):
        tz, tf, tr, tl = TB_EDGE_TOL
        if abs(e.center().Z - skin_top) > tz or abs(e.bounding_box().max.Z - e.bounding_box().min.Z) > tf:
            return False
        fs = [f for f in body.faces() if any(e.is_same(x) for x in f.edges())]
        return len(fs) == 2 and any(f.bounding_box().max.Z > skin_top + tr and f.bounding_box().min.Z < skin_top + tl for f in fs)
    body = b.fillet([e for e in body.edges() if _base_edge(e)], TB_SKIN_FILLET)
    cuts = [_panel_seat("base", i)[0] for i in range(len(INS))] + [_cyl(BASE_HOLE / 2, z0 - TB_CSK_CUT[0], z0 + TB_CSK_CUT[1], (x, y), "z") for x, y in INS]   # 4.5 countersink (STEP RV26 has 3.2 x 0.5; an ISO 10642 M2 head is 4.4 x 1.2, so a smaller seat leaves it proud and binding) then the 2.2 hole
    return _S(body, *cuts)


def top_panel():
    """0.9 mm Ti top panel: four countersunk 2.2 holes in the corner ears over the insert columns take M2 flat-head thread-forming screws
    into 1.7 pilots in the column tops (the STEP has the holes, not the screws). The
    front notches clear the weapon-mount tabs; it stops at |X| 23 beside the switch so the switch stays reachable."""
    z0, t, X, (nx0, nx1), sy = TOP_Z0, TOP_T, TOP_X, TOP_NOTCH_X, TOP_SHOULDER_Y
    core = _poly([(-X, TOP_Y0), (X, TOP_Y0), (X, sy), (nx1, sy), (nx1, TOP_Y1), (-nx1, TOP_Y1), (-nx1, sy), (-X, sy)])
    notch = [_poly([(s * nx0, sy), (s * nx1, sy), (s * nx1, TOP_CUT_Y), (s * nx0, TOP_CUT_Y)]) for s in (1, -1)]
    from shapely.geometry import Point
    ears = [Point(x, y).buffer(EAR_R, SEG) for x, y in TOP_XY]
    # the ears run into the side edges along concave arcs (STEP): each arc is tangent to the |X| TOP_X edge and to its ear
    fills = []
    ex = TOP_XY[0][0]
    a = ex - X                                   # ear centre inboard offset from the side edge
    for sx in (1, -1):
        for ey, yt in zip(sorted({y for _, y in TOP_XY}, reverse=True), TOP_FILL_YT):
            d = abs(ey - yt)
            R = (a * a + d * d - EAR_R ** 2) / (2 * a + 2 * EAR_R)   # (R - a)^2 + d^2 = (R + EAR_R)^2: arc tangent to the edge and the ear
            cx = sx * (X + R)
            box = _poly([(sx * X, yt), (sx * TOP_FILL_X, yt), (sx * TOP_FILL_X, ey), (sx * X, ey)])
            fills.append(box.difference(Point(cx, yt).buffer(R, SEG_FINE)))
    p = core
    fills += [_poly([(sx * nx1, sy), (sx * ex, sy), (sx * ex, TOP_Y1), (sx * nx1, TOP_Y1)]) for sx in (1, -1)]
    for q in ears + fills:
        p = p.union(q)
    for q in notch:
        p = p.difference(q)
    p = p.difference(_poly([(-nx0, TOP_TAB_Y), (nx0, TOP_TAB_Y), (nx0, TOP_CUT_Y), (-nx0, TOP_CUT_Y)]))   # tab front edge
    p = _round(p, r_out=TOP_R_OUT, r_in=TOP_R_IN)
    body = _ext(p, "xy", z0, z0 + t)
    # 2.2 holes countersunk (90 deg, 4.5 at the top face; STEP 3.65) for M2 flat heads into the column-top pilots: the 1.2 head is
    # deeper than the 0.9 plate, so its tip sinks into the chamfer at the column top
    return _S(body, *[_panel_seat("top", i)[0] for i in range(len(TOP_XY))])


def _switch_hole(yy):
    """robot.cad.holes record for a switch screw: M2x3 button thread-forming up into the 1.7 pilot of the deck pad (3.0 mm of pad above its 16.0 head seat)."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool((SWX, yy, 16.0), (0, 0, 1), "M2x3", head="button", into="tapped", side="thread", engage=3.0)


# ------------------------------------------------------------------------------------------------------------ chassis
def _wall_pocket(x0, x1, z0, z1, y0, y1, r_vert=0.5, r_floor=0.8):
    """Rectangular front-wall pocket cutter (X x Z, floor at y1): R0.5 corners and an R0.8 floor, as in the STEP."""
    b = _b()
    s = _box(x0, x1, y0, y1, z0, z1)
    s = b.fillet(s.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[-1].edges(), r_floor)


def _lattice_pocket(pts, y0=-36.5, y1=-35.5, r_vert=0.5, r_floor=0.25):
    """Cutter of one triangular rear-wall pocket (X, Z outline `pts`): R0.45 corners and an R0.95 floor (the STEP's R0.98),
    so the pocket has no sharp internal corner in the print."""
    b = _b()
    with b.BuildPart() as bp:
        with b.BuildSketch(b.Plane.XZ.offset(-y1)):
            b.Polygon(*pts, align=None)
        b.extrude(amount=y1 - y0)
    s = b.fillet(bp.part.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[0].edges(), r_floor)


def _sg(pts, sg):
    """Points mirrored to side `sg` (X sign), order kept."""
    return [(sg * u, v) for u, v in pts]


def _mx(poly, sg):
    """Polygon mirrored to side `sg`."""
    return Polygon(_sg(poly.exterior.coords, sg)).buffer(0)


def _nose(x0, y0, dx, dy, r, seg=48):
    """The corner region at (x0, y0) outside an R r round (dx, dy: directions into the block)."""
    q = Polygon([(x0, y0), (x0 + dx * r, y0), (x0 + dx * r, y0 + dy * r), (x0, y0 + dy * r)])
    return q.difference(Point(x0 + dx * r, y0 + dy * r).buffer(r, seg))


def _ch_shell():
    """Closed-top box printed deck-down: 2 mm chamfer round the top edges, inner bay open at the floor."""
    c = CH
    x, y0, y1, z0, z1, w = c["x"], c["y0"], c["y1"], c["z0"], c["z1"], c["wall"]
    plan = _round(Polygon([(-x, y0), (x, y0), (x, y1), (-x, y1)]), r_out=2.0)
    b = _b()
    top = _round(Polygon([(-x + 2, y0 + 2), (x - 2, y0 + 2), (x - 2, y1 - 2), (-x + 2, y1 - 2)]), r_out=0.5)
    lo = _face(plan, "xy")[0].outer_wire().moved(b.Location((0, 0, z1 - 2.0)))
    hi = _face(top, "xy")[0].outer_wire().moved(b.Location((0, 0, z1)))
    outer = _U(_ext(plan, "xy", z0, z1 - 2.0), b.Solid.make_loft([lo, hi], ruled=True))
    inner = _round(Polygon([(-x + w, y0 + w), (x - w, y0 + w), (x - w, y1 - w), (-x + w, y1 - w)]), r_out=1.0)
    return _S(outer, _ext(inner, "xy", z0 - 1, c["deck"]))


def _ch_columns():
    """Insert columns floor to deck: rear-centre round boss; every foot flares to R3.7 (56 deg cone, prints deck-down
    without support) so the base-panel boss recess keeps a 1 mm wall. Corner blocks come from _ch_blocks."""
    b = _b()
    z0, top = CH["z0"], CH["deck"] + TB_OV
    add = [_cyl(TB_COL_R, z0, top, INS[4], "z")]
    for px, py in INS:
        add.append(_cyl(TB_FOOT_R, z0, TB_FOOT_Z, (px, py), "z"))
        add.append(b.Solid.make_cone(TB_FOOT_R, TB_COL_R, TB_FOOT_CONE, b.Plane(origin=(px, py, TB_FOOT_Z - TB_EPS), z_dir=(0, 0, 1))))
    return add


def _ch_blocks(sg):
    """Corner column blocks merged into the wall corners (R2.5 / R2.6 nose, R0.8 / R0.9 fillets into the walls)."""
    out = []
    for pts, cut, fils in TB_BLKS:
        p = Polygon(pts).difference(_nose(*cut))
        for f in fils:
            p = p.union(_nose(*f))
        out.append(_ext(_mx(p, sg), "xy", CH["z0"], CH["deck"] + TB_OV))
    return out


def _ch_motor_walls(sg):
    """Motor front stop wall (the N10 gearbox bears on it) plus the retention comb: a key tab between the last two gearbox
    plates and a ledge 0.1 over them, both hanging from the deck (printed deck-down: no supports)."""
    c = CH
    wall_x = c["x"] - c["wall"] + TB_OV
    top = c["deck"] + TB_OV
    return [_box(sg * TB_STOP[0], sg * wall_x, TB_STOP[1], TB_STOP[2], c["z0"], top),
            _box(sg * N10_KEY[0], sg * N10_KEY[1], TB_KEY[0], TB_KEY[1], TB_KEY[2], top),
            _box(sg * TB_LEDGE[0], sg * wall_x, TB_LEDGE[1], TB_LEDGE[2], N10_TOP + TB_OV, top)]


def _ch_lobe(sg):
    """Side lobe with the thin M3 nut, root fillet (STEP R1.95) as one ruled loft of the quarter round."""
    x, R_, n = CH["x"], TB_LOBE_R, TB_LOBE_N
    lobe = NUT_LOBE
    return [_ext(lobe, "yz", sg * (x - TB_OV), sg * TB_LOBE_X1),
            _loft_yz_n([(lobe.buffer(R_ - math.sqrt(R_ * R_ - (R_ - h) ** 2), join_style=1), sg * (x - TB_OV + h))
                        for h in (R_ * k / n for k in range(n + 1))])]


def _ch_tabs(sg):
    """Front tabs (key into the weapon-mount notches), the inner tab wall (top-front corner cut back round the weapon axis)
    and the R2 fillet into the front face."""
    tabw = _poly(TB_TABW_PTS).difference(Point(WY, WZ).buffer(WEAPON_CLEAR_R, 128))
    fpts, fc, fr = TB_TABFIL
    fil = Polygon(fpts).difference(Point(*fc).buffer(fr, 48))
    return [_ext(_poly(TB_TAB_PTS), "yz", sg * TB_TAB_X[0], sg * TB_TAB_X[1]),
            _ext(tabw, "yz", sg * TB_TABW_X[0], sg * TB_TABW_X[1]),
            _ext(_mx(fil, sg), "xy", CH["z0"], CH["deck"])]


def _ch_switch_pad(sg):
    """Switch pad under the deck (STEP): the switch ears bear on it (right side only)."""
    if sg < 0:
        return []
    pts, zb = TB_SWPAD
    return [_ext(_round(Polygon(pts), r_out=1.0), "xy", zb, CH["deck"] + TB_OV)]


def _ch_lug(sg):
    """Lug carrying the standoffs (sloped top so it sits under the mount)."""
    lug = Polygon(TB_LUG_HEAD + _arc(SA, *TB_LUG_ARCA) + [TB_LUG_MID] + _arc(SB, *TB_LUG_ARCB) + TB_LUG_TAIL)
    lug = _round(lug.convex_hull.difference(Polygon(TB_LUG_CUT)), r_in=0.0)
    return [_ext(lug, "yz", sg * TB_LUG_X[0], sg * TB_LUG_X[1])]


def _ch_flanges(sg):
    """Front corner flanges (STEP): a bottom flange blending the side wall into the lug, a top flange carrying the deck
    chamfer forward to the lug, and a gusset (52 deg) under the flange top so it is not an unsupported ceiling."""
    z0 = CH["z0"]
    fb, fc, fr = TB_FACE_B
    face = Polygon(TB_FACE_A).union(Polygon(fb).difference(Point(*fc).buffer(fr, 64)))
    bot = _mx(Polygon(TB_BOT_HEAD + TB_BLEND), sg)
    gpts, gy0, gy1, gz = TB_GUS
    gus = _ext(_poly(_sg(gpts, sg)), "xz", gy0, gy1)
    tpts, tx0, tx1 = TB_TOPF
    topf = _ext(_poly(tpts), "yz", sg * tx0, sg * tx1)
    tpoly = Polygon(TB_TOPF_HEAD + TB_BLEND + TB_TOPF_TAIL).buffer(0)
    return [_ext(_mx(face, sg), "xy", z0, TB_FACE_Z), _ext(bot, "xy", z0, TB_BOT_Z1), _I(gus, _ext(bot, "xy", z0, gz)),
            _I(topf, _ext(_mx(tpoly, sg), "xy", *TB_TOPF_Z))]


def _ch_lug_cuts(sg):
    """Lug underside: flat then the ramp; a scallop between the two standoffs; the nose standoff follows its arc; the
    front wall stops at the rabbet under the tab; motor stop wall lower inner edge rounded R4.5 (STEP)."""
    x0, x1 = (sg * v for v in TB_LUGCUT_X)
    upts, ur, useg = TB_UNDER
    under = Polygon(upts).difference(Point(SB).buffer(ur, useg))
    fpts, fc, fr, fy = TB_STOPFIL
    fil = Polygon(fpts).difference(Point(*fc).buffer(fr, 64))
    r = TB_RABBET
    return [_ext(_poly(TB_LUGCUT_A), "yz", x0, x1), _ext(LUG_SCALLOP, "yz", x0, x1), _ext(under, "yz", x0, x1),
            _box(sg * r[0], sg * r[1], r[2], r[3], CH["z0"] - TB_OV, r[4]),
            _ext(_mx(fil, sg), "xz", *fy)]


def _ch_deck_pockets():
    """Deck X-pocket lightening from below (1 mm skin stays): X of 2 mm ribs, side and rear pockets."""
    dz0, dz1 = (CH["deck"] + d for d in TB_DECK_CUT)
    cuts = [_ext(_round(Polygon(t), r_out=TB_DECK_R), "xy", dz0, dz1) for t in TB_TRI]
    for sg in (1, -1):
        cuts.append(_ext(_round(Polygon(_sg(TB_SIDEPK, sg)), r_out=TB_SIDEPK_R), "xy", dz0, dz1))
    xs, ya, yb, rr = TB_REARPK
    for xa, xb in zip(xs[::2], xs[1::2]):
        cuts.append(_ext(_round(Polygon([(xa, ya), (xb, ya), (xb, yb), (xa, yb)]), r_out=rr), "xy", dz0, dz1))
    cpts, cr = TB_REARPK_C
    cuts.append(_ext(_round(Polygon(cpts), r_out=cr), "xy", dz0, dz1))
    return cuts


def _ch_insert_holes():
    """3.0 hole floor to deck with 0.6 chamfers both ends (STEP; the M2 heat-set melts into the bottom); the corner columns
    stop 4 mm under the top and take a 1.7 thread-forming pilot for the top-panel screw."""
    h, z0, z1 = TB_CHOLE, CH["z0"], CH["z1"]
    bb = _b()
    cone = lambda px, py, z, d: bb.Solid.make_cone(h["ch_r"], h["bore"], h["ch_h"], bb.Plane(origin=(px, py, z), z_dir=(0, 0, d)))
    cuts = []
    for px, py in INS:
        rear = (px, py) == tuple(INS[4])
        cuts.append(_cyl(h["bore"], z0 - 1.0, (z1 + 1) if rear else z1 - h["blind"], (px, py), "z"))
        cuts.append(cone(px, py, h["ch_z"] - TB_EPS, 1))
        if not rear:
            cuts.append(_cyl(h["pilot_r"], z1 - h["pilot_z"], z1 + 1, (px, py), "z"))
        cuts.append(cone(px, py, z1 + TB_EPS, -1))
    return cuts


def _ch_switch_slot():
    """Switch slot in the deck beside the top panel (inner edge at the top-panel edge) and its 2 M2 pilot holes."""
    sx, sw, sy, sl, sr, sz = TB_SWSLOT
    z1 = CH["z1"]
    cuts = [_ext(_round(Polygon([(sx, sy), (sx + sw, sy), (sx + sw, sy + sl), (sx, sy + sl)]), r_out=sr), "xy", sz, z1 + 1)]
    cuts += [_cyl(TB_SWPILOT_R, CH["deck"] - TB_SWPILOT_DZ, z1 + 1, (SWX, yy), "z") for yy in TB_SWPILOT]
    return cuts


def _hex_pocket(cx, cy, r1, r2, step=60, off=30, n=6):
    """Hex pocket 0.05 under the nut's 5.5 AF / 6.35 corners (pressed in, cannot shake loose into the bay)."""
    ang = [math.radians(step * i + off) for i in range(n)]
    return Polygon([(cx + r1 * math.cos(a), cy + r2 * math.sin(a)) for a in ang])


def _keyhole(z0, seat_seg=64, pilot_seg=24):
    """N10 keyhole (YZ): round seat narrowing to the floor, opened into a U-slot so the gearbox boss and shaft drop in from below."""
    kr, kz, kpr, kw = TB_KH
    kh = Point(RY, RZ).buffer(kr, seat_seg).union(Point(RY, kz).buffer(kpr, pilot_seg)).convex_hull   # STEP keyhole
    return kh.union(Polygon([(RY - kw, z0 - 1.0), (RY + kw, z0 - 1.0), (RY + kw, RZ), (RY - kw, RZ)]))


def _ch_side_cuts(sg):
    """Per side wall: N10 keyhole (U-slot to the floor so the gearbox drops in from below), M3 nut clearance and hex pocket,
    nut-lobe slot, standoff holes in the lugs and the square key hole."""
    c = CH
    x, w, z0 = c["x"], c["wall"], c["z0"]
    kh = _keyhole(z0)
    nr, nx0, nx1 = TB_NUTHOLE
    b = TB_NUTREL
    hr1, hr2, hx0, hx1 = TB_HEX
    hexp = _hex_pocket(NUT[0], NUT[1], hr1, hr2)
    spts, sr, sx0, sx1 = TB_NUTSLOT
    ra, rb, sx_a, sx_b = TB_STANDOFF
    kpts, kr_, kx0, kx1 = TB_KEYHOLE
    return [_ext(kh, "yz", sg * (x - w - 0.5), sg * (x + 0.5)),
            _cyl(nr, sg * nx0, sg * nx1, NUT),
            _box(sg * b[0], sg * b[1], b[2], b[3], z0 - b[4], z0),
            _ext(hexp, "yz", sg * hx0, sg * hx1),
            _ext(_round(Polygon(spts), r_out=sr), "yz", sg * sx0, sg * sx1),
            _cyl(ra, sg * sx_a, sg * sx_b, SA),
            _cyl(rb, sg * sx_a, sg * sx_b, SB),
            _ext(_round(Polygon(kpts), r_out=kr_), "yz", sg * kx0, sg * kx1)]


def _ch_rear_cuts():
    """Rear wall 1 mm deep triangle lattice on the inner face (STEP), the weapon phase-wire hole and the front-wall pockets."""
    cuts = []
    for sg in (1, -1):
        for t in TB_LAT:
            g = Polygon(_sg(t, sg)).buffer(LAT_GROW, join_style=2)   # STEP rib is 0.35 thinner than the nominal edges
            cuts.append(_lattice_pocket(list(g.exterior.coords)[:-1]))
    wpts, wr, wz0, wz1 = TB_WIRE
    cuts.append(_ext(_round(Polygon(wpts), r_out=wr), "xz", wz0, wz1))
    spans, pz0, pz1, py0, py1 = TB_WALLPK
    cuts += [_wall_pocket(xa, xb, pz0, pz1, py0, py1) for xa, xb in spans]
    return cuts


def _ch_panel_seats(sg):
    """Rabbet for the base panel (flush with the wall bottom lip), recess in each column foot for the ring boss, the motor
    preload pad recess, and the squared R1 inner rear corner where the N10 plates sit."""
    c = CH
    cuts = []
    if sg > 0:
        cuts.append(_ext(_panel_outline(0.05), "xy", c["z0"] - 1.0, TB_RABBET_Z[0]))
        cuts += [_cyl(BOSS_R + 0.3, TB_RABBET_Z[1], TB_RABBET_Z[0] + BOSS_H + 0.05, (px, py), "z") for px, py in INS]
    p = TB_PADREC
    cx, ce, cy = TB_CORNER
    cuts.append(_box(sg * p[0], sg * p[1], p[2], p[3], p[4], p[5]))
    cuts.append(_box(sg * cx, sg * (c["x"] - c["wall"] + ce), c["y0"] + c["wall"] - ce, c["y0"] + c["wall"] + cy, c["z0"] + 2.0, c["deck"]))
    return cuts


def _ch_cage():
    """Electronics cage hung from the deck: ribs 0.1 mm off the Malenki's -x / +x / -y faces and the weapon ESC's -y face,
    so neither board hammers around when the robot is flipped."""
    (ex0, ex1), (ey0, ey1), ez0 = RX_X, RX_Y, RX_Z[0]
    g, (wa, wb), (ya, yb), ztop = TB_CAGE_G, TB_CAGE_W, TB_CAGE_Y, CH["deck"] + TB_CAGE_TOP
    ex, ew, ez = TB_CAGE_ESC
    return [_box(ex0 - g - wa, ex0 - g, ya, yb, ez0, ztop),
            _box(ex1 + g, ex1 + g + wb, ya, yb, ez0, ztop),
            _box(0.0, ex, ey0 - g - ew, ey0 - g, WE_Z[0] + ez, ztop)]


def chassis():
    """RV01 printed chassis: a closed-top box printed deck-down (no supports: the deck is the first layer), open
    underneath for the base panel. X-ribbed deck pockets; 5 insert columns floor to deck; N10 keyhole pockets in the
    side walls; a lobe on each side wall with the captive thin M3 nut; front tabs that key the weapon mounts and
    lugs that carry the standoffs."""
    add = _ch_columns()
    for sg in (1, -1):
        add += _ch_blocks(sg) + _ch_motor_walls(sg) + _ch_lobe(sg) + _ch_tabs(sg) + _ch_switch_pad(sg) + _ch_lug(sg)
    for sg in (1, -1):
        add += _ch_flanges(sg)
    body = _U(_ch_shell(), *add)
    cuts = []
    for sg in (1, -1):
        cuts += _ch_lug_cuts(sg)
    cuts += _ch_deck_pockets() + _ch_insert_holes() + _ch_switch_slot()
    for sg in (1, -1):
        cuts += _ch_side_cuts(sg)
    cuts += _ch_rear_cuts()
    for sg in (1, -1):
        cuts += _ch_panel_seats(sg)
    # the STEP panel and lobe overlap where the panel relief stops: the whole overlapping slab of the lobe tail goes with
    # it, so no 0.05 mm sliver of lobe is left beside the cut
    tpts, tx = TB_TAIL
    tail = NUT_LOBE.intersection(Polygon(tpts))
    cuts += [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)] + [_ext(tail, "yz", sg * PANEL_IN, sg * (CH["x"] + tx)) for sg in (1, -1)]
    return _U(_S(body, *cuts), *_ch_cage())


def esc_tray():
    """TPU tray glued to the base panel under the weapon ESC (not in the STEP, where kapton alone holds it): two rails carry
    the board 0.1 mm off, 1 mm lips 0.1 mm off its -x / +x / +y sides (leads leave above the lips at the board mid-plane).
    The deck cage holds -y and the Malenki above it +z, so the ESC cannot rattle inverted; base panel off, it lifts out."""
    (wx0, wx1), (wy0, wy1), wz0 = WE_X, WE_Y, WE_Z[0]
    T = ESC_TRAY
    g, w, e = T["gap"], T["wall"], T["fuse"]
    z0, top = BASE_Z0 + BASE_T, wz0 + T["lip"]   # sits on the base panel top face; lips rise 1 mm past the board underside
    zw = z0 + w - e
    parts = [_box(wx0 - g - w, wx1 + g + w, wy0, wy1 + g + w, z0, z0 + w)]
    parts += [_box(xa, xa + w, wy0 + T["rail_end"], wy1 - T["rail_end"], zw, wz0 - g) for xa in (wx0 + T["rail_x"][0], wx1 - T["rail_x"][1])]
    parts += [_box(wx0 - g - w, wx0 - g, wy0, wy1 + g + w, zw, top), _box(wx1 + g, wx1 + g + w, wy0, wy1 + g + w, zw, top),
              _box(wx0 - g - w, wx1 + g + w, wy1 + g, wy1 + g + w, zw, top)]
    return _U(*parts)
