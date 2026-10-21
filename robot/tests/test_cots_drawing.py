"""cots.drawing_dims: the datasheet GR1507 is measured from its built solids against the GEPRC drawing."""

import numpy as np
import trimesh

from robot import spec
from robot.checks import Options, verify
from robot.checks import cots_fidelity as cf

X = np.array([1.0, 0.0, 0.0])


def _x(m):
    m.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))
    return m


def _motor(threaded=True, stack=7.0):
    can = _x(trimesh.creation.annulus(7.4, 9.8, 9.7))
    can.apply_translation([0.35, 0, 0])
    stator = _x(trimesh.creation.cylinder(7.5, stack))
    stator.apply_translation([-1.0, 0, 0])
    base = _x(trimesh.creation.annulus(1.0, 9.0, 2.0))
    holes = [_x(trimesh.creation.cylinder(1.0, 4.0)) for _ in range(4)]
    for h, (y, z) in zip(holes, ((6, 0), (-6, 0), (0, 6), (0, -6))):
        h.apply_translation([-10.4, y, z])
    base.apply_translation([-10.4, 0, 0])
    base = base.difference(trimesh.util.concatenate(holes)) if trimesh.boolean.engines_available else base
    stator = trimesh.util.concatenate([stator, base])
    plain = _x(trimesh.creation.cylinder(2.5, 4.0))
    plain.apply_translation([7.2, 0, 0])
    tip = []
    for k in range(20):   # thread proxy: 8 mm of 0.4 mm alternating crest/root rings
        ring = _x(trimesh.creation.cylinder(2.5 if k % 2 == 0 or not threaded else 2.1, 0.4))
        ring.apply_translation([9.4 + 0.4 * k, 0, 0])
        tip.append(ring)
    shaft = trimesh.util.concatenate([plain] + tip)
    return can, stator, shaft


def test_drawing_dims_measures_solids():
    can, stator, shaft = _motor()
    got = cf.drawing_dims(can, stator, [shaft], X, 15.5)
    assert abs(got["can_d"] - 19.6) < 0.1
    assert abs(got["total_len"] - 28.6) < 0.1
    assert abs(got["shaft_protrusion"] - 12.0) < 0.3
    assert got["thread_len"] > 6.0
    assert abs(got["stator_d"] - 15.0) < 0.3
    assert abs(got["stator_stack"] - 7.0) < 0.3


def test_plain_rod_and_short_stack_are_misses():
    can, stator, shaft = _motor(threaded=False, stack=5.0)
    _, miss = cf.drawing_misses(cf.drawing_dims(can, stator, [shaft], X, 15.5))
    names = " ".join(miss)
    assert "thread_len" in names and "stator_stack" in names
    _, miss = cf.drawing_misses(cf.drawing_dims(can, stator, [], X, 15.5))
    assert any(m.startswith("total_len") for m in miss) and any(m.startswith("shaft_protrusion") for m in miss)


def _run(stator, can):
    d = {"name": "g", "parts": [{"id": "weapon_motor_stator", "kind": "weapon_motor", "catalog": stator},
                               {"id": "weapon_motor_can", "kind": "other", "catalog": can}]}
    return verify(spec.Spec(d, None), Options(only=["cots_fidelity"], deep=False, fast=True))


def test_datasheet_variant_is_blocker_step_variant_skipped():
    rep = _run("gr1507", "gr1507_can")
    assert rep.failed("cots.drawing_dims")   # no shaft, stator d14 in the catalog solid
    rep = _run("gr1507_step", "gr1507_step_can")
    assert not any(f.id == "cots.drawing_dims" for f in rep.findings)
