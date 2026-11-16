"""Weapon bar: laser-cut constant-thickness hardened steel, two teeth, 180 deg symmetric.

Made as: one 2D profile (one arm built, the other is the same arm turned 180 deg), extruded BAR_T, then the
counterbores: the 2x M2.5 bar bolts are countersunk from the underside (nothing may protrude below the bar), the
centre bore pilots the bar on the motor's 3 mm shaft, and the lock hole at BAR_LOCK_X takes the pit pin that makes
the weapon safe. Part frame: axis on Z, underside at z = 0, arms along +/-X, spin CCW seen from above (+Z), so each
tooth's cutting face is its +Y edge on the +X arm (and -Y on the -X arm).

Adversarial intent: the leading-edge step bites wheels, forks and skirt hinges at ~5 mm floor height, below where a
vertical spinner or wedge lip can reach it; the root is widest because bending moment from a tip hit peaks at the hub.
"""
import math

import build123d as bd

from . import params as P
from ._reuse import plate
from robot.cad import fastener_catalog as fc


def arm_points():
    """+X arm outline (CCW): root at the hub, taper to the tip, bite step cut into the leading (+Y) edge."""
    r = P.bar_sweep_r()
    hr, ht = P.BAR_W_ROOT / 2, P.BAR_W_TIP / 2
    x_step = r - P.BAR_TOOTH_LEN
    y_lead = hr + (ht - hr) * x_step / r          # leading edge height at the step (on the taper line)
    return [(0.0, -hr), (r, -ht), (r, ht - P.BAR_TOOTH_STEP), (x_step, y_lead), (0.0, hr)]


def _csk(x, y, d):
    """Countersink cone + clearance hole cut from the underside (z = 0) of the bar."""
    dk, _k = fc.head(d, "csk")
    clr = fc.clearance(d) / 2
    depth = (dk - 2 * clr) / 2
    cone = bd.Pos(x, y, 0) * bd.Cone(dk / 2, clr, depth, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    hole = bd.Pos(x, y, 0) * bd.Cylinder(clr, P.BAR_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return cone + hole


def bolt_xy():
    """World-frame (x, y) of the 2x M2.5 bar bolts (on the centreline)."""
    return [(P.BAR_BOLT_PCD / 2 * (1 if i == 0 else -1), 0.0) for i in range(P.BAR_BOLT_N)]


def profile():
    arm = bd.Polygon(*arm_points(), align=None)
    face = (arm + bd.Rot(0, 0, 180) * arm).clean().faces()[0]
    face = plate.round_corners(face, r_out=P.BAR_CORNER_R)    # NOTE: also softens the tooth point; keep_ = tooth tips if too blunt
    face -= bd.Circle(P.SHAFT_D / 2 + P.BAR_BORE_CLR)
    face -= bd.Pos(P.BAR_LOCK_X, 0.0) * bd.Circle(P.BAR_LOCK_D / 2)
    return face


def bar():
    solid = bd.extrude(profile(), P.BAR_T)
    for x, y in bolt_xy():
        solid -= _csk(x, y, P.BAR_BOLT_D)
    return solid
