"""MuJoCo backend: builds one MjSpec from a Scene and any number of RobotModels, then steps it.

Each rigid group becomes a body with explicit mass/inertia (from the verifier's per-part masses), collision geoms are
the convex hulls of the parts, wheels and the weapon are hinges with velocity servos (torque limited).
Geoms of one robot never collide with each other; robots collide with props, the floor, walls and each other.
"""

from __future__ import annotations

import math

import mujoco
import numpy as np

from .model import CHASSIS, RobotModel
from .scene import Placement, Scene

WHEEL_KV = 0.01  # N m per rad/s: servo stiffness of the wheel velocity actuator
WEAPON_KV = 0.005
ARMATURE = 2e-5  # kg m^2 reflected rotor + gearbox inertia on each driven hinge


def _rz(yaw):
    c, s = math.cos(yaw), math.sin(yaw)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def _quat(R):
    q = np.zeros(4)
    mujoco.mju_mat2Quat(q, np.asarray(R, float).reshape(9))
    return q


class Sim:
    def __init__(self, scene: Scene | None = None, timestep=0.001):
        self.scene = scene or Scene()
        self.timestep = timestep
        self.robots: dict[str, RobotModel] = {}
        self.place: dict[str, Placement] = {}
        self._build_scene()
        self.m = self.d = None

    # ---- construction -------------------------------------------------
    def _build_scene(self):
        s = mujoco.MjSpec()
        s.option.timestep = self.timestep
        s.option.integrator = mujoco.mjtIntegrator.mjINT_IMPLICITFAST  # stable velocity servos on tiny wheel inertias
        s.option.gravity = [0, 0, -self.scene.gravity]
        self.spec = s
        w = s.worldbody
        w.add_geom(name="floor", type=mujoco.mjtGeom.mjGEOM_PLANE, size=[2, 2, 0.1],
                   friction=[self.scene.floor_friction, 0.005, 0.0001], rgba=[0.25, 0.27, 0.3, 1])
        h = self.scene.arena_half
        if h:
            t, wh = 0.01, self.scene.wall_height
            for nm, pos, size in (("wall_n", (0, h + t, wh / 2), (h + 2 * t, t, wh / 2)),
                                  ("wall_s", (0, -h - t, wh / 2), (h + 2 * t, t, wh / 2)),
                                  ("wall_e", (h + t, 0, wh / 2), (t, h, wh / 2)),
                                  ("wall_w", (-h - t, 0, wh / 2), (t, h, wh / 2))):
                w.add_geom(name=nm, type=mujoco.mjtGeom.mjGEOM_BOX, size=list(size), pos=list(pos), rgba=[0.5, 0.5, 0.55, 0.4])
        for p in self.scene.props:
            self._add_prop(p)

    def _add_prop(self, p):
        kind = {"box": mujoco.mjtGeom.mjGEOM_BOX, "sphere": mujoco.mjtGeom.mjGEOM_SPHERE,
                "cylinder": mujoco.mjtGeom.mjGEOM_CYLINDER}[p.shape]
        size = list(p.size) + [0.0] * (3 - len(p.size))
        R = _euler_xyz(np.radians(p.euler_deg))
        parent = self.spec.worldbody
        if p.mass is not None:
            parent = parent.add_body(name=p.name, pos=list(p.pos), quat=_quat(R))
            parent.add_freejoint()
            parent.add_geom(name=p.name + "_g", type=kind, size=size, mass=p.mass, friction=[p.friction, 0.005, 0.0001], rgba=list(p.rgba))
        else:
            parent.add_geom(name=p.name, type=kind, size=size, pos=list(p.pos), quat=_quat(R), friction=[p.friction, 0.005, 0.0001], rgba=list(p.rgba))

    def add_robot(self, model: RobotModel, placement: Placement | None = None, name: str | None = None):
        name = name or (placement.name if placement else model.name)
        name = name.replace(' ', '_')
        pl = placement or Placement(name)
        self.robots[name] = model
        self.place[name] = pl
        lo, hi = model.bounds()
        ctr = np.array([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0.0])
        R = _rz(math.radians(pl.yaw_deg))
        t = np.array([pl.xy[0], pl.xy[1], pl.z_clear - lo[2]]) - R @ ctr  # robot frame -> world; ctr to xy, lowest point to floor
        pre = name + "/"
        chassis = self.spec.worldbody.add_body(name=pre + CHASSIS, pos=list(t), quat=_quat(R))
        chassis.add_freejoint(name=pre + "free")
        bodies = {}
        for g in model.groups:
            b = chassis if g.name == CHASSIS else chassis.add_body(name=pre + g.name)
            bodies[g.name] = b
            b.explicitinertial = True
            b.mass = g.mass
            b.ipos = list(g.com)
            I = g.inertia
            b.fullinertia = [I[0, 0], I[1, 1], I[2, 2], I[0, 1], I[0, 2], I[1, 2]]
            if g.name != CHASSIS:
                ax = g.axis
                b.add_joint(name=pre + g.name + "_hinge", type=mujoco.mjtJoint.mjJNT_HINGE, pos=list(g.pivot), axis=list(ax),
                            damping=1e-5, armature=ARMATURE)
                kv = WEAPON_KV if g.kind == "weapon" else WHEEL_KV
                a = self.spec.add_actuator(name=pre + g.name + "_motor", target=pre + g.name + "_hinge",
                                           trntype=mujoco.mjtTrn.mjTRN_JOINT)
                a.gaintype = mujoco.mjtGain.mjGAIN_FIXED
                a.biastype = mujoco.mjtBias.mjBIAS_AFFINE
                a.gainprm[0] = kv
                a.biasprm[2] = -kv  # force = kv * (ctrl - vel)
                a.forcerange = [-0.05, 0.05]
                a.forcelimited = True
            for i, p in enumerate(g.parts):
                self._add_part_geom(b, pre, g, p, i)
        names = [pre + g.name for g in model.groups]
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                self.spec.add_exclude(bodyname1=names[i], bodyname2=names[j])
        return name

    def _add_part_geom(self, body, pre, g, p, i):
        mname = f"{pre}{p.id}_mesh"
        try:
            self.spec.add_mesh(name=mname, uservert=p.verts.reshape(-1).tolist())
            fr = 1.2 if p.kind in ("wheel", "tyre") else 0.4
            body.add_geom(name=f"{pre}{p.id}_g{i}", type=mujoco.mjtGeom.mjGEOM_MESH, meshname=mname, mass=0.0,
                          friction=[fr, 0.005, 0.0001], rgba=_rgba(p.kind))
        except Exception:  # noqa: BLE001 - degenerate hull: fall back to its bounding box
            lo, hi = p.verts.min(axis=0), p.verts.max(axis=0)
            body.add_geom(name=f"{pre}{p.id}_g{i}", type=mujoco.mjtGeom.mjGEOM_BOX, size=list(np.maximum((hi - lo) / 2, 1e-4)),
                          pos=list((lo + hi) / 2), mass=0.0, rgba=_rgba(p.kind))

    # ---- running ------------------------------------------------------
    def compile(self):
        self.m = self.spec.compile()
        self.d = mujoco.MjData(self.m)
        mujoco.mj_forward(self.m, self.d)
        return self

    def _act(self, robot, group):
        return self.m.actuator(f"{robot}/{group}_motor").id

    def drive(self, robot, left, right, forward=(0.0, 1.0)):
        """Set wheel speeds (rad/s, positive = forward). Wheels are split left/right by their position along the lateral axis."""
        model = self.robots[robot]
        f = np.array([forward[0], forward[1], 0.0])
        f /= np.linalg.norm(f)
        lat = np.cross([0, 0, 1.0], f)  # points to the robot's left
        for g in model.wheels:
            side = float(np.dot(g.com, lat))
            v = left if side > 0 else right
            # no-slip rolling: centre velocity = omega * r * (axis x up), so spin sign follows (axis x up) . forward
            sgn = 1.0 if np.dot(np.cross(g.axis, [0, 0, 1.0]), f) > 0 else -1.0
            self.d.ctrl[self._act(robot, g.name)] = sgn * v
        return self

    def spin_weapon(self, robot, omega):
        g = self.robots[robot].weapon
        if g is not None:
            self.d.ctrl[self._act(robot, g.name)] = omega
        return self

    def step(self, seconds):
        for _ in range(int(round(seconds / self.timestep))):
            mujoco.mj_step(self.m, self.d)
        return self

    # ---- queries ------------------------------------------------------
    def pose(self, robot):
        """(position m, rotation matrix) of the chassis body frame in the world."""
        b = self.m.body(f"{robot}/{CHASSIS}").id
        return self.d.xpos[b].copy(), self.d.xmat[b].reshape(3, 3).copy()

    def com(self, robot):
        b = self.m.body(f"{robot}/{CHASSIS}").id
        return self.d.subtree_com[b].copy()

    def up_tilt_deg(self, robot):
        """Angle between the robot's body +z and world up."""
        _, R = self.pose(robot)
        return math.degrees(math.acos(max(-1.0, min(1.0, R[2, 2]))))

    def body_pos(self, name):
        return self.d.xpos[self.m.body(name).id].copy()

    def contacts(self):
        """[(geom a, geom b, force N)] for active contacts."""
        out = []
        f6 = np.zeros(6)
        for i in range(self.d.ncon):
            c = self.d.contact[i]
            mujoco.mj_contactForce(self.m, self.d, i, f6)
            out.append((self.m.geom(c.geom1).name, self.m.geom(c.geom2).name, float(abs(f6[0]))))
        return out

    def render(self, path, lookat=(0, 0, 0.03), distance=0.45, azimuth=135, elevation=-25, size=(640, 480)):
        import imageio.v2 as imageio  # optional dep

        r = mujoco.Renderer(self.m, size[1], size[0])
        cam = mujoco.MjvCamera()
        cam.lookat[:] = lookat
        cam.distance, cam.azimuth, cam.elevation = distance, azimuth, elevation
        r.update_scene(self.d, cam)
        img = r.render()
        r.close()
        imageio.imwrite(path, img)
        return path


def _euler_xyz(a):
    cx, sx, cy, sy, cz, sz = math.cos(a[0]), math.sin(a[0]), math.cos(a[1]), math.sin(a[1]), math.cos(a[2]), math.sin(a[2])
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def _rgba(kind):
    return {"wheel": [0.1, 0.1, 0.1, 1], "tyre": [0.1, 0.1, 0.1, 1], "weapon": [0.85, 0.2, 0.2, 1], "armor": [0.7, 0.7, 0.75, 1],
            "wedge": [0.8, 0.8, 0.3, 1]}.get(kind, [0.55, 0.6, 0.7, 1])
