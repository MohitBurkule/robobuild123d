"""vert_mod: printed weapon module on the Alt chassis deck. A lattice frame screwed down through the four chassis
columns, a sloped hollow top shell rising to a rear bulkhead, two uprights (hull of their deck run and a boss round
the weapon axis: motor on the left, MF85 on the right) and two prongs that drop between the chassis tabs onto the
cross bolt. STEP frame."""
import math

from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _ext, _mirror_x, _solid
from .chassis import halfspace
from .params_chassis import TAB_HOLE_DY, TAB_HOLE_Z, HOLE_D, HY, TAB_LEN, EDGE_CH, WIRE_SLOT_X, WIRE_SLOT_L, HEX, HEX_PHASE, M3
from .params_side import NUT_FIT
from robot.cad import fastener_catalog as fc
from .params_vert import *  # noqa: F401,F403


def _slope():
    """(y0, z0, dz/dy) of the shell's top surface: from the top of its front wall up to SHELL_TOP at the bulkhead."""
    return SHELL_Y[0], SHELL_FRONT, (SHELL_TOP - SHELL_FRONT) / (SHELL_Y[1] - SHELL_Y[0])


def shell_plan(off=0.0):
    w0, w1 = SHELL_W
    f0, f1 = FRONT_FLARE_Y
    p = Polygon([(-w0, SHELL_Y[0]), (w0, SHELL_Y[0]), (w0, f0), (w1, f1), (w1, SHELL_Y[1]), (-w1, SHELL_Y[1]), (-w1, f1), (-w0, f0)])
    return p.buffer(-off, join_style=2) if off else p


def _under_slope(solid, drop=0.0):
    y0, z0, k = _slope()
    n = (0.0, -k, 1.0)
    return _S(solid, halfspace((0, y0, z0 - drop * math.hypot(1, k)), n, BIG))


def shell():
    """Hollow sloped top shell: VM_T walls down to the deck, VM_T top, open underneath."""
    outer = _under_slope(_ext(shell_plan(), "xy", DECK_TOP, SHELL_TOP + VM_T))
    inner = _under_slope(_ext(shell_plan(VM_T), "xy", DECK_TOP - 1, SHELL_TOP), VM_T)
    return _S(outer, inner)


def frame():
    """Frame on the deck: a rim under the shell walls, legs from the shell's front corners to the front corners of
    the deck, and a pad round each of the four column screws (FRAME_LEG wide everywhere)."""
    w0 = SHELL_W[0]
    rim = shell_plan().difference(shell_plan(FRAME_LEG))
    legs = [LineString([(sx * w0, SHELL_Y[0]), (sx * (IN_X - FRAME_LEG / 2), -IN_Y + FRAME_LEG / 2)]).buffer(FRAME_LEG / 2) for sx in (-1, 1)]
    pads = [LineString([p, (p[0] / abs(p[0]) * SHELL_W[0], p[1])]).buffer(FRAME_LEG / 2) for p in POSTS]
    plate = unary_union([rim, *legs, *pads, *[Point(p).buffer(POST_PAD_R) for p in POSTS]]).intersection(sbox(-IN_X, -IN_Y, IN_X, SHELL_Y[1]))
    return _ext(plate, "xy", DECK_TOP, DECK_TOP + VM_T)


def upright_profile():
    """(y, z) outline of an upright: the hull of its run along the shell top, the bulkhead foot and the boss on the
    axis (it stands on the shell; nothing of it is under the shell top)."""
    run = [(SHELL_Y[0], SHELL_FRONT), (SHELL_Y[1], SHELL_TOP), (SHELL_Y[1], DECK_TOP)]
    hull = Polygon(run).union(Point(WY, WZ).buffer(BOSS_R)).convex_hull
    y0, z0, k = _slope()
    inside = Polygon([(y0, z0), (SHELL_Y[1] - VM_T, z0 + k * (SHELL_Y[1] - VM_T - y0)), (SHELL_Y[1] - VM_T, -BIG), (y0, -BIG)])
    hull = hull.difference(inside)                          # nothing of the upright inside the shell: it stands on the slope and the bulkhead
    rear = HY + TAB_LEN                                     # stand clear of the chassis: its deck top and the rear chamfer plane over the tabs
    chassis = Polygon([(-BIG, DECK_TOP), (HY - EDGE_CH, DECK_TOP), (rear, DECK_TOP - EDGE_CH - TAB_LEN), (rear, -BIG), (-BIG, -BIG)])
    return hull.difference(chassis)


