import numpy as np

from robot.fight import arenas
from robot.fight.arena import FightSim
from robot.fight.run import judge


def test_presets_geometry():
    a = arenas.get("aws2025")
    assert a.half * 2 >= 0.75  # AWS 2025 minimum arena
    gap = max(a1 - a0 for spans in a.gaps.values() for a0, a1 in spans)
    assert gap >= 0.2  # at least one 200 mm unwalled gap
    assert not a.on_platform((0.0, 0.32)) and a.on_platform((0.0, 0.0)) and not a.on_platform((0.6, 0))
    c = arenas.get("aws_classic")
    open_len = sum(a1 - a0 for spans in c.gaps.values() for a0, a1 in spans)
    assert open_len >= 0.5 * 8 * c.half - 1e-9  # 50 % of the edge unwalled
    b = arenas.get("beetle_champs")
    assert b.on_platform((0, -0.38), t=10) and not b.on_platform((0, -0.38), t=31)


def test_box_falls_in_pit_and_cover_opens():
    import mujoco
    sim = FightSim(arena="beetle_champs")
    sim.spec.worldbody.add_body(name="blk", pos=[0, -0.38, 0.03]).add_freejoint()
    sim.spec.body("blk").add_geom(type=mujoco.mjtGeom.mjGEOM_BOX, size=[0.02, 0.02, 0.02], mass=0.1)
    sim.compile()
    bid = mujoco.mj_name2id(sim.m, mujoco.mjtObj.mjOBJ_BODY, "blk")
    for _ in range(4000):
        mujoco.mj_step(sim.m, sim.d)
    assert sim.d.xpos[bid][2] > 0.0  # cover still closed: resting on it
    assert sim.open_pits(31.0)
    for _ in range(6000):
        mujoco.mj_step(sim.m, sim.d)
    assert sim.d.xpos[bid][2] < -0.05  # dropped into the pit


def test_judge_first_out_loses():
    res = {"robots": ["a", "b"], "events": [[1.0, "out", "b", "arena", 0], [1.2, "out", "a", "arena", 0]], "hits": [],
           "outcome": {n: {"out_of_arena": True, "stuck_inverted": False, "parts_lost": []} for n in "ab"}}
    assert judge(res) == "a"
