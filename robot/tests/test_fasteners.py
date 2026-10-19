"""Fasteners: driver access, thread engagement, head seat."""

from robot import spec
from robot.checks import Options, verify
from robot.checks.fasteners import tool_radius

BOX = lambda x, y, z: {"type": "box", "size": [x, y, z]}  # noqa: E731


def run(fast, extra=()):
    parts = [
        {"id": "plate", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(30, 30, 2), "at": [0, 0, -1]},
        {"id": "block", "kind": "structure", "material": "pla", "process": "fdm", "shape": BOX(30, 30, 6), "at": [0, 0, -5]},
        *extra,
    ]
    return verify(spec.Spec({"name": "t", "parts": parts, "fasteners": [fast]}), Options(only=["fasteners"], deep=False, fast=True))


F = {"id": "s", "designation": "M2x8", "at": [0, 0, 0], "dir": [0, 0, -1], "through": ["plate"], "threads_into": "block", "tool": "hex1.5"}


def test_tool_radius():
    assert abs(tool_radius("hex1.5") - (1.5 * 0.5 * 1.16 + 0.4)) < 1e-9 and tool_radius("torx6") == 1.5


def test_good_screw():
    assert run(F).get("fastener.ok").passed


def test_blocked_driver():
    cover = {"id": "cover", "kind": "plate", "material": "pla", "process": "fdm", "shape": BOX(30, 30, 2), "at": [0, 0, 8]}
    f = run(F, [cover]).get("fastener.access")
    assert f and not f.passed and "cover" in f.parts


def test_short_engagement_and_no_seat():
    rep = run(dict(F, designation="M2x3"))
    assert rep.failed("fastener.engagement")
    rep = run(dict(F, at=[0, 0, 3]))
    assert rep.failed("fastener.head_seat")


def test_no_tool_and_no_thread():
    rep = run({"id": "s", "designation": "M2x8", "at": [0, 0, 0], "through": ["plate"]})
    assert rep.failed("fastener.no_tool") and rep.failed("fastener.no_thread")


def test_drive_recess_and_hex_nut_shapes():
    from robot import catalog
    from robot.cad import fastener_catalog as fc
    from robot.world import fastener_shape

    for head in (None, "button", "countersunk"):
        assert catalog.has_drive_recess(fastener_shape(3.0, 10.0, head=head))
    plain = catalog.union([catalog.cyl(2.75, 3.0), catalog.cyl(1.5, 10.0)])  # bad: the old drive-less cylinder head
    assert not catalog.has_drive_recess(plain)
    assert catalog.is_hex_nut(catalog.hex_nut(5.5, 2.4, 3.0))
    assert not catalog.is_hex_nut(catalog.minus(catalog.cyl(2.75, 2.4), [catalog.cyl(1.5, 3.0)]))
    assert fc.drive_key(3.0, "cap")[0] == 2.5 and fc.drive_key(3.0, "button")[0] == 2.0 and fc.drive_key(3.0, "countersunk")[0] == 2.0


def test_drive_check_good_and_bad():
    rep = run(F)
    assert rep.get("fastener.drive").passed and not rep.failed("fastener.drive_key")
    nut_ok = {"id": "n", "kind": "nut", "material": "steel", "catalog": "nut_m2", "at": [20, 20, 10]}
    assert run(F, [nut_ok]).get("fastener.drive").passed
    nut_bad = {"id": "n", "kind": "nut", "material": "steel", "process": "cots",
               "shape": {"type": "subtract", "base": {"type": "cylinder", "radius": 2.0, "height": 1.6},
                         "cut": [{"type": "cylinder", "radius": 1.0, "height": 3.0}]}, "at": [20, 20, 10]}
    assert run(F, [nut_bad]).failed("fastener.nut_hex")
    assert run(dict(F, tool="hex2")).failed("fastener.drive_key")  # M2 cap has a 1.5 socket
