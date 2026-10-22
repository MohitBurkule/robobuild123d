"""[tub2] Front corner flange outboard of the lug (Boss-Extrude1 outline, Fillet2 R8, Fillet3 R2, Fillet18 R3): a plan bounded by the side wall,
the 45 deg diagonal from the chassis front corner (x + y = CH_HALF_W + CH_Y1), an R8 blend tangent to the diagonal and the lug face, and the
R2 corner between wall and diagonal. Three layers: the base plate, the front web up to the web face, and the top flange between two
parallel lines sloping like the lug top. Built for +X and mirrored."""
from math import hypot, sqrt
from build123d import BuildLine, BuildSketch, CenterArc, Line, Plane, Polygon, chamfer, extrude, fillet, make_face
from .params_chassis import SB_X0
from .tub2_params import CH_HALF_W, CH_Y1, CH_Z0, CH_Z1, CH_WALL, SKIN, OVER, SEAT_Z, WALL_IN_FRONT, FRONT_RIB
from .tub2_lug import top_line_slope
from .tub2_util import box_xy, concave_filler, prism

BLEND_R = 8.0                          # Fillet2: diagonal into the lug face
FACE_FIL_R = 3 * SKIN                  # Fillet18: web face into the lug face
FACE_Y = CH_Y1 + FRONT_RIB             # front face of the web
BOT_TOP = SEAT_Z + SKIN / 2            # base plate top
FLANGE_T = 2.7                         # vertical thickness of the sloping top flange
APEX_SHY = 0.005                       # as the shell: equal chamfer and round collapse the cone apex
DIAG_S = CH_HALF_W + CH_Y1             # diagonal x + y = DIAG_S, 45 deg, from the front corner of the side wall


def plan():
    """Flange plan (XY): lug face, front wall line, side wall, diagonal, R8 blend back to the lug face; wall/diagonal corner rounded R = wall."""
    cx, cy = CH_HALF_W, DIAG_S - CH_HALF_W + BLEND_R * sqrt(2)         # R8 centre: x = wall plane, tangent to the diagonal
    t_diag = (cx - BLEND_R / sqrt(2), cy - BLEND_R / sqrt(2))
    with BuildSketch() as sk:
        with BuildLine():
            Line((SB_X0, WALL_IN_FRONT), (CH_HALF_W, WALL_IN_FRONT))
            Line((CH_HALF_W, WALL_IN_FRONT), (CH_HALF_W, CH_Y1))
            Line((CH_HALF_W, CH_Y1), t_diag)
            CenterArc((cx, cy), BLEND_R, 225, -45)
            Line((SB_X0, cy), (SB_X0, WALL_IN_FRONT))
        make_face()
        fillet([v for v in sk.vertices() if abs(v.X - CH_HALF_W) < OVER and abs(v.Y - CH_Y1) < OVER], CH_WALL)
    return sk


def flange():
    """Base plate + front web (with its R3 blend into the lug) + sloping top flange."""
    f = plan()
    plate = prism(f, CH_Z0, BOT_TOP)
    web = prism(f, CH_Z0, CH_Z1) & box_xy(SB_X0 - 1, CH_HALF_W + 1, WALL_IN_FRONT - 1, FACE_Y, CH_Z0, CH_Z1)
    s = top_line_slope()
    z_at = lambda y: CH_Z1 + s * (y - CH_Y1)
    y0, y1 = FACE_Y - SKIN, CH_Y1 + 3 * BLEND_R
    with BuildSketch(Plane.YZ.offset(SB_X0 - 1)) as under:        # everything under the lug's sloping top line
        Polygon((y0, CH_Z0), (y1, CH_Z0), (y1, z_at(y1)), (y0, z_at(y0)), align=None)
    blend = prism(concave_filler((SB_X0, FACE_Y), (1, 1), FACE_FIL_R), CH_Z0, CH_Z1) & extrude(under.sketch, CH_HALF_W - SB_X0 + 2)
    with BuildSketch(Plane.YZ.offset(SB_X0 - 1)) as sl:
        Polygon((y0, z_at(y0)), (y1, z_at(y1)), (y1, z_at(y1) - FLANGE_T), (y0, z_at(y0) - FLANGE_T), align=None)
    slab = extrude(sl.sketch, CH_HALF_W - SB_X0 + 2) & prism(f, CH_Z0, CH_Z1)
    clipped = slab & box_xy(SB_X0 - 1, CH_HALF_W + 1, y0, y1, CH_Z0, CH_Z1)
    web = web & (extrude(under.sketch, CH_HALF_W - SB_X0 + 2) + box_xy(SB_X0 - 1, CH_HALF_W + 1, WALL_IN_FRONT - 1, y0, CH_Z0, CH_Z1))                  # the web's front top edge follows the lug's sloping top line too
    body = plate + web + blend + clipped
    return body & _chamfered_plan(f)


def _chamfered_plan(f):
    """The plan prism with the deck chamfer (CH_WALL, 45 deg) on its outer top edges: the side wall, the R-wall corner round (a cone, like the
    shell's corners) and the diagonal. Everything the flange adds lies inside this solid, so intersecting with it chamfers all layers alike."""
    cx, cy = CH_HALF_W - CH_WALL, DIAG_S - CH_HALF_W - CH_WALL * (sqrt(2) - 1)   # corner round centre: tangent to the wall and the diagonal
    prism_f = prism(f, CH_Z0, CH_Z1)

    def outer(e):
        pts = [e.position_at(t) for t in (0.0, 0.5, 1.0)]
        on_wall = all(abs(p.X - CH_HALF_W) < OVER / 10 for p in pts)
        on_diag = all(abs(p.X + p.Y - DIAG_S) < OVER / 10 for p in pts)
        on_round = all(abs(hypot(p.X - cx, p.Y - cy) - CH_WALL) < OVER / 10 for p in pts)
        return abs(pts[1].Z - CH_Z1) < OVER / 10 and (on_wall or on_diag or on_round)
    return chamfer([e for e in prism_f.edges() if outer(e)], CH_WALL - APEX_SHY)
