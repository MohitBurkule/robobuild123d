"""Front wedge, forks, fork mounts, outer skids, side wheel guards, and googly eyes for Disector."""

from __future__ import annotations

import math
import build123d as bd
from . import params as P


def _box_bounds(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> bd.Solid:
    sx, sy, sz = x1 - x0, y1 - y0, z1 - z0
    return bd.Solid.make_box(sx, sy, sz).moved(bd.Location((x0, y0, z0)))


def build_wedge_front() -> bd.Solid:
    """1.5 mm aluminium sloped front wedge plate on the 45-degree front face."""
    # Local box centered on origin, rotated +45 deg around X?
    # Let's check: tub front face goes from (Y=8, Z=24) to (Y=28, Z=4).
    # Normal is (0, +1/sqrt(2), +1/sqrt(2)).
    # A plate in XY plane (normal +Z) rotated +45 deg about X has normal (0, -sin(45), cos(45)) = (0, -0.707, +0.707).
    # Rotated -45 deg about X has normal (0, +sin(45), +cos(45)) = (0, +0.707, +0.707)!
    plate = bd.Solid.make_box(P.WEDGE_W, P.WEDGE_SLOPE_LEN, P.WEDGE_T).moved(
        bd.Location((-P.WEDGE_W / 2, -P.WEDGE_SLOPE_LEN / 2, 0.0))
    )
    # Move 0.05 mm off the tub face to avoid coplanar overlap, then rotate -45 deg about X and place at midpoint
    loc = bd.Location((0.0, P.WEDGE_MID_Y + 0.05, P.WEDGE_MID_Z + 0.05)) * bd.Rotation(-45.0, 0.0, 0.0)
    return plate.moved(loc).clean()


def build_fork_mount(side: float) -> bd.Solid:
    """Orange clevis mount bolted to the lower front wedge (side = -1 left, +1 right)."""
    cx = side * P.FORK_MOUNT_X
    # Wedge outer face is at Y + Z = 32.10 + 1.0*sqrt(2) = 33.51.
    # Flat 45-deg mounting pad at Y + Z = 33.51 + 3.2*sqrt(2) = 38.04 (3.2 mm normal thickness).
    d_in = 33.51
    d_out = 38.04
    pts = [
        (d_in - 2.5, 2.5),
        (d_out - 4.0, 2.5),
        (d_out - 4.0, 4.0),
        (d_in - 12.0 + 3.2 * P.INV_SQRT2, 12.0 + 3.2 * P.INV_SQRT2),
        (d_in - 12.0, 12.0),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=7.5, both=True)
    base = bp.part.solids()[0].moved(bd.Location((cx, 0.0, 0.0)))
    # Two clevis ears around X = cx +/- 1.1 (gap 2.2 mm for 1.5 mm fork)
    ear_l = _box_bounds(cx - 4.0, cx - 1.1, 31.2, 37.0, 2.5, 9.0)
    ear_r = _box_bounds(cx + 1.1, cx + 4.0, 31.2, 37.0, 2.5, 9.0)
    u = base.fuse(ear_l).fuse(ear_r)
    # Cut clevis slot so fork clears freely at all angles
    slot = _box_bounds(cx - 1.1, cx + 1.1, 31.2, 37.5, 3.5, 10.0)
    u = u.cut(slot)
    # Cut pivot pin bore (M2, r=1.1 mm) along X
    pin_hole = bd.Solid.make_cylinder(1.1, 10.0, bd.Plane(origin=(cx - 5.0, P.FORK_PIVOT_Y, P.FORK_PIVOT_Z), z_dir=(1, 0, 0)))
    return u.cut(pin_hole).clean()


def build_fork(side: float) -> bd.Solid:
    """1.5 mm titanium pivoting front fork (side = -1 left, +1 right)."""
    cx = side * P.FORK_MOUNT_X
    # Profile in Y-Z plane, extruded along X by FORK_T (centered on cx)
    pts = [
        (P.FORK_PIVOT_Y - 2.0, P.FORK_PIVOT_Z + 2.8),
        (P.FORK_PIVOT_Y + 3.0, P.FORK_PIVOT_Z + 2.8),
        (P.FORK_TIP_Y, P.FORK_TIP_Z + 0.6),
        (P.FORK_TIP_Y, P.FORK_TIP_Z),
        (P.FORK_PIVOT_Y - 2.0, P.FORK_PIVOT_Z - 2.2),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=P.FORK_T / 2, both=True)
    fork = bp.part.solids()[0].moved(bd.Location((cx, 0.0, 0.0)))
    pin_hole = bd.Solid.make_cylinder(1.05, 4.0, bd.Plane(origin=(cx - 2.0, P.FORK_PIVOT_Y, P.FORK_PIVOT_Z), z_dir=(1, 0, 0)))
    return fork.cut(pin_hole).clean()


def build_skid(side: float) -> bd.Solid:
    """Orange outer forward wedge skid/arm bolted to outer front corner (side = -1 left, +1 right)."""
    cx = side * P.SKID_X
    # Back face sits on wedge_front outer plane (Y + Z = 33.51).
    # Flat 45-deg mounting pad at Y + Z = 38.04 (3.2 mm normal thickness) from Z=6 to Z=20.
    d_in = 33.51
    d_out = 38.04
    pts = [
        (d_in - 20.0, 20.0),
        (d_in - 20.0 + 3.2 * P.INV_SQRT2, 20.0 + 3.2 * P.INV_SQRT2),
        (d_out - 6.0, 6.0),
        (P.SKID_TIP_Y, P.SKID_TIP_Z + 1.5),
        (P.SKID_TIP_Y, P.SKID_TIP_Z),
        (d_in - 4.0, 4.0),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=3.5, both=True)
    return bp.part.solids()[0].moved(bd.Location((cx, 0.0, 0.0))).clean()


def build_guard(side: float) -> bd.Solid:
    """Orange side wheel guard covering the wheel well (side = -1 left, +1 right)."""
    x0 = side * (P.GUARD_X0 + (0.0 if side > 0 else P.GUARD_T))
    x1 = x0 + P.GUARD_T
    # Profile in Y-Z plane: bridges over wheel well [-34, -10], bolted at Y in [-39, -34] and [-10, -4]
    pts = [
        (-39.0, 4.0),
        (-4.0, 4.0),
        (-4.0, 16.0),
        (-16.0, 22.0),
        (-32.0, 22.0),
        (-39.0, 14.0),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=P.GUARD_T)
    return bp.part.solids()[0].moved(bd.Location((x0, 0.0, 0.0))).clean()


def build_eye(side: float) -> bd.Solid:
    """Googly eye disc on the front wedge plate (side = -1 left, +1 right)."""
    # Positioned flush on the 45 deg wedge plate at X = +/-6.5
    disc = bd.Solid.make_cylinder(4.2, 1.4)
    loc = bd.Location((side * 6.5, P.WEDGE_MID_Y + 1.11, P.WEDGE_MID_Z + 1.11)) * bd.Rotation(-45.0, 0.0, 0.0)
    return disc.moved(loc).clean()
