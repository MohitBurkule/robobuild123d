"""Chassis tub, curved tank-hugging bulkheads, rear electronics bay, and side armor rails."""
import build123d as bd
from . import params as P


def build_baseplate() -> bd.Solid:
    """Flat bottom chassis plate spanning from rear to front wedge."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.XY.offset(P.BASE_Z)):
            bd.Polygon(
                [
                    (-32.0, -44.0),
                    (32.0, -44.0),
                    (32.0, 9.0),
                    (43.0, 16.0),
                    (43.0, 42.0),
                    (-43.0, 42.0),
                    (-43.0, 16.0),
                    (-32.0, 9.0),
                ]
            )
        bd.extrude(amount=P.BASE_T)
    return bp.part


def build_side_rail(side: int = 1) -> bd.Solid:
    """Angled green-titanium side armor rail with 4 countersunk screws (side = +1 right, -1 left)."""
    x_pos = side * P.SIDE_RAIL_X
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ.offset(x_pos - P.SIDE_RAIL_T / 2)):
            bd.Polygon(
                [
                    (-44.0, 5.5),
                    (44.0, 1.0),
                    (45.0, 3.0),
                    (16.0, 14.5),
                    (-44.0, 14.5),
                ]
            )
        bd.extrude(amount=P.SIDE_RAIL_T)
        for sy, sz in ((-38.0, 10.0), (-21.0, 10.0), (8.0, 10.0), (32.0, 5.5)):
            with bd.Locations(bd.Location((x_pos, sy, sz)) * bd.Rotation(0, 90, 0)):
                bd.Cylinder(radius=1.5, height=P.SIDE_RAIL_T + 0.4, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_bulkheads() -> bd.Solid:
    """Low curved tank-cradle bulkheads, top electronics frame, and front triangular wedge blocks."""
    with bd.BuildPart() as bp:
        # Left and right curved tank-arch side plates (X = +-30 mm)
        for s in (-1, 1):
            with bd.BuildSketch(bd.Plane.YZ.offset(s * 30.0 - 1.5)):
                bd.Polygon(
                    [
                        (-44.0, P.BASE_Z + P.BASE_T),
                        (16.0, P.BASE_Z + P.BASE_T),
                        (16.0, 22.0),
                        (-6.0, 32.0),
                        (-32.0, 32.0),
                        (-35.0, 43.0),
                        (-40.0, 43.0),
                        (-47.0, 24.0),
                        (-44.0, 22.0),
                    ]
                )
                # Circular arch around the buffer tank end-cap
                with bd.Locations((P.TANK_Y, P.TANK_Z)):
                    bd.Circle(radius=P.TANK_R + 2.2)
                # Cut out the circular window exposing the silver tank end-cap
                with bd.Locations((P.TANK_Y, P.TANK_Z)):
                    bd.Circle(radius=P.TANK_R - 1.2, mode=bd.Mode.SUBTRACT)
                # Cut away the upper-front portion of the ring so the top of the silver tank dome is exposed!
                with bd.Locations((P.TANK_Y + 3.0, P.TANK_Z + 10.5)):
                    bd.Rectangle(30.0, 14.0, mode=bd.Mode.SUBTRACT)
                # Wheel & gear arches at the bottom
                for wy in (P.WHEEL_REAR_Y, P.WHEEL_FRONT_Y):
                    with bd.Locations((wy, P.WHEEL_Z)):
                        bd.Circle(radius=P.WHEEL_R - 2.0, mode=bd.Mode.SUBTRACT)
            bd.extrude(amount=2.5)

        # Top electronics bay frame (sits over the rear-top of the silver tank, leaving front-top dome exposed)
        with bd.Locations((0.0, -28.0, 43.2)):
            bd.Box(63.0, 22.0, 3.5)
        with bd.Locations((0.0, -28.0, 43.2)):
            bd.Box(46.0, 15.0, 5.0, mode=bd.Mode.SUBTRACT)
        # Crossbars inside the top electronics tray
        for cy in (-33.0, -23.0):
            with bd.Locations((0.0, cy, 42.5)):
                bd.Box(58.0, 3.0, 2.0)

        # Enclosed lower rear plate between bulkheads so rear is solid
        with bd.Locations((0.0, -42.5, 16.0)):
            bd.Box(60.0, 3.0, 24.0)

        # Front triangular wedge support blocks
        for s in (-1, 1):
            with bd.BuildSketch(bd.Plane.YZ.offset(s * 36.0 - 2.5)):
                bd.Polygon(
                    [
                        (8.0, P.BASE_Z + P.BASE_T),
                        (42.0, P.BASE_Z + P.BASE_T),
                        (14.0, 24.0),
                    ]
                )
                bd.Polygon(
                    [
                        (13.0, P.BASE_Z + P.BASE_T + 2.5),
                        (32.0, P.BASE_Z + P.BASE_T + 2.5),
                        (16.0, 17.5),
                    ],
                    mode=bd.Mode.SUBTRACT,
                )
            bd.extrude(amount=5.0)

    return bp.part
