"""Thermal/brownout check (robot/checks/thermal.py): pack sag at peak current."""

from types import SimpleNamespace

from robot.checks import thermal


def _ctx(metrics=None, battery_props=None, esc_props=None):
    parts = []
    if battery_props is not None:
        parts.append(SimpleNamespace(part=SimpleNamespace(id="bat", kind="battery", _extra={}),
                                     cat=SimpleNamespace(id="bat_hx100_2s", kind="battery", props=battery_props)))
    if esc_props is not None:
        parts.append(SimpleNamespace(part=SimpleNamespace(id="esc", kind="esc", _extra={}),
                                     cat=SimpleNamespace(id="esc_tiny", kind="esc", props=esc_props)))
    spec = SimpleNamespace(raw={}, parts=[rp.part for rp in parts], connections=[])
    return SimpleNamespace(r=SimpleNamespace(spec=spec, parts=parts), world=SimpleNamespace(bodies=[]),
                           not_checked=[], metrics=dict(metrics or {}))


GOOD = {"cells": 2, "capacity_mah": 450, "c_rating": 75, "nominal_v": 7.4, "internal_resistance_mohm": 25}
SMALL = {"cells": 2, "capacity_mah": 180, "c_rating": 20, "nominal_v": 7.4, "internal_resistance_mohm": 100}


def test_no_battery_is_not_checked():
    ctx = _ctx()
    assert thermal.run(ctx) == []
    assert any("no catalogue battery" in x for x in ctx.not_checked)


def test_missing_props_is_not_checked():
    ctx = _ctx(battery_props={"cells": 2})
    assert thermal.run(ctx) == []
    assert any("missing" in x for x in ctx.not_checked)


def test_healthy_pack_passes():
    ctx = _ctx(metrics={"peak_current_a": 15.0}, battery_props=GOOD)
    out = thermal.run(ctx)
    assert [f.id for f in out] == ["thermal.ok"]
    assert ctx.metrics["pack_v_loaded"] > 7.0


def test_small_pack_browns_out():
    ctx = _ctx(metrics={"peak_current_a": 20.0}, battery_props=SMALL)
    out = thermal.run(ctx)
    assert [f.id for f in out] == ["thermal.brownout"]
    f = out[0]
    assert f.severity == "blocker" and f.fix_hint and "150" not in f.message
    assert f.expected is None and not f.passed


def test_sag_warning_band():
    props = dict(SMALL, internal_resistance_mohm=55)
    ctx = _ctx(metrics={"peak_current_a": 12.0}, battery_props=props)
    out = thermal.run(ctx)
    assert [f.id for f in out] == ["thermal.sag"]


def test_peak_current_falls_back_to_motor_max():
    ctx = _ctx(battery_props=GOOD)
    ctx.r.parts.append(SimpleNamespace(part=SimpleNamespace(id="wm", kind="weapon_motor", _extra={}),
                                       cat=SimpleNamespace(id="bl_1806_2300kv", kind="weapon_motor",
                                                           props={"max_current_a": 15.0})))
    out = thermal.run(ctx)
    assert [f.id for f in out] == ["thermal.ok"]
    assert "lower bound" in out[0].message


def test_esc_overcurrent_warns():
    ctx = _ctx(metrics={"peak_current_a": 8.0}, battery_props=GOOD, esc_props={"max_current_a": 5.0})
    ids = [f.id for f in thermal.run(ctx)]
    assert "thermal.esc_overcurrent" in ids and "thermal.ok" in ids
