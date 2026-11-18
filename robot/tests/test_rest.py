"""Rest / dead-pose check (robot/checks/rest.py): the weapon swept over all rest angles vs the floor."""

import numpy as np
from types import SimpleNamespace

from robot.checks import rest


def _body(vertices, part_idx=0, kind="weapon", bid="weapon1", origin=(0, 0, 0)):
    v = np.asarray(vertices, float)
    lo, hi = v.min(axis=0), v.max(axis=0)
    mesh = SimpleNamespace(vertices=v)
    m = np.eye(4)
    m[:3, 3] = origin
    return SimpleNamespace(id=bid, kind=kind, fastener=False, is_wire=False, part_idx=part_idx,
                           mesh=mesh, aabb=np.array([lo, hi]), M=m,
                           center=(lo + hi) / 2)


def _ctx(bodies, parts, ground_z=0.0, min_clear=1.0):
    prof = SimpleNamespace(min_ground_clearance_mm=min_clear)
    r = SimpleNamespace(parts=parts, profile=prof, spec=SimpleNamespace(ground_z=ground_z, raw={}))
    return SimpleNamespace(r=r, world=SimpleNamespace(bodies=bodies), metrics={}, not_checked=[])


def _part(kind="weapon", spin_axis=None, weapon=True):
    w = SimpleNamespace(spin_axis=spin_axis) if weapon else None
    return SimpleNamespace(kind=kind, weapon=w, _extra={})


def _resolved(part):
    return SimpleNamespace(part=part, cat=None)


def test_no_weapon_is_not_checked():
    ctx = _ctx([_body([[0, 0, 5], [1, 0, 5]], part_idx=0, kind="chassis")], [_resolved(_part(kind="chassis", spin_axis=None, weapon=False))])
    assert rest.run(ctx) == []
    assert any("no weapon body" in x for x in ctx.not_checked)


def test_high_bar_clears_at_every_angle():
    # vertical spinner: axis +Z at z=30, bar at z=30 -> swept lowest stays 30 mm up
    b = _body([[-20, 0, 30], [20, 0, 30]], origin=(0, 0, 30))
    ctx = _ctx([b], [_resolved(_part(spin_axis=[0, 0, 1]))])
    ids = [f.id for f in rest.run(ctx)]
    assert ids == ["rest.ok"]
    assert ctx.metrics["rest.weapon_gap_mm"] == 30.0


def test_sweep_below_floor_blocks():
    # horizontal axis at z=15, a point 20 mm off the axis sweeps down to -5 mm
    b = _body([[0, -20, 15], [0, 20, 15]], origin=(0, 0, 15))
    ctx = _ctx([b], [_resolved(_part(spin_axis=[1, 0, 0]))])
    out = rest.run(ctx)
    f = next(x for x in out if x.id == "rest.weapon_drag")
    assert f.severity == "blocker" and not f.passed and f.fix_hint
    assert ctx.metrics["rest.weapon_gap_mm"] == -5.0


def test_sweep_close_to_floor_warns():
    # horizontal axis at z=20.5, radius 20 -> swept lowest 0.5 mm, inside the 1.0 mm graze band
    b = _body([[0, -20, 20.5], [0, 20, 20.5]], origin=(0, 0, 20.5))
    ctx = _ctx([b], [_resolved(_part(spin_axis=[1, 0, 0]))], min_clear=1.0)
    out = rest.run(ctx)
    f = next(x for x in out if x.id == "rest.weapon_graze")
    assert f.severity == "warning" and not f.passed and f.fix_hint


def test_vertical_axis_never_drops_the_weapon():
    # axis +Z: tilt term sqrt(1-a_z^2) is 0, so the swept lowest equals the built lowest
    b = _body([[0, -20, 5], [0, 20, 5]], origin=(0, 0, 30))
    ctx = _ctx([b], [_resolved(_part(spin_axis=[0, 0, 1]))], min_clear=1.0)
    ids = [f.id for f in rest.run(ctx)]
    assert "rest.weapon_drag" not in ids
