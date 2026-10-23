"""[tub2] Front corner flange outboard of the lug (Boss-Extrude1 outline, Fillet2 R8, Fillet3 R2, Fillet18 R3): a plan bounded by the side wall,
the 45 deg diagonal from the chassis front corner (x + y = CH_HALF_W + CH_Y1), an R8 blend tangent to the diagonal and the lug face, and the
R2 corner between wall and diagonal. Three layers: the base plate, the front web up to the web face, and the top flange between two
parallel lines sloping like the lug top. Built for +X and mirrored."""
from math import sqrt
from build123d import Cylinder, Pos, Rot, BuildLine, BuildSketch, CenterArc, Line, Plane, Polygon, extrude, fillet, make_face
from .params_chassis import SA, SB_X0
from .params_side import WG_SA_R, WG_MOUNT_GAP
from .tub2_params import CH_HALF_W, CH_Y1, CH_Z0, CH_Z1, CH_WALL, SKIN, OVER, SEAT_Z, WALL_IN_FRONT, FRONT_RIB
from .tub2_lug import top_line_slope
from .tub2_util import box_xy, concave_filler, prism

BLEND_R_STEP = 8.0                     # Fillet2 R8: diagonal into the lug face
DIAG_S = CH_HALF_W + CH_Y1             # diagonal x + y = DIAG_S, 45 deg, from the front corner of the side wall
# the concave blend meets the lug face (x = SB_X0) at y = DIAG_S - SB_X0 - R (1 - sqrt 2); the wedgelet's cheek bulb round the axle standoff SA
# stands outboard of that face from SA - WG_SA_R, so the blend ends WG_MOUNT_GAP short of it: R8 as drawn, smaller where SA moves toward the corner
FLANGE_MIN_W = 2 * CH_WALL             # a flange narrower than this (side wall less the lug face) is a wall's worth of nothing: a narrow chassis leaves it out
# the blend's tangent point on the diagonal must stay a wall in from the side wall (a narrow chassis gives the R8 less room): R fits the width
BLEND_R = max(0.1, min(BLEND_R_STEP, (SA[0] - WG_SA_R - WG_MOUNT_GAP - (DIAG_S - SB_X0)) / (sqrt(2) - 1), (CH_HALF_W - CH_WALL - SB_X0) / (1 - 1 / sqrt(2))))
FACE_FIL_R = 3 * SKIN                  # Fillet18: web face into the lug face
FACE_Y = CH_Y1 + FRONT_RIB             # front face of the web
BOT_TOP = SEAT_Z + SKIN / 2            # base plate top
FLANGE_T = 2.7                         # vertical thickness of the sloping top flange


def blend_centre():
    """Centre of the blend circle: tangent to the lug face x = SB_X0 and to the diagonal, on the free side of both (R8: on the wall plane)."""
    return SB_X0 + BLEND_R, DIAG_S - SB_X0 - BLEND_R + BLEND_R * sqrt(2)


def plan():
    """Flange plan (XY): lug face, front wall line, side wall, diagonal, R8 blend back to the lug face; wall/diagonal corner rounded R = wall."""
    cx, cy = blend_centre()
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
    """Base plate + front web (with its R3 blend into the lug) + sloping top flange; None where the chassis is too narrow to hold one."""
    if CH_HALF_W - SB_X0 < FLANGE_MIN_W:
        return None
    f = plan()
    plate = prism(f, CH_Z0, BOT_TOP)
    web = prism(f, CH_Z0, CH_Z1) & box_xy(SB_X0 - 1, CH_HALF_W + 1, WALL_IN_FRONT - 1, FACE_Y, CH_Z0, CH_Z1)
    s = top_line_slope()
    z_at = lambda y: CH_Z1 + s * (y - CH_Y1)
    y0, y1 = FACE_Y - SKIN, CH_Y1 + 3 * BLEND_R_STEP   # the slab reaches past the plan whatever the blend
    with BuildSketch(Plane.YZ.offset(SB_X0 - 1)) as under:        # everything under the lug's sloping top line
        Polygon((y0, CH_Z0), (y1, CH_Z0), (y1, z_at(y1)), (y0, z_at(y0)), align=None)
    blend = prism(concave_filler((SB_X0, FACE_Y), (1, 1), FACE_FIL_R), CH_Z0, CH_Z1) & extrude(under.sketch, CH_HALF_W - SB_X0 + 2)
    with BuildSketch(Plane.YZ.offset(SB_X0 - 1)) as sl:
        Polygon((y0, z_at(y0)), (y1, z_at(y1)), (y1, z_at(y1) - FLANGE_T), (y0, z_at(y0) - FLANGE_T), align=None)
    slab = extrude(sl.sketch, CH_HALF_W - SB_X0 + 2) & prism(f, CH_Z0, CH_Z1)
    clipped = slab & box_xy(SB_X0 - 1, CH_HALF_W + 1, y0, y1, CH_Z0, CH_Z1)
    web = web & (extrude(under.sketch, CH_HALF_W - SB_X0 + 2) + box_xy(SB_X0 - 1, CH_HALF_W + 1, WALL_IN_FRONT - 1, y0, CH_Z0, CH_Z1))   # the web's front top edge follows the lug's sloping top line too
    body = plate + web + blend + clipped
    v_corner = (CH_Y1 - CH_HALF_W) / sqrt(2)                                 # diagonal coordinate of the wall corner
    body = body - _chamfer_wedge(CH_HALF_W, 0, WALL_IN_FRONT - 1, CH_Y1) - _chamfer_wedge(DIAG_S / sqrt(2), 45, v_corner, _tangent_v())
    if DIAG_S - SB_X0 > SA[0] - WG_SA_R - WG_MOUNT_GAP:   # a wide chassis pushes the diagonal over the axle standoff even with the smallest blend: relieve the flange round it (the wedgelet's cheek stands there)
        body = body - Pos((SB_X0 + CH_HALF_W) / 2, SA[0], SA[1]) * Rot(0, 90, 0) * Cylinder(WG_SA_R + WG_MOUNT_GAP, CH_HALF_W - SB_X0 + 2)
    return body


def _tangent_v():
    """Diagonal coordinate v = (y - x) / sqrt(2) of the R8 blend's tangent point on the diagonal."""
    cx, cy = blend_centre()
    tx, ty = cx - BLEND_R / sqrt(2), cy - BLEND_R / sqrt(2)
    return (ty - tx) / sqrt(2)


def _chamfer_wedge(u0, angle, v0, v1):
    """The deck chamfer (CH_WALL, 45 deg) on the top edge of the outer face u = u0, between v0 and v1 along the edge. u / v are the plane
    coordinates rotated `angle` about Z (side wall: 0, diagonal: 45), so both faces share one construction."""
    plane = Plane.XZ.rotated((0, angle, 0)).offset(-v0)
    with BuildSketch(plane) as sk:
        Polygon((u0 - CH_WALL, CH_Z1), (u0 + 1, CH_Z1 - CH_WALL - 1), (u0 + 1, CH_Z1 + 1), (u0 - CH_WALL - 1, CH_Z1 + 1), align=None)
    return extrude(sk.sketch, -(v1 - v0))
