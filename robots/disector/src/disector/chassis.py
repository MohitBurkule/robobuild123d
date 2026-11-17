"""Chassis solids for Disector: unibody tub, top panel, top blue cover, black top spine."""

from __future__ import annotations

import build123d as bd
from . import params as P


def _box_at(sx: float, sy: float, sz: float, cx: float, cy: float, cz: float) -> bd.Solid:
    return bd.Solid.make_box(sx, sy, sz).moved(bd.Location((cx - sx / 2, cy - sy / 2, cz - sz / 2)))


def _box_bounds(x0: float, x1: float, y0: float, y1: float, z0: float, z1: float) -> bd.Solid:
    return _box_at(x1 - x0, y1 - y0, z1 - z0, 0.5 * (x0 + x1), 0.5 * (y0 + y1), 0.5 * (z0 + z1))


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
    tub = bp.part.solids()[0]

    # Cut wheel wells on left and right
    for sx in (-1.0, 1.0):
        x0, x1 = sorted([sx * 38.5, sx * (P.TUB_HALF_W + 1.0)])
        tub = tub.cut(_box_bounds(x0, x1, -34.0, -10.0, 1.0, 23.0))

    # Cut drive motor pockets (drop-in from top, snug at X=+/-17.15 so motor at 17.40 is captured)
    for sx in (-1.0, 1.0):
        x0, x1 = sorted([sx * 17.15, sx * 38.6])
        tub = tub.cut(_box_bounds(x0, x1, -27.5, -16.5, 3.8, P.Z_TOP + 1.0))

    # Cut central battery bay (Y in [-14.2, 4.0]) + front XT30 connector pocket (Y in [4.0, 9.0])
    tub = tub.cut(_box_bounds(-18.6, 18.6, -14.2, 4.0, P.Z_FLOOR_TOP, P.Z_TOP + 1.0))
    tub = tub.cut(_box_bounds(-7.0, 7.0, 3.5, 9.5, P.Z_FLOOR_TOP, 19.0))

    # Cut Malenki Nano bay (right front, Y in [-8.5, 7.5], X in [19.8, 43.0])
    tub = tub.cut(_box_bounds(19.8, 43.0, -8.5, 7.5, P.Z_FLOOR_TOP, P.Z_TOP + 1.0))

    # Cut Weapon ESC bay (left front, Y in [-8.5, 7.5], X in [-43.0, -19.8])
    tub = tub.cut(_box_bounds(-43.0, -19.8, -8.5, 7.5, P.Z_FLOOR_TOP, P.Z_TOP + 1.0))

    # Cut Servo bay (rear center)
    tub = tub.cut(_box_bounds(-12.2, 12.2, -34.5, -21.5, 7.0, P.Z_TOP + 1.0))
    # Servo mounting ear clearance
    tub = tub.cut(_box_bounds(4.8, 9.2, -34.5, -21.5, 2.8, P.Z_TOP + 1.0))

    # Hollow out rear corners (outside servo bay & clear of corner screws & f_tc) to lighten tub
    for sx in (-1.0, 1.0):
        x0, x1 = sorted([sx * 14.5, sx * 43.0])
        tub = tub.cut(_box_bounds(x0, x1, -36.5, -31.0, P.Z_FLOOR_TOP, P.Z_TOP + 1.0))

    # Hollow out front wedge interior (leave 4.6 mm thick sloped front wall, solid at X=+/-43 for skids)
    with bd.BuildPart() as bp_front_cut:
        with bd.BuildSketch(bd.Plane.YZ):
            with bd.BuildLine():
                bd.Polyline((8.0, P.Z_FLOOR_TOP), (19.0, P.Z_FLOOR_TOP), (8.0, 15.0), close=True)
            bd.make_face()
        bd.extrude(amount=38.0, both=True)
    tub = tub.cut(bp_front_cut.part.solids()[0])

    # Wire channels (>= 4 mm wide) connecting all bays & switch pocket (centered at X=15, Y=-17)
    tub = tub.cut(_box_bounds(9.5, 20.5, -20.0, -14.0, 6.0, P.Z_TOP + 1.0))     # switch pit at X=15, Y=-17
    tub = tub.cut(_box_bounds(-22.0, 22.0, -19.0, -14.0, 5.0, 19.0))            # transverse rear bus
    tub = tub.cut(_box_bounds(-22.0, 22.0, -4.0, 2.0, 6.0, 15.0))               # transverse front bus
    tub = tub.cut(_box_bounds(18.0, 23.0, -16.0, 0.0, 5.0, 16.0))               # rear bus -> malenki_rx.bat
    tub = tub.cut(_box_bounds(22.0, 46.0, -15.0, -8.0, 5.0, 16.0))              # malenki -> motor_r & +X loop
    tub = tub.cut(_box_bounds(43.0, 46.0, -12.0, 5.0, 4.0, 10.0))               # malenki +X side channel (below f_gr_2 at Z=13.5)
    tub = tub.cut(_box_bounds(-28.0, -22.0, -18.0, -8.0, 6.0, 16.0))            # wpn_esc -> motor_l
    tub = tub.cut(_box_bounds(-46.0, -18.0, -15.0, -8.0, 5.0, 16.0))            # rear bus -> weapon_esc
    tub = tub.cut(_box_bounds(-46.0, -43.0, -12.0, 5.0, 4.0, 10.0))             # weapon_esc -X side channel (below f_gl_2 at Z=13.5)
    tub = tub.cut(_box_bounds(-25.0, -19.0, -15.5, -9.5, 10.0, P.Z_TOP + 1.0)) # weapon_esc -> weapon_motor vertical slot
    tub = tub.cut(_box_bounds(-18.5, -13.0, -24.0, -18.0, 7.0, 14.0))          # rear bus -> motor_l.terminals
    tub = tub.cut(_box_bounds(12.2, 18.0, -26.0, -18.0, 12.0, P.Z_TOP + 1.0))   # rear bus -> servo signal up-channel

    # Switch mounting ribs at X=15 +/- [5.8, 10.2] -> [4.8, 9.2] and [20.8, 25.2], Y in [-20, -14]
    tub = tub.fuse(_box_bounds(4.8, 9.2, -20.0, -14.0, 19.0, P.Z_TOP))
    tub = tub.fuse(_box_bounds(20.8, 25.2, -20.0, -14.0, 19.0, P.Z_TOP))

    return tub.clean()


