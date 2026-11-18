"""Turned 7075 hub between the bl_1806 bell cap and the bar.

Made as: lathe-turned disc (axisymmetric), bored for the motor's 3 mm shaft, its top 2 mm opened up into a cup that
pilots on the bell's cap rim; drilled through and tapped M2.5 x 2 for the bar screws (the cross taps are declared
secondary ops). The stack is clamped: the M3 nut on the shaft's threaded lower end pulls the hub (and the bar, bolted
to it) up against the bell cap face, so the bell drives the whole rotor through the clamped faces and the shaft's own
press fit in the bell core. Load path: hit -> bar -> 2x M2.5 (shear) + shaft pilot (radial) -> hub -> bell cap face
(clamp) -> motor bearings.
Part frame: axis on Z, bar face at z = 0, bell face at z = HUB_H (hub sits ABOVE the bar, motor above it).
"""
import math

import build123d as bd

from . import params as P
from ._reuse import plate


def profile():
    face = bd.Circle(P.HUB_OD_R) - bd.Circle(P.HUB_BORE_R)
    from robot.cad.fastener_catalog import tap_drill
    for h in plate.holes(tap_drill(P.BAR_BOLT_D) / 2, P.BAR_BOLT_PCD / 2, P.BAR_BOLT_N, phase=0.0):   # M2.5 taps
        face -= h
    return face


def hub():
    solid = bd.extrude(profile(), P.HUB_H)
    cup = bd.Pos(0, 0, P.HUB_H - P.HUB_CUP_H) * bd.Cylinder(P.HUB_CUP_ID_R, P.HUB_CUP_H + 1,
                                                            align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return solid - cup
