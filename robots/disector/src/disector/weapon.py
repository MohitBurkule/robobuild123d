"""Overhead hammer-saw arm, toothed saw disc, and locking bar for Disector."""

from __future__ import annotations

import math
import build123d as bd
from . import params as P


def build_arm() -> bd.Solid:
    """Dark-green curved overhead hammer-saw arm from servo pivot to weapon motor mount."""
    px, py, pz = P.ARM_PIVOT
    tx, ty, tz = P.ARM_TIP
    # Curved arm profile in Y-Z plane (extruded X in [-3.0, +3.0])
    pts = [
        (py - 4.0, pz - 1.5),
        (py + 4.0, pz - 1.5),
        (-30.0, 48.0),
        (ty + 8.5, tz - 8.5),
        (ty + 8.5, tz + 8.5),
        (ty - 8.5, tz + 8.5),
        (-38.0, 52.0),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
            bd.fillet(bd.vertices(), 1.0)
        bd.extrude(amount=3.0, both=True)
    arm = bp.part.solids()[0]
    # Cut central shaft clearance hole at tip
    hole = bd.Solid.make_cylinder(2.6, 8.0, bd.Plane(origin=(-4.0, ty, tz), z_dir=(1, 0, 0)))
    return arm.cut(hole).clean()


def build_weapon_shaft() -> bd.Solid:
    """GR1507 5 mm threaded steel motor shaft (29.1 mm total, 12 mm protrusion, 8 mm M5 thread)."""
    # Built in weapon_motor_bell local frame (bell at X=13.40 -> free end at X=18.70, world X=32.10)
    x_end = 18.70
    total_len = 29.10
    thread_len = 7.2
    p = 0.8
    r = 2.5
    dr = 0.43
    ch = 0.4
    prof = [(0.0, 0.0), (0.0, r - dr - ch), (ch, r - dr)]
    for k in range(int(round(thread_len / p))):
        x = ch + k * p
        prof += [(x + p / 2.0, r), (x + p, r - dr)]
    prof += [(thread_len, r), (total_len, r), (total_len, 0.0)]
    face = bd.Face(bd.Wire.make_polygon([bd.Vector(x_end - x, 0.0, z) for x, z in prof], close=True))
    return bd.Solid.revolve(face, 360.0, bd.Axis((0.0, 0.0, 0.0), (1.0, 0.0, 0.0))).clean()


def build_disc() -> bd.Solid:
    """44 mm OD, 1.0 mm thick titanium circular saw disc with 4 hooked teeth."""
    r_out = P.DISC_R
    r_root = P.DISC_R - 4.5
    n_teeth = 4
    pts = []
    for k in range(n_teeth):
        a0 = 2 * math.pi * k / n_teeth
        a_back = a0 + 0.35
        a_tip = a0 + 1.05
        a_gullet = a0 + 1.15
        pts.append((r_root * math.cos(a0), r_root * math.sin(a0)))
        pts.append((r_out * math.cos(a_back), r_out * math.sin(a_back)))
        pts.append((r_out * math.cos(a_tip), r_out * math.sin(a_tip)))
        pts.append((r_root * math.cos(a_gullet), r_root * math.sin(a_gullet)))

    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.XY):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
            bd.fillet(bd.vertices(), 0.3)
        bd.extrude(amount=P.DISC_T / 2, both=True)
    disc = bp.part.solids()[0]
    # Center bore (5.2 mm dia for GR1507 5 mm shaft)
    disc = disc.cut(bd.Solid.make_cylinder(2.6, P.DISC_T + 2.0, bd.Plane(origin=(0, 0, -P.DISC_T))))
    # 4x M2 clearance holes (>= 2.2 mm) on 9.0 mm PCD (matching GR1507 top_holes phase -54.889 deg)
    phase = math.radians(-54.889)
    for k in range(4):
        ang = phase + k * math.pi / 2
        hx, hy = 4.5 * math.cos(ang), 4.5 * math.sin(ang)
        disc = disc.cut(bd.Solid.make_cylinder(1.15, P.DISC_T + 2.0, bd.Plane(origin=(hx, hy, -P.DISC_T))))
    return disc.clean()


def build_locking_bar() -> bd.Solid:
    """Blue safety locking bar pinning to arm and clearing the saw disc sweep (>= 0.5 mm)."""
    tx, ty, tz = P.ARM_TIP
    # Pin into arm at (ty - 15.0, tz - 19.0) = (-31.0, 61.0), radius from disc center = 24.2 mm (> 22.5 mm)
    pin = bd.Solid.make_cylinder(1.5, 8.0, bd.Plane(origin=(-6.0, ty - 15.0, tz - 19.0), z_dir=(1, 0, 0)))
    # Top stop bar outside disc rim at tz + 24.5 (radius 24.5 > 22.5)
    top_bar = bd.Solid.make_cylinder(1.5, 29.0, bd.Plane(origin=(-6.0, ty, tz + 24.5), z_dir=(1, 0, 0)))
    # Side spine at X = -6.0..-3.5 connecting pin and top_bar
    spine = bd.Solid.make_box(2.5, 18.0, 46.5).moved(bd.Location((-6.0, ty - 16.5, tz - 20.5)))
    return pin.fuse(top_bar).fuse(spine).clean()
