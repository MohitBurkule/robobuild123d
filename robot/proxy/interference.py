"""Fast proxy for `interference`: an AABB pre-pass, then bounds that can only over-report.

  static   every AABB-overlapping pair gets the exact overlap depth (measure.overlap, memoised in the run cache, so
           only pairs with a changed part cost a boolean): the same verdict as interference.overlap.
  sweeps   each revolute joint's moving set and each spinning weapon's rotor is revolved a full turn on a (radius,
           axial) grid (interference.Revolved, CELL_MM). An overlap deeper than the pair's allowance must contain a
           point of the other body at least that deep inside it, so only those voxels (deep_points) are tested
           against the envelope. A full turn contains every pose of any joint range, so a hit the
           3-degree pose sweep would see is not missed (up to the grid, as in the full spin sweep).
Wheel running clearance and captive parts are cheap and run exactly (interference.wheel_clearance / .captive).
Findings: proxy.interference (static pair), proxy.sweep (joint or weapon envelope hits a body).
"""

from __future__ import annotations

import math

import numpy as np
from scipy import ndimage

from .. import geom, measure
from ..checks import interference as itf
from ..checks.power import spin_axis
from ..finding import BLOCKER, fail, ok

G = "proxy"
CELL_MM = 1.0  # revolved-envelope grid (full spin sweep: 0.5 mm)
PAD_CELLS = 1  # dilation covering the coarse grid
EMPTY_MM3 = 1e-6
NEVER_HITS_MM = 1.0e3  # interference: an allowance this deep (weapon on its motor, fused, threaded) is never a hit  # an intersection below this volume is touching


def static(ctx, parts=None):
    """AABB pre-pass, then the exact (memoised) overlap depth of the pairs that touch: the same verdict as the full
    static check; the cache makes unchanged pairs free, so only pairs with a changed part cost a boolean."""
    r, w = ctx.r, ctx.world
    out = []
    for i, a in enumerate(w.bodies):
        for b in w.bodies[i + 1:]:
            if parts is not None and a.id not in parts and b.id not in parts:
                continue
            if a.is_wire or b.is_wire or not measure.aabb_overlap(a.aabb, b.aabb):
                continue
            allow = itf.allowed_depth(r, a, b)
            if math.isinf(allow):
                continue
            o = measure.overlap(a, b, cap=allow)
            if o is not None and o.depth > allow:
                out.append(fail("proxy.interference", G, BLOCKER, "Parts collide",
                                f"`{a.id}` and `{b.id}` overlap by {o.depth:.2f} mm (allowed {allow:.2f}).").on(a.id, b.id).here(o.at))
    return out


def depth_grid(body, h=CELL_MM):
    """(voxel centres, depth of each inside the body) on an h grid."""
    occ, glo, hh = geom.voxelize(body.mesh, h, body.aabb[0] - h, body.aabb[1] + h)
    depth = ndimage.distance_transform_edt(occ) * hh
    idx = np.argwhere(occ)
    return glo + (idx + 0.5) * hh, depth[occ]


def deep_points(grid, allow):
    """Voxel centres deeper than `allow` inside the body: an overlap deeper than `allow` must contain one (to the grid)."""
    P, d = grid
    return P[d > allow]


def _movers(ctx):
    """[(label, origin, axis, moving body ids)] for every revolute joint and spinning weapon."""
    r, w = ctx.r, ctx.world
    out = []
    for rp in r.parts:
        j = rp.part.joint
        if j is None or j.kind != "revolute":
            continue
        moved = itf.descendants(r, rp.part.id)
        moved |= itf.riding_fasteners(r, moved)
        pb = w.body(rp.part.parent) if rp.part.parent else None
        PM = pb.M if pb is not None else np.eye(4)
        ax = PM[:3, :3] @ np.asarray(j.axis, float)
        out.append((f"joint `{rp.part.id}`", (PM @ np.append(np.asarray(j.pivot, float), 1.0))[:3], ax / np.linalg.norm(ax), moved))
    for i, b in enumerate(w.bodies):
        wd = r.parts[b.part_idx].part.weapon if b.part_idx is not None else None
        if wd is None or wd.kind not in ("spinner", "drum", "disc", "bar"):
            continue
        sa = spin_axis(w, r, i)
        if sa is None:
            continue
        rotor = itf.rotor_ids(r, r.parts[b.part_idx].part)
        out.append((f"weapon `{b.id}`", sa[0], sa[1], rotor | itf.riding_fasteners(r, rotor)))
    return out


def sweeps(ctx, parts=None):
    r, w = ctx.r, ctx.world
    out, grids = [], {}  # body id -> depth grid, shared by every mover
    for label, origin, axis, moved in _movers(ctx):
        mov = [b for b in w.bodies if b.id in moved and not b.is_wire]
        revs = [(m, itf.Revolved.build(m, origin, axis, CELL_MM)) for m in mov]
        if any(rv is None for _, rv in revs):
            out.append(fail("proxy.sweep", G, BLOCKER, "Sweep envelope too large", f"{label}: cannot rasterise.").on(*moved))
            continue
        reach = max(rv.nr * rv.cell for _, rv in revs) + CELL_MM
        for o in w.bodies:
            if o.id in moved or o.is_wire:
                continue
            if parts is not None and o.id not in parts and not (moved & set(parts)):
                continue
            q = itf._corners(o.aabb) - origin
            rad = np.linalg.norm(q - np.outer(q @ axis, axis), axis=1)
            if not np.any(rad < reach + float(np.linalg.norm(o.aabb[1] - o.aabb[0]))):
                continue
            for m, rv in revs:
                allow = itf.allowed_depth(r, m, o)
                if allow >= NEVER_HITS_MM:
                    continue
                if o.id not in grids:
                    grids[o.id] = depth_grid(o)
                P = deep_points(grids[o.id], allow)
                if len(P) and rv.near(P, PAD_CELLS).any():
                    out.append(fail("proxy.sweep", G, BLOCKER, "Moving part may hit another part",
                                    f"{label}: `{m.id}` turning a full revolution may reach `{o.id}`.").on(m.id, o.id))
                    break
    return out


def run(ctx, parts=None):
    out = static(ctx, parts) + sweeps(ctx, parts)
    if not out:
        out.append(ok("proxy.interference", G, "No collisions in the proxy", "Static pairs and revolved sweep envelopes clear."))
    out += itf.wheel_clearance(ctx) + itf.captive(ctx)
    return out
