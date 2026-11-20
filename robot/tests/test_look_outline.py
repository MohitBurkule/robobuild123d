"""robot outline / robot window on a hollow printed box."""
import json

from robot import look_outline
from robot import spec as spec_mod
from robot import world as world_mod


def _spec(tmp_path, extra=()):
    shell = {"type": "subtract", "base": {"type": "box", "size": [60, 60, 20]},
             "cut": [{"type": "box", "size": [56, 56, 16]}]}
    sp = {"name": "outlinetest", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0], "shape": shell},
        *extra], "fasteners": [], "wires": [], "connections": []}
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(sp))
    return p


def _body(p, i):
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(str(p)), fast=True))
    return next(b for b in w.bodies if b.id == i)


def test_chamfer_keeps_a_skin(tmp_path):
    p = _spec(tmp_path)
    look_outline.outline(str(p), "chassis", "chamfer", "+y+z", 6.0, 6.0)
    b = _body(p, "chassis")
    assert not b.inside([[0, 29.5, 9.5]]).any()          # the corner is gone
    assert b.inside([[0, 28.5, 4.0]]).any() or b.inside([[0, 27.0, 5.5]]).any()   # a skin behind the bevel
    assert not b.inside([[0, 0, 0]]).any()                # the cavity stays a cavity


def test_window_keeps_rim(tmp_path):
    bat = {"id": "el_battery", "kind": "battery", "catalog": "lipo_2s_180", "at": [0, 0, -4], "rot": [0, 0, 0]}
    p = _spec(tmp_path, [bat])
    look_outline.window(str(p), "chassis", "el_battery", "+z", 2.0)
    d = json.loads(p.read_text())
    cut = d["parts"][0]["shape"]["cut"][-1]
    assert cut["shape"]["type"] == "box"


def test_round_corner_keeps_a_skin(tmp_path):
    p = _spec(tmp_path)
    look_outline.outline(str(p), "chassis", "round", "+y+z", 8.0)
    b = _body(p, "chassis")
    assert not b.inside([[0, 29.5, 9.5]]).any()          # the corner is gone
    assert b.inside([[0, 29.5, 1.0]]).any()               # the face below the fillet is untouched
    assert not b.inside([[0, 0, 0]]).any()


def test_stairs_drop_in_steps(tmp_path):
    p = _spec(tmp_path)
    look_outline.outline(str(p), "chassis", "stairs", "+y+z", 6.0, 18.0, n=3)
    b = _body(p, "chassis")
    assert not b.inside([[0, 29.0, 9.5]]).any()           # outer step gone to the bottom tread
    assert not b.inside([[0, 15.0, 9.5]]).any()           # last tread is 2 mm down
    assert b.inside([[0, 10.0, 9.5]]).any()               # behind the stairs the top is intact


def test_notch_and_arc(tmp_path):
    p = _spec(tmp_path)
    look_outline.outline(str(p), "chassis", "notch", "+z+x", 4.0, 10.0, at=0.0)
    b = _body(p, "chassis")
    assert not b.inside([[0, 29.0, 9.5]]).any() and b.inside([[20, 29.0, 9.5]]).any()
    p2 = _spec(tmp_path)
    look_outline.outline(str(p2), "chassis", "arc", "+z+y", 5.0)
    b2 = _body(p2, "chassis")
    assert not b2.inside([[0, 29.0, 9.5]]).any()          # ends dropped
    assert b2.inside([[29.0, 0.0, 9.5]]).any()            # middle stays full height
