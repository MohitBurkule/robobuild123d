"""build123d part builders for Steve (Stewie)."""
import math
from build123d import (
    Align,
    Axis,
    Box,
    BuildLine,
    BuildSketch,
    Cylinder,
    Line,
    Locations,
    Mode,
    Plane,
    Polygon,
    Spline,
    extrude,
    make_face,
)
from . import params as P


def build_tub():
    """Main dark-green 3D-printed chassis tub with smooth curved top arch and curved front slope."""
    half_w = P.TUB_W / 2.0
    # Smoothly curved top profile in YZ plane (matching Steve's arched green shell)
    curve_pts = [
        (P.TUB_REAR_Y, P.TUB_TOP_Z - 3.0),
        (-22.0, P.TUB_TOP_Z - 0.3),
        (-4.0, P.TUB_TOP_Z),
        (14.0, P.TUB_TOP_Z - 2.2),
        (26.0, P.TUB_TOP_Z - 9.0),
        (P.TUB_FRONT_Y, 8.0),
    ]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Line((P.TUB_REAR_Y, P.GROUND_CLEARANCE), (P.TUB_FRONT_Y, P.GROUND_CLEARANCE))
            Line((P.TUB_FRONT_Y, P.GROUND_CLEARANCE), (P.TUB_FRONT_Y, 8.0))
            Spline(*reversed(curve_pts))
            Line((P.TUB_REAR_Y, P.TUB_TOP_Z - 3.0), (P.TUB_REAR_Y, P.GROUND_CLEARANCE))
        make_face()
    tub = extrude(sk.sketch, amount=half_w, both=True)

    # Cut central flipper slot (X in [-SLOT_W/2, +SLOT_W/2], Y from SLOT_REAR_Y to TUB_FRONT_Y+2)
    slot_len = (P.TUB_FRONT_Y + 2.0) - P.SLOT_REAR_Y
    slot_yc = (P.SLOT_REAR_Y + P.TUB_FRONT_Y + 2.0) / 2.0
    slot_cut = Box(P.SLOT_W, slot_len, P.TUB_TOP_Z + 4.0).translate(
        (0.0, slot_yc, P.GROUND_CLEARANCE + P.FLOOR_T + (P.TUB_TOP_Z + 4.0) / 2.0)
    )
    tub = tub - slot_cut

    # Cut left & right internal electronics bays (under lids)
    bay_w = half_w - P.SLOT_W / 2.0 - P.WALL_T * 2.0
    bay_len = (P.TUB_DECK_END_Y - 3.0) - (P.TUB_REAR_Y + P.WALL_T)
    bay_yc = (P.TUB_REAR_Y + P.WALL_T + P.TUB_DECK_END_Y - 3.0) / 2.0
    bay_h = P.TUB_TOP_Z - P.GROUND_CLEARANCE - P.FLOOR_T - 4.0
    bay_zc = P.GROUND_CLEARANCE + P.FLOOR_T + bay_h / 2.0
    for s in (-1.0, 1.0):
        bay_xc = s * (P.SLOT_W / 2.0 + P.WALL_T + bay_w / 2.0)
        bay_cut = Box(bay_w, bay_len, bay_h).translate((bay_xc, bay_yc, bay_zc))
        tub = tub - bay_cut

    # Wheel-guard mounting frame (standoffs + lower front wheel-arch shelf)
    boss_len = P.GUARD_X - half_w + 0.5
    boss_xc = half_w + boss_len / 2.0 - 0.25
    for s in (-1.0, 1.0):
        for dy in (-12.0, 12.0):
            for dz in (-8.0, 9.0):
                boss = (
                    Cylinder(radius=2.2, height=boss_len)
                    .rotate(Axis.Y, 90)
                    .translate((s * boss_xc, P.WHEEL_Y + dy, P.AXLE_Z + dz))
                )
                tub = tub + boss
        shelf = Box(boss_len, 8.0, 2.5).translate(
            (s * boss_xc, P.WHEEL_Y + 11.0, P.AXLE_Z - 7.0)
        )
        tub = tub + shelf

    # Hinge pin bores through central slot walls
    pin_bore = (
        Cylinder(radius=P.HINGE_PIN_D / 2.0 + 0.1, height=P.TUB_W + 2.0)
        .rotate(Axis.Y, 90)
        .translate((0.0, P.HINGE_Y, P.HINGE_Z))
    )
    tub = tub - pin_bore

    # Motor shaft bores through tub side walls
    shaft_bore = (
        Cylinder(radius=1.8, height=P.TUB_W + 2.0)
        .rotate(Axis.Y, 90)
        .translate((0.0, P.WHEEL_Y, P.AXLE_Z))
    )
    tub = tub - shaft_bore

    return tub


