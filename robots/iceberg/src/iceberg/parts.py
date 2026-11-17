"""Build123d solid generators for every custom part of Iceberg."""
from __future__ import annotations

import math
from build123d import (
    Axis,
    Box,
    BuildPart,
    BuildSketch,
    Circle,
    Cylinder,
    Locations,
    Mode,
    Plane,
    Polygon,
    RectangleRounded,
    SlotOverall,
    extrude,
    fillet,
)

from . import params as P

PLATE_SCREW_XY = [
    (-28.0, -47.0), (28.0, -47.0),
    (-30.0, -14.0), (30.0, -14.0),
    (-28.0, 19.0), (28.0, 19.0),
]


def build_bottom_plate():
    yc = 0.5 * (P.CHASSIS_Y_MIN + P.CHASSIS_Y_MAX)
    with BuildPart() as bp:
        with BuildSketch(Plane.XY.offset(P.BOT_PLATE_Z0)):
            with Locations((0.0, yc)):
                RectangleRounded(2 * P.BODY_X_HALF, P.CHASSIS_LEN, 4.0)
            with Locations(*PLATE_SCREW_XY):
                Circle(1.1, mode=Mode.SUBTRACT)
            for sx in (-16.0, 16.0):
                with Locations((sx, -14.0)):
                    RectangleRounded(12.0, 44.0, 3.0, mode=Mode.SUBTRACT)
        extrude(amount=P.PLATE_T)
    return bp.part


def build_top_plate():
    yc = 0.5 * (P.CHASSIS_Y_MIN + P.CHASSIS_Y_MAX)
    with BuildPart() as bp:
        with BuildSketch(Plane.XY.offset(P.TOP_PLATE_Z0)):
            with Locations((0.0, yc)):
                RectangleRounded(2 * P.BODY_X_HALF, P.CHASSIS_LEN, 4.0)
            with Locations(*PLATE_SCREW_XY):
                Circle(1.1, mode=Mode.SUBTRACT)
            up_pts = [
                (-P.UPRIGHT_TAB_X, -6.0), (-P.UPRIGHT_TAB_X, 14.0),
                (P.UPRIGHT_TAB_X, -6.0), (P.UPRIGHT_TAB_X, 14.0),
            ]
            with Locations(*up_pts):
                Circle(1.1, mode=Mode.SUBTRACT)
            # Switch access slot
            with Locations((P.SW_AT[0], P.SW_AT[1])):
                SlotOverall(9.0, 4.5, rotation=0, mode=Mode.SUBTRACT)
            # Weapon ESC phase wire pass-through hole
            with Locations((11.5, 4.0)):
                RectangleRounded(4.0, 4.0, 1.0, mode=Mode.SUBTRACT)
            # Spinner disc clearance slot (y = -19 .. 24)
            with Locations((P.WPN_DISC_X, 2.5)):
                RectangleRounded(8.0, 43.0, 2.0, mode=Mode.SUBTRACT)
        extrude(amount=P.PLATE_T)
    return bp.part


