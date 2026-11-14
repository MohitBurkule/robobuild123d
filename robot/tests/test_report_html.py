"""HTML report + GLB (robot/report_html.py, robot/glb.py)."""

import json

import numpy as np
import trimesh
from types import SimpleNamespace

from robot import report_html


def _rep(ok=True):
    return {"name": "wedge", "ok": ok, "gate": "design", "tier": "full",
            "summary": {"blockers": 1 if not ok else 0, "warnings": 1, "passed": 10},
            "metrics": {"mass_total_g": 149.0, "mass_lo_g": 147.0, "mass_hi_g": 151.0, "mass_limit_g": 150},
            "findings": [{"id": "mass.over", "pass": False, "severity": "blocker", "message": "over 150 g",
                          "parts": ["disc"], "fix": "thin the disc"},
                         {"id": "combat.R2", "pass": False, "severity": "warning", "message": "clearance", "parts": []}],
            "not_checked": ["Thermal: no battery"]}


def test_html_contains_mass_findings_and_not_checked():
    h = report_html.build_html(_rep(ok=False))
    assert "149.0 g" in h and "mass.over" in h and "Not checked" in h
    assert "fix: thin the disc" in h and "FAIL" in h


def test_html_pass_has_no_failing_rows():
    rep = _rep(ok=True)
    rep["findings"] = []
    h = report_html.build_html(rep)
    assert "PASS" in h and "<tr" not in h


def test_html_escapes_html_in_messages():
    rep = _rep(ok=False)
    rep["findings"][0]["message"] = "<script>alert(1)</script>"
    assert "<script>" not in report_html.build_html(rep)


def test_glb_embeds_as_data_uri():
    glb = b"glTF-binary-mock"
    h = report_html.build_html(_rep(), glb=glb)
    assert "model-viewer" in h and "data:model/gltf-binary;base64," in h


def test_glb_from_world_has_one_node_per_body():
    from robot.glb import world_to_glb

    bodies = []
    for i, (cid, color) in enumerate([("a", "#ff0000"), ("b", "not-a-color")]):
        m = trimesh.creation.box((5, 5, 5))
        m.apply_translation([i * 10, 0, 0])
        bodies.append(SimpleNamespace(id=cid, kind="printed", mesh=m, fastener=False,
                                      M=np.eye(4), color=color))
    data = world_to_glb(SimpleNamespace(bodies=bodies))
    assert data[:4] == b"glTF"
    import struct

    length = struct.unpack("<I", data[12:16])[0]
    chunk = json.loads(data[20:20 + length])
    assert len(chunk["nodes"]) == 2 and len(chunk["meshes"]) == 2
