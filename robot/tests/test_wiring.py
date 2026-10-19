"""Wiring: gauge table, routing through free space, metrics and routes."""

import numpy as np

from robot import spec, world
from robot.checks import Ctx, Options, wiring

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def test_gauge_table():
    assert wiring.wire_od(26) == 1.3 and wiring.wire_od(18) == 2.6 and wiring.wire_od(29.1) == 0.9
    assert wiring.default_awg("power") == 24 and wiring.default_awg("x") == 30
    assert abs(wiring.wire_g_per_mm(26) - 0.0013 * 1.69) < 1e-12


def test_tube_dist():
    d = wiring.tube_dist([[0, 0, 0], [10, 0, 0]], [[5, 3, 0], [-4, 0, 0]])
    assert np.allclose(d, [3, 4])


def test_wedge_routes():
    r = world.resolve(spec.load(ROOT / "templates" / "wedge_2wd.json"), fast=True)
    ctx = Ctx(r, world.World.start(r), Options(fast=True))
    out = wiring.run(ctx)
    assert any(f.id == "wiring.route" for f in out)
    assert len(ctx.routes) == len(r.spec.wires)
    assert 150 < ctx.metrics["wire_length_mm"] < 400
    assert ctx.metrics["wire_mass_g"] > 0
    # routes keep clear of one another
    for i, a in enumerate(ctx.routes):
        for b in ctx.routes[i + 1:]:
            P = np.asarray(a.points)
            seg = np.vstack([P[k] + (P[k + 1] - P[k]) * t for k in range(len(P) - 1) for t in np.linspace(0, 1, 20)])
            far = np.min([np.linalg.norm(seg - e, axis=1) for e in (P[0], P[-1], np.asarray(b.points[0]), np.asarray(b.points[-1]))], axis=0) > wiring.PORT_ZONE
            if far.any():
                assert wiring.tube_dist(b.points, seg[far]).min() >= (a.od_mm + b.od_mm) / 2 - 0.05  # 0.25 mm sampling, as Rust


def test_no_wires_note():
    s = spec.load(ROOT / "templates" / "wedge_2wd.json")
    s.wires = []
    r = world.resolve(s, fast=True)
    out = wiring.run(Ctx(r, world.World.start(r), Options(fast=True)))
    assert [f.id for f in out] == ["wiring.none"]


def test_via_waypoints_followed():
    """A wire's declared `via` waypoints lie on its route: the router goes leg by leg and never pulls taut past them."""
    import copy
    base = spec.load(ROOT / "templates" / "wedge_2wd.json")
    r0 = world.resolve(base, fast=True)
    ctx0 = Ctx(r0, world.World.start(r0), Options(fast=True))
    wiring.run(ctx0)
    rt = ctx0.routes[0]
    P = np.asarray(rt.points)
    seg = np.vstack([P[k] + (P[k + 1] - P[k]) * t for k in range(len(P) - 1) for t in np.linspace(0, 1, 9)])
    via = seg[len(seg) // 2].tolist()   # a free point (on a clear route)
    d = copy.deepcopy(base.raw)
    for w in d["wires"]:
        if w["id"] == rt.id:
            w["via"] = [via]
    r = world.resolve(spec.Spec(d, base.base_dir), fast=True)
    ctx = Ctx(r, world.World.start(r), Options(fast=True))
    wiring.run(ctx)
    Q = np.asarray(next(x for x in ctx.routes if x.id == rt.id).points)
    assert np.linalg.norm(Q - np.asarray(via), axis=1).min() < 1e-6
