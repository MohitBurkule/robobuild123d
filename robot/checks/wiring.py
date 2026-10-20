"""Wiring: every wire is routed through free space as a tube of its real thickness, so fit is proved, not assumed.

Port of the Rust `checks/wiring.rs`: an occupancy grid (CELL mm) from the voxelized bodies, a Euclidean distance
transform, then A* per wire (thick wires first) that keeps clear of solids and of the wires already routed.
"""

from __future__ import annotations

import heapq
import math

import numpy as np
from scipy.ndimage import distance_transform_edt

from .. import geom
from ..finding import BLOCKER, WARNING, Route, fail, note, ok

G = "wiring"
CELL = 0.6
PORT_ZONE = 2.6  # radius around a port where a wire may touch its own part
MAX_EXPANSIONS = 3_000_000
_OD = [(32.0, 0.8), (30.0, 0.9), (28.0, 1.1), (26.0, 1.3), (24.0, 1.6), (22.0, 1.9), (20.0, 2.2), (18.0, 2.6)]
_NB = [(dx, dy, dz) for dx in (-1, 0, 1) for dy in (-1, 0, 1) for dz in (-1, 0, 1) if (dx, dy, dz) != (0, 0, 0)]


def wire_od(awg: float) -> float:
    """Outer diameter in mm of silicone-insulated hookup wire (nearest tabulated gauge)."""
    best = (math.inf, 1.3)
    for a, d in _OD:
        if abs(a - awg) < best[0]:
            best = (abs(a - awg), d)
    return best[1]


def wire_g_per_mm(awg: float) -> float:
    od = wire_od(awg)
    return 0.0013 * od * od


def default_awg(kind: str) -> float:
    return {"power": 24.0, "motor": 28.0}.get(kind, 30.0)


def _from(w):
    return getattr(w, "from", None) or getattr(w, "from_", "")


def tube_dist(points, P):
    """Distance from points P (k,3) to the polyline `points` (unsigned, to the centreline)."""
    P = np.atleast_2d(np.asarray(P, float))
    pts = np.asarray(points, float)
    if len(pts) == 1:
        return np.linalg.norm(P - pts[0], axis=1)
    a, b = pts[:-1], pts[1:]
    ab = b - a
    L2 = np.maximum((ab * ab).sum(1), 1e-18)
    ap = P[:, None, :] - a[None]
    t = np.clip((ap * ab[None]).sum(2) / L2[None], 0, 1)
    d = ap - t[..., None] * ab[None]
    return np.sqrt((d * d).sum(2)).min(1)


