"""Limpet XXT assembly: the tub is the datum; moving parts are placed in world coordinates at rest and carry their
motion in the spec joints (flipper revolute at the hinge, horn revolute at the servo output, wheels free on the axles).

`build(part=...)` is the geometry entry point the spec's model shapes call; `cots()` returns the catalogue parts with
their world poses for the spec.
"""
import build123d as bd

from .params import *  # noqa: F401,F403
from . import parts as P

PARTS = {
    "tub": P.tub,
    "lid_r": P.lid_right,
    "lid_l": P.lid_left,
    "side_r": P.side_plate_right,
    "side_l": P.side_plate_left,
    "flipper": P.flipper,
    "hinge_block": P.hinge_block,
    "horn": P.horn,
    "drive_pin": P.drive_pin,
    "hinge_pin": P.hinge_pin,
    "wheel_fl": lambda: P.wheel(True, True),
    "wheel_fr": lambda: P.wheel(True, False),
    "wheel_rl": lambda: P.wheel(False, True),
    "wheel_rr": lambda: P.wheel(False, False),
}


def build(part="tub", **_kw):
    if part not in PARTS:
        raise KeyError(f"unknown Limpet part `{part}`; one of {sorted(PARTS)}")
    return PARTS[part]()


def cots():
    """Catalogue parts as {name: (catalog_id, build123d Location)} in world coordinates."""
    out = {}
    for front in (True, False):
        for left in (True, False):
            name = f"motor_{'f' if front else 'r'}{'l' if left else 'r'}"
            out[name] = (DRIVE_MOTOR_ID, P.motor_pose(front, left))
    sw_z = P.switch_z()
    out.update({
        "servo": (SERVO_ID, P.servo_pose()),
        "battery": (BATTERY_ID, bd.Pos(BAT_X, 0, TUB_Z0 + WALL + BAT_H / 2)),
        "esc": (ESC_ID, bd.Pos(ESC_X, SIDE_ZONE_Y, TUB_Z0 + WALL + ESC_H / 2)),
        "switch": (SWITCH_ID, bd.Pos(SW_X, -SIDE_ZONE_Y, sw_z)),
    })
    return out


def made_parts():
    """{name: (solid, kind)} for every fabricated part, in world coordinates at rest."""
    made = {name: (fn(), "print" if name in ("tub", "hinge_block", "horn") else
                   ("tyre" if name.startswith("wheel_") else "sheet")) for name, fn in PARTS.items()}
    made["hinge_pin"] = (P.hinge_pin(), "print")
    return made


def mass_report(made):
    fab = {k: v for k, v in made.items() if v[1] != "cots"}
    return P.mass_g(fab)


def export(out_dir, flip_deg=START_FLIP_DEG):
    """STEP of the assembly + one STL per fabricated part."""
    import os
    os.makedirs(out_dir, exist_ok=True)
    made = made_parts()
    for name, (cid, loc) in cots().items():
        made[name] = (P.catalog_solid(cid).moved(loc), "cots")
    bd.export_step(bd.Compound(children=[s for s, _ in made.values()]), os.path.join(out_dir, "limpet_xxt.step"))
    for name, (solid, kind) in made.items():
        if kind != "cots":
            bd.export_stl(solid, os.path.join(out_dir, f"{name}.stl"))
    return made
