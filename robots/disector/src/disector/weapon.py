"""Overhead hammer-saw arm, toothed saw disc, and locking bar for Disector."""

from __future__ import annotations

import math
import build123d as bd
from . import params as P


def build_arm() -> bd.Solid:
    """Dark-green curved overhead hammer-saw arm from servo pivot to weapon motor mount."""
    py, pz = P.ARM_PIVOT[1], P.ARM_PIVOT[2]
    ty, tz = P.ARM_TIP[1], P.ARM_TIP[2]
    r = P.ARM_HEAD_R
    # Curved arm profile in Y-Z plane (extruded X in [-ARM_HALF_T, +ARM_HALF_T])
    pts = [
        (py - P.ARM_BASE_HALF_Y, pz - P.ARM_BASE_DZ),
        (py + P.ARM_BASE_HALF_Y, pz - P.ARM_BASE_DZ),
        P.ARM_MID_FRONT,
        (ty + r, tz - r),
        (ty + r, tz + r),
        (ty - r, tz + r),
        P.ARM_MID_BACK,
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
            bd.fillet(bd.vertices(), P.ARM_FILLET)
        bd.extrude(amount=P.ARM_HALF_T, both=True)
    arm = bp.part.solids()[0]
    # Shaft clearance hole at the tip
    arm = arm.cut(bd.Solid.make_cylinder(P.ARM_BORE_R, 2 * P.ARM_HALF_T + 2.0,
                                         bd.Plane(origin=(-P.ARM_HALF_T - 1.0, ty, tz), z_dir=(1, 0, 0))))
    # Blind socket the locking-bar pin plugs into (radial clearance, stops short of the far face)
    sock = bd.Solid.make_cylinder(P.LOCK_PIN_R + P.SOCKET_CLR, P.LOCK_PIN_DEPTH,
                                  bd.Plane(origin=(-P.ARM_HALF_T, P.LOCK_PIN_Y, P.LOCK_PIN_Z), z_dir=(1, 0, 0)))
    return arm.cut(sock).clean()


def build_weapon_shaft() -> bd.Solid:
    """GR1507 5 mm threaded steel motor shaft (29.1 mm total, 8 mm M5 thread), built in the motor frame."""
    p, r, dr, ch = P.SHAFT_PITCH, P.SHAFT_R, P.SHAFT_THREAD_DEPTH, P.SHAFT_CHAMFER
    prof = [(0.0, 0.0), (0.0, r - dr - ch), (ch, r - dr)]
    for k in range(int(round(P.SHAFT_THREAD_LEN / p))):
        x = ch + k * p
        prof += [(x + p / 2.0, r), (x + p, r - dr)]
    prof += [(P.SHAFT_THREAD_LEN, r), (P.SHAFT_LEN, r), (P.SHAFT_LEN, 0.0)]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(P.SHAFT_END_X - x, 0.0, z) for x, z in prof], close=True))
    return bd.Solid.revolve(face, 360.0, bd.Axis((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))).clean()


def _disc_hole_angles():
    phase = math.radians(P.DISC_HOLE_PHASE)
    return [phase + k * math.pi / 2 for k in range(4)]


def build_disc() -> bd.Solid:
    """44 mm OD, 1.0 mm thick titanium circular saw disc with 4 hooked teeth."""
    r_out = P.DISC_R
    r_root = P.DISC_R - P.DISC_ROOT_DEPTH
    a_back, a_tip, a_gullet = P.DISC_TOOTH_ANGLES
    pts = []
    for k in range(P.DISC_TEETH):
        a0 = 2 * math.pi * k / P.DISC_TEETH
        pts.append((r_root * math.cos(a0), r_root * math.sin(a0)))
        pts.append((r_out * math.cos(a0 + a_back), r_out * math.sin(a0 + a_back)))
        pts.append((r_out * math.cos(a0 + a_tip), r_out * math.sin(a0 + a_tip)))
        pts.append((r_root * math.cos(a0 + a_gullet), r_root * math.sin(a0 + a_gullet)))

    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.XY):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
            bd.fillet(bd.vertices(), P.DISC_FILLET)
        bd.extrude(amount=P.DISC_T / 2, both=True)
    disc = bp.part.solids()[0]
    # Centre bore for the GR1507 5 mm shaft, and 4x M2 clearance holes on the 9 mm PCD (matching the GR1507 top holes)
    thru = P.DISC_T + 2.0
    disc = disc.cut(bd.Solid.make_cylinder(P.DISC_BORE_R, thru, bd.Plane(origin=(0, 0, -P.DISC_T))))
    for ang in _disc_hole_angles():
        hx, hy = P.DISC_PCD_R * math.cos(ang), P.DISC_PCD_R * math.sin(ang)
        disc = disc.cut(bd.Solid.make_cylinder(P.DISC_HOLE_R, thru, bd.Plane(origin=(hx, hy, -P.DISC_T))))
    return disc.clean()


def build_locking_bar() -> bd.Solid:
    """Blue safety locking bar pinning to arm and clearing the saw disc sweep (>= 0.5 mm)."""
    x0 = P.LOCK_X0
    ty = P.ARM_TIP[1]
    # Pin plugs into the arm socket (stops 0.3 mm short of the socket bottom)
    pin = bd.Solid.make_cylinder(P.LOCK_PIN_R, P.LOCK_SPINE_T + P.LOCK_SPINE_OFF + P.LOCK_PIN_DEPTH - 0.3,
                                 bd.Plane(origin=(x0, P.LOCK_PIN_Y, P.LOCK_PIN_Z), z_dir=(1, 0, 0)))
    # Top stop bar outside the disc rim
    top_bar = bd.Solid.make_cylinder(P.LOCK_BAR_R, P.LOCK_BAR_END_X - x0,
                                     bd.Plane(origin=(x0, ty, P.LOCK_BAR_Z), z_dir=(1, 0, 0)))
    # Side spine standing off the arm face, connecting pin and top bar
    spine = bd.Solid.make_box(P.LOCK_SPINE_T, P.LOCK_SPINE_Y1 - P.LOCK_SPINE_Y0, P.LOCK_SPINE_H).moved(
        bd.Location((x0, P.LOCK_SPINE_Y0, P.LOCK_SPINE_Z0)))
    bar = pin.fuse(top_bar).fuse(spine)
    # Window in the spine over the stator screws: driver access to the heads, and less plastic
    win = bd.Solid.make_box(P.LOCK_SPINE_T + 2.0, P.LOCK_WIN_Y[1] - P.LOCK_WIN_Y[0], P.LOCK_WIN_Z[1] - P.LOCK_WIN_Z[0]).moved(
        bd.Location((x0 - 1.0, P.LOCK_WIN_Y[0], P.LOCK_WIN_Z[0])))
    bar = bar.cut(win)
    return bar.clean()
