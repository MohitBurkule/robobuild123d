"""Repo-wide pytest policy for the robot packages: the `slow` marker.

`pytest -m "not slow" robot/tests` and `pytest -m "not slow" robots/revron/tests` are the fast gate
(.github/workflows/robot.yml); the nightly job runs `-m slow`. Run the two directories as separate
pytest invocations: both contain a test_joints.py and neither is a package.

A test is slow when it takes more than about 20 s on a 4-core runner. List it in SLOW below (a node id prefix:
a file, a test function, or one parametrized case) or decorate it with @pytest.mark.slow.
"""
import pytest

# Node id prefixes relative to the repo root, e.g. "robot/tests/test_gen_integration.py" or
# "robot/tests/test_x.py::test_y". EMPTY: the timing run was cut short, nothing has been measured yet.
SLOW: tuple[str, ...] = (
    # full-verify equality tests: each runs the whole verifier 2-4x (15+ min even locally, and the
    # native trimesh/rtree stack segfaults under xdist load on 2-core CI runners)
    "robot/tests/test_cache.py::test_wedge_cached_equals_uncached_and_parallel_equals_serial",
    "robot/tests/test_cache.py::test_one_part_change_reuses_other_queries",
    "robot/tests/test_cad_incremental.py",
    # end-to-end generated-robot gates: each builds and fully verifies several robots (minutes each)
    "robot/tests/test_gen_integration.py",
)


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: takes more than ~20 s; excluded from the fast CI gate, run nightly")


def pytest_collection_modifyitems(config, items):
    for item in items:
        if SLOW and item.nodeid.startswith(SLOW):
            item.add_marker(pytest.mark.slow)