def upright(sx):
    """Upright plate at |X| UP_IN .. UP_IN + UP_T on side sx, with the motor PCD (left) or the bearing seat (right)."""
    prof = upright_profile()
    win = prof.buffer(-UP_RIM).difference(Point(WY, WZ).buffer(BOSS_R)).difference(sbox(-BIG, 0, BIG, SHELL_FRONT + VM_T))
    web = _ext(prof.difference(win.buffer(-UP_WIN_R).buffer(UP_WIN_R)), "yz", UP_IN, UP_IN + UP_WEB)
    thick = Point(WY, WZ).buffer(BOSS_R if sx < 0 else BRG_SEAT_R + 2 * VM_T)   # motor side: the can pocket; bearing side: the MF85 seat
    if sx < 0:   # the motor side also wraps the lead slot
        thick = thick.union(sbox(LEAD_Y - MOTOR_CLR - VM_T, WZ - LEAD_W / 2 - VM_T, WY, WZ + LEAD_W / 2 + VM_T))
    u = _U(web, _ext(prof.intersection(thick), "yz", UP_IN, UP_IN + UP_T))   # full thickness only round the axis and the lead slot
    if sx > 0:
        cut = _cyl(BRG_SEAT_R, UP_IN - 1, UP_IN + UP_T + 1, (WY, WZ), "x")
    else:   # the can's base sinks MOTOR_SINK into the upright; its phase leads leave through a slot under it
        cut = _U(_cyl(MOTOR_R + MOTOR_CLR, UP_IN - 1, UP_IN + MOTOR_SINK, (WY, WZ), "x"),
                 _box(UP_IN - 1, UP_IN + MOTOR_SINK, LEAD_Y - MOTOR_CLR, WY, WZ - LEAD_W / 2, WZ + LEAD_W / 2))
    u = _S(u, cut)
    return u if sx > 0 else _mirror_x(u)


def duct():
    """Phase-lead duct: from the chassis deck wire slot (Cut-Extrude17) along the deck under the shell, out through the
    bulkhead to the forward-pointing lead stub in the left upright's pocket. Open at the bottom onto the deck; the
    walls hold the lead on both sides (wire.exterior_support). Returns (walls, passage)."""
    w, h = DUCT
    x1 = -UP_IN                                             # flush with the upright web's inner face (no sliver of web beside it)
    x0 = x1 - w                                             # over the deck wire slot, inside the shell side wall
    y0, yb, y1 = -WIRE_SLOT_L / 2, SHELL_Y[1] - VM_T, LEAD_Y
    z1 = WZ + LEAD_W / 2
    low = _box(x0 - VM_T, x1 + VM_T, y0 - VM_T, yb, DECK_TOP, DECK_TOP + h + VM_T)   # under the shell, inside its side wall
    rise = _box(x0 - VM_T, x1 + VM_T, yb, y1, DECK_TOP, z1 + VM_T)                  # bulkhead to the lead stub: closed round
    hole = _U(_box(x0, x1, y0, yb + 1, 0, DECK_TOP + h), _box(x0, x1, yb - 1, y1 + 1, 0, z1))   # open below: the deck / nothing
    return _U(low, rise), hole


def prongs():
    """Prongs from the deck down between the chassis tabs, on the cross-bolt line."""
    p = _U(_box(*PRONG_X, *PRONG_Y, 0, DECK_TOP + VM_T),
           _box(UP_IN, PRONG_X[1], *PRONG_Y, DECK_TOP, DECK_TOP + VM_T))   # bridge to the upright web, above the chassis rear chamfer
    y, z = HY + TAB_HOLE_DY, TAB_HOLE_Z
    af, m = fc.nut(M3, "thin")
    r = (af + NUT_FIT) / math.sqrt(3)
    nut = _ext(Polygon([(y + r * math.cos(math.radians(a)), z + r * math.sin(math.radians(a))) for a in range(HEX_PHASE, 360, 360 // HEX)])
               .union(sbox(y - (af + NUT_FIT) / 2, -1, y + (af + NUT_FIT) / 2, z)), "yz", PRONG_X[0] - 1, PRONG_X[0] + m)   # cross-bolt nut, dropped in from below
    p = _S(p, _cyl(HOLE_D / 2, PRONG_X[0] - 1, PRONG_X[1] + 1, (y, z), "x"), nut)
    return _U(p, _mirror_x(p))


def vert_mod():
    from .fasteners import cutters
    d_out, d_in = duct()
    return _solid(_S(_U(frame(), shell(), upright(1), upright(-1), prongs(), d_out), d_in, cutters("vert_mod")))
