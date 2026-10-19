import numpy as np

from robot import render
from robot.world import Body, World

SPEC = {
    "parts": [
        {"id": "tub"}, {"id": "top_panel"}, {"id": "hatch", "tags": ["cover"]}, {"id": "bat_lid"},
        {"id": "esc_cap", "role": "lid"}, {"id": "base_panel"}, {"id": "side_l", "name": "Side armor"},
    ],
    "fasteners": [
        {"id": "bolt_t0", "through": ["top_panel"], "threads_into": "insert_t0"},
        {"id": "bolt_h0", "through": ["tub"], "threads_into": "hatch"},
        {"id": "bolt_b0", "through": ["base_panel", "tub"], "threads_into": "insert_b0"},
    ],
}


def test_lid_ids_cover_every_lid_part_and_its_bolts():
    assert render.lid_ids(SPEC) == {"top_panel", "hatch", "bat_lid", "esc_cap", "bolt_t0", "bolt_h0"}


def test_nolid_world_leaves_out_every_lid_or_cover():
    ids = [p["id"] for p in SPEC["parts"]] + [f["id"] for f in SPEC["fasteners"]]
    w = World([Body(i, "structure", None, np.eye(4), None, n, False) for n, i in enumerate(ids)], {})
    kept = {b.id for b in render.without_lid(w, SPEC).bodies}
    assert kept == {"tub", "base_panel", "side_l", "bolt_b0"}
    tagged = {p["id"] for p in SPEC["parts"] if any(k in str(p.get(f, "")).lower() for f in ("id", "role", "tags") for k in ("lid", "cover"))}
    assert tagged and not tagged & kept


def test_revron_spec_nolid_drops_top_panel_and_bolts():
    import json
    from pathlib import Path

    p = Path(__file__).resolve().parents[2] / "robots/revron/spec.json"
    if not p.exists():
        return
    d = render.lid_ids(json.loads(p.read_text()))
    assert "top_panel" in d and {"bolt_t0", "bolt_t1", "bolt_t2", "bolt_t3"} <= d
