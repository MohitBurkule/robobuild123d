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
import os

import numpy as np
import trimesh

from . import cache, catalog, geom, profile, shapes, xform
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
    from . import progress
    tess = geom.FAST if fast else geom.FINE
    prof = profile.named(spec.profile)
    parts, errors = [], []
    _prebuild(spec, tess)
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
            progress.log(f"part {p.id} FAILED: {type(e).__name__}: {e}")
        else:
            progress.log(f"part {p.id} built")
        parts.append(RPart(p, shape, cat, g))
    return Resolved(spec, prof, parts, errors, fast)


BUILD_TIMEOUT_S = float(os.environ.get("ROBOT_BUILD_TIMEOUT") or 600)
JOBS = int(os.environ.get("ROBOT_JOBS") or 0) or (os.cpu_count() or 1)


def _part_shape(p):
    if p.catalog:
        cat = catalog.find(p.catalog)
        return cat.shape if cat else None
    if p.model:
        return {"type": "model", "file": p.model, "params": p.params or {}}
    return p.shape


def _build_one(args):
    shape, base_dir, tess = args
    try:
        geom.geom_for(shape, base_dir, tess)
        return None
    except Exception as e:  # noqa: BLE001 - the serial pass reports it as a finding
        return f"{type(e).__name__}: {e}"


def _prebuild(spec, tess):
    """Build every uncached part solid concurrently (one process per part); results land in the geometry cache."""
    if JOBS <= 1 or not cache.enabled():
        return
    todo, seen = [], set()
    for p in spec.parts:
        sh = _part_shape(p)
        if sh is None:
            continue
        try:
            shapes.validate(sh)
        except shapes.ShapeError:
            continue
        k = geom.key_for(sh, spec.base_dir, tess)
        if k in seen or geom.cached(k):
            continue
        seen.add(k)
        todo.append((sh, spec.base_dir, tess))
    if len(todo) < 2:
        return
    import multiprocessing as mp
    from concurrent.futures import ProcessPoolExecutor

    n = min(JOBS, len(todo))
    print(f"building {len(todo)} changed part solids on {n} processes", flush=True)
    # spawn, not fork: forking a process that holds OCP / BLAS threads can deadlock the children.
    ex = ProcessPoolExecutor(n, mp_context=mp.get_context("spawn"))
    try:
        list(ex.map(_build_one, todo, timeout=BUILD_TIMEOUT_S))
        ex.shutdown(wait=True)
    except Exception as e:  # noqa: BLE001 - timeout or worker crash: the serial pass builds what is missing
        print(f"parallel build failed ({type(e).__name__}); building the rest serially", flush=True)
        for pr in list((getattr(ex, "_processes", None) or {}).values()):
            pr.terminate()
        ex.shutdown(wait=False, cancel_futures=True)


def _contains(mesh, Q):
    """mesh.contains with a fixed seed: trimesh re-casts ambiguous rays along *random* directions, so without this the
    answer depends on whatever ran before and cached and uncached runs could differ. Older trimesh draws from the
    global numpy RNG; trimesh >= 4.6 draws from `trimesh.util.random_generator()`, a shared Generator seeded from OS
    entropy (not reproducible even between two runs), so both are pinned here."""
    import trimesh.util as tu

    st = np.random.get_state()
    np.random.seed(12345)
    orig = getattr(tu, "random_generator", None)
    if orig is not None:
        rng = np.random.default_rng(12345)
        tu.random_generator = lambda seed=None: rng if seed is None else orig(seed)
    try:
        return mesh.contains(Q)
    finally:
        np.random.set_state(st)
        if orig is not None:
            tu.random_generator = orig


def csk_dims(d):
    """(head diameter, head depth) of an ISO 10642 countersunk screw (90 deg), by thread diameter."""
    return 2.2 * d, 0.6 * d


def button_dims(d):
    """(head diameter, head height) of an ISO 7380 button-head screw (M3: 5.7 x 1.65, 2 mm key)."""
    return 1.9 * d, 0.55 * d


def fastener_shape(d, length, head=None):
    """Screw solid in its own frame: `at` is the origin, the shank runs along +z. A socket/button head sits behind `at`
    (-z); a countersunk head is a 90 deg cone *inside* the part, flush with the surface at `at` (ISO length is overall)."""
    shank = catalog.at(catalog.cyl(d / 2, length), 0, 0, length / 2)
    if head == "countersunk":
        dk, k = csk_dims(d)
        cone = {"type": "revolve", "profile": [[0.0, 0.0], [dk / 2, 0.0], [d / 2, k], [0.0, k]]}
        return catalog.union([cone, shank])
    dk, k, _ = catalog.screw_dims(d)
    if head == "button":
        dk, k = button_dims(d)
    hd = catalog.at(catalog.cyl(dk / 2, k), 0, 0, -k / 2)
    return catalog.union([hd, shank])


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
            Q = P[m]
            out[m] = cache.memo("inside", ("in", cache.body_sig(self), Q), lambda: _contains(self.mesh, Q))
        return out

    def distance(self, P) -> np.ndarray:
        P = np.atleast_2d(np.asarray(P, float))
        return cache.memo("distance", ("dist", cache.body_sig(self), P),
                          lambda: trimesh.proximity.closest_point(self.mesh, P)[1])

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
            g = geom.geom_for(fastener_shape(*dl, head=f.head if f.head in ("countersunk", "button") else None), None, tess)
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
            # Enclosed parts travel with their enclosure: a side pod moves outward and takes its wheels, tyres,
            # hubs, pulleys, belts and axles with it so they stay inside it in the exploded view.
            orig = {b.id: b for b in w.bodies}
            pods = [b for b in w.bodies if "pod" in b.id and not b.fastener and not b.is_wire]
            ride = ("wheel", "tyre", "pulley", "belt", "pin", "wheel_hub", "hub")
            for i, b in enumerate(out):
                src = orig[b.id]
                if src in pods:
                    out[i] = src.moved(np.array([16.0 if src.center[0] >= 0 else -16.0, 0, 0]) * amount)
                    continue
                if src.kind not in ride or src.fastener:
                    continue
                for pb in pods:
                    lo, hi = pb.aabb
                    if np.all(src.center >= lo) and np.all(src.center <= hi):
                        out[i] = src.moved(np.array([16.0 if pb.center[0] >= 0 else -16.0, 0, 0]) * amount)
                        break
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
