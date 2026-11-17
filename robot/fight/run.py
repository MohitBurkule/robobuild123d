"""Run one fight: load two specs, place them in the arena, drive both brains, log hits and breaks, write a video.

    python -m robot.fight robots/revron/spec.json robots/expandabot/spec.json --seconds 20 --out fight.mp4
"""

from __future__ import annotations

import json
import math
import os
import time
from pathlib import Path

import numpy as np

from .. import spec as spec_mod
from ..sim.scene import Placement
from . import brains, profile
from .arena import FightSim

CONTROL_DT = 0.004  # brain rate (s)


def load_model(path, cache_dir=None):
    """RobotModel for a spec, cached as a pickle keyed on the spec mtime (the CAD build is the slow part)."""
    import pickle

    from ..sim import model as model_mod

    path = Path(path)
    cache_dir = Path(cache_dir or os.environ.get("ROBOT_FIGHT_CACHE", Path.home() / ".cache" / "robot_fight"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    key = cache_dir / f"{path.parent.name}_{int(path.stat().st_mtime)}.pkl"
    if key.exists():
        return pickle.loads(key.read_bytes())
    m = model_mod.load(path)
    key.write_bytes(pickle.dumps(m))
    return m


def outcome(sim, names, t):
    """Per robot: upside-down (and cannot drive inverted), parts lost, weapon speed."""
    out = {}
    for n in names:
        _, _, R = sim.frame(n)
        prof = sim.profiles[n]
        lost = [w.part for w in sim.welds if w.robot == n and w.broken_at is not None]
        out[n] = {"inverted": bool(R[2, 2] < -0.3), "stuck_inverted": bool(R[2, 2] < -0.3 and not prof.can_run_inverted
                                                                          and not prof.lifter),
                  "out_of_arena": bool(max(abs(float(v)) for v in sim.com(n)[:2]) > sim.scene.arena_half + 0.03),
                  "parts_lost": lost, "pos": [round(float(v), 3) for v in sim.com(n)]}
    return out


def fight(spec_a, spec_b, seconds=20.0, out=None, fps=30, size=(640, 480), timestep=1e-4, seed=0, log=print, view="arena", follow=None):
    sa, sb = spec_mod.load(spec_a), spec_mod.load(spec_b)
    ma, mb = load_model(spec_a), load_model(spec_b)
    pa, pb = profile.build(sa, ma), profile.build(sb, mb)
    na = (sa.name or "A").split(" (")[0].replace(" ", "_")
    nb = (sb.name or "B").split(" (")[0].replace(" ", "_")
    if na == nb:
        nb += "_2"
    rng = np.random.default_rng(seed)
    sim = FightSim(timestep=timestep)
    jit = rng.uniform(-10, 10, 2)
    sim.add_fighter(ma, pa, Placement(na, (-0.3, -0.05), 0 + jit[0]))
    sim.add_fighter(mb, pb, Placement(nb, (0.3, 0.05), 180 + jit[1]))
    sim.compile()
    ba, bb = brains.make(pa.strategy, na, nb), brains.make(pb.strategy, nb, na)
    from .hazards import Hazards

    hz = Hazards(sim, {na: sa, nb: sb}, seed=seed)
    hz.setup_collision_bits()
    writer = renderer = None
    if out:
        os.environ.setdefault("MUJOCO_GL", "egl")
        import imageio.v2 as imageio
        import mujoco

        renderer = mujoco.Renderer(sim.m, size[1], size[0])
        writer = imageio.get_writer(out, fps=fps, quality=7, macro_block_size=8)
        cam = mujoco.MjvCamera()
        cam.distance, cam.azimuth, cam.elevation = 0.75, 90, -58
    n_ctrl = max(1, int(round(CONTROL_DT / timestep)))
    n_frame = max(1, int(round(1.0 / fps / timestep)))
    steps = int(seconds / timestep)
    t0 = time.time()
    hits = []
    prev_w = {n: 0.0 for n in (na, nb)}
    peak = {n: {"tilt_deg": 0.0, "lift_mm": 0.0} for n in (na, nb)}
    z0 = {n: float(sim.com(n)[2]) for n in (na, nb)}
    for k in range(steps):
        t = k * timestep
        if k % n_ctrl == 0:
            for b in (ba, bb):
                cmd = hz.delay(b.me, t, b.act(sim, t, CONTROL_DT))  # driver reaction delay + steering noise
                if cmd is None or hz.dead[b.me]:
                    continue
                sim.drive(b.me, *cmd["drive"])
                if "weapon" in cmd:
                    sim.spin_weapon(b.me, cmd["weapon"])
                if "lift" in cmd:
                    sim.lift(b.me, cmd["lift"])
            for n in (na, nb):
                peak[n]["tilt_deg"] = max(peak[n]["tilt_deg"], round(sim.tilt(n), 1))
                peak[n]["lift_mm"] = max(peak[n]["lift_mm"], round((float(sim.com(n)[2]) - z0[n]) * 1000, 1))
            for n in (na, nb):  # a weapon hit = a sudden drop in spinner speed
                w = sim.weapon_omega(n)
                g = sim.robots[n].weapon
                if g is not None and abs(prev_w[n]) - abs(w) > 60:
                    I = float(g.axis @ g.inertia @ g.axis)
                    e = 0.5 * I * (prev_w[n] ** 2 - w ** 2)
                    hits.append((round(t, 3), n, round(e, 2)))
                    sim.events.append((t, "hit", n, "weapon", round(e, 2)))
                prev_w[n] = w
        if k % 5 == 0:
            hz.tick(t, 5 * timestep)
            sim.step_plant(5 * timestep)
        sim.step_damage()
        if writer is not None and k % n_frame == 0:
            _aim(cam, sim, view, follow or na, nb if (follow or na) == na else na)
            renderer.update_scene(sim.d, cam)
            writer.append_data(renderer.render())
    if writer is not None:
        writer.close()
        renderer.close()
    res = {"robots": [na, nb], "seconds": seconds, "wall_s": round(time.time() - t0, 1),
           "events": [list(e) for e in sim.events], "hits": hits, "outcome": outcome(sim, (na, nb), seconds), "peak": peak,
           "welds": [{"robot": w.robot, "part": w.part, "break_N": round(w.break_n, 1), "peak_N": round(w.peak_n, 1),
                      "broken_at": w.broken_at} for w in sim.welds],
           "defaults": {na: pa.defaults, nb: pb.defaults},
           "hazards": {"dead": hz.dead, "tyres": {f"{r}/{g}": round(v, 2) for (r, g), v in hz.tyre.items()},
                       "wires_cut": {r: sorted(v) for r, v in hz.cut.items()},
                       "debris_live": sorted(f"{r}/{p}" for r, p in hz.debris_live)},
           "electric": {n: {"battery_v": round(pl["battery"].v, 2), "soc": round(pl["battery"].soc, 3),
                            "motors": {g: {"temp_c": round(m.temp, 1), "dead": m.dead} for g, m in pl["motors"].items()}}
                        for n, pl in sim.plant.items()}}
    res["winner"] = judge(res)
    log(json.dumps({k: res[k] for k in ("robots", "wall_s", "winner")}))
    return res


def judge(res):
    """Simple judging: a robot stuck upside down loses; else fewer parts lost and more damage dealt wins."""
    a, b = res["robots"]
    oa, ob = res["outcome"][a], res["outcome"][b]
    dz = res.get("hazards", {}).get("dead", {})
    if bool(dz.get(a)) != bool(dz.get(b)):  # switch knocked off / power wire cut: robot is dead
        return b if dz.get(a) else a
    if oa["out_of_arena"] != ob["out_of_arena"]:  # thrown out of the arena: immediate loss (AWS rules)
        return b if oa["out_of_arena"] else a
    if oa["stuck_inverted"] != ob["stuck_inverted"]:
        return b if oa["stuck_inverted"] else a
    dealt = {n: sum(e for _, who, e in res["hits"] if who == n) for n in (a, b)}
    sa = len(ob["parts_lost"]) * 10 + dealt[a]
    sb = len(oa["parts_lost"]) * 10 + dealt[b]
    return a if sa > sb else b if sb > sa else "draw"


def _aim(cam, sim, view, me, other):
    """arena: overhead on the midpoint; chase: behind `me`, looking along its heading; fpv: from `me`'s top deck,
    looking forward (a driver's camera bolted to the robot)."""
    if view == "arena":
        mid = (sim.com(me) + sim.com(other)) / 2
        cam.distance, cam.azimuth, cam.elevation = 0.75, 90, -58
        cam.lookat[:] = [mid[0] * 0.8, mid[1] * 0.8, 0.0]
        return
    c = sim.com(me)
    _, h, _ = sim.frame(me)
    f = np.array([math.cos(h), math.sin(h), 0.0])
    cam.azimuth = math.degrees(h)
    if view == "chase":
        cam.distance, cam.elevation = 0.32, -22
        cam.lookat[:] = c + 0.06 * f + [0, 0, 0.01]
    else:  # fpv
        cam.distance, cam.elevation = 0.14, -8
        cam.lookat[:] = c + 0.14 * f + [0, 0, 0.035]
