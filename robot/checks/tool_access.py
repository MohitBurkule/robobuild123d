"""Driver and wrench access for EVERY fastener (`tool_access.*`, G4).

WHY: `fastener.access` proves the driver path only for screws that declare a `tool` (one
without a tool just gets `fastener.no_tool`, its access unjudged), and nothing proves a
WRENCH can reach the NUT a screw threads into - a nut in a pocket that no spanner or
socket fits cannot be tightened, so the joint is only finger-tight.

tool_access.blocked (BLOCKER): a screw with no declared tool (the catalog hex key of its
head is used) whose straight driver path out of the head is blocked by another part.
tool_access.nut_blocked (BLOCKER): the ring a wrench must occupy around a nut (its own
width across flats + `profile.driver_access_radius_mm` clearance) is blocked by a part
that is not in the joint being tightened.

Both probes are the fastener group's own (robot/checks/fasteners.py: perp, _first_inside,
tool_radius), so the verdicts agree with `fastener.access`.
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..cad import fastener_catalog
from ..finding import BLOCKER, fail, ok
from .fasteners import _first_inside, perp, tool_radius

G = "tool_access"


def driver_path_blocked(w, dr, at, d, key, reach, skip):
    """(distance above the head, blocking body id) of the first hit on the driver path, or None when clear."""
    rad = tool_radius(f"hex{key:g}")
    k = catalog.screw_dims(d)[1]
    top = at - dr * k  # the probe starts just above the head, like fasteners.access
    u, v = perp(dr)
    pts, ts = [], []
    for s in range(int(reach / 0.5) + 1):
        t = s * 0.5
        c = top - dr * (t + 0.05)
        for a in range(8):
            ang = a * np.pi / 4
            pts.append(c if a == 0 else c + u * (rad * np.cos(ang)) + v * (rad * np.sin(ang)))
            ts.append(t)
    hit = _first_inside(w.bodies, np.array(pts), skip)
    return None if hit is None else (ts[hit[0]], hit[1].id)


def nut_ring_blocked(w, f, dr, nb, clearance, skip_ids):
    """(blocking body id) when the wrench ring around the nut `nb` is occupied, else None."""
    lo, hi = np.asarray(nb.aabb, float)
    c = np.asarray((lo + hi) / 2.0, float)
    perp_span = max(float(np.linalg.norm((hi - lo) - dr * float((hi - lo) @ dr))), 0.1)
    rad = 0.5 * perp_span + clearance
    u, v = perp(dr)
    pts = [c + u * (rad * np.cos(a * np.pi / 6)) + v * (rad * np.sin(a * np.pi / 6)) for a in range(12)]
    for b in w.bodies:
        if b.id in skip_ids or getattr(b, "is_wire", False) or getattr(b, "fastener", False):
            continue
        if bool(b.inside(np.array(pts)).any()):
            return b.id
    return None


def run(ctx):
    r, w = ctx.r, ctx.world
    out, n = [], 0
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            ctx.not_checked.append(f"Tool access: fastener `{f.id}` designation `{f.designation}` not understood")
            continue
        d, ln = dl
        dr = np.asarray(f.dir, float)
        dr = dr / np.linalg.norm(dr)
        at = np.asarray(f.at, float)
        own = w.body(f.id)
        joint = set(f.through or []) | ({f.threads_into} if f.threads_into else set())
        skip = lambda b: b is own or b.is_wire or b.id in joint  # noqa: E731
        n += 1
        if not f.tool:
            key = fastener_catalog.drive_key(d, f.head if f.head in ("countersunk", "button") else None)[0]
            hit = driver_path_blocked(w, dr, at, d, key, r.profile.driver_access_len_mm, skip)
            if hit is not None:
                t, bid = hit
                out.append(fail("tool_access.blocked", G, BLOCKER, "Driver cannot reach the screw",
                                f"`{f.id}` ({f.designation}, no `tool` declared; its {key:g} mm hex key is assumed) is blocked "
                                f"by `{bid}` {t:.1f} mm above the head; the driver needs a clear straight path out.")
                           .on(f.id, bid).here(at - dr * t)
                           .fix("Declare `tool` for this screw and open a straight access hole, or move it out from "
                                "under the overhang."))
        tid = f.threads_into
        tp = r.spec.part(tid) if tid else None
        if tp is not None and tp.kind == "nut":
            nb = w.body(tid)
            if nb is None:
                ctx.not_checked.append(f"Tool access: nut `{tid}` of `{f.id}` is not a body, wrench clearance not checked")
                continue
            bid = nut_ring_blocked(w, f, dr, nb, r.profile.driver_access_radius_mm, joint | {f.id, tid})
            if bid is not None:
                out.append(fail("tool_access.nut_blocked", G, BLOCKER, "Wrench cannot reach the nut",
                                f"`{tid}` (the nut of `{f.id}`) is boxed in by `{bid}`: no spanner or socket fits around it, "
                                f"so the joint cannot be tightened.")
                           .on(tid, f.id, bid).here(np.asarray(nb.aabb, float).mean(axis=0))
                           .fix("Open a wrench pocket around the nut (or use a nut retained in a printed slot and "
                                "design the joint so the screw alone needs turning)."))
    if n and not out:
        out.append(ok("tool_access.ok", G, "Every fastener is reachable by its tool",
                      f"{n} fasteners: undeclared-tool screws have a clear driver path, every nut has wrench clearance."))
    elif not r.spec.fasteners:
        ctx.not_checked.append("Tool access: the spec declares no fasteners")
    return out
