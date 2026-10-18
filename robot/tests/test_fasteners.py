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
