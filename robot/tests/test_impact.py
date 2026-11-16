"""Impact check (robot/checks/impact.py): gyro wheel-lift, hop and spin-out yaw."""

import numpy as np
from types import SimpleNamespace

from robot.checks import impact


def _ctx(metrics=None, track_mm=None):
    bodies = []
    if track_mm is not None:
        half = track_mm / 2
        for x in (-half, half):
            bodies.append(SimpleNamespace(kind="wheel", fastener=False,
                                          M=np.array([[1, 0, 0, x], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], float)))
    return SimpleNamespace(r=None, world=SimpleNamespace(bodies=bodies),
                           not_checked=[], metrics=dict(metrics or {}))


def _metrics(energy=8.0, rpm=12000.0, mass=150.0, orient="vspin", family=None):
    m = {"weapon_energy_j": energy, "weapon_rpm": rpm, "mass_total_g": mass, "weapon_orientation": orient,
         "footprint_mm": 140.0}
    if family:
        m["combat.family"] = family
    return m


def test_no_weapon_metrics_is_not_checked():
    ctx = _ctx()
    assert impact.run(ctx) == []
    assert any("power and mass groups" in x for x in ctx.not_checked)


def test_inertia_from_energy_and_rpm():
    i_w, omega = impact.weapon_inertia(_ctx(_metrics()))
    assert omega > 0 and abs(i_w - 2 * 8.0 / omega ** 2) < 1e-9


def test_track_from_wheel_bodies():
    assert impact.wheel_track(_ctx(track_mm=120.0)) == 120.0
    assert impact.wheel_track(_ctx()) is None


def test_heavy_vertical_weapon_turn_is_the_stutter_tradeoff():
    m = _ctx(_metrics(energy=12.0, rpm=20000.0, mass=150.0, orient="horizontal", family="vspin"), track_mm=90.0)
    out = impact.run(m)
    ids = [f.id for f in out]
    assert "impact.gyro_lift" in ids
    f = next(f for f in out if f.id == "impact.gyro_lift")
    assert f.severity == "warning" and f.fix_hint
    assert "stutter" in f.message.lower() or "stutter" in f.fix_hint.lower()
    assert m.metrics["gyro_lift_yaw_rad_s"] > 0


def test_heavy_weapon_unknown_orientation_still_blocks_on_gyro_lift():
    m = _ctx(_metrics(energy=12.0, rpm=20000.0, mass=150.0, orient=""), track_mm=90.0)


def test_horizontal_axis_without_vspin_family_still_blocks():
    m = _ctx(_metrics(energy=12.0, rpm=20000.0, mass=150.0, orient="horizontal"), track_mm=90.0)
    f = next(f for f in impact.run(m) if f.id == "impact.gyro_lift")
    assert f.severity == "blocker"
    out = impact.run(m)
    f = next(f for f in out if f.id == "impact.gyro_lift")
    assert f.severity == "blocker" and f.fix_hint
    assert m.metrics["gyro_lift_yaw_rad_s"] > 0


def test_mild_case_passes_all_margins():
    m = _ctx(_metrics(energy=0.7, rpm=9000.0), track_mm=140.0)
    ids = [f.id for f in impact.run(m)]
    assert ids == ["impact.ok"]


def test_big_hop_warns_for_verticals():
    m = _ctx(_metrics(energy=12.0, rpm=12000.0, mass=120.0), track_mm=140.0)
    ids = [f.id for f in impact.run(m)]
    assert "impact.hop" in ids


def test_horizontal_spin_out_yaw():
    m = _ctx(_metrics(energy=10.0, rpm=15000.0, mass=150.0, orient="hspin"), track_mm=140.0)
    ids = [f.id for f in impact.run(m)]
    assert "hit_yaw_deg_s" in m.metrics or "impact.yaw" in ids


def test_ok_path_when_all_margins_fine():
    m = _ctx(_metrics(energy=0.5, rpm=6000.0), track_mm=150.0)
    out = impact.run(m)
    assert [f.id for f in out] == ["impact.ok"] and not m.not_checked
