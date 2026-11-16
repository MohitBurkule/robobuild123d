"""Gallery page (E6, robot/gallery.py): cards, degradation, self-contained html."""

import base64
import json

from robot.gallery import build_gallery, card, robots_in

PNG_1PX = base64.b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")


def _robot(root, slug, spec=None, report=None, iso=True):
    d = root / slug
    (d / "renders").mkdir(parents=True)
    (d / "spec.json").write_text(json.dumps(spec if spec is not None else {"name": slug.title(), "robot_type": "wedge"}))
    if report is not None:
        (d / "report.json").write_text(json.dumps(report))
    if iso:
        (d / "renders" / "iso.png").write_bytes(PNG_1PX)
    return d


def test_card_reads_spec_report_and_iso(tmp_path):
    d = _robot(tmp_path, "alpha", report={"ok": True, "profile": "aws2025", "summary": {"blockers": 0, "warnings": 2},
                                          "metrics": {"mass_total_g": 141.5, "mass_limit_g": 150}})
    c = card(d)
    assert c["name"] == "Alpha" and c["ok"] is True and c["mass"] == 141.5
    assert c["png"] == d / "renders" / "iso.png"


def test_dir_without_spec_is_skipped(tmp_path):
    _robot(tmp_path, "alpha")
    (tmp_path / "not_a_robot").mkdir()
    assert [c["slug"] for c in robots_in(tmp_path)] == ["alpha"]


def test_missing_report_and_render_degrade(tmp_path):
    d = _robot(tmp_path, "beta", report=None, iso=False)
    c = card(d)
    assert c["ok"] is None and c["png"] is None and c["slug"] == "beta"


def test_build_gallery_embeds_png_and_verdicts(tmp_path):
    _robot(tmp_path, "ok_bot", report={"ok": True, "summary": {"blockers": 0, "warnings": 1},
                                       "metrics": {"mass_total_g": 100.0, "mass_limit_g": 150}})
    _robot(tmp_path, "fail_bot", report={"ok": False, "summary": {"blockers": 3, "warnings": 4},
                                         "metrics": {"mass_total_g": 160.0, "mass_limit_g": 150}})
    h = build_gallery(tmp_path)
    assert "2 robots" in h and "PASS" in h and "FAIL" in h
    assert "3 blockers" in h and "160.0 g" in h
    assert f"data:image/png;base64,{base64.b64encode(PNG_1PX).decode()}" in h
    assert "not verified" not in h


def test_unverified_robot_card(tmp_path):
    _robot(tmp_path, "mystery", report=None)
    h = build_gallery(tmp_path)
    assert "not verified" in h and "mystery" in h


def test_empty_and_missing_root(tmp_path):
    assert build_gallery(tmp_path).startswith("<!doctype html>")
    assert robots_in(tmp_path / "nope") == []
