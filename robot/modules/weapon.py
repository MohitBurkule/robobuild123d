"""Spinner weapon module: laser-cut disc/bar on a catalogue outrunner (UNTESTED: written without running).

Masters: motor id, weapon shape ('disc' | 'bar'), tip radius, sheet thickness, tooth count, orientation
('vertical' | 'horizontal'). Everything else derives from the motor's catalogue props (shaft dia, bell radius,
mount hole circle) or from those masters.

Module frame: spin axis along +Z for 'horizontal', along +X for 'vertical' (spin plane vertical, axis horizontal).
Origin = motor base back face (the 'chassis' mount). 'shaft' mount sits on the weapon mid-plane on the axis.
"""
from __future__ import annotations

import math
from dataclasses import dataclass

from build123d import (Box, BuildPart, BuildSketch, Circle, Location, Mode, Part, PolarLocations,
                       Rectangle, RegularPolygon, Rot, extrude)

from robot import catalog
from robot.modules.base import Mount, ModuleResult

STEEL_DENSITY_G_MM3 = 7.85e-3      # weapon sheet (hardened steel / AR500 class)
ALU_DENSITY_G_MM3 = 2.70e-3        # hub + mount plate
SCREW_CLEAR = 0.2                  # radial clearance over nominal screw dia
SHAFT_CLEAR = 0.05                 # weapon bore slip fit over shaft dia
TIP_CLEAR = 1.0                    # envelope margin past the swept tip circle


def _entry(cid: str):
    return next(e for e in catalog.builtin() if e.id == cid)


@dataclass
class WeaponModule:
    name: str = "weapon"
    motor: str = "gr1507"
    shape: str = "disc"                 # disc | bar
    orientation: str = "vertical"       # vertical | horizontal
    tip_r: float = 30.0                 # swept tip radius
    sheet_t: float = 3.0                # laser-cut sheet thickness
    teeth: int = 2
    plate_t: float = 2.0                # motor mount plate thickness

    def build(self) -> ModuleResult:
        if self.orientation not in ("vertical", "horizontal"):
            raise ValueError(f"orientation must be vertical|horizontal, got {self.orientation!r}")
        m = _entry(self.motor)
        p, shaft = m.props, (m.shaft or {})
        shaft_d = shaft.get("dia", 5.0)
        bell_r = p.get("bell_r", shaft_d * 2)
        body_len = (p["body_x"][1] - p["body_x"][0]) if "body_x" in p else shaft.get("len", 0.0)
        pcd, n_holes, screw_d, phase = (p.get("mount_holes") or [[4 * shaft_d, 4, 2.0, 0.0]])[0]

        # relations
        hub_r = bell_r                                   # hub matches bell OD so the disc clamps on the bell face
        hub_h = self.sheet_t                             # spacer: one sheet thickness between bell and weapon
        plate_r = pcd / 2 + 2 * screw_d                  # plate covers hole circle with 2d edge margin
        tooth_h = self.tip_r * 0.15                      # tooth depth as a fraction of tip radius
        body_r = self.tip_r - tooth_h                    # disc rim radius, teeth reach tip_r
        bar_w = 2 * hub_r                                # bar is as wide as the hub
        z_hub = self.plate_t + body_len                  # bell top along axis
        z_weapon = z_hub + hub_h                         # weapon lower face

        # motor mount plate (chassis side), screw holes on catalogue pitch circle, shaft-stub clearance
        with BuildPart() as plate:
            with BuildSketch():
                Circle(plate_r)
            extrude(amount=self.plate_t)
            with BuildSketch(Location((0, 0, self.plate_t))):
                with PolarLocations(pcd / 2, int(n_holes), start_angle=phase):
                    Circle(screw_d / 2 + SCREW_CLEAR)
                Circle(p.get("base_hub_r", shaft_d / 2) + SCREW_CLEAR)
            extrude(amount=-self.plate_t, mode=Mode.SUBTRACT)

        # hub / spacer
        with BuildPart() as hub:
            with BuildSketch(Location((0, 0, z_hub))):
                Circle(hub_r)
                Circle(shaft_d / 2 + SHAFT_CLEAR, mode=Mode.SUBTRACT)
            extrude(amount=hub_h)

        # weapon: constant-thickness 2D profile, extruded
        with BuildPart() as weapon:
            with BuildSketch(Location((0, 0, z_weapon))):
                if self.shape == "bar":
                    Rectangle(2 * self.tip_r, bar_w)
                else:
                    Circle(body_r)
                    with PolarLocations(body_r, self.teeth):
                        RegularPolygon(tooth_h * 2 / math.sqrt(3), 3)   # triangular tooth, apex reaches ~tip_r
                Circle(shaft_d / 2 + SHAFT_CLEAR, mode=Mode.SUBTRACT)
                with PolarLocations(p["top_holes"][0][0] / 2 if "top_holes" in p else hub_r / 2,
                                    int(p["top_holes"][0][1]) if "top_holes" in p else 0,
                                    start_angle=p["top_holes"][0][3] if "top_holes" in p else 0.0):
                    Circle(screw_d / 2 + SCREW_CLEAR, mode=Mode.SUBTRACT)
            extrude(amount=self.sheet_t)

        # orient: horizontal keeps axis on +Z; vertical lays axis onto +X
        orient = Location() if self.orientation == "horizontal" else Location(Rot(0, 90, 0))
        parts: dict[str, Part] = {k: orient * s.part for k, s in
                                  {"mount_plate": plate, "hub": hub, "weapon": weapon}.items()}

        mid = z_weapon + self.sheet_t / 2
        env_r = self.tip_r + TIP_CLEAR
        envelope = orient * Location((0, 0, mid)) * Box(2 * env_r, 2 * env_r, self.sheet_t + 2 * TIP_CLEAR)

        mass = (parts["weapon"].volume * STEEL_DENSITY_G_MM3
                + (parts["hub"].volume + parts["mount_plate"].volume) * ALU_DENSITY_G_MM3)
        return ModuleResult(
            name=self.name,
            parts=parts,
            mounts={
                "chassis": Mount("chassis", orient * Location(), "screw", f"m{screw_d:g}"),
                "shaft": Mount("shaft", orient * Location((0, 0, mid)), "revolute"),
            },
            envelope=envelope,
            bom=[self.motor] + ([p["rotor_part"]] if "rotor_part" in p else []),
            mass_g=mass + m.mass_g,
        )
