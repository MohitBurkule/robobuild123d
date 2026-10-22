"""[tub2] Front standoff lug (Boss-Extrude1/2 cut by Cut-Extrude1 + Fillet6 R4): the side profile is a closed sketch of tangent arcs - floor,
R4 blend down to the axle-standoff round SA, R4 blend back up, flat, R4 blend down to the nose round SB, SB round, then the line from the
front-top corner tangent to SB. The two standoff holes are circles in the same sketch. Built for +X and mirrored."""
from build123d import BuildLine, BuildSketch, Circle, CenterArc, Line, Locations, Mode, Plane, extrude, make_face
from .params_chassis import SA, SB, LUG_SA_R, LUG_SB_R, LUG_SCALLOP_R, SA_X0, SB_X0, SO_R, M3, fc
from .tub2_params import CH_Y1, CH_Z0, CH_Z1, WALL_IN_FRONT, CH_WALL, OVER
from math import atan2, cos, hypot, sin, sqrt
from .tub2_arcs import angle, floor_blend, tangent_from_point

BLEND_R = LUG_SCALLOP_R                         # Fillet6 R4 under the lug (the scallop R)
NOSE_TIP_OFF, NOSE_TIP_R = (0.16, 0.2), 3.0         # top of the nose: a slightly smaller round, shifted up-front, takes the top line (STEP: R3.0 on the section)
SA_HOLE_R, SB_HOLE_R = SO_R, fc.clearance(M3, 'close') / 2   # standoff end (its own radius), M3 clearance (Sketch4 D1 / D4)


def profile_points():
    """Key points of the tangent chain: the three blends, the tangent point U on SB's top line, and the front-top corner P."""
    c1, t1, f1 = floor_blend(SA, LUG_SA_R, CH_Z0, BLEND_R, -1)
    c2, t2, f2 = floor_blend(SA, LUG_SA_R, CH_Z0, BLEND_R, +1)
    c3, t3, f3 = floor_blend(SB, LUG_SB_R, CH_Z0, BLEND_R, -1)
    corner = (CH_Y1, CH_Z1)
    return c1, t1, f1, c2, t2, f2, c3, t3, f3, tangent_from_point(corner, nose_tip()[0], NOSE_TIP_R), corner


def nose_tip():
    """Centre of the nose-top round and where it meets the SB round (upper intersection of the two circles)."""
    c = (SB[0] + NOSE_TIP_OFF[0], SB[1] + NOSE_TIP_OFF[1])
    d = hypot(c[0] - SB[0], c[1] - SB[1])
    a = (LUG_SB_R ** 2 - NOSE_TIP_R ** 2 + d * d) / (2 * d)
    h = sqrt(LUG_SB_R ** 2 - a * a)
    ux, uy = (c[0] - SB[0]) / d, (c[1] - SB[1]) / d
    pts = [(SB[0] + a * ux - s * h * uy, SB[1] + a * uy + s * h * ux) for s in (1, -1)]
    return c, max(pts, key=lambda p: p[0])


def top_line_slope():
    """dz/dy of the lug's top line (also the tab wall top and the flange top)."""
    u, c = profile_points()[-2], profile_points()[-1]
    return (u[1] - c[1]) / (u[0] - c[0])


def side_profile():
    """Closed side profile of the lug (sketch x = world Y, y = world Z) with the two standoff holes cut."""
    c1, t1, f1, c2, t2, f2, c3, t3, f3, u, p = profile_points()
    with BuildSketch(Plane.YZ.offset(SA_X0)) as sk:
        with BuildLine():
            Line((WALL_IN_FRONT, CH_Z0), f1)
            CenterArc(c1, BLEND_R, 90, angle(c1, t1) - 90)
            CenterArc(SA, LUG_SA_R, angle(SA, t1), angle(SA, t2) - angle(SA, t1))
            CenterArc(c2, BLEND_R, angle(c2, t2), 90 - angle(c2, t2))
            Line(f2, f3)
            CenterArc(c3, BLEND_R, 90, angle(c3, t3) - 90)
            tip, x = nose_tip()
            CenterArc(SB, LUG_SB_R, angle(SB, t3), angle(SB, x) - angle(SB, t3))
            CenterArc(tip, NOSE_TIP_R, angle(tip, x), angle(tip, u) - angle(tip, x))
            Line(u, p)
            Line(p, (WALL_IN_FRONT, CH_Z1))
            Line((WALL_IN_FRONT, CH_Z1), (WALL_IN_FRONT, CH_Z0))
        make_face()
        for c, r in ((SA, SA_HOLE_R), (SB, SB_HOLE_R)):
            with Locations(c):
                Circle(r, mode=Mode.SUBTRACT)
    return sk


def lug():
    """The lug between the axle-standoff inner end and the nose-standoff inner end."""
    return extrude(side_profile().sketch, SB_X0 - SA_X0)