def build_tub():
    yc = 0.5 * (P.CHASSIS_Y_MIN + P.CHASSIS_Y_MAX)
    h = P.CAVITY_Z1 - P.CAVITY_Z0
    with BuildPart() as bp:
        with BuildSketch(Plane.XY.offset(P.CAVITY_Z0)):
            with Locations((0.0, yc)):
                RectangleRounded(2 * P.TUB_X_HALF, P.CHASSIS_LEN - 2.0, 3.0)
            # Carve large central electronics & motor cavity (y=-45.5..+14.5, clears rear N10 motors at -44..-32)
            with Locations((0.0, -15.5)):
                RectangleRounded(60.5, 61.5, 3.0, mode=Mode.SUBTRACT)
            # Carve rear battery/ESC bay between rear motors (leave 2.0 mm rear wall)
            with Locations((0.0, -30.0)):
                RectangleRounded(20.0, 38.0, 2.0, mode=Mode.SUBTRACT)
            # Carve front weapon clearance cavity (y=1..21, leaving 2.0 mm front wall at y=21..23)
            with Locations((0.0, 11.0)):
                RectangleRounded(24.0, 20.0, 2.0, mode=Mode.SUBTRACT)
        extrude(amount=h)

        # Cut wheel/motor shaft windows ONLY through middle z (7.0..19.0), keeping continuous top & bottom rails!
        for sx in (-1.0, 1.0):
            for wy in (P.WHEEL_REAR_Y, P.WHEEL_FRONT_Y):
                with Locations((sx * (P.TUB_X_HALF - 2.0), wy, P.AXLE_Z)):
                    Box(10.0, 14.0, 12.0, mode=Mode.SUBTRACT)

        # Cut spinner disc slot through top/front of tub (z=11.5..23.5, y=-19..26)
        with Locations((P.WPN_DISC_X, 3.5, 17.5)):
            Box(8.0, 45.0, 12.0, mode=Mode.SUBTRACT)

        # Lateral standoff bosses for blue TPU side guards (3 per side, stop cleanly at GUARD_X_IN)
        for sx in (-1.0, 1.0):
            boss_len = P.GUARD_X_IN - P.TUB_X_HALF
            cx = sx * (P.TUB_X_HALF + 0.5 * boss_len)
            for gy, gz in ((P.GUARD_MOUNT_Y1, P.GUARD_MOUNT_Z), (P.GUARD_MOUNT_Y2, P.GUARD_MOUNT_Z), (P.GUARD_MOUNT_Y3, P.GUARD_MOUNT_Z3)):
                with Locations((cx, gy, gz)):
                    Box(boss_len, 3.0, 4.0)
                    Cylinder(0.85, boss_len + 2.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)

        # Internal bosses for middle plate screws (x=+-30.0, y=-14.0, inner edge at 28.2 clears drive_rx at -27.7)
        for sx in (-1.0, 1.0):
            with Locations((sx * 30.1, -14.0, P.CAVITY_Z0 + 0.5 * h)):
                Box(3.8, 4.5, h)

        # Printed nylon baffle wall between battery (y<=-12) and weapon bay, tied to side walls at z=3.5..6.0
        with Locations((0.0, -10.5, P.CAVITY_Z0 + 5.5)):
            Box(20.0, 1.5, 11.0)
        with Locations((0.0, -10.5, P.CAVITY_Z0 + 1.25)):
            Box(62.0, 1.5, 2.5)

        # Snug battery pocket ribs tied to battery bay walls (x=+-10.0)
        for sx in (-1.0, 1.0):
            with Locations((sx * 9.5, -30.0, 9.5)):
                Box(2.0, 20.0, 12.0)
        for by in (-43.0, -16.0):
            with Locations((0.0, by, 18.6)):
                Box(22.0, 3.0, 7.8)

        # Snug drive_rx pocket ribs tied to left outer wall (x=-30.0)
        with Locations((-23.5, -15.2, 6.0)):
            Box(13.5, 3.0, 5.0)
        with Locations((-23.5, -15.2, 18.5)):
            Box(13.5, 3.0, 8.0)

        # Snug weapon_esc pocket ribs tied to right outer wall (x=+30.0)
        with Locations((23.5, -11.0, 5.45)):
            Box(13.5, 4.0, 3.9)
        with Locations((23.5, -11.0, 17.55)):
            Box(13.5, 4.0, 9.9)
        with Locations((28.4, -11.0, 10.0)):
            Box(3.6, 6.0, 4.0)
        with Locations((20.5, 0.95, 10.0)):
            Box(19.0, 0.3, 4.0)

        # Snug xt30 pocket ribs tied to right outer wall (x=+30.0)
        with Locations((23.5, -27.0, 4.1)):
            Box(13.5, 3.0, 1.2)
        with Locations((23.5, -27.0, 17.9)):
            Box(13.5, 3.0, 9.2)
        with Locations((27.2, -27.0, 9.0)):
            Box(6.0, 3.0, 4.0)

        # N10 motor saddles & full-width Y walls (boxing all 4 motors along Z, Y, and inner X)
        for sx in (-1.0, 1.0):
            for wy in (P.WHEEL_REAR_Y, P.WHEEL_FRONT_Y):
                for mx, mw in ((14.5, 3.0), (27.5, 5.0)):
                    with Locations((sx * mx, wy, 5.75)):
                        Box(mw, 12.0, 4.5)
                    with Locations((sx * mx, wy, 20.25)):
                        Box(mw, 12.0, 4.5)
                for dy in (-6.45, 6.45):
                    with Locations((sx * 20.5, wy + dy, P.CAVITY_Z0 + 0.5 * h)):
                        Box(19.0, 0.9, h)

        # Front fork mount bosses + socket lip (z=3.5..16.7, pocket y=21.75..24.25)
        for sx in (-1.0, 1.0):
            with Locations((sx * P.FORK_X, 24.5, 10.1)):
                Box(9.4, 3.0, 13.2)
            with Locations((sx * P.FORK_X, 23.0, 9.75)):
                Box(7.2, 2.5, 11.7, mode=Mode.SUBTRACT)
            with Locations((sx * P.FORK_X, 22.0, 12.0)):
                Cylinder(0.85, 6.0, rotation=(90, 0, 0), mode=Mode.SUBTRACT)

        # Screw holes in top & bottom faces for plate & upright M2 screws
        for px, py in PLATE_SCREW_XY:
            with Locations((px, py, P.CAVITY_Z0 + 0.5 * h)):
                Cylinder(0.85, h + 1.0, mode=Mode.SUBTRACT)
        for sx in (-1.0, 1.0):
            for py in (-6.0, 14.0):
                with Locations((sx * P.UPRIGHT_TAB_X, py, P.CAVITY_Z1 - 3.0)):
                    Cylinder(0.85, 7.0, mode=Mode.SUBTRACT)
    return bp.part


