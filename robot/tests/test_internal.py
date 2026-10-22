"""Internal flaws: parts touching nothing, screws through air, wires through solids."""

import numpy as np

from robot import spec, world
from robot.checks import Ctx, Options, internal, verify
from robot.finding import Route

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731
BASE = {"id": "base", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(40, 40, 4), "at": [0, 0, 2]}


def rep(parts, fasteners=()):
    return verify(spec.Spec({"name": "t", "parts": [BASE, *parts], "fasteners": list(fasteners)}),
                  Options(only=["internal"], deep=False, fast=True))


def test_no_contact_good_and_bad():
    on = {"id": "blk", "kind": "structure", "material": "pla", "shape": BOX(10, 10, 4), "at": [0, 0, 6]}
    assert rep([on]).get("internal.no_contact").passed
    off = dict(on, at=[0, 0, 12])
    r = rep([off])
    assert r.failed("internal.no_contact")
    assert any("blk" in f.parts for f in r.findings if f.id == "internal.no_contact" and not f.passed)


def test_fastener_void_good_and_bad():
    good = {"id": "s", "designation": "M2x4", "at": [0, 0, 4], "dir": [0, 0, -1], "threads_into": "base", "tool": "hex1.5"}
    assert rep([], [good]).get("internal.fastener_void").passed
    bad = dict(good, at=[0, 0, 20])
    assert rep([], [bad]).failed("internal.fastener_void")


def _ctx(route_pts):
    wall = {"id": "wall", "kind": "structure", "material": "pla", "shape": BOX(4, 40, 20), "at": [0, 0, 10]}
    s = spec.Spec({"name": "t", "parts": [BASE, wall], "wires": [{"id": "w1", "from": "base.a", "to": "base.b"}]})
    r = world.resolve(s, fast=True)
    c = Ctx(r, world.World.start(r), Options(fast=True))
    c.routes = [Route("w1", 28, "signal", 1.1, 0.0, route_pts)]
    return c


def test_wire_in_solid_good_and_bad():
    bad = internal.wire_in_solid(_ctx([[-15, 0, 10], [15, 0, 10]]))
    assert any(not f.passed and f.id == "internal.wire_in_solid" for f in bad)
    good = internal.wire_in_solid(_ctx([[-15, 0, 10], [-15, 0, 25], [15, 0, 25], [15, 0, 10]]))
    assert all(f.passed for f in good) and good


def test_wire_without_routes_is_not_checked():
    c = _ctx([])
    c.routes = []
    assert internal.wire_in_solid(c) == [] and any("wire_in_solid" in n for n in c.not_checked)


def test_solid_invalid_good_and_bad():
    import trimesh

    s = spec.Spec({"name": "t", "parts": [BASE]})
    r = world.resolve(s, fast=True)
    c = Ctx(r, world.World.start(r), Options(fast=True))
    assert all(f.passed for f in internal.solid_valid(c))
    b = c.world.bodies[0]
    m = b.mesh.copy()
    m.invert()  # inside-out: negative volume
    b._mesh, b._man = m, None
    f = internal.solid_valid(c)
    assert any(x.id == "internal.solid_invalid" and not x.passed for x in f) and c.not_checked


def test_no_contact_waiver_claims_one_pair_with_cited_reason():
    # battery at the STEP height with a 1 mm gap to the tub floor and no pad modelled (RVRN 2.0 battery at STEP z12)
    gap = {"id": "blk", "kind": "structure", "material": "pla", "shape": BOX(10, 10, 4), "at": [0, 0, 7.5]}
    good = dict(gap, no_contact_ok={"with": "base", "reason": "held by the STEP press fit at RV16 z12, no pad modelled"})
    assert not rep([good]).failed("internal.no_contact")
    for bad in ({"with": "base", "reason": "it is fine"},                                       # too short, no citation
                {"with": "base", "reason": "held there by friction and nothing else at all"},   # no citation
                {"with": "nope", "reason": "held by the STEP press fit at RV16 z12, no pad"}):  # unknown partner
        assert rep([dict(gap, no_contact_ok=bad)]).failed("internal.no_contact")
    far = dict(good, at=[0, 0, 12])   # 6 mm off: beyond the waivable gap
    assert rep([far]).failed("internal.no_contact")


def test_tape_is_a_hold_method():
    from robot.checks.support import HOLD_METHODS

    assert "tape" in HOLD_METHODS and "glue" in HOLD_METHODS
