"""Backend-neutral rigid-body description of a robot, extracted from the verifier's World.

Pure numpy (no physics engine): parts are grouped into rigid groups (chassis, each wheel, the weapon), each group
gets mass, centre of mass and an inertia tensor, plus an optional hinge (world-frame pivot and axis).
SI units (m, kg) throughout; the verifier works in mm and g.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from .. import spec as spec_mod

MM = 1e-3
CHASSIS = "chassis"


@dataclass
class SimPart:
    id: str
    kind: str
    verts: np.ndarray  # world-frame hull vertices, m
    mass: float  # kg
    com: np.ndarray  # m
    inertia: np.ndarray  # 3x3 about own com, kg m^2


@dataclass
class Group:
    name: str
    kind: str  # chassis | wheel | weapon | other
    parts: list = field(default_factory=list)
    pivot: np.ndarray | None = None  # world frame, m
    axis: np.ndarray | None = None  # unit, world frame
    lo: float | None = None
    hi: float | None = None

    @property
    def mass(self) -> float:
        return float(sum(p.mass for p in self.parts))

    @property
    def com(self) -> np.ndarray:
        m = self.mass
        if m <= 0:
            return np.zeros(3)
        return sum(p.mass * p.com for p in self.parts) / m

    @property
    def inertia(self) -> np.ndarray:
        c = self.com
        I = np.zeros((3, 3))
        for p in self.parts:
            d = p.com - c
            I += p.inertia + p.mass * (d @ d * np.eye(3) - np.outer(d, d))
        return I


@dataclass
class RobotModel:
    name: str
    groups: list
    skipped: list = field(default_factory=list)  # (part id, reason)

    @property
    def mass(self) -> float:
        return sum(g.mass for g in self.groups)

    def group(self, name):
        return next((g for g in self.groups if g.name == name), None)

    @property
    def wheels(self):
        return [g for g in self.groups if g.kind == "wheel"]

    @property
    def weapon(self):
        return next((g for g in self.groups if g.kind == "weapon"), None)

    def bounds(self):
        v = np.vstack([p.verts for g in self.groups for p in g.parts])
        return v.min(axis=0), v.max(axis=0)


def part_inertia(mesh, mass_kg):
    """Inertia tensor about the mesh centroid for a uniform solid of the given mass (falls back to the hull)."""
    m = mesh if mesh.is_watertight and mesh.volume > 1e-9 else mesh.convex_hull
    vol = m.volume  # mm^3
    if vol <= 1e-9:
        return m.centroid * MM, np.zeros((3, 3))
    # trimesh: moment_inertia at unit density, about centre of mass, mm^5
    I = m.moment_inertia * (mass_kg / vol) * MM * MM
    return m.center_mass * MM, I


def wheel_axis(mesh):
    """Symmetry axis of a wheel-like solid: the principal axis with the largest moment of inertia."""
    m = mesh if mesh.is_watertight else mesh.convex_hull
    w, V = np.linalg.eigh(m.moment_inertia)
    return V[:, int(np.argmax(w))] / np.linalg.norm(V[:, int(np.argmax(w))])


def _group_of(p, joint_groups):
    rw = p.rotates_with
    if rw and rw != "fixed" and rw in joint_groups:
        return rw
    if p.fixed:
        return CHASSIS
    return CHASSIS


def extract(world, resolved, name=None) -> RobotModel:
    """Build a RobotModel from a verifier World + Resolved pair (see robot.world)."""
    from ..checks.connections import part_mass_g

    parts = [rp.part for rp in resolved.parts]
    by_id = {b.id: b for b in world.bodies}
    # a rotating group is named by `rotates_with`; its hinge is the jointed part carrying that label
    hinges = {}
    for p in parts:
        if p.joint is not None and p.rotates_with and p.rotates_with != "fixed":
            hinges.setdefault(p.rotates_with, p)
    groups = {CHASSIS: Group(CHASSIS, "chassis")}
    skipped = []
    for rp in resolved.parts:
        p = rp.part
        b = by_id.get(p.id)
        if b is None:
            continue
        mg = part_mass_g(rp, b)
        if mg is None or mg <= 0:
            skipped.append((p.id, "no mass"))
            continue
        gname = _group_of(p, hinges)
        if gname == CHASSIS and p.kind == "wheel" and p.joint is None:
            gname = p.id  # un-jointed wheel: spins about its own symmetry axis
            if gname not in groups:
                ax = wheel_axis(b.mesh)
                groups[gname] = Group(gname, "wheel", pivot=b.mesh.center_mass * MM, axis=ax)
        if gname not in groups:
            hp = hinges[gname]
            hb = by_id[hp.id]
            j = hp.joint
            par = by_id.get(hp.parent) if hp.parent else None
            Mp = par.M if par is not None else np.eye(4)
            axis = Mp[:3, :3] @ np.asarray(j.axis, float)
            axis = axis / np.linalg.norm(axis)
            piv = (Mp @ np.append(np.asarray(j.pivot, float), 1.0))[:3] * MM
            kinds = {q.kind for q in parts if hinges.get(q.rotates_with) is hp}
            kind = "weapon" if "weapon" in kinds else "wheel" if "wheel" in kinds or "tyre" in kinds else "other"
            groups[gname] = Group(gname, kind, pivot=piv, axis=axis)
        com, I = part_inertia(b.mesh, mg * 1e-3)
        verts = np.asarray(b.mesh.convex_hull.vertices, float) * MM
        groups[gname].parts.append(SimPart(p.id, p.kind, verts, mg * 1e-3, com, I))
    return RobotModel(name or resolved.spec.name or "robot", [g for g in groups.values() if g.parts], skipped)


def load(path, fast=True) -> RobotModel:
    from .. import world as world_mod

    sp = spec_mod.load(path)
    r = world_mod.resolve(sp, fast=fast)
    w = world_mod.World.build(r)
    return extract(w, r)
