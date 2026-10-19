"""SectorSweep band fill (VERIFIER_ISSUES #3) and joint pivot/axis frame (VERIFIER_ISSUES #4) on claude/template-engine-ctcfhz."""

import numpy as np

from robot import spec, world
from robot.checks import Options, verify
from robot.checks import interference, kinematics
from test_kinematics import PLA, run, wheels

PIV = [0, -40, 20]


def scoop(block_r):
    """A lifter whose hub sits on the pivot (r 2.5) and whose plate is far out (r 20-37) in the same axial slice, with a
    static block in that slice (its face in the same plane as the hub and plate faces, x = 3) at radius `block_r`
    on the plate's side."""
    d = wheels()
    hub = {"type": "place", "at": [0, 0, 0], "rot": [0, 90, 0], "shape": {"type": "cylinder", "radius": 2.5, "height": 6}}
    plate = {"type": "place", "at": [0, -28.5, 0], "shape": {"type": "box", "size": [6, 17, 2]}}
    cheek = {"type": "place", "at": [7, -18.5, 0], "shape": {"type": "box", "size": [2, 37, 2]}}
    tab = {"type": "place", "at": [4.5, 0, 0], "shape": {"type": "box", "size": [3, 4, 2]}}
    tab2 = {"type": "place", "at": [4.5, -28.5, 0], "shape": {"type": "box", "size": [3, 4, 2]}}
    d["parts"].append({"id": "arm", "kind": "structure", **PLA, "at": PIV,
                       "shape": {"type": "union", "items": [hub, plate, cheek, tab, tab2]},
                       "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": PIV, "min": -35, "max": 0}})
    d["parts"].append({"id": "block", "kind": "structure", **PLA, "at": [1, PIV[1] - block_r, PIV[2]],
                       "shape": {"type": "box", "size": [4, 4, 4]}})
    return d


def fails(rep, cid):
    return [f.message for f in rep.findings if f.id == cid and not f.passed]


def test_block_between_hub_and_plate_is_clear():
    rep, _ = run(scoop(11))
    assert not fails(rep, "kin.sweep_static"), fails(rep, "kin.sweep_static")
    assert not [m for m in fails(rep, "kin.rub_gap") if "`block`" in m]


def test_block_in_plate_path_still_fails():
    rep, _ = run(scoop(28))
    assert [m for m in fails(rep, "kin.sweep_static") if "`block`" in m]


# ---- #4: joint pivot/axis are in the parent's declared world pose (its at/rot, through its own parents)
def servo_arm(pivot):
    return {"name": "t", "robot_type": "lifter", "parts": [
        {"id": "base", "kind": "structure", **PLA, "at": [0, 0, 2], "shape": {"type": "box", "size": [60, 60, 4]}},
        {"id": "servo", "kind": "servo", "catalog": "servo_cs07", "at": [10, 5, 12], "rot": [90, 0, 90]},
        {"id": "arm", "kind": "structure", **PLA, "parent": "servo", "at": [0, 0, 3], "rot": [-90, -90, 0],
         "shape": {"type": "box", "size": [4, 20, 3]},
         "joint": {"kind": "revolute", "axis": [0, 0, 1], "pivot": pivot, "min": 0, "max": 35}}]}


def motion_axis(r):
    """World axis and a point on it, from the arm's real pose at two joint values."""
    M0 = world.World.build(r, {"arm": 0}).body("arm").M
    M1 = world.World.build(r, {"arm": 30}).body("arm").M
    D = M1 @ np.linalg.inv(M0)
    w, v = np.linalg.eig(D[:3, :3])
    ax = np.real(v[:, np.argmin(abs(w - 1))])
    p = np.linalg.lstsq(np.eye(3) - D[:3, :3], D[:3, 3], rcond=None)[0]
    return ax / np.linalg.norm(ax), p


def on_line(p, o, a):
    q = np.asarray(p) - o
    return np.linalg.norm(q - (q @ a) * a)


def test_joint_frame_is_parent_declared_pose():
    r = world.resolve(spec.Spec(servo_arm([0, 0, 3])), fast=True)
    a, o = motion_axis(r)
    # servo local z -> world x; the arm swings about world x through the servo centre line (y 5, z 12)
    assert abs(abs(a[0]) - 1) < 1e-6 and on_line([10, 5, 12], o, a) < 1e-6
    w = world.World.start(r)
    ctx = type("C", (), {"r": r, "world": w, "not_checked": [], "metrics": {}})()
    kp, ka = kinematics.Kin(ctx).joint_world("arm")
    assert abs(abs(ka @ a) - 1) < 1e-6 and on_line(kp, o, a) < 1e-6
    ip, ia = interference.wheel_axis(r, w, w.index("arm"))
    assert abs(abs(ia @ a) - 1) < 1e-6 and on_line(ip, o, a) < 1e-6


def test_joint_pivot_written_in_world_frame_under_servo_is_flagged():
    # world coordinates of the servo face written as if they were in the servo frame: lands ~20 mm off the parts
    rep = verify(spec.Spec(servo_arm([13, 5, 12])), Options(only=["connections"], deep=False, fast=True))
    assert any(f.id == "connection.joint_pivot" and not f.passed for f in rep.findings)
    good = verify(spec.Spec(servo_arm([0, 0, 3])), Options(only=["connections"], deep=False, fast=True))
    assert not any(f.id == "connection.joint_pivot" and not f.passed for f in good.findings)
