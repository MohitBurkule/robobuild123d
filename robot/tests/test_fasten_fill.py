"""`robot fasteners --fill` measures grip on the geometry; the shipped template already carries those records."""
import json
import subprocess
import sys


def test_template_fasteners_have_holes():
    from robot import cli  # noqa: F401
    from pathlib import Path
    t = json.loads((Path(__file__).parents[1] / "templates" / "wedge_2wd.json").read_text())
    assert all(f.get("hole") for f in t["fasteners"])


def test_fill_measures_grip(tmp_path):
    from pathlib import Path
    t = json.loads((Path(__file__).parents[1] / "templates" / "wedge_2wd.json").read_text())
    for f in t["fasteners"]:
        f.pop("hole", None)
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(t))
    from robot import fasten_fill
    assert fasten_fill.main(str(p), fill=True) == 0
    got = {f["id"]: f["hole"]["grip"] for f in json.loads(p.read_text())["fasteners"]}
    assert 2.0 < got["bolt_wl"] < 3.0      # 2.4 mm wedge lug
    assert 14.0 < got["bolt_fl"] < 16.0    # outer surface (2.2 cbore) down to the insert
