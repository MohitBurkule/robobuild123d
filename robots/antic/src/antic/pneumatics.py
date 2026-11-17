"""Pneumatic system: buffer tank, blue anodized hex fitting, and flipper ram."""
import build123d as bd
from . import params as P


def build_buffer_tank() -> bd.Solid:
    """Transverse cylindrical CO2 / buffer tank."""
    with bd.BuildPart() as bp:
        with bd.Locations(bd.Location((0.0, P.TANK_Y, P.TANK_Z)) * bd.Rotation(0, 90, 0)):
            bd.Cylinder(radius=P.TANK_R, height=P.TANK_L)
            # End-cap recess
            with bd.Locations((0, 0, P.TANK_L / 2 - 1.5)):
                bd.Cylinder(radius=P.TANK_R * 0.68, height=4.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_hex_fitting() -> bd.Solid:
    """Blue anodized hex fitting / nut on the right side of the pneumatic manifold."""
    with bd.BuildPart() as bp:
        with bd.Locations(bd.Location((36.5, -10.5, 27.5)) * bd.Rotation(0, 90, 0)):
            # Threaded boss
            bd.Cylinder(radius=4.2, height=10.0)
            # Hex nut head
            with bd.Locations((0, 0, 3.5)):
                with bd.BuildSketch():
                    bd.RegularPolygon(radius=P.HEX_NUT_R, side_count=6)
                bd.extrude(amount=P.HEX_NUT_T)
            # Center port bore
            bd.Cylinder(radius=1.8, height=16.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_pneumatic_ram() -> bd.Solid:
    """Forward-angled blue pneumatic actuator cylinder and piston rod."""
    with bd.BuildPart() as bp:
        with bd.Locations(bd.Location((0.0, 4.0, 14.0)) * bd.Rotation(54, 0, 0)):
            # Blue cylinder barrel
            bd.Cylinder(radius=P.RAM_R, height=P.RAM_L * 0.7)
            # Piston rod extending forward-upward
            with bd.Locations((0, 0, P.RAM_L * 0.35 + 4.0)):
                bd.Cylinder(radius=2.2, height=10.0)
    return bp.part