def build_upright(side: int = 1):
    pts = [
        (-13.0, P.UPRIGHT_Z0),
        (22.0, P.UPRIGHT_Z0),
        (22.0, 34.0),
        (P.UPRIGHT_TOP_Y + 4.5, P.UPRIGHT_TOP_Z + 1.0),
        (P.UPRIGHT_TOP_Y - 4.5, P.UPRIGHT_TOP_Z + 1.0),
        (-9.0, 56.0),
        (-13.5, 53.0),
        (-11.5, 49.0),
        (-13.0, P.UPRIGHT_Z0),
    ]
    with BuildPart() as bp:
        with BuildSketch(Plane.YZ):
            Polygon(*pts, align=None)
            with Locations((P.UPRIGHT_TOP_Y, P.UPRIGHT_TOP_Z)):
                Circle(1.1, mode=Mode.SUBTRACT)
            with Locations((0.5, 55.0)):
                Circle(4.2, mode=Mode.SUBTRACT)
            with Locations((P.WPN_Y, P.WPN_Z)):
                Circle(4.0 if side < 0 else 2.55, mode=Mode.SUBTRACT)
            if side > 0:
                # 4x M2 holes on 12 mm circle for GR1507 stator
                for ang in (0, 90, 180, 270):
                    a = math.radians(ang)
                    with Locations((P.WPN_Y + 6.0 * math.cos(a), P.WPN_Z + 6.0 * math.sin(a))):
                        Circle(1.1, mode=Mode.SUBTRACT)
            else:
                # 4x M2/hex1.5 driver access holes on 4.5 mm radius (for GR1507 bell cap screws)
                for ang in (54.889, 144.889, 234.889, 324.889):
                    a = math.radians(ang)
                    with Locations((P.WPN_Y + 4.5 * math.cos(a), P.WPN_Z + 4.5 * math.sin(a))):
                        Circle(2.0, mode=Mode.SUBTRACT)
        extrude(amount=0.5 * P.UPRIGHT_T, both=True)

        dx_tab = side * (P.UPRIGHT_TAB_X - P.UPRIGHT_X_MID)
        with Locations((0.5 * dx_tab, 4.0, P.UPRIGHT_Z0 + 1.5)):
            Box(abs(dx_tab) + 4.0, 28.0, 3.0)
        for py in (-6.0, 14.0):
            with Locations((dx_tab, py, P.UPRIGHT_Z0 + 1.5)):
                Cylinder(1.1, 4.0, mode=Mode.SUBTRACT)
        tab_y_edges = [
            e for e in bp.edges().filter_by(Axis.Y)
            if abs(e.center().Z - (P.UPRIGHT_Z0 + 3.0)) < 0.2 and abs(e.center().X - side * 0.5 * P.UPRIGHT_T) < 0.2
        ]
        if tab_y_edges:
            fillet(tab_y_edges, radius=1.1)
        upper_x_edges = [e for e in bp.edges().filter_by(Axis.X) if e.center().Z > P.UPRIGHT_Z0 + 3.5]
        if upper_x_edges:
            fillet(upper_x_edges, radius=0.6)
    return bp.part


