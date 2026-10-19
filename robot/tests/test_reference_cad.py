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


def _frame_cfg(tmp_path, p, **k):
    return {"dir": str(tmp_path), "ref_to_world": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
            "parts": [dict({"part": "plate", "file": p.name}, **k)]}


def test_silhouette_passes_for_the_same_shape_in_place(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    fs = RC.run(_ctx([_plate(size=(40.2, 30.1, 3))], _frame_cfg(tmp_path, p)))
    f = [f for f in fs if f.id == "reference_cad.silhouette"]
    assert f and f[0].passed


def test_silhouette_fails_on_a_shape_difference_with_matching_size(tmp_path):
    """Same bounding box and volume class, different outline: an L-plate against a rectangle fails the IoU."""
    p = _ref_stl(tmp_path, _plate())
    lplate = {"id": "plate", "kind": "structure", "material": "PLA", "shape": {"type": "subtract",
              "base": {"type": "box", "size": [40, 30, 3]},
              "cut": [{"type": "place", "shape": {"type": "box", "size": [16, 14, 10]}, "at": [12, 8, 0]}]}}
    fs = RC.run(_ctx([lplate], _frame_cfg(tmp_path, p)))
    f = [f for f in fs if f.id == "reference_cad.silhouette"]
    assert f and not f[0].passed and f[0].severity == "blocker"


def test_silhouette_catches_misplacement_and_mirror(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    moved = dict(_plate(size=(40.2, 30.1, 3)), at=[8, 0, 0])
    fs = RC.run(_ctx([moved], _frame_cfg(tmp_path, p)))
    assert any(f.id == "reference_cad.silhouette" and not f.passed for f in fs)
    # a right-hand copy at -X matches its left-hand reference only when mirrored
    left = dict(_plate(), at=[30, 0, 0])
    pl = _ref_stl(tmp_path, left)
    right = dict(_plate(size=(40.2, 30.1, 3)), at=[-30, 0, 0])
    ok_ = RC.run(_ctx([right], _frame_cfg(tmp_path, pl, mirror_x=True)))
    bad = RC.run(_ctx([right], _frame_cfg(tmp_path, pl)))
    assert any(f.id == "reference_cad.silhouette" and f.passed for f in ok_)
    assert any(f.id == "reference_cad.silhouette" and not f.passed for f in bad)


def test_outline_only_ignores_holes(tmp_path):
    p = _ref_stl(tmp_path, _plate())
    solid = {"id": "plate", "kind": "structure", "material": "PLA", "shape": {"type": "box", "size": [40, 30, 3]}}
    fs = RC.run(_ctx([solid], _frame_cfg(tmp_path, p, outline_only=True, mode="envelope")))
    assert any(f.id == "reference_cad.silhouette" and f.passed for f in fs)


def test_silhouette_iou_values():
    import trimesh
    a = trimesh.creation.box([10, 10, 10])
    b = trimesh.creation.box([10, 10, 10]); b.apply_translation([5, 0, 0])
    iou = RC.silhouette_iou(a, b, 0.1)
    assert abs(iou[0] - 1.0) < 0.03 and abs(iou[1] - 1 / 3) < 0.03 and abs(iou[2] - 1 / 3) < 0.03


def test_with_parts_compares_the_union_clipped_to_the_reference(tmp_path):
    """A bought-in part modelled as two bodies (flange + a long shaft carrying its spigot) is compared as their union
    clipped to the reference span."""
    flange = {"id": "flange", "kind": "other", "material": "aluminium", "shape": {"type": "box", "size": [10, 10, 2]}, "at": [0, 0, 1]}
    whole = {"id": "whole", "kind": "other", "material": "aluminium", "shape": {"type": "union", "items": [
        {"type": "place", "shape": {"type": "box", "size": [10, 10, 2]}, "at": [0, 0, 1]},
        {"type": "place", "shape": {"type": "cylinder", "radius": 1.5, "height": 8.0}, "at": [0, 0, 6]}]}}
    p = _ref_stl(tmp_path, whole)
    shaft = {"id": "shaft", "kind": "shaft", "material": "steel", "shape": {"type": "cylinder", "radius": 1.5, "height": 30.0}, "at": [0, 0, 12]}
    cfg = {"dir": str(tmp_path), "ref_to_world": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
           "parts": [{"part": "flange", "file": p.name, "mode": "envelope", "tol_mm": 0.3}]}
    alone = RC.run(_ctx([flange, shaft], cfg))
    assert any(f.id == "reference_cad.dims" and not f.passed for f in alone)
    cfg["parts"][0].update(with_parts=["shaft"], clip_to_ref=True)
    both = RC.run(_ctx([flange, shaft], cfg))
    assert any(f.id == "reference_cad.dims" and f.passed for f in both)


def test_surface_deviation_clusters_flag_a_bump_and_not_a_match():
    import trimesh

    from robot.checks import ref_diff

    a = trimesh.creation.box((20, 20, 4))
    same = ref_diff.surface_deviation(a, a.copy(), 4000)
    assert ref_diff.deviation_clusters(same, 0.5) == []
    bump = trimesh.util.concatenate([a, trimesh.creation.box((4, 4, 2), transform=trimesh.transformations.translation_matrix((5, 5, 3)))])
    cl = ref_diff.deviation_clusters(ref_diff.surface_deviation(bump, a, 6000), 0.5, min_pts=2)
    assert cl and cl[0]["kind"] == "extra" and cl[0]["max_mm"] > 0.5
    assert abs(cl[0]["centroid"][0] - 5) < 2 and abs(cl[0]["centroid"][1] - 5) < 2


def test_equal_primitive_boxes_are_not_a_copy():
    import trimesh

    from robot.checks.reference_cad import is_copy

    assert is_copy(trimesh.creation.box((23.5, 12, 5)), trimesh.creation.box((23.5, 12, 5)))[0] is False


def test_clean_drops_sliver_shells_and_diff_is_exact():
    import trimesh

    from robot.checks import ref_diff

    box = trimesh.creation.box((10, 10, 4))
    sliver = trimesh.Trimesh(vertices=[[0, 0, 5], [1, 0, 5], [0, 1, 5]], faces=[[0, 1, 2]])
    dirty = trimesh.util.concatenate([box, sliver])
    assert not dirty.is_watertight
    c = ref_diff.clean(dirty)
    assert c.is_watertight and abs(c.volume - box.volume) < 1e-6
    d = ref_diff.boolean_diff(box.copy(), dirty)
    assert d["method"].startswith("brep") and d["extra_mm3"] < 0.01 and d["missing_mm3"] < 0.01
