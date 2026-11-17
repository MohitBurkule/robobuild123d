"""Entry point for building Steve (Stewie) parts for robobuild123d."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from steve import parts as PP


def build(part: str = "tub"):
    """Build a named part in its local frame."""
    if part == "tub":
        return PP.build_tub()
    if part == "lid_l":
        return PP.build_lid(side=1)
    if part == "lid_r":
        return PP.build_lid(side=-1)
    if part == "guard_l":
        return PP.build_guard()
    if part == "guard_r":
        return PP.build_guard()
    if part == "wheel_l":
        return PP.build_wheel()
    if part == "wheel_r":
        return PP.build_wheel()
    if part == "flipper":
        return PP.build_flipper()
    if part == "scoop":
        return PP.build_scoop()
    if part == "hinge_pin":
        return PP.build_hinge_pin()
    if part == "horn":
        return PP.build_horn()
    raise ValueError(f"Unknown part: {part!r}")


if __name__ == "__main__":
    from build123d import export_stl

    out_dir = os.path.abspath(os.path.join(HERE, "..", "stl"))
    os.makedirs(out_dir, exist_ok=True)
    for name in ("tub", "lid_l", "lid_r", "guard_l", "guard_r", "wheel_l", "wheel_r", "flipper", "scoop", "hinge_pin", "horn"):
        solid = build(name)
        export_stl(solid, os.path.join(out_dir, f"{name}.stl"))
    print("Exported all Steve STLs to", out_dir)