def build_top_rod():
    span = 2 * P.UPRIGHT_X_IN
    with BuildPart() as bp:
        Cylinder(P.TOP_ROD_R, span, rotation=(0, 90, 0))
        Cylinder(0.85, span + 1.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
    return bp.part


def build_weapon_shaft():
    with BuildPart() as bp:
        with Locations((-1.6, 0.0, 0.0)):
            Cylinder(P.WPN_SHAFT_R, 31.8, rotation=(0, 90, 0))
    return bp.part


def build_weapon_disc():
    r_out = P.WPN_DISC_R
    with BuildPart() as bp:
        with BuildSketch(Plane.YZ):
            Circle(r_out)
            with Locations((r_out * 0.65, r_out * 0.55)):
                Polygon((-6, -2), (10, -2), (10, 12), (-2, 12), align=None, mode=Mode.SUBTRACT)
            Circle(P.WPN_SHAFT_R + 0.05, mode=Mode.SUBTRACT)
            for ang in (15, 105, 195, 285):
                a = math.radians(ang)
                with Locations((17.0 * math.cos(a), 17.0 * math.sin(a))):
                    Circle(7.2, mode=Mode.SUBTRACT)
        extrude(amount=0.5 * P.WPN_DISC_T, both=True)
        fillet(bp.edges().filter_by(Axis.X), radius=0.5)
    return bp.part


def build_weapon_hub():
    with BuildPart() as bp:
        Cylinder(13.0, 1.5, rotation=(0, 90, 0))
        with Locations((2.0, 0.0, 0.0)):
            Cylinder(5.0, 3.0, rotation=(0, 90, 0))
        Cylinder(P.WPN_SHAFT_R + 0.05, 8.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
    return bp.part


def build_guard():
    t = P.GUARD_X_OUT - P.GUARD_X_IN
    pts = [
        (P.GUARD_Y_MIN + 8.0, P.GUARD_Z0),
        (P.GUARD_Y_MAX - 8.0, P.GUARD_Z0),
        (P.GUARD_Y_MAX, P.GUARD_Z0 + 6.0),
        (P.GUARD_Y_MAX - 2.0, P.GUARD_Z1),
        (P.GUARD_Y_MIN + 8.0, P.GUARD_Z1),
        (P.GUARD_Y_MIN, 0.5 * (P.GUARD_Z0 + P.GUARD_Z1)),
    ]
    with BuildPart() as bp:
        with BuildSketch(Plane.YZ):
            Polygon(*pts, align=None)
            with Locations((-15.0, 12.0)):
                RectangleRounded(6.0, 6.0, 1.5, mode=Mode.SUBTRACT)
            for gy, gz in ((P.GUARD_MOUNT_Y1, P.GUARD_MOUNT_Z), (P.GUARD_MOUNT_Y2, P.GUARD_MOUNT_Z), (P.GUARD_MOUNT_Y3, P.GUARD_MOUNT_Z3)):
                with Locations((gy, gz)):
                    Circle(1.1, mode=Mode.SUBTRACT)
        extrude(amount=0.5 * t, both=True)
        fillet(bp.edges().filter_by(Axis.X), radius=0.8)
    return bp.part


def build_fork_mount():
    with BuildPart() as bp:
        with BuildSketch(Plane.YZ):
            Polygon(
                (P.FORK_MOUNT_Y0, 4.0),
                (P.FORK_MOUNT_Y1, 4.0),
                (P.FORK_MOUNT_Y1 - 2.0, 13.5),
                (P.FORK_MOUNT_Y0, 15.5),
                align=None,
            )
        extrude(amount=3.5, both=True)
        # Rear socket tang seating into tub pocket (y=22.0..24.0)
        with Locations((0.0, P.FORK_MOUNT_Y0 - 1.0, 9.75)):
            Box(6.8, 2.0, 11.3)
        # Cut flat vertical seat at y=26.5 for scr_fork_mount head
        with Locations((0.0, 31.0, 13.0)):
            Box(8.0, 9.0, 6.0, mode=Mode.SUBTRACT)
        with Locations((0.0, 31.0, 6.0)):
            Box(2.4, 9.5, 11.0, mode=Mode.SUBTRACT)
        with Locations((0.0, 26.25, 6.0)):
            Cylinder(1.2, 11.0, mode=Mode.SUBTRACT)
        with Locations((0.0, P.FORK_PIN_Y, P.FORK_PIN_Z)):
            Cylinder(1.05, 10.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
        with Locations((0.0, 25.5, 12.0)):
            Cylinder(1.1, 8.0, rotation=(90, 0, 0), mode=Mode.SUBTRACT)
    return bp.part


def build_fork():
    dy = P.FORK_LEN
    pts = [
        (P.FORK_PIN_Y, P.FORK_PIN_Z - 2.2),
        (P.FORK_PIN_Y + dy, P.FORK_TIP_Z),
        (P.FORK_PIN_Y + dy, P.FORK_TIP_Z + 0.6),
        (P.FORK_PIN_Y + dy - 4.0, P.FORK_TIP_Z + 2.2),
        (P.FORK_PIN_Y + 12.0, P.FORK_PIN_Z + 2.2),
        (P.FORK_PIN_Y, P.FORK_PIN_Z + 2.2),
    ]
    with BuildPart() as bp:
        with BuildSketch(Plane.YZ):
            Polygon(*pts, align=None)
            with Locations((P.FORK_PIN_Y, P.FORK_PIN_Z)):
                Circle(2.2)
                Circle(1.05, mode=Mode.SUBTRACT)
        extrude(amount=0.75, both=True)
    return bp.part


def build_wheel():
    with BuildPart() as bp:
        Cylinder(P.WHEEL_R, P.WHEEL_W, rotation=(0, 90, 0))
        with Locations((2.0, 0.0, 0.0)):
            Cylinder(8.5, 3.2, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
        Cylinder(1.55, P.WHEEL_W + 1.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
    return bp.part


def build_locking_bar():
    with BuildPart() as bp:
        Cylinder(1.5, 22.0, rotation=(0, 90, 0))
        with Locations((11.0, 0.0, 0.0)):
            Box(2.5, 6.0, 4.0)
    return bp.part


def build_bearing():
    with BuildPart() as bp:
        Cylinder(4.0, 3.0, rotation=(0, 90, 0))
        Cylinder(2.0, 4.0, rotation=(0, 90, 0), mode=Mode.SUBTRACT)
    return bp.part
