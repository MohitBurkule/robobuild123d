"""DrivePod: catalogue gearmotor + clamp block + Wheel (UNTESTED: written without running).

Frame: motor axis on +X (catalogue frame), origin at the motor body centre. A left pod is `mirrored(right)`.
Mounts: 'chassis' (screw sites on the clamp base, -Z face) and 'axle' (the wheel's inner face on the shaft).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from build123d import Box, GridLocations, Location, Plane, Pos, mirror

from robot import catalog
from robot.modules.base import Module, Mount, ModuleResult
from robot.modules.wheel import Wheel

CLAMP_WALL_MM = 2.0            # clamp wall round the motor body
CLAMP_FIT_MM = 0.15            # clearance between body and clamp
CLAMP_LEN_FRACTION = 0.6       # clamp covers this share of the motor body length
SCREW_D_MM = 2.0               # M2 chassis screws
SCREW_FASTENER_ID = "m2_screw"
SCREW_EDGE_FACTOR = 2.0        # screw centre this many screw diameters in from the flange edge
FLANGE_WIDTH_FACTOR = 4.0      # flange sticks out this many screw diameters each side
WHEEL_GAP_MM = 1.0             # wheel inner face clear of the shaft root


def _body_bbox(entry):
    """Motor rigid body size (shaft excluded) from the catalogue solid: (len_x, w_y, h_z, shaft_root_x)."""
    from robot.cad.bay import derive_bay   # reuse bay's rigid-body logic; local import keeps load light
    bay = derive_bay(entry, insert_dir="+z")
    env = bay.required_envelope()
    bb = env.bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z, entry.shaft["at"][0]


@dataclass
class DrivePod(Module):
    name: str = "drive_pod"
    motor_id: str = "n10_2200rpm_spicy"
    wheel: Wheel = field(default_factory=Wheel)

    def build(self) -> ModuleResult:
        motor = catalog.find(self.motor_id)
        lx, wy, hz, shaft_root = _body_bbox(motor)
        clamp_len = lx * CLAMP_LEN_FRACTION
        cw = wy + 2 * (CLAMP_WALL_MM + CLAMP_FIT_MM)
        ch = hz + 2 * (CLAMP_WALL_MM + CLAMP_FIT_MM)
        flange_w = cw + 2 * FLANGE_WIDTH_FACTOR * SCREW_D_MM
        base_z = -ch / 2 + CLAMP_WALL_MM / 2
        block = Box(clamp_len, cw, ch) + Pos(0, 0, base_z) * Box(clamp_len, flange_w, CLAMP_WALL_MM)
        pocket = Box(lx + 2 * CLAMP_FIT_MM, wy + 2 * CLAMP_FIT_MM, hz + 2 * CLAMP_FIT_MM)
        screw_dx = clamp_len - 2 * SCREW_EDGE_FACTOR * SCREW_D_MM
        screw_dy = flange_w - 2 * SCREW_EDGE_FACTOR * SCREW_D_MM
        sites = [Pos(0, 0, -ch / 2) * loc for loc in GridLocations(screw_dx, screw_dy, 2, 2)]
        from build123d import Cylinder
        holes = [s * Pos(0, 0, CLAMP_WALL_MM / 2) * Cylinder(SCREW_D_MM / 2, CLAMP_WALL_MM) for s in sites]
        clamp = block - pocket
        for h in holes:
            clamp = clamp - h

        self.wheel.motor_id = self.motor_id
        wr = self.wheel.build()
        axle_at = Location((shaft_root + WHEEL_GAP_MM, 0, 0))
        wheel_at = axle_at * wr.mounts["axle"].location.inverse()
        parts = {"clamp": clamp, **{f"wheel_{k}": wheel_at * p for k, p in wr.parts.items()}}
        mounts = {"chassis": Mount("chassis", Location((0, 0, -ch / 2)), kind="screw", screw=SCREW_FASTENER_ID),
                  "axle": Mount("axle", axle_at, kind="revolute")}
        for i, s in enumerate(sites):
            mounts[f"chassis_screw_{i}"] = Mount(f"chassis_screw_{i}", s, kind="screw", screw=SCREW_FASTENER_ID)
        return ModuleResult(self.name, parts, mounts, bom=[self.motor_id, *wr.bom] + [SCREW_FASTENER_ID] * len(sites),
                            mass_g=motor.mass_g + wr.mass_g)


def mirrored(result: ModuleResult) -> ModuleResult:
    """Left pod from a right one: mirror solids across YZ (wheel on -X). Mount frames flip X position only."""
    parts = {k: mirror(p, Plane.YZ) for k, p in result.parts.items()}
    mounts = {}
    for k, m in result.mounts.items():
        x, y, z = m.location.position
        mounts[k] = Mount(m.name, Location((-x, y, z), (0, 0, 180)) if m.kind == "revolute" else Location((-x, y, z)),
                          m.kind, m.screw)
    return ModuleResult(result.name + "_mirrored", parts, mounts, result.envelope, list(result.bom), result.mass_g)