class Router:
    def __init__(self, world):
        bl = world.bounds()
        self.min = bl[0] - 2.0
        size = (bl[1] + 2.0) - self.min
        self.n = tuple(int(math.ceil(s / CELL)) + 1 for s in size)
        nx, ny, nz = self.n
        c = [self.min[k] + (np.arange(self.n[k]) + 0.5) * CELL for k in range(3)]
        self.axes = c
        structs = [b.aabb for b in world.bodies if b.kind == "structure"]
        solid = np.ones(self.n, bool)
        if structs:
            lo = np.min([s[0] for s in structs], 0) + 0.4
            hi = np.max([s[1] for s in structs], 0) - 0.4
            inside = [(c[k] >= lo[k]) & (c[k] <= hi[k]) for k in range(3)]
            solid = ~(inside[0][:, None, None] & inside[1][None, :, None] & inside[2][None, None, :])
        for b in world.bodies:
            lo, hi = b.aabb
            if b.kind in ("wheel", "weapon", "pulley", "belt"):
                lo, hi = lo - 0.6, hi + 0.6
                m = [(c[k] >= lo[k]) & (c[k] <= hi[k]) for k in range(3)]
                solid |= m[0][:, None, None] & m[1][None, :, None] & m[2][None, None, :]
                continue
            i0 = np.clip(np.floor((lo - self.min) / CELL).astype(int), 0, np.array(self.n))
            i1 = np.clip(np.ceil((hi - self.min) / CELL).astype(int), 0, np.array(self.n))
            if np.any(i1 <= i0):
                continue
            occ, _, h = geom.voxelize(b.mesh, CELL, self.min + i0 * CELL, self.min + i1 * CELL)
            if abs(h - CELL) > 1e-9:  # grid was coarsened; fall back to the box (conservative)
                occ = np.ones(tuple(i1 - i0), bool)
            sx, sy, sz = (slice(int(i0[k]), int(i0[k]) + occ.shape[k]) for k in range(3))
            solid[sx, sy, sz] |= occ
        self.solid = solid
        # Distance (mm) from each cell centre to the nearest solid, to within half a cell.
        self.dist = distance_transform_edt(~solid) * CELL - CELL * 0.5 if (~solid).any() else np.full(self.n, -1.0)
        self.done: list[Route] = []

    def cell(self, p):
        return tuple(int(math.floor((p[k] - self.min[k]) / CELL)) for k in range(3))

    def centre(self, c):
        return self.min + (np.asarray(c, float) + 0.5) * CELL

    def inb(self, c):
        return all(0 <= c[k] < self.n[k] for k in range(3))

    def free_pts(self, P, r, ends):
        """True where a wire of radius r can sit with its centreline at each point of P."""
        P = np.atleast_2d(np.asarray(P, float))
        out = np.ones(len(P), bool)
        near = np.zeros(len(P), bool)
        for e in ends:
            near |= np.linalg.norm(P - e, axis=1) < PORT_ZONE
        idx = np.floor((P - self.min) / CELL).astype(int)
        inb = np.all((idx >= 0) & (idx < np.array(self.n)), axis=1)
        d = np.full(len(P), -1.0)
        d[inb] = self.dist[idx[inb, 0], idx[inb, 1], idx[inb, 2]]
        out &= d >= r + 0.05
        for o in self.done:
            out &= tube_dist(o.points, P) >= r + o.od_mm * 0.5 + 0.02
        return out | near

    def blocked_grid(self, r, ends):
        """Per-cell blocked mask for the search (same test as free_pts at cell centres)."""
        blocked = self.dist < r + 0.05
        X, Y, Z = self.axes
        for o in self.done:
            pts = np.asarray(o.points, float)
            reach = r + o.od_mm * 0.5 + 0.02
            lo = np.floor((pts.min(0) - reach - self.min) / CELL).astype(int).clip(0, np.array(self.n))
            hi = np.ceil((pts.max(0) + reach - self.min) / CELL).astype(int).clip(0, np.array(self.n))
            if np.any(hi <= lo):
                continue
            G3 = np.stack(np.meshgrid(X[lo[0]:hi[0]], Y[lo[1]:hi[1]], Z[lo[2]:hi[2]], indexing="ij"), -1)
            sub = tube_dist(pts, G3.reshape(-1, 3)).reshape(G3.shape[:3]) < reach
            blocked[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] |= sub
        for e in ends:
            lo = np.floor((e - PORT_ZONE - self.min) / CELL).astype(int).clip(0, np.array(self.n))
            hi = np.ceil((e + PORT_ZONE - self.min) / CELL).astype(int).clip(0, np.array(self.n))
            if np.any(hi <= lo):
                continue
            G3 = np.stack(np.meshgrid(X[lo[0]:hi[0]], Y[lo[1]:hi[1]], Z[lo[2]:hi[2]], indexing="ij"), -1)
            near = np.linalg.norm(G3 - e, axis=-1) < PORT_ZONE
            blocked[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]] &= ~near
        return blocked

    def route(self, a, b, r):
        """A* over 26-neighbours. Returns (path, None) or (None, (gap, closest point))."""
        sc, gc = self.cell(a), self.cell(b)
        closest = (float(np.linalg.norm(b - a)), a)
        if not (self.inb(sc) and self.inb(gc)):
            return None, closest
        blocked = self.blocked_grid(r, [a, b])
        cost = {sc: 0.0}
        came = {}
        heap = [(closest[0], 0.0, sc)]
        steps = 0
        bx, by, bz = b
        mn = self.min
        nx, ny, nz = self.n
        while heap:
            f, g, cur = heapq.heappop(heap)
            if cur == gc:
                path = [b]
                k = cur
                while k in came:
                    k = came[k]
                    path.append(self.centre(k))
                path.append(a)
                path.reverse()
                return path, None
            base = cost[cur]
            if g > base + 1e-9:
                continue  # stale heap entry
            steps += 1
            if steps > MAX_EXPANSIONS:
                return None, closest
            here = self.centre(cur)
            dh = float(np.linalg.norm(b - here))
            if dh < closest[0]:
                closest = (dh, here)
            cx, cy, cz = cur
            for dx, dy, dz in _NB:
                x, y, z = cx + dx, cy + dy, cz + dz
                if not (0 <= x < nx and 0 <= y < ny and 0 <= z < nz):
                    continue
                nc = (x, y, z)
                if nc != gc and blocked[x, y, z]:
                    continue
                nd = base + math.sqrt(dx * dx + dy * dy + dz * dz) * CELL
                if nd < cost.get(nc, math.inf):
                    cost[nc] = nd
                    came[nc] = cur
                    px, py, pz = mn[0] + (x + 0.5) * CELL, mn[1] + (y + 0.5) * CELL, mn[2] + (z + 0.5) * CELL
                    heapq.heappush(heap, (nd + math.sqrt((bx - px) ** 2 + (by - py) ** 2 + (bz - pz) ** 2), nd, nc))
        return None, closest

    def segment_free(self, p, q, r, ends):
        k = max(int(math.ceil(np.linalg.norm(q - p) / 0.25)), 1)
        t = np.linspace(0, 1, k + 1)[:, None]
        return bool(self.free_pts(p + (q - p) * t, r, ends).all())

    def smooth(self, path, r, ends):
        """Pull the path taut: skip waypoints whenever the straight line stays clear."""
        out, i = [], 0
        while i < len(path):
            p = path[i]
            out.append(p)
            j = len(path) - 1
            while j > i + 1 and not self.segment_free(p, path[j], r, ends):
                j -= 1
            if j <= i:
                break
            i = j
        return out


