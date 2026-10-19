"""Assembly with captive screws, button heads and motor face screws (RVRN weapon module: the upright-to-standoff screws
back out and stay in the upright, which then slides forward off the chassis)."""

import copy

from robot import spec
from robot.checks import Options, verify

PLA = {"material": "pla", "process": "fdm"}


def box(x0, x1, y0, y1, z0, z1):
    return {"type": "place", "shape": {"type": "box", "size": [x1 - x0, y1 - y0, z1 - z0]},
            "at": [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2], "rot": [0, 0, 0]}


def cylx(r, x0, x1, y, z):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": x1 - x0},
            "at": [(x0 + x1) / 2, y, z], "rot": [0, 90, 0]}


def run(d, *groups):
    rep = verify(spec.Spec(copy.deepcopy(d)), Options(fast=True, only=list(groups)))
    return [f for f in rep.findings if f.group in groups]


def failed(fs, fid):
    return [f for f in fs if f.id == fid and not f.passed]


def _module(gap):
    """A plate (x 0..4) with a cap `gap` mm behind the screw head; an M3x10 through the plate into a standoff
    (x 4..20); a hook on the base keeps the plate from leaving except forward (+y)."""
    return {"name": "t", "parts": [
        dict(id="base", kind="structure", shape={"type": "union", "items": [box(-30, 30, -30, 30, -2, 0), box(-12, 8, -12, -10, 0, 30), box(-14, -8.6, -10, 10, 0, 30)]}, **PLA),
        dict(id="plate", kind="plate", shape={"type": "union", "items": [
            {"type": "subtract", "base": box(0, 4, -10, 10, 1, 21), "cut": [cylx(1.6, -1, 5, 0, 10)]},
            box(-3 - gap - 3, -3 - gap, -10, 10, 1, 21), box(-3 - gap - 3, 4, -10, -8, 1, 21)]}, **PLA),
        dict(id="so", kind="pin", material="aluminium", process="cots",
             shape={"type": "subtract", "base": cylx(2.5, 4, 20, 0, 10), "cut": [cylx(1.25, 3, 21, 0, 10)]})],
        "fasteners": [{"id": "s", "designation": "M3x10", "at": [0, 0, 10], "dir": [1, 0, 0], "through": ["plate"],
                       "threads_into": "so", "tool": "hex2.5"}]}


def test_captive_screw_leaves_with_its_plate():
    # The head can back off 2 mm only: the screw cannot come out, but once the standoff has gone it stays in the plate.
    fs = run(_module(2.0), "assembly")
    assert not failed(fs, "assembly.blocked"), [f.message for f in failed(fs, "assembly.blocked")]


def test_captive_screw_still_blocks_when_its_shank_is_caught():
    # A wall just forward of the plate, past the standoff end, that the backed-off shank (tip at x 8) still crosses.
    d = _module(2.0)
    d["parts"][0]["shape"] = {"type": "union", "items": [d["parts"][0]["shape"], {"type": "subtract", "base": box(5, 9, -5, 5, 0, 30),
                                                                               "cut": [cylx(2.6, 4, 10, 0, 10)]}]}
    fs = run(d, "assembly")
    assert failed(fs, "assembly.blocked")


def test_button_head_is_low():
    from robot.world import button_dims
    dk, k = button_dims(3)
    assert abs(dk - 5.7) < 0.01 and abs(k - 1.65) < 0.01


def test_motor_face_screw_engagement_uses_the_motor_rule():
    d = {"name": "t", "parts": [
        dict(id="up", kind="structure", shape={"type": "subtract", "base": box(0, 4, -15, 15, -15, 15),
                                               "cut": [cylx(1.1, -1, 5, 8, 0)]}, **PLA),
        dict(id="m", kind="weapon_motor", catalog="be1806_bbb", at=[-10.25, 0, 0], rot=[90, 0, 180])],
        "fasteners": [{"id": "f", "designation": "M2x6", "at": [4, 8, 0], "dir": [-1, 0, 0], "through": ["up"],
                       "threads_into": "m", "tool": "hex1.5"}]}
    fs = run(d, "fasteners")
    assert not failed(fs, "fastener.engagement"), [f.message for f in failed(fs, "fastener.engagement")]
