import pytest
from robot.solve import Lever, solve_mass, MassInfeasible


def lin(v):
    return 100 + 10 * v["a"] + 5 * v["b"]


def test_hits_limit():
    r = solve_mass(lin, [Lever("a", 0, 10, 8), Lever("b", 0, 4, 2, priority=1)], 150, band_g=0.5)
    assert 149.5 <= r.final_g <= 150


def test_priority_first_lever_moves():
    r = solve_mass(lin, [Lever("a", 0, 10, 8), Lever("b", 0, 4, 2, priority=1)], 150)
    assert "a" in r.changed and "b" not in r.changed


def test_infeasible():
    with pytest.raises(MassInfeasible):
        solve_mass(lin, [Lever("a", 5, 10, 8)], 120)


def test_step_snaps_down():
    r = solve_mass(lin, [Lever("a", 0, 10, 8, step=0.4)], 150, band_g=2)
    assert r.final_g <= 150
