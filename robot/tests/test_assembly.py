"""Assembly by disassembly."""

from robot import spec, world
from robot.checks import Ctx, Options, assembly
from robot.tests.test_interference import box


def _run(parts):
    r = world.resolve(spec.Spec({"name": "t", "parts": parts}), fast=True)
    c = Ctx(r, world.World.start(r), Options(fast=True))
    return assembly.run(c), c


def test_open_box_assembles():
    parts = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-8, 0, 0), (2, 30, 10), kind="armor"),
             box("bat", (0, 0, 0), (14, 14, 10), kind="battery")]
    fs, c = _run(parts)
    assert fs[0].id == "assembly.order" and fs[0].passed
    assert {s.id for s in c.assembly} == {"w1", "bat"}


def test_trapped_part_blocked():
    shell = {"id": "shell", "kind": "structure", "material": "pla",
             "shape": {"type": "subtract", "base": {"type": "box", "size": [30, 30, 30]}, "cut": [{"type": "box", "size": [20, 20, 20]}]}}
    fs, c = _run([shell, box("bat", (0, 0, 0), (14, 14, 14), kind="battery")])
    f = [x for x in fs if x.id == "assembly.blocked"]
    assert f and f[0].parts == ["bat"] and "shell" in f[0].message
