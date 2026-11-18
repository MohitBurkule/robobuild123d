"""Top and base plates: two identical-outline carbon laminate plates (the robot is invertible, both are "top").

Wheel windows are cut through the side edges of the plates (aligned with the tub notches), so once a plate is off the
wheels slide out sideways. M2 csk clearance holes at the bolt sites, switch access hole in BOTH plates.
"""
import build123d as bd

from robot.cad.holes import hole_tool

from . import tub
from .params import (Z_BASE, Z_TOP, PLATE_T, PLATE_HALF_W, PLATE_HALF_L, WELL, BOLT_SITES, PLATE_SCREW,
                     PLATE_HEAD, switch_hole_xy, switch_sky_xy, switch_sky_pins)


def _sheet(t):
    face = tub.outline(PLATE_HALF_W, PLATE_HALF_L)
    # wheel windows open through the +-X edges, aligned with the tub notches
    wx0, wx1 = WELL["x0"], PLATE_HALF_W + 2.0
    wy0, wy1 = WELL["y0"], WELL["y1"]
    # window: sharp corners at the plate edge (outside the outline anyway), radiused inner corners (kerf)
    win = bd.Pos((wx0 + wx1) / 2, (wy0 + wy1) / 2) * bd.Rectangle(wx1 - wx0, wy1 - wy0)
    for cy in (wy0, wy1):
        win = win + bd.Pos(wx0, cy) * bd.Circle(1.5)
    win = win + win.mirror(bd.Plane.YZ)
    win = win + win.mirror(bd.Plane.XZ) + win.mirror(bd.Plane.XZ).mirror(bd.Plane.YZ)
    face = face - win
    hx, hy, hr = switch_hole_xy()
    sx, sy, sr = switch_sky_xy()
    face = face - bd.Pos(hx, hy) * bd.Circle(hr) - bd.Pos(sx, sy) * bd.Circle(sr)
    for px, py, pr in switch_sky_pins():
        face = face - bd.Pos(px, py) * bd.Circle(pr)
    return bd.extrude(face, t)


def _screw_holes(plate, z_face, axis):
    """M2 csk clearance holes in the plate at the bolt sites (the tap is in the tub column). The cone meets the
    clearance cylinder exactly (no membrane ring at the far face) and the head seats 0.15 recessed - nothing
    protrudes past the skid face (joint.head_ground; a button head is 1.3 tall and can never recess in 1.0 plate)."""
    recs = []
    for x, y in BOLT_SITES:
        cut, rec = hole_tool(at=(x, y, z_face), axis=axis, fastener=PLATE_SCREW, head=PLATE_HEAD, into="through",
                             grip=PLATE_T)
        plate = plate - cut
        recs.append(rec)
    return plate, recs


def top_plate():
    p = bd.Pos(0, 0, Z_TOP - PLATE_T) * _sheet(PLATE_T)
    return _screw_holes(p, Z_TOP, (0, 0, -1))


def base_plate():
    p = bd.Pos(0, 0, Z_BASE) * _sheet(PLATE_T)
    return _screw_holes(p, Z_BASE, (0, 0, 1))
