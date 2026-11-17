"""Spinner wobble in MuJoCo: real-world imbalance, flexible mount and a hit, then the swept clearance at that deflection.

A real weapon is never balanced (cut tolerance, bolt pattern, a tooth heavier than the counterweight) and never held
rigidly (bearing play, printed uprights flex). Here the weapon sits on a carrier body with two radial springs and two tilt
springs (mount stiffness) between it and the chassis; its centre of mass is offset by the imbalance. The robot sits on the
floor on its own wheels, the weapon spins up to its rpm, then takes one hit (a radial force pulse at the rim).
Outputs: steady wobble (radial mm, tilt deg), peak deflection under the hit, mount natural frequency vs spin frequency
(resonance), chassis vibration (g). `clearance()` then sweeps the real weapon mesh (every part, full detail) through a
turn at that deflection and tilt, and reports every static part it would touch.

Spec (all optional, defaults reported as guessed):
  sim.weapon.imbalance_mm   centre-of-mass offset (default 0.05 mm: laser-cut disc + bolt pattern, unbalanced)
  sim.weapon.mount_k_Npm    radial stiffness of bearings + uprights (default 2e5 N/m: printed uprights)
  sim.weapon.tilt_k_Nm      tilt stiffness (default 20 N m/rad)
  sim.weapon.play_mm        radial bearing play added on top (default 0.02 mm)
  sim.weapon.hit_N          radial hit force pulse, 0.3 ms (default 1500 N)
"""

from __future__ import annotations

import math

import mujoco
import numpy as np

from ..sim.model import CHASSIS
from .profile import Profile

DEFAULTS = {"imbalance_mm": 0.05, "mount_k_Npm": 2e5, "tilt_k_Nm": 20.0, "play_mm": 0.02, "hit_N": 1500.0}


def params(spec):
    w = dict((spec.raw.get("sim") or {}).get("weapon") or {})
    out, guessed = {}, []
    for k, v in DEFAULTS.items():
        if k in w:
            out[k] = float(w[k])
        else:
            out[k] = v
            guessed.append(k)
    return out, guessed


def _basis(axis):
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    u = np.cross(a, [1.0, 0, 0] if abs(a[0]) < 0.9 else [0, 1.0, 0])
    u /= np.linalg.norm(u)
    return a, u, np.cross(a, u)


def simulate(model, prof: Profile, p: dict, spin_s=1.2, timestep=5e-5):
    w = model.weapon
    if w is None or not prof.weapon_omega:
        return None
    a, u, v = _basis(w.axis)
    s = mujoco.MjSpec()
    s.option.timestep = timestep
    s.option.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST
    s.worldbody.add_geom(type=mujoco.mjtGeom.mjGEOM_PLANE, size=[1, 1, 0.1])
    lo, _ = model.bounds()
    ch = s.worldbody.add_body(name="chassis", pos=[0, 0, -lo[2] + 5e-4])
    ch.add_freejoint()
    rest = [g for g in model.groups if g is not w]
    parts = [pp for g in rest for pp in g.parts]
    m = sum(pp.mass for pp in parts)
    com = sum(pp.mass * pp.com for pp in parts) / m
    I = np.zeros((3, 3))
    for pp in parts:
        d = pp.com - com
        I += pp.inertia + pp.mass * (d @ d * np.eye(3) - np.outer(d, d))
    ch.explicitinertial = True
    ch.mass, ch.ipos = m, list(com)
    ch.fullinertia = [I[0, 0], I[1, 1], I[2, 2], I[0, 1], I[0, 2], I[1, 2]]
    for i, pp in enumerate(parts):
        if pp.kind in ("wheel", "tyre"):
            s.add_mesh(name=f"m{i}", uservert=pp.verts.reshape(-1).tolist())
            ch.add_geom(type=mujoco.mjtGeom.mjGEOM_MESH, meshname=f"m{i}", mass=0, friction=[1.2, 0.005, 1e-4])
    car = ch.add_body(name="carrier", pos=list(w.pivot))
    car.explicitinertial = True
    car.mass, car.ipos, car.fullinertia = 1e-4, [0, 0, 0], [1e-10, 1e-10, 1e-10, 0, 0, 0]
    for nm, ax in (("ru", u), ("rv", v)):
        car.add_joint(name=nm, type=mujoco.mjtJoint.mjJNT_SLIDE, axis=list(ax), stiffness=p["mount_k_Npm"], damping=2.0)
    for nm, ax in (("tu", u), ("tv", v)):
        car.add_joint(name=nm, type=mujoco.mjtJoint.mjJNT_HINGE, axis=list(ax), stiffness=p["tilt_k_Nm"], damping=0.002)
    wb = car.add_body(name="weapon")
    wb.explicitinertial = True
    wb.mass = w.mass
    wb.ipos = list(w.com - w.pivot + u * p["imbalance_mm"] * 1e-3)
    J = w.inertia
    wb.fullinertia = [J[0, 0], J[1, 1], J[2, 2], J[0, 1], J[0, 2], J[1, 2]]
    wb.add_joint(name="spin", type=mujoco.mjtJoint.mjJNT_HINGE, axis=list(a), damping=1e-6, armature=2e-6)
    act = s.add_actuator(name="m", target="spin", trntype=mujoco.mjtTrn.mjTRN_JOINT)
    kv = 0.004
    act.gainprm[0], act.biasprm[2] = kv, -kv
    act.gaintype, act.biastype = mujoco.mjtGain.mjGAIN_FIXED, mujoco.mjtBias.mjBIAS_AFFINE
    act.forcelimited, act.forcerange = True, [-prof.weapon_torque, prof.weapon_torque]
    mm = s.compile()
    d = mujoco.MjData(mm)
    d.ctrl[0] = prof.weapon_omega
    jq = {n: mm.joint(n).qposadr[0] for n in ("ru", "rv", "tu", "tv", "spin")}
    jv = mm.joint("spin").dofadr[0]
    wid = mm.body("weapon").id
    cid = mm.body("chassis").id
    steady_r = steady_t = 0.0
    acc = []
    n = int(spin_s / timestep)
    for k in range(n):
        mujoco.mj_step(mm, d)
        if k > 0.6 * n:
            steady_r = max(steady_r, math.hypot(d.qpos[jq["ru"]], d.qpos[jq["rv"]]))
            steady_t = max(steady_t, math.hypot(d.qpos[jq["tu"]], d.qpos[jq["tv"]]))
            acc.append(float(np.linalg.norm(d.qacc[:3])) if k % 20 == 0 else 0.0)
    omega = float(d.qvel[jv])
    # one hit: radial force pulse at the rim (world frame), 0.3 ms
    pulse = int(3e-4 / timestep)
    R = d.xmat[wid].reshape(3, 3)
    fdir = R @ u
    peak_r = peak_t = 0.0
    for k in range(int(0.05 / timestep)):
        d.xfrc_applied[wid, :3] = -fdir * p["hit_N"] if k < pulse else 0.0
        mujoco.mj_step(mm, d)
        peak_r = max(peak_r, math.hypot(d.qpos[jq["ru"]], d.qpos[jq["rv"]]))
        peak_t = max(peak_t, math.hypot(d.qpos[jq["tu"]], d.qpos[jq["tv"]]))
    f_n = math.sqrt(p["mount_k_Npm"] / max(w.mass, 1e-6)) / (2 * math.pi)
    return {"omega_rad_s": round(omega, 1), "spin_hz": round(abs(omega) / (2 * math.pi), 1), "mount_hz": round(f_n, 1),
            "wobble_mm": round(steady_r * 1e3 + p["play_mm"], 3), "wobble_tilt_deg": round(math.degrees(steady_t), 3),
            "hit_mm": round(peak_r * 1e3 + p["play_mm"], 3), "hit_tilt_deg": round(math.degrees(peak_t), 3),
            "chassis_vib_g": round(float(max(acc or [0])) / 9.81, 1), "imbalance_gmm": round(w.mass * 1e3 * p["imbalance_mm"], 3)}


