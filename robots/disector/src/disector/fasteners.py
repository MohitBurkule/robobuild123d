"""Centralized fastener table and CAD hole-cutting for Disector."""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

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
    down, along_x = (0, 0, -1), (1, 0, 0)
    z_pt = P.Z_TOP + P.PANEL_TOP_T
    z_sp = z_pt + P.TOP_SPINE_T
    out: list[FastenerSpec] = []

    # Top panel -> tub (4 corners)
    for tag, sx, sy, y in (("fl", -1, 1, P.PT_Y_FRONT), ("fr", 1, 1, P.PT_Y_FRONT),
                           ("rl", -1, -1, P.PT_Y_REAR), ("rr", 1, -1, P.PT_Y_REAR)):
        out.append(FastenerSpec(f"f_pt_{tag}", "M2x8", (sx * P.PT_X, y, z_pt), down, ("panel_top",), "tub", grip=P.PANEL_TOP_T))
    # Top spine -> panel_top -> tub
    for tag, sx in (("l", -1), ("r", 1)):
        out.append(FastenerSpec(f"f_sp_{tag}", "M2x8", (sx * P.SP_X, P.SP_Y, z_sp), down, ("top_spine", "panel_top"), "tub",
                                grip=P.PANEL_TOP_T + P.TOP_SPINE_T))
    # Wedge front -> tub (centre of the plate outer face)
    for tag, sx in (("l", -1), ("r", 1)):
        out.append(FastenerSpec(f"f_wf_{tag}", "M2x6", (sx * P.WF_X, P.WEDGE_OUT_Y, P.WEDGE_OUT_Z), n_front,
                                ("wedge_front",), "tub", grip=P.WEDGE_T))
    # Fork mounts and skids -> wedge_front -> tub (screws along the 45-deg pad: Y + Z = PAD_OUT_D)
    for tag, sx in (("l", -1.0), ("r", 1.0)):
        for k, dx in enumerate((-P.FM_DX, P.FM_DX), 1):
            out.append(FastenerSpec(f"f_fm_{tag}{k}", "M2x10", (sx * P.FORK_MOUNT_X + dx, P.PAD_OUT_D - P.FM_Z, P.FM_Z), n_front,
                                    (f"fork_mount_{tag}", "wedge_front"), "tub", grip=P.PAD_GRIP))
        for k, (z, dx) in enumerate(zip(P.SK_Z, (P.SK_DX, -P.SK_DX)), 1):
            out.append(FastenerSpec(f"f_sk_{tag}{k}", "M2x10", (sx * (P.SKID_X + dx), P.PAD_OUT_D - z, z), n_front,
                                    (f"skid_{tag}", "wedge_front"), "tub", grip=P.PAD_GRIP))
    # Side wheel guards -> tub (screws point inboard from the outer face)
    for tag, sx in (("l", -1.0), ("r", 1.0)):
        for k, (y, z) in enumerate(P.GUARD_SCREWS, 1):
            out.append(FastenerSpec(f"f_g{tag}_{k}", "M2x8", (sx * (P.GUARD_X0 + P.GUARD_T), y, z), (-sx, 0, 0),
                                    (f"guard_{tag}",), "tub", grip=P.GUARD_T))
    # Switch -> tub ribs
    for k, sx in enumerate((-1.0, 1.0), 1):
        out.append(FastenerSpec(f"f_sw_{k}", "M2x6", (P.SWITCH_AT[0] + sx * P.SW_EAR_DX, P.SWITCH_AT[1], P.SW_SCREW_Z), down,
                                ("switch",), "tub", grip=0.5, reason="M2 screw clamps switch mounting ear vertically onto tub rib"))
    # GR1507 stator -> arm (12 mm PCD along +/-Y, base at the arm outer face)
    ty, tz = P.ARM_TIP[1], P.ARM_TIP[2]
    for k, sy in enumerate((1.0, -1.0), 1):
        out.append(FastenerSpec(f"f_wm_{k}", "M2x8", (-P.ARM_HALF_T, ty + sy * P.STATOR_PCD_R, tz), along_x, ("arm",),
                                "weapon_motor_stator", grip=2 * P.ARM_HALF_T, into="through"))
    # Disc -> GR1507 bell (two of the 9 mm PCD holes, opposite each other)
    for k, i in enumerate((0, 2), 1):
        a = math.radians(P.DISC_HOLE_PHASE) + i * math.pi / 2
        out.append(FastenerSpec(f"f_dc_{k}", "M2x4", (P.DISC_FACE_X, ty + P.DISC_PCD_R * math.cos(a), tz + P.DISC_PCD_R * math.sin(a)),
                                (-1, 0, 0), ("disc",), "weapon_motor_bell", grip=P.DISC_T, into="through"))
    return out


def _thread_depth(fs: FastenerSpec) -> float:
    """Depth of the tap drill the hole record expects (screw tip + 0.5 mm, measured from the grip plane)."""
    import build123d as bd

    _, rec = hole(bd.Solid.make_box(1, 1, 1), at=fs.at, axis=fs.axis, fastener=fs.designation, head=fs.head,
                  into=fs.into, grip=fs.grip or 0.0)
    return float(rec.hole["thread_depth"])


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
            ax = np.asarray(fs.axis, float)
            ax = ax / np.linalg.norm(ax)
            grip = fs.grip or 0.0
            at_thread = tuple(float(c) for c in (np.asarray(fs.at, float) + grip * ax))
            solid, _ = hole(
                solid,
                at=at_thread,
                axis=fs.axis,
                fastener=fs.designation,
                head=fs.head,
                into=fs.into,
                side="thread",
                grip=0.0,
                engage=_thread_depth(fs) - 0.5,   # tap drill only as deep as the screw actually reaches (+0.5 added by hole())
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
