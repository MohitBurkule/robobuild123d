"""Resolved geometry: catalog parts expanded, joints applied, fasteners turned into solids, every body placed in the world.

API used by the checks (all coordinates world mm, numpy arrays):
  resolve(spec, fast=False) -> Resolved            parts with geometry, load errors
  World.build(r, joint_values) / World.start(r)
  world.bodies[i]: Body(id, kind, part_idx, fastener, M (4x4), color, geom)
      .mesh (trimesh, world) .manifold (manifold3d, world) .aabb (2x3) .center
      .inside(P) -> bool[]   .distance(P) -> float[] (unsigned)   .sdf(P) (negative inside; exact, slow, few points)
      .surface(h) -> (points, normals)   .moved(shift) -> Body
  world.index(id), world.body(id), world.bounds(), world.port(r, "part.port")
  world.with_routes(routes), world.with_assembly(steps), world.exploded(amount)
"""

from __future__ import annotations

import copy

import numpy as np
import trimesh

from . import catalog, geom, profile, shapes, xform
from .spec import Spec

DEFAULT_COLORS = {
    "structure": "#2b2e34", "armor": "#444850", "wedge": "#ff6a1a", "motor": "#9aa0a6", "weapon_motor": "#5a5e66",
    "wheel": "#25282c", "battery": "#2a9d8f", "esc": "#e76f51", "receiver": "#ff9800", "servo": "#4a4e57",
    "switch": "#c02020", "weapon": "#c8cdd2", "locking_bar": "#ffd100", "plate": "#1c1c1e",
}


def parse_color(s):
    if not isinstance(s, str):
        return None
    h = s.strip().lstrip("#")
    if len(h) != 6:
        return None
    try:
        v = int(h, 16)
    except ValueError:
        return None
    return [(v >> 16) & 255, (v >> 8) & 255, v & 255]


class RPart:
    def __init__(self, part, shape, cat, g):
        self.part = part
        self.shape = shape
        self.cat = cat
        self.geom = g


class Resolved:
    def __init__(self, spec: Spec, prof, parts, load_errors, fast):
        self.spec = spec
        self.profile = prof
        self.parts = parts
        self.load_errors = load_errors
        self.fast = fast


def resolve(spec: Spec, fast: bool = False) -> Resolved:
    tess = geom.FAST if fast else geom.FINE
    prof = profile.named(spec.profile)
    parts, errors = [], []
    for p in spec.parts:
        cat = None
        if p.catalog:
            cat = catalog.find(p.catalog)
            if cat is None:
                errors.append((p.id, f"unknown catalog id `{p.catalog}`"))
        if cat is not None:
            shape = cat.shape
        elif p.model:
            shape = {"type": "model", "file": p.model, "params": p.params or {}}
        elif p.shape is not None:
            shape = p.shape
        else:
            errors.append((p.id, "part has neither `shape`, `model` nor `catalog`"))
            shape = {"type": "box", "size": [0.1, 0.1, 0.1]}
        try:
            shapes.validate(shape)
        except shapes.ShapeError as e:
            errors.append((p.id, f"bad shape: {e}"))
            shape = {"type": "box", "size": [0.1, 0.1, 0.1]}
        try:
            g = geom.geom_for(shape, spec.base_dir, tess)
        except Exception as e:  # noqa: BLE001 - a broken solid is a finding, not a crash
            errors.append((p.id, f"geometry failed: {type(e).__name__}: {e}"))
            shape = {"type": "box", "size": [0.1, 0.1, 0.1]}
            g = geom.geom_for(shape, spec.base_dir, tess)
        parts.append(RPart(p, shape, cat, g))
    return Resolved(spec, prof, parts, errors, fast)


def fastener_shape(d, length):
    dk, k, _ = catalog.screw_dims(d)
    head = catalog.at(catalog.cyl(dk / 2, k), 0, 0, -k / 2)
    shank = catalog.at(catalog.cyl(d / 2, length), 0, 0, length / 2)
    return catalog.union([head, shank])


