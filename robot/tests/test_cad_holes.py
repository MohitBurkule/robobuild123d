import math

import build123d as bd
import numpy as np
import pytest
import trimesh

from robot.cad import fastener_catalog as fc
from robot.cad import seat
from robot.cad.holes import hole
from robot.geom import FINE, tessellate


def mesh(s):
    V, F = tessellate(s, FINE)
    return trimesh.Trimesh(V, F)


def block():
    return bd.Box(20, 20, 12)  # top face z = 6


def test_catalog_values():
    assert fc.head(3, "csk") == (6.72, 1.86)  # ISO 10642
    assert fc.head(3, "button") == (5.7, 1.65)  # ISO 7380
    assert fc.head(3, "cap") == (5.5, 3.0)  # ISO 4762
    assert fc.nut(3) == (5.5, 2.4) and fc.nut(3, "thin") == (5.5, 1.8)
    assert fc.clearance(2) == 2.4 and fc.tap_drill(2) == 1.6
    assert fc.parse("m2.5 x 8").designation == "M2.5x8"
    with pytest.raises(ValueError):
        fc.parse("M7x3")


def test_csk_volume_and_record():
    p, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "csk", "tapped", grip=3)
    r0, rc = rec.hole["csk_d"] / 2, rec.hole["clearance_d"] / 2
    h = rec.hole["csk_depth"]
    assert math.isclose(h, r0 - rc, abs_tol=1e-3)  # 90 deg cone
    cone = math.pi * h / 3 * (r0 ** 2 + r0 * rc + rc ** 2)
    tap = rec.hole["tap_d"] / 2
    expect = cone + math.pi * rc ** 2 * (3 - h) + math.pi * tap ** 2 * (10.5 - 3)
    assert math.isclose(block().volume - p.volume, expect, rel_tol=0.01)
    s = rec.to_spec("b", through=["blk"], threads_into="blk")
    assert s["head"] == "countersunk" and s["at"] == [0, 0, 6] and s["dir"] == [0, 0, -1]


def test_cap_counterbore_default_flush():
    p, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x8", "cap", "through")
    assert rec.at == (0.0, 0.0, 3.0)  # bearing face = surface - k
    assert rec.hole["cbore_depth"] == 3.0
    assert mesh(p).is_watertight


def test_nut_pocket_press_and_drop():
    _, a = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "cap", "nut", grip=4, nut_fit="press")
    _, b = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "cap", "nut", grip=4, nut_fit="drop")
    assert a.hole["nut_pocket_af"] == pytest.approx(5.55) and b.hole["nut_pocket_af"] == pytest.approx(5.8)


def test_placed_record_world():
    _, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M2x6", "button", "insert", grip=2)
    M = np.eye(4)
    M[:3, 3] = [10, 0, 0]
    assert rec.placed(M).at == (10.0, 0.0, 6.0)


@pytest.mark.parametrize("head,into,kw", [("csk", "tapped", {"grip": 3}), ("cap", "nut", {"grip": 4}),
                                          ("button", "insert", {"grip": 2}), ("cap", "through", {})])
def test_seat_probe_passes_own_hole(head, into, kw):
    p, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", head, into, **kw)
    f = rec.to_spec("x")
    rows = seat.judge(f, seat.probe(f, mesh(p).contains))
    assert all(r[1] for r in rows), rows


def _bad(rec, part):
    f = rec.to_spec("x")
    return {r[0] for r in seat.judge(f, seat.probe(f, mesh(part).contains)) if not r[1]}


def test_seat_probe_catches_missing_countersink():
    _, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "csk", "tapped", grip=3)
    wrong, _ = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "cap", "tapped", grip=3, cbore=0)
    assert "head_clash" in _bad(rec, wrong)


def test_seat_probe_catches_wrong_cbore_depth():
    _, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "cap", "through")
    shallow, _ = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "cap", "through", cbore=1.0)
    assert "cbore_depth" in _bad(rec, shallow)


def test_seat_probe_catches_sunk_csk():
    _, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "csk", "tapped", grip=3)
    deep, _ = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "csk", "tapped", grip=3, sink=1.0)
    assert "head_bearing" in _bad(rec, deep)  # cone 1 mm deeper than the head: it does not bear


def test_seat_probe_catches_proud_csk():
    p, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "csk", "tapped", grip=3)
    rec.at = (0.0, 0.0, 6.8)  # spec says the screw sits 0.8 mm proud
    assert "csk_flush" in _bad(rec, p)


def test_seat_probe_catches_missing_insert_bore():
    _, rec = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "button", "insert", grip=2)
    tapped, _ = hole(block(), (0, 0, 6), (0, 0, -1), "M3x10", "button", "tapped", grip=2)
    assert "insert_bore" in _bad(rec, tapped)
