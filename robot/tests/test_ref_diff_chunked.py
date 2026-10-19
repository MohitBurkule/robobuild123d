import numpy as np
import trimesh

from robot.checks import ref_diff


def test_closest_dist_chunked_matches_unchunked():
    m = trimesh.creation.icosphere(subdivisions=3, radius=5.0)
    pts = np.random.default_rng(0).uniform(-8, 8, (1000, 3))
    want = trimesh.proximity.closest_point(m, pts)[1]
    got = ref_diff.closest_dist_chunked(m, pts, chunk=37)
    assert got.shape == want.shape
    assert np.allclose(got, want)


def test_surface_deviation_uses_chunked_query(monkeypatch):
    calls = []
    real = trimesh.proximity.closest_point
    monkeypatch.setattr(trimesh.proximity, "closest_point", lambda m, p: calls.append(len(p)) or real(m, p))
    a = trimesh.creation.box((10, 10, 1))
    ref_diff.surface_deviation(a, a.copy(), n=2000)
    assert calls and max(calls) <= 256
