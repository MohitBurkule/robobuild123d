"""Front option (b): hinged TPU plough with a hardened-steel face, for horizontal spinners. Same pin, same cheeks."""
import build123d as bd

from .params import (PLOUGH_REACH, PLOUGH_BODY_T, PLOUGH_T_STEEL, PLOUGH_W, PLOUGH_REST_DEG, EYE_R, PIN_CLEAR)
from . import front_mount


def body_profile():
    """YZ section, plough frame: eye on the origin, lip at +Y on the face line Z = 0."""
    wedge = bd.Polygon((0, -EYE_R), (PLOUGH_REACH, 0), (0, 0), align=None) + \
        bd.Polygon((0, -EYE_R), (PLOUGH_REACH * 0.6, -PLOUGH_BODY_T), (PLOUGH_REACH, 0), align=None)
    return wedge + bd.Circle(EYE_R) - bd.Circle(PIN_CLEAR / 2)


def body_local():
    return bd.extrude(bd.Plane.YZ * body_profile(), PLOUGH_W / 2, both=True)


def face_local():
    """Steel face: flat blank on the body's top face (Z = 0 .. PLOUGH_T_STEEL)."""
    return bd.Pos(0, (EYE_R + PLOUGH_REACH) / 2, PLOUGH_T_STEEL / 2) * bd.Box(PLOUGH_W, PLOUGH_REACH - EYE_R, PLOUGH_T_STEEL)


def front():
    loc = front_mount.mount_location(PLOUGH_REST_DEG)
    return dict(plough_body=loc * body_local(), plough_face=loc * face_local())
