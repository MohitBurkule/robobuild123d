"""Disassembly dependency graph.

Nodes are part ids and fastener ids. An edge X -> Y means "X must be removed before Y can be reached / removed":

* driver line: a part (or another screw) sits in the screwdriver's straight path out of fastener Y's head -> X before Y;
* clamp: fastener F passes through or threads into part P -> F before P;
* trapped: part P cannot move in any axis direction because of parts B (``captive`` map from the interference group)
  -> each B before P.

Permanent parts (heat-set inserts, nuts, parts fused to another, `fixed` structure that never comes off) are still nodes,
but nothing needs them removed: they are not counted as removals.
"""

from __future__ import annotations

import numpy as np

from .. import catalog

PERMANENT_KINDS = {"insert", "nut"}


def _perp(d):
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(d, a)
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    return u, v / np.linalg.norm(v)


def driver_blockers(w, f, reach_mm, tool_radius=1.3, step=0.5):
    """Ids of every body (part or other screw) inside the driver cylinder straight out of the head of `f`, in path order."""
    dl = catalog.parse_designation(f.designation)
    if not dl:
        return None
    d, _ = dl
    k = catalog.screw_dims(d)[1]
    dr = np.asarray(f.dir, float)
    n = np.linalg.norm(dr)
    if not n > 1e-9:
        return None
    dr = dr / n
    top = np.asarray(f.at, float) - dr * k
    u, v = _perp(dr)
    pts, ts = [], []
    for s in range(int(reach_mm / step) + 1):
        t = s * step
        c = top - dr * (t + 0.05)
        for a in range(9):
            ang = a * np.pi / 4
            pts.append(c if a == 8 else c + u * (tool_radius * np.cos(ang)) + v * (tool_radius * np.sin(ang)))
            ts.append(t)
    P, ts = np.array(pts), np.array(ts)
    lo, hi = P.min(0), P.max(0)
    hits = []
    own = {f.id}
    for b in w.bodies:
        if b.id in own or b.is_wire:
            continue
        blo, bhi = b.aabb
        if np.any(bhi < lo) or np.any(blo > hi):
            continue
        ins = b.inside(P)
        if ins.any():
            hits.append((float(ts[ins].min()), b.id))
    return [bid for _, bid in sorted(hits)]


class Graph:
    def __init__(self):
        self.nodes = {}  # id -> "part" | "fastener"
        self.before = {}  # node -> {node: reason}: predecessors that must come off first
        self.permanent = set()

    def add_node(self, nid, kind):
        self.nodes.setdefault(nid, kind)
        self.before.setdefault(nid, {})

    def add_edge(self, first, then, why):
        if first == then or first not in self.nodes or then not in self.nodes:
            return
        self.before[then].setdefault(first, why)

    def deps(self, nid):
        """Transitive set of nodes that must be removed before `nid` (excluding it)."""
        seen, stack = set(), list(self.before.get(nid, {}))
        while stack:
            x = stack.pop()
            if x in seen or x == nid:
                continue
            seen.add(x)
            stack.extend(self.before.get(x, {}))
        return seen

    def removals(self, nid):
        """Removals needed to free `nid`: its dependency set without permanent parts."""
        return sorted(x for x in self.deps(nid) if x not in self.permanent)

    def cycles(self):
        """Strongly connected components with more than one node (or a self-loop): disassembly deadlocks."""
        index, low, on, st, out = {}, {}, set(), [], []
        counter = [0]

        def strong(v):
            index[v] = low[v] = counter[0]
            counter[0] += 1
            st.append(v)
            on.add(v)
            for wv in self.before[v]:
                if wv not in index:
                    strong(wv)
                    low[v] = min(low[v], low[wv])
                elif wv in on:
                    low[v] = min(low[v], index[wv])
            if low[v] == index[v]:
                comp = []
                while True:
                    x = st.pop()
                    on.discard(x)
                    comp.append(x)
                    if x == v:
                        break
                if len(comp) > 1:
                    out.append(sorted(comp))

        import sys
        old = sys.getrecursionlimit()
        sys.setrecursionlimit(max(old, 4 * len(self.nodes) + 100))
        try:
            for v in list(self.nodes):
                if v not in index:
                    strong(v)
        finally:
            sys.setrecursionlimit(old)
        return out

    def order(self, nid):
        """A removal order (topological over the dependency set) that frees `nid`, or None if it sits on a cycle."""
        need = self.deps(nid) | {nid}
        done, seq = set(), []
        while len(done) < len(need):
            ready = sorted(x for x in need - done if all(p in done or p not in need for p in self.before[x]))
            if not ready:
                return None
            for x in ready:
                done.add(x)
                seq.append(x)
        return [x for x in seq if x != nid and x not in self.permanent]


def build(r, w, captive=None, reach_mm=None):
    """Build the disassembly graph of resolved spec `r` in world `w`. Returns (graph, unknown) where `unknown` lists
    fasteners whose driver line could not be evaluated."""
    g = Graph()
    reach = reach_mm if reach_mm is not None else getattr(r.profile, "driver_access_len_mm", 40.0)
    for p in r.spec.parts:
        g.add_node(p.id, "part")
        if p.kind in PERMANENT_KINDS or p.fused_with is not None:
            g.permanent.add(p.id)
    for f in r.spec.fasteners:
        g.add_node(f.id, "fastener")
    unknown = []
    for f in r.spec.fasteners:
        held = set(f.through or []) | ({f.threads_into} if f.threads_into else set())
        for pid in held:
            g.add_edge(f.id, pid, f"`{f.id}` clamps it")
        hits = driver_blockers(w, f, reach)
        if hits is None:
            unknown.append(f.id)
            continue
        for bid in hits:
            if bid in held:
                continue
            g.add_edge(bid, f.id, f"`{bid}` is in the driver line of `{f.id}`")
    for pid, blockers in (captive or {}).items():
        for bid in blockers:
            # mutual trapping (a clamped stack) comes apart as one unit once its screws are out: no ordering edge
            if bid in g.permanent or pid in (captive or {}).get(bid, ()):
                continue
            g.add_edge(bid, pid, f"`{pid}` is trapped by `{bid}`")
    # A permanent part comes off with its host; the host's removal also needs whatever traps the permanent part.
    return g, unknown
