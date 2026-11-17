"""Fight sim: profile/requirements from the spec, breakable welds snap, brains steer. Synthetic robots (no CAD build)."""

import math

import numpy as np
import pytest

from robot import spec as spec_mod
from robot.fight import profile

mujoco = pytest.importorskip("mujoco")


def _spec(**kw):
    d = {"name": "T", "robot_type": kw.pop("robot_type", "vertical_spinner"),
         "parts": [{"id": "tub", "kind": "structure"}, {"id": "lid", "kind": "armor"}],
         "fasteners": [{"id": "f0", "designation": "M3x6", "through": ["lid", "tub"]}]}
    d.update(kw)
    return spec_mod.Spec(d)


def test_requirements_missing_block():
    assert profile.requirements(_spec())[0][0] == "sim"


def test_requirements_spinner_and_lifter():
    assert ("sim.weapon.rpm", "spinner without a target weapon speed") in profile.requirements(_spec(sim={"forward": [0, 1]}))
    req = profile.requirements(_spec(robot_type="flipper", sim={"forward": [0, 1], "lifter": {"group": "nope", "up_rad": 1}}))
    assert any(k == "sim.lifter.group" for k, _ in req)
    assert profile.requirements(_spec(sim={"forward": [0, 1], "weapon": {"rpm": 9000}})) == []


def test_break_force_from_fasteners_and_override():
    p = profile.build(_spec(sim={"forward": [1, 0], "weapon": {"rpm": 6000}}))
    assert p.breakable == {"lid": profile.FASTENER_N["M3"]}
    assert math.isclose(p.weapon_omega, 6000 * 2 * math.pi / 60)
    assert math.isclose(p.heading0, 0.0)
    p = profile.build(_spec(sim={"breakable": {"lid": 50}}))
    assert p.breakable["lid"] == 50.0


def _box_part(pid, kind, lo, hi, mass):
    from robot.sim.model import SimPart

    lo, hi = np.asarray(lo, float), np.asarray(hi, float)
    v = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    e = hi - lo
    I = mass / 12 * np.diag([e[1] ** 2 + e[2] ** 2, e[0] ** 2 + e[2] ** 2, e[0] ** 2 + e[1] ** 2])
    return SimPart(pid, kind, v, mass, (lo + hi) / 2, I)


def _model():
    from robot.sim.model import CHASSIS, Group, RobotModel

    ch = Group(CHASSIS, "chassis", [_box_part("tub", "structure", (-.03, -.03, .005), (.03, .03, .03), .1),
                                    _box_part("lid", "armor", (-.03, -.03, .03), (.03, .03, .032), .005)])
    wl = Group("wl", "wheel", [_box_part("wl", "wheel", (.03, -.01, 0), (.035, .01, .02), .004)], pivot=np.array([.032, 0, .01]),
               axis=np.array([1.0, 0, 0]))
    wr = Group("wr", "wheel", [_box_part("wr", "wheel", (-.035, -.01, 0), (-.03, .01, .02), .004)], pivot=np.array([-.032, 0, .01]),
               axis=np.array([1.0, 0, 0]))
    return RobotModel("T", [ch, wl, wr])


def test_weld_holds_then_breaks():
    from robot.fight.arena import FightSim
    from robot.sim.scene import Placement

    for limit, want_broken in ((1e6, False), (1e-3, True)):
        sp = _spec(robot_type="wedge", sim={"forward": [0, 1], "breakable": {"lid": limit}})
        sim = FightSim()
        sim.add_fighter(_model(), profile.build(sp), Placement("A", (0, 0), 90))
        sim.compile()
        for _ in range(3000):
            sim.step_damage()
        assert (sim.welds[0].broken_at is not None) == want_broken
        if not want_broken:  # welded lid stays on the chassis
            c = sim.d.xpos[sim.m.body("A/chassis").id]
            l = sim.d.xpos[sim.m.body("A/lid").id]
            assert np.linalg.norm(c - l) < 1e-3


def test_sector_pieces_keep_tooth():
    from robot.fight.arena import sector_pieces

    ang = np.linspace(0, 2 * np.pi, 48, endpoint=False)
    r = np.where(np.abs(ang - np.pi / 2) < 0.15, 0.04, 0.025)  # one tooth
    ring = np.c_[np.zeros_like(ang), r * np.cos(ang), r * np.sin(ang)]
    v = np.vstack([ring + [-.002, 0, 0], ring + [.002, 0, 0]])
    p = _box_part("disc", "weapon", (-.002, -.04, -.04), (.002, .04, .04), .01)
    p.verts = v
    pieces = sector_pieces(p, np.zeros(3), np.array([1.0, 0, 0]))
    assert len(pieces) >= 8
