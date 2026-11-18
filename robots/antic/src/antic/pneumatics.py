"""Pneumatic system: buffer tank, angled blue hex fitting, and flipper ram."""
import build123d as bd
from . import params as P


def build_buffer_tank() -> bd.Solid:
    """Transverse cylindrical CO2 / buffer tank with recessed end-caps."""
    with bd.BuildPart() as bp:
        with bd.Locations(bd.Location((0.0, P.TANK_Y, P.TANK_Z)) * bd.Rotation(0, 90, 0)):
            bd.Cylinder(radius=P.TANK_R, height=56.5)
            for s in (-1, 1):
                with bd.Locations((0, 0, s * (28.25 - 2.0))):
                    bd.Cylinder(radius=P.TANK_R * 0.62, height=5.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_hex_fitting() -> bd.Solid:
    """Angled blue threaded stem with teal/cyan hex cap on the right side."""
    with bd.BuildPart() as bp:
        # Stem points backward-upward into the tank (-Y, +Z) and outward (+X) to the hex cap
        with bd.Locations(bd.Location((37.8, -5.5, 31.0)) * bd.Rotation(-35, 68, 15)):
            # Threaded blue stem
            bd.Cylinder(radius=3.6, height=12.0)
            # Hex nut cap at the outer/lower-front end
            with bd.Locations((0, 0, 4.5)):
                with bd.BuildSketch():
                    bd.RegularPolygon(radius=P.HEX_NUT_R, side_count=6)
                bd.extrude(amount=P.HEX_NUT_T)
            # Center port bore
            bd.Cylinder(radius=1.6, height=18.0, mode=bd.Mode.SUBTRACT)
    return bp.part


def build_pneumatic_ram() -> bd.Solid:
    """Forward-angled blue pneumatic actuator cylinder and piston rod."""
    with bd.BuildPart() as bp:
        with bd.Locations(bd.Location((0.0, 10.0, 15.0)) * bd.Rotation(54, 0, 0)):
            bd.Cylinder(radius=P.RAM_R, height=P.RAM_L * 0.6)
            with bd.Locations((0, 0, P.RAM_L * 0.3 + 4.0)):
                bd.Cylinder(radius=2.2, height=8.0)
    return bp.part
