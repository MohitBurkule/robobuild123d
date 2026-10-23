"""ELVRN3.0 Alt chassis: printed open-bottom block, deck on top, N10 / standoff keyholes in the side walls, side bosses
with captive M3 nuts, 4 + 2 screw columns, rear cross-bolt tabs for the vertical module.

Built in the dump's order (Boss-Extrude1 block -> edge breaks -> Cut-Extrude1 cavity -> rebate -> keyholes -> side boss ->
deck slots -> lattice -> rear tabs). Every size is a params_chassis relation; the left side is the mirror of the right.
"""
import math

import build123d as bd
from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _I, _mirror_x, _ext, _solid
from .params_chassis import *  # noqa: F401,F403


def _both(s):
    """A right-hand feature and its mirror about the YZ plane (dump MirrorPattern)."""
    return None if s is None else _U(s, _mirror_x(s))


def block():
    """Boss-Extrude1 with the rear tabs (Boss-Extrude3, LPattern1, Mirror7): the outer envelope before any cut."""
    tabs = [_box(TAB_X_OUT - k * TAB_PITCH - TAB_W, TAB_X_OUT - k * TAB_PITCH, HY, HY + TAB_LEN, 0, CH_H) for k in range(TAB_N)]
    x0, x1 = TAB_X_OUT - (TAB_N - 1) * TAB_PITCH - TAB_W, TAB_X_OUT - (TAB_N - 1) * TAB_PITCH   # inner tab: round end round the bolt hole
    end = _I(_cyl(TAB_END_R, x0, x1, (HY + TAB_HOLE_DY, TAB_HOLE_Z), "x"), _box(x0, x1, HY, HY + TAB_LEN + TAB_END_R, 0, CH_H))
    return _U(_box(-HX, HX, -HY, HY, 0, CH_H), *[_both(t) for t in tabs], _both(end))


def halfspace(point, normal, size):
    """Everything on the +normal side of the plane through `point` (a cube `size` wide standing on the plane)."""
    pl = bd.Plane(origin=point, z_dir=normal)
    return bd.Solid.make_box(size, size, size).moved(bd.Location(pl) * bd.Location((-size / 2, -size / 2, 0)))


def edge_breaks():
    """Chamfer1: C2 x 45 deg on the top outer edges; the rear plane runs on over the tabs (Chamfer3). Fillet1 rounds
    the front vertical corners. Returned as the material to remove."""
    size = 2 * (CH_L + TAB_LEN)
    cut = [halfspace((n[0] * (HX - EDGE_CH), n[1] * (HY - EDGE_CH), CH_H), (n[0], n[1], 1), size)
           for n in ((1, 0), (-1, 0), (0, -1), (0, 1))]
    corner = []
    for sx in (-1, 1):
        cx, cy = sx * (HX - CORNER_R), -(HY - CORNER_R)
        corner.append(_S(_box(cx, cx + sx * CORNER_R, cy, cy - CORNER_R, 0, CH_H), _cyl(CORNER_R, 0, CH_H, (cx, cy), "z")))
    return _U(*cut, *corner)


