"""reference_cad: per-part dims/volume/holes/placement vs a reference mesh, and import/copy detection."""

from pathlib import Path

from robot import spec as spec_mod, world as world_mod
from robot.checks import Ctx, Options, reference_cad as RC

ROOT = Path(__file__).resolve().parents[2]


def _plate(hole_r=10.0, size=(40, 30, 3)):
    return {"id": "plate", "kind": "structure", "material": "PLA", "shape": {"type": "subtract",
            "base": {"type": "box", "size": list(size)},
            "cut": [{"type": "place", "shape": {"type": "cylinder", "radius": 1.6, "height": 10}, "at": [x, 0, 0]}
                    for x in (-hole_r, hole_r)]}}


def _ctx(parts, cad):
    r = world_mod.resolve(spec_mod.Spec({"name": "t", "parts": parts, "reference_cad": cad}, ROOT), fast=True)
    return Ctx(r, world_mod.World.start(r), Options())


def _ref_stl(tmp_path, part):
    ctx = _ctx([part], {})
    p = tmp_path / "ref.stl"
    ctx.world.body(part["id"]).mesh.export(p)
    return p


def test_exact_copy_is_blocked(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    fs = RC.run(_ctx([_plate()], {"dir": str(tmp_path), "parts": [{"part": "plate", "file": p.name}]}))
    f = [f for f in fs if f.id == "reference_cad.copied"]
    assert f and not f[0].passed and f[0].severity == "blocker"


def test_parametric_match_passes_and_is_not_a_copy(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    moved = dict(_plate(), at=[5, 7, 2], rot=[0, 0, 90])  # the same mesh moved and turned
    fs = RC.run(_ctx([_plate(size=(40.2, 30.1, 3))], {"dir": str(tmp_path), "parts": [{"part": "plate", "file": p.name}]}))
    ids = {(f.id, f.passed) for f in fs}
    assert ("reference_cad.copied", False) not in ids
    assert ("reference_cad.dims", True) in ids and ("reference_cad.volume", True) in ids and ("reference_cad.holes", True) in ids
    fs = RC.run(_ctx([moved], {"dir": str(tmp_path), "parts": [{"part": "plate", "file": p.name}]}))
    assert any(f.id == "reference_cad.copied" for f in fs)  # pose does not hide a copy


def test_wrong_holes_and_size_fail(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    fs = RC.run(_ctx([_plate(hole_r=6.0, size=(46, 30, 2))], {"dir": str(tmp_path), "parts": [
        {"part": "plate", "file": p.name, "at": [0, 20, 0], "at_tol": 1.0}]}))
    bad = {f.id for f in fs if not f.passed}
    assert {"reference_cad.dims", "reference_cad.holes", "reference_cad.placement"} <= bad


def test_missing_file_or_part_is_not_checked(tmp_path):
    ctx = _ctx([_plate()], {"dir": str(tmp_path), "parts": [{"part": "plate", "file": "nope.stl"},
                                                            {"part": "ghost", "file": "nope.stl"}]})
    fs = RC.run(ctx)
    assert [f.id for f in fs] == ["reference_cad.unusable"] * 2 and len(ctx.not_checked) == 2


def test_plate_hole_fingerprint():
    ctx = _ctx([_plate()], {})
    holes = RC.fingerprint(ctx.world.body("plate").mesh)["holes"]
    assert len(holes) == 2 and all(abs(d - 3.2) < 0.2 and abs(r - 10) < 0.3 for d, r in holes)
