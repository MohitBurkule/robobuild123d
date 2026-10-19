"""fastener.hole_record: every fastener carries a `hole` record (clearance, head seat, grip) so the hole and seat
checks can judge it; a fastener with none (`hole: null`) was never checked. And a screw that threads straight into a
printed part needs `review.fastener.min_engagement_d` x d of thread in the plastic (default 2.5 d), or an insert / nut.

Engagement = length - grip (hole.grip when recorded, else the summed thickness is unknown and the whole length is the
upper bound).
"""

from __future__ import annotations

from .. import catalog
from ..finding import BLOCKER, fail, ok
from ._review import params, x

G = "fastener_record"
DEFAULTS = {"min_engagement_d": 2.5}


def run(ctx):
    spec = ctx.r.spec
    k = float(params(spec, "fastener", DEFAULTS)["min_engagement_d"])
    out, n = [], 0
    for f in spec.fasteners:
        hole = x(f, "hole")
        good = True
        if not hole:
            good = False
            out.append(fail("fastener.hole_record", G, BLOCKER, "Fastener has no hole record",
                            f"`{f.id}` ({f.designation}) has no `hole`, so no hole or seat check ever judged it.")
                       .on(f.id, *(f.through or [])).here(f.at)
                       .fix("Give it a `hole` record (d, clearance_d, head seat, grip) and cut that hole in the parts."))
        host = spec.part(f.threads_into) if f.threads_into else None
        dl = catalog.parse_designation(f.designation)
        if host is not None and dl and host.kind not in ("nut", "insert") and catalog.part_is_printed(host.process, host.material):
            d, length = dl
            grip = (hole or {}).get("grip")
            eng = length - float(grip) if grip is not None else length
            need = k * d
            if eng < need - 1e-6:
                good = False
                out.append(fail("fastener.hole_record", G, BLOCKER, "Too little thread in plastic",
                                f"`{f.id}` ({f.designation}) threads straight into printed `{host.id}` with "
                                f"{'about ' if grip is None else ''}{eng:.1f} mm of engagement"
                                f"{' (no grip recorded: whole length)' if grip is None else ''}; plastic threads need "
                                f">= {k:g} d = {need:.1f} mm or they strip after a few rebuilds.")
                           .on(f.id, host.id).here(f.at).expect(f">= {need:.1f} mm", f"{eng:.1f} mm")
                           .fix("Use a heat-set insert or a captive nut, a longer screw into a deeper boss, or bond the part."))
        n += good
    if n == len(spec.fasteners) and n:
        out.append(ok("fastener.hole_record", G, "Fasteners recorded", f"{n} fasteners have hole records and enough thread."))
    return out
