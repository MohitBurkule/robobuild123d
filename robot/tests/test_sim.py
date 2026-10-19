"""Physics simulation (robot.sim): unit tests on the extraction and engine, integration tests on real robots."""

import numpy as np
import pytest

mujoco = pytest.importorskip("mujoco")

from robot import sim  # noqa: E402
from robot.sim import scenarios  # noqa: E402
from robot.sim.model import Group, SimPart, part_inertia  # noqa: E402

ROOT = __import__("pathlib").Path(__file__).resolve().parents[2]


def box_robot():
    """A 100 g, 60 mm box on four wheel groups would be heavy to build; a bare chassis box is enough for unit tests."""
    import trimesh

    b = trimesh.creation.box(extents=(60, 60, 20))
    b.apply_translation([0, 0, 10])
    com, I = part_inertia(b, 0.1)
    part = SimPart("box", "structure", b.vertices * 1e-3, 0.1, com, I)
    return sim.RobotModel("box", [Group("chassis", "chassis", [part])])


def test_part_inertia_matches_closed_form_box():
    import trimesh

    b = trimesh.creation.box(extents=(60, 60, 20))
    com, I = part_inertia(b, 0.1)
    assert np.allclose(com, 0, atol=1e-9)
    assert I[2, 2] == pytest.approx(0.1 / 12 * (0.06**2 + 0.06**2), rel=1e-3)


def test_group_mass_com_and_parallel_axis():
    m = np.ones((1, 3))
    a = SimPart("a", "x", m, 1.0, np.array([0.1, 0, 0]), np.zeros((3, 3)))
    b = SimPart("b", "x", m, 1.0, np.array([-0.1, 0, 0]), np.zeros((3, 3)))
    g = Group("g", "chassis", [a, b])
    assert g.mass == 2.0 and np.allclose(g.com, 0)
    assert g.inertia[2, 2] == pytest.approx(2 * 0.1**2)


def test_free_fall_matches_gravity():
    s = sim.Sim(sim.Scene(arena_half=0))
    n = s.add_robot(box_robot(), sim.Placement("box", (0, 0), 0, z_clear=1.0))
    s.compile()
    z0 = s.pose(n)[0][2]
    s.step(0.2)
    assert z0 - s.pose(n)[0][2] == pytest.approx(0.5 * 9.81 * 0.2**2, rel=0.02)


def test_box_rests_on_floor():
    s = sim.Sim()
    n = s.add_robot(box_robot(), sim.Placement("box"))
    s.compile().step(1.0)
    assert s.up_tilt_deg(n) < 0.5
    assert s.pose(n)[0][2] == pytest.approx(0.0, abs=2e-3)


def test_zero_gravity_scene():
    s = sim.Sim(sim.Scene(gravity=0.0, arena_half=0))
    n = s.add_robot(box_robot(), sim.Placement("box", z_clear=0.1))
    s.compile()
    z0 = s.pose(n)[0][2]
    s.step(0.3)
    assert s.pose(n)[0][2] == pytest.approx(z0, abs=1e-6)


def test_prop_falls_and_lands():
    s = sim.Sim(sim.Scene().box("b", (0.02,) * 3, (0, 0.3, 0.2), mass=0.05))
    s.add_robot(box_robot(), sim.Placement("box"))
    s.compile().step(1.0)
    assert s.body_pos("b")[2] == pytest.approx(0.02, abs=2e-3)


@pytest.fixture(scope="module")
def wedge():
    return sim.load(ROOT / "robots/wedge_2wd/spec.json")


def test_load_groups_wheels(wedge):
    assert {g.name for g in wedge.wheels} == {"wheel_l", "wheel_r"}
    assert 0.03 < wedge.mass < 0.15


def test_drive_forward_and_straight(wedge):
    r = scenarios.drive_test(wedge)
    assert r["forward_m"] > 0.1 and abs(r["drift_m"]) < 0.05


def test_drop_lands_upright(wedge):
    r = scenarios.drop_test(wedge, 0.2)
    assert r["settled_tilt_deg"] < 5 and r["peak_g"] > 1


def test_push_light_block(wedge):
    assert scenarios.push_prop_test(wedge)["block_pushed_m"] > 0.05


def test_revron_weapon_and_ram():
    rv = sim.load(ROOT / "robots/revron/spec.json")
    assert rv.weapon is not None and len(rv.wheels) == 4
    r = scenarios.ram_test(rv, rv)
    assert r["peak_robot_contact_n"] > 1 and r["a_tilt_deg"] < 45
