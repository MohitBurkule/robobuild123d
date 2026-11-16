"""Top panel (the tension skin the weapon boss hangs from); Revron fastening (M2 button into printed posts).

Top panel: 1 mm printed PA-CF, outline = the tub top outline grown by PANEL_OVERHANG so every screw head and hole
sits fully on the skin. Drilled for: the stator flange screws (the bl_1806's 16 mm tap circle), the rim screws
(into the printed posts), the switch key hole and the weapon-lock pin hole (over the bar's lock hole, so the pit
pin reaches through panel, floor and bar down to the floor slab). The rim screws thread straight into the printed
posts (thread-forming, like the Revron top panel): the 1.5 mm wall tops are too thin to take a screw directly.
"""
import math

import build123d as bd

from . import params as P
from . import tub

SWITCH_HOLE_D = 4.0     # mm hex-key access to the FingerTech mini switch (tool-free rule: key on a lanyard)
PANEL_SCREW_CLR_R = 1.1  # M2 normal clearance
SWITCH_KEY_OFF_X = 3.175  # mm: the switch's mounting bushing sits this far +X of its centre at rot 270


def rim_xy():
    """World (x, y) of every panel rim screw = the post centres (tub.post_xy)."""
    return tub.post_xy()


def top_panel():
    face = tub.top_outline(P.PANEL_OVERHANG).faces()[0]
    for k in range(4):
        a = math.radians(90.0 * k)
        face -= bd.Pos(P.BL_SCREW_PCD / 2 * math.cos(a), P.WPN_AXIS_Y + P.BL_SCREW_PCD / 2 * math.sin(a)) * bd.Circle(1.1)
    for x, y in rim_xy():
        face -= bd.Pos(x, y) * bd.Circle(PANEL_SCREW_CLR_R)
    face -= bd.Pos(SWITCH_KEY_OFF_X, P.switch_y()) * bd.Circle(SWITCH_HOLE_D / 2)
    face -= bd.Pos(P.BAR_LOCK_X, P.WPN_AXIS_Y) * bd.Circle(P.BAR_LOCK_D / 2 + 0.2)
    return bd.Pos(0, 0, P.TUB_TOP_Z - P.TOP_PANEL_T) * bd.extrude(face, P.TOP_PANEL_T)
