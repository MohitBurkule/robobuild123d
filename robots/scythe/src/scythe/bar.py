"""Weapon bar: laser-cut constant-thickness hardened steel, two teeth, 180 deg symmetric. UNTESTED.

Made as: one 2D profile (one arm built, the other is the same arm turned 180 deg), extruded BAR_T. Part frame: axis
on Z, underside at z = 0, arms along +/-X, spin CCW seen from above (+Z), so each tooth's cutting face is its +Y edge
on the +X arm (and -Y on the -X arm).
Adversarial intent: the leading-edge step bites wheels, forks and skirt hinges at 2 mm floor height, below where a
vertical spinner or wedge lip can reach it; the root is widest because bending moment from a tip hit peaks at the hub.
"""
import build123d as bd

from . import params as P
from ._reuse import plate


def arm_points():
    """+X arm outline (CCW): root at the hub, taper to the tip, bite step cut into the leading (+Y) edge."""
    r = P.bar_sweep_r()
    hr, ht = P.BAR_W_ROOT / 2, P.BAR_W_TIP / 2
    x_step = r - P.BAR_TOOTH_LEN
    y_lead = hr + (ht - hr) * x_step / r          # leading edge height at the step (on the taper line)
    return [(0.0, -hr), (r, -ht), (r, ht - P.BAR_TOOTH_STEP), (x_step, y_lead), (0.0, hr)]


def profile():
    arm = bd.Polygon(*arm_points(), align=None)
    face = (arm + bd.Rot(0, 0, 180) * arm).clean().faces()[0]
    face = plate.round_corners(face, r_out=P.BAR_CORNER_R)    # NOTE: also softens the tooth point; keep_ = tooth tips if too blunt
    bore = bd.Circle(P.SHAFT_D / 2 + P.BAR_BORE_CLR)
    bolts = plate.holes(P.BAR_BOLT_D / 2 + 0.1, P.BAR_BOLT_PCD / 2, P.BAR_BOLT_N, phase=0.0)   # on the bar centreline (16 mm root leaves 6.4 mm each side of a 3.2 hole)
    for h in [bore] + bolts:
        face = face - h
    return face


def bar():
    return bd.extrude(profile(), P.BAR_T)
