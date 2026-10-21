"""[fix-B] Drisk: spider, floating Hardox discs, drisk spacer, GR1507 shaft.

[fix-B-rebuild] Every plate is one build123d sketch in the drisk frame (u, v about the spin axis, drawn on the spider's
own clocking DR_ROT), extruded over its stack span DR_X and placed on the weapon frame W_FRAME. Shared masters:
BOLT_R / N_STACK (the stack-bolt pattern every plate carries), HUB_R (the bell's screw circle), DISC_R, SHAFT_R."""
import math

import build123d as bd

from . import plate as pl
from .common import _m2
from .params_weapon import (BOLT_R, DISC_BAL_PTS, DISC_BORE_ROUND, DISC_ECC, DISC_ECC_A, DISC_HOLE_R_WIN, DISC_R,
                            DISC_ROUND, DOG, DR_ROT, DR_X, HALF_PITCH, HUB_R, N_STACK, SPACER, SPIDER, TOOTH_A,
                            TOOTH_BACK_A, TOOTH_BACK_R, TOOTH_HOOK, TOOTH_R, W_FRAME, WSHAFT)
from .params_chassis import WY, WZ


# ------------------------------------------------------------------------------------------------------- the frame
def _disc_local(u, v):
    """Drisk-local (u, v) -> world (Y, Z): the drisk_plane() basis about the axis, then onto the axis (WY, WZ)."""
    p = drisk_plane(0.0).from_local_coords((u, v))
    return (WY + p.Y, WZ + p.Z)


def drisk_plane(x):
    """Sketch plane of a drisk plate at axial X = x (weapon frame): u clocked DR_ROT about the axis, normal -X (the
    plates are drawn looking at the bell cap from outboard, as the STEP's Drisk_V4)."""
    a = math.radians(DR_ROT)
    return bd.Plane(origin=(x, 0, 0), x_dir=(0, -math.cos(a), math.sin(a)), z_dir=(-1, 0, 0))


def _plate(sketch, span):
    """Prism of a drisk sketch over its stack span (x0, x1) in the weapon frame, placed on W_FRAME (world)."""
    x0, x1 = span
    return pl.placed(bd.extrude(drisk_plane(x1) * sketch, amount=x1 - x0), W_FRAME)


def _at(r, deg):
    return bd.Vector(r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))


# ------------------------------------------------------------------------------------------------------------ discs
def disc_outline():
    """Single-tooth eccentric disc: rim DISC_R centred DISC_ECC off towards DISC_ECC_A so the rim mass balances the
    tooth. The tooth tip sits at (TOOTH_R, TOOTH_A); the leading flank runs in from the tip TOOTH_HOOK deg off the
    radial, the tip land runs back to the back-face top (TOOTH_BACK_R, TOOTH_BACK_A), and the back face drops to the
    rim tangent point (a smooth join). Tip land rounded DISC_ROUND r_out, flank root r_in."""
    ec = _at(DISC_ECC, DISC_ECC_A)
    tip, top = _at(TOOTH_R, TOOTH_A), _at(TOOTH_BACK_R, TOOTH_BACK_A)
    d = (top - ec).length                                           # back face: tangent from its top to the rim
    a = math.degrees(math.atan2(top.Y - ec.Y, top.X - ec.X) + math.acos(DISC_R / d))
    foot = ec + _at(DISC_R, a)
    root = tip + _at(TOOTH_R, TOOTH_A + 180 + TOOTH_HOOK)            # flank run in to the hub (inside the rim and the bore)
    rim = bd.Pos(ec.X, ec.Y) * bd.Circle(DISC_R)
    tooth = bd.Polygon(top, foot, root, tip, align=None)                 # counter-clockwise, as the rim
    return pl.round_corners(rim + tooth, **DISC_ROUND)


