"""Wire chafe, bend radius and connector strain relief (`wire_care.*`, G5).

WHY: the deep `wiring` router proves a wire FITS, and `electrical`'s bend rule only runs
when routes exist. The declared harness (from/to ports + `via` waypoints) already says
where a wire bends and what it crosses, so three builder judgements need no router:

wire_care.bend (WARNING): a bend at a `via` corner tighter than `bend_x_od` x the wire's
outer diameter (default 2, the same floor as the routed-wire rule) fatigues the strands.
wire_care.chafe (WARNING): the wire passes THROUGH a thin wall of a part it does not
terminate on (in and out of the part's extent along one axis inside `wall_max_mm` of run,
never inside the solid, so through a hole) - the hole edge saws the insulation; opt out
with `grommet: true` on the wire.
wire_care.strain_relief (WARNING): a wire ending on a vibrating part (motor, weapon_motor,
servo) needs declared relief: a `via` anchor within `relief_dist_mm` of that end, or
`slack_mm`, or a `strain_relief` note on the wire.

A wire whose ports do not resolve is NOT CHECKED (never a pass).
"""

from __future__ import annotations

import numpy as np

from ..finding import WARNING, fail, ok
from ._review import params, x
from .wiring import default_awg, wire_od

G = "wire_care"
DEFAULTS = {"bend_x_od": 2.0, "wall_max_mm": 6.0, "relief_dist_mm": 12.0}
VIBRATING = {"motor", "weapon_motor", "servo"}
PORT_ZONE_MM = 2.6  # matches wiring.PORT_ZONE: a wire may touch its own part near its port


def _from(w):
    return getattr(w, "from", None) or getattr(w, "from_", "")


def wire_points(world, r, w):
    a = world.port(r, _from(w))
    b = world.port(r, w.to)
    if a is None or b is None:
        return None
    return np.array([a] + [list(v) for v in (w.via or [])] + [b], float)


def bend_radius(P):
    """(index, radius) of the tightest via corner of polyline P, or (None, inf) when there is none."""
    worst = (None, np.inf)
    for i in range(1, len(P) - 1):
        a, b, c = P[i - 1], P[i], P[i + 1]
        ab, bc = np.linalg.norm(b - a), np.linalg.norm(c - b)
        if ab < 1.0 or bc < 1.0:  # a port stub or a duplicated point is not a bend
            continue
        area = np.linalg.norm(np.cross(b - a, c - a)) / 2.0
        if area < 1e-6:
            continue
        r = ab * bc * np.linalg.norm(c - a) / (4.0 * area)
        if r < worst[1]:
            worst = (i, r)
    return worst


def crosses_wall(world, w, P, wall_max):
    """(part id) of a thin wall the wire passes through, or None. A hole crossing: in and out of the part's
    extent along one axis within `wall_max` of run, never inside the solid."""
    ends = {_from(w).split(".", 1)[0], str(w.to).split(".", 1)[0]}
    lo, hi = P.min(axis=0), P.max(axis=0)
    for b in world.bodies:
        if getattr(b, "is_wire", False) or b.id in ends or b.part_idx is None:
            continue
        blo, bhi = np.asarray(b.aabb, float)
        if np.any(bhi < lo - 0.1) or np.any(blo > hi + 0.1):
            continue
        inside_slab = (P[:, 0] >= blo[0]) & (P[:, 0] <= bhi[0]) & (P[:, 1] >= blo[1]) & (P[:, 1] <= bhi[1]) \
            & (P[:, 2] >= blo[2]) & (P[:, 2] <= bhi[2])
        idx = np.nonzero(inside_slab)[0]
        if len(idx) == 0 or idx[0] == 0 or idx[-1] == len(P) - 1:
            continue  # never inside the part's extent, or the wire ends inside it
        if np.linalg.norm(P[idx[-1]] - P[idx[0]]) > wall_max:
            continue  # a long run inside the part (a pocket or channel), not a wall crossing
        if bool(b.inside(P[idx]).any()):
            continue  # through the material, not a hole (internal.* owns that)
        for ax in range(3):
            below = np.nonzero(P[:, ax] < blo[ax] - 1e-9)[0]
            above = np.nonzero(P[:, ax] > bhi[ax] + 1e-9)[0]
            if len(below) and len(above) and (below[0] < idx[0] < above[-1] or above[0] < idx[0] < below[-1]):
                return b.id
    return None


def run(ctx):
    r, w = ctx.r, ctx.world
    p = params(r.spec, "wire_care", DEFAULTS)
    out, n = [], 0
    for wi in r.spec.wires:
        P = wire_points(w, r, wi)
        if P is None:
            ctx.not_checked.append(f"Wire care: `{wi.id}` ports {_from(wi)} / {wi.to} do not resolve")
            continue
        n += 1
        od = wire_od(float(wi.awg) if wi.awg is not None else default_awg(wi.kind))
        i, rr = bend_radius(P)
        if i is not None and rr < p["bend_x_od"] * od:
            out.append(fail("wire_care.bend", G, WARNING, "Wire bends tighter than its fatigue limit",
                            f"`{wi.id}` turns a {rr:.1f} mm radius bend at via {list(map(float, P[i]))}; "
                            f"{p['bend_x_od']:.0f} x its {od:.1f} mm diameter is the floor.")
                       .on(wi.id).here(P[i])
                       .fix("Move the via so the bend opens up, or add a waypoint: a tight kink work-hardens the "
                            "strands and the lead fails at the connector."))
        if not x(wi, "grommet", False):
            bid = crosses_wall(w, wi, P, p["wall_max_mm"])
            if bid is not None:
                out.append(fail("wire_care.chafe", G, WARNING, "Wire crosses a bare hole edge",
                                f"`{wi.id}` passes through `{bid}` with no grommet: the hole edge saws the insulation "
                                f"with every hit and the print's layer lines are a rasp.")
                           .on(wi.id, bid).here(P[len(P) // 2])
                           .fix("Line the hole with an edge clip / grommet, deburr and open the hole, or reroute; "
                                "declare `grommet: true` on the wire when it is protected."))
        for end_name, end_pt in ((_from(wi), P[0]), (wi.to, P[-1])):
            pid = str(end_name).split(".", 1)[0]
            part = r.spec.part(pid)
            if part is None or part.kind not in VIBRATING:
                continue
            anchored = any(np.linalg.norm(np.asarray(v, float) - end_pt) <= p["relief_dist_mm"] for v in (wi.via or []))
            if not anchored and wi.slack_mm is None and not x(wi, "strain_relief"):
                out.append(fail("wire_care.strain_relief", G, WARNING, "No strain relief at a vibrating connector",
                                f"`{wi.id}` ends on `{pid}` with no anchor within {p['relief_dist_mm']:.0f} mm, no "
                                f"`slack_mm` and no `strain_relief` note: vibration works the crimp until it fails.")
                           .on(wi.id, pid).here(end_pt)
                           .fix("Zip-tie the lead to a boss within a few mm of the connector (add the point as a "
                                "`via`), declare `slack_mm`, or note the connector's own clamp as `strain_relief`."))
    if n and not out:
        out.append(ok("wire_care.ok", G, "Wires bend easy, cross walls protected, end anchored",
                      f"{n} wires: no bend under the floor, no bare hole crossings, every vibrating end anchored."))
    elif not r.spec.wires:
        ctx.not_checked.append("Wire care: the spec declares no wires")
    return out