def cavity():
    """Cut-Extrude1: the open-bottom pocket inside 2 mm walls up to the deck, leaving the screw columns and the
    motor-bay cross walls; Cut-Extrude2: the base-panel rebate."""
    keep = [_cyl(COL_R, 0, DECK_Z, p, "z") for p in POSTS + END_POSTS]
    px, py = POST_PITCH[0] / 2, POST_PITCH[1] / 2
    web = IN_X - px                                         # Sketch2 D10/D11: column centre 2.5 in from the side wall
    for sy, x0, rf in ((1, BAY_X0[0], BAY_FILLET[0]), (-1, BAY_X0[1], BAY_FILLET[1])):
        y0 = sy * (IN_Y - BAY_LEN)
        wall_ = _box(x0, IN_X, y0, y0 - sy * WALL, 0, DECK_Z)                        # cross wall closing each axle bay,
        corner = _S(_box(x0 - 1, x0 + BAY_END_R, *sorted((y0 + sy, y0 - sy * (WALL + 1))), -1, WALL + BAY_END_R),
                    _cyl(BAY_END_R, *sorted((y0 + sy, y0 - sy * (WALL + 1))), (x0 + BAY_END_R, WALL + BAY_END_R), "y"))
        keep.append(_both(_S(wall_, corner)))                                         # its free end rounded into its foot over the rebate
        keep.append(_both(fillet_filler((px, sy * py), COL_R, "y", y0 - sy * WALL, rf, -1)))   # Fillet15 / Fillet3: column into the bay wall face
        keep.append(_both(fillet_filler((px, sy * py), COL_R, "x", IN_X - BOSS_IN, PAD_FILLET, -sy)))   # Fillet2: column into the boss pad
    keep += [_both(_box(px, IN_X, sy * py - COL_R, sy * py + COL_R, 0, DECK_Z)) for sy in (-1, 1)]   # each column joined to the side wall
    keep.append(_both(_box(IN_X - BOSS_IN, IN_X, -(py - COL_R), py - COL_R, WALL, DECK_Z)))   # inner boss pad, column to column
    for sy in (-1, 1):                                      # Fillet9 R2: the end columns blend into the end walls
        ey = sy * END_POST_Y
        xc = math.sqrt((COL_R + END_FILLET) ** 2 - (IN_Y - END_FILLET - END_POST_Y) ** 2)
        fill = _box(-xc, xc, ey, sy * IN_Y, 0, DECK_Z)
        keep.append(_S(fill, *[_cyl(END_FILLET, -1, DECK_Z + 1, (sx * xc, sy * (IN_Y - END_FILLET)), "z") for sx in (-1, 1)]))
    pocket = _S(_box(-IN_X, IN_X, -IN_Y, IN_Y, -1, DECK_Z), *keep)
    rebate = _box(-(HX - REBATE), HX - REBATE, -(HY - REBATE), HY - REBATE, -1, WALL)
    for sx in (-1, 1):   # front corners concentric with Fillet1 (STEP: the lip stays a wall thick round the corner)
        cx, cy = sx * (HX - CORNER_R), -(HY - CORNER_R)
        rebate = _S(rebate, _S(_box(cx, cx + sx * CORNER_R, cy, cy - CORNER_R, -1, WALL), _cyl(CORNER_R - REBATE, -1, WALL, (cx, cy), "z")))
    return _U(pocket, rebate)


def fillet_filler(c, rc, axis, at, r, side):
    """Material of a concave round of radius r between a column (centre c, radius rc, along Z) and a wall plane
    (`axis` = at). side picks which of the two tangent rounds (-1: toward lower x / y on the free axis)."""
    gap = abs(at - c[1 if axis == "y" else 0]) - r
    if gap >= rc + r:                                       # the wall is out of reach of the column: no round
        return None
    if axis == "y":
        dy = at - c[1]
        dx = side * math.sqrt((rc + r) ** 2 - (abs(dy) - r) ** 2)
        f = (c[0] + dx, at - math.copysign(r, dy))
    else:
        dx = at - c[0]
        dy = side * math.sqrt((rc + r) ** 2 - (abs(dx) - r) ** 2)
        f = (at - math.copysign(r, dx), c[1] + dy)
    k = rc / (rc + r)
    tc = (c[0] + (f[0] - c[0]) * k, c[1] + (f[1] - c[1]) * k)              # tangent point on the column
    tw, q = ((f[0], at), (c[0], at)) if axis == "y" else ((at, f[1]), (at, c[1]))   # tangent point on the wall, wall foot of the column axis
    return _S(_ext(Polygon([c, tc, tw, q]).buffer(0), "xy", 0, DECK_Z), _cyl(r, -1, DECK_Z + 1, f, "z"))   # an exact round: no facet slivers


