"""AntiC (150g antweight pneumatic flipper) CAD package."""
import build123d as bd
from . import chassis, drive, flipper, params, pneumatics

PARTS = (
    "baseplate",
    "side_rail_r",
    "side_rail_l",
    "bulkheads",
    "wheels",
    "gears",
    "buffer_tank",
    "hex_fitting",
    "pneumatic_ram",
    "flipper_plate",
    "wedge_tip",
    "front_skirt",
    "flipper_arms",
    "assembly",
)


def build(part: str = "assembly") -> bd.Shape:
    """Build a named part or the full AntiC assembly."""
    if part == "baseplate":
        return chassis.build_baseplate()
    if part == "side_rail_r":
        return chassis.build_side_rail(1)
    if part == "side_rail_l":
        return chassis.build_side_rail(-1)
    if part == "bulkheads":
        return chassis.build_bulkheads()
    if part == "wheels":
        return drive.build_wheels()
    if part == "gears":
        return drive.build_gears()
    if part == "buffer_tank":
        return pneumatics.build_buffer_tank()
    if part == "hex_fitting":
        return pneumatics.build_hex_fitting()
    if part == "pneumatic_ram":
        return pneumatics.build_pneumatic_ram()
    if part == "flipper_plate":
        return flipper.build_flipper_plate()
    if part == "wedge_tip":
        return flipper.build_wedge_tip()
    if part == "front_skirt":
        return flipper.build_front_skirt()
    if part == "flipper_arms":
        return flipper.build_flipper_arms()
    if part == "assembly":
        return bd.Compound(
            [
                chassis.build_baseplate(),
                chassis.build_side_rail(1),
                chassis.build_side_rail(-1),
                chassis.build_bulkheads(),
                drive.build_wheels(),
                drive.build_gears(),
                pneumatics.build_buffer_tank(),
                pneumatics.build_hex_fitting(),
                pneumatics.build_pneumatic_ram(),
                flipper.build_flipper_plate(),
                flipper.build_wedge_tip(),
                flipper.build_front_skirt(),
                flipper.build_flipper_arms(),
            ]
        )
    raise ValueError(f"Unknown AntiC part: {part!r}")
