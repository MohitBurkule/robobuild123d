"""Unit tests for the dump-vs-model diagnosis (pure parts: classification and rendering)."""
import numpy as np

from robot.cad import dump_misses as dm
from robot.cad import dump_misses_md as md


def _f(t, name="F", dims=None):
    return {"name": name, "type": t, "dims": dims or {}, "parents": []}


def test_present_when_all_samples_match():
    fc = {"type": "cyl", "r": 0.001}
    st, cat, _ = dm.classify(_f("Fillet"), [fc], [np.zeros(5)], [np.full(5, 0.01)], 1.0)
    assert st == "present" and cat is None


def test_sharp_edge_reads_as_fillet_skipped():
    fc = {"type": "cyl", "r": 0.002}
    st, cat, _ = dm.classify(_f("Fillet"), [fc], [np.zeros(5)], [np.full(5, dm.SHARP * 2.0)], 2.0)
    assert (st, cat) == ("missing", "fillet skipped")


def test_small_offset_is_wrong_radius():
    st, cat, _ = dm.classify(_f("Fillet"), [{"type": "cyl"}], [np.zeros(4)], [np.full(4, 0.1)], 1.0)
    assert (st, cat) == ("wrong", "fillet wrong radius")


def test_unshown_faces_are_not_compared():
    st, cat, _ = dm.classify(_f("ICE"), [{"type": "plane"}], [np.full(3, 2.0)], [np.zeros(3)])
    assert st == "not shown"


def test_far_extrude_is_missing():
    st, cat, _ = dm.classify(_f("Extrusion"), [{"type": "plane", "n": np.array([0, 0, 1.0])}], [np.zeros(3)], [np.full(3, 3.0)])
    assert (st, cat) == ("missing", "feature missing")


def test_render_groups_fixes_and_counts_blind_spots():
    r = {"part": "p", "dump": "d", "stl": "s.stl", "reg_gap_mm": 0.0, "tol_mm": 1.0, "vol_ours": 99.0, "vol_ref": 100.0, "extra": [],
         "rows": [{"feature": "Fillet1", "type": "Fillet", "dims": {"D1": 1.0}, "status": "wrong", "category": "fillet wrong radius",
                   "numbers": "x", "at": [0, 0, 0], "caught": [], "waiver": None, "fix": None}]}
    out = md.render([r], {})
    assert "| fillet wrong radius | 1 | 0 | 0 | 1 |" in out
    assert "### tool" in out and "NOTHING" in out
