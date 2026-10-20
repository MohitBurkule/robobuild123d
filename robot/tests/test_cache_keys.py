"""Cache keys are content hashes of everything a result depends on, never of the folder it was verified from."""

import json
import shutil
from pathlib import Path

import pytest

from robot import cache, checks, geom, spec as spec_mod

MODEL = '''
from helpers import size
import build123d as b

def build(**p):
    return b.Box(size(), 10, 10)
'''


@pytest.fixture
def tmp_cache(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOT_CACHE", str(tmp_path / "cache"))
    monkeypatch.setattr(cache, "_db", None)
    monkeypatch.setattr(geom, "_MEM", {})
    cache.set_enabled(True)
    cache.reset_stats()
    yield tmp_path
    cache.set_enabled(True)


def _proj(d: Path, w=10) -> Path:
    (d / "src").mkdir(parents=True)
    (d / "src" / "part.py").write_text(MODEL)
    (d / "src" / "helpers.py").write_text(f"def size():\n    return {w}\n")
    return d


def test_helper_change_invalidates_model_key(tmp_path):
    d = _proj(tmp_path / "p")
    shape = {"type": "model", "file": "src/part.py"}
    k1 = geom.key_for(shape, d)
    (d / "src" / "helpers.py").write_text("def size():\n    return 12\n")
    k2 = geom.key_for(shape, d)
    assert k1 != k2
    labels = [lab for lab, _ in cache.model_closure(d / "src" / "part.py")]
    assert "local:helpers.py" in labels


def test_robot_package_helper_is_in_closure():
    f = Path(__file__).resolve().parents[2] / "robots" / "revron" / "src" / "build_revron.py"
    if not f.exists():
        pytest.skip("revron not in this checkout")
    labels = [lab for lab, _ in cache.model_closure(f)]
    assert "pkg:robot/cad/holes.py" in labels and "pkg:robot/cad/fastener_catalog.py" in labels


def test_same_content_two_paths_same_key(tmp_path):
    a = _proj(tmp_path / "a")
    b = tmp_path / "deeper" / "x" / "b"
    b.parent.mkdir(parents=True)
    shutil.copytree(a, b)
    shape = {"type": "model", "file": "src/part.py"}
    assert geom.key_for(shape, a) == geom.key_for(shape, b)
    raw = {"parts": [{"model": "src/part.py"}], "reference_cad": {"dir": "src"}}
    assert cache.referenced_hash(raw, a) == cache.referenced_hash(raw, b)
    (b / "src" / "helpers.py").write_text("def size():\n    return 3\n")
    assert cache.referenced_hash(raw, a) != cache.referenced_hash(raw, b)


def test_code_hash_covers_subpackages():
    files = {f.relative_to(cache.HERE).as_posix() for f in cache.HERE.rglob("*.py")}
    assert "cad/holes.py" in files  # sanity: the subpackage exists
    # code_hash must read it: patch its content hash and the key moves
    real = cache.source_hash
    k1 = cache.code_hash()
    try:
        cache.source_hash = lambda *fs: real(*fs) if not any(str(f).endswith("cad/holes.py") for f in fs) else "x"
        assert cache.code_hash() != k1
    finally:
        cache.source_hash = real


def test_verify_same_result_and_hits_from_two_paths(tmp_cache):
    tpl = Path(checks.__file__).resolve().parents[1] / "templates"
    src = next(f for f in sorted(tpl.glob("*.json")) if '"model"' not in f.read_text())
    a, b = tmp_cache / "a", tmp_cache / "elsewhere" / "deep" / "b"
    a.mkdir()
    b.mkdir(parents=True)
    shutil.copy(src, a / "spec.json")
    shutil.copy(src, b / "spec.json")
    opts = checks.Options(only=["assembly"]) if "only" in vars(checks.Options()) else checks.Options()

    def rep(p):
        d = checks.verify(spec_mod.load(p / "spec.json"), opts).to_dict()
        d.pop("timings_s", None)
        return json.dumps(d, sort_keys=True, default=str)

    ra = rep(a)
    cache.reset_stats()
    rb = rep(b)
    assert ra == rb
    s = cache.stats()
    assert s.get("group", {}).get("misses", 0) == 0, s
