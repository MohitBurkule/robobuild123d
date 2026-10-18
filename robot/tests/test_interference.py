"""Interference: overlap vs touching, joint sweeps, spin sweep, captive/retention."""

from robot import spec, world
from robot.checks import Ctx, Options, interference


def _ctx(parts, **extra):
    d = {"name": "t", "parts": parts, **extra}
    r = world.resolve(spec.Spec(d), fast=True)
    return Ctx(r, world.World.start(r), Options(fast=True))


def box(id, at, size=(10, 10, 10), kind="structure", **kw):
    return {"id": id, "kind": kind, "shape": {"type": "box", "size": list(size)}, "at": list(at), "material": "pla", **kw}


def ids(fs, fid):
    return [f for f in fs if f.id == fid]


def test_touching_is_fine_overlap_fails():
    c = _ctx([box("a", (0, 0, 0)), box("b", (10, 0, 0))])
    f = ids(interference.run(c), "interference.overlap")
    assert len(f) == 1 and f[0].passed
    c = _ctx([box("a", (0, 0, 0)), box("b", (8, 0, 0))])
    f = ids(interference.run(c), "interference.overlap")
    assert not f[0].passed and abs(float(f[0].actual.split()[0]) - 1.0) < 0.1


def test_allowed_depth_rules():
    c = _ctx([box("a", (0, 0, 0)), box("b", (8, 0, 0), fused_with="a")])
    assert interference.allowed_depth(c.r, c.world.bodies[0], c.world.bodies[1]) == float("inf")
    c = _ctx([box("a", (0, 0, 0)), box("b", (9.5, 0, 0))], allow_overlap=[{"a": "b", "b": "a", "max_depth_mm": 0.6}])
    assert interference.allowed_depth(c.r, c.world.bodies[0], c.world.bodies[1]) == 0.6
    assert ids(interference.run(c), "interference.overlap")[0].passed


def test_joint_sweep_hits():
    arm = box("arm", (0, 0, 0), (40, 4, 4), kind="weapon",
              joint={"kind": "revolute", "axis": [0, 0, 1], "pivot": [-20, 0, 0], "min": 0, "max": 90})
    c = _ctx([box("base", (0, 30, 0)), arm])
    f = ids(interference.run(c), "interference.sweep")
    assert f and not f[0].passed and f[0].parts == ["arm", "base"]


def test_spin_sweep_hit_and_clear():
    disc = box("disc", (0, 0, 0), (40, 4, 3), kind="weapon", weapon={"kind": "bar"})
    c = _ctx([disc, box("post", (0, 12, 0), (4, 4, 10))])  # inside the r=20 sweep, clear of the bar at rest
    f = ids(interference.run(c), "interference.spin")
    assert f and not f[0].passed
    c = _ctx([disc, box("post", (40, 0, 0), (8, 8, 10))])
    f = ids(interference.run(c), "interference.spin")
    assert f and f[0].passed


def test_loose_battery_and_captive_map():
    walls = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-8, 0, 0), (2, 30, 10)), box("w2", (8, 0, 0), (2, 30, 10)),
             box("w3", (0, -8, 0), (30, 2, 10)), box("w4", (0, 8, 0), (30, 2, 10)), box("lid", (0, 0, 6), (30, 30, 2))]
    batt = box("bat", (0, 0, 0), (14, 14, 10), kind="battery", retained="pocket")
    c = _ctx(walls + [batt])
    fs = interference.run(c)
    assert not ids(fs, "retention.loose") and ids(fs, "retention.captive")[0].passed
    assert "bat" in c.captive
    c = _ctx(walls[:-1] + [batt])  # no lid: free to +z
    f = ids(interference.run(c), "retention.loose")
    assert f and f[0].severity == "blocker" and "+z" in f[0].message


def test_battery_retention_must_be_declared():
    walls = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-8, 0, 0), (2, 30, 10)), box("w2", (8, 0, 0), (2, 30, 10)),
             box("w3", (0, -8, 0), (30, 2, 10)), box("w4", (0, 8, 0), (30, 2, 10)), box("lid", (0, 0, 6), (30, 30, 2))]
    fs = interference.run(_ctx(walls + [box("bat", (0, 0, 0), (14, 14, 10), kind="battery")]))
    f = ids(fs, "retention.battery_undeclared")
    assert f and f[0].severity == "blocker"
