"""Front option (b): hinged TPU plough with a hardened-steel face, for horizontal spinners.
UNTESTED: never built, run, rendered or verified.

Made as really made: the body is a TPU prism (YZ wedge profile extruded along X, prints on its flat side, no supports)
with an eye round the common pin; the face is a 0.6 mm hardened-steel sheet, a flat cut blank bonded + screwed on the
sloped top of the body. Same pin, same cheeks, same rest logic as the forks (front_mount.py), so the swap is one setting.
Adversarial intent: a horizontal spinner's tooth meets a low, sloped steel face backed by PLOUGH_BODY_T of TPU: the
steel stops the tooth cutting, the TPU spreads the impulse and the hinge lets the whole plough kick up and come back
instead of passing the energy into the tub. Rounded side edges (PLOUGH_EDGE_R) leave no corner to snag.
"""
import build123d as bd

from .params import (PLOUGH_REACH, PLOUGH_BODY_T, PLOUGH_T_STEEL, PLOUGH_W, PLOUGH_REST_DEG, PLOUGH_EDGE_R, EYE_R, PIN_CLEAR)
from . import front_mount


def body_profile():
    """YZ section, plough frame: eye on the origin, lip at +Y on the face line Z = 0 (face = top of the body)."""
    wedge = bd.Polygon((0, -EYE_R), (PLOUGH_REACH, 0), (0, 0), align=None) + \
        bd.Polygon((0, -EYE_R), (PLOUGH_REACH * 0.6, -PLOUGH_BODY_T), (PLOUGH_REACH, 0), align=None)
    return wedge + bd.Circle(EYE_R) - bd.Circle(PIN_CLEAR / 2)


def body_local():
    b = bd.extrude(bd.Plane.YZ * body_profile(), PLOUGH_W / 2, both=True)
    return b.fillet(PLOUGH_EDGE_R, b.edges().filter_by(bd.Axis.Y))   # TODO: edge selection guessed; may need narrowing


def face_local():
    """Steel face: flat blank, constant thickness, lying on the body's top face (Z = 0 .. PLOUGH_T_STEEL)."""
    return bd.Pos(0, (EYE_R + PLOUGH_REACH) / 2, PLOUGH_T_STEEL / 2) * bd.Box(PLOUGH_W, PLOUGH_REACH - EYE_R, PLOUGH_T_STEEL)


def front():
    loc = front_mount.mount_location(PLOUGH_REST_DEG)
    return dict(plough_body=loc * body_local(), plough_face=loc * face_local())