def polyline_len(pts):
    return float(sum(np.linalg.norm(np.asarray(b) - np.asarray(a)) for a, b in zip(pts, pts[1:])))


def _unit(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v * 0.0


def sharp_bend(pts, od):
    """(corner point, degrees) of the last corner tighter than a 2 x OD bend radius allows, else None."""
    pts = [np.asarray(p, float) for p in pts]
    min_bend = 2.0 * od
    sharp = None
    for p, q, s in zip(pts, pts[1:], pts[2:]):
        u, v = _unit(q - p), _unit(s - q)
        theta = math.acos(float(np.clip(u.dot(v), -1, 1)))
        need = min_bend * math.tan(theta / 2)
        room = min(np.linalg.norm(q - p), np.linalg.norm(s - q))
        if theta > 0.2 and need > room * 0.9 + 0.5:
            sharp = (q, math.degrees(theta))
    return sharp


def run(ctx):
    out = []
    r, world = ctx.r, ctx.world
    if not r.spec.wires:
        out.append(note("wiring.none", G, "No wires declared",
                        "The spec lists no wires, so nothing is routed or counted for mass."))
        return out
    router = Router(world)
    total_len = total_g = 0.0
    nok = 0
    order = sorted(r.spec.wires, key=lambda w: -wire_od(w.awg if w.awg is not None else default_awg(w.kind)))
    for w in order:
        awg = float(w.awg) if w.awg is not None else default_awg(w.kind)
        od = wire_od(awg)
        wf, wt = _from(w), w.to
        a, b = world.port(r, wf), world.port(r, wt)
        if a is None or b is None:
            out.append(fail("wiring.port", G, BLOCKER, "Wire end not found",
                            f"Wire `{w.id}` runs `{wf}` to `{wt}` but one of those ports does not exist.")
                       .fix("Use `part.port` names from the catalog entry or the part's `ports`."))
            continue
        a, b = np.asarray(a, float), np.asarray(b, float)
        radius = od * 0.5
        ends = [a, b]
        legs = [a] + [np.asarray(v, float) for v in (w.via or [])] + [b]
        raw, miss = [], None
        for p0, p1 in zip(legs, legs[1:]):   # declared waypoints: route leg by leg, so the wire follows the designer's channel
            seg, miss = router.route(p0, p1, radius)
            if seg is None:
                raw = None
                break
            seg = router.smooth(seg, radius, ends)   # taut within the leg; the waypoints themselves stay
            raw += list(seg) if not raw else list(seg)[1:]
        if raw is None:
            gap, at = miss
            at = np.asarray(at, float)
            toward = at + _unit(b - at) * 1.4
            cands = [(float(bd.sdf(toward)[0]), bd.id) for bd in world.bodies if not bd.is_wire]
            blocker = min(cands)[1] if cands else ""
            out.append(fail("wiring.route", G, BLOCKER, "No room for this wire",
                            f"Wire `{w.id}` ({awg:g} AWG, {od:.1f} mm thick) from `{wf}` to `{wt}` has no clear path; "
                            f"it gets within {gap:.1f} mm of the end at ({at[0]:.1f}, {at[1]:.1f}, {at[2]:.1f}) and "
                            f"`{blocker}` blocks it.")
                       .on(wf, wt).here(at)
                       .fix("Cut a wire channel (at least 2.5 mm wide) through the walls between those parts, or move "
                            "the parts closer."))
            continue
        pts = raw
        slack = w.slack_mm if w.slack_mm is not None else 6.0
        length = polyline_len(pts) + slack
        min_bend = 2.0 * od
        sharp = sharp_bend(pts, od)
        total_len += length
        total_g += length * wire_g_per_mm(awg)
        if sharp is not None:
            at, deg = sharp
            out.append(fail("wiring.bend", G, WARNING, "Wire bends too tightly",
                            f"Wire `{w.id}` turns {deg:.0f} degrees with less than {min_bend:.1f} mm bend radius; it "
                            "will kink or pull off its solder joint.")
                       .here(at).fix("Widen the channel at the corner or route it in a straighter line."))
        else:
            nok += 1
        router.done.append(Route(w.id, awg, w.kind, od, length, [[float(x) for x in p] for p in pts]))
    ctx.metrics["wire_length_mm"] = total_len
    ctx.metrics["wire_mass_g"] = total_g
    ctx.routes = list(router.done)
    if all(f.passed or f.id == "wiring.none" for f in out):
        out.append(ok("wiring.route", G, "Every wire has a route",
                      f"{nok} wires routed as real-thickness tubes through free space, {total_len:.0f} mm in total, "
                      "no collisions."))
    return out
