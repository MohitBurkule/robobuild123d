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