def build_lid(side: int = 1):
    """Curved dark-green top deck lid (+1 = left/+X, -1 = right/-X) following the chassis arch with 2 screws."""
    lid_w = (P.TUB_W / 2.0) - (P.SLOT_W / 2.0) - 0.5
    lid_yc = (P.TUB_REAR_Y + P.TUB_DECK_END_Y) / 2.0
    lid_zc = P.LID_Z + P.LID_T / 2.0
    pts_bot = [
        (P.TUB_REAR_Y - lid_yc, P.TUB_TOP_Z - 3.0 - lid_zc),
        (-22.0 - lid_yc, P.TUB_TOP_Z - 0.3 - lid_zc),
        (-4.0 - lid_yc, P.TUB_TOP_Z - lid_zc),
        (14.0 - lid_yc, P.TUB_TOP_Z - 2.2 - lid_zc),
        (P.TUB_DECK_END_Y - lid_yc, P.TUB_TOP_Z - 5.2 - lid_zc),
    ]
    pts_top = [(y, z + P.LID_T) for (y, z) in pts_bot]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Line(pts_bot[0], pts_top[0])
            Spline(*pts_top)
            Line(pts_top[-1], pts_bot[-1])
            Spline(*reversed(pts_bot))
        make_face()
    lid = extrude(sk.sketch, amount=lid_w / 2.0, both=True)
    # 2 low-profile button-head screws at rear and front outer corners
    screw_yz = [
        (P.TUB_REAR_Y + 5.0 - lid_yc, P.TUB_TOP_Z - 2.2 - lid_zc + P.LID_T),
        (P.TUB_DECK_END_Y - 4.5 - lid_yc, P.TUB_TOP_Z - 3.8 - lid_zc + P.LID_T),
    ]
    for sy, sz in screw_yz:
        head = Cylinder(radius=2.3, height=0.9).translate(
            (side * (lid_w / 2.0 - 4.5), sy, sz + 0.3)
        )
        socket = Cylinder(radius=0.8, height=0.8).translate(
            (side * (lid_w / 2.0 - 4.5), sy, sz + 0.6)
        )
        lid = lid + (head - socket)
    return lid


def build_guard():
    """Outboard wheel guard plate in local YZ-aligned frame (curved front edge, flat rear edge)."""
    hw = P.GUARD_L / 2.0
    hh = P.GUARD_H / 2.0
    pts_curve = [
        (-hw + 3.0, hh),
        (2.0, hh),
        (hw - 2.0, hh - 5.0),
        (hw, 0.0),
        (hw - 3.0, -hh + 5.0),
        (0.0, -hh),
        (-hw + 3.0, -hh),
    ]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Spline(*pts_curve)
            Line((-hw + 3.0, -hh), (-hw, -hh + 3.0))
            Line((-hw, -hh + 3.0), (-hw, hh - 3.0))
            Line((-hw, hh - 3.0), (-hw + 3.0, hh))
        make_face()
    plate = extrude(sk.sketch, amount=P.GUARD_T / 2.0, both=True)
    return plate


def build_wheel():
    """Ø28 x 8 mm wheel with circumferential tread grooves, axis along X."""
    r = P.WHEEL_D / 2.0
    w = P.WHEEL_W
    wheel = Cylinder(radius=r, height=w).rotate(Axis.Y, 90)
    for dx in (-2.2, 0.0, 2.2):
        groove_outer = Cylinder(radius=r + 0.5, height=0.8).rotate(Axis.Y, 90).translate((dx, 0, 0))
        groove_inner = Cylinder(radius=r - 0.8, height=1.0).rotate(Axis.Y, 90).translate((dx, 0, 0))
        wheel = wheel - (groove_outer - groove_inner)
    bore = Cylinder(radius=1.5, height=w + 2.0).rotate(Axis.Y, 90)
    wheel = wheel - bore
    return wheel


def build_flipper():
    """Black 3D-printed central flipper arm in local frame (hinge at origin (0,0,0))."""
    top_pts = [
        (-3.0, 3.0),
        (12.0, 7.2),
        (30.0, 7.5),
        (46.0, 3.5),
        (54.0, -1.8),
        (65.0, -6.5),
    ]
    bot_pts = [
        (65.0, -11.0),
        (50.0, -4.5),
        (26.0, 1.0),
        (-3.0, -3.5),
    ]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Spline(*top_pts)
            Line(top_pts[-1], bot_pts[0])
            Spline(*bot_pts)
            Line(bot_pts[-1], top_pts[0])
        make_face()
    arm = extrude(sk.sketch, amount=P.ARM_W / 2.0, both=True)
    bore = Cylinder(radius=P.HINGE_PIN_D / 2.0 + 0.1, height=P.ARM_W + 2.0).rotate(Axis.Y, 90)
    arm = arm - bore
    return arm


