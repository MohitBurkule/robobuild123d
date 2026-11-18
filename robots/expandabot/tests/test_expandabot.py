"""Smoke and packaging tests for Expandabot CAD (`robots/expandabot`)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "src"))
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from expandabot import assembly, params  # noqa: E402


def test_params_relations():
    assert params.check() == []
    assert params.REST_L <= params.START_CUBE
    assert max(params.OVERALL_L, params.OVERALL_W) <= params.FOOTPRINT_SQUARE


def test_all_parts_build_single_manifold_solids():
    made = assembly.made_parts()
    assert len(made) == 13
    for name, (solid, _kind) in made.items():
        solids = solid.solids()
        assert len(solids) == 1, f"{name} produced {len(solids)} solids"
        assert solid.is_valid, f"{name} is not valid"
        assert solid.volume > 0.0, f"{name} has non-positive volume"
    total_mass = assembly.mass_report(made)
    assert 80.0 < total_mass <= params.MASS_LIMIT_G
