"""Count the changes that turn one robot spec into another (e.g. a generated spec into a hand-built reference).

Parts are matched by id first, then greedily by (kind, catalog) and nearest world position, then by kind alone.
Fasteners match by designation then nearest position; wires by the kinds of the parts at their ends; connections by
the kinds of their two parts plus the method. Every unmatched or differing item is one change.

Changes are split into *architectural* (a part kind or drive/weapon element appears or disappears, a joint method
between part kinds changes) and *detail* (moves, rotations, reshapes, materials, fasteners, wires).
"""

from __future__ import annotations

import json
import math
from collections import Counter

import numpy as np

from .. import xform

MOVE_MM = 2.0
ROT_DEG = 2.0
# part kinds whose presence is a detail (hardware, small printed fittings), not a design decision
DETAIL_KINDS = {"insert", "nut", "washer", "spacer", "standoff", "pin", "shaft", "screw", "bolt", "clip", "label",
                "cable_tie", "heatshrink", "connector", "other"}
CATEGORIES = ("parts_added", "parts_removed", "moved", "rotated", "reshaped", "material_process", "fasteners",
              "wires", "connections")


def _load(s):
    if isinstance(s, (str, bytes)) or hasattr(s, "__fspath__"):
        with open(s) as f:
            return json.load(f)
    return s


def world_poses(spec) -> dict:
    parts = {p["id"]: p for p in spec.get("parts", [])}
    out = {}

    def pose(pid, seen=()):
        if pid in out:
            return out[pid]
        p = parts[pid]
        M = xform.pose(p.get("at") or [0, 0, 0], p.get("rot") or [0, 0, 0])
        par = p.get("parent")
        if par in parts and par not in seen:
            M = pose(par, seen + (pid,)) @ M
        out[pid] = M
        return M

    for pid in parts:
        pose(pid)
    return out


def _rot_deg(A, B) -> float:
    R = A[:3, :3].T @ B[:3, :3]
    return math.degrees(math.acos(max(-1.0, min(1.0, (np.trace(R) - 1) / 2))))


def _canon(v):
    return json.dumps(v, sort_keys=True)


def match_parts(a, b) -> dict:
    """{id in a: id in b}."""
    pa, pb = {p["id"]: p for p in a["parts"]}, {p["id"]: p for p in b["parts"]}
    Ma, Mb = world_poses(a), world_poses(b)
    m = {i: i for i in pa if i in pb and pa[i].get("kind") == pb[i].get("kind")}
    free_b = set(pb) - set(m.values())
    for key in (lambda p: (p.get("kind"), p.get("catalog")), lambda p: p.get("kind")):
        cands = []
        for i in pa:
            if i in m:
                continue
            for j in free_b:
                if key(pa[i]) == key(pb[j]):
                    cands.append((float(np.linalg.norm(Ma[i][:3, 3] - Mb[j][:3, 3])), i, j))
        for _, i, j in sorted(cands):
            if i not in m and j in free_b:
                m[i] = j
                free_b.discard(j)
    return m


def _greedy(items_a, items_b, key, dist):
    used, pairs = set(), []
    unmatched_a = []
    for x in items_a:
        best = None
        for k, y in enumerate(items_b):
            if k in used or key(x) != key(y):
                continue
            d = dist(x, y)
            if best is None or d < best[0]:
                best = (d, k)
        if best is None:
            unmatched_a.append(x)
        else:
            used.add(best[1])
            pairs.append((x, items_b[best[1]]))
    return pairs, unmatched_a, [y for k, y in enumerate(items_b) if k not in used]


