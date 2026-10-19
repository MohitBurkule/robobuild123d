"""Layout CSP of the template engine (robot/gen/layout)."""

import pytest

from robot.gen.layout import Component, Keepout, LayoutInputs, Link, solve
from robot.gen.layout import constraints as C
from robot.gen.layout.model import Placement
from robot.gen.layout.solver import distinct

BOX = [[-30, -40], [30, -40], [30, 40], [-30, 40]]


def _inp(**kw):
    comps = kw.pop("components", [Component("battery", "battery", (36, 17, 11), 21.5, min_front_mm=10, min_side_mm=5),
                                  Component("esc", "esc", (15, 10, 5), 3.0, ports={"m1": (7, 0, 0)}),
                                  Component("rx", "receiver", (20, 14, 4), 2.0)])
    return LayoutInputs(outline=BOX, components=comps, **kw)


def _ok(inp, pls):
    for c in inp.components:
        pl = pls[c.id]
        assert C.unary_ok(inp, c, pl), (c.id, [f(inp, c, pl) for f in C.UNARY])
    ids = list(pls)
    for i, a in enumerate(ids):
        assert C.binary_ok(inp, pls[a], [pls[b] for b in ids[:i]])


def test_solve_returns_distinct_legal_layouts():
    inp = _inp()
    lays = solve(inp, k=5)
    assert 2 <= len(lays) <= 5
    for L in lays:
        _ok(inp, L.placements)
    for i, a in enumerate(lays):
        for b in lays[:i]:
            assert distinct(a.placements, b.placements)
    assert [L.score for L in lays] == sorted(L.score for L in lays)


def test_keepouts_and_fixed_positions_respected():
    inp = _inp(keepouts=[Keepout("motor", -30, 30, -10, 10)])
    inp.components[2].fixed_at = (0.0, -25.0)
    for L in solve(inp, k=3):
        rx = L.placements["rx"]
        assert (rx.x, rx.y) == (0.0, -25.0)
        for p in L.placements.values():
            x0, x1, y0, y1 = p.rect(0.0)
            assert y1 <= -10 or y0 >= 10, p


def test_battery_margins():
    inp = _inp()
    b = inp.components[0]
    near_front = Placement("battery", 0, 40 - 9, 0, 0.0, b.footprint(0), b.extent(0))
    assert C.edge_margins(inp, b, near_front) == "too close to the front"


def test_impossible_raises_named_component():
    inp = _inp(components=[Component("huge", "battery", (90, 90, 5), 10)])
    with pytest.raises(ValueError, match="huge"):
        solve(inp, k=1)


def test_links_pull_components_together():
    inp = _inp(components=[Component("a", size=(10, 10, 4)), Component("b", size=(10, 10, 4))],
               links=[Link("a", "b")], anchors={})
    L = solve(inp, k=1)[0]
    pa, pb = L.placements["a"], L.placements["b"]
    assert abs(pa.x - pb.x) + abs(pa.y - pb.y) < 30


def test_from_dict_roundtrip():
    d = {"outline": BOX, "components": [{"id": "esc", "size": [15, 10, 5]}], "keepouts": [{"id": "k", "x0": -5, "x1": 5, "y0": -5, "y1": 5}]}
    assert solve(d, k=1)[0].placements["esc"]


def test_avoid_moves_component():
    inp = _inp()
    first = solve(inp, k=1)[0].placements["battery"]
    inp.avoid = [("battery", first.x, first.y, first.rot_z)]
    second = solve(inp, k=1)[0].placements["battery"]
    assert (second.x, second.y, second.rot_z) != (first.x, first.y, first.rot_z)
