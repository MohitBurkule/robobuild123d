"""robot screws: real flush M2 screws on a lid, clamping it to the chassis under it."""
import json

from robot import look_screws


def _spec(tmp_path):
    sp = {"name": "screwtest", "parts": [
        {"id": "chassis", "kind": "structure", "material": "pla", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
         "shape": {"type": "box", "size": [60, 60, 20]}},
        {"id": "lid", "kind": "other", "material": "pla", "process": "fdm", "at": [0, 0, 11.5], "rot": [0, 0, 0],
         "shape": {"type": "box", "size": [60, 60, 3]}}],
          "fasteners": [], "wires": [], "connections": []}
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(sp))
    return p


def test_corners_clamp_lid(tmp_path):
    p = _spec(tmp_path)
    look_screws.main(str(p), "lid", "+z", "corners", 4, 6.0)
    d = json.loads(p.read_text())
    fs = d["fasteners"]
    assert len(fs) == 4
    for f in fs:
        assert f["through"] == ["lid"] and f["threads_into"] == "chassis"
        assert f["dir"] == [0, 0, -1] and abs(f["at"][2] - (13.0 - look_screws.HEAD_K)) < 0.2   # head flush with the top
        assert f.get("hole")
    lid = next(x for x in d["parts"] if x["id"] == "lid")
    assert lid["shape"]["type"] == "subtract" and len(lid["shape"]["cut"]) == 8      # counterbore + clearance hole each


def test_dry_changes_nothing(tmp_path):
    p = _spec(tmp_path)
    before = p.read_text()
    look_screws.main(str(p), "lid", "+z", "row", 3, 6.0, dry=True)
    assert p.read_text() == before
