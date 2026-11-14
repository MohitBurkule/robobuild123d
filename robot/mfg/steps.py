"""Ordered assembly steps from the part tree (parent/joint), fasteners (through/threads_into) and declared teardown.

Order: reverse of the declared teardown (service order), then remaining parts parent-before-child (topological),
inserts/nuts installed into their host before anything screws into them. Each step lists the screws that close it.
"""

from __future__ import annotations

from collections import defaultdict

from ._util import x


def _topo(spec):
    kids, ids = defaultdict(list), [p.id for p in spec.parts]
    for p in spec.parts:
        if x(p, "parent"):
            kids[x(p, "parent")].append(p.id)
    roots = [i for i in ids if not x(spec.part(i), "parent") or spec.part(x(spec.part(i), "parent")) is None]
    out, seen = [], set()

    def walk(i):
        if i in seen:
            return
        seen.add(i)
        out.append(i)
        for k in kids[i]:
            walk(k)

    for r in roots:
        walk(r)
    out += [i for i in ids if i not in seen]  # cycles: keep spec order
    return out


def assembly_steps(spec):
    order = _topo(spec)
    # teardown declared as remove-order; assembly installs those groups last, in reverse
    late = []
    for t in reversed(spec.teardown or []):
        g = [i for i in t.get("parts", []) if i in order]
        late.append((g, t.get("reason")))
    late_ids = {i for g, _ in late for i in g}
    # inserts / nuts first into their host
    pre = [p.id for p in spec.parts if p.kind in ("insert", "nut")]
    body = [i for i in order if i not in late_ids and i not in pre]
    groups = [([i], None) for i in pre] + [([i], None) for i in body] + late
    placed, steps = set(), []
    pending = list(spec.fasteners)
    for g, why in groups:
        placed |= set(g)
        closes = [f for f in pending if set(list(f.through or []) + ([f.threads_into] if f.threads_into else [])) <= placed]
        pending = [f for f in pending if f not in closes]
        verb = "Press heat-set insert" if spec.part(g[0]).kind == "insert" else "Fit"
        host = x(spec.part(g[0]), "parent")
        steps.append({"n": len(steps) + 1, "parts": g,
                      "text": f"{verb} {', '.join(g)}" + (f" onto {host}" if host else "") + (f" ({why})" if why else ""),
                      "fasteners": [{"id": f.id, "designation": f.designation, "tool": f.tool,
                                     "into": f.threads_into} for f in closes]})
    if pending:
        steps.append({"n": len(steps) + 1, "parts": [], "text": "Remaining screws (hosts not in part list)",
                      "fasteners": [{"id": f.id, "designation": f.designation, "tool": f.tool,
                                     "into": f.threads_into} for f in pending]})
    return steps
