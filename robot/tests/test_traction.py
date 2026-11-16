"""Traction patch check (robot/checks/traction.py): COM over the drive contact patch."""

import numpy as np
from types import SimpleNamespace

from robot.checks import traction


def _wheel(bid, x, y, r=10, driven=True, z=0.0, point=False):
    if point:
        v = np.array([[x, y, z]], float)
    else:
        v = np.array([[x - r, y - r, z], [x + r, y - r, z], [x - r, y + r, z], [x + r, y + r, z], [x, y, z + 2 * r]], float)
    return SimpleNamespace(id=bid, kind="wheel", fastener=False, is_wire=False,
                           mesh=SimpleNamespace(vertices=v), part_idx=None,
                           _p=SimpleNamespace(id=bid, kind="wheel", material=None, _extra={} if driven else {"driven": False}))


def _ctx(wheels, com=None):
    metrics = {}
    if com is not None:
        metrics.update({"com_x": com[0], "com_y": com[1], "com_z": 10.0, "ground_z": 0.0})
    bodies = []
    parts = []
    for w in wheels:
        b = SimpleNamespace(id=w.id, kind=w.kind, fastener=False, is_wire=False,
                            mesh=w.mesh, part_idx=len(parts), center=np.zeros(3), aabb=None)
        bodies.append(b)
        parts.append(SimpleNamespace(part=w._p, cat=None, geom=None))
    return SimpleNamespace(r=SimpleNamespace(spec=SimpleNamespace(raw={}, parts=[p.part for p in parts]), parts=parts),
                           world=SimpleNamespace(bodies=bodies), not_checked=[], metrics=metrics)


def test_no_com_is_not_checked():
    ctx = _ctx([_wheel("w1", -30, 0), _wheel("w2", 30, 0)])
    assert traction.run(ctx) == []
    assert any("no centre of mass" in x for x in ctx.not_checked)


def test_no_driven_wheels_touching_is_not_checked():
    ctx = _ctx([_wheel("w1", -30, 0, driven=False), _wheel("w2", 30, 0, driven=False)], com=(0, 0))
    assert traction.run(ctx) == []
    assert any("no driven wheel" in x for x in ctx.not_checked)


def test_com_outside_patch_warns():
    ctx = _ctx([_wheel("w1", -30, 0), _wheel("w2", 30, 0)], com=(0, 60))
    out = traction.run(ctx)
    assert "traction.com_outside_patch" in [f.id for f in out]
    f = next(f for f in out if f.id == "traction.com_outside_patch")
    assert f.severity == "warning" and not f.passed and f.fix_hint
    assert ctx.metrics["com_in_drive_patch"] is False and ctx.metrics["drive_patch_margin_mm"] < 0


def test_com_at_patch_edge_warns():
    ctx = _ctx([_wheel("w1", -30, 0), _wheel("w2", 30, 0), _wheel("w3", 0, 30), _wheel("w4", 0, -30)], com=(0, 36))
    out = traction.run(ctx)
    assert "traction.patch_margin" in [f.id for f in out]
    f = next(f for f in out if f.id == "traction.patch_margin")
    assert f.severity == "warning" and f.fix_hint


def test_com_centred_over_patch_ok():
    ctx = _ctx([_wheel("w1", -30, 0), _wheel("w2", 30, 0), _wheel("w3", 0, 30), _wheel("w4", 0, -30)], com=(0, 0))
    out = traction.run(ctx)
    assert [f.id for f in out] == ["traction.ok"]
    assert ctx.metrics["com_in_drive_patch"] is True and ctx.metrics["drive_patch_margin_mm"] > 0


def test_point_contacts_do_not_form_a_patch():
    ctx = _ctx([_wheel("w1", -30, 0, point=True), _wheel("w2", 30, 0, point=True)], com=(0, 0))
    out = traction.run(ctx)
    assert out == []
    assert any("do not form a patch" in x for x in ctx.not_checked)


def test_two_wheel_axle_patch_centred_ok():
    ctx = _ctx([_wheel("w1", -30, 0), _wheel("w2", 30, 0)], com=(0, 0))
    out = traction.run(ctx)
    assert [f.id for f in out] == ["traction.ok"]
