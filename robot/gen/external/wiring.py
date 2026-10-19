"""Wires and the channels they run in.

Each wire is a Manhattan path between two port positions, cut as a 3 mm wide channel through the bottom half (from
the floor band up to the split face) so the router finds free space through every housing wall on the way.
"""

from __future__ import annotations

import math

from ..layout import geom
from . import sh

CH_W = 3.0
CH_Z = (-5.0, 0.5)


def port_world(plan, ref: str):
    """World position of `part.port` from the part's catalog/explicit ports and its at/rot (z-rotation only)."""
    if ref in plan.anchors:
        return plan.anchors[ref]
    from ... import catalog

    pid, _, port = ref.partition(".")
    p = plan.get(pid)
    if p is None:
        raise KeyError(f"wire end {ref}: no part {pid}")
    ports = dict(p.get("ports") or {})
    if not ports and p.get("catalog"):
        ports = dict(catalog.find(p["catalog"]).ports)
    lx, ly, lz = ports[port]
    a = math.radians(p["rot"][2])
    x, y, z = p["at"]
    return (x + lx * math.cos(a) - ly * math.sin(a), y + lx * math.sin(a) + ly * math.cos(a), z + lz)


GRID = 1.0


def grid_route(a, b, blocked, inside, step=GRID, free_rects=()):
    """A* over a `step` grid in XY from a to b, 4-connected, avoiding `blocked` rectangles grown by half a channel,
    staying inside the polygon `inside`; each turn costs 4 mm so channels stay straight. Returns corner points."""
    import heapq

    half = CH_W / 2 + 0.01
    grown = [(r[0] - half, r[1] + half, r[2] - half, r[3] + half) for r in blocked]
    inner = inside.buffer(-half)

    def key(p):
        return (round(p[0] / step), round(p[1] / step))

    def free(k):
        x, y = k[0] * step, k[1] * step
        if any(f[0] <= x <= f[1] and f[2] <= y <= f[3] for f in free_rects):
            return True
        if not inner.contains(_pt(x, y)):
            return False
        return not any(g[0] < x < g[1] and g[2] < y < g[3] for g in grown)

    start, goal = key(a), key(b)
    cache = {start: True, goal: True}
    openq = [(0.0, 0.0, start, None)]
    came, cost = {}, {(start, None): 0.0}
    while openq:
        _, g, k, d = heapq.heappop(openq)
        if k == goal:
            return _corners(a, b, _walk(came, (k, d)), step)
        for nd in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nk = (k[0] + nd[0], k[1] + nd[1])
            if nk not in cache:
                cache[nk] = free(nk)
            if not cache[nk]:
                continue
            ng = g + step + (4.0 if d is not None and d != nd else 0.0)
            if ng < cost.get((nk, nd), 1e18):
                cost[(nk, nd)] = ng
                came[(nk, nd)] = (k, d)
                h = (abs(nk[0] - goal[0]) + abs(nk[1] - goal[1])) * step
                heapq.heappush(openq, (ng + h, ng, nk, nd))
        if len(cache) > 200000:
            break
    return None


def _pt(x, y):
    from shapely.geometry import Point
    return Point(x, y)


def _walk(came, node):
    out = [node[0]]
    while node in came:
        node = came[node]
        out.append(node[0])
    return out[::-1]


def _corners(a, b, cells, step):
    pts = [(c[0] * step, c[1] * step) for c in cells]
    keep = [pts[0]]
    for i in range(1, len(pts) - 1):
        p0, p1, p2 = keep[-1], pts[i], pts[i + 1]
        if (p1[0] - p0[0]) * (p2[1] - p1[1]) != (p1[1] - p0[1]) * (p2[0] - p1[0]):
            keep.append(p1)
    keep.append(pts[-1])
    return [tuple(a[:2])] + [p for p in keep] + [tuple(b[:2])]


def channel_boxes(path, z=CH_Z):
    out = []
    for (ax, ay), (bx, by) in zip(path, path[1:]):
        if abs(ax - bx) < 1e-6 and abs(ay - by) < 1e-6:
            continue
        out.append(sh.boxr(min(ax, bx) - CH_W / 2, max(ax, bx) + CH_W / 2, min(ay, by) - CH_W / 2, max(ay, by) + CH_W / 2, *z))
    return out


