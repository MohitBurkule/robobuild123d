"""A screw threaded into a standoff that can only leave after it: the screw counts as removed once its shank has cleared the host."""
from robot import spec
from robot.checks import Options, verify


def part(id, kind, shape, at, **kw):
    return {"id": id, "kind": kind, "shape": shape, "at": list(at), "material": "steel", "process": "cnc", **kw}


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def screw(host_x, wall_x):
    # (the screw's `at` is its head end, it extends -x; it backs out along +x) base with a standoff holding a screw lying along x; a far wall at wall_x stops the straight slide to infinity
    d = {"name": "sh", "parts": [part("base", "structure", box(80, 30, 4), (0, 0, 0)),
                                 part("stand", "other", box(6, 6, 6), (host_x, 0, 5)),
                                 part("wall", "other", box(2, 20, 20), (wall_x, 0, 8)),
                                 # the standoff sits in a closed channel (roof, side plates, end plug), so it can only leave once the screw is out of its way... and it never can: the circular case
                                 part("roof", "other", box(6, 20, 2), (0, 0, 9.5)),
                                 part("sl", "other", box(60, 2, 20), (0, -4, 8)),
                                 part("sr", "other", box(60, 2, 20), (0, 4, 8)),
                                 part("plug", "other", box(2, 20, 20), (-29, 0, 8))],
         "fasteners": [{"id": "scr", "designation": "M2x8", "material": "steel", "at": [host_x, 0, 5], "dir": [-1, 0, 0],
                        "through": [], "threads_into": "stand", "removable": True}]}
    rep = verify(spec.Spec(d), Options(fast=True, only=["assembly"]))
    return [f for f in rep.findings if f.id == "assembly.blocked" and not f.passed and "`scr` is trapped" in f.message]


def test_screw_clears_host_before_wall_is_not_blocked():
    assert screw(0, 30) == []


def test_screw_still_inside_host_at_wall_is_blocked():
    assert screw(0, 4.5)


def test_screw_boxed_in_after_backing_out_still_fails():
    # same channel, but a lid box above and below the screw's lane blocks every sideways exit after it clears the host
    d = {"name": "sh", "parts": [part("base", "structure", box(80, 30, 4), (0, 0, 0)),
                                 part("stand", "other", box(6, 6, 6), (0, 0, 5)),
                                 part("wall", "other", box(2, 20, 20), (30, 0, 8)),
                                 part("roof", "other", box(60, 20, 2), (0, 0, 9.5)),
                                 part("sl", "other", box(60, 2, 20), (0, -4, 8)),
                                 part("sr", "other", box(60, 2, 20), (0, 4, 8)),
                                 part("plug", "other", box(2, 20, 20), (-29, 0, 8))],
         "fasteners": [{"id": "scr", "designation": "M2x8", "material": "steel", "at": [0, 0, 5], "dir": [-1, 0, 0],
                        "through": [], "threads_into": "stand", "removable": True}]}
    rep = verify(spec.Spec(d), Options(fast=True, only=["assembly"]))
    assert [f for f in rep.findings if f.id == "assembly.blocked" and not f.passed and "`scr` is trapped" in f.message]
