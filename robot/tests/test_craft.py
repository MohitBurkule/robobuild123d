"""craft: designer red flags made measurable."""
import numpy as np
import trimesh

from robot.checks import craft


class Geo:
    def __init__(self, m):
        self.volume = float(m.volume)


class B:
    def __init__(self, id, kind, center, size):
        self.id, self.kind, self.is_wire, self.fastener = id, kind, False, False
        self.mesh = trimesh.creation.box(extents=size)
        self.mesh.apply_translation(center)
        self.geom = Geo(self.mesh)
        self.aabb = self.mesh.bounds
        self.center = np.array(center, float)


class Ctx:
    def __init__(self, bodies):
        self.world = type("W", (), {"bodies": bodies})()
        self.metrics, self.not_checked = {}, []


def test_pole_below_floor_is_stray():
    tub = B("tub", "structure", (0, 0, 10), (100, 100, 16))
    pin = B("front_pin", "other", (0, 0, -40), (3, 3, 85))
    out = craft.stray(Ctx([tub, pin]), 2.0)
    assert [f.id for f in out] == ["craft.stray_part"] and "front_pin" in out[0].message


def test_solid_box_is_brick():
    tub = B("tub", "structure", (0, 0, 10), (80, 80, 20))
    out = craft.brick(Ctx([tub]))
    assert out and out[0].id == "craft.brick"


def test_box_body_has_sharp_silhouette():
    tub = B("tub", "structure", (0, 0, 10), (80, 80, 20))
    out = craft.sharp_edges(Ctx([tub]))
    assert out and out[0].id == "craft.sharp_edges"
