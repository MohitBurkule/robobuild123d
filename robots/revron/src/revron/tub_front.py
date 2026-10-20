"""Tub front corner flanges, front-wall pockets and the rear-wall triangle lattice (`additions(c)` / `cuts(c)`)."""
import math
from shapely.affinity import scale
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_lugs import _both

FL_X = (21.4, 29.5)                                      # flange |X| span, side wall to the lug
FACE_Y, FACE_TOP, BOT_TOP, TOPF_Z = 15.6, 16.4, 5.0, (10.0, 20.0)
FLANGE_Y = (13.0, 27.5)
DIAG_S, DIAG_DEG = 44.5, 45.0                            # outer diagonal edge of the corner: x + y = DIAG_S (STEP), its direction angle
# param: organic corner outline, wall corner R1 then the 45 deg diagonal and the blend into the lug (STEP RV01 front corner), (X, Y)
BLEND = [(29.5, 14.4), (29.3, 15.0), (28.9, FACE_Y), (23.6, 20.9), (22.9, 21.9), (22.3, 22.9), (21.9, 24.0), (21.6, 25.2), (21.5, 28.2)]
# param: end
BOT_POLY = Polygon([(21.5, FLANGE_Y[0]), (FL_X[1], FLANGE_Y[0])] + BLEND)
TOPF_CLIP = Polygon([(FL_X[0], FLANGE_Y[0]), (FL_X[1], FLANGE_Y[0])] + BLEND + [(FL_X[0], BLEND[-1][1])]).buffer(0)
# front face of the corner at Y 15.6, R2.7 fillet into the lug (STEP)
FACE_FIL_C, FACE_FIL_R = (24.2, 18.3), 2.7
FLANGE_FACE = Polygon([(FL_X[0], FLANGE_Y[0])] + BLEND[:3] + [(FL_X[0], FACE_Y)]).union(
    Polygon([(FL_X[0], FACE_Y - 0.1), (FACE_FIL_C[0], FACE_Y - 0.1), FACE_FIL_C, (FL_X[0], FACE_FIL_C[1])]).difference(Point(FACE_FIL_C).buffer(FACE_FIL_R, 64)))
# param: organic top flange carrying the deck chamfer forward to the lug (Y, Z): sloped 0.45/mm top and underside, 2.7 thick
TOPF_YZ = _poly([(13.0, 19.5), (15.1, 19.5), (25.2, 14.96), (25.2, 12.17), (15.8, 16.4), (13.0, 16.4)])
# param: end

WIRE_HOLE, WIRE_Y, WIRE_R = (7.25, 5.0, 10.25, 17.0), (12.0, 16.0), 1.45   # weapon phase wire hole through the front wall: (x0, z0, x1, z1) box
WALL_POCKET_X, WALL_POCKET_Z, WALL_POCKET_Y = ((-18.25, 4.25), (13.25, 18.2)), (6.55, 15.55), (12.0, 13.85)
LAT_Y, LAT_R_VERT, LAT_R_FLOOR = (-36.62, -35.5), 0.95, 0.93   # rear-wall pocket floor / opening Y, corner radius, floor fillet (STEP)
LAT_C = (15.62, 11.0)                                           # symmetry centre of the lattice (X, Z): the pockets mirror about it
# param: organic rear-wall lattice, sharp outlines of the two base pockets measured at Y -35.75 (STEP RV01), X Z
LAT_SIDE = Polygon([(4.76, 6.22), (4.76, 15.78), (13.54, LAT_C[1])])                                       # wall-side triangle
LAT_MID = Polygon([(10.58, 5.51), (20.66, 5.51), (20.66, 7.07), (LAT_C[0], 9.83), (10.58, 7.07)])         # lower pentagon
# param: end
LATTICE = [LAT_SIDE, scale(LAT_SIDE, -1, 1, origin=(LAT_C[0], 0)), LAT_MID, scale(LAT_MID, 1, -1, origin=(0, LAT_C[1]))]


def _wall_pocket(x0, x1, z0, z1, y0, y1, r_vert=0.5, r_floor=0.8):
    """Rectangular front-wall pocket cutter (X x Z, floor at y1): R0.5 corners and an R0.8 floor, as in the STEP."""
    b = _b()
    s = _box(x0, x1, y0, y1, z0, z1)
    s = b.fillet(s.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[-1].edges(), r_floor)


def _lattice_pocket(pts, y0=LAT_Y[0], y1=LAT_Y[1], r_vert=LAT_R_VERT, r_floor=LAT_R_FLOOR):
    """Cutter of one triangular rear-wall pocket (X, Z outline `pts`): R0.5 corners and an R0.98 floor fillet (STEP), so the
    pocket has no sharp internal corner in the print."""
    b = _b()
    with b.BuildPart() as bp:
        with b.BuildSketch(b.Plane.XZ.offset(-y1)):
            b.Polygon(*pts, align=None)
        b.extrude(amount=y1 - y0)
    s = b.fillet(bp.part.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[0].edges(), r_floor)


def _chamfer_xz(c):
    """X-Z outline of the flange with the deck chamfer carried forward along its outer top edge (STEP z17.6: wall at 29.4)."""
    x0, x1 = FL_X
    return _poly([(x0, c["z0"]), (x1, c["z0"]), (x1, c["z1"] - c["cham"]), (x1 - c["cham"], c["z1"]), (x0, c["z1"])])


def _chamfer_diag(c):
    """Deck chamfer carried around the diagonal outer edge (x + y = DIAG_S): the same 45 deg cham, cut square to that edge."""
    b = _b()
    u = DIAG_S / math.sqrt(2.0)
    reach = u + FL_X[1]
    prof = _poly([(-reach, c["z0"]), (u, c["z0"]), (u, c["z1"] - c["cham"]), (u - c["cham"], c["z1"]), (-reach, c["z1"])])
    return _ext(prof, "xz", -reach, reach).rotate(b.Axis.Z, DIAG_DEG)


def _flange(c):
    return [_ext(FLANGE_FACE, "xy", c["z0"], FACE_TOP), _ext(BOT_POLY, "xy", c["z0"], BOT_TOP),
            _I(_I(_I(_ext(TOPF_YZ, "yz", *FL_X), _ext(TOPF_CLIP, "xy", *TOPF_Z)), _ext(_chamfer_xz(c), "xz", *FLANGE_Y)), _chamfer_diag(c))]


def _lattice():
    return [_lattice_pocket(list(t.exterior.coords)[:-1]) for t in LATTICE]


def _wire_hole():
    x0, z0, x1, z1 = WIRE_HOLE
    return _ext(_round(Polygon([(x0, z0), (x1, z0), (x1, z1), (x0, z1)]), r_out=WIRE_R), "xz", *WIRE_Y)


def additions(c):
    return [m for s in _flange(c) for m in _both(s)]


def cuts(c):
    return [m for s in _lattice() for m in _both(s)] + [_wire_hole()] + [
        _wall_pocket(xa, xb, *WALL_POCKET_Z, *WALL_POCKET_Y) for xa, xb in WALL_POCKET_X]
