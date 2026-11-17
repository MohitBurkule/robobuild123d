"""3-part layered flipper/wedge assembly: black upper plate, pink tip, clear skirt, and internal arms."""
import math
import build123d as bd
from . import params as P

# Slope angle from hinge (-10, 46) to front tip (52, 0.5)
_DY = P.FRONT_TIP_Y - P.HINGE_Y
_DZ = P.HINGE_Z - P.FRONT_TIP_Z
SLOPE_DEG = math.degrees(math.atan2(_DZ, _DY))  # ~36.3 deg


def _wedge_plane(offset_n: float = 0.0) -> bd.Plane:
    """Plane aligned with the flipper slope, origin at hinge (0, HINGE_Y, HINGE_Z)."""
    return bd.Plane(
        origin=(0.0, P.HINGE_Y, P.HINGE_Z),
        x_dir=(1.0, 0.0, 0.0),
        z_dir=(0.0, math.sin(math.radians(SLOPE_DEG)), math.cos(math.radians(SLOPE_DEG))),
    ).offset(offset_n)


def build_flipper_plate() -> bd.Solid:
    """Upper black textured flipper plate with 4 socket-head screw bosses."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(_wedge_plane(0.0)):
            bd.Polygon(
                [
                    (-P.WEDGE_W / 2, 0.0),
                    (P.WEDGE_W / 2, 0.0),
                    (P.WEDGE_W / 2, 46.0),
                    (22.0, 34.0),
                    (-22.0, 34.0),
                    (-P.WEDGE_W / 2, 46.0),
                ]
            )
        bd.extrude(amount=P.FLIPPER_T)
    return bp.part


def build_wedge_tip() -> bd.Solid:
    """Pink/magenta anodized aluminum front wedge tip."""
    with bd.BuildPart() as bp:
        with bd.BuildSketch(_wedge_plane(0.2)):
            bd.Polygon(
                [
                    (-P.WEDGE_W / 2, 46.0),
                    (-22.0, 34.0),
                    (22.0, 34.0),
                    (P.WEDGE_W / 2, 46.0),
                    (P.WEDGE_W / 2, 62.0),
                    (-P.WEDGE_W / 2, 62.0),
                ]
            )
        bd.extrude(amount=P.TIP_T)
    return bp.part


def build_front_skirt() -> bd.Solid:
    """Translucent UHMW/polycarbonate ground-scraping front lip."""
    with bd.BuildPart() as bp2:
        with bd.BuildSketch(_wedge_plane(-0.2)):
            with bd.Locations((0.0, 61.5)):
                bd.Rectangle(P.WEDGE_W, 15.0, align=(bd.Align.CENTER, bd.Align.MIN))
        bd.extrude(amount=P.SKIRT_T)
    return bp2.part


def build_flipper_arms() -> bd.Compound:
    """Twin internal linkage arms under the flipper plate (visible in white prototype)."""
    solids = []
    for sx in (-1, 1):
        with bd.BuildPart() as bp:
            with bd.BuildSketch(bd.Plane.YZ.offset(sx * 18.0 - 2.0)):
                bd.Polygon(
                    [
                        (P.HINGE_Y, P.HINGE_Z - 2.0),
                        (24.0, 20.0),
                        (22.0, 16.0),
                        (P.HINGE_Y, P.HINGE_Z - 8.0),
                    ]
                )
            bd.extrude(amount=4.0)
        solids.append(bp.part)
    return bd.Compound(solids)