class Body:
    def __init__(self, id, kind, g, M, color, part_idx=None, fastener=False):
        self.id = id
        self.kind = kind
        self.geom = g
        self.M = np.asarray(M, float)
        self.color = color
        self.part_idx = part_idx
        self.fastener = fastener
        self._mesh = None
        self._man = None
        self._surf = {}

    @property
    def mesh(self) -> trimesh.Trimesh:
        if self._mesh is None:
            m = self.geom.mesh.copy()
            m.apply_transform(self.M)
            self._mesh = m
        return self._mesh

    @property
    def manifold(self):
        if self._man is None:
            self._man = geom.to_manifold(self.mesh)
        return self._man

    @property
    def aabb(self) -> np.ndarray:
        return self.mesh.bounds

    @property
    def center(self) -> np.ndarray:
        return self.aabb.mean(axis=0)

    @property
    def is_wire(self) -> bool:
        return self.id.startswith("wire:")

    def inside(self, P) -> np.ndarray:
        P = np.atleast_2d(np.asarray(P, float))
        out = np.zeros(len(P), bool)
        lo, hi = self.aabb
        m = np.all((P >= lo - 1e-9) & (P <= hi + 1e-9), axis=1)
        if m.any():
            out[m] = self.mesh.contains(P[m])
        return out

    def distance(self, P) -> np.ndarray:
        P = np.atleast_2d(np.asarray(P, float))
        _, d, _ = trimesh.proximity.closest_point(self.mesh, P)
        return d

    def sdf(self, P) -> np.ndarray:
        d = self.distance(P)
        return np.where(self.inside(P), -d, d)

    def surface(self, h: float):
        if h not in self._surf:
            self._surf[h] = geom.sample_surface(self.mesh, h)
        return self._surf[h]

    def moved(self, shift) -> "Body":
        b = Body(self.id, self.kind, self.geom, xform.translation(shift) @ self.M, self.color, self.part_idx, self.fastener)
        return b

    def placed(self, M) -> "Body":
        return Body(self.id, self.kind, self.geom, M, self.color, self.part_idx, self.fastener)


class World:
    def __init__(self, bodies, joints):
        self.bodies = bodies
        self.joints = joints
        self.plan = {}
        self._idx = {b.id: i for i, b in enumerate(bodies)}

    @staticmethod
    def build(r: Resolved, joint_values: dict | None = None) -> "World":
        jv = joint_values or {}
        by_id = {rp.part.id: i for i, rp in enumerate(r.parts)}
        cache = {}
        bodies, joints = [], {}
        for i, rp in enumerate(r.parts):
            M = _world_xf(r, by_id, i, jv, cache, 0)
            j = rp.part.joint
            if j is not None:
                joints[rp.part.id] = jv.get(rp.part.id, r.spec.start_pose.get(rp.part.id, j.default))
            color = parse_color(rp.part.color) or (parse_color(rp.cat.color) if rp.cat else None) or parse_color(
                DEFAULT_COLORS.get(rp.part.kind, "#b0b4ba"))
            bodies.append(Body(rp.part.id, rp.part.kind, rp.geom, M, color, i, False))
        tess = geom.FAST if r.fast else geom.FINE
        for f in r.spec.fasteners:
            dl = catalog.parse_designation(f.designation)
            if not dl:
                continue
            g = geom.geom_for(fastener_shape(*dl), None, tess)
            M = xform.make(xform.align_z_to(f.dir), f.at)
            bodies.append(Body(f.id, "other", g, M, [0xcc, 0xcc, 0xd0], None, True))
        return World(bodies, joints)

    @staticmethod
    def start(r: Resolved) -> "World":
        return World.build(r, {})

    def index(self, bid):
        return self._idx.get(bid)

    def body(self, bid):
        i = self.index(bid)
        return None if i is None else self.bodies[i]

    def bounds(self, skip_wires=False) -> np.ndarray:
        bs = [b.aabb for b in self.bodies if not (skip_wires and b.is_wire)]
        return np.array([np.min([b[0] for b in bs], axis=0), np.max([b[1] for b in bs], axis=0)])

    def port(self, r: Resolved, name: str):
        if "." not in name:
            return None
        pid, port = name.split(".", 1)
        b = self.body(pid)
        if b is None or b.part_idx is None:
            return None
        rp = r.parts[b.part_idx]
        local = rp.part.ports.get(port) if rp.part.ports else None
        if local is None and rp.cat is not None:
            local = rp.cat.ports.get(port)
        if local is None:
            return None
        return xform.apply(b.M, local)

    def copy(self) -> "World":
        w = World(list(self.bodies), dict(self.joints))
        w.plan = dict(self.plan)
        return w

    def with_routes(self, routes, tess=None) -> "World":
        w = self.copy()
        colors = {"power": [0xd0, 0x20, 0x20], "motor": [0xe8, 0xb0, 0x20]}
        for rt in routes:
            g = route_geom(rt)
            if g is None:
                continue
            w.bodies.append(Body(f"wire:{rt.id}", "other", g, np.eye(4), colors.get(rt.kind, [0x30, 0x80, 0xe0])))
        w._idx = {b.id: i for i, b in enumerate(w.bodies)}
        return w

    def with_assembly(self, steps) -> "World":
        w = self.copy()
        n = len(steps)
        w.plan = {s.id: (np.asarray(s.dir, float), s.travel_mm + 2.5 * max(n - s.order, 0)) for s in steps}
        return w

    def exploded(self, amount: float = 1.0) -> "World":
        w = self.copy()
        if w.plan:
            out = []
            for b in w.bodies:
                if b.is_wire:
                    continue
                if b.id in w.plan:
                    d, t = w.plan[b.id]
                    b = b.moved(d * min(t + 4, 90) * amount)
                out.append(b)
            w.bodies = out
        else:
            out = []
            for b in w.bodies:
                x = b.M[0, 3]
                d = {"wheel": [16 if x >= 0 else -16, 0, 0], "insert": [0, 0, -12], "nut": [0, 0, -12], "battery": [0, 0, 12],
                     "esc": [0, 0, 12], "receiver": [0, 0, 12], "servo": [0, 0, 12], "switch": [0, 0, 22], "wedge": [0, 9, -4],
                     "weapon": [0, 0, 26], "locking_bar": [0, 0, 26], "motor": [6 if x >= 0 else -6, 0, 4],
                     "weapon_motor": [6 if x >= 0 else -6, 0, 4]}.get(b.kind, [0, 0, 0])
                if b.fastener:
                    d = [0, 0, 42]
                elif "top" in b.id:
                    d = [0, 0, 30]
                out.append(b.moved(np.asarray(d, float) * amount))
            w.bodies = out
        w._idx = {b.id: i for i, b in enumerate(w.bodies)}
        return w


