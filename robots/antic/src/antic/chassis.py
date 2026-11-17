"""Chassis tub, internal bulkheads, rear electronics bay, and side armor rails."""
import build123d as bd
from . import params as P


def build_baseplate() -> bd.Solid:
    """Flat bottom chassis plate spanning from rear to front wedge."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.XY.offset(P.BASE_Z)):
            bd.Polygon(
                [
                    (-33.0, -45.0),
                    (33.0, -45.0),
                    (33.0, 2.0),
                    (44.0, 12.0),
                    (44.0, 38.0),
                    (-44.0, 38.0),
                    (-44.0, 12.0),
                    (-33.0, 2.0),
                ]
            )
        bd.extrude(amount=P.BASE_T)
    return bp.part


def build_side_rail(side: int = 1) -> bd.Solid:
    """Angled metal side armor rail (side = +1 right, -1 left)."""
    x_pos = side * P.SIDE_RAIL_X
    with bd.BuildPart() as bp:
        with bd.BuildSketch(bd.Plane.YZ.offset(x_pos - P.SIDE_RAIL_T / 2)):
            bd.Polygon(
                [
                    (-46.0, 6.0),
                    (36.0, 2.0),
                    (38.0, 5.0),
                    (10.0, 20.0),
                    (-44.0, 20.0),
                ]
            )
        bd.extrude(amount=P.SIDE_RAIL_T)
    return bp.part


def build_bulkheads() -> bd.Solid:
    """Internal 3D-printed bulkheads, tank cradle, and rear electronics bay frame."""
    with bd.BuildPart() as bp:
        # Left and right inner chassis walls (X = +-31 mm)
        for s in (-1, 1):
            with bd.BuildSketch(bd.Plane.YZ.offset(s * 31.0 - 1.5)):
                bd.Polygon(
                    [
                        (-45.0, P.BASE_Z + P.BASE_T),
                        (18.0, P.BASE_Z + P.BASE_T),
                        (18.0, 16.0),
                        (-10.0, 45.0),
                        (-38.0, 45.0),
                        (-46.0, 36.0),
                    ]
                )
            bd.extrude(amount=3.0)

        # Rear electronics bay top frame rails
        with bd.Locations((0.0, -35.0, 43.0)):
            bd.Box(64.0, 18.0, 3.0)
        with bd.Locations((0.0, -35.0, 43.0)):
            bd.Box(48.0, 14.0, 4.0, mode=bd.Mode.SUBTRACT)

        # Rear angled bumper/skirt
        with bd.BuildSketch(bd.Plane.YZ.offset(-31.0)):
            bd.Polygon(
                [
                    (-45.0, 36.0),
                    (-49.0, 22.0),
                    (-47.0, 22.0),
                    (-43.0, 36.0),
                ]
            )
        bd.extrude(amount=62.0)

        # Front wedge support gussets
        for s in (-1, 1):
            with bd.BuildSketch(bd.Plane.YZ.offset(s * 38.0 - 2.0)):
                bd.Polygon(
                    [
                        (8.0, P.BASE_Z + P.BASE_T),
                        (38.0, P.BASE_Z + P.BASE_T),
                        (12.0, 24.0),
                    ]
                )
            bd.extrude(amount=4.0)

    return bp.part
