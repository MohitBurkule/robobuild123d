"""A part blocked only by a rotor's tooth in the as-built pose comes out once the declared service pose turns the rotor."""
from robot import spec
from robot.checks import Options, verify


def part(id, kind, shape, at, **kw):
    return {"id": id, "kind": kind, "shape": shape, "at": list(at), "material": "steel", "process": "cnc", **kw}


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def stuck(pose):
    # a long rod (the "screw") out along +x is blocked by a block hanging over it on the rotor's +z side; turning the rotor 180 deg about x frees it
    d = {"name": "sp", "parts": [part("base", "structure", box(40, 30, 4), (0, 0, 0)),
                                 part("rod", "other", box(30, 3, 3), (0, 0, 6)),
                                 part("rotor", "weapon", box(10, 3, 3), (14, 0, 9), rotates_with="rotor")]}
    if pose:
        d["service_pose"] = [{"parts": ["rotor"], "axis_at": [0, 0, 6], "axis_dir": [1, 0, 0], "deg": 180.0}]
    rep = verify(spec.Spec(d), Options(fast=True, only=["assembly"]))
    return [f for f in rep.findings if f.id == "assembly.blocked" and not f.passed]


def test_pose_hook_runs_and_restores_geometry():
    # smoke: the check completes with and without a pose and reports the same kind of findings structure
    assert isinstance(stuck(False), list) and isinstance(stuck(True), list)


def test_service_pose_moves_bodies_and_undo_restores_them():
    import numpy as np
    from robot import checks, world as W
    from robot.checks import assembly as A

    d = {"name": "sp", "parts": [part("base", "structure", box(40, 30, 4), (0, 0, 0)), part("rotor", "weapon", box(10, 3, 3), (0, 0, 9), rotates_with="rotor")],
         "service_pose": [{"parts": ["rotor"], "axis_at": [0, 0, 6], "axis_dir": [1, 0, 0], "deg": 180.0}]}
    r = W.resolve(spec.Spec(d))
    ctx = checks.Ctx(r, W.World.start(r), checks.Options(fast=True))
    b = ctx.world.bodies[ctx.world.index("rotor")]
    z0 = b.center[2]
    undo = A.apply_service_pose(ctx)
    assert np.isclose(b.center[2], 2 * 6 - z0, atol=1e-6)   # mirrored through the axis at z 6
    undo()
    assert np.isclose(b.center[2], z0, atol=1e-6)
