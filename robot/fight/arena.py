"""MuJoCo fight world: robot.sim's rigid groups plus breakable parts held on by weld constraints that snap.

Each breakable part (armour, wedges, forks, lids: profile.BREAKABLE_KINDS or spec sim.breakable) becomes its own free body
welded to the chassis. Every step the weld's constraint force is read back; above the part's break force (from the
fasteners through it, or the spec) the weld is switched off and the part flies free: a chunk chopped off. A sturdy robot
keeps its welds and is thrown as a whole instead. Optionally a part is pre-cut into Voronoi chunks (chunks.py) welded to
each other, so a panel can lose a corner instead of coming off whole.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import mujoco
import numpy as np

from ..sim.engine import ARMATURE, Sim, _quat, _rgba, _rz
from ..sim.model import CHASSIS, Group, RobotModel
from ..sim.scene import Placement, Scene
from .profile import Profile


@dataclass
class Weld:
    robot: str
    part: str
    eq: int  # equality id
    break_n: float
    broken_at: float | None = None
    peak_n: float = 0.0


class FightSim(Sim):
    def __init__(self, scene: Scene | None = None, timestep=1e-4):
        # AWS antweight arenas are closed polycarbonate boxes: walls plus a roof (robots get thrown, not lost)
        super().__init__(scene or Scene(arena_half=0.6, wall_height=0.4), timestep)
        self.profiles: dict[str, Profile] = {}
        self.welds: list[Weld] = []
        self._weld_spec = []  # (robot, part, eq name, break)
        self.events: list = []
        self.lifter_joint: dict[str, str] = {}
        w = self.spec.worldbody
        h = self.scene.arena_half
        if h:
            w.add_geom(name="roof", type=mujoco.mjtGeom.mjGEOM_BOX, size=[h, h, 0.005], pos=[0, 0, self.scene.wall_height + 0.005],
                       rgba=[0.6, 0.7, 0.8, 0.0])
        w.add_light(pos=[0, 0, 1.5], dir=[0, 0, -1], diffuse=[0.9, 0.9, 0.9], castshadow=True)
        w.add_light(pos=[0.6, -0.6, 1.0], dir=[-0.4, 0.4, -1], diffuse=[0.4, 0.4, 0.4])
        self.spec.visual.headlight.ambient = [0.35, 0.35, 0.35]
        if h:  # steel floor sheets: 0.4 mm proud seams every 300 mm (wheels bump, wedges catch)
            for k in range(-1, 2):
                for ax in (0, 1):
                    size = [h, 0.001, 0.0002] if ax == 0 else [0.001, h, 0.0002]
                    pos = [0, k * 0.3, 0.0002] if ax == 0 else [k * 0.3, 0, 0.0002]
                    w.add_geom(name=f"seam{ax}{k}", type=mujoco.mjtGeom.mjGEOM_BOX, size=size, pos=pos,
                               rgba=[0.35, 0.37, 0.4, 1], friction=[0.5, 0.005, 1e-4])
        self.plant: dict = {}  # robot -> {"battery", "motors": {group: Motor}, "duty": {group: d}}
        self.fixed_motors = False  # True = old ideal velocity servos (no curves / sag / heat)

    def add_fighter(self, model: RobotModel, prof: Profile, placement: Placement):
        name = placement.name.replace(" ", "_")
        model = _prep(model, prof)
        self.profiles[name] = prof
        self.robots[name] = model
        self.place[name] = placement
        lo, hi = model.bounds()
        ctr = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0.0])
        # spawn yaw: placement yaw is the WORLD heading of the robot's forward axis
        yaw = math.radians(placement.yaw_deg) - prof.heading0
        R = _rz(yaw)
        t = np.array([placement.xy[0], placement.xy[1], placement.z_clear - lo[2]]) - R @ ctr
        pre = name + "/"
        q = _quat(R)
        chassis = self.spec.worldbody.add_body(name=pre + CHASSIS, pos=list(t), quat=q)
        chassis.add_freejoint(name=pre + "free")
        names = []
        for g in model.groups:
            loose = g.kind == "loose"
            if g.name == CHASSIS:
                b = chassis
            elif loose:
                b = self.spec.worldbody.add_body(name=pre + g.name, pos=list(t), quat=q)
                b.add_freejoint(name=pre + g.name + "_free")
            elif g.kind == "weapon" and not self.fixed_motors:
                wp = wobble_params(prof)
                car = chassis.add_body(name=pre + "carrier", pos=list(g.pivot))
                car.explicitinertial = True
                car.mass, car.ipos, car.fullinertia = 1e-4, [0, 0, 0], [1e-10, 1e-10, 1e-10, 0, 0, 0]
                a_, u_, v_ = _basis(g.axis)
                for nm, ax in (("ru", u_), ("rv", v_)):
                    car.add_joint(name=f"{pre}{nm}", type=mujoco.mjtJoint.mjJNT_SLIDE, axis=list(ax),
                                  stiffness=wp["mount_k_Npm"], damping=5.0, armature=1e-3)
                for nm, ax in (("tu", u_), ("tv", v_)):
                    car.add_joint(name=f"{pre}{nm}", type=mujoco.mjtJoint.mjJNT_HINGE, axis=list(ax),
                                  stiffness=wp["tilt_k_Nm"], damping=0.01, armature=2e-6)
                b = car.add_body(name=pre + g.name, pos=list(-np.asarray(g.pivot)))
                names.append(pre + "carrier")
            else:
                b = chassis.add_body(name=pre + g.name)
            names.append(pre + g.name)
            b.explicitinertial = True
            b.mass = max(g.mass, 1e-5)
            b.ipos = list(g.com)
            if g.kind == "weapon" and not self.fixed_motors:  # real discs are never balanced
                b.ipos = list(g.com + _basis(g.axis)[1] * wobble_params(prof)["imbalance_mm"] * 1e-3)
            I = g.inertia + np.eye(3) * 1e-10
            b.fullinertia = [I[0, 0], I[1, 1], I[2, 2], I[0, 1], I[0, 2], I[1, 2]]
            if loose:
                e = self.spec.add_equality(name=pre + g.name + "_weld", type=mujoco.mjtEq.mjEQ_WELD,
                                           objtype=mujoco.mjtObj.mjOBJ_BODY, name1=pre + CHASSIS, name2=pre + g.name)
                e.data = [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1] + [0] * (len(e.data) - 11)  # same frame: no offset, torquescale 1
                e.solref = [0.002, 1.0]  # stiff: bolted
                self._weld_spec.append((name, g.name, e.name, prof.breakable.get(g.name, 150.0)))
            elif g.name != CHASSIS:
                self._hinge(pre, g, b, prof)
            for i, p in enumerate(g.parts):
                if g.kind == "weapon":  # teeth: a hull would round them off; sector hulls keep each tooth's face
                    for k, piece in enumerate(sector_pieces(p, g.pivot, g.axis)):
                        self._add_part_geom(b, pre, g, piece, i * 100 + k)
                else:
                    self._add_part_geom(b, pre, g, p, i)
        if self.fixed_motors:  # hazards mode uses contype/conaffinity bits instead, so debris can hit its own robot
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    self.spec.add_exclude(bodyname1=names[i], bodyname2=names[j])
        return name

    def _hinge(self, pre, g, b, prof):
        jn = pre + g.name + "_hinge"
        lifter = prof.lifter and g.name == prof.lifter["group"]
        kw = {}
        if lifter:
            kw = dict(limited=True, range=[min(prof.lifter["down_rad"], prof.lifter["up_rad"]) - 0.05,
                                           max(prof.lifter["down_rad"], prof.lifter["up_rad"]) + 0.05])
        b.add_joint(name=jn, type=mujoco.mjtJoint.mjJNT_HINGE, pos=list(g.pivot), axis=list(g.axis), damping=1e-5,
                    armature=ARMATURE, **kw)
        a = self.spec.add_actuator(name=pre + g.name + "_motor", target=jn, trntype=mujoco.mjtTrn.mjTRN_JOINT)
        a.gaintype = mujoco.mjtGain.mjGAIN_FIXED
        a.biastype = mujoco.mjtBias.mjBIAS_AFFINE
        if lifter:  # position servo
            kp, kd = 2.0, 0.02
            a.gainprm[0] = kp
            a.biasprm[1], a.biasprm[2] = -kp, -kd
            tq = prof.lifter["torque_Nm"]
            self.lifter_joint[pre[:-1]] = jn
        elif self.fixed_motors:
            kv = 0.004 if g.kind == "weapon" else 0.01
            a.gainprm[0] = kv
            a.biasprm[2] = -kv
            tq = prof.weapon_torque if g.kind == "weapon" else prof.drive_torque
        else:  # torque actuator; robot/fight/physics.py motor model sets ctrl = torque
            from . import physics

            a.gainprm[0] = 1.0
            tq = 10.0
            pl = self.plant.setdefault(pre[:-1], {"battery": physics.battery(prof.raw), "motors": {}, "duty": {}})
            pl["motors"][g.name] = (physics.weapon_motor(prof.raw, g.name) if g.kind == "weapon"
                                    else physics.drive_motor(prof.raw, g.name))
            pl["duty"][g.name] = 0.0
        a.forcerange = [-tq, tq]
        a.forcelimited = True

    CONTACT_TC = 3e-4  # contact time constant (s): printed/metal impacts last ~0.1-0.5 ms; MuJoCo's 20 ms default is a pillow

    def compile(self):
        tc = max(self.CONTACT_TC, 2.5 * self.timestep)
        blade = {}
        for r, prof in self.profiles.items():
            wg = self.robots[r].weapon
            if wg is not None:  # blade flex: a thin disc/bar gives a little on impact -> longer, softer contact
                blade[f"{r}/"] = (wg, max(tc, float((prof.raw.get("weapon") or {}).get("blade_tc", 4e-4))))
        for g in self.spec.geoms:
            # damping ratio < 1 = some bounce: printed parts / polycarbonate walls rebound (restitution ~0.3-0.5)
            g.solref = [tc, 0.5]
            for pre, (wg, btc) in blade.items():
                if any(g.name.startswith(pre + p.id + "_") for p in wg.parts):
                    g.solref = [btc, 0.5]
        super().compile()
        if not self.fixed_motors:  # own-robot geoms never collide; robots hit the world, each other and (later) debris
            bits = {r: 1 << (i + 1) for i, r in enumerate(self.robots)}
            for gi in range(self.m.ngeom):
                r = self.m.geom(gi).name.split("/")[0]
                if r in bits:
                    self.m.geom_contype[gi], self.m.geom_conaffinity[gi] = bits[r], 0xFFFF & ~bits[r]
                else:
                    self.m.geom_contype[gi], self.m.geom_conaffinity[gi] = 1, 0xFFFF
        self.welds = [Weld(r, p, self.m.equality(n).id, bn) for r, p, n, bn in self._weld_spec]
        return self

    # ---- control ------------------------------------------------------
    def drive(self, robot, left, right, forward=None):
        prof = self.profiles[robot]
        vmax = prof.drive_max
        left, right = (max(-vmax, min(vmax, v)) for v in (left, right))
        super().drive(robot, left, right, tuple(prof.forward))
        pl = self.plant.get(robot)
        if pl:  # the brain's wheel speeds become throttle (duty), like an RC transmitter stick
            for g in self.robots[robot].wheels:
                pl["duty"][g.name] = float(self.d.ctrl[self._act(robot, g.name)]) / vmax
        return self

    def spin_weapon(self, robot, omega):
        pl = self.plant.get(robot)
        g = self.robots[robot].weapon
        if pl and g is not None:
            # throttle set so the no-load speed on a full pack is the declared rpm (drivers rarely run 100 %); the speed
            # then really sags with the battery and drops on every hit
            mot = pl["motors"][g.name]
            pl["duty"][g.name] = max(-1.0, min(1.0, omega * mot.ke / pl["battery"].ocv())) if omega else 0.0
            return self
        return super().spin_weapon(robot, omega)

    def step_plant(self, dt):
        """Motor curves + battery sag + heating: set every driven hinge's torque from throttle, battery and speed."""
        for robot, pl in self.plant.items():
            bat = pl["battery"]
            i_tot = 0.0
            for gname, mot in pl["motors"].items():
                j = self.m.joint(f"{robot}/{gname}_hinge")
                om = float(self.d.qvel[j.dofadr[0]])
                tq = mot.torque(pl["duty"][gname], bat.v, om)
                self.d.ctrl[self._act(robot, gname)] = tq
                i_tot += abs(pl["duty"][gname] * mot.i)
                mot.heat(dt)
            bat.update(i_tot, dt)

    def lift(self, robot, angle):
        model = self.robots[robot]
        lf = self.profiles[robot].lifter
        g = lf["group"] if lf else None
        if g and model.group(g) is not None:
            self.d.ctrl[self._act(robot, g)] = angle

    def lifter_angle(self, robot):
        jn = self.lifter_joint.get(robot)
        return float(self.d.qpos[self.m.joint(jn).qposadr[0]]) if jn else 0.0

    def weapon_omega(self, robot):
        g = self.robots[robot].weapon
        if g is None:
            return 0.0
        j = self.m.joint(f"{robot}/{g.name}_hinge")
        return float(self.d.qvel[j.dofadr[0]])

    # ---- stepping with damage -----------------------------------------
    def step_damage(self):
        mujoco.mj_step(self.m, self.d)
        d = self.d
        if not self.welds:
            return []
        eqf = {}
        typ = d.efc_type[: d.nefc]
        sel = np.nonzero(typ == mujoco.mjtConstraint.mjCNSTR_EQUALITY)[0]
        for i in sel:
            k = int(d.efc_id[i])
            eqf.setdefault(k, []).append(float(d.efc_force[i]))
        broke = []
        for w in self.welds:
            if w.broken_at is not None:
                continue
            f = eqf.get(w.eq)
            if not f:
                continue
            fn = float(np.linalg.norm(f[:3]))
            w.peak_n = max(w.peak_n, fn)
            if fn > w.break_n:
                d.eq_active[w.eq] = 0
                w.broken_at = float(d.time)
                broke.append(w)
                self.events.append((float(d.time), "break", w.robot, w.part, round(fn, 1)))
        return broke

    def tilt(self, robot):
        return self.up_tilt_deg(robot)

    def yaw_rate(self, robot):
        j = self.m.joint(f"{robot}/free")
        return float(self.d.qvel[j.dofadr[0] + 5])

    def vel_xy(self, robot):
        j = self.m.joint(f"{robot}/free")
        return np.array(self.d.qvel[j.dofadr[0]:j.dofadr[0] + 2])

    def frame(self, robot):
        """(xy position, heading of the robot's forward axis in world, R) of a robot's chassis."""
        x, R = self.pose(robot)
        f = R @ np.array([*self.profiles[robot].forward, 0.0])
        c = self.com(robot)
        return c[:2], math.atan2(f[1], f[0]), R


