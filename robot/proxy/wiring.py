"""Fast proxy for `wiring`: replay the routes of the last full run against the current geometry.

The full group voxelises the robot and runs A* per wire. Here every baseline route (report.json `routes`) is sampled
every SAMPLE_MM along its polyline and each sample must still clear every body by the wire radius + CLEAR_MARGIN_MM
(less GRID_SLACK_MM, the router's own cell-centre leniency)
(point-to-surface distance; the band around each route only meets bodies whose AABB it reaches), stay inside the
structure envelope, and its ends must still sit on the wire's ports (PORT_MOVE_MM). Wheels, weapons, pulleys and belts
count as their padded AABB, as in the router. A wire with no baseline route, a moved port or a blocked sample is
flagged `proxy.wiring` (the full router may still find another path: a false alarm, never a miss).
"""

from __future__ import annotations

import numpy as np

from ..checks import wiring as wr
from ..finding import BLOCKER, WARNING, fail, ok

G = "proxy"
SAMPLE_MM = 0.25  # same step as the router's segment_free
CLEAR_MARGIN_MM = 0.05  # router: dist >= r + 0.05
GRID_SLACK_MM = wr.CELL * 3 ** 0.5 / 2  # the router reads distance at the cell centre: a sample may sit this far off
PORT_MOVE_MM = 0.3  # an end that moved further than this re-routes in the full run
BOX_PAD_KINDS = ("wheel", "weapon", "pulley", "belt")
BOX_PAD_MM = 0.6  # router pads these AABBs
STRUCT_INSET_MM = 0.4  # router: cells outside the structure AABB shrunk by this are solid


def sample(points, step=SAMPLE_MM):
    pts = np.asarray(points, float)
    if len(pts) < 2:
        return pts
    out = [pts[0]]
    for p, q in zip(pts, pts[1:]):
        k = max(int(np.ceil(np.linalg.norm(q - p) / step)), 1)
        out += [p + (q - p) * t for t in np.linspace(0, 1, k + 1)[1:]]
    return np.asarray(out)


def blocked(world, P, r, ends):
    """Per sample: (bool blocked, id of the body that blocks it or '')."""
    near = np.zeros(len(P), bool)
    for e in ends:
        near |= np.linalg.norm(P - e, axis=1) < wr.PORT_ZONE
    hit = np.zeros(len(P), bool)
    who = np.full(len(P), "", object)
    structs = [b.aabb for b in world.bodies if b.kind == "structure"]
    if structs:
        lo = np.min([s[0] for s in structs], 0) + STRUCT_INSET_MM
        hi = np.max([s[1] for s in structs], 0) - STRUCT_INSET_MM
        out = ~np.all((P >= lo) & (P <= hi), axis=1)
        hit |= out
        who[out] = "outside the structure"
    reach = r + CLEAR_MARGIN_MM - GRID_SLACK_MM
    for b in world.bodies:
        if b.is_wire:
            continue
        lo, hi = b.aabb
        pad = BOX_PAD_MM if b.kind in BOX_PAD_KINDS else 0.0
        m = np.all((P >= lo - pad - reach) & (P <= hi + pad + reach), axis=1) & ~near & ~hit
        if not m.any():
            continue
        if pad:
            bad = np.all((P[m] >= lo - pad) & (P[m] <= hi + pad), axis=1)
        else:
            bad = b.sdf(P[m]) < reach
        idx = np.flatnonzero(m)[bad]
        hit[idx] = True
        who[idx] = b.id
    return hit, who


def run(ctx, routes, parts=None):
    """routes: baseline [{id, od_mm, points}] from a full report. parts: only wires with an end on these parts."""
    r, world = ctx.r, ctx.world
    base = {x["id"]: x for x in routes or []}
    out, nok = [], 0
    for w in r.spec.wires:
        wf, wt = wr._from(w), w.to
        if parts is not None and wf.split(".")[0] not in parts and wt.split(".")[0] not in parts:
            continue
        a, b = world.port(r, wf), world.port(r, wt)
        rt = base.get(w.id)
        why, at = None, None
        if a is None or b is None:
            why = "a port does not exist"
        elif rt is None or len(rt.get("points") or []) < 2:
            why = "no baseline route (run the full `wiring` group once and pass its report)"
        else:
            P = np.asarray(rt["points"], float)
            a, b = np.asarray(a, float), np.asarray(b, float)
            moved = max(np.linalg.norm(P[0] - a), np.linalg.norm(P[-1] - b))
            if moved > PORT_MOVE_MM:
                why, at = f"its ports moved {moved:.2f} mm since the baseline route", a
            else:
                S = sample(P)
                hit, who = blocked(world, S, float(rt["od_mm"]) / 2, [a, b])
                if hit.any():
                    k = int(np.flatnonzero(hit)[0])
                    why, at = f"the baseline route is now blocked by `{who[k]}` ({int(hit.sum())} samples)", S[k]
        if why:
            f = fail("proxy.wiring", G, BLOCKER, "Wire route likely broken", f"Wire `{w.id}` (`{wf}` to `{wt}`): {why}.").on(wf, wt)
            out.append((f.here(at) if at is not None else f).fix("Run the full `wiring` group to re-route it."))
        else:
            nok += 1
        bend = wr.sharp_bend(rt["points"], float(rt["od_mm"])) if rt and len(rt.get("points") or []) > 2 else None
        if bend is not None:
            out.append(fail("proxy.wiring_bend", G, WARNING, "Wire bends too tightly",
                            f"Wire `{w.id}` turns {bend[1]:.0f} degrees on its baseline route.").here(bend[0]))
    if not any(f.id == "proxy.wiring" for f in out):
        out.append(ok("proxy.wiring", G, "Baseline wire routes still clear", f"{nok} routes replayed clear of every body."))
    return out
