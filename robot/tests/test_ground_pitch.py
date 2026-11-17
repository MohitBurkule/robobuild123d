"""ground.pitch_rest: a 2-wheel robot pitched toward its centre of mass must land on a skid, not the weapon."""
import numpy as np
import trimesh

from robot.checks import ground


class B:
    def __init__(self, id, kind, center, size):
        self.id, self.kind, self.is_wire = id, kind, False
        self.mesh = trimesh.creation.box(extents=size)
        self.mesh.apply_translation(center)


class W:
    def __init__(self, bodies):
        self.bodies = bodies


class Ctx:
    def __init__(self, bodies):
        self.world, self.metrics = W(bodies), {}


LOWS = [(None, np.array([-30.0, -40.0, 0.0])), (None, np.array([30.0, -40.0, 0.0]))]


def test_weapon_first_contact_is_blocker_with_caster_height():
    bar = B("bar", "weapon", (0, 30, 2.0), (116, 10, 3))
    tub = B("tub", "structure", (0, 0, 10), (100, 100, 10))
    out = ground.pitch_rest(Ctx([bar, tub]), LOWS, 0.0, (0.0, 0.0))
    assert out[0].id == "ground.pitch_rest" and out[0].severity == "blocker"
    assert "bar" in out[0].message and "caster" in out[0].fix_hint


def test_skid_ahead_of_weapon_is_ok():
    bar = B("bar", "weapon", (0, 30, 2.0), (116, 10, 3))
    skid = B("ball", "caster", (0, 10, 0.5), (6, 6, 1))
    out = ground.pitch_rest(Ctx([bar, skid]), LOWS, 0.0, (0.0, 0.0))
    assert out[0].passed and "Rests on a skid" in out[0].title
