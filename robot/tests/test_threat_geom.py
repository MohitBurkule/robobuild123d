"""Combat failure modes end to end on small synthetic robots, the attack-model helpers, and the extended clusters."""

import numpy as np

from robot import spec, world as world_mod
from robot.checks import Ctx, Options, verify
from robot.checks import threat
from robot.checks.threat import attack as A
from robot.checks.threat import rules_ext as X
from robot.finding import Route

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
WHEEL = {"type": "cylinder", "radius": 15, "height": 8}


def bot(disc_z=16.0, switch_side=False):
    parts = [
        {"id": "chassis", "kind": "structure", "material": "nylon", "process": "fdm", "shape": BOX(80, 80, 20), "at": [0, 0, 0]},
        {"id": "wl", "kind": "wheel", "material": "silicone", "shape": WHEEL, "at": [36, -10, 0], "rot": [0, 90, 0]},
        {"id": "wr", "kind": "wheel", "material": "silicone", "shape": WHEEL, "at": [-36, -10, 0], "rot": [0, 90, 0]},
        {"id": "disc", "kind": "weapon", "material": "steel", "process": "waterjet", "shape": {"type": "cylinder", "radius": 30, "height": 4},
         "at": [0, 60, disc_z - 15], "rot": [0, 90, 0], "weapon": {"kind": "disc", "spin_axis": [0, 0, 1]}},
        {"id": "sw", "kind": "switch", "shape": BOX(6, 6, 6), "at": [42 if switch_side else 0, 0, 0]},
    ]
    return {"name": "t", "robot_type": "vertical_spinner", "ground_z": -15.0, "parts": parts}


def ctx_of(d, routes=()):
    r = world_mod.resolve(spec.Spec(d), fast=True)
    c = Ctx(r, world_mod.World.start(r), Options(fast=True, deep=False))
    c.routes = list(routes)
    return c


def test_visible_sees_only_the_near_face():
    P = np.array([[0.5, 10, 0.5], [0.5, -10, 0.5], [5.5, 10, 3.5]], float)
    m = A.visible(P, A.travel_dir(90))  # attacker in front travels toward -Y
    assert m.tolist() == [True, False, True]


def test_bite_depth_and_cylinder_gap():
    assert abs(A.bite_depth() - 6.0) < 1e-9
    g = A.cyl_gap(np.array([[0, 0, 35.0], [0, 0, 10.0]]), np.zeros(3), np.array([1.0, 0, 0]), 30.0, -2, 2)
    assert abs(g[0] - 5.0) < 1e-6 and g[1] < 0


def test_weapon_floor_strike_is_a_blocker():
    rep = verify(spec.Spec(bot(disc_z=16.0)), Options(only=["threat"], deep=False, fast=True))
    f = rep.get("threat.CF-OW01")
    assert f is not None and not f.passed and f.severity == "blocker", f and f.message
    rep = verify(spec.Spec(bot(disc_z=40.0)), Options(only=["threat"], deep=False, fast=True))
    assert rep.get("threat.CF-OW01").passed


def test_wire_in_weapon_sweep_is_a_blocker():
    near = Route("w1", 24, "power", 1.5, 40.0, [[0, 30, 0], [0, 60, 30]])
    far = Route("w1", 24, "power", 1.5, 40.0, [[10, -20, 0], [-10, -20, 0]])
    out = {f.id: f for f in threat.run(ctx_of(bot(disc_z=40.0), [near]))}
    assert not out["threat.CF-GD08"].passed and out["threat.CF-GD08"].severity == "blocker"
    out = {f.id: f for f in threat.run(ctx_of(bot(disc_z=40.0), [far]))}
    assert out["threat.CF-GD08"].passed


def test_switch_cluster_on_geometry():
    out = {f.id: f for f in threat.run(ctx_of(bot(disc_z=40.0, switch_side=True)))}
    assert not out["threat.CFX-SWITCH"].passed
    out = {f.id: f for f in threat.run(ctx_of(bot(disc_z=40.0)))}
    assert out["threat.CFX-SWITCH"].passed


def test_ext_rules_good_and_bad():
    assert X.sw({"x.switch": [{"id": "s", "side_hit": False, "top_gap": 5.0, "top_visible": False}]})[0] is True
    assert X.sw({"x.switch": [{"id": "s", "side_hit": False, "top_gap": 0.5, "top_visible": True}]})[0] is False
    assert X.antenna({"x.antenna": []})[0] is True and X.antenna({"x.antenna": ["antenna"]})[0] is False
    assert X.friction({"x.friction": []})[0] is True and X.friction({"x.friction": ["pin/wheel"]})[0] is False
    assert X.tape({"x.tape": []})[0] is True and X.tape({"x.tape": ["rx"]})[0] is False
    good = {k: True for k in X.STATE_TEXT}
    assert X.states({"x.states": good})[0] is True
    assert X.states({"x.states": {**good, "inverted": False}})[0] is False


def test_friction_and_tape_from_spec():
    d = bot(disc_z=40.0)
    d["parts"] += [{"id": "rx", "kind": "receiver", "shape": BOX(10, 10, 4), "at": [0, -20, 0]},
                   {"id": "p1", "kind": "pin", "material": "steel", "shape": BOX(2, 2, 10), "at": [20, -20, 0]}]
    d["connections"] = [{"a": "rx", "b": "chassis", "method": "tape"}, {"a": "p1", "b": "chassis", "method": "press_fit"}]
    out = {f.id: f for f in threat.run(ctx_of(d))}
    assert not out["threat.CFX-TAPE"].passed and not out["threat.CFX-FRICTION"].passed
