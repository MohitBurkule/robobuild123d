"""Turned 7075 hub between the GR1507 bell cap and the bar. UNTESTED.

Made as: lathe-turned disc, bored to the shaft (slide fit), drilled through on the bell-top screw circle read from
revron weapon_motor.describe('gr1507')['top_holes'] (never retyped), tapped M3 x BAR_BOLT_N for the bar.
Load path: bar -> 2x M3 (shear) + shaft pilot (radial) -> hub -> bell-top M2 screws (torque) -> bell -> motor bearings.
Part frame: axis on Z, bar face at z = 0, bell face at z = HUB_H (hub sits ABOVE the bar, motor is shaft-down above it).
"""
import math

import build123d as bd

from . import params as P
from ._reuse import plate, weapon_motor


def motor():
    return weapon_motor.describe(P.WEAPON_MOTOR)


def profile():
    m = motor()
    face = bd.Circle(P.HUB_OD / 2) - bd.Circle(m["shaft_r"] + P.HUB_SHAFT_CLR)
    for r, deg, d in m["top_holes"]:                                  # bell-top screws, catalogue circle and phase
        face -= bd.Pos(r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg))) * bd.Circle(d / 2 + 0.1)
    from robot.cad.fastener_catalog import tap_drill
    for h in plate.holes(tap_drill(P.BAR_BOLT_D) / 2, P.BAR_BOLT_PCD / 2, P.BAR_BOLT_N, phase=0.0):   # M3 tapped
        face -= h
    return face


def hub():
    return bd.extrude(profile(), P.HUB_H)
