"""Fastener engagement percent (`engagement.*`, G3): screw length vs the clamped stack.

WHY: `fastener.engagement` blocks a screw whose thread overlap with the threaded host is
under `profile.engagement_d` x diameter, but nothing measures the CLAMPED STACK - the summed
MATERIAL thickness of the `through` parts the screw must span before any thread reaches the
host. A screw shorter than its stack clamps nothing (the head bottoms out on the first part)
and a screw threading into printed plastic wants more than the 1.5 d metal minimum (2 d here,
`review.engagement.plastic_x_d`).

The stack and the engagement are measured as material, not bounding boxes: ring samples just
outside the clearance hole (thread radius + 0.4 mm, 3 azimuths, 0.5 mm steps along the shank)
that fall inside a part count as clamped / engaged length.

engagement.clamp_short (BLOCKER): usable shank length < clamped stack + 0.2 mm.
engagement.pct_low (WARNING): thread engagement under `plastic_x_d` x diameter in a printed
host (above the fastener group's 1.5 d blocker floor, so only the marginal band fires). The
minimum engagement percent of the design lands in the report metrics.
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, ok
from ._review import params
from .fasteners import perp

G = "engagement"
DEFAULTS = {"plastic_x_d": 2.0}
PRINTED = {"fdm", "resin", "sla", "mjf", "sls", "printed", "print", "polyjet"}
TIP_MARGIN_MM = 0.2  # the tip's partial thread counts for nothing
RING_D = 0.4  # sample ring sits just outside the clearance hole: thread radius + this
STEP_MM = 0.5


def material_spans(w, f, dr, at, ln, ids):
    """{part id: material length (mm)} along the shank: ring samples (3 azimuths, RING_D past the thread)
    inside the part, counted where ANY azimuth is in. An axis sample inside a hole reads as empty."""
    u, v = perp(dr)
    d, _ = catalog.parse_designation(f.designation)
    r = d / 2.0 + RING_D
    out = {pid: 0.0 for pid in ids}
    bodies = {pid: w.body(pid) for pid in ids}
    for s in range(int(ln / STEP_MM) + 1):
        t = min(s * STEP_MM, ln)
        c = at + dr * t
        pts = np.array([c + u * (r * np.cos(a * 2 * np.pi / 3)) + v * (r * np.sin(a * 2 * np.pi / 3))
                        for a in range(3)])
        for pid, b in bodies.items():
            if b is not None and bool(b.inside(pts).any()):
                out[pid] += (STEP_MM if t < ln else ln - int(ln / STEP_MM) * STEP_MM)
    return out


def _host_printed(r, tid):
    p = r.spec.part(tid)
    if p is None or p.kind in ("nut", "insert", "bearing", "motor", "weapon_motor"):
        return False  # metal hardware / maker-tapped holes: the 1.5 d floor governs
    return str(p.process or "").strip().lower() in PRINTED


def run(ctx):
    r, w = ctx.r, ctx.world
    p = params(r.spec, "engagement", DEFAULTS)
    out, n, worst = [], 0, np.inf
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            ctx.not_checked.append(f"Engagement: fastener `{f.id}` designation `{f.designation}` not understood")
            continue
        d, ln = dl
        dr = np.asarray(f.dir, float)
        dr = dr / np.linalg.norm(dr)
        at = np.asarray(f.at, float)
        tid = f.threads_into
        through = [pid for pid in (f.through or []) if w.body(pid) is not None]
        spans = material_spans(w, f, dr, at, ln, through + ([tid] if tid and w.body(tid) is not None else []))
        stack = sum(spans[pid] for pid in through)
        n += 1
        if stack + TIP_MARGIN_MM >= ln:
            parts = [pid for pid in through if spans[pid] > 0] or through
            out.append(fail("engagement.clamp_short", G, BLOCKER, "Screw is shorter than the stack it must clamp",
                            f"`{f.id}` ({f.designation}) spans {stack:.1f} mm of clamped material ({', '.join(parts) or 'no resolved parts'}) "
                            f"but has only {ln:.1f} mm of shank: the head bottoms out before anything is clamped.")
                       .on(f.id, *parts).expect(f"> {stack:.1f} mm shank", f"{ln:.1f} mm")
                       .fix("Use a longer screw (or an insert closer to the tip) so at least a full diameter of thread "
                            "reaches past the last clamped part into the host."))
            continue
        engaged = spans.get(tid, 0.0) if tid else 0.0
        if tid and engaged > 0:
            pct = engaged / d * 100.0
            worst = min(worst, pct)
            if _host_printed(r, tid) and engaged < p["plastic_x_d"] * d:
                out.append(fail("engagement.pct_low", G, WARNING, "Little thread in printed plastic",
                                f"`{f.id}` engages {engaged:.1f} mm in `{tid}` ({pct:.0f}% of one diameter); threads cut or "
                                f"self-tapped into printed plastic strip under {p['plastic_x_d']:.1f} x d.")
                           .on(f.id, tid).expect(f">= {p['plastic_x_d'] * d:.1f} mm", f"{engaged:.1f} mm")
                           .fix("Use a longer screw into a heat-set insert, or add wall depth so at least "
                                f"{p['plastic_x_d']:.1f} x the thread diameter engages."))
    if n and np.isfinite(worst):
        ctx.metrics["fastener_engagement_min_pct"] = round(float(worst), 1)
    if n and not out:
        out.append(ok("engagement.ok", G, "Screws span their stacks and bite enough",
                      f"{n} fasteners: every shank is longer than its clamped stack"
                      + (f", minimum thread engagement {worst:.0f}% of one diameter." if np.isfinite(worst) else ".")))
    elif not r.spec.fasteners:
        ctx.not_checked.append("Engagement: the spec declares no fasteners")
    return out
