"""[fix-B] Drisk: spider, floating Hardox discs, drisk spacer, GR1507 shaft.

[fix-B-rebuild] Every plate is one build123d sketch in the drisk frame (u, v about the spin axis, drawn on the spider's
own clocking DR_ROT), extruded over its stack span DR_X and placed on the weapon frame W_FRAME. Shared masters:
BOLT_R / N_STACK (the stack-bolt pattern every plate carries), HUB_R (the bell's screw circle), DISC_R, SHAFT_R."""
import math

import build123d as bd

from . import plate as pl
from .common import _m2
from .params_weapon import (BIG, BOLT_R, DISC_BAL_PTS, DISC_BORE_ROUND, DISC_ECC, DISC_ECC_A, DISC_HOLE_R_WIN, DISC_R,
                            DISC_ROUND, DOG, DR_ROT, DR_X, HALF_PITCH, HUB_R, N_STACK, SPACER, SPIDER, STACK_CLR_R, STACK_TAP_R, TOOTH_A,
                            TOOTH_R, W_FRAME, WSHAFT)
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
    tooth. The tooth tip sits at (TOOTH_R, TOOTH_A); the leading flank runs radially in from the tip and the straight
    back face runs from the tip down to its rim tangent point (a smooth join). Tip DISC_ROUND r_out (sharp), flank
    root r_in."""
    ec = _at(DISC_ECC, DISC_ECC_A)
    tip = _at(TOOTH_R, TOOTH_A)
    d = (tip - ec).length                                           # back face: tangent from the tip to the rim
    a = math.degrees(math.atan2(tip.Y - ec.Y, tip.X - ec.X) + math.acos(DISC_R / d))
    foot = ec + _at(DISC_R, a)
    root = bd.Vector(0, 0)                                          # radial flank, run in to the axis (inside the rim and the bore)
    rim = bd.Pos(ec.X, ec.Y) * bd.Circle(DISC_R)
    tooth = bd.Polygon(tip, foot, root, align=None)                 # counter-clockwise, as the rim
    return pl.round_corners(rim + tooth, **DISC_ROUND)


def _dog_bore():
    """Bore with N_STACK ramped drive dogs: base circle DOG r; each dog a straight flank from the base at t0 up to the
    peak corner (r + rise, t1), then a convex ramp arc of radius ramp_r back down to the base at t2 (deg after the
    dog's pitch start). The peak corner is rounded into the dog's nose (nose_r), the two feet DISC_BORE_ROUND."""
    d, edges = DOG, []
    for k in range(N_STACK):
        p = 2 * HALF_PITCH * k
        foot, peak, end = _at(d["r"], p + d["t0"]), _at(d["r"] + d["rise"], p + d["t1"]), _at(d["r"], p + d["t2"])
        edges += [bd.Edge.make_line(foot, peak), bd.RadiusArc(peak, end, -d["ramp_r"]),
                  bd.Edge.make_three_point_arc(end, _at(d["r"], p + (d["t2"] + d["t0"]) / 2 + HALF_PITCH), _at(d["r"], p + d["t0"] + 2 * HALF_PITCH))]
    bore = pl.round_corners(bd.Face(bd.Wire(edges)), r_in=DISC_BORE_ROUND)
    return pl.round_corners(bore, r_out=d["nose_r"])


def floating_disc():
    """Disc sketch: outline minus the dog bore, the stack-bolt clearance holes and the balance window by the tooth."""
    # param: organic balance window: rounded triangle on three measured corners (STEP), corner radius DISC_HOLE_R_WIN
    win = bd.offset(bd.Polygon(*DISC_BAL_PTS, align=None), DISC_HOLE_R_WIN, kind=bd.Kind.ARC)
    # param: end
    return disc_outline() - _dog_bore() - pl.holes(STACK_CLR_R, BOLT_R, N_STACK) - win


def disc(which):
    return _plate(floating_disc(), DR_X[which])


# ----------------------------------------------------------------------------------------------------------- spider
def _quarter_window(r_in, r_out, arm, rnd):
    """One window, centred between two stack-bolt axes (0 and 2 HALF_PITCH): the ring r_in..r_out cut by sides
    parallel to, and `arm` off, the two bolt axes (a constant-width spoke along each bolt axis, for any N_STACK), all
    corners rounded rnd."""
    ccw_of_0 = bd.Pos(0, arm + BIG / 2) * bd.Rectangle(2 * BIG, BIG)                     # arm off bolt axis 0, towards the window
    cw_of_pitch = bd.Rot(0, 0, 2 * HALF_PITCH) * bd.Pos(0, -arm - BIG / 2) * bd.Rectangle(2 * BIG, BIG)   # arm off the next bolt axis
    return pl.round_corners((bd.Circle(r_out) - bd.Circle(r_in)) & ccw_of_0 & cw_of_pitch, r_out=rnd)


def spider_sketch():
    """3 mm aluminium spider on the GR1507 bell: disc with N_STACK lobes round the stack bolts (root filleted), the
    quarter windows, the shaft-collar bore, M2 clearance on the bell's HUB_R screw circle and M2 tap holes on BOLT_R
    (the stack screws thread in)."""
    sp = SPIDER
    clr_r = _m2()[1]                                                # bell screws (M2, motor catalog)
    body = pl.round_corners(bd.Circle(sp["r"]) + pl.holes(sp["lobe_r"], BOLT_R, N_STACK), r_in=sp["round_in"])
    return body - pl.polar(_quarter_window(sp["hub_r"], sp["win_r"], sp["arm"], sp["win_round"]), N_STACK) - bd.Circle(sp["bore_r"]) - pl.holes(clr_r, HUB_R, N_STACK) - pl.holes(STACK_TAP_R, BOLT_R, N_STACK)


def spider():
    return _plate(spider_sketch(), DR_X["spider"])


# ----------------------------------------------------------------------------------------------------------- spacer
def spacer_sketch():
    """6 mm printed spacer between the discs: ring round the bell, a window midway between each pair of stack bolts
    leaving a constant-width spoke (2 arm) along each bolt axis."""
    sp = SPACER
    win = _quarter_window(sp["win_in"], sp["win_out"], sp["arm"], sp["win_round"])
    return bd.Circle(sp["r"]) - bd.Circle(sp["bore_r"]) - pl.polar(win, N_STACK) - pl.holes(STACK_CLR_R, BOLT_R, N_STACK)


def drisk_spacer():
    return _plate(spacer_sketch(), DR_X["spacer"])


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
