"""Example antweight (150 g) vertical spinner built from robot.modules (UNTESTED: written without running).

Everything is config: edit CONFIG, not geometry. Run (when allowed): python robots/example_modular/robot.py
"""
from __future__ import annotations

CONFIG = {
    "name": "example_vert_ant",
    "pods": {
        "type": "drive_pod",
        "kwargs": {"motor": "n20_300rpm", "wheel": {"diameter": 32.0, "width": 10.0}},
        "at": [-15.0, 32.0, 0.0],
        "mirror": True,
    },
    "weapon": {
        "type": "weapon",
        "kwargs": {"kind": "vertical_spinner", "disc_diameter": 60.0, "thickness": 6.0, "motor": "2204_brushless"},
        "at": [40.0, 0.0, 18.0],
    },
    "electronics": {
        "type": "electronics_bay",
        "kwargs": {"battery": "2s_300mah", "esc": "dual_esc_mini", "receiver": "rx_mini"},
        "at": [-10.0, 0.0, 4.0],
    },
    "tub": {"type": "tub", "kwargs": {"material": "tpu"}, "wall_mm": 2.5, "clearance_mm": 1.0},
    "mass_limit_g": 150.0,
}


def main() -> None:
    from robot.modules.compose import compose
    res = compose(CONFIG)
    print(f"{res['name']}: {res['mass_g']:.1f} g (limit {CONFIG['mass_limit_g']} g)")
    print("BOM:", ", ".join(res["bom"]))
    if res["assembly"] is not None:
        try:
            from build123d import export_step
            export_step(res["assembly"], "example_vert_ant.step")
        except Exception as e:  # noqa: BLE001
            print("export skipped:", e)


if __name__ == "__main__":
    main()
