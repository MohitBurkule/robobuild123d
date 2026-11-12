"""2WD drive: N10 1000 rpm gearmotors + BBB 34 x 6.5 wheels, rear pod, right side built and mirrored. UNTESTED.

The parts are catalogue solids (revron hw.placed); this file only decides WHERE, from params relations:
wheel centre X = pod half width + half tyre, Y = P.wheel_y() (tyre footprint at bar-top height sits BAR_TYRE_CLR
outside the bar sweep), Z = wheel radius (axle at mid body height -> same ride both ways up: invertible).
Adversarial intent: the tyres are behind the sweep circle so our own bar never touches them; a horizontal opponent
reaches only the tyre's rear quarter, which is inside the footprint of the pod corners.
"""
from . import params as P
from ._reuse import hw


def wheel_pose(side=1):
    return (side * P.wheel_x(), P.wheel_y(), P.WHEEL_CZ), (0.0, 0.0, 0.0 if side > 0 else 180.0)


def motor_pose(side=1):
    """Gearmotor shaft pointing outboard (+X on the right), body inside the pod; catalogue frame x along the shaft."""
    L, _, _ = hw.size(P.DRIVE_MOTOR)
    x = side * (P.POD_W / 2 - P.TUB_WALL - L / 2)
    return (x, P.wheel_y(), P.WHEEL_CZ), (0.0, 0.0, 0.0 if side > 0 else 180.0)


def parts():
    out = {}
    for name, side in (("r", 1), ("l", -1)):
        at, rot = wheel_pose(side)
        out[f"wheel_{name}"] = hw.placed(P.WHEEL, at, rot)
        at, rot = motor_pose(side)
        out[f"drive_motor_{name}"] = hw.placed(P.DRIVE_MOTOR, at, rot)
    return out