def clearance(world, model, deflect_mm, tilt_deg, h=1.5, n_ang=8, couple_mm=0.6):
    """Static parts the real weapon meshes touch when the weapon is shifted `deflect_mm` (8 radial directions) and tilted
    `tilt_deg`, at n_ang spin angles. Parts already touching the weapon at rest (stator, bearings, shaft seat) are judged
    by the static interference check and skipped here. Returns {part id: points inside}."""
    from .. import xform  # noqa: F401

    w = model.weapon
    ids = {pp.id for pp in w.parts}
    wb = [b for b in world.bodies if b.id in ids]
    static = [b for b in world.bodies if b.id not in ids and not b.is_wire and not b.fastener]
    sv = [b.surface(h) for b in wb]
    pts = np.vstack([x[0] for x in sv])
    nrm = np.vstack([x[1] for x in sv])
    piv = w.pivot * 1e3
    a, u, v = _basis(w.axis)
    lo, hi = pts.min(0) - 6, pts.max(0) + 6
    near = [b for b in static if np.all(b.aabb[1] >= lo) and np.all(b.aabb[0] <= hi)]
    dil = pts + couple_mm * nrm
    touching0 = {b.id for b in near if b.inside(pts).any() or b.inside(dil).any()}
    near = [b for b in near if b.id not in touching0]
    hits = {}
    t = math.radians(tilt_deg)
    for k in range(n_ang):
        R = _rot(a, 2 * math.pi * k / n_ang)
        P0 = (pts - piv) @ R.T
        for j in range(8):
            th = 2 * math.pi * j / 8
            dvec = math.cos(th) * u + math.sin(th) * v
            Rt = _rot(np.cross(a, dvec), t)
            P = P0 @ Rt.T + piv + deflect_mm * dvec
            for b in near:
                c = int(b.inside(P).sum())
                if c:
                    hits[b.id] = hits.get(b.id, 0) + c
    return hits, sorted(touching0)


def _rot(axis, ang):
    a = np.asarray(axis, float)
    n = np.linalg.norm(a)
    if n < 1e-12 or abs(ang) < 1e-12:
        return np.eye(3)
    a = a / n
    K = np.array([[0, -a[2], a[1]], [a[2], 0, -a[0]], [-a[1], a[0], 0]])
    return np.eye(3) + math.sin(ang) * K + (1 - math.cos(ang)) * K @ K