def keyholes():
    """Cut-Extrude3: a bore on each axle line through both side walls with a slot dropping KEY_DROP below it."""
    out = []
    for y in (-AXLE_Y, AXLE_Y):
        bore = _cyl(KEY_R, IN_X - 1, HX + 1, (y, AXLE_Z), "x")
        slot = _U(_box(IN_X - 1, HX + 1, y - KEY_SLOT_R, y + KEY_SLOT_R, AXLE_Z - KEY_DROP, AXLE_Z),
                  _cyl(KEY_SLOT_R, IN_X - 1, HX + 1, (y, AXLE_Z - KEY_DROP), "x"))
        out.append(_both(_U(bore, slot)))
    return _U(*out)


def side_boss():
    """Boss-Extrude2 (+ Mirror3): R5 obround pad on the outer wall face round the two side-panel screws."""
    ys = (-BOSS_PITCH / 2, BOSS_PITCH / 2)
    pad = _obround(HX - 1, HX + BOSS_OUT)
    body = _U(_S(_box(HX - 2 * BOSS_FILLET, HX, -HY, HY, 0, CH_H), edge_breaks()), pad)   # a wall deep enough to carry the round, its top edge broken
    reach = BOSS_PITCH / 2 + BOSS_R
    on_wall = lambda c: abs(c.X - HX) < GEOM_TOL or abs(c.X + c.Z - (HX - EDGE_CH + CH_H)) < GEOM_TOL   # the wall face or the Chamfer1 plane
    root = [e for e in body.edges() if on_wall(e.center()) and abs(e.center().Y) <= reach and abs(e.center().Z - AXLE_Z) <= BOSS_R + GEOM_TOL
            and e.center().X > HX - GEOM_TOL - EDGE_CH]
    out = _S(body.fillet(BOSS_FILLET - OCC_EPS, root), _box(HX - 3 * BOSS_FILLET, HX, -CH_L, CH_L, -1, CH_H + 1))   # Fillet5: R3 root round
    pad = _U(out, _box(HX - 1, HX, -BOSS_PITCH / 2, BOSS_PITCH / 2, AXLE_Z - BOSS_R, AXLE_Z + BOSS_R))   # plus a stub keying it into the wall
    return _both(pad)


def side_boss_core():
    """The obround pad itself: Boss-Extrude2 comes after Chamfer1, so the edge break does not touch it."""
    ys = (-BOSS_PITCH / 2, BOSS_PITCH / 2)
    return _both(_obround(HX - 1, HX + BOSS_OUT))


def _obround(x0, x1):
    """R5 obround round the two side-panel screws, one exact-arc prism (no tangent strips between a box and two cylinders)."""
    from shapely.geometry import LineString
    return _ext(LineString([(-BOSS_PITCH / 2, AXLE_Z), (BOSS_PITCH / 2, AXLE_Z)]).buffer(BOSS_R, quad_segs=64), "yz", x0, x1, arcs=True)


