"""[tub2] Front standoff lug (Boss-Extrude1/2 cut by Cut-Extrude1 + Fillet6 R4): the side profile is a closed sketch of tangent arcs - floor,
R4 blend down to the axle-standoff round SA, R4 blend back up, flat, R4 blend down to the nose round SB, SB round, then the line from the
front-top corner tangent to SB. The two standoff holes are circles in the same sketch. Built for +X and mirrored."""
from build123d import BuildLine, BuildSketch, Circle, CenterArc, Line, Locations, Mode, Plane, extrude, make_face
from .params_chassis import SA, SB, LUG_SA_R, LUG_SB_R, SA_X0, SB_X0
from .tub2_params import CH_Y1, CH_Z0, CH_Z1, WALL_IN_FRONT, CH_WALL, OVER
from .tub2_arcs import angle, floor_blend, tangent_from_point

BLEND_R = 4.0                                   # Fillet6 R4 under the lug
SA_HOLE_R, SB_HOLE_R = 2.5, 1.6                 # 25 mm standoff end clearance, M3 clearance (Sketch4 D1 / D4)


def profile_points():
    """Key points of the tangent chain: the three blends, the tangent point U on SB's top line, and the front-top corner P."""
    c1, t1, f1 = floor_blend(SA, LUG_SA_R, CH_Z0, BLEND_R, -1)
    c2, t2, f2 = floor_blend(SA, LUG_SA_R, CH_Z0, BLEND_R, +1)
    c3, t3, f3 = floor_blend(SB, LUG_SB_R, CH_Z0, BLEND_R, -1)
    corner = (CH_Y1, CH_Z1)
    return c1, t1, f1, c2, t2, f2, c3, t3, f3, tangent_from_point(corner, SB, LUG_SB_R), corner


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
            CenterArc(SB, LUG_SB_R, angle(SB, t3), angle(SB, u) + 360 - angle(SB, t3))
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