def _dog_bore():
    """Bore with N_STACK ramped drive dogs: base circle DOG r, a steep rise of DOG rise from t0 to t1 and a long ramp
    back down to t2 (deg after each dog's pitch start); every corner rounded DISC_BORE_ROUND."""
    d, edges = DOG, []
    for k in range(N_STACK):
        p = 2 * HALF_PITCH * k
        r1 = d["r"] + d["rise"]
        ramp = lambda t0, ra, t1, rb: bd.Edge.make_three_point_arc(_at(ra, p + t0), _at((ra + rb) / 2, p + (t0 + t1) / 2), _at(rb, p + t1))  # noqa: E731
        edges += [ramp(d["t0"], d["r"], d["t1"], r1), ramp(d["t1"], r1, d["t2"], d["r"]),
                  bd.Edge.make_three_point_arc(_at(d["r"], p + d["t2"]), _at(d["r"], p + (d["t2"] + d["t0"]) / 2 + HALF_PITCH), _at(d["r"], p + d["t0"] + 2 * HALF_PITCH))]
    return pl.round_corners(bd.Face(bd.Wire(edges)), r_out=DISC_BORE_ROUND, r_in=DISC_BORE_ROUND)


def floating_disc():
    """Disc sketch: outline minus the dog bore, the stack-bolt clearance holes and the balance window by the tooth."""
    # param: organic balance window: rounded triangle on three measured corners (STEP), corner radius DISC_HOLE_R_WIN
    win = bd.offset(bd.Polygon(*DISC_BAL_PTS, align=None), DISC_HOLE_R_WIN, kind=bd.Kind.ARC)
    # param: end
    return disc_outline() - _dog_bore() - pl.holes(_m2()[1], BOLT_R, N_STACK) - win


def disc(which):
    return _plate(floating_disc(), DR_X[which])


# ----------------------------------------------------------------------------------------------------------- spider
def _spider_window():
    """One quarter window, centred between two arms: hub ring (hub_r) to the lobe circles' inner edge (win_r), its
    sides an arm half-width off the arm axes, all four corners rounded win_round."""
    sp = SPIDER
    side = sp["win_r"] - sp["arm"]
    box = bd.Pos(sp["arm"] + side / 2, sp["arm"] + side / 2) * bd.Rectangle(side, side)
    q = (bd.Circle(sp["win_r"]) - bd.Circle(sp["hub_r"])) & box
    return pl.round_corners(q, r_out=sp["win_round"])


def spider():
    """3 mm aluminium spider on the GR1507 bell: disc with N_STACK lobes round the stack bolts (root filleted), the
    quarter windows, the shaft-collar bore, M2 clearance on the bell's HUB_R screw circle and M2 tap holes on BOLT_R
    (the stack screws thread in)."""
    sp = SPIDER
    tap_r, clr_r, _ = _m2()
    body = pl.round_corners(bd.Circle(sp["r"]) + pl.holes(sp["lobe_r"], BOLT_R, N_STACK), r_in=sp["round_in"])
    sk = body - pl.polar(_spider_window(), N_STACK) - bd.Circle(sp["bore_r"]) - pl.holes(clr_r, HUB_R, N_STACK) - pl.holes(tap_r, BOLT_R, N_STACK)
    return _plate(sk, DR_X["spider"])


# ----------------------------------------------------------------------------------------------------------- spacer
def drisk_spacer():
    """6 mm printed spacer between the discs: ring round the bell, a window midway between each pair of stack bolts."""
    sp = SPACER
    win = pl.ring_window(sp["win_in"], sp["win_out"], sp["half_deg"], sp["win_round"])
    sk = bd.Circle(sp["r"]) - bd.Circle(sp["bore_r"]) - pl.polar(win, N_STACK, sp["phase"]) - pl.holes(_m2()[1], BOLT_R, N_STACK)
    return _plate(sk, DR_X["spacer"])


# ------------------------------------------------------------------------------------------------------------ shaft
def weapon_shaft():
    """GR1507 5 mm shaft, revolved about the weapon axis: V-thread (pitch, depth, length from the free end) behind a
    lead-in chamfer, then plain to the circlip end."""
    w = WSHAFT
    p, r, dr = w["thread_pitch"], w["r"], w["thread_depth"]
    prof = [(0.0, 0.0), (0.0, r - dr - w["chamfer"]), (w["chamfer"], r - dr)]
    for k in range(int(round(w["thread_len"] / p))):
        x = w["chamfer"] + k * p
        prof += [(x + p / 2, r), (x + p, r - dr)]
    prof += [(w["thread_len"], r), (w["len"], r), (w["len"], 0.0)]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(w["x_end"] + x, 0, z) for x, z in prof], close=True))
    return pl.placed(bd.Solid.revolve(face, 360, bd.Axis.X), W_FRAME)
