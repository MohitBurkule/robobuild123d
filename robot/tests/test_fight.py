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


def test_motor_curve_battery_sag_heat():
    from robot.fight import physics

    m = physics.weapon_motor({"weapon": {"motor": {"kv": 3800, "r_ohm": 0.12, "i_max_a": 30}}}, "w")
    b = physics.battery({})
    t_stall = m.torque(1.0, b.v, 0.0)
    assert m.i == 30.0 and math.isclose(t_stall, m.ke * 30)  # ESC current limit at stall
    w0 = b.v / m.ke
    assert abs(m.torque(1.0, b.v, w0)) < 1e-9  # no torque at no-load speed
    assert m.torque(1.0, b.v, 0.9 * w0) < t_stall
    v0 = b.v
    b.update(30.0, 0.1)
    assert b.v < v0 - 2.0 and b.soc < 1.0  # sag under spin-up current, charge used
    m.torque(1.0, 8.4, 0.0)
    for _ in range(2000):
        m.heat(0.01)
    assert m.temp > 60  # stalled 20 s: hot
    hot = physics.Motor("h", 0.0025, 0.12, 30, t_cut=50)
    hot.torque(1.0, 8.4, 0.0)
    for _ in range(1000):
        hot.heat(0.01)
    assert hot.dead and hot.torque(1.0, 8.4, 0.0) == 0.0


def _spinner_model():
    from robot.sim.model import Group

    m = _model()
    disc = _box_part("disc", "weapon", (-.003, .02, .005), (.003, .07, .055), .03)
    m.groups.append(Group("weapon", "weapon", [disc], pivot=np.array([0, .045, .03]), axis=np.array([1.0, 0, 0])))
    return m


def test_gyro_tilts_a_turning_spinner():
    """A vertical spinner turning on the spot tips further with its disc spinning (gyroscopic torque)."""
    from robot.fight.arena import FightSim
    from robot.sim.scene import Placement

    sp = _spec(sim={"forward": [0, 1], "weapon": {"rpm": 12000, "imbalance_mm": 0.0}, "breakable": {"lid": 1e6}})
    tilt = {}
    for spin in (False, True):
        prof = profile.build(sp)
        sim = FightSim()
        sim.add_fighter(_spinner_model(), prof, Placement("A", (0, 0), 90))
        sim.compile()
        mx = 0.0
        for k in range(12000):
            if k % 40 == 0:
                sim.spin_weapon("A", prof.weapon_omega if spin else 0)
                sim.drive("A", *((0, 0) if k < 8000 else (-230, 230)))
            if k % 5 == 0:
                sim.step_plant(5e-4)
            sim.step_damage()
            if k >= 8000:
                mx = max(mx, sim.tilt("A"))
        tilt[spin] = mx
        if spin:
            assert abs(sim.weapon_omega("A")) > 300
    assert tilt[True] > tilt[False] + 1.0, tilt
