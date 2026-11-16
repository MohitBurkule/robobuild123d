"""Top panel (the tension skin the weapon boss hangs from); Revron fastening (M2 button into the tub wall tops,
the same call Revron's panel_top.seat uses).

Top panel: 1 mm printed PA-CF (Ti 0.5 is the upgrade if mass allows), outline = tub outline at the top (sloped
inset), drilled for the stator screws (catalogue circle) + rim screws (6 on the disc wall, 4 on the pod walls) +
switch access hole. The rim screws thread straight into the printed wall tops (thread-forming, like the Revron
top panel): the wall is 2 mm wide so the button head bears on the panel skin over the cavity edge, which is fine
because the skin is continuous.
"""
import math

import build123d as bd

from . import params as P
from . import tub
from ._reuse import weapon_motor

SWITCH_HOLE_D = 4.0     # mm hex-key access to the FingerTech mini switch (tool-free rule: key on a lanyard)
PANEL_SCREW_CLR_R = 1.1  # M2 normal clearance (fastener_catalog.clearance(2) = 2.4 dia would not fit the 2 mm wall)


def rim_r():
    """Radius of the disc wall centre at the panel (the screws thread into the 2 mm wall top)."""
    return P.TUB_R - tub._slope_inset(tub.height()) - P.TUB_WALL / 2


def disc_angles():
    """Six rim angles avoiding the plan sector where the rear pod swallows the disc wall (237..303 deg)."""
    return [20.0, 70.0, 110.0, 160.0, 215.0, 325.0]


def pod_screw_x():
    """Pod wall centre x at the panel."""
    return P.POD_W / 2 - tub._slope_inset(tub.height()) - P.TUB_WALL / 2


def rim_xy():
    """World (x, y) of every panel rim screw: 6 on the disc wall + 2 on each pod wall."""
    pts = [(rim_r() * math.cos(math.radians(a)), P.WPN_AXIS_Y + rim_r() * math.sin(math.radians(a)))
           for a in disc_angles()]
    for y in (-55.0, -25.0):
        pts.append((pod_screw_x(), y))
        pts.append((-pod_screw_x(), y))
    return pts


def top_panel():
    inset = tub._slope_inset(tub.height())
    face = tub.outline(-inset).faces()[0]
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    for r, deg, d in m["base_holes"]:
        face -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg))) * bd.Circle(d / 2 + 0.1)
    for x, y in rim_xy():
        face -= bd.Pos(x, y) * bd.Circle(PANEL_SCREW_CLR_R)
    face -= bd.Pos(0, P.wheel_y()) * bd.Circle(SWITCH_HOLE_D / 2)
    return bd.Pos(0, 0, P.TUB_TOP_Z - P.TOP_PANEL_T) * bd.extrude(face, P.TOP_PANEL_T)