def build_panel_top() -> bd.Solid:
    """Top deck panel closing all electronics pockets, with cutouts for servo, switch, and weapon wire."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.XY.offset(P.Z_TOP)):
            bd.Rectangle(2 * P.TUB_HALF_W - 1.0, P.Y_FRONT_TOP - P.Y_REAR - 1.2, align=(bd.Align.CENTER, bd.Align.MIN))
        bd.extrude(amount=P.PANEL_TOP_T)
    panel = bp.part.solids()[0].moved(bd.Location((0.0, P.Y_REAR + 1.0, 0.0)))
    # Cutout for servo protruding up into top_cover (and servo signal wire channel at X=14.5)
    panel = panel.cut(_box_bounds(-13.0, 15.8, -35.0, -21.5, P.Z_TOP - 1.0, P.Z_TOP + P.PANEL_TOP_T + 1.0))
    # Cutout for switch_bbb_ant_rvrn2 body and flange (centered at X=15.0, Y=-17.0)
    panel = panel.cut(_box_bounds(4.5, 25.5, -20.0, -14.0, P.Z_TOP - 1.0, P.Z_TOP + P.PANEL_TOP_T + 1.0))
    # Wire pass-through slot for weapon motor phase leads (over weapon_esc bay, clear of battery & top_cover)
    panel = panel.cut(_box_bounds(-25.0, -19.0, -15.5, -9.5, P.Z_TOP - 1.0, P.Z_TOP + P.PANEL_TOP_T + 1.0))
    return panel.clean()


def build_top_cover() -> bd.Solid:
    """Blue raised protective housing on top center covering servo (clear of switch at Y=-17.0)."""
    z0 = P.Z_TOP + P.PANEL_TOP_T
    z1 = P.TOP_COVER_Z1
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ):
            pts = [
                (-36.5, z0),
                (-20.2, z0),
                (-20.2, z1 - 2.0),
                (-22.2, z1),
                (-36.0, z1),
                (-36.5, z0 + 4.0),
            ]
            with bd.BuildLine():
                bd.Polyline(*pts, close=True)
            bd.make_face()
        bd.extrude(amount=16.2, both=True)
    cov = bp.part.solids()[0]
    # Add flat 2 mm mounting ears at X = +/-[15.8, 20.8] for unobstructed vertical screw access
    for sx in (-1.0, 1.0):
        x0, x1 = sorted([sx * 15.8, sx * 20.8])
        cov = cov.fuse(_box_bounds(x0, x1, -30.5, -22.0, z0, z0 + 2.0))
    # Hollow inside for servo top & arm clevis clearance (servo Y in [-34.0, -22.0])
    cov = cov.cut(_box_bounds(-12.6, 15.0, -34.5, -21.6, z0 - 0.5, z1 - 3.0))
    # Open U-slot at top for overhead arm (arm Z>=33.5 at Y>=-32, and Z>=45 at Y=-37)
    cov = cov.cut(_box_bounds(-3.6, 3.6, -33.0, -24.0, 33.0, 35.5))
    cov = cov.cut(_box_bounds(-3.6, 3.6, -37.0, -24.0, 35.2, z1 + 1.0))
    return cov.clean()


def build_top_spine() -> bd.Solid:
    """Black strap/bracket bolted along the top front edge of the chassis."""
    z0 = P.Z_TOP + P.PANEL_TOP_T
    return _box_bounds(-42.0, 42.0, 2.0, 7.8, z0, z0 + P.TOP_SPINE_T).clean()