def box_rects(shapes):
    """XY rectangles (x0, x1, y0, y1) of the unrotated boxes among `shapes`."""
    out = []
    for s in shapes:
        if s.get("type") == "place" and s["shape"].get("type") == "box" and not any(s["rot"]):
            (sx, sy, _), (x, y, _) = s["shape"]["size"], s["at"]
            out.append((x - sx / 2, x + sx / 2, y - sy / 2, y + sy / 2))
    return out


def pocket_rects(plan):
    """Cavity and housing outlines of every pocket (edges a channel must not run a sliver beside)."""
    out = []
    for p in plan.pockets:
        out.append((p.x0, p.x1, p.y0, p.y1))
        out += [n[:4] for n in p.notches]
        if p.housing > 0:
            out.append(p.outer())
    return out


def snap(rect, others, tol=1.0):
    """Move channel edges that would leave a sliver (< tol) next to another cavity's edge onto that edge."""
    x0, x1, y0, y1 = rect
    for o in others:
        if min(y1, o[3]) - max(y0, o[2]) > -tol:  # overlapping (or nearly) in y: x edges matter
            for e in (o[0], o[1]):
                if 0 < x0 - e < tol:
                    x0 = e
                if 0 < e - x1 < tol:
                    x1 = e
        if min(x1, o[1]) - max(x0, o[0]) > -tol:
            for e in (o[2], o[3]):
                if 0 < y0 - e < tol:
                    y0 = e
                if 0 < e - y1 < tol:
                    y1 = e
    return x0, x1, y0, y1


def exit_lane(pk, q, reach=CH_W + 2.0):
    """A one-cell-wide strip from port q straight out of pocket pk (along the axis the port is nearest the edge)."""
    d = {"-x": q[0] - pk.x0, "+x": pk.x1 - q[0], "-y": q[1] - pk.y0, "+y": pk.y1 - q[1]}
    side = min(d, key=d.get)
    x, y = q[0], q[1]
    if side == "-x":
        return (pk.x0 - reach, x, y - 0.4, y + 0.4)
    if side == "+x":
        return (x, pk.x1 + reach, y - 0.4, y + 0.4)
    if side == "-y":
        return (x - 0.4, x + 0.4, pk.y0 - reach, y)
    return (x - 0.4, x + 0.4, y, pk.y1 + reach)


def add_wire(plan, wid, a, b, kind, awg=26, slack=6.0, avoid=()):
    """Route one wire on the chassis plane and cut its channel into the bottom half."""
    from .shell import inner_outline
    from ..layout import geom as g2

    pa, pb = port_world(plan, a), port_world(plan, b)
    appr = plan.extra.get("approach", {})
    qa, qb = appr.get(a, pa), appr.get(b, pb)  # route to an approach point, then straight in to the port
    ends = {a.split(".")[0], b.split(".")[0]}
    blocked = [(k[1], k[2], k[3], k[4]) for k in plan.keepouts if k[0] not in avoid and not k[0].startswith("lane")]
    blocked += [(p.x0, p.x1, p.y0, p.y1) for p in plan.pockets if not (p.wire_through and p.id in ends)]
    # the only way into an end pocket: a straight exit from the port, outward from the pocket centre
    free = []
    for q, ref in ((qa, a), (qb, b)):
        free.append((q[0] - 0.5, q[0] + 0.5, q[1] - 0.5, q[1] + 0.5))
        pk = next((p for p in plan.pockets if p.id == ref.split(".")[0]), None)
        if pk is not None and q is (pa if ref == a else pb):
            free.append(exit_lane(pk, q))
    path = grid_route(qa, qb, blocked, g2.polygon(inner_outline(plan.frame)), free_rects=free)
    if path is None:
        raise ValueError(f"wire {wid}: no channel route from {a} to {b}")
    path = ([tuple(pa[:2])] if qa is not pa else []) + path + ([tuple(pb[:2])] if qb is not pb else [])
    others = box_rects(plan.cuts["bottom"]) + box_rects(plan.adds["bottom"]) + pocket_rects(plan)
    for ch in channel_boxes(path):
        (sx, sy, sz), (x, y, z) = ch["shape"]["size"], ch["at"]
        r = snap((x - sx / 2, x + sx / 2, y - sy / 2, y + sy / 2), others)
        plan.cut("bottom", sh.boxr(*r, z - sz / 2, z + sz / 2))
    plan.wires.append({"id": wid, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": slack})
    return path