def build_scoop():
    """Curved brushed-metal front flipper scoop with side cheek gussets and 4 top bolts, in flipper-hinge local frame."""
    y_top = P.SCOOP_TOP_Y - P.HINGE_Y      # 54.0
    z_top = P.SCOOP_TOP_Z - P.HINGE_Z      # -0.5
    y_tip = P.SCOOP_TIP_Y - P.HINGE_Y      # 86.0
    z_tip = P.SCOOP_TIP_Z - P.HINGE_Z      # -24.5

    # Exact spline points for upper surface of curved scoop
    curve_upper = [
        (y_top, z_top),
        (y_top + 8.0, z_top - 3.5),
        (y_top + 18.0, z_top - 10.0),
        (y_top + 27.0, z_top - 18.0),
        (y_tip, z_tip),
    ]
    curve_lower = [(y, z - P.SCOOP_T) for (y, z) in curve_upper]

    with BuildSketch(Plane.YZ) as sk_yz:
        with BuildLine():
            Spline(*curve_upper)
            Line(curve_upper[-1], curve_lower[-1])
            Spline(*reversed(curve_lower))
            Line(curve_lower[0], curve_upper[0])
        make_face()
    raw_sheet = extrude(sk_yz.sketch, amount=P.SCOOP_BOT_W / 2.0, both=True)

    # Trim to trapezoidal planform in XY with slightly curved outer side edges
    hw_bot = P.SCOOP_BOT_W / 2.0
    hw_top = P.SCOOP_TOP_W / 2.0
    for s in (-1.0, 1.0):
        cut_pts = [
            (s * hw_top, y_top - 5.0),
            (s * (hw_bot + 15.0), y_top - 5.0),
            (s * (hw_bot + 15.0), y_tip + 5.0),
            (s * hw_bot, y_tip + 5.0),
        ]
        with BuildSketch(Plane.XY) as sk_cut:
            Polygon(*cut_pts, align=None)
        cutter = extrude(sk_cut.sketch, amount=40.0, both=True)
        raw_sheet = raw_sheet - cutter

    # Triangular side cheek gussets flush under the outer wings of the scoop (visible in reference.png)
    for s in (-1.0, 1.0):
        cheek_pts = [
            (y_top + 13.0, z_top - 7.5),
            (y_tip - 1.5, z_tip + 0.5),
            (y_top + 19.0, z_tip + 0.5),
        ]
        with BuildSketch(Plane.YZ) as sk_ch:
            Polygon(*cheek_pts, align=None)
        cheek = extrude(sk_ch.sketch, amount=0.8, both=True).translate((s * (hw_top + 6.5), 0.0, 0.0))
        raw_sheet = raw_sheet + cheek

    # 4 protruding bolts + washers + nuts in a 2x2 cluster at top center (matching reference.png)
    # At dy_off=3.5 -> z on curve is z_top - 1.5; at dy_off=8.5 -> z on curve is z_top - 3.7
    bolt_specs = [
        (-3.2, 3.5, z_top - 1.4),
        (3.2, 3.5, z_top - 1.4),
        (-3.0, 8.5, z_top - 3.6),
        (3.0, 8.5, z_top - 3.6),
    ]
    for dx, dy_off, bz in bolt_specs:
        by = y_top + dy_off
        washer = (
            Cylinder(radius=2.6, height=0.8)
            .rotate(Axis.X, -28)
            .translate((dx, by, bz + 0.4))
        )
        nut = (
            Cylinder(radius=1.8, height=1.4)
            .rotate(Axis.X, -28)
            .translate((dx, by + 0.5, bz + 1.1))
        )
        stud = (
            Cylinder(radius=0.9, height=2.6)
            .rotate(Axis.X, -28)
            .translate((dx, by + 0.9, bz + 1.8))
        )
        raw_sheet = raw_sheet + washer + nut + stud

    return raw_sheet


def build_hinge_pin():
    """Steel hinge pin along X."""
    return Cylinder(radius=P.HINGE_PIN_D / 2.0, height=P.TUB_W - 4.0).rotate(Axis.Y, 90)


def build_horn():
    """Printed servo horn."""
    return Box(6.0, 10.0, 3.0).translate((0.0, 3.0, 0.0))
