"""Measurements between bodies, on exact mesh booleans (manifold3d) and mesh queries (trimesh)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import trimesh

from . import geom


@dataclass
class Overlap:
    depth: float  # deepest penetration in mm (0 when touching or apart): radius of the largest ball inside both
    at: np.ndarray
    volume: float  # overlapping volume mm3


def aabb_overlap(a, b, margin=0.0) -> bool:
    return bool(np.all(a[0] <= b[1] + margin) and np.all(a[1] + margin >= b[0]))


def overlap(a, b, shift=None, cap=None) -> Overlap | None:
    """Overlap of body `a` (moved by `shift`) with body `b`. `cap`: only need to know whether depth exceeds cap."""
    shift = np.zeros(3) if shift is None else np.asarray(shift, float)
    abox = a.aabb + shift
    if not aabb_overlap(abox, b.aabb):
        return None
    ma = a.manifold.translate(tuple(float(x) for x in shift)) if np.any(shift) else a.manifold
    inter = ma ^ b.manifold
    vol = float(inter.volume())
    lo = np.maximum(abox[0], b.aabb[0])
    hi = np.minimum(abox[1], b.aabb[1])
    if vol < 1e-7:
        return Overlap(0.0, (lo + hi) / 2, max(vol, 0.0))
    depth, where = geom.inscribed_depth(inter, cap)
    return Overlap(depth, where if where is not None else (lo + hi) / 2, vol)


def overlap_exceeds(a, b, thresh, shift=None) -> bool:
    o = overlap(a, b, shift, cap=thresh)
    return bool(o and o.depth > thresh)


def min_gap(a, b, search: float = 5.0) -> float:
    """Smallest distance between the surfaces (0 when touching or overlapping), capped at `search`."""
    if not aabb_overlap(a.aabb, b.aabb, search):
        return float("inf")
    g = float(a.manifold.min_gap(b.manifold, search))
    return g if g < search else float("inf")


def lowest_point(body) -> np.ndarray:
    v = body.mesh.vertices
    z = v[:, 2].min()
    sel = v[v[:, 2] <= z + 1e-3]
    return np.array([sel[:, 0].mean(), sel[:, 1].mean(), z])


def highest_point(body) -> np.ndarray:
    v = body.mesh.vertices
    z = v[:, 2].max()
    sel = v[v[:, 2] >= z - 1e-3]
    return np.array([sel[:, 0].mean(), sel[:, 1].mean(), z])


def inside_any(bodies, P, skip=lambda b: False) -> np.ndarray:
    P = np.atleast_2d(np.asarray(P, float))
    out = np.zeros(len(P), bool)
    for b in bodies:
        if skip(b):
            continue
        rest = ~out
        if rest.any():
            out[rest] |= b.inside(P[rest])
    return out


class Scene:
    """Ray casts against a set of bodies."""

    def __init__(self, bodies):
        self.bodies = list(bodies)
        meshes = [b.mesh for b in self.bodies]
        self.mesh = trimesh.util.concatenate(meshes) if meshes else None
        self.owner = np.concatenate([np.full(len(m.faces), i) for i, m in enumerate(meshes)]) if meshes else np.zeros(0, int)

    def first_hit(self, origins, dirs, max_dist=np.inf):
        """Distance to the first surface hit along each ray (inf when none) and the body index hit (-1)."""
        origins = np.atleast_2d(np.asarray(origins, float))
        dirs = np.atleast_2d(np.asarray(dirs, float))
        n = len(origins)
        dist = np.full(n, np.inf)
        who = np.full(n, -1)
        if self.mesh is None or n == 0:
            return dist, who
        locs, ray_i, tri_i = self.mesh.ray.intersects_location(origins, dirs, multiple_hits=True)
        if len(ray_i):
            d = np.einsum("ij,ij->i", locs - origins[ray_i], dirs[ray_i])
            ok = d > 1e-7
            for k in np.nonzero(ok)[0]:
                ri = ray_i[k]
                if d[k] < dist[ri]:
                    dist[ri] = d[k]
                    who[ri] = self.owner[tri_i[k]]
        dist[dist > max_dist] = np.inf
        return dist, who


def footprint_mm(points: np.ndarray) -> float:
    """Smallest square, over rotations about Z in 1 degree steps, that holds the XY points."""
    P = np.asarray(points, float)[:, :2]
    best = np.inf
    for deg in range(90):
        a = np.radians(deg)
        c, s = np.cos(a), np.sin(a)
        x = P[:, 0] * c + P[:, 1] * s
        y = -P[:, 0] * s + P[:, 1] * c
        best = min(best, max(x.max() - x.min(), y.max() - y.min()))
    return float(best)
