"""Wire care checks (robot/checks/wire_care.py): chafe, bend radius, strain relief (G5)."""

from types import SimpleNamespace

import numpy as np

from robot.checks import wire_care
from robot.spec import Spec


class Body:
    def __init__(self, id, aabb, hollow=False):
        self.id = id
        self.aabb = np.asarray(aabb, float)
        self.is_wire = False
        self.fastener = False
        self.part_idx = 0
        self._hollow = hollow

    def inside(self, P):
        if self._hollow:
            return np.zeros(len(np.atleast_2d(P)), bool)
        lo, hi = self.aabb
        return np.all((np.atleast_2d(P) >= lo) & (np.atleast_2d(P) <= hi), axis=1)


def _ctx(wires, parts, bodies=None):
    spec = Spec({"parts": parts, "wires": wires})
    bs = bodies if bodies is not None else [Body(p["id"], p.get("_aabb", [[-9, -9, -9], [9, 9, 9]])) for p in parts]

    def port(r, name):
        pid, pname = str(name).split(".", 1)
        for p in parts:
            if p["id"] == pid:
                return np.asarray(p.get("_ports", {}).get(pname, [0.0, 0.0, 0.0]), float)
        return None

    world = SimpleNamespace(bodies=bs, port=port, body=lambda pid: next((b for b in bs if b.id == pid), None))
    return SimpleNamespace(r=SimpleNamespace(spec=spec, parts=[]), world=world, not_checked=[], metrics={})


def _parts(*ids):
    return [{"id": i, "kind": "structure"} for i in ids]


WIRE = {"id": "w1", "from": "esc.out", "to": "rx.in", "kind": "signal"}


def test_straight_wire_passes():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}}]
    ctx = _ctx([WIRE], parts, bodies=[])
    out = wire_care.run(ctx)
    assert [f.id for f in out] == ["wire_care.ok"]


def test_tight_via_bend_warns():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}}]
    w = dict(WIRE, via=[[9, 0, 0], [10, 0.5, 0], [11, 0, 0]])  # a hairpin: radius ~ 1.25 mm
    ctx = _ctx([w], parts, bodies=[])
    out = wire_care.run(ctx)
    assert [f.id for f in out] == ["wire_care.bend"]
    f = out[0]
    assert f.severity == "warning" and not f.passed and f.fix_hint
    assert "w1" in f.parts


def test_open_via_bend_is_fine():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}}]
    w = dict(WIRE, via=[[8, 0, 0], [10, 6, 0], [12, 0, 0]])  # a wide swoop
    ctx = _ctx([w], parts, bodies=[])
    assert [f.id for f in wire_care.run(ctx)] == ["wire_care.ok"]


def test_chafe_through_a_wall_warns():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}},
             {"id": "wall", "kind": "structure"}]
    wall = Body("wall", [[9, -5, -5], [11, 5, 5]], hollow=True)  # a hollow wall: the wire passes through a hole
    ctx = _ctx([dict(WIRE, via=[[10, 0, 0]])], parts, bodies=[wall])
    out = wire_care.run(ctx)
    assert [f.id for f in out] == ["wire_care.chafe"]
    f = out[0]
    assert f.severity == "warning" and not f.passed and f.fix_hint
    assert "wall" in f.message


def test_grommet_opts_chafe_out():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}},
             {"id": "wall", "kind": "structure"}]
    wall = Body("wall", [[9, -5, -5], [11, 5, 5]], hollow=True)
    ctx = _ctx([dict(WIRE, via=[[10, 0, 0]], grommet=True)], parts, bodies=[wall])
    assert [f.id for f in wire_care.run(ctx)] == ["wire_care.ok"]


def test_long_run_inside_a_part_is_not_chafe():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "rx", "kind": "receiver", "_ports": {"in": [20, 0, 0]}},
             {"id": "tub", "kind": "structure"}]
    tub = Body("tub", [[-1, -5, -5], [21, 5, 5]], hollow=True)  # the whole wire runs through the open tub
    ctx = _ctx([WIRE], parts, bodies=[tub])
    assert [f.id for f in wire_care.run(ctx)] == ["wire_care.ok"]


def test_strain_relief_needed_at_vibrating_end():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "m", "kind": "weapon_motor", "_ports": {"ph": [20, 0, 0]}}]
    w = {"id": "w1", "from": "esc.out", "to": "m.ph", "kind": "motor"}
    ctx = _ctx([w], parts, bodies=[])
    out = wire_care.run(ctx)
    assert [f.id for f in out] == ["wire_care.strain_relief"]
    f = out[0]
    assert f.severity == "warning" and not f.passed and f.fix_hint
    assert "m" in f.message


def test_strain_relief_satisfied_by_via_anchor():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "m", "kind": "weapon_motor", "_ports": {"ph": [20, 0, 0]}}]
    w = {"id": "w1", "from": "esc.out", "to": "m.ph", "kind": "motor", "via": [[19, 0, 3]]}
    assert [f.id for f in wire_care.run(_ctx([w], parts, bodies=[]))] == ["wire_care.ok"]


def test_strain_relief_satisfied_by_slack_or_note():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}},
             {"id": "m", "kind": "weapon_motor", "_ports": {"ph": [20, 0, 0]}}]
    w1 = {"id": "w1", "from": "esc.out", "to": "m.ph", "kind": "motor", "slack_mm": 8.0}
    assert [f.id for f in wire_care.run(_ctx([w1], parts, bodies=[]))] == ["wire_care.ok"]
    w2 = {"id": "w1", "from": "esc.out", "to": "m.ph", "kind": "motor", "strain_relief": "molded boot"}
    assert [f.id for f in wire_care.run(_ctx([w2], parts, bodies=[]))] == ["wire_care.ok"]


def test_unresolved_port_is_not_checked():
    parts = [{"id": "esc", "kind": "esc", "_ports": {"out": [0, 0, 0]}}]
    ctx = _ctx([WIRE], parts, bodies=[])
    assert wire_care.run(ctx) == []
    assert any("do not resolve" in x for x in ctx.not_checked)


def test_no_wires_is_not_checked():
    ctx = _ctx([], [])
    assert wire_care.run(ctx) == []
    assert any("no wires" in x for x in ctx.not_checked)
