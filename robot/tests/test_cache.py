"""Incremental run cache: cached, uncached, parallel and serial runs must give identical reports."""

import json
from pathlib import Path

import numpy as np
import pytest

from robot import cache, checks, geom, measure, spec as spec_mod, world as world_mod

T = Path(__file__).resolve().parents[1] / "templates"


@pytest.fixture
def tmp_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOT_CACHE", str(tmp_path))
    monkeypatch.setattr(cache, "_db", None)
    monkeypatch.setattr(geom, "_MEM", {})
    cache.set_enabled(True)
    cache.reset_stats()
    yield tmp_path
    cache.set_enabled(True)


def _rep(spec, opts):
    d = checks.verify(spec, opts).to_dict()
    d.pop("timings_s", None)
    return json.dumps(d, sort_keys=True, default=str)


def test_hash_stable_and_sensitive():
    a = np.eye(4)
    assert cache.h("x", a, [1, 2.0]) == cache.h("x", a.copy(), [1, 2.0])
    b = a.copy()
    b[0, 3] = 1e-3
    assert cache.h("x", a) != cache.h("x", b)


def test_geom_key_tracks_shape_and_tess(tmp_cache):
    s1 = {"type": "box", "size": [1, 2, 3]}
    s2 = {"type": "box", "size": [1, 2, 3.1]}
    assert geom.key_for(s1, None) == geom.key_for(dict(s1), None)
    assert geom.key_for(s1, None) != geom.key_for(s2, None)
    assert geom.key_for(s1, None, geom.FINE) != geom.key_for(s1, None, geom.FAST)


def test_geom_key_tracks_model_source(tmp_path):
    m = tmp_path / "m.py"
    m.write_text("def build():\n    import build123d as b\n    return b.Box(1, 1, 1)\n")
    s = {"type": "model", "file": "m.py", "params": {}}
    k1 = geom.key_for(s, tmp_path)
    m.write_text("def build():\n    import build123d as b\n    return b.Box(1, 1, 2)\n")
    assert geom.key_for(s, tmp_path) != k1


def test_pairwise_memo_hits_only_for_unchanged_pair(tmp_cache):
    ga = geom.geom_for({"type": "box", "size": [10, 10, 10]}, None, geom.FAST)
    gb = geom.geom_for({"type": "box", "size": [6, 6, 6]}, None, geom.FAST)
    A = world_mod.Body("a", "structure", ga, np.eye(4), None)
    B = world_mod.Body("b", "structure", gb, np.eye(4), None)
    o1 = measure.overlap(A, B)
    assert cache.misses["overlap"] == 1
    o2 = measure.overlap(world_mod.Body("a", "structure", ga, np.eye(4), None), B)
    assert cache.hits["overlap"] == 1
    assert o1.volume == pytest.approx(o2.volume) and o1.depth == o2.depth
    measure.overlap(A.moved([1, 0, 0]), B)  # a moved part is a new pair
    assert cache.misses["overlap"] == 2


def test_no_cache_flag_bypasses(tmp_cache):
    cache.set_enabled(False)
    g = {"type": "box", "size": [3, 3, 3]}
    geom.geom_for(g, None, geom.FAST)
    geom.geom_for(g, None, geom.FAST)
    assert cache.hits["part_geom"] == 0


def test_wedge_cached_equals_uncached_and_parallel_equals_serial(tmp_cache, monkeypatch):
    s = spec_mod.load(T / "wedge_2wd.json")
    opts = checks.Options(fast=True, deep=False)
    cache.set_enabled(False)
    monkeypatch.setattr(world_mod, "JOBS", 1)
    base = _rep(s, opts)
    cache.set_enabled(True)
    monkeypatch.setattr(world_mod, "JOBS", 4)
    cold = _rep(s, opts)  # parallel part builds, all misses
    warm = _rep(s, opts)  # every group a hit
    assert cache.hits["group"] > 0
    import difflib
    diff = "\n".join(list(difflib.unified_diff(base.split(", "), warm.split(", "), lineterm=""))[:40])
    assert base == cold, "cold"
    assert base == warm, diff


def test_one_part_change_reuses_other_queries(tmp_cache):
    s = spec_mod.load(T / "wedge_2wd.json")
    opts = checks.Options(fast=True, deep=False)
    _rep(s, opts)
    d = json.loads(json.dumps(s.raw))
    p = next(p for p in d["parts"] if p.get("shape"))
    p["shape"] = {"type": "place", "shape": p["shape"], "at": [0, 0, 0.01], "rot": [0, 0, 0]}
    s2 = spec_mod.Spec(d, s.base_dir)
    cache.reset_stats()
    cached = _rep(s2, opts)
    assert cache.misses["group"] > 0 and cache.hits["overlap"] > 0
    cache.set_enabled(False)
    assert cached == _rep(s2, opts)
