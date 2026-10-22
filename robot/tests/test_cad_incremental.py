"""Incremental verify must give exactly the full verify's report, before and after a part changes."""

import json
from pathlib import Path

import pytest

from robot import cache, checks, geom, spec as spec_mod
from robot.cad import incremental

T = Path(__file__).resolve().parents[1] / "templates"


@pytest.fixture
def tmp_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOT_CACHE", str(tmp_path))
    monkeypatch.setattr(cache, "_db", None)
    monkeypatch.setattr(geom, "_MEM", {})
    # integrity.volume compares with the PREVIOUS run's volumes (a store each run rewrites), so back-to-back runs differ
    # in that message by design; every run here sees "no previous run" so full and incremental stay comparable
    from robot.checks import integrity
    monkeypatch.setattr(integrity, "_load", lambda path: {})
    cache.set_enabled(True)
    cache.reset_stats()
    yield tmp_path
    cache.set_enabled(True)


def _norm(rep):
    d = rep.to_dict()
    d.pop("timings_s", None)
    return json.dumps(d, sort_keys=True, default=str)


def _full(spec, opts):
    cache.set_enabled(False)
    try:
        return checks.verify(spec, opts)
    finally:
        cache.set_enabled(True)


def test_incremental_equals_full_and_reuses(tmp_cache):
    opts = checks.Options(fast=True, deep=False)
    d = json.loads((T / "wedge_2wd.json").read_text())
    s = spec_mod.Spec(d, T)
    full0 = _full(s, opts)
    r0, st0 = incremental.verify_incremental(spec_mod.Spec(d, T), opts)
    assert _norm(r0) == _norm(full0)
    assert not st0["reused"]
    # unchanged -> everything reused, same report
    r1, st1 = incremental.verify_incremental(spec_mod.Spec(d, T), opts)
    assert _norm(r1) == _norm(full0)
    assert not st1["rerun"]
    # move the battery by 3 mm: only groups that read its geometry rerun, report equals a full run
    d2 = json.loads(json.dumps(d))
    bat = next(p for p in d2["parts"] if p["id"] == "battery")
    bat["at"] = [bat["at"][0], bat["at"][1] + 3.0, bat["at"][2]]
    full2 = _full(spec_mod.Spec(d2, T), opts)
    r2, st2 = incremental.verify_incremental(spec_mod.Spec(d2, T), opts)
    assert _norm(r2) == _norm(full2)
    assert st2["rerun"]
    # change metadata (not geometry): base key changes, everything reruns, still equal
    d3 = json.loads(json.dumps(d2))
    d3["parts"][0]["label"] = "renamed"
    r3, st3 = incremental.verify_incremental(spec_mod.Spec(d3, T), opts)
    assert _norm(r3) == _norm(_full(spec_mod.Spec(d3, T), opts))
    assert not st3["reused"]
