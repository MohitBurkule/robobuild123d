"""[tub2] ONE master block of the RV01 tub. Shared masters (wall, skin, column radius, column/bolt pattern INS) drive every
feature file; only the dims below are literals, everything else is a relation. World frame: X across, Y front, Z up."""
from .params_chassis import (CH_HALF_W, CH_Y0, CH_Y1, CH_Z0, CH_Z1, CH_WALL, CH_IN_X, COL_R, INS, INS_Z, N10_TOP, N10_KEY,
                             KEY_SPAN, SA_X0, WALL_IN_FRONT, WALL_IN_REAR, BASE_Z0, BASE_T, BASE_OUT, PRELOAD_PAD)

SKIN = CH_WALL / 2                      # master: skin left under pockets; also every small fillet / rib in the tub
DECK = CH_Z1 - CH_WALL                  # deck underside
SEAT_Z = BASE_Z0 + BASE_T               # base panel top = rabbet floor
CAVITY_R = 3 * SKIN / 2                 # inner cavity corner R
OVER = SKIN / 10                        # boolean overlap (fuse), not a dimension
# right-hand (+X) bolt pattern; the rear-centre one sits on the axis
INS_RIGHT = tuple(p for p in INS if p[0] > 0)
INS_AXIS = tuple(p for p in INS if p[0] == 0)
# columns
INSERT_OD, KNURL = 3.5, 0.25            # FS1 M2 heat-set: knurled OD and knurl depth
BORE_R, BORE_CH = INSERT_OD / 2 - KNURL, 0.6   # heat-set bore = the insert's core (the knurl melts in), chamfer 0.6 at both ends
# corner blocks: face tangent to the column, nose R = COL_R, wall-end fillet = SKIN
# stop wall / key tab / ledge
STOP_FRONT_Y = KEY_SPAN[1]              # stop wall front face is the key tab front face
STOP_BACK_Y = STOP_FRONT_Y - CH_WALL    # one wall thick
LEDGE_X0, LEDGE_Y0, LEDGE_R = 20.0, -27.3, 1.5
STOP_ROUND_R = 5.0
# deck pockets: two diagonal ribs run from the centre (mid of the front/rear column rows) through the column centres; each rib is
# 2 walls wide. The four regions between the ribs are the pockets (X pockets on the axis, side pockets); R = wall at every rib corner.
CENTRE_Y = sum(y for _, y in INS_RIGHT) / len(INS_RIGHT)         # crossing point of the ribs on the axis
DIAG_K = (INS_RIGHT[0][1] - CENTRE_Y) / INS_RIGHT[0][0]           # rib slope: centre -> front column
RIB_OFF = CH_WALL * (1 + DIAG_K ** 2) ** 0.5                      # vertical offset of a rib edge from its centre line (half width = wall)
POCKET_X = INS_RIGHT[0][0] - COL_R                                # X pocket half width = corner block face (tangent to the column)
SIDE_X = CH_IN_X - 5.0                                            # side pocket right edge = switch pad inner edge (pad 5 wide)
FRONT_RIB = 0.6                                                   # X pocket stops this far short of the front wall inner face
STOP_GAP = 0.2                                                    # rear X pocket stops this far in front of the stop wall face between the walls
POCKET_SKIN = 1.1                                                 # rear boxes stay this far from the rear wall and from the stop wall
CENTRE_Y0 = -30.0                                                 # centre rear box rear edge
REAR_R = 1.5                                                      # rear box corner R
# base seat
PAD_MARGIN = 0.3
PANEL_CLEARANCE = 0.2                  # rabbet = RV26 outline offset by this (print clearance)
