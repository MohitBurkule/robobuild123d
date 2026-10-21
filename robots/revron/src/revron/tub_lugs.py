"""Tub front lugs: weapon-mount tabs, the standoff lugs and their underside cuts, standoff / key holes.

Everything is built for the +X half and mirrored; `additions(c)` / `cuts(c)` take the CH dict and return solids."""
import math
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from functools import partial as _partial
_ext = _partial(_ext, arcs=True)   # polygonised arcs become true arcs (cylinders, not facets)

# ---- tables are (Y, Z) in the yz plane unless noted; the |X| spans are the extrusion ranges
SEG_AXIS = 128                  # facets of the weapon-axis clearance circle
FUSE = 0.1                      # overlap that fuses a feature into its neighbour / cutter overshoot past a face
MNT_GAP = (0.2, 0.1)            # tab / tab wall stop this far short of the weapon-mount inner face (tab keys into the notch)
LUG_X = (SA_X0, SB_X0)      # lug spans from the axle standoff end to the nose standoff end
TAB_X = (MNT_IN - MNT_GAP[0], LUG_X[0] + FUSE)          # key tab: from the mount face (inside the notch) into the lug
TABW_THK = 3.0                  # inner tab wall thickness
TABW_X = (MNT_IN - MNT_GAP[1] - TABW_THK, MNT_IN - MNT_GAP[1])
LUG_CUT_X = (LUG_X[0] - FUSE, LUG_X[1] + FUSE)        # underside cutters overshoot the lug faces
HOLE_OVER = 0.5                 # standoff hole cutters overshoot the lug faces
HOLE_X = (LUG_X[0] - HOLE_OVER, LUG_X[1] + HOLE_OVER)
KEY_X = (TABW_X[0] - 0.3, HOLE_X[1])                  # key hole runs through tab wall and lug (0.3 overshoot past the wall)
SA_HOLE_R, SB_HOLE_R, KEY_R = 2.5, 1.6, 0.9           # standoff end clearance holes (SA M5, SB M3), key hole corner radius
FRONT_Y = CH_Y1              # front wall outer face
RABBET_X, RABBET_Y = (TABW_X[1], LUG_X[0]), (12.0, FRONT_Y + FUSE)   # front wall stops at the base-panel rabbet under the tab
RABBET_TOP = CH_Z0 + CH_WALL                    # rabbet floor: top of the base panel

KEY_BOX, KEY_CHAM, KEY_WALL = (18.5, 5.4, 26.5, 13.5), 1.0, 1.5   # key tab (Y0, Z0, Y1, Z1), its chamfer, wall left round the key hole


def _octagon(y0, z0, y1, z1, ch):
    return [(y0 + ch, z0), (y1 - ch, z0), (y1, z0 + ch), (y1, z1 - ch), (y1 - ch, z1), (y0 + ch, z1), (y0, z1 - ch), (y0, z0 + ch)]


TAB_PROFILE = _octagon(*KEY_BOX, KEY_CHAM)   # key tab octagon that keys into the weapon-mount notch
LUG_Y0 = FRONT_Y - CH_WALL   # lug / tab wall start at the front wall's inner face
# param: organic inner tab wall (STEP outline) right flank and top slope; the rest follows the chassis and key tab
_KY1 = KEY_BOX[2]
TABW_PROFILE = [(LUG_Y0, CH_Z0), (_KY1 - KEY_CHAM, CH_Z0), (_KY1, CH_Z0 + KEY_CHAM), (_KY1, 12.35), (25.59, 14.75),
                (FRONT_Y, CH_Z1), (LUG_Y0, CH_Z1)]
# param: end
TAB_WALL = Polygon(TABW_PROFILE).difference(Point(WY, WZ).buffer(WEAPON_CLEAR_R, SEG_AXIS))
FIL_R = 2.0                     # R2 fillet block into the front face (XY): corner circle at (x0, y1)
FIL_BOX = (TABW_X[0] - FIL_R, FRONT_Y - FUSE, TABW_X[0] + FUSE, FRONT_Y + FIL_R)   # abuts the tab wall, sunk into the front wall
FIL_BLOCK = Polygon([(FIL_BOX[0], FIL_BOX[1]), (FIL_BOX[2], FIL_BOX[1]), (FIL_BOX[2], FIL_BOX[3]), (FIL_BOX[0], FIL_BOX[3])]).difference(
    Point(FIL_BOX[0], FIL_BOX[3]).buffer(FIL_R, 48))

