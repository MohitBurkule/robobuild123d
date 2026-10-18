"""Making the parts: wall thickness for the process and material, and the printer bed (port of mfg.rs)."""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, ok
from ..measure import Scene
from ..spec import ELECTRONIC

G = "mfg"
MAX_SAMPLES = 8000


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
    d, _ = Scene([body]).first_hit(pts - nrm * eps, -nrm, max_dist=min_wall * 2.5 + 0.2)
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
