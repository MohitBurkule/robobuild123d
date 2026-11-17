"""Chassis solids for Disector: unibody tub, top panel, black top spine."""

from __future__ import annotations

import build123d as bd
from . import params as P


def _box_bounds(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> bd.Solid:
    return bd.Solid.make_box(x1 - x0, y1 - y0, z1 - z0).moved(bd.Location((x0, y0, z0)))


def _cut(solid: bd.Solid, *boxes) -> bd.Solid:
    for b in boxes:
        solid = solid.cut(_box_bounds(*b))
    return solid


# Pockets, bays and wire channels cut into the tub (all boxes live in params.py, placed from the part sizes)
TUB_CUTS = [
    P.WHEEL_WELL, P.mx(P.WHEEL_WELL),
    P.MOTOR_POCKET, P.mx(P.MOTOR_POCKET),
    P.BAT_BAY, P.XT30_POCKET,
    P.MAL_BAY, P.mx(P.MAL_BAY),              # Malenki Nano (right front) / weapon ESC (left front)
    P.SERVO_BAY, P.SERVO_EAR_CUT, P.SERVO_LEAD_CH,
    P.REAR_HOLLOW, P.mx(P.REAR_HOLLOW),
    P.SWITCH_PIT, P.BUS_REAR, P.BUS_BAT_SLOT, P.BUS_FRONT,
    P.CH_MAL_BUS, P.CH_MAL_MOTOR, P.CH_MAL_LANE, P.CH_MAL_SIDE,
    P.CH_ESC_MOTOR, P.CH_ESC_BUS, P.CH_ESC_LANE, P.CH_ESC_SIDE, P.CH_ESC_WEAPON, P.CH_MOTOR_L,
]


def build_tub() -> bd.Solid:
    # Extrude Y-Z side profile along X in [-TUB_HALF_W, +TUB_HALF_W]
    pts = [
        (P.Y_REAR, P.Z_FLOOR_BOT),
        (P.Y_FRONT_BOT, P.Z_FLOOR_BOT),
        (P.Y_FRONT_BOT, P.Z_FLOOR_TOP),
        (P.Y_FRONT_TOP, P.Z_TOP),
        (P.Y_REAR, P.Z_TOP),
    ]
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=P.TUB_HALF_W, both=True)
    tub = _cut(bp.part.solids()[0], *TUB_CUTS)

    # Hollow out the front wedge interior: a thick sloped wall where the fork mount / wedge screws bite (out to
    # FRONT_HOLLOW_HALF_W), a thin one across the middle where it only carries the wedge plate
    y0, z0 = P.FRONT_HOLLOW_Y0, P.Z_FLOOR_TOP
    for half_w, d in ((P.FRONT_HOLLOW_HALF_W, P.FRONT_HOLLOW_D), (P.FRONT_CORE_HALF_W, P.FRONT_CORE_D)):
        with bd.BuildPart() as bp_front_cut:
            with bd.BuildSketch(bd.Plane.YZ):
                with bd.BuildLine():
                    bd.Polyline((y0, z0), (d - z0, z0), (y0, d - y0), close=True)
                bd.make_face()
            bd.extrude(amount=half_w, both=True)
        tub = tub.cut(bp_front_cut.part.solids()[0])

    # Switch mounting ribs under the switch ear screws
    for rib in P.SWITCH_RIBS:
        tub = tub.fuse(_box_bounds(*rib))
    return tub.clean()


def build_panel_top() -> bd.Solid:
    """Top deck panel closing all electronics pockets, with cutouts for servo, switch, and weapon wire."""
    panel = _box_bounds(-P.PANEL_X, P.PANEL_X, P.PANEL_Y0, P.PANEL_Y1, P.Z_TOP, P.Z_TOP + P.PANEL_TOP_T)
    return _cut(panel, P.PANEL_SERVO_CUT, P.PANEL_SWITCH_CUT, P.PANEL_WIRE_CUT).clean()


def build_top_spine() -> bd.Solid:
    """Black strap/bracket bolted along the top front edge of the chassis."""
    z0 = P.Z_TOP + P.PANEL_TOP_T
    return _box_bounds(-P.SPINE_X, P.SPINE_X, P.SPINE_Y0, P.SPINE_Y1, z0, z0 + P.TOP_SPINE_T).clean()
