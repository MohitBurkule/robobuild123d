"""Ripsaw top and base panels: printed nylon sheets on M2 screws into the tub's heat-set inserts. UNTESTED.
Revron's panel_base / panel_top are tied to Revron's tub outline, so only the shared plate helpers are reused here.
The top panel has a hole over the switch (tool-free access, AWS) and a cut-out for the rails/disc slot."""
import build123d as bd

from . import params as P
from . import tub as T
from ._reuse import plate
from robot.cad import fastener_catalog as FC


def _sheet(t, z0):
    s = bd.extrude(bd.Plane.XY.offset(z0) * T._outline(), t)
    for x, y in T.insert_points():
        s = s - bd.Pos(x, y, z0 + t / 2) * bd.Cylinder(FC.clearance(P.PANEL_SCREW) / 2, 2 * t)
    rail_gap = bd.Pos((P.RAIL_L_X[0] + P.RAIL_R_X[1]) / 2, P.TUB_Y1, z0 + t / 2) * \
        bd.Box(P.RAIL_R_X[1] - P.RAIL_L_X[0], 2 * P.RAIL_L, 2 * t)
    return s - rail_gap


def base_panel():
    s = _sheet(P.PANEL_T_BASE, P.TUB_FLOOR_Z - P.PANEL_T_BASE)
    s.label = "panel_base"
    return s


def top_panel():
    s = _sheet(P.PANEL_T_TOP, P.TUB_TOP_Z)
    sw = T.bay_locations()[P.SWITCH].position
    s = s - bd.Pos(sw.X, sw.Y, P.TUB_TOP_Z) * bd.Cylinder(P.SW_W / 3, 3 * P.PANEL_T_TOP)   # switch key access
    s.label = "panel_top"
    return s
