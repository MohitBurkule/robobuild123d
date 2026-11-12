"""Shared front interface: the pivot pin both front attachments hang on. UNTESTED: never built, run, rendered or verified.

The interface IS the joint: axis along X through (0, PIN_Y, PIN_Z), carried by the two tub cheeks (tub.cheeks). An
attachment is any part whose own frame has its eye on the origin and its pin axis on X; it is placed by `mount_joint`
and swung to its resting angle. Swapping forks <-> plough changes only `settings.front`; pin, cheeks, holes and the
tub are untouched. The pin is a catalogue M3 cap screw (robot/cad/fastener_catalog.py) with a nyloc at the far cheek.
"""
import build123d as bd

from robot.cad.holes import hole_tool

from .params import PIN_Y, PIN_Z, PIN_SCREW, CHEEK_HALF_X, CHEEK_T


def pin_axis():
    """(origin, direction) of the pivot, robot frame."""
    return (0.0, PIN_Y, PIN_Z), (1.0, 0.0, 0.0)


def mount_location(rest_deg):
    """Location of an attachment frame on the pin, tipped down `rest_deg` (positive = tip toward the floor)."""
    return bd.Pos(0, PIN_Y, PIN_Z) * bd.Rot(-rest_deg, 0, 0)


def mount_joint(part, label="front_pin"):
    """build123d RevoluteJoint on the tub side (the attachment connects its own RigidJoint at its eye to this)."""
    return bd.RevoluteJoint(label=label, to_part=part, axis=bd.Axis((0, PIN_Y, PIN_Z), (1, 0, 0)), angular_range=(-180, 180))


def pin_record():
    """Fastener record of the pivot screw: head at the -X cheek outer face, travelling +X, nyloc at the +X cheek."""
    _, rec = hole_tool(at=(-(CHEEK_HALF_X + CHEEK_T / 2), PIN_Y, PIN_Z), axis=(1, 0, 0), fastener=PIN_SCREW, head="cap",
                       into="nut", grip=2 * CHEEK_HALF_X + CHEEK_T)
    return rec
