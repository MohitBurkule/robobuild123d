"""Drive: four catalogue gearmotors + wheels, one corner built and mirrored.

Adversarial intent: motors sit inside the printed tub, backed by the spine ribs; the wheels are inside the plan
outline and proud of both plates by WHEEL_PROUD, so the robot drives either way up and a vertical spinner that flips
it gains nothing. The shaft carries only the wheel (direct drive, D-bore press fit).
"""
import build123d as bd

from robot import catalog

from . import hw   # catalogue-derived solids / placement (src/undertow/hw.py)

from .params import MOTOR_ID, WHEEL_ID, X_MOTOR_BACK, X_WHEEL_C, Y_AXLE, Z_AXLE

QUADRANTS = ((1, 1), (-1, 1), (1, -1), (-1, -1))   # (sx, sy): +X/+Y is the built corner, the rest are mirrors


def motor_pose(sx, sy):
    """Spec `at` / `rot` of a corner motor. Catalogue frame: shaft on +X, origin on the axis at the back face.
    The motor back face sits on the spine at X_MOTOR_BACK; the shaft points outboard."""
    r = hw.reach(MOTOR_ID)
    x_origin = X_MOTOR_BACK - r["x0"]           # back face (bbox x0) onto the spine
    return (sx * x_origin, sy * Y_AXLE, Z_AXLE), (0.0, 0.0, 0.0 if sx > 0 else 180.0)


def wheel_pose(sx, sy):
    """Wheel centred on X_WHEEL_C on the motor axis (catalogue wheel frame: axis on X, centred)."""
    return (sx * X_WHEEL_C, sy * Y_AXLE, Z_AXLE), (0.0, 0.0, 0.0 if sx > 0 else 180.0)


def motors():
    return [hw.placed(MOTOR_ID, *motor_pose(sx, sy)) for sx, sy in QUADRANTS]


def wheels():
    return [hw.placed(WHEEL_ID, *wheel_pose(sx, sy)) for sx, sy in QUADRANTS]


def motor_terminal_world(sx, sy):
    """World position of the motor's terminals port (local [-12.75, 0, 0] on the back face)."""
    at, rot = motor_pose(sx, sy)
    p = catalog.find(MOTOR_ID).ports["terminals"]
    v = bd.Vertex(*p)
    loc = bd.Pos(*at) * bd.Rot(*rot)
    w = loc * v
    return (w.X, w.Y, w.Z)
