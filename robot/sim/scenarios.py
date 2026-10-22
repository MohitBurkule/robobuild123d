"""Ready-made physics experiments. Each returns a plain dict of measurements so tests and reports can assert on them."""

from __future__ import annotations

import numpy as np

from .engine import Sim
from .model import RobotModel
from .scene import Placement, Scene


def _fresh(model, scene=None, yaw=0.0, xy=(0.0, 0.0), z_clear=0.0005):
    s = Sim(scene or Scene())
    n = s.add_robot(model, Placement(model.name.replace(" ", "_"), xy, yaw, z_clear))
    return s, n


def drop_test(model: RobotModel, height_m=0.3, settle_s=1.5) -> dict:
    """Drop from height onto the floor: peak contact force, settled tilt, whether it landed on its wheels."""
    s, n = _fresh(model, z_clear=height_m)
    s.compile()
    peak, t = 0.0, 0.0
    while t < settle_s:
        s.step(0.002)
        t += 0.002
        peak = max([peak] + [f for *_, f in s.contacts()])
    pos, _ = s.pose(n)
    return {"peak_contact_n": peak, "settled_tilt_deg": s.up_tilt_deg(n), "settled_z_m": float(pos[2]),
            "weight_n": model.mass * 9.81, "peak_g": peak / (model.mass * 9.81)}


def drive_test(model: RobotModel, speed_rad_s=40.0, seconds=1.5) -> dict:
    """Drive straight on the floor: distance along +y, sideways drift, final tilt."""
    s, n = _fresh(model)
    s.compile().step(0.5)
    p0, _ = s.pose(n)
    s.drive(n, speed_rad_s, speed_rad_s).step(seconds)
    p1, _ = s.pose(n)
    return {"forward_m": float(p1[1] - p0[1]), "drift_m": float(p1[0] - p0[0]), "tilt_deg": s.up_tilt_deg(n)}


def ramp_test(model: RobotModel, angle_deg=20.0, speed_rad_s=60.0, seconds=2.0) -> dict:
    """Drive up an incline from rest at its foot: height gained and whether it flipped."""
    sc = Scene(arena_half=0).ramp("ramp", 0.5, 0.4, angle_deg, 0.0, y=0.12)
    s, n = _fresh(model, sc, xy=(0.0, -0.05))
    s.compile().step(0.4)
    s.drive(n, speed_rad_s, speed_rad_s).step(seconds)
    p, _ = s.pose(n)
    return {"final_z_m": float(p[2]), "climbed": bool(p[2] > 0.02), "tilt_deg": s.up_tilt_deg(n), "y_m": float(p[1])}


def ram_test(a: RobotModel, b: RobotModel, gap_m=0.2, speed_rad_s=60.0, seconds=1.5, b_yaw_deg=180.0) -> dict:
    """Robot A drives (+y) into robot B facing it. Returns peak inter-robot contact force and each robot's displacement."""
    s = Sim(Scene())
    na = s.add_robot(a, Placement("A", (0.0, -gap_m / 2 - 0.08), 0.0))
    nb = s.add_robot(b, Placement("B", (0.0, gap_m / 2 + 0.08), b_yaw_deg))
    s.compile().step(0.4)
    pa0, pb0 = s.pose(na)[0], s.pose(nb)[0]
    s.drive(na, speed_rad_s, speed_rad_s)
    s.spin_weapon(na, 300.0)
    s.spin_weapon(nb, 300.0)
    peak = 0.0
    for _ in range(int(seconds / 0.005)):
        s.step(0.005)
        peak = max([peak] + [f for ga, gb, f in s.contacts() if ga.split("/")[0] != gb.split("/")[0] and "/" in ga and "/" in gb])
    pa, pb = s.pose(na)[0], s.pose(nb)[0]
    return {"peak_robot_contact_n": peak, "a_moved_m": float(np.linalg.norm(pa - pa0)), "b_moved_m": float(np.linalg.norm(pb - pb0)),
            "a_tilt_deg": s.up_tilt_deg(na), "b_tilt_deg": s.up_tilt_deg(nb)}


def push_prop_test(model: RobotModel, prop_mass_kg=0.03, speed_rad_s=60.0, seconds=1.5) -> dict:
    """Drive into a free box in front of the robot and measure how far it is pushed."""
    sc = Scene().box("block", (0.03, 0.03, 0.03), (0.0, 0.18, 0.03), mass=prop_mass_kg)
    s, n = _fresh(model, sc, xy=(0.0, -0.05))
    s.compile().step(0.4)
    b0 = s.body_pos("block")
    s.drive(n, speed_rad_s, speed_rad_s).step(seconds)
    return {"block_pushed_m": float(np.linalg.norm(s.body_pos("block") - b0)), "robot_y_m": float(s.pose(n)[0][1])}
