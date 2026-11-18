"""Bolted titanium skirts on both sides and the rear.

Each 0.5 mm Ti gr5 plate seats flush on two printed pads on the tub flank and is held by 2x M2 button screws
(5 mm thread engagement into the pad), so it is real armour, not a hinge leaf: a horizontal spinner tooth meets a
bolted plate backed by the printed pad, and the lower edge sits SKIRT_BOT over the floor either way up.
"""
import build123d as bd

from robot.cad import fastener_catalog as fc

from .params import (SKIRT_T, SKIRT_X, SKIRT_REAR_Y, SKIRT_BOT, SKIRT_TOP, SKIRT_SIDE_LEN, SKIRT_REAR_LEN,
                     SKIRT_PAD_Y, REAR_PAD_X, SKIRT_PAD_Z0, SKIRT_PAD_Z1, SKIRT_SCREW)

HOLE_R = fc.clearance(fc.parse(SKIRT_SCREW).d, "normal") / 2   # button head: plain clearance hole through the skirt


def _side_skirt(sx=1):
    """Side skirt plate: vertical, seated on the pads, clearance holes at the pad centres."""
    zc = (SKIRT_PAD_Z0 + SKIRT_PAD_Z1) / 2
    h = SKIRT_TOP - SKIRT_BOT
    plate = bd.Pos(sx * SKIRT_X, 0, SKIRT_BOT) * bd.Box(SKIRT_T, SKIRT_SIDE_LEN, h,
                                                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for sy in (1, -1):
        plate = plate - bd.Pos(sx * SKIRT_X, sy * SKIRT_PAD_Y, zc) * bd.Rot(0, 90, 0) * bd.Cylinder(HOLE_R, SKIRT_T + 1)
    return plate


def _rear_skirt():
    """Rear skirt plate: same section, on the rear flank, holes at the rear pad centres."""
    zc = (SKIRT_PAD_Z0 + SKIRT_PAD_Z1) / 2
    h = SKIRT_TOP - SKIRT_BOT
    plate = bd.Pos(0, SKIRT_REAR_Y, SKIRT_BOT) * bd.Box(SKIRT_REAR_LEN, SKIRT_T, h,
                                                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for sx in (1, -1):
        plate = plate - bd.Pos(sx * REAR_PAD_X, SKIRT_REAR_Y, zc) * bd.Rot(90, 0, 0) * bd.Cylinder(HOLE_R, SKIRT_T + 1)
    return plate


def skirts():
    return dict(skirt_r=_side_skirt(1), skirt_l=_side_skirt(-1), skirt_rear=_rear_skirt())
