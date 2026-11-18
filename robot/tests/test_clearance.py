"""Clearance at rest (robot/checks/clearance.py): tyre squash under weight and wedge deflection."""

import numpy as np
from types import SimpleNamespace

from robot.checks import clearance


def _body(vertices, kind="chassis", bid="body1", part_idx=0, material="pla"):
    v = np.asarray(vertices, float)
    lo, hi = v.min(axis=0), v.max(axis=0)
    return SimpleNamespace(id=bid, kind=kind, fastener=False, is_wire=False, part_idx=part_idx,
                           mesh=SimpleNamespace(vertices=v), aabb=np.array([lo, hi]),
                           center=(lo + hi) / 2)


def _ctx(bodies, parts, metrics=None, raw=None, min_clear=1.0):
    prof = SimpleNamespace(min_ground_clearance_mm=min_clear)
    r = SimpleNamespace(parts=parts, profile=prof,
                        spec=SimpleNamespace(ground_z=0.0, raw=raw or {}))
    return SimpleNamespace(r=r, world=SimpleNamespace(bodies=bodies),
                           metrics=dict(metrics or {}), not_checked=[])


def _part(kind="chassis", material="pla", **extra):
    return SimpleNamespace(kind=kind, material=material, _extra=dict(extra))


def _resolved(part):
    return SimpleNamespace(part=part, cat=None)


def test_no_wheels_is_not_checked():
    ctx = _ctx([_body([[0, 0, 5], [1, 0, 6]])], [_resolved(_part())])
    assert clearance.run(ctx) == []
    assert any("no wheel parts" in x for x in ctx.not_checked)


def test_no_mass_is_not_checked():
    wheel = _body([[0, 0, 0], [1, 0, 10]], kind="wheel", bid="wheel1")
    ctx = _ctx([wheel], [_resolved(_part(kind="wheel", material="tpu"))])
    assert clearance.run(ctx) == []
    assert any("no total mass" in x for x in ctx.not_checked)


def test_squashed_body_scrapes():
    # elastomer wheel 20 mm tall -> squash 8% of radius 10 = 0.8 mm; belly 1.5 mm up -> 0.7 mm left
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    belly = _body([[0, 0, 1.5], [1, 0, 6]], kind="chassis", bid="chassis1")
    ctx = _ctx([wheel, belly], [_resolved(_part(kind="wheel", material="tpu")),
                                _resolved(_part(kind="chassis", material="pla"))],
               metrics={"mass_total_g": 150.0})
    out = clearance.run(ctx)
    f = next(x for x in out if x.id == "clearance.squash")
    assert not f.passed and f.severity == "warning" and f.fix_hint
    assert ctx.metrics["clearance.tire_squash_mm"] == 0.8
    # no wedge: that half is not checked
    assert any("no wedge parts" in x for x in ctx.not_checked)


def test_rigid_wheel_keeps_clearance():
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    belly = _body([[0, 0, 1.5], [1, 0, 6]], kind="chassis", bid="chassis1")
    ctx = _ctx([wheel, belly], [_resolved(_part(kind="wheel", material="pla")),
                                _resolved(_part(kind="chassis", material="pla"))],
               metrics={"mass_total_g": 150.0})
    out = clearance.run(ctx)
    f = next(x for x in out if x.id == "clearance.squash")
    assert f.passed
    assert ctx.metrics["clearance.tire_squash_mm"] == 0.2


def test_spec_override_forces_squash():
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    belly = _body([[0, 0, 1.5], [1, 0, 6]], kind="chassis", bid="chassis1")
    ctx = _ctx([wheel, belly], [_resolved(_part(kind="wheel", material="tpu")),
                                _resolved(_part(kind="chassis", material="pla"))],
               metrics={"mass_total_g": 150.0}, raw={"rest": {"tire_squash_mm": 1.2}})
    out = clearance.run(ctx)
    f = next(x for x in out if x.id == "clearance.squash")
    assert not f.passed and ctx.metrics["clearance.tire_squash_mm"] == 1.2


def test_no_wedge_load_is_not_checked():
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    wedge = _body([[0, 0, 0.5], [1, 30, 6]], kind="wedge", bid="wedge1")
    ctx = _ctx([wheel, wedge], [_resolved(_part(kind="wheel", material="pla")),
                                _resolved(_part(kind="wedge", material="pla"))],
               metrics={"mass_total_g": 150.0})
    out = clearance.run(ctx)
    assert [x.id for x in out if x.id.startswith("clearance.")] == []
    assert any("no wedge load" in x for x in ctx.not_checked)


def test_loaded_thin_wedge_digs_in():
    # 30% of 150 g on a 60 mm long, 10 mm wide, 0.8 mm thick PLA wedge bends the tip ~21 mm down
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    wedge = _body([[0, 0, 0.5], [10, 0, 0.5], [10, 60, 0.5], [10, 60, 1.3], [0, 60, 0.5], [0, 60, 1.3]], kind="wedge", bid="wedge1")
    ctx = _ctx([wheel, wedge], [_resolved(_part(kind="wheel", material="pla")),
                                _resolved(_part(kind="wedge", material="pla"))],
               metrics={"mass_total_g": 150.0, "wedge_load_frac": 0.3})
    out = clearance.run(ctx)
    f = next(x for x in out if x.id == "clearance.wedge_deflection")
    assert not f.passed and f.severity == "warning" and f.fix_hint
    assert ctx.metrics["clearance.wedge_deflection_mm.wedge1"] > 20.0


def test_stiff_wedge_tip_stays_up():
    wheel = _body([[0, 0, 0], [1, 0, 20]], kind="wheel", bid="wheel1")
    # thick root (5 mm) at the back of the slope: I is large, deflection negligible
    v = np.array([[0, 0, 0.5], [40, 0, 0.5], [40, 60, 0.5], [40, 60, 5.5], [0, 60, 0.5], [0, 60, 5.5]], float)
    wedge = _body(v, kind="wedge", bid="wedge1")
    ctx = _ctx([wheel, wedge], [_resolved(_part(kind="wheel", material="pla")),
                                _resolved(_part(kind="wedge", material="pla"))],
               metrics={"mass_total_g": 150.0, "wedge_load_frac": 0.1})
    out = clearance.run(ctx)
    f = next(x for x in out if x.id == "clearance.wedge_deflection")
    assert f.passed
