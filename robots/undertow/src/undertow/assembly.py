"""Undertow assembly: every part in the robot frame, the front attachment by SETTINGS["front"].
UNTESTED: never built, run, rendered or verified.

Placement: tub, plates, drive and skirts are built in place from shared masters (the relation IS the mate: plates on
the tub faces, motors on the spine, wheels on the shafts, skirts on the wall pins). The front attachment is placed by
the shared pivot joint (front_mount.mount_joint) at its resting / start angle.
"""
import build123d as bd

from .settings import SETTINGS
from .params import UP_STOP_DEG, FORK_REST_DEG, PLOUGH_REST_DEG, START_FOLDED
from . import tub, panels, drive, skirts, front_mount, front_forks, front_plough

FRONTS = {"forks": front_forks.front, "plough": front_plough.front}


def parts(start_config=False):
    """{name: build123d shape}. start_config=True folds the attachment up (UP_STOP_DEG) only when rules="aws_v43_cube".
    NOTE: the folded pose is applied as an extra rotation about the pin; front_*.front() build the resting pose."""
    out = {"tub": tub.tub(), "top_plate": panels.top_plate()[0], "base_plate": panels.base_plate()[0]}
    for i, m in enumerate(drive.motors()):
        out[f"motor_{i}"] = m
    for i, w in enumerate(drive.wheels()):
        out[f"wheel_{i}"] = w
    out.update(skirts.skirts())
    front = FRONTS[SETTINGS["front"]]()
    if start_config and START_FOLDED:   # only the cube rule set starts folded; the square default starts forks-down
        rest = FORK_REST_DEG if SETTINGS["front"] == "forks" else PLOUGH_REST_DEG
        (ox, oy, oz), _ = front_mount.pin_axis()
        fold = bd.Pos(ox, oy, oz) * bd.Rot(rest + UP_STOP_DEG, 0, 0) * bd.Pos(-ox, -oy, -oz)
        front = {k: fold * v for k, v in front.items()}
    out.update(front)
    return out


def assembly(start_config=False):
    return bd.Compound(children=[s for s in parts(start_config).values()], label="undertow")
