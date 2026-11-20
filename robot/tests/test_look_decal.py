"""robot decal: a flush, fused colour-split graphic on a printed part."""
import json

import pytest

from robot import look_decal
from robot import spec as spec_mod
from robot import world as world_mod


def _spec(tmp_path, shell=None, extra=()):
    shell = shell or {"type": "box", "size": [60, 40, 20]}
    sp = {"name": "decaltest", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0], "shape": shell},
        *extra], "fasteners": [], "wires": [], "connections": []}
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(sp))
    return p


def _bodies(p):
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(str(p)), fast=True))
    return {b.id: b for b in w.bodies}


def test_pair_of_eyes_is_flush_and_fused(tmp_path):
    p = _spec(tmp_path)
    look_decal.decal(str(p), "chassis", "+y", "circle", [8.0], "0,4", 24.0, color="#ffffff", pid="eyes")
    d = json.loads(p.read_text())
    eyes = next(q for q in d["parts"] if q["id"] == "eyes")
    assert eyes["fused_with"] == "chassis" and eyes["material"] == "pla" and eyes["color"] == "#ffffff"
    B = _bodies(p)
    lo, hi = B["eyes"].aabb
    assert abs(hi[1] - 20.0) < 0.05 and abs(lo[1] - 18.35) < 0.05     # flush, 0.8 + 0.25 deep, web 0.6 under
    assert B["eyes"].inside([[12, 19.8, 4]]).any() and B["eyes"].inside([[-12, 19.8, 4]]).any()
    assert not B["chassis"].inside([[12, 19.6, 4]]).any()              # host pocket under the eye
    assert B["chassis"].inside([[0, 19.6, 4]]).any()                   # host face between the eyes stays


def test_text_and_sloped_face(tmp_path):
    wedge = {"type": "place", "shape": {"type": "box", "size": [60, 40, 4]}, "at": [0, 0, 0], "rot": [-20, 0, 0]}
    p = _spec(tmp_path, wedge)
    look_decal.decal(str(p), "chassis", "+z", "text", [8.0], None, text="AB", pid="name")
    B = _bodies(p)
    n = B["name"].mesh
    assert n.volume > 10
    assert B["chassis"].mesh.volume + n.volume == pytest.approx(60 * 40 * 4 + 0.25 * n.volume / 1.05, rel=0.05)


def test_refuses_off_the_part(tmp_path):
    p = _spec(tmp_path)
    with pytest.raises(SystemExit):
        look_decal.decal(str(p), "chassis", "+y", "rect", [80.0, 5.0])


def test_pair_is_one_solid(tmp_path):
    p = _spec(tmp_path)
    look_decal.decal(str(p), "chassis", "+y", "circle", [8.0], "0,4", 24.0, pid="eyes")
    B = _bodies(p)
    assert B["eyes"].mesh.body_count == 1


def test_iris_over_eye_replaces_it(tmp_path):
    p = _spec(tmp_path)
    look_decal.decal(str(p), "chassis", "+y", "circle", [16.0], "0,0", color="#111111", pid="eye")
    look_decal.decal(str(p), "chassis", "+y", "circle", [6.0], "0,0", color="#22aa44", pid="iris")
    B = _bodies(p)
    assert B["iris"].inside([[0, 19.8, 0]]).any() and not B["eye"].inside([[0, 19.8, 0]]).any()
    assert B["eye"].inside([[6, 19.8, 0]]).any()
    import numpy as np
    G = np.array([[x, y, z] for x in np.arange(-8, 8, 0.4) for y in np.arange(18.5, 20, 0.2) for z in np.arange(-8, 8, 0.4)])
    assert not (B["eye"].inside(G) & B["iris"].inside(G)).any()      # no overlap between the two graphics