def side_boss_cuts():
    """Cut-Extrude4 (3.2 screw holes), Cut-Extrude5 (hex nut pockets from the inside), Cut-Extrude15 (window)."""
    ys = (-BOSS_PITCH / 2, BOSS_PITCH / 2)
    holes = [_cyl(HOLE_D / 2, IN_X - BOSS_IN - 1, HX + BOSS_OUT + 1, (y, AXLE_Z), "x") for y in ys]
    r_hex = NUT_AF / math.sqrt(3)
    nuts = [bd.Solid.extrude(bd.Face(bd.Wire.make_polygon([(0, y + r_hex * math.cos(math.radians(a)), AXLE_Z + r_hex * math.sin(math.radians(a))) for a in range(HEX_PHASE, 360, 360 // HEX)], close=True)),
                             bd.Vector(NUT_DEPTH, 0, 0)).moved(bd.Location((IN_X - BOSS_IN, 0, 0))) for y in ys]
    x0 = HX + BOSS_OUT - WIN_DEPTH
    win = _box(x0, HX + BOSS_OUT + 1, -WIN_W / 2, WIN_W / 2, AXLE_Z - WIN_H / 2, AXLE_Z + WIN_H / 2)
    win = win.fillet(WIN_R, [e for e in win.edges() if e.center().X < HX + BOSS_OUT and abs(e.tangent_at().X) > COS_ALONG])   # Fillet12 R1: corners,
    win = win.fillet(WIN_R * WIN_FLOOR_K, [e for e in win.edges() if abs(e.center().X - x0) < GEOM_TOL])   # then the floor (torus blends: no sphere poles to tessellate)
    lead = [bd.extrude(bd.Face(_hex_wire(IN_X - BOSS_IN, y, NUT_AF + 2 * NUT_CH)), amount=NUT_CH, dir=(1, 0, 0), taper=LEAD_TAPER) for y in ys]   # Chamfer3 0.4 nut lead-in (planar flanks)
    return _both(_U(*holes, *nuts, *lead, win))


def _hex_wire(x, y, af):
    r = af / math.sqrt(3)
    return bd.Wire.make_polygon([(x, y + r * math.cos(math.radians(a)), AXLE_Z + r * math.sin(math.radians(a))) for a in range(HEX_PHASE, 360, 360 // HEX)], close=True)


def column_holes():
    """Tapping holes down every screw column, through the deck, with the 0.6 lead-in at the rebate floor."""
    out = []
    for p in POSTS + END_POSTS:
        out.append(_cyl(TAP_D / 2, -1, CH_H + 1, p, "z"))
        out.append(bd.Solid.make_cone(TAP_D / 2 + LEAD_CH, TAP_D / 2, LEAD_CH, bd.Plane(origin=(p[0], p[1], WALL), z_dir=(0, 0, 1))))
        out.append(bd.Solid.make_cone(TAP_D / 2 + LEAD_CH, TAP_D / 2, LEAD_CH, bd.Plane(origin=(p[0], p[1], CH_H), z_dir=(0, 0, -1))))   # Chamfer4 at the deck top
    return _U(*out)


def deck_cuts():
    """Cut-Extrude6 switch slot + its two pilots, Cut-Extrude17 wire slot."""
    sx0 = IN_X - SW_SLOT_IN
    sw = _box(sx0 - SW_SLOT[0], sx0, -SW_SLOT[1] / 2, SW_SLOT[1] / 2, DECK_Z - 1, CH_H + 1)
    pil = [_cyl(SW_PILOT_D / 2, DECK_Z - 1, CH_H + 1, (sx0 - SW_SLOT[0] / 2, s * SW_PITCH / 2), "z") for s in (-1, 1)]
    half = WIRE_SLOT_L / 2                                  # Sketch21 D2: the straight run; R1.5 ends beyond it
    wire = _U(_box(WIRE_SLOT_X - WIRE_SLOT_R, WIRE_SLOT_X + WIRE_SLOT_R, -half, half, DECK_Z - 1, CH_H + 1),
              *[_cyl(WIRE_SLOT_R, DECK_Z - 1, CH_H + 1, (WIRE_SLOT_X, s * half), "z") for s in (-1, 1)])
    return _U(sw, *pil, wire)


def lattice_profile():
    """2D windows of the deck lattice (Sketch9/18/20). The ribs run column to column: the two diagonals of the column
    grid, the column rows and the lines from each corner column to the end column. Centre cells (between the diagonals)
    are shrunk LAT_RIB_C (one column radius); end cells LAT_RIB_E; corners rounded LAT_R."""
    a, b = POST_PITCH[0] / 2, POST_PITCH[1] / 2
    e = END_POST_Y
    win = []
    for sy in (-1, 1):   # top / bottom centre triangles and the end triangles
        win.append(_rounded(Polygon([(0, 0), (a, sy * b), (-a, sy * b)]).buffer(-LAT_RIB_C, join_style=2), LAT_R_C))
        end = Polygon([(-a, sy * b), (a, sy * b), (0, sy * e)]).buffer(-LAT_RIB_E, join_style=2)
        win.append(end.intersection(sbox(-LAT_END_X, -CH_L, LAT_END_X, CH_L)))
        xl = LAT_CORNER_X[0 if sy > 0 else 1]
        for sx in (-1, 1):   # corner pockets between the end wall, a rib to the end column and the bay wall
            if sy > 0:       # rear: the rib is the column-to-end-column line
                rib, half = ((sx * a, sy * b), (0, sy * e)), LAT_RIB_E
            else:            # front: the rib runs from the axle-bay wall corner to the end column
                rib, half = ((sx * BAY_X0[1], sy * (IN_Y - BAY_LEN)), (0, sy * e)), LAT_RIB_F
            cell = Polygon([(0, sy * e), rib[0], (sx * a, sy * b), (sx * a, sy * IN_Y), (0, sy * IN_Y)]).buffer(0)
            cell = cell.difference(LineString(rib).buffer(half))
            cell = cell.difference(Point(0, sy * e).buffer(COL_R))
            win.append(cell.intersection(sbox(-xl, -IN_Y, xl, IN_Y)))
    for sx in (-1, 1):   # left / right centre triangles
        win.append(_rounded(Polygon([(0, 0), (sx * a, b), (sx * a, -b)]).buffer(-LAT_RIB_C, join_style=2), LAT_R_C))
    return unary_union([_rounded(x, LAT_R) for x in win if not x.is_empty])


def _rounded(p, r):
    """Shapely polygon with every convex corner rounded r (the windows' 2D fillets)."""
    return p.buffer(-r).buffer(r)


def lattice():
    """Cut-Extrude7/14/16: the windows pocketed LAT_DEPTH up into the deck underside."""
    w = lattice_profile()
    polys = list(w.geoms) if hasattr(w, "geoms") else [w]
    out = [_ext(p, "xy", DECK_Z - BOOL_EPS, DECK_Z + LAT_DEPTH, arcs=True) for p in polys if p.area > 1]   # from the deck underside: the columns and walls under it stay whole
    return _U(*out)


def tab_holes():
    """Boss-Extrude3 hole (Sketch11 D4 3.2) on the cross-bolt line through all four tabs, Chamfer5 on the outer ends."""
    y = HY + TAB_HOLE_DY
    x_in = TAB_X_OUT - (TAB_N - 1) * TAB_PITCH - TAB_W   # inner face of the inner tab: the bolt head / nut side
    leads = [bd.Solid.make_cone(HOLE_D / 2 + TAB_LEAD, HOLE_D / 2, TAB_LEAD, bd.Plane(origin=(sx * x_in, y, TAB_HOLE_Z), z_dir=(sx, 0, 0))) for sx in (-1, 1)]
    return _U(_cyl(HOLE_D / 2, -HX - 1, HX + 1, (y, TAB_HOLE_Z), "x"), *leads)


def chassis():
    """The Alt chassis in its part frame (= the STEP frame)."""
    above_pad = _box(-CH_W, CH_W, -CH_L, CH_L, AXLE_Z + BOSS_R + BOOL_EPS, 2 * CH_H)   # Boss-Extrude2 follows Chamfer1: the chamfer trims the root round, not the pad
    s = _U(_S(block(), edge_breaks()), _S(side_boss(), _I(edge_breaks(), above_pad)))
    s = _S(s, cavity(), keyholes())
    s = _S(s, side_boss_cuts(), column_holes(), deck_cuts(), lattice(), tab_holes())
    s = _solid(s)
    end = HY + TAB_LEN                                      # Fillet R2 where the outer tabs' end face meets the rear chamfer plane
    E = [e for e in s.edges() if e.geom_type.name == "LINE" and abs(e.center().Y - end) < GEOM_TOL and abs(e.tangent_at().X) > COS_ALONG
         and abs(e.center().X) > TAB_X_OUT - TAB_W and e.center().Z > GEOM_TOL]
    return s.fillet(TAB_TIP_R, E)
