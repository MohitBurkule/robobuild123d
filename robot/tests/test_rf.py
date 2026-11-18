"""RF placement check (robot/checks/rf.py): receiver noise distance and antenna exit path."""

import numpy as np
from types import SimpleNamespace

from robot.checks import rf


def _body(bid, kind, center, size=(20, 14, 4), material=None, part_idx=None, fastener=False):
    c = np.asarray(center, float)
    half = np.asarray(size, float) / 2
    return SimpleNamespace(id=bid, kind=kind, fastener=fastener, is_wire=False, center=c,
                           aabb=np.array([c - half, c + half]), part_idx=part_idx)


def _ctx(bodies, parts=None):
    parts = parts or []
    rparts = [SimpleNamespace(part=p, cat=None, geom=None) for p in parts]
    return SimpleNamespace(r=SimpleNamespace(spec=SimpleNamespace(raw={}), parts=rparts),
                           world=SimpleNamespace(bodies=bodies), not_checked=[], metrics={})


def _part(pid, kind, material=None):
    return SimpleNamespace(id=pid, kind=kind, material=material, _extra={})


def test_no_receiver_is_not_checked():
    ctx = _ctx([_body("m1", "motor", [0, 0, 0])], [_part("m1", "motor")])
    assert rf.run(ctx) == []
    assert any("no receiver" in x for x in ctx.not_checked)


def test_receiver_next_to_esc_warns():
    parts = [_part("rx", "receiver"), _part("esc", "esc")]
    bodies = [_body("rx", "receiver", [0, 0, 10]), _body("esc", "esc", [12, 0, 10], size=(15, 10, 5))]
    ctx = _ctx(bodies, parts)
    out = rf.run(ctx)
    assert "rf.noise_proximity" in [f.id for f in out]
    f = next(f for f in out if f.id == "rf.noise_proximity")
    assert f.severity == "warning" and not f.passed and f.fix_hint
    assert ctx.metrics["rf_min_noise_mm.rx"] == 12.0


def test_moderate_distance_still_warns():
    parts = [_part("rx", "receiver"), _part("esc", "esc")]
    bodies = [_body("rx", "receiver", [0, 0, 10]), _body("esc", "esc", [25, 0, 10])]
    out = rf.run(_ctx(bodies, parts))
    assert "rf.noise_proximity" in [f.id for f in out]


def test_receiver_far_from_noise_ok():
    parts = [_part("rx", "receiver"), _part("esc", "esc")]
    bodies = [_body("rx", "receiver", [0, 0, 10]), _body("esc", "esc", [60, 0, 10])]
    out = rf.run(_ctx(bodies, parts))
    assert [f.id for f in out] == ["rf.ok"]


def test_conductive_plate_over_receiver_blocks_antenna():
    parts = [_part("rx", "receiver"), _part("plate", "plate", "aluminium"), _part("esc", "esc")]
    bodies = [_body("rx", "receiver", [0, 0, 10], part_idx=0), _body("plate", "plate", [0, 0, 18], size=(60, 60, 2), part_idx=1),
              _body("esc", "esc", [60, 0, 10], part_idx=2)]
    out = rf.run(_ctx(bodies, parts))
    assert "rf.antenna_blocked" in [f.id for f in out]
    f = next(f for f in out if f.id == "rf.antenna_blocked")
    assert f.severity == "warning" and f.fix_hint


def test_plastic_over_receiver_is_fine():
    parts = [_part("rx", "receiver"), _part("lid", "plate", "petg")]
    bodies = [_body("rx", "receiver", [0, 0, 10], part_idx=0), _body("lid", "plate", [0, 0, 18], size=(60, 60, 2), part_idx=1)]
    out = rf.run(_ctx(bodies, parts))
    assert [f.id for f in out] == ["rf.ok"]


def test_carbon_filled_counts_as_conductive():
    parts = [_part("rx", "receiver"), _part("lid", "plate", "pa_cf")]
    bodies = [_body("rx", "receiver", [0, 0, 10], part_idx=0), _body("lid", "plate", [0, 0, 18], size=(60, 60, 2), part_idx=1)]
    out = rf.run(_ctx(bodies, parts))
    assert "rf.antenna_blocked" in [f.id for f in out]
