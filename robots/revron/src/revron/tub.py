"""[fix-S] Chassis tub and its panels: chassis, base_panel, top_panel, esc_tray, inserts / panel seats."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from . import tub_shell, tub_lobes, tub_lugs, tub_front
from .tub_util import rect

SW_PAD = dict(x=(22.5, 27.5), y=(-15.6, 4.4), r=1.5, z0=16.5, fillet=1.5, over=0.5, up=0.1)   # switch pad under the deck (STEP): X / Y span (the +X end is the wall), free corner R, bottom Z, wall fillet R, reach into the wall, reach up into the deck


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
    skin_top = z0 + t
    px, py = PRELOAD_PAD["c"]
    for s in (1, -1):   # plain boxes (not shapely polylines) so the base can take a fillet
        pad = b.Pos(s * px, py, skin_top - PRELOAD_PAD["sink"] + PRELOAD_PAD["h"] / 2) * b.Box(PRELOAD_PAD["s"], PRELOAD_PAD["s"], PRELOAD_PAD["h"])
        body = body + b.fillet(pad.edges().filter_by(b.Axis.Z), PRELOAD_PAD["r"])
    # the 1 mm skin is thinner than the 1.2 mm M2 flat head: a ring boss over each screw gives the seat material (no knife edge
    # under the head) and keys the panel into the column feet, so side hits shear the bosses, not the screws
    for x, y in INS:
        body = body + b.Pos(x, y, skin_top - PRELOAD_PAD["sink"] + (BOSS_H + PRELOAD_PAD["sink"]) / 2) * b.Cylinder(BOSS_R, BOSS_H + PRELOAD_PAD["sink"])
    # small fillet where pads and bosses meet the skin: no sharp internal corner in the print (the STEP has r 0.5 at the pads)
    def _base_edge(e):
        if abs(e.center().Z - skin_top) > BASE_EDGE_TOL or abs(e.bounding_box().max.Z - e.bounding_box().min.Z) > FLAT_TOL:
            return False
        fs = [f for f in body.faces() if any(e.is_same(x) for x in f.edges())]
        return len(fs) == 2 and any(f.bounding_box().max.Z > skin_top + BASE_EDGE_UP and f.bounding_box().min.Z < skin_top + BASE_EDGE_TOL / 2 for f in fs)
    body = b.fillet([e for e in body.edges() if _base_edge(e)], BASE_FILLET)
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
def switch_pad(c):
    """Pad under the deck that the switch ears bear on (STEP); +X side only."""
    from shapely.geometry import Point
    P = SW_PAD
    (x0, x1), (y0, y1), f = P["x"], P["y"], P["fillet"]
    plan = _round(rect(x0, x1 + P["over"], y0, y1), r_out=P["r"])
    for yw, d in ((y0, -1), (y1, 1)):   # concave fillet where the pad ends meet the side wall
        q = rect(x1 - f, x1, *sorted((yw, yw + d * f)))
        plan = plan.union(q.difference(Point(x1 - f, yw + d * f).buffer(f, SEG)))
    return _ext(plan, "xy", P["z0"], c["deck"] + P["up"])


def chassis():
    """RV01 printed chassis: a closed-top box printed deck-down, open underneath for the base panel. Composed from the
    per-feature modules: shell (box, columns, deck pockets, base seat), lobes (side lobes with the captive M3 nut),
    lugs (front tabs and standoff lugs), front (corner flanges, rear lattice, wire hole, wall pockets)."""
    c = CH
    adds = tub_shell.additions(c) + tub_lobes.additions(c) + tub_lugs.additions(c) + tub_front.additions(c) + [switch_pad(c)]
    cuts = tub_shell.cuts(c) + tub_lobes.cuts(c) + tub_lugs.cuts(c) + tub_front.cuts(c)
    return _U(_S(_U(tub_shell.shell(c), *adds), *cuts), *tub_shell.ribs(c))


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
