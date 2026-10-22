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


def test_chassis_lobe_root_is_one_fillet():
    """tub2 builds the lobe root as ONE fillet of radius LOBE_ROOT_R after the unions (no slices fused): the tub is one valid solid and carries
    cylindrical root faces of exactly that radius on the outer wall plane."""
    import sys

    sys.path.insert(0, str(SRC.parent))
    from revron import tub2, tub2_fillets
    from revron.tub2_params import CH_HALF_W

    t = tub2.chassis2()
    assert len(t.solids()) == 1 and t.is_valid
    roots = [f for f in t.faces() if f.geom_type.name == "CYLINDER" and abs(f.radius - tub2_fillets.LOBE_ROOT_R) < 1e-6
             and abs(abs(f.center().X) - CH_HALF_W) < tub2_fillets.LOBE_ROOT_R + 1.0]
    assert roots


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
