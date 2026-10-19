"""reference.feature_ratio (design proportions vs photos) and plausibility.density (mass vs envelope)."""

from pathlib import Path

from robot import spec as spec_mod, world as world_mod
from robot.checks import Ctx, Options, plausibility, reference_ratios

ROOT = Path(__file__).resolve().parents[2]


def _ctx(raw):
    r = world_mod.resolve(spec_mod.Spec(raw, ROOT), fast=True)
    return Ctx(r, world_mod.World.start(r), Options())


def _robot(ratios, extra=()):
    return {"name": "box", "parts": [
        {"id": "body", "kind": "chassis", "shape": {"type": "box", "size": [80, 120, 30]}, "material": "PLA"},
        {"id": "fork_l", "kind": "fork", "shape": {"type": "box", "size": [2, 20, 2]}, "at": [35, 70, 1], "material": "steel"},
        {"id": "fork_r", "kind": "fork", "shape": {"type": "box", "size": [2, 20, 2]}, "at": [-35, 70, 1], "material": "steel"},
        *extra], "reference_ratios": ratios}


def _by_name(fs):
    return {f.message.split("`")[1]: f for f in fs if f.id == "reference.feature_ratio"}


def test_good_proportions_pass():
    ctx = _ctx(_robot([
        {"name": "w_over_l", "num": "overall.W", "den": "overall.L", "value": 80 / 140, "tol": 0.02},
        {"name": "fork_span", "num": "part:fork_*.W", "den": "overall.W", "value": 72 / 80, "tol": 0.02},
        {"name": "forks", "num": "kind:fork.count", "value": 2, "tol": 0}]))
    fs = _by_name(reference_ratios.run(ctx))
    assert all(f.passed for f in fs.values()), [f.message for f in fs.values()]
    assert abs(ctx.metrics["reference_ratio.fork_span"] - 0.9) < 0.01


def test_bad_proportions_fail_with_severity():
    ctx = _ctx(_robot([
        {"name": "h_over_l", "num": "overall.H", "den": "overall.L", "value": 0.5, "tol": 0.05, "severity": "blocker"},
        {"name": "fork_span", "num": "part:fork_*.W", "den": "overall.W", "value": 0.6, "tol_frac": 0.1}]))
    fs = _by_name(reference_ratios.run(ctx))
    assert not fs["h_over_l"].passed and fs["h_over_l"].severity == "blocker"
    assert not fs["fork_span"].passed and fs["fork_span"].severity == "warning"


def test_unmeasurable_term_is_not_checked():
    ctx = _ctx(_robot([{"name": "ghost", "num": "part:nope.L", "value": 1, "tol": 1},
                       {"name": "late", "num": "metric:archetype.disc_dia_mm", "value": 40, "tol": 1},
                       {"name": "typo", "num": "overal.L", "value": 1, "tol": 1}]))
    fs = [f for f in reference_ratios.run(ctx) if f.id == "reference.feature_ratio"]
    assert len(fs) == 3 and not any(f.passed for f in fs)
    assert sum("Reference proportion" in n for n in ctx.not_checked) == 3


def test_metric_term_and_mass():
    ctx = _ctx(_robot([{"name": "rotor_frac", "num": "metric:weapon_mass_fraction", "value": 0.21, "tol": 0.03}]))
    ctx.metrics["weapon_mass_fraction"] = 0.12
    assert not _by_name(reference_ratios.run(ctx))["rotor_frac"].passed
    ctx.metrics["weapon_mass_fraction"] = 0.22
    assert _by_name(reference_ratios.run(ctx))["rotor_frac"].passed


def test_no_ratios_no_findings():
    assert reference_ratios.run(_ctx(_robot([]))) == []


def _bat(mass):
    return {"id": "bat", "kind": "battery", "shape": {"type": "box", "size": [36, 17, 11]}, "mass_g": mass}


def test_battery_density_bad_and_good():
    bad = _ctx(_robot([], [_bat(21.5)]))  # 3.2 g/cm3: impossible LiPo (the Revron catalog error)
    f = [f for f in plausibility.run(bad) if f.id == "plausibility.density"][0]
    assert not f.passed and "3.1" in f.message
    good = _ctx(_robot([], [_bat(12.5)]))
    assert [f for f in plausibility.run(good) if f.id == "plausibility.density"][0].passed
