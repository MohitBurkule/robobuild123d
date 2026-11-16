"""Service check (robot/checks/service.py): straight-line extraction of battery / weapon / wheels."""

import numpy as np
import trimesh
from types import SimpleNamespace

from robot.checks import service


def _body(kind, bid, part_idx, mesh=None, key=None):
    import uuid
    mesh = mesh if mesh is not None else trimesh.creation.box(extents=(4.0, 4.0, 4.0))
    mesh = mesh.apply_translation([0.0, 0.0, 10.0])
    lo, hi = mesh.bounds
    # unique geom key per mesh: the ray-cast memo is keyed by it, and two tests must never share one
    key = key or f"{bid}-{uuid.uuid4().hex[:8]}"
    return SimpleNamespace(id=bid, kind=kind, fastener=False, is_wire=False, part_idx=part_idx,
                           mesh=mesh, aabb=np.array([lo, hi]), geom=SimpleNamespace(key=key),
                           M=np.eye(4), center=(lo + hi) / 2,
                           surface=lambda h: (np.asarray(mesh.vertices, float),),
                           inside=lambda P: np.zeros(np.atleast_2d(P).shape[0], bool))


def _ctx(bodies, parts):
    r = SimpleNamespace(parts=parts, profile=SimpleNamespace(min_ground_clearance_mm=1.0),
                        spec=SimpleNamespace(ground_z=0.0, raw={}))
    return SimpleNamespace(r=r, world=SimpleNamespace(bodies=bodies), metrics={}, not_checked=[])


def _resolved(kind, pid):
    return SimpleNamespace(part=SimpleNamespace(id=pid, kind=kind, _extra={}), cat=None)


def test_no_service_parts_is_not_checked():
    ctx = _ctx([_body("chassis", "chassis1", 0)], [_resolved("chassis", "chassis1")])
    assert service.run(ctx) == []
    assert any("no battery, weapon or wheel parts" in x for x in ctx.not_checked)


def test_lone_battery_pulls_out():
    b = _body("battery", "bat1", 0)
    ctx = _ctx([b], [_resolved("battery", "bat1")])
    ids = [f.id for f in service.run(ctx)]
    assert ids == ["service.ok"]
    assert ctx.metrics["service.extract.bat1"] == [1.0, 0.0, 0.0]


def test_enclosed_battery_has_no_straight_path():
    # a closed box around the battery blocks every axis and diagonal direction
    bat = _body("battery", "bat1", 0, mesh=trimesh.creation.box(extents=(4.0, 4.0, 4.0)))
    shell = _body("chassis", "shell1", 1, mesh=trimesh.creation.box(extents=(10.0, 10.0, 10.0)))
    ctx = _ctx([bat, shell], [_resolved("battery", "bat1"), _resolved("chassis", "shell1")])
    out = service.run(ctx)
    f = next(x for x in out if x.id == "service.battery_pull")
    assert not f.passed and f.severity == "warning" and f.fix_hint
    assert f.parts == ["bat1"]
    assert "service.ok" not in [x.id for x in out]


def test_box_with_open_top_lets_the_battery_out():
    # five walls: the +Z direction is clear, so the battery lifts straight out
    bat = _body("battery", "bat1", 0, mesh=trimesh.creation.box(extents=(4.0, 4.0, 4.0)))
    boxes = []
    for ext, tr in (((10.0, 10.0, 1.0), (0, 0, -5.0)), ((10.0, 1.0, 10.0), (0, 4.5, 0)),
                    ((10.0, 1.0, 10.0), (0, -4.5, 0)), ((1.0, 10.0, 10.0), (4.5, 0, 0)),
                    ((1.0, 10.0, 10.0), (-4.5, 0, 0))):
        p = trimesh.creation.box(extents=ext)
        boxes.append(p.apply_translation(list(tr)))
    walls = trimesh.util.concatenate(boxes)
    shell = _body("chassis", "shell1", 1, mesh=walls)
    ctx = _ctx([bat, shell], [_resolved("battery", "bat1"), _resolved("chassis", "shell1")])
    ids = [f.id for f in service.run(ctx)]
    assert ids == ["service.ok"]
    assert ctx.metrics["service.extract.bat1"] == [0.0, 0.0, 1.0]


def test_weapon_and_wheel_get_their_own_ids():
    wpn = _body("weapon", "wpn1", 0, mesh=trimesh.creation.box(extents=(4.0, 4.0, 4.0)))
    whl_mesh = trimesh.creation.box(extents=(4.0, 4.0, 4.0)).apply_translation([20.0, 0, 0])
    whl = _body("wheel", "whl1", 1, mesh=whl_mesh)
    ctx = _ctx([wpn, whl], [_resolved("weapon", "wpn1"), _resolved("wheel", "whl1")])
    ids = [f.id for f in service.run(ctx)]
    assert ids == ["service.ok"]
    assert ctx.metrics["service.extract.wpn1"] == [-1.0, 0.0, 0.0]
    assert ctx.metrics["service.extract.whl1"] == [1.0, 0.0, 0.0]


def test_enclosed_weapon_and_wheel_get_their_own_findings():
    wpn = _body("weapon", "wpn1", 0, mesh=trimesh.creation.box(extents=(4.0, 4.0, 4.0)))
    whl = _body("wheel", "whl1", 1, mesh=trimesh.creation.box(extents=(4.0, 4.0, 4.0)).apply_translation([20.0, 0, 0]))
    shell = _body("chassis", "shell1", 2, mesh=trimesh.creation.box(extents=(50.0, 10.0, 10.0)))
    ctx = _ctx([wpn, whl, shell], [_resolved("weapon", "wpn1"), _resolved("wheel", "whl1"),
                                    _resolved("chassis", "shell1")])
    ids = [f.id for f in service.run(ctx)]
    assert "service.weapon_pull" in ids
    assert "service.wheel_pull" in ids
    assert "service.ok" not in ids
    for f in service.run(ctx):
        assert f.fix_hint
