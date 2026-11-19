"""`robot brackets` / `robot electronics`: planning on small fake worlds (no CAD)."""

import numpy as np
import trimesh

from robot import look_brackets, look_electronics


class FB:
    def __init__(self, id, mesh, fastener=False):
        self.id, self.mesh, self.fastener = id, mesh, fastener

    @property
    def aabb(self):
        return self.mesh.bounds

    @property
    def center(self):
        return self.aabb.mean(axis=0)

    @property
    def is_wire(self):
        return self.id.startswith("wire:")

    def inside(self, P):
        return self.mesh.contains(np.atleast_2d(P))


class W:
    def __init__(self, bodies):
        self.bodies = bodies


def _cyl_x(r, h, x):
    m = trimesh.creation.cylinder(radius=r, height=h, sections=64)
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    m.apply_translation((x, 0, 0))
    return m


def _wheel_world(stub_len=1.6):
    chassis = FB("chassis", trimesh.creation.box(extents=(60, 40, 20)))
    chassis.mesh.apply_translation((-40, 0, 0))
    tyre = _cyl_x(10, 8, 0)  # solid is fine: only the cap's room outside x = 4 is probed
    hub = trimesh.util.concatenate([_cyl_x(5.2, 9.2, 0.6), _cyl_x(2.6, stub_len, 5.2 + stub_len / 2)])
    raw = {"parts": [{"id": "chassis", "kind": "structure", "shape": {}},
                     {"id": "wheel", "kind": "wheel", "tyre_of": "hub", "shape": {}},
                     {"id": "hub", "kind": "other", "shape": {"type": "box", "size": [1, 1, 1]}, "at": [0, 0, 0]}]}
    return raw, W([chassis, FB("wheel", tyre), FB("hub", hub)])


def test_brackets_cap_on_the_outer_side_within_the_stub():
    raw, w = _wheel_world()
    todo, notes = look_brackets.plan(raw, w)
    assert len(todo) == 1, notes
    wid, hid, ring, pockets, info = todo[0]
    assert (wid, hid) == ("wheel", "hub") and len(pockets) == 5
    assert ring["rot"] == [0, 90, 0]
    x = ring["at"][0]
    h = ring["shape"]["base"]["height"]
    assert x > 0  # chassis is at -x, so the outer side is +x
    assert x + h / 2 <= 5.2 + 1.6 + 1e-6  # never past the axle stub: outline unchanged
    assert ring["shape"]["cut"][0]["radius"] > 2.6  # clears the stub
    assert ring["shape"]["base"]["radius"] < 5.2  # inside the hub rim, off the tyre


def test_brackets_refuses_without_room():
    raw, w = _wheel_world(stub_len=0.5)
    todo, notes = look_brackets.plan(raw, w)
    assert not todo and "no room" in notes[0]


def _box(ext, at):
    m = trimesh.creation.box(extents=ext)
    m.apply_translation(at)
    return m


def test_electronics_covers_and_window():
    tub = trimesh.util.concatenate([_box((60, 40, 2), (0, 0, 0)), _box((60, 40, 2), (0, 0, 16))])
    raw = {"parts": [{"id": "chassis", "kind": "structure", "shape": {"type": "box", "size": [60, 40, 18]}, "at": [0, 0, 8]},
                     {"id": "bat", "kind": "battery", "catalog": "lipo"}]}
    Bd = {"chassis": FB("chassis", tub), "bat": FB("bat", _box((30, 20, 8), (0, 0, 6)))}
    out, bad = look_electronics.covers(Bd, raw, "bat")
    assert out == ["chassis"] and not bad
    area, why = look_electronics.window_through(raw, Bd, "bat", out, lip=2.0)
    assert why is None and abs(area - 26 * 16) < 1e-6
    cut = raw["parts"][0]["shape"]["cut"][0]
    assert cut["type"] == "place" and cut["shape"]["size"][:2] == [26.0, 16.0]


def test_electronics_refuses_when_a_screw_is_in_the_way():
    tub = _box((60, 40, 2), (0, 0, 16))
    raw = {"parts": [{"id": "chassis", "kind": "structure", "shape": {"type": "box", "size": [60, 40, 2]}, "at": [0, 0, 16]},
                     {"id": "bat", "kind": "battery", "catalog": "lipo"}]}
    Bd = {"chassis": FB("chassis", tub), "bat": FB("bat", _box((30, 20, 8), (0, 0, 6))),
          "s1": FB("s1", _box((2, 2, 6), (0, 0, 15)), fastener=True)}
    out, _ = look_electronics.covers(Bd, raw, "bat")
    area, why = look_electronics.window_through(raw, Bd, "bat", out)
    assert area == 0 and "s1" in why
