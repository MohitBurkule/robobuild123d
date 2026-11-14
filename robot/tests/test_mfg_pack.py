"""UNTESTED: written without running. Pure-data tests of robot.mfg on a tiny spec (no B-rep build)."""

import numpy as np

from robot.mfg import assembly_steps, buy_list, cut_list, fastener_counts, mass_budget, print_settings
from robot.mfg.pack import bed_matrix
from robot.spec import Spec

SPEC = {
    "name": "t",
    "parts": [
        {"id": "tub", "kind": "structure", "material": "petg", "process": "fdm", "print_orientation": "-z", "mass_g": 40},
        {"id": "ins1", "kind": "insert", "parent": "tub", "mass_g": 0.3},
        {"id": "lid", "kind": "panel", "material": "titanium", "process": "laser", "thickness_mm": 0.8,
         "parent": "tub", "mass_g": 12},
    ],
    "fasteners": [{"id": "s1", "designation": "M2x6", "through": ["lid"], "threads_into": "ins1"},
                  {"id": "s2", "designation": "M2x6", "through": ["lid"], "threads_into": "tub"}],
}


def test_counts_and_buy():
    s = Spec(SPEC)
    assert fastener_counts(s)["M2x6"] == 2
    assert any(r["name"] == "M2x6" and r["order_qty"] >= 3 for r in buy_list(s))


def test_mass_budget():
    m = mass_budget(Spec(SPEC))
    assert abs(m["total_g"] - 52.3) < 1e-6 and m["ok"] and m["limit_g"] == 150.0


def test_print_and_cut():
    s = Spec(SPEC)
    assert [r["id"] for r in print_settings(s)] == ["tub"]
    assert print_settings(s)[0]["up_axis"] == "-z"
    c = cut_list(s)
    assert c["rows"][0]["id"] == "lid" and c["sheets"][0]["thickness_mm"] == 0.8


def test_steps_order():
    st = assembly_steps(Spec(SPEC))
    first = [s["parts"][0] for s in st if s["parts"]]
    assert first.index("ins1") < first.index("lid")
    closed = {f["id"] for s in st for f in s["fasteners"]}
    assert closed == {"s1", "s2"}


def test_bed_matrix():
    for up in ("+x", "-x", "+y", "-y", "+z", "-z"):
        M = bed_matrix(up)
        a = {"+x": [1, 0, 0], "-x": [-1, 0, 0], "+y": [0, 1, 0], "-y": [0, -1, 0], "+z": [0, 0, 1], "-z": [0, 0, -1]}[up]
        assert np.allclose(M[:3, :3] @ np.array(a, float), [0, 0, 1])
