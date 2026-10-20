"""Tub front corner flanges, front-wall pockets and the rear-wall triangle lattice (`additions(c)` / `cuts(c)`)."""
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_lugs import _both

FL_X = (21.4, 29.5)                                      # flange |X| span, side wall to the lug
FACE_TOP, BOT_TOP, GUSSET_CLIP_Z, TOPF_Z = 16.4, 5.0, 8.0, (10.0, 20.0)
GUSSET_Y = (13.0, 27.5)
# param: organic blend from the side wall into the lug (STEP RV01 front corner), (X, Y)
BLEND = [(29.5, 15.0), (28.7, 16.0), (26.5, 18.5), (24.2, 21.0), (22.8, 22.8), (22.0, 24.6), (21.6, 26.3), (21.5, 27.5)]
# param: end
BOT_POLY = Polygon([(21.5, 13.0), (FL_X[1], 13.0)] + BLEND)
TOPF_CLIP = Polygon([(FL_X[0], 13.0), (FL_X[1], 13.0)] + BLEND + [(FL_X[0], BLEND[-1][1])]).buffer(0)
# front face of the corner at Y 15.6, R2.7 fillet into the lug, R1 outer corner (STEP)
FACE_FIL_C, FACE_FIL_R = (24.2, 18.3), 2.7
FLANGE_FACE = Polygon([(FL_X[0], 13.0), (FL_X[1], 13.0), (FL_X[1], 14.6), (28.5, 15.6), (FL_X[0], 15.6)]).union(
    Polygon([(FL_X[0], 15.5), (FACE_FIL_C[0], 15.5), FACE_FIL_C, (FL_X[0], FACE_FIL_C[1])]).difference(Point(FACE_FIL_C).buffer(FACE_FIL_R, 64)))
# 2 x 2.6 gusset (52 deg) between the flange top and the lug face: narrows the printed-ceiling span, stiffens the root (X, Z)
GUSSET = _poly([(21.45, BOT_TOP - 0.01), (23.5, BOT_TOP - 0.01), (21.45, 7.6)])
# param: organic top flange carrying the deck chamfer forward to the lug (Y, Z)
TOPF_YZ = _poly([(13.0, 19.5), (15.3, 19.5), (23.0, 15.83), (23.0, 13.47), (15.3, 16.4), (13.0, 16.4)])
# param: end

WIRE_HOLE, WIRE_Y, WIRE_R = (7.25, 5.0, 10.25, 17.0), (12.0, 16.0), 1.45   # weapon phase wire hole through the front wall: (x0, z0, x1, z1) box
WALL_POCKET_X, WALL_POCKET_Z, WALL_POCKET_Y = ((-18.25, 4.25), (13.25, 18.2)), (6.55, 15.55), (12.0, 13.85)
# param: organic rear-wall triangle lattice, +X half (STEP RV01 inner rear face, X Z)
LATTICE = [Polygon([(4.84, 7.0), (4.84, 15.0), (12.4, 11.0)]), Polygon([(26.42, 7.0), (26.42, 15.0), (18.85, 11.0)]),
           Polygon([(10.6, 5.58), (20.65, 5.58), (15.6, 9.7)]), Polygon([(10.6, 16.42), (20.65, 16.42), (15.6, 12.3)])]
# param: end


def _wall_pocket(x0, x1, z0, z1, y0, y1, r_vert=0.5, r_floor=0.8):
    """Rectangular front-wall pocket cutter (X x Z, floor at y1): R0.5 corners and an R0.8 floor, as in the STEP."""
    b = _b()
    s = _box(x0, x1, y0, y1, z0, z1)
    s = b.fillet(s.edges().filter_by(b.Axis.Y), r_vert)
    return b.fillet(s.faces().sort_by(b.Axis.Y)[-1].edges(), r_floor)


def _lattice_pocket(pts, y0=-36.5, y1=-35.5, r_vert=0.5, r_floor=0.25):
    """Cutter of one triangular rear-wall pocket (X, Z outline `pts`): R0.45 corners and an R0.95 floor (the STEP's R0.98),
    so the pocket has no sharp internal corner in the print."""
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


def _flange(c):
    return [_ext(FLANGE_FACE, "xy", c["z0"], FACE_TOP), _ext(BOT_POLY, "xy", c["z0"], BOT_TOP),
            _I(_ext(GUSSET, "xz", *GUSSET_Y), _ext(BOT_POLY, "xy", c["z0"], GUSSET_CLIP_Z)),
            _I(_I(_ext(TOPF_YZ, "yz", *FL_X), _ext(TOPF_CLIP, "xy", *TOPF_Z)), _ext(_chamfer_xz(c), "xz", *GUSSET_Y))]


def _lattice():
    """STEP rib is 0.35 thinner than the nominal triangle edges: each pocket grows by LAT_GROW."""
    return [_lattice_pocket(list(t.buffer(LAT_GROW, join_style=2).exterior.coords)[:-1]) for t in LATTICE]


def _wire_hole():
    x0, z0, x1, z1 = WIRE_HOLE
    return _ext(_round(Polygon([(x0, z0), (x1, z0), (x1, z1), (x0, z1)]), r_out=WIRE_R), "xz", *WIRE_Y)


def additions(c):
    return [m for s in _flange(c) for m in _both(s)]


def cuts(c):
    return [m for s in _lattice() for m in _both(s)] + [_wire_hole()] + [
        _wall_pocket(xa, xb, *WALL_POCKET_Z, *WALL_POCKET_Y) for xa, xb in WALL_POCKET_X]
