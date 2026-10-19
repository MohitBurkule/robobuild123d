"""`world._contains` must be reproducible: trimesh re-casts ambiguous inside/outside rays along a random direction, and
trimesh >= 4.6 draws it from a shared, OS-seeded Generator (`trimesh.util.random_generator`), not the global numpy RNG.
Unpinned, this made `ground.wheel_exposed_frac` differ between runs (flaky test_cache parity)."""
import numpy as np
import trimesh
import trimesh.util as tu

from robot import world


class _Probe:
    """Stands in for a mesh: `contains` returns the random direction trimesh would use for a broken ray."""

    def contains(self, Q):
        return tu.random_generator().random(3)


def test_contains_pins_trimesh_generator_and_restores_it():
    orig = tu.random_generator
    tu.random_generator().random(5)  # advance the shared generator as other code would
    a = world._contains(_Probe(), np.zeros((1, 3)))
    tu.random_generator().random(7)
    b = world._contains(_Probe(), np.zeros((1, 3)))
    assert np.array_equal(a, b)
    assert tu.random_generator is orig


def test_contains_still_answers():
    m = trimesh.creation.box((2, 2, 2))
    assert world._contains(m, np.array([[0, 0, 0], [5, 0, 0]])).tolist() == [True, False]
