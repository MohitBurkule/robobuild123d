"""Ripsaw disc: laser/waterjet-cut constant-thickness hardox sheet, single tooth, balance by an enlarged window.
Own frame: spin axis = +Z (sheet plane XY, thickness 0..DISC_T), tooth face on +X.

Adversarial intent: the tooth face is a radial line (full section behind it) so a hit loads the rim in compression;
windows stop RIM short of the rim so a cracked spoke leaves the rim ring intact. The tooth root carries a fillet
(laser kerf floor) and the balance window keeps HUB_LAND of web round the bolt circle."""
import math

import build123d as bd

from . import params as P
from ._reuse import plate


def _p(r, deg):
    a = math.radians(deg)
    return bd.Vector(r * math.cos(a), r * math.sin(a))


def outline():
    """Rim arc from the tooth tip round to the ramp start, spiral ramp down TOOTH_STEP, radial tooth face back up.
    The root corner (ramp meets tooth face) is filleted TOOTH_ROOT_R: a sharp internal corner is a laser-cut no."""
    R, S = P.DISC_R, P.TOOTH_STEP
    tip, ramp0 = _p(R, 0.0), _p(R, -P.RAMP_DEG)
    root = _p(R - S, 0.0)
    fil0 = _p(R - S + P.TOOTH_ROOT_R, 0.0)                       # fillet start on the tooth face
    a1 = -2.0                                                   # fillet end on the ramp (deg): the ramp point there
    fil1 = _p(R - S * (a1 + P.RAMP_DEG) / P.RAMP_DEG, a1)
    arc = bd.Edge.make_three_point_arc(tip, _p(R, (360.0 - P.RAMP_DEG) / 2), ramp0)
    n = 8
    ramp = bd.Edge.make_spline([ramp0] + [_p(R - S * k / n, -P.RAMP_DEG * (1 - k / n)) for k in range(1, n)] + [fil1])
    fillet = bd.Edge.make_three_point_arc(fil1, _p(R - S + P.TOOTH_ROOT_R * 0.45, -0.8), fil0)
    face_line = bd.Edge.make_line(fil0, tip)
    return bd.Face(bd.Wire([arc, ramp, fillet, face_line]))


def disc():
    f = outline()
    cuts = [bd.Circle(P.DISC_BORE / 2)]
    cuts += [bd.Pos(*_p(r, a)) * bd.Circle(d / 2 + P.MOVING_CLR / 2) for r, a, d in P.WM["top_holes"]]   # bell screws, catalogue pattern
    for k in range(P.WIN_N):
        phase = P.BAL_BEARING + 360.0 * k / P.WIN_N
        half = P.WIN_HALF_DEG + (P.BAL_EXTRA_DEG if k == 0 else 0.0)  # window 0 is opposite the notch: enlarged to balance
        cuts.append(bd.Rot(0, 0, phase) * plate.ring_window(P.WIN_R_IN, P.WIN_R_OUT, half, P.WIN_ROUND))
    sk = bd.Sketch() + f
    for c in cuts:
        sk = sk - c
    s = bd.extrude(sk, P.DISC_T)
    s.label = "disc"
    bd.RevoluteJoint("spin", s, axis=bd.Axis((0, 0, 0), (0, 0, 1)))
    return s
