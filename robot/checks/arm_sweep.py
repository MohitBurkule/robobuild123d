"""Hinged weapons (lifters, flippers, axes, hammers): what they sweep and what drives them. Not a check group.

A spinner turns without end, so its keep-out is the solid of revolution of the rotor (`wire_review.swept_bands`). A
hinged arm only moves over its joint's declared `min`..`max`, so treating it as a full revolution blocks wires, the
battery and the router from space the arm can never reach. This module gives every check one answer:

- `is_arm(weapon)`: `weapon.kind` is a hinged kind (ARM_KINDS). Anything else (disc, bar, drum, ring, saw, an unknown
  or missing kind) is a spinner, so the strict rules stay on by default.
- `arm_range(spec, world, group, ids)`: (lo, hi) degrees of travel relative to the current pose, for a revolute group
  that carries a hinged weapon, no spinning weapon, and a joint range under FULL_TURN_DEG. Else None (full revolution).
- `ArcSweep`: the volume the group's posed bodies sweep over that range; `dist` is a lower bound on the distance to it
  (0 inside), `occupancy` marks a voxel grid for the router.
"""

from __future__ import annotations

import math

import numpy as np

from .. import geom, xform

ARM_KINDS = frozenset({"lifter", "flipper", "axe", "hammer", "arm", "grabber", "crusher", "clamp", "self_right"})
FULL_TURN_DEG = 359.0
SAMPLE_MM = 0.25   # surface sample spacing for the distance tree
ARC_MM = 0.25      # angular step: the farthest point of the group moves at most this far between two steps
VOXEL_MM = 0.25    # body occupancy for the inside test


def is_arm(weapon) -> bool:
    return weapon is not None and str(getattr(weapon, "kind", "") or "").lower() in ARM_KINDS


def is_spinner(weapon) -> bool:
    return weapon is not None and not is_arm(weapon)


def _joint(p):
    j = getattr(p, "joint", None) or (getattr(p, "_extra", None) or {}).get("joint")
    if not j:
        return None
    return j if isinstance(j, dict) else getattr(j, "__dict__", {})


def arm_range(spec, world, group, ids):
    """(lo, hi) degrees relative to the current pose when `group` is a hinged weapon on a limited joint, else None."""
    members = [spec.part(i) for i in ids]
    weps = [p.weapon for p in members if p is not None and getattr(p, "weapon", None) is not None]
    if not weps or any(is_spinner(w) for w in weps):
        return None
    jp = next((p for p in spec.parts if _joint(p) and _joint(p).get("kind") == "revolute"
               and (p.rotates_with if p.rotates_with not in (None, "fixed") else p.id) == group), None)
    if jp is None:
        return None
    j = _joint(jp)
    if j.get("min") is None or j.get("max") is None:
        return None
    lo, hi = sorted((float(j["min"]), float(j["max"])))
    if hi - lo >= FULL_TURN_DEG:
        return None
    v0 = float((getattr(world, "joints", None) or {}).get(jp.id, j.get("default") or 0.0)) if world is not None else 0.0
    return lo - v0, hi - v0


