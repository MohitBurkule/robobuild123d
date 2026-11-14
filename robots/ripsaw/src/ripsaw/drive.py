"""Ripsaw drive: 2WD N10 gearmotors, catalogue wheels inside the tub outline, rear-biased. Build the right side, mirror.
UNTESTED. Adversarial intent: the side wall stands outside the tyre (WHEEL_GAP + WALL), so a horizontal spinner meets
nylon, not tread; the gearmotor sits in a closed pocket, its shaft through a wall slot."""
import build123d as bd

from . import params as P
from ._reuse import hw


def wheel_at(side=1):
    """World location of a wheel centre, axis along X; side +1 right, -1 left (mirror of the right)."""
    return bd.Location((side * P.WHEEL_X, P.WHEEL_Y, P.WHEEL_Z), (0, 90 * side, 0))


def motor_at(side=1):
    """Gearmotor along X inboard of its wheel, shaft outward (catalogue +X = shaft direction assumed, see risks)."""
    x = side * (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2)
    return bd.Location((x, P.WHEEL_Y, P.WHEEL_Z), (0, 0, 0 if side > 0 else 180))


def wheel_well(side=1):
    """Cut in the tub for one wheel: tyre + WHEEL_GAP, open at floor and top so the tyre stands proud both ways up."""
    box = bd.Box(P.WHEEL_W + 2 * P.WHEEL_GAP, P.WHEEL_OD + 2 * P.WHEEL_GAP, P.WHEEL_OD + 2 * P.WHEEL_GAP)
    return bd.Pos(side * P.WHEEL_X, P.WHEEL_Y, P.WHEEL_Z) * box


def motor_pocket(side=1):
    """Pocket for the gearmotor body (the catalogue solid, placed): tub.py subtracts it."""
    loc = motor_at(side)
    return hw.placed(P.DRIVE_MOTOR, tuple(loc.position), tuple(loc.orientation))


def wells_and_pockets():
    right = [wheel_well(1), motor_pocket(1)]
    return right + [bd.mirror(s, about=bd.Plane.YZ) for s in right]
