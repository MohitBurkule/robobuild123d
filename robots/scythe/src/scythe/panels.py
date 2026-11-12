"""Top panel (the tension skin the weapon boss hangs from) and pod base panel; Revron fastening (M2 CSK/button into
heat-sets, robot/cad/holes.hole_tool, the same call Revron's panel_top.seat uses). UNTESTED.

Top panel: 1 mm printed PA-CF (Ti 0.5 is the upgrade if mass allows), outline = tub outline at the top (sloped
inset), drilled for the stator screws (catalogue circle) + PANEL_SCREW_N rim screws (PolarLocations on the disc) +
switch access hole. Base panel: pod only (the disc floor is printed in with the tub so the bar side has no seam).
"""
import math

import build123d as bd
from robot.cad.holes import hole_tool

from . import params as P
from . import tub
from ._reuse import weapon_motor

SWITCH_HOLE_D = 4.0     # mm hex-key access to the FingerTech mini switch (tool-free rule: key on a lanyard)


def rim_xy():
    r = P.TUB_R - tub._slope_inset(tub.height()) - 2 * P.TUB_WALL
    return [(loc.position.X, loc.position.Y + P.WPN_AXIS_Y) for loc in bd.PolarLocations(r, P.PANEL_SCREW_N)]


def seat(i):
    """FastenerRecord of rim screw i, as Revron panel_top.seat (button head on the sheet, clearance through)."""
    x, y = rim_xy()[i]
    return hole_tool((x, y, P.TUB_TOP_Z), (0, 0, -1), "M2x6", head="button", into="through", side="head", grip=P.TOP_PANEL_T, cbore=0)


def top_panel():
    inset = tub._slope_inset(tub.height())
    face = tub.outline(-inset).faces()[0]
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    for r, deg, d in m["base_holes"]:
        face -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg))) * bd.Circle(d / 2 + 0.1)
    for x, y in rim_xy():
        face -= bd.Pos(x, y) * bd.Circle(1.1)       # M2 normal clearance (fastener_catalog.clearance(2) = 2.2)
    face -= bd.Pos(0, P.wheel_y()) * bd.Circle(SWITCH_HOLE_D / 2)
    return bd.Pos(0, 0, P.TUB_TOP_Z - P.TOP_PANEL_T) * bd.extrude(face, P.TOP_PANEL_T)
