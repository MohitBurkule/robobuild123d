"""[tub2] ONE master block of the RV01 tub. Shared masters (wall, skin, column radius, column/bolt pattern INS) drive every
feature file; only the dims below are literals, everything else is a relation. World frame: X across, Y front, Z up."""
from .params_chassis import (CH_HALF_W, CH_Y0, CH_Y1, CH_Z0, CH_Z1, CH_WALL, CH_IN_X, COL_R, INS, INS_Z, N10_TOP, N10_KEY,
                             KEY_SPAN, SA_X0, WALL_IN_FRONT, WALL_IN_REAR, BASE_Z0, BASE_T, BASE_OUT, PANEL_EAR_R,
                             PANEL_EAR_EDGE, PANEL_R_IN, PRELOAD_PAD)

SKIN = CH_WALL / 2                      # master: skin left under pockets; also every small fillet / rib in the tub
DECK = CH_Z1 - CH_WALL                  # deck underside
SEAT_Z = BASE_Z0 + BASE_T               # base panel top = rabbet floor
OVER = SKIN / 10                        # boolean overlap (fuse), not a dimension
# right-hand (+X) bolt pattern; the rear-centre one sits on the axis
INS_RIGHT = tuple(p for p in INS if p[0] > 0)
INS_AXIS = tuple(p for p in INS if p[0] == 0)
# columns
FOOT_R = COL_R + SKIN                   # foot flares 45 deg from this radius into the column
BORE_R, BORE_CH = 1.5, 0.6              # heat-set bore, chamfer at both ends
# corner blocks: face tangent to the column, nose R = COL_R, wall-end fillet = SKIN
# stop wall / key tab / ledge
STOP_FRONT_Y = KEY_SPAN[1]              # stop wall front face is the key tab front face
STOP_BACK_Y = STOP_FRONT_Y - CH_WALL    # one wall thick
LEDGE_X0, LEDGE_Y0, LEDGE_R = 20.0, -27.3, 1.5
STOP_ROUND_R = 4.5
# deck pockets: X pockets on the axis, side pockets between their diagonals, rear boxes between the stop walls
UP_APEX, LO_APEX, DIAG_K, RIB_V = -3.07, -8.13, 0.6404, 4.9
CENTRE_Y0 = -30.0
POCKET_X = INS_RIGHT[0][0] - COL_R      # pocket half width = corner block face
# base seat
PAD_MARGIN = 0.3
