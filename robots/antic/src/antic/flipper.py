"""3-part layered flipper/wedge assembly: black upper plate, pink tip, clear skirt, and internal arms."""
import math
import build123d as bd
from . import params as P

_DY = P.FRONT_TIP_Y - P.HINGE_Y
_DZ = P.HINGE_Z - P.FRONT_TIP_Z
SLOPE_DEG = math.degrees(math.atan2(_DZ, _DY))


def _wedge_plane(offset_n: float = 0.0) -> bd.Plane:
    """Plane aligned with the flipper slope, origin at hinge (0, HINGE_Y, HINGE_Z)."""
    return bd.Plane(
        origin=(0.0, P.HINGE_Y, P.HINGE_Z),
        x_dir=(1.0, 0.0, 0.0),
        z_dir=(0.0, math.sin(math.radians(SLOPE_DEG)), math.cos(math.radians(SLOPE_DEG))),
    ).offset(offset_n)


def build_flipper_plate() -> bd.Solid:
    """Upper black textured flipper plate with 4 silver socket-head screws."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(_wedge_plane(0.0)):
            bd.Polygon(
                [
                    (-P.WEDGE_W / 2, 0.0),
                    (P.WEDGE_W / 2, 0.0),
                    (P.WEDGE_W / 2, 48.0),
                    (22.0, 35.0),
                    (-22.0, 35.0),
                    (-P.WEDGE_W / 2, 48.0),
                ]
            )
        bd.extrude(amount=P.FLIPPER_T)
        for sx, sy in ((-18.0, 14.0), (18.0, 14.0), (-20.0, 30.0), (20.0, 30.0)):
            with bd.BuildSketch(_wedge_plane(0.5)):
                with bd.Locations((sx, sy)):
                    bd.Circle(radius=2.1)
            bd.extrude(amount=-1.5, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_wedge_tip() -> bd.Solid:
    """Pink/magenta anodized aluminum front wedge tip flush with the upper flipper plate."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(_wedge_plane(0.0)):
            bd.Polygon(
                [
                    (-P.WEDGE_W / 2, 48.0),
                    (-22.0, 35.0),
                    (22.0, 35.0),
                    (P.WEDGE_W / 2, 48.0),
                    (P.WEDGE_W / 2, 62.0),
                    (-P.WEDGE_W / 2, 62.0),
                ]
            )
        bd.extrude(amount=P.FLIPPER_T)
        for sx, sy in ((-14.0, 40.0), (14.0, 40.0)):
            with bd.BuildSketch(_wedge_plane(0.5)):
                with bd.Locations((sx, sy)):
                    bd.Circle(radius=1.9)
            bd.extrude(amount=-1.5, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_front_skirt() -> bd.Solid:
    """Translucent UHMW/polycarbonate ground-scraping front lip."""
    with bd.BuildPart() as bp2:
        with bd.BuildSketch(_wedge_plane(-0.2)):
            with bd.Locations((0.0, 61.5)):
                bd.Rectangle(P.WEDGE_W, 16.0, align=(bd.Align.CENTER, bd.Align.MIN))
        bd.extrude(amount=P.SKIRT_T)
    return bp2.part


def build_flipper_arms() -> bd.Compound:
    """Twin internal linkage arms + 6 silver screw heads visible on top of the flipper/wedge."""
    solids = []
    for sx in (-1, 1):
        with bd.BuildPart() as bp:
            with bd.BuildSketch(bd.Plane.YZ.offset(sx * 16.0 - 2.0)):
                bd.Polygon(
                    [
                        (P.HINGE_Y + 4.0, P.HINGE_Z - 6.0),
                        (22.0, 18.0),
                        (20.0, 14.0),
                        (P.HINGE_Y + 4.0, P.HINGE_Z - 11.0),
                    ]
                )
            bd.extrude(amount=4.0)
        solids.append(bp.part)
    # 6 silver screw heads on top of the flipper plate and pink wedge tip
    for sx, sy in ((-18.0, 14.0), (18.0, 14.0), (-20.0, 30.0), (20.0, 30.0), (-14.0, 40.0), (14.0, 40.0)):
        with bd.BuildPart() as sp:
            with bd.BuildSketch(_wedge_plane(0.2)):
                with bd.Locations((sx, sy)):
                    bd.Circle(radius=1.8)
            bd.extrude(amount=-1.1)
        solids.append(sp.part)
    return bd.Compound(solids)
