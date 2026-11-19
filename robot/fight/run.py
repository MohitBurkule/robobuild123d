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

os.environ.setdefault("MUJOCO_GL", "egl")  # before mujoco is imported anywhere (headless render)

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


def _out(sim, n):
    """Touched the floor outside the arena: COM below the platform (pit / drop-off), or past the walls of a closed box."""
    c = sim.com(n)
    if sim.arena is not None:
        return bool(float(c[2]) < sim.arena.out_z)
    return bool(max(abs(float(v)) for v in c[:2]) > sim.scene.arena_half + 0.03)


def outcome(sim, names, t):
    """Per robot: upside-down (and cannot drive inverted), parts lost, out of the arena."""
    out = {}
    for n in names:
        _, _, R = sim.frame(n)
        prof = sim.profiles[n]
        lost = [w.part for w in sim.welds if w.robot == n and w.broken_at is not None]
        out[n] = {"inverted": bool(R[2, 2] < -0.3), "stuck_inverted": bool(R[2, 2] < -0.3 and not prof.can_run_inverted
                                                                          and not prof.lifter),
                  "out_of_arena": _out(sim, n),
                  "parts_lost": lost, "pos": [round(float(v), 3) for v in sim.com(n)]}
    return out


def fight(spec_a, spec_b, seconds=20.0, out=None, fps=30, size=(640, 480), timestep=5e-5, seed=0, log=print, view="arena", follow=None,
          arena=None):
    sa, sb = spec_mod.load(spec_a), spec_mod.load(spec_b)
    ma, mb = load_model(spec_a), load_model(spec_b)
    pa, pb = profile.build(sa, ma), profile.build(sb, mb)
    na = (sa.name or "A").split(" (")[0].replace(" ", "_")
    nb = (sb.name or "B").split(" (")[0].replace(" ", "_")
    if na == nb:
        nb += "_2"
    rng = np.random.default_rng(seed)
    sim = FightSim(timestep=timestep, arena=arena)
    jit = rng.uniform(-10, 10, 2)
    sx = sim.arena.spawn if sim.arena is not None else 0.3
    sim.add_fighter(ma, pa, Placement(na, (-sx, -0.05), 0 + jit[0]))
    sim.add_fighter(mb, pb, Placement(nb, (sx, 0.05), 180 + jit[1]))
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
    t0 = time.time()
    hits = []
    import copy

    import mujoco as mujoco_

    res_unstable = None
    retries = 0
    prev_w = {n: 0.0 for n in (na, nb)}
    peak = {n: {"tilt_deg": 0.0, "lift_mm": 0.0} for n in (na, nb)}
    z0 = {n: float(sim.com(n)[2]) for n in (na, nb)}
    m_, d_ = sim.m, sim.d
    spec_state = mujoco_.mjtState.mjSTATE_INTEGRATION
    n_state = mujoco_.mj_stateSize(m_, spec_state)

    def snapshot():
        st = np.empty(n_state)
        mujoco_.mj_getState(m_, d_, st, spec_state)
        py = copy.deepcopy((sim.welds, len(sim.events), sim.plant, hz.tyre, hz.dead, hz.cut, hz.debris_live, hz.stall_t,
                            hz.queue, sim.profiles, ba.__dict__, bb.__dict__, hits, prev_w, peak))
        arr = (m_.geom_contype.copy(), m_.geom_conaffinity.copy(), m_.geom_friction.copy())
        return st, py, arr, next_ctrl, next_plant, next_frame

    next_ctrl = next_plant = next_frame = 0.0
    snap, fine_until = snapshot(), -1.0
    out_t = None
    while d_.time < seconds:
        t = float(d_.time)
        if t >= next_ctrl:
            next_ctrl += CONTROL_DT
            for nm in sim.open_pits(t):
                sim.events.append((t, "pit_open", "", nm, 0))
            if out_t is None:
                for n in (na, nb):
                    if _out(sim, n):  # touched the pit / outside floor: fight over (keep filming 0.5 s)
                        out_t = t
                        sim.events.append((t, "out", n, "arena", 0))
            if out_t is not None and t > out_t + 0.5:
                break
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
            if int(t / CONTROL_DT) % 5 == 0 and t > fine_until:  # checkpoint every 20 ms
                snap = snapshot()
        if t >= next_plant:
            dtp = 5 * timestep
            next_plant += dtp
            hz.tick(t, dtp)
            sim.step_plant(dtp)
        m_.opt.timestep = timestep / 4 if t < fine_until else timestep
        sim.step_damage()
        if d_.warning[mujoco_.mjtWarning.mjWARN_BADQACC].number:
            # adaptive step: the solver diverged on a violent contact; go back to the last checkpoint and redo that
            # stretch at a quarter of the step (what any adaptive integrator does), instead of losing the fight
            d_.warning[mujoco_.mjtWarning.mjWARN_BADQACC].number = 0
            retries += 1
            if retries > 20:
                res_unstable = round(t, 4)
                sim.events.append((t, "unstable", "", "solver", 0))
                break
            st, py, arr, next_ctrl, next_plant, next_frame = snap
            mujoco_.mj_setState(m_, d_, st, spec_state)
            (welds, n_ev, plant, hz.tyre, hz.dead, hz.cut, hz.debris_live, hz.stall_t, hz.queue, profs, ba_d, bb_d,
             hits, prev_w, peak) = copy.deepcopy(py)
            sim.welds[:] = welds
            del sim.events[n_ev:]
            sim.plant.clear()
            sim.plant.update(plant)
            sim.profiles.update(profs)
            ba.__dict__.update(ba_d)
            bb.__dict__.update(bb_d)
            m_.geom_contype[:], m_.geom_conaffinity[:], m_.geom_friction[:] = arr
            mujoco_.mj_forward(m_, d_)
            fine_until = float(d_.time) + 0.03
            continue
        if writer is not None and d_.time >= next_frame:
            next_frame += 1.0 / fps
            _aim(cam, sim, view, follow or na, nb if (follow or na) == na else na)
            renderer.update_scene(sim.d, cam)
            writer.append_data(renderer.render())
    if writer is not None:
        writer.close()
        renderer.close()
    res = {"robots": [na, nb], "seconds": seconds, "arena": sim.arena.name if sim.arena else "closed", "wall_s": round(time.time() - t0, 1),
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
    res["unstable_at"] = res_unstable
    res["solver_retries"] = retries
    res["winner"] = judge(res) if res_unstable is None else "unstable"
    log(json.dumps({k: res[k] for k in ("robots", "wall_s", "winner")}))
    return res


def judge(res):
    """Simple judging: a robot stuck upside down loses; else fewer parts lost and more damage dealt wins."""
    a, b = res["robots"]
    oa, ob = res["outcome"][a], res["outcome"][b]
    first_out = next((e[2] for e in res.get("events", []) if e[1] == "out"), None)
    if first_out in (a, b):  # pit / out of the arena first: immediate loss, even if the other follows it down
        return b if first_out == a else a
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
        h = sim.scene.arena_half or 0.6
        cam.distance, cam.azimuth, cam.elevation = 0.75 * max(1.0, h / 0.45), 90, -58
        cam.lookat[:] = [mid[0] * 0.5, mid[1] * 0.5, 0.0]
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
