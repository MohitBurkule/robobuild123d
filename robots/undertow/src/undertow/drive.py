"""Drive: four catalogue gearmotors + wheels, one corner built and mirrored. UNTESTED: never built, run, rendered or verified.

Adversarial intent: motors sit fully inside the TPU tub (a spinner reaches only TPU wall, skirt or plate); the wheels are
inside the plan outline and proud of both plates by WHEEL_PROUD, so the robot drives either way up and a vertical
spinner that flips it gains nothing. The shaft carries only the wheel (direct drive): a side hit loads the tub wall,
not the shaft, because the wall is WHEEL_RUN outside the tyre and the wheel well sides carry the motor plate stack.
"""
import build123d as bd

from robot.cad.bay import derive_bay
from robot import catalog

import revron.hw as hw   # catalogue-derived solids / placement (robots/revron/src/revron/hw.py)

from .params import (MOTOR_ID, WHEEL_ID, X_MOTOR_BACK, X_WHEEL_C, Y_AXLE, Z_AXLE, MOTOR_FIT)

QUADRANTS = ((1, 1), (-1, 1), (1, -1), (-1, -1))   # (sx, sy): +X/+Y is the built corner, the rest are mirrors


def motor_pose(sx, sy):
    """Spec `at` / `rot` of a corner motor. Catalogue frame: shaft on +X (robot/catalog.py), origin from hw.reach().
    The motor back face sits on the spine at X_MOTOR_BACK; the shaft points outboard."""
    r = hw.reach(MOTOR_ID)
    x_origin = X_MOTOR_BACK - r["x0"]           # back face (bbox x0) onto the spine
    return (sx * x_origin, sy * Y_AXLE, Z_AXLE), (0.0, 0.0, 0.0 if sx > 0 else 180.0)


def wheel_pose(sx, sy):
    """Wheel centred on X_WHEEL_C on the motor axis (catalogue wheel frame: axis on X, centred)."""
    return (sx * X_WHEEL_C, sy * Y_AXLE, Z_AXLE), (0.0, 0.0, 0.0 if sx > 0 else 180.0)


def motor_bay(sx, sy):
    """Pocket the motor drops into from the top (robot/cad/bay.py:derive_bay): swept to the top face, never trapped."""
    at, rot = motor_pose(sx, sy)
    return derive_bay(catalog.find(MOTOR_ID), placement=bd.Pos(*at) * bd.Rot(*rot), clearance=MOTOR_FIT, insert_dir="-z")


def motors():
    return [hw.placed(MOTOR_ID, *motor_pose(sx, sy)) for sx, sy in QUADRANTS]


def wheels():
    return [hw.placed(WHEEL_ID, *wheel_pose(sx, sy)) for sx, sy in QUADRANTS]
