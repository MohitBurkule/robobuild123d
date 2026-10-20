"""[fix-S] Chassis tub and its panels: chassis, base_panel, top_panel, esc_tray, inserts / panel seats."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


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
    z0, t = 3.5, 1.0
    out = _panel_outline(0.0)
    b = _b()
    body = _solid(_ext(out, "xy", z0, z0 + t))
    for s in (1, -1):   # [fix-D] 0.45: top 4.95, 0.05 under the N10; plain boxes (not shapely polylines) so the base can take a fillet
        pad = b.Pos(s * 22.5, -30.3, z0 + t - 0.01 + 0.2325) * b.Box(9.1, 9.1, 0.465)
        body = body + b.fillet(pad.edges().filter_by(b.Axis.Z), 0.6)
    # the 1 mm skin is thinner than the 1.2 mm M2 flat head: a 0.3 mm ring boss over each screw gives the seat 1.3 mm of
    # material (no knife edge under the head) and keys the panel into the column feet, so side hits shear the bosses, not the screws
    for x, y in INS:
        body = body + b.Pos(x, y, z0 + t - 0.01 + (BOSS_H + 0.01) / 2) * b.Cylinder(BOSS_R, BOSS_H + 0.01)
    # R0.25 where pads and bosses meet the skin: no sharp internal corner in the print (the STEP has r 0.5 at the pads)
    skin_top = z0 + t
    def _base_edge(e):
        if abs(e.center().Z - skin_top) > 0.02 or abs(e.bounding_box().max.Z - e.bounding_box().min.Z) > 1e-3:
            return False
        fs = [f for f in body.faces() if any(e.is_same(x) for x in f.edges())]
        return len(fs) == 2 and any(f.bounding_box().max.Z > skin_top + 0.1 and f.bounding_box().min.Z < skin_top + 0.01 for f in fs)
    body = b.fillet([e for e in body.edges() if _base_edge(e)], 0.25)
    cuts = [_panel_seat("base", i)[0] for i in range(len(INS))] + [_cyl(BASE_HOLE / 2, z0 - 1, z0 + 3, (x, y), "z") for x, y in INS]   # 4.5 countersink (STEP RV26 has 3.2 x 0.5; an ISO 10642 M2 head is 4.4 x 1.2, so a smaller seat leaves it proud and binding) then the 2.2 hole
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


def chassis():
    """RV01 printed chassis: a closed-top box printed deck-down (no supports: the deck is the first layer), open
    underneath for the base panel. X-ribbed deck pockets; 5 insert columns floor to deck; N10 keyhole pockets in the
    side walls; a lobe on each side wall with the captive thin M3 nut; front tabs that key the weapon mounts and
    lugs that carry the standoffs."""
    from shapely.geometry import Point, Polygon
    c = CH
    x, y0, y1, z0, z1, w = c["x"], c["y0"], c["y1"], c["z0"], c["z1"], c["wall"]
    plan = _round(Polygon([(-x, y0), (x, y0), (x, y1), (-x, y1)]), r_out=2.0)
    b = _b()
    outer = _ext(plan, "xy", z0, z1)
    # 2 mm chamfer round the top edges (hits slide over)
    top = _round(Polygon([(-x + 2, y0 + 2), (x - 2, y0 + 2), (x - 2, y1 - 2), (-x + 2, y1 - 2)]), r_out=0.5)
    lo = _face(plan, "xy")[0].outer_wire().moved(b.Location((0, 0, z1 - 2.0)))
    hi = _face(top, "xy")[0].outer_wire().moved(b.Location((0, 0, z1)))
    cap = b.Solid.make_loft([lo, hi], ruled=True)
    outer = _U(_ext(plan, "xy", z0, z1 - 2.0), cap)
    inner = _round(Polygon([(-x + w, y0 + w), (x - w, y0 + w), (x - w, y1 - w), (-x + w, y1 - w)]), r_out=1.0)
    body = _S(outer, _ext(inner, "xy", z0 - 1, c["deck"]))
    add = []
    # insert columns (floor to deck): the rear-centre one a round boss on the rear wall, the corner ones blocks merged
    # into the wall corners with a R2.6 nose (STEP)
    add.append(_cyl(2.75, z0, c["deck"] + 0.1, INS[4], "z"))
    # every column foot flares to R3.7 (56 deg cone, prints deck-down without support) so the base-panel boss recess keeps a 1 mm wall
    for px, py in INS:
        add.append(_cyl(3.7, z0, 5.2, (px, py), "z"))
        add.append(_b().Solid.make_cone(3.7, 2.75, 1.4, _b().Plane(origin=(px, py, 5.2 - 0.001), z_dir=(0, 0, 1))))   # 56 deg: no overhang printed deck-down
    for sg in (1, -1):
        def mx(poly):
            return Polygon([(sg * u, v) for u, v in poly.exterior.coords]).buffer(0)
        def nose(x0, y0, dx, dy, r):   # the corner region at (x0, y0) outside an R r round (dx, dy: directions into the block)
            q = Polygon([(x0, y0), (x0 + dx * r, y0), (x0 + dx * r, y0 + dy * r), (x0, y0 + dy * r)])
            return q.difference(Point(x0 + dx * r, y0 + dy * r).buffer(r, 48))
        front_blk = Polygon([(22.25, 7.65), (27.6, 7.65), (27.6, 13.1), (22.25, 13.1)]).difference(nose(22.25, 7.65, 1, 1, 2.5))
        front_blk = front_blk.union(nose(22.25, 13.0, -1, -1, 0.8)).union(nose(27.5, 7.65, -1, -1, 0.8))      # R0.8 fillets into the walls
        rear_blk = Polygon([(22.21, -23.45), (27.6, -23.45), (27.6, -18.85), (22.21, -18.85)]).difference(nose(22.21, -18.85, 1, -1, 2.6))
        rear_blk = rear_blk.union(nose(22.21, -23.4, -1, 1, 0.9)).union(nose(27.5, -18.85, -1, 1, 0.9))
        add.append(_ext(mx(front_blk), "xy", z0, c["deck"] + 0.1))
        add.append(_ext(mx(rear_blk), "xy", z0, c["deck"] + 0.1))
        # motor front stop wall (load path: the N10 gearbox bears on it, not the base screws)
        add.append(_box(sg * 17.7, sg * (x - w + 0.1), -25.4, -23.4, z0, c["deck"] + 0.1))
        # N10 retention comb off the stop wall (deviation from the STEP, which leaves the motor to the hub and grub):
        # a key tab drops between the last two gearbox plates (|X| 23.4 / 26.3, 0.15 each side) so a hit or a drop
        # cannot walk the motor along its shaft, and a 0.4 mm ledge 0.1 over the gearbox plates stops it lifting off the
        # base-panel preload pad when inverted. Both hang from the deck (printed deck-down: no supports) and clear the
        # rounded can, so the motor still drops straight out downwards once the base panel is off.
        add.append(_box(sg * N10_KEY[0], sg * N10_KEY[1], -26.15, -23.4, 16.0, c["deck"] + 0.1))
        add.append(_box(sg * 20.0, sg * (x - w + 0.1), -27.3, -23.4, N10_TOP + 0.1, c["deck"] + 0.1))
        # side lobe with the thin M3 nut (Y -16.3..2.8)
        lobe = NUT_LOBE
        add.append(_ext(lobe, "yz", sg * (x - 0.1), sg * 32.5))
        R_ = 1.95   # root fillet where the lobe leaves the wall (STEP R1.95): one ruled loft, 12 bands of the quarter round
        add.append(_loft_yz_n([(lobe.buffer(R_ - math.sqrt(R_ * R_ - (R_ - h) ** 2), join_style=1), sg * (x - 0.1 + h))
                               for h in (R_ * k / 12 for k in range(13))]))
        # front tabs (key into the weapon-mount notches) and inner tab walls
        add.append(_ext(_poly([(18.5, 6.4), (19.5, 5.4), (25.5, 5.4), (26.5, 6.4), (26.5, 12.5), (25.5, 13.5), (19.5, 13.5), (18.5, 12.5)]), "yz", sg * 13.2, sg * 17.6))
        # inner tab wall, its top-front corner cut back on a R15.9 about the weapon axis: the drisk (swept R ~14.8 at the wall)
        # keeps >= 1 mm, so a bent tooth or a chassis flexed by a hit does not rub
        tabw = _poly([(13.0, 2.5), (25.5, 2.5), (26.5, 3.5), (26.5, 12.35), (25.59, 14.75), (15.0, 19.5), (13.0, 19.5)]).difference(Point(WY, WZ).buffer(WEAPON_CLEAR_R, 128))
        add.append(_ext(tabw, "yz", sg * 10.3, sg * 13.3))
        fil = Polygon([(8.3, 14.9), (10.4, 14.9), (10.4, 17.0), (8.3, 17.0)]).difference(Point(8.3, 17.0).buffer(2.0, 48))   # R2 into the front face
        add.append(_ext(Polygon([(sg * u, v) for u, v in fil.exterior.coords]).buffer(0), "xy", z0, c["deck"]))
        # switch pad under the deck (STEP): the switch ears bear on it
        if sg > 0:
            add.append(_ext(_round(Polygon([(22.0, -15.6), (27.5, -15.6), (27.5, 4.4), (22.0, 4.4)]), r_out=1.0), "xy", 16.5, c["deck"] + 0.1))
        # lugs carrying the standoffs (sloped top so they sit under the mount)
        lug = Polygon([(13.0, z0), (26.0, z0), (30.4, 1.0)] + _arc(SA, 4.5, 250, 300, 6) + [(36.6, 2.5)] + _arc(SB, 3.25, 250, 400, 24) + [(15.0, z1), (13.0, z1)])
        lug = _round(lug.convex_hull.difference(Polygon([(26.0, 0.0), (26.0, 2.5), (30.0, 1.0), (40.0, 0.9), (60, 0)])), r_in=0.0)
        add.append(_ext(lug, "yz", sg * 17.5, sg * 21.5))
    for sg in (1, -1):
        # front corner flanges (STEP): a bottom flange that blends from the side wall into the lug, and a top flange
        # that carries the deck chamfer forward to the lug
        blend = [(29.5, 15.0), (28.7, 16.0), (26.5, 18.5), (24.2, 21.0), (22.8, 22.8), (22.0, 24.6), (21.6, 26.3), (21.5, 27.5)]
        # front face of the corners at Y 15.6 with a R2.7 fillet into the lug, R1 outer corner (STEP)
        face = Polygon([(21.4, 13.0), (29.5, 13.0), (29.5, 14.6), (28.5, 15.6), (21.4, 15.6)]).union(
            Polygon([(21.4, 15.5), (24.2, 15.5), (24.2, 18.3), (21.4, 18.3)]).difference(Point(24.2, 18.3).buffer(2.7, 64)))
        add.append(_ext(Polygon([(sg * x_, y_) for x_, y_ in face.exterior.coords]).buffer(0), "xy", z0, 16.4))
        bot = Polygon([(21.5, 13.0), (29.5, 13.0)] + blend)
        add.append(_ext(Polygon([(sg * x_, y_) for x_, y_ in bot.exterior.coords]).buffer(0), "xy", z0, 5.0))
        # 2 x 2.6 gusset (52 deg) in the corner between the flange top and the lug face: printed deck-down the flange top is a
        # ceiling; the gusset narrows its unsupported span and stiffens the flange root
        gus = _ext(_poly([(sg * 21.45, 4.99), (sg * 23.5, 4.99), (sg * 21.45, 7.6)]), "xz", 13.0, 27.5)
        add.append(_I(gus, _ext(Polygon([(sg * x_, y_) for x_, y_ in bot.exterior.coords]).buffer(0), "xy", z0, 8.0)))
        topf = _ext(_poly([(13.0, 19.5), (15.3, 19.5), (23.0, 15.83), (23.0, 13.47), (15.3, 16.4), (13.0, 16.4)]), "yz", sg * 21.4, sg * 29.5)
        add.append(_I(topf, _ext(Polygon([(sg * x_, y_) for x_, y_ in Polygon([(21.4, 13.0), (29.5, 13.0)] + blend + [(21.4, 27.5)]).buffer(0).exterior.coords]).buffer(0), "xy", 10.0, 20.0)))
    body = _U(body, *add)
    cuts = []
    for sg in (1, -1):
        # lug underside: flat to Y 26, then the ramp; a scallop between the two standoffs (STEP)
        cuts.append(_ext(_poly([(10.0, -5.0), (10.0, 2.5), (26.0, 2.5), (30.4, 1.0), (30.4, -5.0)]), "yz", sg * 17.4, sg * 21.6))
        cuts.append(_ext(LUG_SCALLOP, "yz", sg * 17.4, sg * 21.6))   # lug underside rises along a big arc tangent to the flat at LUG_FLOOR_Z (fit to STEP RV01 sections at X 19.5)
        # under the nose standoff the lug follows its R3.25 arc (STEP): no hull chord below it where the scallop meets it
        under = Polygon([(LUG_SCALLOP_YT, 0.0), (40.5, 0.0), (40.5, LUG_FLOOR_Z), (LUG_SCALLOP_YT, LUG_FLOOR_Z)]).difference(Point(SB).buffer(LUG_SB_R, 96)).difference(LUG_BLEND_FILL)   # the cusp between the scallop circle and the standoff arc
        cuts.append(_ext(under, "yz", sg * 17.4, sg * 21.6))
        cuts.append(_box(sg * 13.3, sg * 17.5, 12.0, 15.1, z0 - 0.1, 4.5))   # front wall stops at the rabbet under the tab (STEP)
        # motor stop wall: lower inner edge rounded R4.5 (STEP)
        fil = Polygon([(17.6, 4.4), (22.2, 4.4), (22.2, 9.0), (17.6, 9.0)]).difference(Point(22.2, 9.0).buffer(4.5, 64))
        cuts.append(_ext(Polygon([(sg * x_, z_) for x_, z_ in fil.exterior.coords]).buffer(0), "xz", -25.5, -22.4))   # through the R0.9 corner fillet too: no 0.1 mm skin left under it
    # deck X-pocket lightening (from below, 1 mm skin stays)
    dz0, dz1 = c["deck"] - 0.5, c["deck"] + 1.0
    # deck pockets (STEP RV01 at Z 18): an X of 2 mm ribs, two diagonals at slope 0.64
    k_ = 0.6404
    tri = [Polygon([(0.0, -3.07), (-22.25, -3.07 + k_ * 22.25), (-22.25, 12.4), (22.25, 12.4), (22.25, -3.07 + k_ * 22.25)]),
           Polygon([(0.0, -8.13), (22.25, -8.13 - k_ * 22.25), (22.25, -23.4), (17.5, -23.4), (17.5, -23.6), (-17.5, -23.6), (-17.5, -23.4),
                    (-22.25, -23.4), (-22.25, -8.13 - k_ * 22.25)])]
    for t in tri:
        cuts.append(_ext(_round(t, r_out=0.8), "xy", dz0, dz1))
    for sg in (1, -1):   # side pockets: apex R2 towards the centre
        side = Polygon([(sg * 3.72, -5.59), (sg * 22.0, 4.51 + 0.640 * 2.49), (sg * 22.0, -15.71 - 0.6407 * 2.49)])   # right edge at |X| 22.0 (STEP 22.5): 1.0 mm rib to the 23.0 switch slot, not 0.5
        cuts.append(_ext(_round(side, r_out=1.9), "xy", dz0, dz1))
    for xa, xb in ((-26.5, -16.13), (-14.12, -3.75), (3.75, 14.12), (16.13, 26.5)):   # rear deck pockets
        cuts.append(_ext(_round(Polygon([(xa, -34.5), (xb, -34.5), (xb, -26.5), (xa, -26.5)]), r_out=0.6), "xy", dz0, dz1))
    cuts.append(_ext(_round(Polygon([(-2.75, -30.0), (2.75, -30.0), (2.75, -26.5), (-2.75, -26.5)]), r_out=1.2), "xy", dz0, dz1))
    bb = _b()
    for px, py in INS:
        # 3.0 hole floor to deck top, 0.6 chamfers both ends (STEP); the 3.5 M2 heat-set melts into its bottom
        cuts.append(_cyl(1.5, z0 - 1.0, (z1 + 1) if py == -33.6 else z1 - 4.0, (px, py), "z"))
        cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, 4.5 - 0.001), z_dir=(0, 0, 1))))
        if py == -33.6:
            cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, z1 + 0.001), z_dir=(0, 0, -1))))
        else:   # corner columns: a 1.7 thread-forming pilot in the top 4 mm for the top-panel screw (deviation: STEP 3.0 through),
            # under the STEP 0.6 top chamfer, which takes the tip of the M2 flat head that the 0.9 plate is too thin to hold
            cuts.append(_cyl(1.7, z1 - 4.0, z1 + 1, (px, py), "z"))   # 3.4 bore: the M2 heat-set (3.5 OD x 4) melts in flush with the column top
            cuts.append(bb.Solid.make_cone(2.1, 1.5, 0.6, bb.Plane(origin=(px, py, z1 + 0.001), z_dir=(0, 0, -1))))
    # switch slot in the deck beside the top panel, 2 M2 pilot holes
    sw_x0, sw_w, sw_y0, sw_l = 23.0, 4.0, -11.6, 12.0   # slot: inner edge 23.0 (top-panel edge), 4.0 wide and 12 long as measured on RV01
    cuts.append(_ext(_round(Polygon([(sw_x0, sw_y0), (sw_x0 + sw_w, sw_y0), (sw_x0 + sw_w, sw_y0 + sw_l), (sw_x0, sw_y0 + sw_l)]), r_out=0.45), "xy", 16.0, z1 + 1))
    for yy in (1.9, -13.1):
        cuts.append(_cyl(0.85, c["deck"] - 3, z1 + 1, (SWX, yy), "z"))
    for sg in (1, -1):
        # N10 keyhole: round seat for the gearbox shaft boss, narrowing to the floor (motor tilts in)
        kh = Point(RY, RZ).buffer(2.5, 64).union(Point(RY, 5.85).buffer(0.85, 24)).convex_hull   # STEP keyhole
        # opened into a U-slot to the floor (deviation): the gearbox boss (4 dia) and the shaft drop in from below with
        # the base panel off, instead of threading the shaft through a closed hole the motor cannot reach in a straight line
        kh = kh.union(Polygon([(RY - 2.05, z0 - 1.0), (RY + 2.05, z0 - 1.0), (RY + 2.05, RZ), (RY - 2.05, RZ)]))
        cuts.append(_ext(kh, "yz", sg * (x - w - 0.5), sg * (x + 0.5)))
        # nut: M3 clearance through lobe + wall, hex pocket on the inside
        cuts.append(_cyl(1.6, sg * 26.0, sg * 33.0, NUT))
        cuts.append(_box(sg * 29.0, sg * 34.0, -20.0, 6.0, z0 - 3.0, z0))   # the lobe root fillet must not hang below the floor plane
        # hex pocket 0.05 under the nut's 5.5 AF / 6.35 corners: the nut is pressed in and cannot shake loose into the bay
        hexp = Polygon([(NUT[0] + 3.12 * math.cos(math.radians(60 * i + 30)), NUT[1] + 3.13 * math.sin(math.radians(60 * i + 30))) for i in range(6)])
        cuts.append(_ext(hexp, "yz", sg * 27.0, sg * 29.5))
        cuts.append(_ext(_round(Polygon([(-7.14, 6.85), (-3.45, 7.05), (-3.45, 7.95), (-6.9, 8.9)]), r_out=0.25), "yz", sg * 29.0, sg * 33.0))
        # standoff holes in the lugs, square key hole
        cuts.append(_cyl(2.5, sg * 17.0, sg * 22.0, SA))
        cuts.append(_cyl(1.6, sg * 17.0, sg * 22.0, SB))
        cuts.append(_ext(_round(Polygon([(20.0, 6.9), (25.0, 6.9), (25.0, 12.0), (20.0, 12.0)]), r_out=0.9), "yz", sg * 10.0, sg * 22.0))
    # rear wall: 1 mm deep triangle lattice on the inner face (STEP)
    lat = []
    for sg in (1, -1):
        lat += [Polygon([(sg * 4.84, 7.0), (sg * 4.84, 15.0), (sg * 12.4, 11.0)]), Polygon([(sg * 26.42, 7.0), (sg * 26.42, 15.0), (sg * 18.85, 11.0)]),
                Polygon([(sg * 10.6, 5.58), (sg * 20.65, 5.58), (sg * 15.6, 9.7)]), Polygon([(sg * 10.6, 16.42), (sg * 20.65, 16.42), (sg * 15.6, 12.3)])]
    for t in lat:   # STEP rib is 0.35 thinner than the nominal triangle edges: grow each pocket by LAT_GROW
        cuts.append(_lattice_pocket(list(t.buffer(LAT_GROW, join_style=2).exterior.coords)[:-1]))
    # weapon phase wire hole in the front wall
    cuts.append(_ext(_round(Polygon([(7.25, 5.0), (10.25, 5.0), (10.25, 17.0), (7.25, 17.0)]), r_out=1.45), "xz", 12.0, 16.0))
    for xa, xb in ((-18.25, 4.25), (13.25, 18.2)):
        cuts.append(_wall_pocket(xa, xb, 6.55, 15.55, 12.0, 13.85))
    # rabbet for the base panel (recessed flush with the wall bottom lip) and the mating faces of the mounts and side
    # panels: the parts seat on the chassis, they do not share material with it
    pan = _panel_outline(0.05)
    cuts.append(_ext(pan, "xy", z0 - 1.0, 4.5))
    for px, py in INS:   # recess in each column foot for the base-panel ring boss
        cuts.append(_cyl(BOSS_R + 0.3, 4.4, 4.5 + BOSS_H + 0.05, (px, py), "z"))   # 0.25 base fillet round the boss
    for sg in (1, -1):
        cuts.append(_box(sg * 17.65, sg * 27.35, -35.15, -25.45, 4.4, 4.8))   # pad + 0.25 base fillet   # motor preload pads
        # square the R1 inner rear corner where the N10 gearbox plates sit (their corner would bite 0.14 into the round)
        cuts.append(_box(sg * 25.5, sg * (x - w + 0.05), y0 + w - 0.05, y0 + w + 2.0, z0 + 2.0, c["deck"]))
    # the STEP panel and lobe overlap (31 mm3) where the panel relief stops, at Y -11.7: the panel cuts the chassis, and the whole
    # overlapping slab of the lobe tail goes with it (rounded inside corner), so no 0.05 mm sliver of lobe is left beside the cut
    tail_y = NUT_RELIEF_Y0
    tail = Polygon([(PANEL_IN, tail_y - 12.0), (x + 4.0, tail_y - 12.0), (x + 4.0, tail_y), (PANEL_IN, tail_y)]).buffer(-NUT_STEP_R).buffer(NUT_STEP_R)
    tz0, tz1 = NUT_LOBE.bounds[1] - 2.0, NUT_LOBE.bounds[3] + 2.0
    cuts += [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)] + [
        _ext(Polygon([(sg * x_, y_) for x_, y_ in tail.exterior.coords]).buffer(0), "xy", tz0, tz1) for sg in (1, -1)]
    body = _S(body, *cuts)
    # electronics cage hung from the deck (up into the 1 mm deck skin through the lightening pockets; prints as part of the deck-down first layers): ribs 0.1 mm off the Malenki's
    # -x / +x / -y faces and the weapon ESC's -y face, so neither board hammers around when the robot is flipped
    (ex0, ex1), (ey0, ey1), ez0 = RX_X, RX_Y, RX_Z[0]
    G_ = 0.1
    ribs = [_box(ex0 - G_ - 1.28, ex0 - G_, -12.0, 8.0, ez0, c["deck"] + 1.1),          # -x, in the gap to the pack
            _box(ex1 + G_, ex1 + G_ + 1.2, -12.0, 8.0, ez0, c["deck"] + 1.1),           # +x
            _box(0.0, 14.6, ey0 - G_ - 1.0, ey0 - G_, WE_Z[0] + 0.9, c["deck"] + 1.1)]   # -y, down over the ESC's end
    return _U(body, *ribs)


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
