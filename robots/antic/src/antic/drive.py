"""4WD geared drivetrain: ribbed wheels, central spur gears, and axles."""
import build123d as bd
from . import params as P


def _toothed_wheel(radius: float, width: float, teeth: int = 24) -> bd.Solid:
    """Ribbed/toothed combat robot wheel with recessed hub."""
    with bd.BuildPart() as bp:
        bd.Cylinder(radius=radius - 0.8, height=width)
        for i in range(teeth):
            ang = 360.0 * i / teeth
            with bd.Locations(bd.Rotation(0, 0, ang) * bd.Location((radius - 0.6, 0, 0))):
                bd.Box(1.4, 1.3, width * 0.92)
        with bd.Locations((0, 0, width * 0.2)):
            bd.Cylinder(radius=radius * 0.55, height=width * 0.65, mode=bd.Mode.SUBTRACT)
        bd.Cylinder(radius=P.AXLE_R, height=width + 1.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def _spur_gear(radius: float, width: float, teeth: int = 16) -> bd.Solid:
    """Central spur gear meshing with front and rear wheels."""
    with bd.BuildPart() as bp:
        bd.Cylinder(radius=radius - 0.7, height=width)
        for i in range(teeth):
            ang = 360.0 * i / teeth
            with bd.Locations(bd.Rotation(0, 0, ang) * bd.Location((radius - 0.5, 0, 0))):
                bd.Box(1.5, 1.4, width)
        bd.Cylinder(radius=P.AXLE_R, height=width + 1.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_wheels() -> bd.Compound:
    """All 4 ribbed wheels (rear & front, left & right)."""
    w_base = _toothed_wheel(P.WHEEL_R, P.WHEEL_W)
    solids = []
    for sx in (-1, 1):
        rot = bd.Rotation(0, 90, 0) if sx > 0 else bd.Rotation(0, -90, 0)
        for wy in (P.WHEEL_REAR_Y, P.WHEEL_FRONT_Y):
            solids.append(w_base.moved(bd.Location((sx * P.WHEEL_X, wy, P.WHEEL_Z)) * rot))
    return bd.Compound(solids)


def build_gears() -> bd.Compound:
    """Central spur gears and axles on both sides."""
    g_base = _spur_gear(P.GEAR_R, P.GEAR_W)
    solids = []
    for sx in (-1, 1):
        rot = bd.Rotation(0, 90, 0)
        solids.append(g_base.moved(bd.Location((sx * P.WHEEL_X, P.GEAR_Y, P.GEAR_Z)) * rot))
        for (ay, az) in (
            (P.WHEEL_REAR_Y, P.WHEEL_Z),
            (P.GEAR_Y, P.GEAR_Z),
            (P.WHEEL_FRONT_Y, P.WHEEL_Z),
        ):
            with bd.BuildPart() as ax:
                with bd.Locations(bd.Location((sx * P.WHEEL_X, ay, az)) * rot):
                    bd.Cylinder(radius=P.AXLE_R - 0.1, height=P.WHEEL_W + 4.0)
            solids.append(ax.part)
    return bd.Compound(solids)