# param: organic lug outline (STEP RV01): foot, ramp toe, standoff arcs SA / SB, nose tip, top
LUG_FOOT_Y, LUG_RAMP_TOE, LUG_NOSE_TIP, LUG_TOP_Y = 26.0, (SA[0], SA[1] - 4.5), (36.6, LUG_FLOOR_Z), FRONT_Y
# param: end
FULL_TURN = 360.0
UNDER_BLEND_N, UNDER_SB_N = 24, 24                  # facets of the underside blend / standoff arcs
# the lug's top edge runs from the top-back corner tangent to the nose standoff arc: the arc ends where that tangent leaves it
_TOP_D = (SB[0] - LUG_TOP_Y, SB[1] - CH_Z1)
SB_TOP_ANG = math.degrees(math.atan2(-_TOP_D[1], -_TOP_D[0]) - math.acos(LUG_SB_R / math.hypot(*_TOP_D)))   # direction standoff centre -> tangent point
SA_ARC, SB_ARC = (LUG_SA_R, 250, 300, 6), (LUG_SB_R, 250, SB_TOP_ANG + FULL_TURN, 36)
# param: organic underside the hull must not fill (STEP ramp, Y/Z)
LUG_UNDER_POLY = Polygon([(LUG_FOOT_Y, 0.0), (LUG_FOOT_Y, LUG_FLOOR_Z), (30.0, 1.0), (40.0, 0.9), (60, 0)])
# param: end
CUT_Y0, CUT_Z0 = LUG_Y0 - 3.0, CH_Z0 - 7.5   # flat-ramp cutter starts clear behind the lug and reaches well below the floor
# param: underside ramp of the axle standoff boss (STEP, fitted at X 19.5): an R4 concave fillet off the floor tangent to the R4.5 boss round (Fillet6 R4)
RAMP_R = 4.0
_RC = (SA[0] - math.sqrt((LUG_SA_R + RAMP_R) ** 2 - (SA[1] - (LUG_FLOOR_Z - RAMP_R)) ** 2), LUG_FLOOR_Z - RAMP_R)   # fillet centre
_RA = math.degrees(math.atan2(SA[1] - _RC[1], SA[0] - _RC[0]))                                                   # direction fillet centre -> tangent point
RAMP_CURVE = _arc(_RC, RAMP_R, 90.0, _RA, 16) + _arc(SA, LUG_SA_R, _RA + 180.0, 270.0, 16)[1:]                    # floor -> fillet -> boss bottom
# param: end
LUG_FLAT_RAMP = _poly([(CUT_Y0, CUT_Z0), (CUT_Y0, LUG_FLOOR_Z)] + RAMP_CURVE + [(SA[0], CUT_Z0)])
RAMP_KEEP = _poly(RAMP_CURVE + [(SA[0], LUG_FLOOR_Z + 0.5), (_RC[0], LUG_FLOOR_Z + 0.5)])          # material above the curve
RAMP_ZONE = Polygon([(_RC[0], 0.0), (SA[0], 0.0), (SA[0], LUG_FLOOR_Z + 0.5), (_RC[0], LUG_FLOOR_Z + 0.5)])   # hull layer the curve replaces
# under the nose standoff the lug follows its arc: no hull chord below it where the scallop meets it
# one path floor -> blend arc -> standoff arc, so the blend and standoff arcs share their tangent point exactly (no boolean sliver)
_T_ON_BLEND = math.degrees(math.atan2(SB[1] - _blend_c[1], SB[0] - _blend_c[0]))   # direction blend centre -> tangent point
_T_ON_SB = _T_ON_BLEND - 180.0                                                     # direction standoff centre -> tangent point
LUG_UNDER = Polygon(_arc(_blend_c, LUG_BLEND_R, 90.0, _T_ON_BLEND, UNDER_BLEND_N) + _arc(SB, LUG_SB_R, _T_ON_SB + 360.0, 270.0, UNDER_SB_N)[1:]
                    + [(SB[0], 0.0), (LUG_SCALLOP_YT, 0.0)])
_k0 = KEY_WALL
KEY_HOLE = _round(Polygon([(KEY_BOX[0] + _k0, KEY_BOX[1] + _k0), (KEY_BOX[2] - _k0, KEY_BOX[1] + _k0), (KEY_BOX[2] - _k0, KEY_BOX[3] - _k0),
                           (KEY_BOX[0] + _k0, KEY_BOX[3] - _k0)]), r_out=KEY_R)   # square key hole = key tab inset by KEY_WALL


def _both(s):
    return [s, _mirror_x(s)]


def _tabs(c):
    return [_ext(_poly(TAB_PROFILE), "yz", *TAB_X), _ext(TAB_WALL, "yz", *TABW_X), _ext(FIL_BLOCK, "xy", c["z0"], c["deck"])]


def _lug(c):
    hull = Polygon([(LUG_Y0, c["z0"]), (LUG_FOOT_Y, c["z0"]), LUG_RAMP_TOE] + _arc(SA, *SA_ARC) + [LUG_NOSE_TIP]
                   + _arc(SB, *SB_ARC) + [(LUG_TOP_Y, c["z1"]), (LUG_Y0, c["z1"])])
    return _ext(hull.convex_hull.difference(LUG_UNDER_POLY).difference(RAMP_ZONE).union(RAMP_KEEP), "yz", *LUG_X)


def _underside(c):
    return [_ext(p, "yz", *LUG_CUT_X) for p in (LUG_FLAT_RAMP, LUG_SCALLOP, LUG_UNDER)] + [
        _box(*RABBET_X, *RABBET_Y, c["z0"] - FUSE, RABBET_TOP)]


def _holes():
    return [_cyl(SA_HOLE_R, *HOLE_X, SA), _cyl(SB_HOLE_R, *HOLE_X, SB), _ext(KEY_HOLE, "yz", *KEY_X)]


def additions(c):
    return [m for s in _tabs(c) + [_lug(c)] for m in _both(s)]


def cuts(c):
    return [m for s in _underside(c) + _holes() for m in _both(s)]
