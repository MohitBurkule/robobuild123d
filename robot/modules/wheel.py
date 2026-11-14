"""Wheel module: printed hub + tyre (UNTESTED: written without running).

Frame (catalogue convention): axle along +X, origin at the wheel centre. Sizes come from a catalogue wheel
(`props.diameter_mm` / `props.width_mm`) or from the masters; the bore comes from the motor shaft (`entry.shaft.dia`).
"""
from __future__ import annotations

from dataclasses import dataclass

from build123d import Axis, Box, Cylinder, Location, Rot

from robot import catalog
from robot.modules.base import Module, Mount, ModuleResult

BORE_CLEARANCE_MM = 0.1        # press/slip fit on the shaft
HUB_TO_TYRE_RATIO = 0.68       # hub outer d as a fraction of tyre d (catalogue 19/28)
TYRE_HUB_OVERLAP_MM = 0.5      # tyre inner radius sits this far inside the hub (grip, one solid seat)
D_FLAT_FRACTION = 0.3          # D-flat depth as a fraction of shaft d
DEFAULT_SHAFT_D_MM = 3.0       # N20 / micro-metal shaft when no motor is given


def _x_cyl(r: float, length: float):
    """Cylinder with its axis on X, centred on the origin (catalogue frame)."""
    return Rot(0, 90, 0) * Cylinder(r, length)


@dataclass
class Wheel(Module):
    name: str = "wheel"
    wheel_id: str | None = "wheel_28x10"   # catalogue wheel; None -> use the masters
    motor_id: str | None = None            # bore from this motor's shaft
    diameter_mm: float = 28.0              # master (used only when wheel_id is None)
    width_mm: float = 10.0                 # master (used only when wheel_id is None)
    d_flat: bool = True

    def _dims(self):
        if self.wheel_id:
            p = catalog.find(self.wheel_id).props
            return p["diameter_mm"], p["width_mm"]
        return self.diameter_mm, self.width_mm

    def shaft_d(self) -> float:
        if self.motor_id:
            sh = catalog.find(self.motor_id).shaft or {}
            return sh.get("dia", DEFAULT_SHAFT_D_MM)
        return DEFAULT_SHAFT_D_MM

    def build(self) -> ModuleResult:
        dia, width = self._dims()
        hub_r = dia * HUB_TO_TYRE_RATIO / 2
        shaft_d = self.shaft_d()
        bore_r = shaft_d / 2 + BORE_CLEARANCE_MM
        hub = _x_cyl(hub_r, width) - _x_cyl(bore_r, width)
        if self.d_flat:
            flat_depth = shaft_d * D_FLAT_FRACTION
            # key fills the bore above (r - flat_depth): the D-flat the shaft mates
            key = Location((0, 0, bore_r - flat_depth / 2)) * Box(width, 2 * bore_r, flat_depth)
            hub = hub + (key & _x_cyl(bore_r, width))
        tyre = _x_cyl(dia / 2, width) - _x_cyl(hub_r - TYRE_HUB_OVERLAP_MM, width)
        mounts = {
            "axle": Mount("axle", Location((-width / 2, 0, 0)), kind="revolute"),   # inner face, +X out
            "ground": Mount("ground", Location((0, 0, -dia / 2))),
        }
        return ModuleResult(self.name, {"hub": hub, "tyre": tyre}, mounts,
                            envelope=_x_cyl(dia / 2, width), bom=[self.wheel_id] if self.wheel_id else [],
                            mass_g=catalog.find(self.wheel_id).mass_g if self.wheel_id else 0.0)
