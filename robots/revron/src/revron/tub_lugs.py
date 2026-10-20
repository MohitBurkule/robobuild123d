"""Tub front lugs: weapon-mount tabs, the standoff lugs and their underside cuts, standoff / key holes.

Everything is built for the +X half and mirrored; `additions(c)` / `cuts(c)` take the CH dict and return solids."""
import math
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403

# ---- tables are (Y, Z) in the yz plane unless noted; the |X| spans are the extrusion ranges
SEG_AXIS = 128                  # facets of the weapon-axis clearance circle
TAB_X, TABW_X = (13.2, 17.6), (10.3, 13.3)
LUG_X = (17.5, 21.5)
LUG_CUT_X = (LUG_X[0] - 0.1, LUG_X[1] + 0.1)          # underside cutters overshoot the lug faces
HOLE_X, KEY_X = (17.0, 22.0), (10.0, 22.0)
SA_HOLE_R, SB_HOLE_R, KEY_R = 2.5, 1.6, 0.9
RABBET_X, RABBET_Y, RABBET_TOP = (TABW_X[1], LUG_X[0]), (12.0, 15.1), 4.5   # front wall stops at the base-panel rabbet under the tab

# param: organic key tab octagon (chamfer 1) that keys into the weapon-mount notch
TAB_PROFILE = [(18.5, 6.4), (19.5, 5.4), (25.5, 5.4), (26.5, 6.4), (26.5, 12.5), (25.5, 13.5), (19.5, 13.5), (18.5, 12.5)]
# param: end
# param: organic inner tab wall (STEP outline); its top-front corner is cut back on WEAPON_CLEAR_R about the weapon axis
TABW_PROFILE = [(13.0, 2.5), (25.5, 2.5), (26.5, 3.5), (26.5, 12.35), (25.59, 14.75), (15.0, 19.5), (13.0, 19.5)]
# param: end
TAB_WALL = Polygon(TABW_PROFILE).difference(Point(WY, WZ).buffer(WEAPON_CLEAR_R, SEG_AXIS))
FIL_BOX, FIL_R = (8.3, 14.9, 10.4, 17.0), 2.0           # R2 fillet block into the front face (XY): corner circle at (x0, y1)
FIL_BLOCK = Polygon([(FIL_BOX[0], FIL_BOX[1]), (FIL_BOX[2], FIL_BOX[1]), (FIL_BOX[2], FIL_BOX[3]), (FIL_BOX[0], FIL_BOX[3])]).difference(
    Point(FIL_BOX[0], FIL_BOX[3]).buffer(FIL_R, 48))

# param: organic lug outline (STEP RV01): foot, ramp toe, standoff arcs SA / SB, nose tip, top
LUG_Y0, LUG_FOOT_Y, LUG_RAMP_TOE, LUG_NOSE_TIP, LUG_TOP_Y = 13.0, 26.0, (30.4, 1.0), (36.6, LUG_FLOOR_Z), 15.0
# param: end
UNDER_BLEND_N, UNDER_SB_N = 24, 24                  # facets of the underside blend / standoff arcs
SA_ARC, SB_ARC = (4.5, 250, 300, 6), (LUG_SB_R, 250, 400, 24)
LUG_UNDER_POLY = Polygon([(LUG_FOOT_Y, 0.0), (LUG_FOOT_Y, LUG_FLOOR_Z), (30.0, 1.0), (40.0, 0.9), (60, 0)])   # underside the hull must not fill
LUG_FLAT_RAMP = _poly([(10.0, -5.0), (10.0, LUG_FLOOR_Z), (LUG_FOOT_Y, LUG_FLOOR_Z), LUG_RAMP_TOE, (LUG_RAMP_TOE[0], -5.0)])
# under the nose standoff the lug follows its arc: no hull chord below it where the scallop meets it
# one path floor -> blend arc -> standoff arc, so the blend and standoff arcs share their tangent point exactly (no boolean sliver)
_T_ON_BLEND = math.degrees(math.atan2(SB[1] - _blend_c[1], SB[0] - _blend_c[0]))   # direction blend centre -> tangent point
_T_ON_SB = _T_ON_BLEND - 180.0                                                     # direction standoff centre -> tangent point
LUG_UNDER = Polygon(_arc(_blend_c, LUG_BLEND_R, 90.0, _T_ON_BLEND, UNDER_BLEND_N) + _arc(SB, LUG_SB_R, _T_ON_SB + 360.0, 270.0, UNDER_SB_N)[1:]
                    + [(SB[0], 0.0), (LUG_SCALLOP_YT, 0.0)])
# param: organic square key hole through lug and tab wall
KEY_HOLE = _round(Polygon([(20.0, 6.9), (25.0, 6.9), (25.0, 12.0), (20.0, 12.0)]), r_out=KEY_R)
# param: end


def _both(s):
    return [s, _mirror_x(s)]


def _tabs(c):
    return [_ext(_poly(TAB_PROFILE), "yz", *TAB_X), _ext(TAB_WALL, "yz", *TABW_X), _ext(FIL_BLOCK, "xy", c["z0"], c["deck"])]


def _lug(c):
    hull = Polygon([(LUG_Y0, c["z0"]), (LUG_FOOT_Y, c["z0"]), LUG_RAMP_TOE] + _arc(SA, *SA_ARC) + [LUG_NOSE_TIP]
                   + _arc(SB, *SB_ARC) + [(LUG_TOP_Y, c["z1"]), (LUG_Y0, c["z1"])])
    return _ext(hull.convex_hull.difference(LUG_UNDER_POLY), "yz", *LUG_X)


def _underside(c):
    return [_ext(p, "yz", *LUG_CUT_X) for p in (LUG_FLAT_RAMP, LUG_SCALLOP, LUG_UNDER)] + [
        _box(*RABBET_X, *RABBET_Y, c["z0"] - 0.1, RABBET_TOP)]


def _holes():
    return [_cyl(SA_HOLE_R, *HOLE_X, SA), _cyl(SB_HOLE_R, *HOLE_X, SB), _ext(KEY_HOLE, "yz", *KEY_X)]


def additions(c):
    return [m for s in _tabs(c) + [_lug(c)] for m in _both(s)]


def cuts(c):
    return [m for s in _underside(c) + _holes() for m in _both(s)]
