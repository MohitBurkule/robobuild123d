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
    """Main dark-green 3D-printed chassis tub in world frame."""
    half_w = P.TUB_W / 2.0
    # Side profile in YZ plane:
    # (y, z)
    # Smoothly curved top profile in YZ plane (matching Steve's arched shell)
    curve_pts = [
        (P.TUB_REAR_Y, P.TUB_TOP_Z - 3.5),
        (-24.0, P.TUB_TOP_Z - 0.5),
        (-8.0, P.TUB_TOP_Z),
        (10.0, P.TUB_TOP_Z - 4.0),
        (24.0, P.TUB_FRONT_Z + 8.0),
        (P.TUB_FRONT_Y, P.TUB_FRONT_Z),
    ]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            l1 = Line((P.TUB_REAR_Y, P.GROUND_CLEARANCE), (P.TUB_FRONT_Y, P.GROUND_CLEARANCE))
            l2 = Line((P.TUB_FRONT_Y, P.GROUND_CLEARANCE), (P.TUB_FRONT_Y, P.TUB_FRONT_Z))
            s1 = Spline(*reversed(curve_pts))
            l3 = Line((P.TUB_REAR_Y, P.TUB_TOP_Z - 3.5), (P.TUB_REAR_Y, P.GROUND_CLEARANCE))
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
    bay_len = (P.TUB_DECK_END_Y - 2.0) - (P.TUB_REAR_Y + P.WALL_T)
    bay_yc = (P.TUB_REAR_Y + P.WALL_T + P.TUB_DECK_END_Y - 2.0) / 2.0
    bay_h = P.TUB_TOP_Z - P.GROUND_CLEARANCE - P.FLOOR_T + 1.0
    bay_zc = P.GROUND_CLEARANCE + P.FLOOR_T + bay_h / 2.0
    for s in (-1.0, 1.0):
        bay_xc = s * (P.SLOT_W / 2.0 + P.WALL_T + bay_w / 2.0)
        bay_cut = Box(bay_w, bay_len, bay_h).translate((bay_xc, bay_yc, bay_zc))
        tub = tub - bay_cut

    # Wheel-guard mounting standoffs (4 corners per side)
    boss_len = P.GUARD_X - half_w + 0.5
    boss_xc = half_w + boss_len / 2.0 - 0.25
    for s in (-1.0, 1.0):
        for dy in (-11.0, 11.0):
            for dz in (-8.0, 8.0):
                boss = (
                    Cylinder(radius=2.2, height=boss_len)
                    .rotate(Axis.Y, 90)
                    .translate((s * boss_xc, P.WHEEL_Y + dy, P.AXLE_Z + dz))
                )
                tub = tub + boss

    # Hinge pin bores through central slot walls
    pin_bore = (
        Cylinder(radius=P.HINGE_PIN_D / 2.0 + 0.1, height=P.TUB_W + 2.0)
        .rotate(Axis.Y, 90)
        .translate((0.0, P.HINGE_Y, P.HINGE_Z))
    )
    tub = tub - pin_bore

    return tub


