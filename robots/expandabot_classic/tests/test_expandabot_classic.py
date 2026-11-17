"""Smoke tests for Expandabot Classic CAD (`robots/expandabot_classic`)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "src"))
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from expandabot_classic import assembly, params  # noqa: E402


def test_params_and_solids():
    assert params.check() == []
    made = assembly.made_parts()
    for name, (solid, _kind) in made.items():
        assert len(solid.solids()) == 1, f"{name} produced {len(solid.solids())} solids"
        assert solid.is_valid, f"{name} is not valid"
    assert assembly.mass_report(made) <= params.MASS_LIMIT_G