class ArcSweep:
    """Volume swept by posed `bodies` turning about (origin, axis) from `lo` to `hi` degrees (relative to the pose)."""

    def __init__(self, bodies, origin, axis, lo, hi):
        from scipy.spatial import cKDTree

        self.bodies = [b for b in bodies if b.mesh is not None and len(b.mesh.faces)]
        self.o = np.asarray(origin, float)
        self.a = xform.norm(np.asarray(axis, float))
        self.lo, self.hi = float(min(lo, hi)), float(max(lo, hi))
        self.S = np.vstack([b.surface(SAMPLE_MM)[0] for b in self.bodies])
        q = self.S - self.o
        self.R = float(np.linalg.norm(q - np.outer(q @ self.a, self.a), axis=1).max())
        step = math.degrees(ARC_MM / max(self.R, 1.0))
        n = max(int(math.ceil((self.hi - self.lo) / step)), 1)
        self.angles = np.linspace(self.lo, self.hi, n + 1)
        self.tree = cKDTree(self.S)
        self.occ = [geom.voxelize(b.mesh, VOXEL_MM, b.aabb[0] - VOXEL_MM, b.aabb[1] + VOXEL_MM) for b in self.bodies]
        from .wire_review import swept_bands
        self.bands = swept_bands(self.bodies, self.o, self.a)   # the full revolution: a cheap lower bound
        Q = np.vstack([self._turn(self.S, d) for d in self.angles[:: max(len(self.angles) // 64, 1)]] + [self._turn(self.S, self.hi)])
        self.box = np.array([Q.min(0) - ARC_MM, Q.max(0) + ARC_MM])

    def label(self):
        return f"{self.lo:.0f}..{self.hi:.0f} deg range"

    def _turn(self, P, deg):
        R = xform.axis_angle(self.a, deg)
        return (np.atleast_2d(P) - self.o) @ R.T + self.o

    def _inside(self, Q):
        out = np.zeros(len(Q), bool)
        for occ, lo, h in self.occ:
            idx = np.floor((Q - lo) / h).astype(np.int64)
            m = np.all((idx >= 0) & (idx < np.array(occ.shape)), axis=1)
            if m.any():
                out[m] |= occ[idx[m, 0], idx[m, 1], idx[m, 2]]
        return out

    def _exact(self, P, k):
        """Exact distance of each point P[i] to the bodies posed at angle index k[i] (one batched query per body)."""
        import trimesh

        th = -np.radians(self.angles[k])[:, None]
        q = np.atleast_2d(P) - self.o
        a = self.a[None]
        Q = q * np.cos(th) + np.cross(a, q) * np.sin(th) + a * (q @ self.a)[:, None] * (1 - np.cos(th)) + self.o
        out = np.full(len(Q), np.inf)
        for b in self.bodies:
            out = np.minimum(out, trimesh.proximity.closest_point(b.mesh, Q)[1])
        return out

    def dist(self, P, cap=10.0):
        """Per point, a lower bound on its distance to the swept volume (0 inside). Points farther than `cap` from the
        full revolution return that (smaller, still valid) bound without the exact test."""
        from .wire_review import band_dist

        P = np.atleast_2d(np.asarray(P, float))
        out = band_dist(P, self.o, self.a, self.bands)
        c = np.flatnonzero(out < cap)
        if not len(c):
            return out
        Pc = P[c]
        K = np.full((len(self.angles), len(c)), np.inf)
        ins = np.zeros(len(c), bool)
        for k, d in enumerate(self.angles):
            act = np.flatnonzero(~ins)   # a point found inside at one pose is done (distance 0)
            if not len(act):
                break
            Q = self._turn(Pc[act], -d)
            inn = self._inside(Q)
            ins[act[inn]] = True
            if (~inn).any():
                # approximate (eps) nearest sample: only picks the start angle for the exact walk below
                K[k, act[~inn]] = self.tree.query(Q[~inn], eps=0.5, distance_upper_bound=cap + 2.0)[0]
        # The tree only knows surface samples (spacing ~SAMPLE_MM): from each point's best sampled angle, walk the angle
        # grid both ways on the real meshes while the exact distance keeps falling (it is smooth in the angle near
        # its minimum), so a sample gap cannot hide the true closest pose.
        best = K.min(axis=0)
        exact = best.copy()
        live = np.flatnonzero(~ins & np.isfinite(best))
        if len(live):
            k0 = K[:, live].argmin(axis=0)
            e0 = self._exact(Pc[live], k0)
            for step in (-1, 1):
                k, e, act = k0.copy(), e0.copy(), np.arange(len(live))
                while len(act):
                    kn = k[act] + step
                    okk = (kn >= 0) & (kn < len(self.angles))
                    act, kn = act[okk], kn[okk]
                    if not len(act):
                        break
                    en = self._exact(Pc[live[act]], kn)
                    better = en < e[act] - 1e-9
                    act, kn, en = act[better], kn[better], en[better]
                    k[act], e[act] = kn, en
                e0 = np.minimum(e0, e)
            exact[live] = e0
        q = Pc - self.o
        rad = np.linalg.norm(q - np.outer(q @ self.a, self.a), axis=1)
        half_arc = rad * math.radians(float(np.diff(self.angles).max()) if len(self.angles) > 1 else 0.0) / 2
        res = np.where(ins, 0.0, np.maximum(exact - half_arc, 0.0))
        out[c] = np.maximum(out[c], np.minimum(res, cap))
        return out

    def nearest(self, P):
        """(distance, world point of the sweep nearest to the closest of P): for line-of-sight tests."""
        P = np.atleast_2d(np.asarray(P, float))
        d = self.dist(P)
        i = int(np.argmin(d))
        best, at = np.inf, None
        for ang in self.angles:
            Q = self._turn(P[i:i + 1], -ang)
            kd, j = self.tree.query(Q)
            if kd[0] < best:
                best, at = float(kd[0]), self._turn(self.S[j[0]:j[0] + 1], ang)[0]
        return float(d[i]), at

    def occupancy(self, lo, cell, n):
        """Bool grid (shape n, cell centres lo + (i + 0.5) cell) of the cells the swept volume passes through: surface
        samples (cell / 2 apart) and interior cell centres of every body, turned in steps that move the farthest point
        <= cell / 2. The router pads the result by one cell, as it pads the boxes of spinners."""
        n = tuple(int(v) for v in n)
        grid = np.zeros(n, bool)
        step = math.degrees(cell * 0.5 / max(self.R, 1.0))
        angles = np.linspace(self.lo, self.hi, max(int(math.ceil((self.hi - self.lo) / step)), 1) + 1)
        pts = []
        for b in self.bodies:
            pts.append(b.surface(cell * 0.5)[0])
            occ, olo, h = geom.voxelize(b.mesh, cell, b.aabb[0], b.aabb[1])
            idx = np.argwhere(occ)
            if len(idx):
                pts.append(olo + (idx + 0.5) * h)
        base = np.vstack(pts)
        lo = np.asarray(lo, float)
        for d in angles:
            idx = np.floor((self._turn(base, d) - lo) / cell).astype(np.int64)
            m = np.all((idx >= 0) & (idx < np.array(n)), axis=1)
            grid[idx[m, 0], idx[m, 1], idx[m, 2]] = True
        return grid


def arm_sweeps(spec, world):
    """{body id: ArcSweep} for every body of a hinged-weapon group on a limited joint (the router's and proxy's
    keep-out for those bodies is the sweep, not their padded box)."""
    from .wire_review import rotor_groups

    out = {}
    for grp, piv, ax, ids in rotor_groups(spec, world):
        rng = arm_range(spec, world, grp, ids)
        if rng is None:
            continue
        bodies = [b for b in (world.body(i) for i in ids) if b is not None and not b.is_wire]
        if not bodies:
            continue
        sw = ArcSweep(bodies, piv, ax, *rng)
        for b in bodies:
            out[b.id] = sw
    return out
