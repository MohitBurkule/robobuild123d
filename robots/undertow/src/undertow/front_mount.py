"""Shared front interface: the pivot pin both front attachments hang on.

The interface IS the joint: axis along X through (0, PIN_Y, PIN_Z), carried by the two tub cheeks (tub.cheeks). An
attachment is any part whose own frame has its eye on the origin and its pin axis on X; it is placed by `mount_location`
and swung to its resting angle. The pin is a stocked M3x50 cap screw: head at the -X cheek outer face, nyloc in a
press-fit hex pocket in the boss on the +X cheek outer face.
"""
import build123d as bd

from robot.cad.holes import hole_tool

from .params import PIN_Y, PIN_Z, PIN_SCREW, CHEEK_HALF_X, CHEEK_T, NUT_BOSS_T


def pin_axis():
    """(origin, direction) of the pivot, robot frame."""
    return (0.0, PIN_Y, PIN_Z), (1.0, 0.0)


def mount_location(rest_deg):
    """Location of an attachment frame on the pin, tipped down `rest_deg` (positive = tip toward the floor)."""
    return bd.Pos(0, PIN_Y, PIN_Z) * bd.Rot(-rest_deg, 0, 0)


def pin_record():
    """Fastener record of the pivot screw: head at the -X cheek outer face, travelling +X, nyloc in the +X boss."""
    _, rec = hole_tool(at=(-(CHEEK_HALF_X + CHEEK_T / 2), PIN_Y, PIN_Z), axis=(1, 0, 0), fastener=PIN_SCREW,
                       head="cap", into="nut", grip=2 * CHEEK_HALF_X + CHEEK_T, nut_fit="press")
    return rec