def diff(a, b) -> dict:
    """Changes from spec `a` to spec `b` (paths or dicts)."""
    a, b = _load(a), _load(b)
    pa, pb = {p["id"]: p for p in a["parts"]}, {p["id"]: p for p in b["parts"]}
    Ma, Mb = world_poses(a), world_poses(b)
    m = match_parts(a, b)
    items = {c: [] for c in CATEGORIES}
    arch = []
    for j in sorted(set(pb) - set(m.values())):
        items["parts_added"].append(j)
        if pb[j].get("kind") not in DETAIL_KINDS:
            arch.append(f"added {pb[j].get('kind')} `{j}`")
    for i in sorted(set(pa) - set(m)):
        items["parts_removed"].append(i)
        if pa[i].get("kind") not in DETAIL_KINDS:
            arch.append(f"removed {pa[i].get('kind')} `{i}`")
    for i, j in sorted(m.items()):
        A, B = Ma[i], Mb[j]
        d = float(np.linalg.norm(A[:3, 3] - B[:3, 3]))
        if d > MOVE_MM:
            items["moved"].append((i, j, round(d, 1)))
        r = _rot_deg(A, B)
        if r > ROT_DEG:
            items["rotated"].append((i, j, round(r, 1)))
        if _canon(pa[i].get("shape")) != _canon(pb[j].get("shape")) or pa[i].get("catalog") != pb[j].get("catalog") \
                or _canon(pa[i].get("model")) != _canon(pb[j].get("model")):
            items["reshaped"].append((i, j))
        if (pa[i].get("material"), pa[i].get("process")) != (pb[j].get("material"), pb[j].get("process")):
            items["material_process"].append((i, j, f"{pa[i].get('material')}/{pa[i].get('process')} -> "
                                                    f"{pb[j].get('material')}/{pb[j].get('process')}"))
    fa, fb = a.get("fasteners", []), b.get("fasteners", [])
    pairs, ua, ub = _greedy(fa, fb, lambda f: f.get("designation"),
                            lambda x, y: float(np.linalg.norm(np.subtract(x.get("at", [0] * 3), y.get("at", [0] * 3)))))
    items["fasteners"] = [("removed", f["id"], f.get("designation")) for f in ua] + \
                         [("added", f["id"], f.get("designation")) for f in ub] + \
                         [("moved", x["id"], y["id"]) for x, y in pairs
                          if np.linalg.norm(np.subtract(x.get("at", [0] * 3), y.get("at", [0] * 3))) > MOVE_MM]
    ka = {p["id"]: p.get("kind") for p in a["parts"]}
    kb = {p["id"]: p.get("kind") for p in b["parts"]}

    def wkey(kinds):
        return lambda w: tuple(sorted(kinds.get(str(w.get(e, "")).split(".")[0], "?") for e in ("from", "to")))

    wa = Counter(map(wkey(ka), a.get("wires", [])))
    wb = Counter(map(wkey(kb), b.get("wires", [])))
    items["wires"] = [("removed", k) for k in wa for _ in range(max(wa[k] - wb[k], 0))] + \
                     [("added", k) for k in wb for _ in range(max(wb[k] - wa[k], 0))]

    def ckey(kinds):
        return lambda c: (tuple(sorted((kinds.get(c.get("a"), "?"), kinds.get(c.get("b"), "?")))), c.get("method"))

    ca, cb = Counter(map(ckey(ka), a.get("connections", []))), Counter(map(ckey(kb), b.get("connections", [])))
    for k in sorted(set(ca) | set(cb), key=str):
        n = cb[k] - ca[k]
        if n:
            items["connections"].append((k[0], k[1], n))
            pair_methods_a = {kk[1] for kk in ca if kk[0] == k[0]}
            if k[1] not in pair_methods_a and n > 0 and pair_methods_a:
                arch.append(f"{k[0][0]}-{k[0][1]} joined by {k[1]} instead of {', '.join(sorted(map(str, pair_methods_a)))}")
    counts = {c: len(v) for c, v in items.items()}
    total = sum(counts.values())
    return {"counts": counts, "total": total, "architectural": arch, "n_architectural": len(arch),
            "n_detail": total - len(arch), "items": items, "matched": m}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(prog="robot.gen.diff", description=__doc__.splitlines()[0])
    ap.add_argument("a")
    ap.add_argument("b")
    args = ap.parse_args(argv)
    d = diff(args.a, args.b)
    print(json.dumps({k: d[k] for k in ("counts", "total", "n_architectural", "n_detail", "architectural")}, indent=1))


if __name__ == "__main__":
    main()
