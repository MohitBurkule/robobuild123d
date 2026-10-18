"""Measurements between bodies, on exact mesh booleans (manifold3d) and mesh queries (trimesh)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import trimesh

from . import cache, geom

_QSRC = None


def _qv():
    global _QSRC
    if _QSRC is None:
        from pathlib import Path
        d = Path(__file__).parent
        _QSRC = cache.source_hash(d / 'measure.py', d / 'geom.py')
    return _QSRC


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
    return cache.memo("overlap", ("ov", _qv(), cache.body_sig(a), cache.body_sig(b), shift, cap),
                      lambda: _overlap(a, b, shift, abox, cap))


def _overlap(a, b, shift, abox, cap):
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
    g = cache.memo("min_gap", ("gap", _qv(), cache.body_sig(a), cache.body_sig(b), float(search)),
                   lambda: float(a.manifold.min_gap(b.manifold, search)))
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
        self._mesh = None

    @property
    def mesh(self):
        if self._mesh is None and self.bodies:
            self._mesh = trimesh.util.concatenate([b.mesh for b in self.bodies])
        return self._mesh

    def first_hit(self, origins, dirs, max_dist=np.inf):
        """Distance to the first surface hit along each ray (inf when none) and the body index hit (-1).

        Computed body by body (each memoised on that body's geometry and placement), so a changed part only re-casts
        its own rays; the nearest hit over bodies equals a cast against the concatenated scene."""
        origins = np.atleast_2d(np.asarray(origins, float))
        dirs = np.atleast_2d(np.asarray(dirs, float))
        n = len(origins)
        dist = np.full(n, np.inf)
        who = np.full(n, -1)
        if not self.bodies or n == 0:
            return dist, who
        for i, b in enumerate(self.bodies):
            d = _body_hits(b, origins, dirs)
            better = d < dist
            dist[better] = d[better]
            who[better] = i
        dist[dist > max_dist] = np.inf
        return dist, who


def _rays_touch_box(lo, hi, O, D) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        inv = 1.0 / D
        t1, t2 = (lo - 1e-6 - O) * inv, (hi + 1e-6 - O) * inv
        t1 = np.where(np.isnan(t1), -np.inf, t1)
        t2 = np.where(np.isnan(t2), np.inf, t2)
    tmin = np.minimum(t1, t2).max(axis=1)
    tmax = np.maximum(t1, t2).min(axis=1)
    return (tmax >= np.maximum(tmin, 0.0))


def _body_hits(b, origins, dirs):
    lo, hi = b.aabb
    m = _rays_touch_box(lo, hi, origins, dirs)
    out = np.full(len(origins), np.inf)
    if not m.any():
        return out
    if not m.all():
        out[m] = _body_hits_all(b, origins[m], dirs[m])
        return out
    return _body_hits_all(b, origins, dirs)


def _body_hits_all(b, origins, dirs):
    def compute():
        out = np.full(len(origins), np.inf)
        locs, ray_i, _ = b.mesh.ray.intersects_location(origins, dirs, multiple_hits=True)
        if len(ray_i):
            d = np.einsum("ij,ij->i", locs - origins[ray_i], dirs[ray_i])
            ok = d > 1e-7
            np.minimum.at(out, ray_i[ok], d[ok])
        return out

    return cache.memo("ray", ("ray", _qv(), cache.body_sig(b), origins, dirs), compute)


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
