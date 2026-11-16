"""Engagement checks (robot/checks/engagement.py): screw length vs the clamped stack (G3)."""

from types import SimpleNamespace

import numpy as np

from robot.checks import engagement
from robot.spec import Spec


class _Body:
    def __init__(self, pid, aabb):
        self.id = pid
        self.aabb = np.asarray(aabb, float)
        self.is_wire = False
        self.fastener = False

    def inside(self, P):
        P = np.atleast_2d(P)
        lo, hi = self.aabb
        return np.all((P >= lo) & (P <= hi), axis=1)


def _body(pid, aabb):
    return _Body(pid, aabb)


def _ctx(fasteners, parts=None, review=None):
    spec = Spec({"parts": parts or [], "fasteners": fasteners, "review": review or {}})
    bodies = {p["id"]: _body(p["id"], p.pop("_aabb", [[-5, -5, 0], [5, 5, 2]])) for p in (parts or [])}
    world = SimpleNamespace(bodies=list(bodies.values()), body=lambda pid: bodies.get(pid))
    return SimpleNamespace(r=SimpleNamespace(spec=spec, parts=[]), world=world, not_checked=[], metrics={})


SCREW = {"id": "s1", "designation": "M2x8", "at": [0, 0, 5], "dir": [0, 0, -1],
         "through": ["plate"], "threads_into": "boss"}


def test_clamp_short_is_a_blocker():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 8]]},
             {"id": "boss", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, -4], [5, 5, 0]]}]
    ctx = _ctx([dict(SCREW, designation="M2x4")], parts)  # the 4 mm shank never spans the 8 mm plate
    out = engagement.run(ctx)
    assert [f.id for f in out] == ["engagement.clamp_short"]
    f = out[0]
    assert f.severity == "blocker" and not f.passed and f.fix_hint
    assert "plate" in f.message and f.expected and f.actual


def test_long_enough_screw_passes():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "boss", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, -4], [5, 5, 0]]}]
    ctx = _ctx([dict(SCREW, designation="M2x10")], parts)  # 2.5 mm stack, 4.5 mm into the boss = 225% of d
    out = engagement.run(ctx)
    assert [f.id for f in out] == ["engagement.ok"]
    assert ctx.metrics["fastener_engagement_min_pct"] == 225.0


def test_low_pct_in_printed_plastic_warns():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "boss", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, -0.5], [5, 5, 0]]}]
    ctx = _ctx([SCREW], parts)  # 1 mm in plastic = 50% of d
    out = engagement.run(ctx)
    assert [f.id for f in out] == ["engagement.pct_low"]
    f = out[0]
    assert f.severity == "warning" and f.fix_hint
    assert ctx.metrics["fastener_engagement_min_pct"] == 50.0


def test_marginal_pct_in_metal_host_is_fine():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "boss", "kind": "insert", "process": "cots", "_aabb": [[-5, -5, -1], [5, 5, 0]]}]
    ctx = _ctx([SCREW], parts)  # 1 mm in an insert = 50% of d, but metal: the 1.5 d floor governs
    out = engagement.run(ctx)
    assert [f.id for f in out] == ["engagement.ok"]


def test_plastic_band_is_tunable():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "boss", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, -1], [5, 5, 0]]}]
    ctx = _ctx([SCREW], parts, review={"engagement": {"plastic_x_d": 0.4, "reason": "nylon-carbon, strong threads"}})
    assert [f.id for f in engagement.run(ctx)] == ["engagement.ok"]


def test_unparseable_designation_is_not_checked():
    ctx = _ctx([dict(SCREW, designation="widget")])
    out = engagement.run(ctx)
    assert out == []
    assert any("not understood" in x for x in ctx.not_checked)


def test_no_fasteners_is_not_checked():
    ctx = _ctx([])
    assert engagement.run(ctx) == []
    assert any("no fasteners" in x for x in ctx.not_checked)


def test_metric_missing_without_host_engagement():
    parts = [{"id": "plate", "kind": "structure", "process": "fdm", "_aabb": [[-5, -5, 0], [5, 5, 2]]}]
    ctx = _ctx([dict(SCREW, threads_into=None, through=["plate"])], parts)
    out = engagement.run(ctx)
    assert [f.id for f in out] == ["engagement.ok"]
    assert "fastener_engagement_min_pct" not in ctx.metrics
