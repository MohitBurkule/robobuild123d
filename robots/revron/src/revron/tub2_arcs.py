"""[tub2] Tangent constructions the designer gets from sketch relations (tangent arcs, tangent lines), as plain 2D formulas: a fillet circle
tangent to a floor line and a round, and the tangent line from a point to a round."""
from math import asin, atan2, cos, degrees, hypot, radians, sin, sqrt


def floor_blend(round_c, round_r, floor_z, r, side):
    """Fillet circle of radius r lying below the floor line z = floor_z (tangent to it) and externally tangent to the round (centre,
    radius) on `side` (-1: fillet centre before the round along +u, +1: after). Returns (centre, tangent point on the round, point on the floor)."""
    cz = floor_z - r
    cu = round_c[0] + side * sqrt((r + round_r) ** 2 - (round_c[1] - cz) ** 2)
    f = round_r / (r + round_r)
    tangent = (round_c[0] + f * (cu - round_c[0]), round_c[1] + f * (cz - round_c[1]))
    return (cu, cz), tangent, (cu, floor_z)


def tangent_from_point(p, round_c, round_r):
    """Tangent point on the round of the line from p that passes above it (the round lies below the line)."""
    d = hypot(round_c[0] - p[0], round_c[1] - p[1])
    beta = atan2(round_c[1] - p[1], round_c[0] - p[0]) + asin(round_r / d)
    length = sqrt(d * d - round_r * round_r)
    return (p[0] + length * cos(beta), p[1] + length * sin(beta))


def angle(c, p):
    """Direction of p seen from c, degrees."""
    return degrees(atan2(p[1] - c[1], p[0] - c[0]))
