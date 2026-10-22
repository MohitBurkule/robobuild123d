"""Elevron 3.0 Alt chassis masters (ELVRN3.0_Alt chassis.SLDPRT dump + RVRN_revdev STEP `Alt_chassis`).

Part frame = the STEP assembly frame: X lateral, Y forward (weapon end), Z up from the chassis underside. Every value is a
designer dimension from the dump (DIM lines) or a relation of those; the dump names are in the comments.
"""
from robot.cad import fastener_catalog as fc

# ---- MASTER DESIGN PARAMETERS ----------------------------------------------------------------------------------------
CH_W, CH_L, CH_H = 59.0, 66.6, 17.0   # Sketch1 D2 x D1, Boss-Extrude1 D1: the printed block
WALL = 2.0                            # Sketch2 D2/D3 (walls) = deck thickness (Cut-Extrude1 stops at z 15)
AXLE_Y, AXLE_Z = 26.2, 8.5            # Sketch2 D... (wheelbase 52.4 = 2 x 26.2), N10 shaft height
POST_PITCH = (50.0, 32.0)             # Sketch2 D4 x D5: the 2 x 2 screw-column grid (Revron RV01 INS grid, same 32 pitch)
M3 = 3.0
# -----------------------------------------------------------------------------------------------------------------------
HX, HY = CH_W / 2, CH_L / 2           # outer half sizes (29.5, 33.3)
IN_X, IN_Y = HX - WALL, HY - WALL     # inner wall faces (27.5, 31.3)
DECK_Z = CH_H - WALL                  # deck underside (15)
EDGE_CH = WALL                        # Chamfer1: the top outer edges (and the rear plane carried over the tabs, Chamfer3)
CORNER_R = WALL                       # Fillet1: vertical front corners
# base-panel rebate (Cut-Extrude2 Sketch3 D1 = 1): the panel drops into a lip half a wall deep in, one wall tall
REBATE = WALL / 2
# screw columns (Cut-Extrude1 circles D6 = 2.9 tapping hole in a R3.1 column, Chamfer2/4 0.6 lead-ins)
PRINT_HOLE_ALLOW = 0.4               # FDM holes print undersize: tap drill 2.5 drawn 2.9
TAP_D = fc.tap_drill(M3) + PRINT_HOLE_ALLOW   # 2.9: printed M3 thread-forming hole
COL_R = 3.1                           # column radius round the tap hole
LEAD_CH = 0.6                         # Chamfer2 / Chamfer4
POSTS = tuple((sx * POST_PITCH[0] / 2, sy * POST_PITCH[1] / 2) for sx in (-1, 1) for sy in (-1, 1))
END_POST_Y = HY - WALL - 2.3          # Boss-Extrude4 (Sketch13 D1 = 58 between the two): end columns on the centre line, 29
END_POSTS = ((0.0, -END_POST_Y), (0.0, END_POST_Y))
# motor-bay cross walls (Sketch2 D1 10.2 x D9 23 bays, D8 2 wall, D7 5.4 return): one wall each side of the axle bay
BAY_LEN = 10.2                        # bay depth along Y from the end inner wall: cross wall at |y| 21.1 .. 19.1
BAY_X0 = (16.0, 19.6)                 # inner end of the cross wall (rear: N10 gearbox side, front: standoff side)
# axle keyholes through the side walls (Cut-Extrude3 Sketch4: D1 6 bore, D2 R1.8 slot, D3 4 drop)
KEY_R, KEY_SLOT_R, KEY_DROP = 3.0, 1.8, 4.0
# side boss (Boss-Extrude2 Sketch6 R5 obround, 3 out; Sketch5 D1 14 pitch, D2 3.2 holes; Sketch7 5.6 hex 2.5 deep; Fillet5 R3)
BOSS_R, BOSS_OUT, BOSS_PITCH = 5.0, 3.0, 14.0
BOSS_IN = 0.5                         # the obround also stands proud of the inner wall face (27.0)
HOLE_D = fc.clearance(M3, "close")    # 3.2 (Sketch5 D2)
NUT_CLR = 0.1
NUT_AF = fc.nut(M3)[0] + NUT_CLR      # 5.6 (Sketch7 D1): M3 nut pocket from the inside
NUT_DEPTH = 2.5                       # Cut-Extrude5 D1
BOSS_FILLET = 3.0
OCC_EPS = 1e-3                        # OCC fails a round that exactly meets a neighbouring face: drawn this much under
# boss window (Cut-Extrude15 Sketch19: D2 5 wide, D1 1.5 half slot, 4 deep, Fillet12 R1)
WIN_W, WIN_H, WIN_DEPTH, SLOT_HALF = 5.0, 7.0, 4.0, 1.5
# rear tabs (Boss-Extrude3 Sketch11 D1 10, D2 12, D3 4.5, D4 3.2; LPattern1 2 x 12; Mirror7)
TAB_W, TAB_PITCH, TAB_N = 6.0, 12.0, 2
TAB_X_OUT = HX                        # outer tab flush with the side wall
TAB_LEN = 8.0                         # beyond the rear face (to y 41.3)
TAB_HOLE_Z, TAB_HOLE_DY = 4.0, 4.9    # cross-bolt hole height, and its distance in from the rear face (y 38.2)
TAB_LEAD = 1.5                        # Chamfer5
# deck (Cut-Extrude6 Sketch8: D1 15 screw pitch, D2 1.7 pilots, D3 4 x D5 12 switch slot, D4 3 in from the wall)
SW_SLOT = (4.0, 12.0)
SW_SLOT_IN = 1.5                      # slot outer edge off the inner wall face (x 26)
SW_PITCH, SW_PILOT_D = 15.0, 1.7
# wire slot (Cut-Extrude17 Sketch21 D2 8, D1 R1.5, D3 6 off the left lattice edge)
WIRE_SLOT_X, WIRE_SLOT_L, WIRE_SLOT_R = -15.9, 8.0, 1.5
# deck lattice (Cut-Extrude7/14/16: 1 mm pockets from below, Fillet6 R2): X ribs between the columns
LAT_DEPTH = 1.0
LAT_RIB_C = COL_R                     # centre cells: rib half-width = column radius (window edge 3.1 off each rib line)
LAT_RIB_E = 2.05                      # end cells: Chamfer2 radius, the end ribs are lighter
LAT_END_X = 13.5                      # end triangle stops at the vert_mod upright inner face
LAT_CORNER_X = (BAY_X0[0] - 1.5, BAY_X0[1])   # corner pockets stop short of the axle-bay cross walls (rear, front)
LAT_R = 1.0                           # Fillet13 R1 (end and corner windows)
LAT_R_C = 2.0                         # Fillet6 R2 (centre windows)

__all__ = [n for n in dir() if not n.startswith("__")]
