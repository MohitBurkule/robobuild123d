"""Making the parts: wall thickness for the process and material, and the printer bed (port of mfg.rs)."""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, ok
from ..spec import ELECTRONIC

G = "mfg"
MAX_SAMPLES = 8000
GRAZE_COS = 0.5  # exit face within 60 degrees of facing the ray


def min_wall_for(prof, process, mat_id) -> float:
    mat = catalog.material(mat_id)
    printed = catalog.part_is_printed(process, mat_id)
    if process == "resin":
        pm = prof.min_wall_resin_mm
    elif mat is not None and mat.cls == "elastomer":
        pm = prof.min_wall_tpu_mm
    elif printed:
        pm = prof.min_wall_fdm_mm
    else:
        pm = 0.0
    return max(pm, mat.min_wall_mm if mat else 0.0)


def wall_samples(body, min_wall):
    from .. import cache

    return cache.memo("part_check", ("wall", cache.source_hash(__file__), cache.body_sig(body), float(min_wall)),
                      lambda: _wall_samples(body, min_wall))


def _wall_samples(body, min_wall):
    """Local wall thickness at sampled surface points: inward ray from each point to where it leaves the solid.

    Returns (thickness, points) for samples whose ray left the solid within the search depth.
    """
    pts, nrm = body.surface(max(min_wall / 3.0, 0.25))
    stride = max(len(pts) // MAX_SAMPLES, 1)
    pts, nrm = pts[::stride], nrm[::stride]
    ln = np.linalg.norm(nrm, axis=1)
    keep = ln > 0.5
    pts, nrm = pts[keep], nrm[keep] / ln[keep, None]
    eps = 1e-3
    o, dirs = pts - nrm * eps, -nrm
    d = np.full(len(o), np.inf)
    cos = np.zeros(len(o))
    if len(o):
        locs, ri, ti = body.mesh.ray.intersects_location(o, dirs, multiple_hits=True)
        if len(ri):
            dk = np.einsum("ij,ij->i", locs - o[ri], dirs[ri])
            ck = np.abs(np.einsum("ij,ij->i", body.mesh.face_normals[ti], dirs[ri]))
            k = dk > 1e-7
            ri, dk, ck = ri[k], dk[k], ck[k]
            order = np.lexsort((dk, ri))  # nearest hit per ray
            ri, dk, ck = ri[order], dk[order], ck[order]
            first = np.r_[True, ri[1:] != ri[:-1]]
            d[ri[first]], cos[ri[first]] = dk[first], ck[first]
    d[d > min_wall * 2.5 + 0.2] = np.inf
    # A wall is measured between two faces that face each other. When the ray leaves through a face it runs nearly
    # parallel to (grazing), the distance is not a wall thickness: that is how the rim of a curved (spline / polygon)
    # extrusion end reads, because the tessellated cap and side strips do not share vertices and their chords cross by
    # tens of microns. Real thin walls, including tapered ones and knife edges, exit through a facing surface.
    d[cos < GRAZE_COS] = np.inf
    t = d + eps
    m = np.isfinite(d)
    return t[m], pts[m]


def run(ctx):
    r, w = ctx.r, ctx.world
    prof = r.profile
    out = []
    checked = 0
    overall = np.inf
    for rp in r.parts:
        p = rp.part
        if p.catalog is not None or p.kind in ELECTRONIC:
            continue
        i = w.index(p.id)
        if i is None:
            ctx.not_checked.append(f"Wall thickness and bed size of `{p.id}`: no geometry")
            continue
        body = w.bodies[i]
        printed = catalog.part_is_printed(p.process, p.material)
        min_wall = min_wall_for(prof, p.process, p.material)
        if printed:
            s = sorted((float(v) for v in body.aabb[1] - body.aabb[0]), reverse=True)
            bed = sorted(prof.bed_mm, reverse=True)
            if any(a > b for a, b in zip(s, bed)):
                out.append(fail("mfg.bed", G, BLOCKER, "Part is bigger than the print bed",
                                f"`{p.id}` is {s[0]:.0f} x {s[1]:.0f} x {s[2]:.0f} mm.").on(p.id)
                           .fix("Split it into two parts joined with screws."))
        if (p.process or "") == "cots" or p.kind == "belt":   # bought parts have no made walls (VERIFIER_ISSUES #5)
            continue
        if min_wall <= 0.0:
            if catalog.material(p.material) is None:
                ctx.not_checked.append(f"Minimum wall of `{p.id}`: material `{p.material}` unknown")
            continue
        checked += 1
        t, P = wall_samples(body, min_wall)
        thin = t < min_wall - 0.05
        if not thin.any():
            continue
        k = int(np.argmin(np.where(thin, t, np.inf)))
        tw, at = float(t[k]), P[k]
        overall = min(overall, tw)
        if int(thin.sum()) >= 8:  # grid slivers are not walls: need a cluster of samples
            sev = BLOCKER if tw < min_wall * 0.7 else WARNING
            out.append(fail("mfg.thin_wall", G, sev, "Wall too thin to make",
                            f"`{p.id}` has walls down to {tw:.2f} mm near ({at[0]:.1f}, {at[1]:.1f}, {at[2]:.1f}); "
                            f"{p.process or 'this process'} {p.material or ''} needs at least {min_wall:.1f} mm.")
                       .on(p.id).here(at).expect(f">= {min_wall:.1f} mm", f"{tw:.2f} mm")
                       .fix("Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature."))
    if np.isfinite(overall):
        ctx.metrics["min_wall_mm"] = float(overall)
    if checked > 0 and all(f.passed for f in out):
        out.append(ok("mfg.walls", G, "Walls are thick enough to make",
                      f"{checked} made parts checked for minimum wall and bed size."))
    return out