def _basis(axis):
    a = np.asarray(axis, float) / np.linalg.norm(axis)
    u = np.cross(a, [1.0, 0, 0] if abs(a[0]) < 0.9 else [0, 1.0, 0])
    u /= np.linalg.norm(u)
    return a, u, np.cross(a, u)


def wobble_params(prof):
    from .wobble import DEFAULTS

    w = dict((prof.raw.get("weapon") or {}))
    return {k: float(w.get(k, v)) for k, v in DEFAULTS.items()}


def sector_pieces(p, pivot, axis, n=12):
    """Split a weapon part's hull vertices into n angular sectors about the spin axis (half-sector overlap), so a tooth that
    sticks out of the hull keeps a flat leading face: the hull of a toothed disc is a round cam with no bite."""
    from dataclasses import replace

    v = p.verts
    a = np.asarray(axis, float)
    u = np.cross(a, [1.0, 0, 0] if abs(a[0]) < 0.9 else [0, 1.0, 0])
    u /= np.linalg.norm(u)
    w = np.cross(a, u)
    q = v - pivot
    r = np.linalg.norm(q - np.outer(q @ a, a), axis=1)
    if r.max() < 0.008 or len(v) < 12:
        return [p]
    ang = np.arctan2(q @ w, q @ u)
    out = []
    for k in range(n):
        c = -math.pi + (k + 0.5) * 2 * math.pi / n
        dlt = np.abs((ang - c + math.pi) % (2 * math.pi) - math.pi)
        sel = dlt <= 0.75 * 2 * math.pi / n
        # keep the hub too so each piece is a solid wedge from the axis out
        hub = pivot + np.outer(q[sel] @ a, a)
        pts = np.vstack([v[sel], hub])
        if len(pts) >= 4 and np.linalg.matrix_rank(pts - pts.mean(0), tol=1e-6) == 3:
            out.append(replace(p, id=f"{p.id}_s{k}", verts=pts))
    return out or [p]


def _prep(model: RobotModel, prof: Profile) -> RobotModel:
    """Copy of the model with breakable parts split off the chassis as 'loose' groups, lifter lock groups merged in."""
    groups = []
    chassis = None
    for g in model.groups:
        if g.name == CHASSIS:
            chassis = Group(CHASSIS, "chassis", list(g.parts))
            groups.append(chassis)
    lock = set(prof.lifter.get("lock", [])) if prof.lifter else set()
    for g in model.groups:
        if g.name == CHASSIS:
            continue
        if g.name in lock or (g.kind == "other" and not (prof.lifter and g.name == prof.lifter["group"])):
            chassis.parts.extend(g.parts)  # passive linkage parts ride on the chassis
            continue
        groups.append(g)
    keep = []
    for p in chassis.parts:
        if p.id in prof.breakable and p.mass > 2e-4:
            groups.append(Group(p.id, "loose", [p]))
        else:
            keep.append(p)
    chassis.parts = keep
    return RobotModel(model.name, groups, model.skipped)
