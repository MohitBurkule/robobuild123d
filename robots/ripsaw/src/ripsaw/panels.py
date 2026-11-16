"""Ripsaw top and base panels: printed nylon sheets on M2 screws into the tub's side-wall bosses. UNTESTED.
The base panel carries the N10 cradle pedestals (the motors drop in from below with the panel off); the top panel
has a keyway over the switch (tool-free access, AWS) and a slot clearing the weapon sweep."""
import build123d as bd

from . import params as P
from . import tub as T
from ._reuse import plate
from robot.cad import fastener_catalog as FC


def _screw_axes():
    return [(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy * P.PANEL_SCREW_Y) for sx in (1, -1) for sy in (1, -1)]


def _sheet(t, z0):
    s = bd.extrude(bd.Plane.XY.offset(z0) * T._outline(), t)
    for x, y in _screw_axes():
        s = s - bd.Pos(x, y, z0 + t / 2) * bd.Cylinder(FC.clearance(P.PANEL_SCREW) / 2, 2 * t)
    return s


def motor_pedestals():
    """Pads on the base panel the N10s rest on: can pad to the can's underside (z 9), gearbox pad to z 10."""
    out = []
    for side in (1, -1):
        mx = side * (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2)
        can0, can1 = mx - 12.75, mx + 2.25          # catalogue can span in the gearmotor frame
        gb0, gb1 = mx + 2.25, mx + 11.25           # gearbox span
        out.append(bd.Pos((can0 + can1) / 2, P.WHEEL_Y, P.TUB_FLOOR_Z + (9.0 - P.TUB_FLOOR_Z) / 2)
                   * bd.Box(can1 - can0 - 5.0, 8.0, 9.0 - P.TUB_FLOOR_Z))
        out.append(bd.Pos((gb0 + gb1) / 2, P.WHEEL_Y, P.TUB_FLOOR_Z + (10.0 - P.TUB_FLOOR_Z) / 2)
                   * bd.Box(gb1 - gb0 - 1.0, 8.0, 10.0 - P.TUB_FLOOR_Z))
    return out


def base_panel():
    s = _sheet(P.PANEL_T_BASE, P.TUB_FLOOR_Z - P.PANEL_T_BASE)
    for p in motor_pedestals():
        s = s + p
    s.label = "panel_base"
    return s


def top_panel():
    s = _sheet(P.PANEL_T_TOP, P.TUB_TOP_Z)
    sw = P.SW_AT
    s = s - bd.Pos(sw[0], sw[1], P.TUB_TOP_Z + P.PANEL_T_TOP / 2) * bd.Cylinder(P.SW_W / 3, 3 * P.PANEL_T_TOP)
    sweep = bd.Pos(0, (P.TUB_Y1 + 20.5) / 2, P.TUB_TOP_Z + P.PANEL_T_TOP / 2) \
        * bd.Box(2 * (P.DISC_T / 2 + P.MOVING_CLR + 0.1), P.TUB_Y1 - 20.5, 2 * P.PANEL_T_TOP)
    s = s - sweep
    s = s - bd.Pos(-14.5, P.TUB_Y1 - 1.0, P.TUB_TOP_Z + P.PANEL_T_TOP / 2) \
        * bd.Box(4.2, 3.0, 2 * P.PANEL_T_TOP + 0.4)   # phase-lead cable notch, matches the tub wall notch
    s.label = "panel_top"
    return s
    s.label = "panel_top"
    return s
