"""likeness gate: a stock template dropped next to reference photos is blocked."""
import json
from pathlib import Path

import numpy as np
from PIL import Image

from robot import checks, spec as spec_mod, world as world_mod

TPL = Path(__file__).parents[1] / "templates" / "wedge_2wd.json"


def _verify(p):
    r = world_mod.resolve(spec_mod.load(p), fast=True)
    return checks.verify_resolved(r, checks.Options(fast=True, only=["likeness"]))


def test_template_copy_blocked(tmp_path):
    d = tmp_path / "robots" / "x"
    (d / "reference").mkdir(parents=True)
    img = np.full((120, 160, 3), 255, np.uint8)
    img[40:90, 30:130] = 20
    Image.fromarray(img).save(d / "reference" / "p.png")
    (d / "REFERENCE.json").write_text(json.dumps({"robot_type": "vertical_spinner", "wheels": 2}))
    (d / "spec.json").write_text(TPL.read_text())
    ids = {f.id for f in _verify(d / "spec.json").findings if not f.passed}
    assert {"likeness.template_copy", "likeness.type", "likeness.no_reference"} <= ids


def test_inactive_without_photos(tmp_path):
    p = tmp_path / "spec.json"
    p.write_text(TPL.read_text())
    assert not [f for f in _verify(p).findings if f.group == "likeness"]


def test_weapon_facts(tmp_path):
    d = tmp_path / "robots" / "y"
    (d / "reference").mkdir(parents=True)
    (d / "spec.json").write_text((TPL.parent / "vspin_drisk.json").read_text())
    (d / "REFERENCE.json").write_text(json.dumps({"robot_type": "vertical_spinner", "wheels": 2,
                                                  "weapon": {"kind": "drum", "axis": "z", "position": "rear"}}))
    msgs = [f.message for f in _verify(d / "spec.json").findings if f.id == "likeness.weapon" and not f.passed]
    assert len(msgs) == 3
    (d / "REFERENCE.json").write_text(json.dumps({"robot_type": "vertical_spinner", "wheels": 2,
                                                  "weapon": {"kind": "disc", "axis": "x", "position": "front", "teeth": 2}}))
    assert not [f for f in _verify(d / "spec.json").findings if f.id == "likeness.weapon" and not f.passed]


def test_textured_mask(tmp_path):
    import numpy as np
    from PIL import Image
    from robot.mask import photo_mask
    rng = np.random.default_rng(0)
    H, W = 300, 400
    x = np.mgrid[:H, :W][1]
    a = np.stack([160 + 40 * np.sin(x / 6.0) + rng.normal(0, 15, (H, W))] * 3, -1) * [1, 0.75, 0.5]
    a[100:200, 140:260] = [30, 30, 35]
    a[0:40, 0:60] = [60, 40, 20]  # dark knot in the wood
    p = tmp_path / "wood.png"
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(p)
    gt = np.zeros((H, W), bool)
    gt[100:200, 140:260] = True
    f = photo_mask(p, mode="textured")
    assert (f & gt).sum() / (f | gt).sum() > 0.75
