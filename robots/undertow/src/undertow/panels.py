"""Top and base plates: two identical-outline carbon laminate plates (the robot is invertible, both are "top").
UNTESTED: never built, run, rendered or verified.

Made as really made: a 2D profile (tub outline, wheel windows, holes) water-jet / CNC cut from constant-thickness sheet.
Adversarial intent: a vertical spinner landing on top meets a stiff, slick plate clamped over a TPU spring (the
plate spreads the hit, the TPU absorbs it); holes are only where a part needs them (wheel windows, switch access,
M2 CSK flush heads: nothing sticks up for a tooth to catch).
"""
import build123d as bd

from robot.cad.holes import hole_tool   # catalogue CSK clearance + head recess

from . import tub
from .params import (Z_BASE, Z_TOP, PLATE_T_TOP, PLATE_T_BASE, WELL, SWITCH_X, SWITCH_Y, SWITCH_ACCESS_R, PLATE_SCREW, PLATE_HEAD)


def _sheet(t):
    face = tub.outline()
    win = bd.Pos((WELL["x0"] + WELL["x1"]) / 2, (WELL["y0"] + WELL["y1"]) / 2) * bd.Rectangle(WELL["x1"] - WELL["x0"], WELL["y1"] - WELL["y0"])
    wins = [win, win.mirror(bd.Plane.YZ)]
    wins += [w.mirror(bd.Plane.XZ) for w in wins]
    face = face - wins[0] - wins[1] - wins[2] - wins[3]
    face = face - bd.Pos(SWITCH_X, SWITCH_Y) * bd.Circle(SWITCH_ACCESS_R)
    return bd.extrude(face, t)


def _screw_holes(plate, z_face, axis):
    _, pts = tub._standoff_bores()
    recs = []
    for x, y in pts:
        cut, rec = hole_tool(at=(x, y, z_face), axis=axis, fastener=PLATE_SCREW, head=PLATE_HEAD, into="through",
                             grip=PLATE_T_TOP)
        plate = plate - cut
        recs.append(rec)
    return plate, recs


def top_plate():
    p = bd.Pos(0, 0, Z_TOP - PLATE_T_TOP) * _sheet(PLATE_T_TOP)
    return _screw_holes(p, Z_TOP, (0, 0, -1))


def base_plate():
    p = bd.Pos(0, 0, Z_BASE) * _sheet(PLATE_T_BASE)
    return _screw_holes(p, Z_BASE, (0, 0, 1))
