"""Revron lobe root fillet: one multi-section ruled loft, not a chain of slices handed to a single fuse (a cold chassis
build with 24 touching slices in one fuse was OOM-killed in CI)."""

import importlib.util
import math
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[2] / "robots" / "revron" / "src" / "build_revron.py"


def _mod():
    spec = importlib.util.spec_from_file_location("build_revron_t", SRC)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.mark.skipif(not SRC.exists(), reason="revron sources absent")
def test_multi_section_loft_matches_slices():
    from shapely.geometry import Point

    br = _mod()
    lobe = Point(0.0, 0.0).buffer(4.0, 32)
    R = 1.95
    hs = [R * k / 4 for k in range(5)]
    secs = [(lobe.buffer(R - math.sqrt(R * R - (R - h) ** 2), join_style=1), h) for h in hs]
    one = br._loft_yz_n(secs, n=64)
    assert one.is_valid and len(one.solids()) == 1
    slices = sum(br._loft_yz(secs[i][0], secs[i][1], secs[i + 1][0], secs[i + 1][1], n=64).volume for i in range(4))
    assert one.volume == pytest.approx(slices, rel=1e-6)


@pytest.mark.skipif(not SRC.exists(), reason="revron sources absent")
def test_chassis_lobe_fillet_is_one_loft():
    text = SRC.read_text()
    assert "_loft_yz_n([(lobe.buffer(" in text


def test_contains_chunked_matches_whole(monkeypatch):
    """world._contains answers in blocks (bounded memory without embree) and agrees with one whole-array call."""
    import numpy as np
    import trimesh

    from robot import world

    m = trimesh.creation.icosphere(subdivisions=3, radius=5.0)
    Q = np.random.default_rng(0).uniform(-6, 6, (1000, 3))
    whole = m.contains(Q)
    monkeypatch.setattr(world, "CONTAINS_CHUNK", 64)
    calls = []
    orig = trimesh.Trimesh.contains
    monkeypatch.setattr(trimesh.Trimesh, "contains", lambda self, P: calls.append(len(P)) or orig(self, P))
    got = world._contains(m, Q)
    assert max(calls) <= 64 and sum(calls) == len(Q)
    assert (got == whole).all()