def build_lid(side: int = 1):
    """Curved top deck lid (+1 = left/+X, -1 = right/-X) in local frame centred at (0,0,0)."""
    lid_w = (P.TUB_W / 2.0) - (P.SLOT_W / 2.0) - 0.5
    lid_yc = (P.TUB_REAR_Y + P.TUB_DECK_END_Y) / 2.0
    lid_zc = P.LID_Z + P.LID_T / 2.0
    # Local YZ coordinates relative to (lid_yc, lid_zc)
    pts_bot = [
        (P.TUB_REAR_Y - lid_yc, P.TUB_TOP_Z - 3.5 - lid_zc),
        (-24.0 - lid_yc, P.TUB_TOP_Z - 0.5 - lid_zc),
        (-8.0 - lid_yc, P.TUB_TOP_Z - lid_zc),
        (P.TUB_DECK_END_Y - lid_yc, P.TUB_TOP_Z - 3.5 - lid_zc),
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
    # 2 M2 screw holes at front and rear outer corners
    lid_len = P.TUB_DECK_END_Y - P.TUB_REAR_Y
    for dy in (-lid_len / 2.0 + 4.5, lid_len / 2.0 - 4.5):
        hole = Cylinder(radius=P.M2_CLEAR_D / 2.0, height=12.0).translate(
            (side * (lid_w / 2.0 - 4.5), dy, 0.0)
        )
        lid = lid - hole
    return lid


def build_guard():
    """Outboard wheel guard plate in local YZ-aligned frame (thickness along X)."""
    hw = P.GUARD_L / 2.0
    hh = P.GUARD_H / 2.0
    ch = 5.0
    pts = [
        (-hw + ch, -hh),
        (hw - ch, -hh),
        (hw, -hh + ch),
        (hw, hh - ch),
        (hw - ch, hh),
        (-hw + ch, hh),
        (-hw, hh - ch),
        (-hw, -hh + ch),
    ]
    with BuildSketch(Plane.YZ) as sk:
        Polygon(*pts, align=None)
    plate = extrude(sk.sketch, amount=P.GUARD_T / 2.0, both=True)
    return plate


def build_wheel():
    """Ø28 x 8 mm wheel with circumferential tread grooves, axis along X."""
    r = P.WHEEL_D / 2.0
    w = P.WHEEL_W
    wheel = Cylinder(radius=r, height=w).rotate(Axis.Y, 90)
    # Circumferential tread grooves
    for dx in (-2.2, 0.0, 2.2):
        groove_outer = Cylinder(radius=r + 0.5, height=0.8).rotate(Axis.Y, 90).translate((dx, 0, 0))
        groove_inner = Cylinder(radius=r - 0.8, height=1.0).rotate(Axis.Y, 90).translate((dx, 0, 0))
        wheel = wheel - (groove_outer - groove_inner)
    # Axle bore
    bore = Cylinder(radius=1.5, height=w + 2.0).rotate(Axis.Y, 90)
    wheel = wheel - bore
    return wheel


def build_flipper():
    """Black 3D-printed central flipper arm in local frame (hinge at origin (0,0,0))."""
    # Local Y is forward from hinge, Z is up
    dy_front = P.ARM_FRONT_Y - P.HINGE_Y   # ~66 mm
    dz_front = P.ARM_FRONT_Z - P.HINGE_Z   # ~-15 mm
    # Smooth curved top profile matching the chassis arch
    top_pts = [
        (-4.0, 2.0),
        (10.0, 5.5),
        (28.0, 5.0),
        (46.0, 0.0),
        (dy_front, dz_front + 2.0),
    ]
    with BuildSketch(Plane.YZ) as sk:
        with BuildLine():
            Line((-4.0, -4.0), (dy_front - 10.0, dz_front - 3.0))
            Line((dy_front - 10.0, dz_front - 3.0), (dy_front, dz_front + 2.0))
            Spline(*reversed(top_pts))
            Line((-4.0, 2.0), (-4.0, -4.0))
        make_face()
    arm = extrude(sk.sketch, amount=P.ARM_W / 2.0, both=True)
    # Hinge pin bore at origin
    bore = Cylinder(radius=P.HINGE_PIN_D / 2.0 + 0.1, height=P.ARM_W + 2.0).rotate(Axis.Y, 90)
    arm = arm - bore
    return arm


def build_scoop():
    """Brushed metal trapezoidal front flipper scoop in local frame (flat in XY, thickness Z)."""
    # Local Y: 0 = front leading edge, -SCOOP_LEN = top edge
    hw_bot = P.SCOOP_BOT_W / 2.0
    hw_top = P.SCOOP_TOP_W / 2.0
    pts = [
        (-hw_bot, 0.0),
        (hw_bot, 0.0),
        (hw_top, -P.SCOOP_LEN),
        (-hw_top, -P.SCOOP_LEN),
    ]
    sk = Polygon(*pts, align=None)
    scoop = extrude(sk, amount=P.SCOOP_T / 2.0, both=True)

    # 4 mounting holes in a 2x2 diamond cluster near top-center (matching reference.png)
    for dx, dy in [(-4.0, -P.SCOOP_LEN + 5.0), (4.0, -P.SCOOP_LEN + 5.0),
                   (-3.5, -P.SCOOP_LEN + 11.0), (3.5, -P.SCOOP_LEN + 11.0)]:
        hole = Cylinder(radius=P.M2_CLEAR_D / 2.0, height=P.SCOOP_T + 1.0).translate((dx, dy, 0.0))
        scoop = scoop - hole
    return scoop


def build_hinge_pin():
    """Steel hinge pin along X."""
    return Cylinder(radius=P.HINGE_PIN_D / 2.0, height=P.TUB_W - 4.0).rotate(Axis.Y, 90)


def build_horn():
    """Printed servo horn."""
    return Box(6.0, 14.0, 3.0).translate((0.0, 5.0, 0.0))
