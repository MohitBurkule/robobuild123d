"""Gravity-hinged titanium skirts on both sides and the rear. UNTESTED: never built, run, rendered or verified.

Made as really made: 0.5 mm Ti gr5 strip, a flat leaf with one rolled hinge knuckle (inside radius SKIRT_BEND_R) round
a 1 mm music-wire pin that runs through the tub wall on the mid-plane. The leaf hangs to whichever side is down and
rests on the tub's V flank, so it is sloped outward FLANK_DEG and its edge sits SKIRT_DROP over the floor either way up.
Adversarial intent: a wedge or fork meets a floor-level sloped edge (no lip to get under); a horizontal spinner tooth
meets a sloped, free-swinging leaf that deflects up and away instead of a fixed edge it can bite and throw; a lost skirt
costs a skirt, not the robot (pin through the TPU, nothing structural). Built for +X side, mirrored to -X; the rear
skirt is the same profile turned 90 deg.
"""
import math

import build123d as bd

from .params import (SKIRT_T, SKIRT_BEND_R, SKIRT_PIN_D, SKIRT_PIN_Z, SKIRT_DEPTH, FLANK_DEG, SKIRT_SIDE_LEN,
                     SKIRT_REAR_LEN, HALF_W_TUB, HALF_L_TUB, SKIRT_GAP, WALL)


def _profile():
    """XZ section of the sheet in the skirt frame: knuckle centred on the origin (pin axis), leaf running down and out.
    Constant thickness SKIRT_T: an arc band (the roll) + a straight band (the leaf)."""
    r_in = max(SKIRT_BEND_R, SKIRT_PIN_D / 2 + 0.05)
    r_out = r_in + SKIRT_T
    roll = bd.Circle(r_out) - bd.Circle(r_in)
    a = math.radians(FLANK_DEG)
    d = (math.sin(a), -math.cos(a))               # leaf direction, down and outward
    n = (math.cos(a), math.sin(a))                # leaf normal
    p0 = (r_in * n[0], r_in * n[1])               # leaf inner face is tangent to the roll's inner circle side
    pts = [p0, (p0[0] + SKIRT_DEPTH * d[0], p0[1] + SKIRT_DEPTH * d[1]),
           (p0[0] + SKIRT_DEPTH * d[0] + SKIRT_T * n[0], p0[1] + SKIRT_DEPTH * d[1] + SKIRT_T * n[1]),
           (p0[0] + SKIRT_T * n[0], p0[1] + SKIRT_T * n[1])]
    return roll + bd.Polygon(*pts, align=None)


def _skirt(length):
    """Skirt along the Y axis in its own frame (pin axis = Y)."""
    return bd.extrude(bd.Plane.XZ * _profile(), length / 2, both=True)


def side_skirt(sx=1):
    """+X side skirt hung on the side-wall pin; sx=-1 mirrors it."""
    s = bd.Pos(HALF_W_TUB - WALL / 2, 0, SKIRT_PIN_Z) * _skirt(SKIRT_SIDE_LEN)
    return s if sx > 0 else s.mirror(bd.Plane.YZ)


def rear_skirt():
    """Rear skirt: same section, turned so the leaf runs to -Y, on a pin through the rear wall."""
    s = _skirt(SKIRT_REAR_LEN)
    return bd.Pos(0, -(HALF_L_TUB - WALL / 2), SKIRT_PIN_Z) * bd.Rot(0, 0, -90) * s


def skirts():
    return dict(skirt_r=side_skirt(1), skirt_l=side_skirt(-1), skirt_rear=rear_skirt())
