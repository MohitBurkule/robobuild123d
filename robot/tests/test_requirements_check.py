"""Requirements group (robot/checks/requirements.py): declared intent vs measured metrics."""

from types import SimpleNamespace

from robot.checks import requirements


def _ctx(req, metrics):
    spec = SimpleNamespace(raw={"requirements": req} if req else {}, parts=[], connections=[])
    return SimpleNamespace(r=SimpleNamespace(spec=spec, parts=[]), world=SimpleNamespace(bodies=[]),
                           not_checked=[], metrics=dict(metrics))


def test_no_requirements_block_is_not_checked():
    ctx = _ctx(None, {})
    assert requirements.run(ctx) == []
    assert ctx.not_checked and "no requirements" in ctx.not_checked[0]


def test_energy_requirement_pass_and_fail():
    good = requirements.run(_ctx({"weapon_energy_j": {"min": 5}}, {"weapon_energy_j": 8.0}))
    assert [f.id for f in good] == ["requirements.weapon_energy_j"] and good[0].passed
    bad = requirements.run(_ctx({"weapon_energy_j": {"min": 5}}, {"weapon_energy_j": 3.0}))
    f = bad[0]
    assert not f.passed and f.severity == "blocker" and f.fix_hint and f.expected and f.actual


def test_mass_max_and_margin():
    out = requirements.run(_ctx({"mass_max_g": {"max": 155}}, {"mass_total_g": 149.0}))
    assert out[0].passed
    out = requirements.run(_ctx({"mass_max_g": {"max": 148}}, {"mass_total_g": 149.0}))
    assert not out[0].passed
    out = requirements.run(_ctx({"mass_margin_g": {"min": 2}}, {"mass_hi_g": 149.0, "mass_limit_g": 150.0}))
    assert not out[0].passed and abs(float(out[0].actual.split()[0]) - 1.0) < 1e-6


def test_tip_speed_converted_from_mph():
    out = requirements.run(_ctx({"weapon_tip_speed_mps": {"min": 20}}, {"tip_speed_mph": 50.0}))
    assert out[0].passed  # 50 mph = 22.35 m/s
    out = requirements.run(_ctx({"weapon_tip_speed_mps": {"min": 25}}, {"tip_speed_mph": 50.0}))
    assert not out[0].passed


def test_unknown_key_blocks():
    out = requirements.run(_ctx({"colour": {"min": 1}}, {}))
    assert [f.id for f in out] == ["requirements.unknown_key"] and not out[0].passed


def test_missing_metric_is_not_checked():
    ctx = _ctx({"weapon_energy_j": {"min": 5}}, {})
    assert requirements.run(ctx) == []
    assert any("not computed" in x for x in ctx.not_checked)


def test_no_metric_yet_keys_go_to_not_checked():
    ctx = _ctx({"top_speed_mps": {"min": 1.5}, "push_force_n": {"min": 3}}, {})
    assert requirements.run(ctx) == []
    assert len(ctx.not_checked) == 2
