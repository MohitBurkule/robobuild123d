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


def _pinned_plate(teardown=None):
    """A plate with a cross pin through it inside an open-top cup: the pin cannot lift out of the plate's hole and
    the plate cannot lift off the pin; the cup walls stop both sideways. Only together do they lift out."""
    cup = {"id": "cup", "kind": "structure", "material": "pla",
           "shape": {"type": "subtract", "base": {"type": "box", "size": [40, 40, 30]},
                     "cut": [{"type": "place", "shape": {"type": "box", "size": [30, 30, 30]}, "at": [0, 0, 5]}]}}
    plate = {"id": "plate", "kind": "armor", "material": "pla", "at": [0, 0, 2],
             "shape": {"type": "subtract", "base": {"type": "box", "size": [4, 29.6, 20]}, "cut": [{"type": "box", "size": [6, 4, 4]}]}}
    pin = box("pin", (0, 0, 2), (29.6, 3, 3), kind="pin")
    d = {"name": "t", "parts": [cup, plate, pin]}
    if teardown:
        d["teardown"] = teardown
    r = world.resolve(spec.Spec(d), fast=True)
    c = Ctx(r, world.World.start(r), Options(fast=True))
    return assembly.run(c), c


def test_interlocked_pair_trapped_without_teardown():
    fs, _ = _pinned_plate()
    assert {p for f in fs if f.id == "assembly.blocked" for p in f.parts} == {"plate", "pin"}


def test_declared_teardown_move_frees_interlocked_pair():
    fs, c = _pinned_plate([{"parts": ["plate", "pin"], "dir": [0, 0, 1], "reason": "pin and plate lift out as one"}])
    assert fs[0].id == "assembly.order" and fs[0].passed
    assert {s.id for s in c.assembly} == {"plate", "pin"}
    # the field survives Spec.copy() (to_dict keeps it)
    assert spec.Spec({"teardown": [{"parts": ["a"], "dir": [0, 0, 1]}]}).copy().teardown[0]["parts"] == ["a"]


def test_small_part_with_two_leg_exit_assembles():
    """A nut in a pocket whose open side faces a cavity wall: it slides in 3 mm, then drops out through the floor."""
    shell = {"id": "shell", "kind": "structure", "material": "pla",
             "shape": {"type": "subtract", "base": {"type": "box", "size": [20, 30, 30]},
                       "cut": [{"type": "place", "shape": {"type": "box", "size": [4, 4, 4]}, "at": [5, 0, 0]},
                               {"type": "place", "shape": {"type": "box", "size": [14, 30, 30]}, "at": [-3, 0, -2]}]}}
    nut = box("nut", (5, 0, 0), (3.6, 3.6, 3.6), kind="nut")
    fs, c = _run([shell, nut])
    assert not [f for f in fs if f.id == "assembly.blocked"], [f.message for f in fs]
    assert {s.id for s in c.assembly} == {"nut"}


def test_assembly_ok_waiver_claims_one_trapped_part():
    shell = {"id": "shell", "kind": "structure", "material": "pla",
             "shape": {"type": "subtract", "base": {"type": "box", "size": [30, 30, 30]}, "cut": [{"type": "box", "size": [20, 20, 20]}]}}
    why = {"reason": "RVRN RV12 N10 goes in tilted shaft-first through the closed keyhole"}
    a = box("mot", (-5, 0, 0), (8, 16, 16), kind="motor", assembly_ok=why)
    b = box("bat", (5, 0, 0), (8, 16, 16), kind="battery")
    fs, c = _run([shell, a, b])
    assert [f.parts for f in fs if f.id == "assembly.waived"] == [["mot"]]
    assert [f.parts for f in fs if f.id == "assembly.blocked"] == [["bat"]]   # claims one part only
    a["assembly_ok"] = {"reason": "trust me, it goes in somehow"}            # uncited: no waiver
    fs, _ = _run([shell, a])
    f = [x for x in fs if x.id == "assembly.blocked"]
    assert f and "Invalid assembly_ok" in f[0].message and not [x for x in fs if x.id == "assembly.waived"]
