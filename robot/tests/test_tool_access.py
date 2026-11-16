"""Tool access checks (robot/checks/tool_access.py): driver path + wrench clearance (G4)."""

from types import SimpleNamespace

import numpy as np

from robot.checks import tool_access
from robot.profile import Profile
from robot.spec import Spec


class Body:
    def __init__(self, id, aabb, inside_box=None):
        self.id = id
        self.aabb = np.asarray(aabb, float)
        self.is_wire = False
        self.fastener = id.startswith("bolt_")
        self.part_idx = 0
        box = np.asarray(inside_box if inside_box is not None else aabb, float)
        self._box = box

    def inside(self, P):
        P = np.atleast_2d(P)
        lo, hi = self._box
        return np.all((P >= lo) & (P <= hi), axis=1)


def _ctx(fasteners, parts, bodies=None):
    spec = Spec({"parts": parts, "fasteners": fasteners})
    bs = bodies if bodies is not None else [Body(p["id"], p.get("_aabb", [[-10, -10, -10], [10, 10, 10]])) for p in parts]
    world = SimpleNamespace(bodies=bs, body=lambda pid: next((b for b in bs if b.id == pid), None))
    return SimpleNamespace(r=SimpleNamespace(spec=spec, parts=[], profile=Profile()), world=world, not_checked=[], metrics={})


SCREW = {"id": "s1", "designation": "M2x6", "at": [0, 0, 5], "dir": [0, 0, -1],
         "through": ["plate"], "threads_into": "nut1"}


def test_undeclared_tool_with_clear_path_passes():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut", "_aabb": [[-3, -3, -2], [3, 3, 0]]}]
    out = tool_access.run(_ctx([SCREW], parts))
    assert [f.id for f in out] == ["tool_access.ok"]


def test_undeclared_tool_blocked_is_a_blocker():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut", "_aabb": [[-3, -3, -2], [3, 3, 0]]}]
    overhang = Body("lid", [[-4, -4, 6], [4, 4, 8]])  # right above the screw head at z=5
    ctx = _ctx([SCREW], parts, bodies=[Body("plate", [[-5, -5, 0], [5, 5, 2]]),
                                       Body("nut1", [[-3, -3, -2], [3, 3, 0]]), overhang])
    out = tool_access.run(ctx)
    assert [f.id for f in out] == ["tool_access.blocked"]
    f = out[0]
    assert f.severity == "blocker" and not f.passed and f.fix_hint
    assert "lid" in f.message and "s1" in f.parts


def test_declared_tool_screws_are_left_to_fasteners():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut", "_aabb": [[-3, -3, -2], [3, 3, 0]]}]
    overhang = Body("lid", [[-4, -4, 6], [4, 4, 8]])
    ctx = _ctx([dict(SCREW, tool="hex1.5")], parts,
               bodies=[Body("plate", [[-5, -5, 0], [5, 5, 2]]), Body("nut1", [[-3, -3, -2], [3, 3, 0]]), overhang])
    assert [f.id for f in tool_access.run(ctx)] == ["tool_access.ok"]  # fasteners.access owns that verdict


def test_nut_ring_blocked_is_a_blocker():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut", "_aabb": [[-3, -3, -2], [3, 3, 0]]}]
    wall = Body("wall", [[2.0, -4, -3], [8, 4, 1]])  # hugs the nut's side: no wrench fits
    ctx = _ctx([SCREW], parts,
               bodies=[Body("plate", [[-5, -5, 0], [5, 5, 2]]), Body("nut1", [[-3, -3, -2], [3, 3, 0]]), wall])
    out = tool_access.run(ctx)
    assert [f.id for f in out] == ["tool_access.nut_blocked"]
    f = out[0]
    assert f.severity == "blocker" and not f.passed and f.fix_hint
    assert "wall" in f.message and "nut1" in f.parts


def test_nut_ring_clear_with_clamping_parts_only():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut", "_aabb": [[-3, -3, -2], [3, 3, 0]]}]
    out = tool_access.run(_ctx([SCREW], parts))
    assert [f.id for f in out] == ["tool_access.ok"]  # the plate is in the joint: it may cover the nut


def test_unparseable_designation_is_not_checked():
    ctx = _ctx([dict(SCREW, designation="widget")], [{"id": "plate", "kind": "structure"}])
    assert tool_access.run(ctx) == []
    assert any("not understood" in x for x in ctx.not_checked)


def test_no_fasteners_is_not_checked():
    ctx = _ctx([], [])
    assert tool_access.run(ctx) == []
    assert any("no fasteners" in x for x in ctx.not_checked)


def test_nut_not_a_body_is_not_checked():
    parts = [{"id": "plate", "kind": "structure", "_aabb": [[-5, -5, 0], [5, 5, 2]]},
             {"id": "nut1", "kind": "nut"}]
    ctx = _ctx([dict(SCREW, tool="hex1.5")], parts, bodies=[Body("plate", [[-5, -5, 0], [5, 5, 2]])])
    out = tool_access.run(ctx)
    assert [f.id for f in out] == ["tool_access.ok"]  # nothing judged at the nut, so no pass claim about it
    assert any("nut1" in x for x in ctx.not_checked)
