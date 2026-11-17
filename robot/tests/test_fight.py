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
            assert abs(sim.weapon_omega("A")) > 200
    assert tilt[True] > tilt[False] + 1.0, tilt


def test_hazards_wire_effects_and_delay():
    from types import SimpleNamespace

    from robot.fight import hazards

    h = hazards.Hazards.__new__(hazards.Hazards)
    h.kind = {"A": {"battery": "battery", "power_switch": "switch", "motor_l": "motor", "wmotor": "weapon_motor",
                    "servo": "servo", "esc": "esc"}}
    h.com = {"A": {"motor_l": np.array([-0.02, 0, 0])}}
    eff = lambda a, b: h._wire_effect("A", {"ends": (a, b)})  # noqa: E731
    assert eff("battery", "power_switch") == "all"
    assert eff("esc", "motor_l") == "side:l"
    assert eff("esc", "wmotor") == "weapon"
    assert eff("esc", "servo") == "lifter"
    assert hazards._seg_dist(np.array([0, 0.001, 0]), np.array([[-1, 0, 0], [1, 0, 0.0]])) == pytest.approx(0.001)
    # driver delay: a command comes back reaction_s later
    h.p = {"A": dict(hazards.DEFAULTS, steer_noise=0.0)}
    h.queue = {"A": hazards.deque()}
    h.rng = np.random.default_rng(0)
    h.sim = SimpleNamespace(profiles={"A": SimpleNamespace(drive_max=100.0)})
    assert h.delay("A", 0.0, {"drive": (1, 1)}) is None
    assert h.delay("A", 0.1, {"drive": (2, 2)}) is None
    assert h.delay("A", 0.16, {"drive": (3, 3)})["drive"] == (1, 1)


def test_debris_collides_with_own_robot_after_breaking():
    from robot.fight import hazards
    from robot.fight.arena import FightSim
    from robot.sim.scene import Placement

    sp = _spec(robot_type="wedge", sim={"forward": [0, 1], "breakable": {"lid": 1e-3}})
    sim = FightSim()
    sim.add_fighter(_model(), profile.build(sp), Placement("A", (0, 0), 90))
    sim.compile()
    hz = hazards.Hazards(sim, {"A": sp})
    lid = [g for g, o in hz.owner.items() if o[2] == "lid"]
    assert all(sim.m.geom_contype[g] != hazards.DEBRIS_BIT for g in lid)
    sim.d.qvel[:] = 0
    for k in range(6000):
        if k == 10:  # knock the broken lid off its seat
            b = sim.m.body("A/lid").id
            sim.d.xfrc_applied[b, :3] = [0, 0, 0.3]
        if k == 200:
            sim.d.xfrc_applied[:] = 0
        sim.step_damage()
        if k % 5 == 0:
            hz.tick(k * sim.timestep, 5 * sim.timestep)
    assert ("A", "lid") in hz.debris_live
    assert all(sim.m.geom_contype[g] == hazards.DEBRIS_BIT for g in lid)


def _ramp_climb(force, theta_deg, mu):
    """A 100 g block pushed horizontally into a fixed ramp (angle theta, friction mu, same contact settings as fights):
    returns how high it is after 0.5 s (m). Starts touching the ramp, at rest."""
    from robot.fight import materials

    th = math.radians(theta_deg)
    dr = materials.damp_ratio(0.45)
    L = 0.4
    h = L * math.tan(th)
    verts = " ".join(f"{x} {y} {z}" for y in (-.03, .03) for x, z in ((0, 0), (L, 0), (L, h)))
    xml = f"""<mujoco><asset><mesh name="ramp" vertex="{verts}"/></asset><option timestep="1e-4" integrator="implicitfast" cone="elliptic"><flag multiccd="enable"/></option>
      <worldbody>
        <geom type="plane" size="1 1 .1" friction="0.0001 0.005 0.0001" solref="3e-4 {dr}"/>
        <geom type="mesh" mesh="ramp" friction="{mu} 0.005 0.0001" solref="3e-4 {dr}"/>
        <body name="b" pos="-.0102 0 .0101"><joint type="slide" axis="1 0 0"/><joint type="slide" axis="0 0 1"/>
          <geom type="box" size=".01 .01 .01" mass=".1" friction="{mu} 0.005 0.0001" solref="3e-4 {dr}"/>
        </body></worldbody></mujoco>"""
    m = mujoco.MjModel.from_xml_string(xml)
    d = mujoco.MjData(m)
    b = m.body("b").id
    z0 = float(d.xpos[b, 2])
    for _ in range(5000):
        d.xfrc_applied[b, 0] = force
        mujoco.mj_step(m, d)
    return float(d.xpos[b, 2]) - z0


def test_ramp_lift_matches_incline_physics():
    """Wedge physics check: a push climbs a ramp only above F = m g (sin + mu cos) / (cos - mu sin)."""
    for theta, mu in ((20.0, 0.35), (30.0, 0.35), (15.0, 0.8)):
        th = math.radians(theta)
        f_crit = 0.1 * 9.81 * (math.sin(th) + mu * math.cos(th)) / (math.cos(th) - mu * math.sin(th))
        base = _ramp_climb(0.5 * f_crit, theta, mu)  # where it settles against the ramp toe
        assert _ramp_climb(0.95 * f_crit, theta, mu) - base < 0.002, (theta, mu)  # below threshold: stays
        assert _ramp_climb(1.1 * f_crit, theta, mu) - base > 0.01, (theta, mu)  # just above: climbs
