"""Silhouette-vs-photo check (robot/checks/reference.py)."""

from pathlib import Path

import numpy as np

from robot import spec as spec_mod, world as world_mod
from robot.checks import Ctx, Options, reference as R

ROOT = Path(__file__).resolve().parents[2]
SIDE = ROOT / "robots/revron/reference/side_mask.png"


def test_mask_vs_itself_is_perfect():
    m = R.load_mask(SIDE)
    stats, a, b = R.compare(m, m)
    assert stats["iou"] > 0.99 and min(stats["regions"].values()) > 0.99 and stats["hausdorff_frac"] < 0.01
    assert R.overlay_png(a, b)[:4] == b"\x89PNG"


def test_scale_and_offset_do_not_matter():
    m = R.load_mask(SIDE)
    big = np.kron(m, np.ones((2, 2), bool))
    big = np.pad(big, ((30, 5), (40, 10)))
    assert R.compare(big, m)[0]["iou"] > 0.97


def _box_spec():
    return spec_mod.Spec({"name": "box", "parts": [
        {"id": "body", "kind": "chassis", "shape": {"type": "box", "size": [80, 140, 60]}, "material": "PLA"}],
        "reference": [{"view": "side", "mask": str(SIDE)}]}, ROOT)


def test_box_robot_fails():
    sp = _box_spec()
    r = world_mod.resolve(sp, fast=True)
    ctx = Ctx(r, world_mod.World.start(r), Options())
    fs = R.run(ctx)
    f = [f for f in fs if f.id == "reference.silhouette"][0]
    assert not f.passed and f.severity == "blocker", f.message
    assert ctx.metrics["reference"]["side"]["iou"] < 0.80
    assert Path(ctx.metrics["reference"]["side"]["overlay"]).exists()


def test_missing_mask_fails_closed():
    sp = _box_spec()
    sp.raw["reference"] = [{"view": "side", "mask": "nope.png"}]
    r = world_mod.resolve(sp, fast=True)
    ctx = Ctx(r, world_mod.World.start(r), Options())
    fs = R.run(ctx)
    assert fs[0].id == "reference.unusable" and not fs[0].passed and ctx.not_checked


def test_no_reference_no_findings():
    sp = _box_spec()
    sp.raw.pop("reference")
    r = world_mod.resolve(sp, fast=True)
    assert R.run(Ctx(r, world_mod.World.start(r), Options())) == []


def _ctx(sp):
    r = world_mod.resolve(sp, fast=True)
    return Ctx(r, world_mod.World.start(r), Options())


def test_feature_presence_and_organic_box():
    sp = _box_spec()
    sp.raw.pop("reference")
    sp.raw["parts"][0]["organic"] = True
    sp = spec_mod.Spec(dict(sp.raw, reference_features={"body": "body", "fork": ["fork_l"]}), ROOT)
    fs = {(f.id, f.passed) for f in R.run(_ctx(sp))}
    assert ("shape.feature_presence", True) in fs and ("shape.feature_presence", False) in fs
    assert ("shape.curvature", False) in fs
