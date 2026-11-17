"""Front wedge, forks, fork mounts, outer skids, side wheel guards, and googly eyes for Disector."""

from __future__ import annotations

import build123d as bd
from . import params as P


def _box_bounds(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> bd.Solid:
    return bd.Solid.make_box(x1 - x0, y1 - y0, z1 - z0).moved(bd.Location((x0, y0, z0)))


def _yz_prism(pts, half_w: float, cx: float = 0.0) -> bd.Solid:
    """Y-Z polygon extruded along X, `half_w` each side of x = cx."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=half_w, both=True)
    return bp.part.solids()[0].moved(bd.Location((cx, 0.0, 0.0)))


def build_wedge_front() -> bd.Solid:
    """Aluminium sloped front wedge plate on the 45-degree front face, with a scoop lip below the tub's front edge."""
    # Plate lies in local XY (normal +Z); rotating -45 deg about X gives normal (0, +sin45, +cos45): the slope normal.
    # Local +Y runs forward/down the slope, so the lip extends the +Y end.
    length = P.WEDGE_SLOPE_LEN + P.WEDGE_LIP
    plate = bd.Solid.make_box(P.WEDGE_W, length, P.WEDGE_T).moved(
        bd.Location((-P.WEDGE_W / 2, -P.WEDGE_SLOPE_LEN / 2, 0.0))
    )
    # Stand off the tub face so the plate does not sit coplanar-overlapping, then rotate and place at the slope midpoint
    loc = bd.Location((0.0, P.WEDGE_MID_Y + P.WEDGE_GAP, P.WEDGE_MID_Z + P.WEDGE_GAP)) * bd.Rotation(-45.0, 0.0, 0.0)
    return plate.moved(loc).clean()


def build_fork_mount(side: float) -> bd.Solid:
    """Orange clevis mount bolted to the lower front wedge (side = -1 left, +1 right)."""
    cx = side * P.FORK_MOUNT_X
    d_in, d_out = P.WEDGE_OUT_D, P.PAD_OUT_D
    s = P.PAD_T * P.INV_SQRT2
    z0, z1, toe = P.FORK_MOUNT_Z0, P.FORK_MOUNT_Z1, P.FORK_MOUNT_TOE
    pts = [
        (d_in - z0, z0),
        (d_out - z0 - toe, z0),
        (d_out - z0 - toe, z0 + toe),
        (d_in - z1 + s, z1 + s),
        (d_in - z1, z1),
    ]
    base = _yz_prism(pts, P.FORK_MOUNT_W, cx)
    # Two clevis ears around the fork (gap 2.2 mm for the 1.5 mm fork), clear of the heel and pivot pin
    for sx in (-1.0, 1.0):
        x0, x1 = sorted([cx + sx * P.FORK_EAR_X0, cx + sx * P.FORK_EAR_X1])
        base = base.fuse(_box_bounds(x0, x1, *P.FORK_EAR_Y, *P.FORK_EAR_Z))
    # Cut clevis slot so the fork clears freely
    base = base.cut(_box_bounds(cx - P.FORK_EAR_X0, cx + P.FORK_EAR_X0, P.FORK_EAR_Y[0], P.FORK_SLOT_Y1, *P.FORK_SLOT_Z))
    # Cut pivot pin bore (M2) along X through both ears
    pin_len = 2 * (P.FORK_EAR_X1 + 1.0)
    pin_hole = bd.Solid.make_cylinder(P.FORK_BORE_R, pin_len,
                                      bd.Plane(origin=(cx - pin_len / 2, P.FORK_PIVOT_Y, P.FORK_PIVOT_Z), z_dir=(1, 0, 0)))
    return base.cut(pin_hole).clean()


def build_fork(side: float) -> bd.Solid:
    """1.5 mm titanium pivoting front fork (side = -1 left, +1 right)."""
    cx = side * P.FORK_MOUNT_X
    py, pz, back = P.FORK_PIVOT_Y, P.FORK_PIVOT_Z, P.FORK_BACK
    pts = [
        (py - back, pz + P.FORK_TOP_DZ),
        (py + P.FORK_NOSE_DY, pz + P.FORK_TOP_DZ),
        (P.FORK_TIP_Y, P.FORK_TIP_Z + P.FORK_TIP_T),
        (P.FORK_TIP_Y, P.FORK_TIP_Z),
        (py - back, pz - P.FORK_BOT_DZ),
    ]
    fork = _yz_prism(pts, P.FORK_T / 2, cx)
    pin_hole = bd.Solid.make_cylinder(P.FORK_PIN_R, 2 * P.FORK_T,
                                      bd.Plane(origin=(cx - P.FORK_T, py, pz), z_dir=(1, 0, 0)))
    return fork.cut(pin_hole).clean()


def build_skid(side: float) -> bd.Solid:
    """Orange outer forward wedge skid/arm bolted to outer front corner (side = -1 left, +1 right)."""
    d_in, d_out = P.WEDGE_OUT_D, P.PAD_OUT_D
    s = P.PAD_T * P.INV_SQRT2
    pts = [
        (d_in - P.SKID_Z1, P.SKID_Z1),
        (d_in - P.SKID_Z1 + s, P.SKID_Z1 + s),
        (d_out - P.SKID_Z0, P.SKID_Z0),
        (P.SKID_TIP_Y, P.SKID_TIP_Z + P.SKID_TOE_T),
        (P.SKID_TIP_Y, P.SKID_TIP_Z),
        (d_in - P.SKID_Z2, P.SKID_Z2),
    ]
    return _yz_prism(pts, P.SKID_HALF_W, side * P.SKID_X).clean()


def build_guard(side: float) -> bd.Solid:
    """Orange side wheel guard covering the wheel well (side = -1 left, +1 right)."""
    x0 = side * (P.GUARD_X0 + (0.0 if side > 0 else P.GUARD_T))
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*P.GUARD_PROFILE, close=True)
            bd.make_face()
        bd.extrude(amount=P.GUARD_T)
    return bp.part.solids()[0].moved(bd.Location((x0, 0.0, 0.0))).clean()


def build_eye(side: float) -> bd.Solid:
    """Googly eye disc on the front wedge plate (side = -1 left, +1 right)."""
    disc = bd.Solid.make_cylinder(P.EYE_R, P.EYE_T)
    loc = bd.Location((side * P.EYE_X, P.EYE_Y, P.EYE_Z)) * bd.Rotation(-45.0, 0.0, 0.0)
    return disc.moved(loc).clean()