def route_geom(rt):
    """Tube mesh for a routed wire (world frame); B-rep built lazily only for STEP export."""
    pts = np.asarray(rt.points, float)
    if len(pts) < 2:
        return None
    r = rt.od_mm / 2
    parts = [trimesh.creation.icosphere(subdivisions=1, radius=r).apply_translation(p) for p in pts]
    for a, b in zip(pts, pts[1:]):
        L = float(np.linalg.norm(b - a))
        if L < 1e-6:
            continue
        c = trimesh.creation.cylinder(radius=r, height=L, sections=12)
        c.apply_translation([0, 0, L / 2])
        c.apply_transform(xform.make(xform.align_z_to(b - a), a))
        parts.append(c)
    mesh = trimesh.util.concatenate(parts)
    try:
        m = geom.from_manifold(geom.to_manifold(parts[0]).__class__.batch_boolean([geom.to_manifold(p) for p in parts], geom.mf.OpType.Add))
        if len(m.faces):
            mesh = m
    except Exception:  # noqa: BLE001
        pass
    g = geom.PartGeom("wire", mesh.vertices, mesh.faces, mesh.volume, mesh.center_mass, np.zeros((3, 3)), None)
    g.route = copy.copy(rt)
    return g


def _world_xf(r, by_id, i, jv, cache, depth):
    if i in cache:
        return cache[i]
    rp = r.parts[i]
    own = xform.pose(rp.part.at, rp.part.rot)
    local = own
    j = rp.part.joint
    if j is not None:
        v = jv.get(rp.part.id, r.spec.start_pose.get(rp.part.id, j.default))
        axis = np.asarray(j.axis, float)
        if np.linalg.norm(axis) < 1e-9:
            axis = np.array([1.0, 0, 0])
        if j.kind == "prismatic":
            jx = xform.translation(xform.norm(axis) * float(v))
        else:
            jx = xform.rotation_about(j.pivot, axis, float(v))
        local = jx @ own
    pi = by_id.get(rp.part.parent) if rp.part.parent else None
    if pi is not None and pi != i and depth < 16:
        M = _world_xf(r, by_id, pi, jv, cache, depth + 1) @ local
    else:
        M = local
    cache[i] = M
    return M
