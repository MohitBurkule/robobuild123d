"""vert_mod: printed weapon module on the Alt chassis deck. A lattice frame screwed down through the four chassis
columns, a sloped hollow top shell rising to a rear bulkhead, two uprights (hull of their deck run and a boss round
the weapon axis: motor on the left, MF85 on the right) and two prongs that drop between the chassis tabs onto the
cross bolt. STEP frame."""
import math

from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.ops import unary_union

from robocad.geom import _box, _cyl, _U, _S, _ext, _mirror_x, _solid
from .chassis import halfspace
from .params_chassis import TAB_HOLE_DY, TAB_HOLE_Z, HOLE_D, HY
from .params_vert import *  # noqa: F401,F403


def _slope():
    """(y0, z0, dz/dy) of the shell's top surface: from the top of its front wall up to SHELL_TOP at the bulkhead."""
    return SHELL_Y[0], SHELL_FRONT, (SHELL_TOP - SHELL_FRONT) / (SHELL_Y[1] - SHELL_Y[0])


def shell_plan(off=0.0):
    w0, w1 = SHELL_W
    p = Polygon([(-w0, SHELL_Y[0]), (w0, SHELL_Y[0]), (w1, FRONT_FLARE_Y), (w1, SHELL_Y[1]), (-w1, SHELL_Y[1]), (-w1, FRONT_FLARE_Y)])
    return p.buffer(-off, join_style=2) if off else p


def _under_slope(solid, drop=0.0):
    y0, z0, k = _slope()
    n = (0.0, -k, 1.0)
    return _S(solid, halfspace((0, y0, z0 - drop * math.hypot(1, k)), n, 4 * (SHELL_Y[1] - SHELL_Y[0])))


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
    pads = [LineString([p, (p[0] / abs(p[0]) * SHELL_W[0 if p[1] < FRONT_FLARE_Y else 1], p[1])]).buffer(FRAME_LEG / 2) for p in POSTS]
    plate = unary_union([rim, *legs, *pads, *[Point(p).buffer(FRAME_LEG / 2) for p in POSTS]]).intersection(sbox(-IN_X, -IN_Y, IN_X, SHELL_Y[1]))
    f = _ext(plate, "xy", DECK_TOP, DECK_TOP + VM_T)
    return _S(f, *[_cyl(POST_HOLE_D / 2, DECK_TOP - 1, DECK_TOP + VM_T + 1, p, "z") for p in POSTS])


def upright_profile():
    """(y, z) outline of an upright: the hull of its run along the shell top, the bulkhead foot and the boss on the
    axis (it stands on the shell; nothing of it is under the shell top)."""
    run = [(SHELL_Y[0], SHELL_FRONT), (SHELL_Y[1], SHELL_TOP), (SHELL_Y[1], DECK_TOP)]
    return Polygon(run).union(Point(WY, WZ).buffer(BOSS_R)).convex_hull


def upright(sx):
    """Upright plate at |X| UP_IN .. UP_IN + UP_T on side sx, with the motor PCD (left) or the bearing seat (right)."""
    prof = upright_profile()
    win = prof.buffer(-UP_RIM).difference(Point(WY, WZ).buffer(BOSS_R)).difference(sbox(-1e3, 0, 1e3, SHELL_FRONT + VM_T))
    u = _ext(prof.difference(win.buffer(-UP_WIN_R).buffer(UP_WIN_R)), "yz", UP_IN, UP_IN + UP_T)
    if sx > 0:
        cut = _cyl(BRG_SEAT_R, UP_IN - 1, UP_IN + UP_T + 1, (WY, WZ), "x")
    else:
        cut = _U(_cyl(BRG_SEAT_R, UP_IN - 1, UP_IN + UP_T + 1, (WY, WZ), "x"),
                 *[_cyl(MOTOR_SCREW / 2 + 0.1, UP_IN - 1, UP_IN + UP_T + 1, (WY + MOTOR_PCD_R * math.cos(a), WZ + MOTOR_PCD_R * math.sin(a)), "x")
                   for a in [math.radians(45 + 90 * k) for k in range(4)]])
    u = _S(u, cut)
    return u if sx > 0 else _mirror_x(u)


def prongs():
    """Prongs from the deck down between the chassis tabs, on the cross-bolt line."""
    p = _box(*PRONG_X, *PRONG_Y, 0, DECK_TOP + VM_T)
    p = _S(p, _cyl(HOLE_D / 2, PRONG_X[0] - 1, PRONG_X[1] + 1, (HY + TAB_HOLE_DY, TAB_HOLE_Z), "x"))
    return _U(p, _mirror_x(p))


def vert_mod():
    return _solid(_U(frame(), shell(), upright(1), upright(-1), prongs()))
