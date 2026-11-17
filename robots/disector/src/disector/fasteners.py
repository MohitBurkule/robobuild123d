"""Centralized fastener table and CAD hole-cutting for Disector."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from robot.cad.holes import hole
from . import params as P


@dataclass(frozen=True)
class FastenerSpec:
    id: str
    designation: str
    at: tuple[float, float, float]
    axis: tuple[float, float, float]
    through: tuple[str, ...]
    threads_into: str
    head: str = "button"
    tool: str = "hex1.3"
    grip: float | None = None
    into: str = "tapped"
    reason: str | None = None


def fastener_specs() -> list[FastenerSpec]:
    n_front = (0.0, -P.INV_SQRT2, -P.INV_SQRT2)
    z_top_pt = P.Z_TOP + P.PANEL_TOP_T
    z_top_sp = z_top_pt + P.TOP_SPINE_T
    z_top_tc = z_top_pt + 2.0

    # Wedge outer face: Y + Z = 32 + 0.05*2 + WEDGE_T * sqrt(2)
    wy_mid = P.WEDGE_MID_Y + 0.05 + P.WEDGE_T * P.INV_SQRT2
    wz_mid = P.WEDGE_MID_Z + 0.05 + P.WEDGE_T * P.INV_SQRT2

    return [
        # Top panel -> tub (4 corners, >= 1.35 mm inside edges, >= 0.85 mm from ESC bay)
        FastenerSpec("f_pt_fl", "M2x8", (-45.0, 5.5, z_top_pt), (0, 0, -1), ("panel_top",), "tub", grip=1.2),
        FastenerSpec("f_pt_fr", "M2x8", (45.0, 5.5, z_top_pt), (0, 0, -1), ("panel_top",), "tub", grip=1.2),
        FastenerSpec("f_pt_rl", "M2x8", (-45.0, -37.0, z_top_pt), (0, 0, -1), ("panel_top",), "tub", grip=1.2),
        FastenerSpec("f_pt_rr", "M2x8", (45.0, -37.0, z_top_pt), (0, 0, -1), ("panel_top",), "tub", grip=1.2),
        # Top spine -> panel_top -> tub (threads into solid tub at X=+/-15, Y=5.2)
        FastenerSpec("f_sp_l", "M2x8", (-15.0, 5.2, z_top_sp), (0, 0, -1), ("top_spine", "panel_top"), "tub", grip=2.8),
        FastenerSpec("f_sp_r", "M2x8", (15.0, 5.2, z_top_sp), (0, 0, -1), ("top_spine", "panel_top"), "tub", grip=2.8),
        # Top cover -> panel_top -> tub (on flat ears at X=+/-18.2, Y=-28.5 behind motor pockets)
        FastenerSpec("f_tc_l", "M2x10", (-18.2, -28.5, z_top_tc), (0, 0, -1), ("top_cover", "panel_top"), "tub", grip=3.2),
        FastenerSpec("f_tc_r", "M2x10", (18.2, -28.5, z_top_tc), (0, 0, -1), ("top_cover", "panel_top"), "tub", grip=3.2),
        # Wedge front -> tub
        FastenerSpec("f_wf_l", "M2x8", (-32.0, wy_mid, wz_mid), n_front, ("wedge_front",), "tub", head="button", grip=1.0),
        FastenerSpec("f_wf_r", "M2x8", (32.0, wy_mid, wz_mid), n_front, ("wedge_front",), "tub", head="button", grip=1.0),
        # Fork mounts -> wedge_front -> tub (outer pad Y+Z=38.04, grip=3.2+1.0=4.2)
        FastenerSpec("f_fm_l1", "M2x8", (-P.FORK_MOUNT_X - 4.2, 38.04 - 10.2, 10.2), n_front, ("fork_mount_l", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_fm_l2", "M2x8", (-P.FORK_MOUNT_X + 4.2, 38.04 - 10.2, 10.2), n_front, ("fork_mount_l", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_fm_r1", "M2x8", (P.FORK_MOUNT_X - 4.2, 38.04 - 10.2, 10.2), n_front, ("fork_mount_r", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_fm_r2", "M2x8", (P.FORK_MOUNT_X + 4.2, 38.04 - 10.2, 10.2), n_front, ("fork_mount_r", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        # Skids -> wedge_front -> tub (2 screws along 45-deg pad Y+Z=38.04)
        FastenerSpec("f_sk_l1", "M2x10", (-P.SKID_X, 38.04 - 17.5, 17.5), n_front, ("skid_l", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_sk_l2", "M2x8", (-P.SKID_X, 38.04 - 10.0, 10.0), n_front, ("skid_l", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_sk_r1", "M2x10", (P.SKID_X, 38.04 - 17.5, 17.5), n_front, ("skid_r", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        FastenerSpec("f_sk_r2", "M2x8", (P.SKID_X, 38.04 - 10.0, 10.0), n_front, ("skid_r", "wedge_front"), "tub", head="cap", tool="hex1.5", grip=4.2),
        # Side wheel guards -> tub
        FastenerSpec("f_gl_1", "M2x8", (-(P.GUARD_X0 + P.GUARD_T), -36.5, 10.0), (1, 0, 0), ("guard_l",), "tub", grip=3.0),
        FastenerSpec("f_gl_2", "M2x8", (-(P.GUARD_X0 + P.GUARD_T), -6.5, 13.5), (1, 0, 0), ("guard_l",), "tub", grip=3.0),
        FastenerSpec("f_gr_1", "M2x8", (P.GUARD_X0 + P.GUARD_T, -36.5, 10.0), (-1, 0, 0), ("guard_r",), "tub", grip=3.0),
        FastenerSpec("f_gr_2", "M2x8", (P.GUARD_X0 + P.GUARD_T, -6.5, 13.5), (-1, 0, 0), ("guard_r",), "tub", grip=3.0),
        # Switch -> tub ribs (centered at X=15, Y=-17, flange top at Z=24.50)
        FastenerSpec("f_sw_1", "M2x6", (7.5, -17.0, 24.50), (0, 0, -1), ("switch",), "tub", grip=0.5, reason="M2 screw clamps switch mounting ear vertically onto tub rib"),
        FastenerSpec("f_sw_2", "M2x6", (22.5, -17.0, 24.50), (0, 0, -1), ("switch",), "tub", grip=0.5, reason="M2 screw clamps switch mounting ear vertically onto tub rib"),
        # GR1507 stator -> arm (12 mm PCD -> r=6.0 along +/-Y, base at X=+3.00, arm at X=-3..+3)
        FastenerSpec("f_wm_1", "M2x8", (-3.0, -16.0 + 6.0, 80.0), (1, 0, 0), ("arm",), "weapon_motor_stator", grip=6.0, into="through"),
        FastenerSpec("f_wm_2", "M2x8", (-3.0, -16.0 - 6.0, 80.0), (1, 0, 0), ("arm",), "weapon_motor_stator", grip=6.0, into="through"),
        # Disc -> GR1507 bell (9 mm PCD -> r=4.5 at -54.889 deg & +125.111 deg; disc X=20.10..21.10)
        FastenerSpec("f_dc_1", "M2x4", (21.10, -16.0 + 2.588, 80.0 - 3.681), (-1, 0, 0), ("disc",), "weapon_motor_bell", grip=1.0, into="through"),
        FastenerSpec("f_dc_2", "M2x4", (21.10, -16.0 - 2.588, 80.0 + 3.681), (-1, 0, 0), ("disc",), "weapon_motor_bell", grip=1.0, into="through"),
    ]


def apply_holes_to_part(part_id: str, solid):
    """Cut all fastener clearance/thread holes belonging to `part_id`."""
    for fs in fastener_specs():
        if part_id in fs.through:
            solid, _ = hole(
                solid,
                at=fs.at,
                axis=fs.axis,
                fastener=fs.designation,
                head=fs.head,
                into="through",
                side="head",
            )
        elif part_id == fs.threads_into:
            # Start thread bore behind grip along fs.axis
            import numpy as np
            ax = np.asarray(fs.axis, float)
            ax = ax / np.linalg.norm(ax)
            g = fs.grip or 0.0
            at_thread = tuple(float(c) for c in (np.asarray(fs.at, float) + g * ax))
            solid, _ = hole(
                solid,
                at=at_thread,
                axis=fs.axis,
                fastener=fs.designation,
                head=fs.head,
                into=fs.into,
                side="thread",
                grip=0.0,
            )
    return solid


def build_fastener_records() -> list[dict]:
    """Return spec-ready fasteners[] list with exact hole records."""
    import build123d as bd

    dummy = bd.Solid.make_box(1, 1, 1)
    out = []
    for fs in fastener_specs():
        _, rec = hole(
            dummy,
            at=fs.at,
            axis=fs.axis,
            fastener=fs.designation,
            head=fs.head,
            into=fs.into,
            grip=fs.grip or 0.0,
        )
        d = rec.to_spec(
            fs.id,
            through=list(fs.through),
            threads_into=fs.threads_into,
            tool=fs.tool,
            removable=True,
        )
        if fs.reason:
            d["reason"] = fs.reason
        out.append(d)
    return out
