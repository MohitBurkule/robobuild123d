"""Backtracking CSP over a discrete grid: place every component, keep the top-K distinct layouts by objective.

Pure python and deterministic for a given `seed`: candidates are generated on a grid aligned to the origin, filtered by
the unary constraints, ordered by a cheap per-component heuristic (ties broken by a seeded RNG), and searched depth
first with the binary constraints checked at each step. The node budget bounds the run time.
"""

from __future__ import annotations

import math
import random

from . import constraints, geom, objectives
from .model import Layout, LayoutInputs, Placement

BRANCH_TOP = 16  # values tried for the first component (diversity of the top-K)
BRANCH = 5  # values tried deeper


def _grid(lo, hi, step):
    k0, k1 = math.ceil(lo / step), math.floor(hi / step)
    return [k * step for k in range(k0, k1 + 1)]


def candidates(inp: LayoutInputs, comp) -> list:
    """Every placement of one component allowed by the unary constraints, best first."""
    z = comp.fixed_at[2] if comp.fixed_at is not None and len(comp.fixed_at) > 2 else 0.0
    if comp.fixed_at is not None:
        xs, ys = [comp.fixed_at[0]], [comp.fixed_at[1]]
    else:
        x0, x1, y0, y1 = geom.bounds(inp.outline)
        xs, ys = _grid(x0, x1, inp.grid), _grid(y0, y1, inp.grid)
    out = []
    for rz in comp.rot_choices:
        fp, ext = comp.footprint(rz), comp.extent(rz)
        for x in xs:
            for y in ys:
                pl = Placement(comp.id, x, y, z, rz, fp, ext)
                if constraints.unary_ok(inp, comp, pl):
                    out.append(pl)
    rng = random.Random(f"{inp.seed}:{comp.id}")
    keyed = [(_heuristic(inp, comp, p), rng.random(), p) for p in out]
    keyed.sort(key=lambda t: (t[0], t[1]))
    return [p for _, _, p in keyed]


def _heuristic(inp, comp, pl) -> float:
    """Mass pulls a component to the CoG target; wires pull it toward the anchors it links to."""
    h = comp.mass_g * math.hypot(pl.x - inp.cog_target[0], pl.y - inp.cog_target[1]) * 0.2
    for l in inp.links:
        for mine, other in ((l.a, l.b), (l.b, l.a)):
            if mine.split(".")[0] == comp.id and other in inp.anchors:
                h += 0.05 * geom.manhattan((pl.x, pl.y), inp.anchors[other])
    return h


def _thin(cands, n):
    """Keep n candidates: the best half (no two within 4 mm at the same rotation) plus an even spread of the rest,
    so later components still find room when the best spots are taken."""
    kept = []
    for p in cands:
        if all(p.rot_z != q.rot_z or abs(p.x - q.x) + abs(p.y - q.y) >= 4.0 for q in kept):
            kept.append(p)
        if len(kept) >= n // 2:
            break
    rest = [p for p in cands if p not in kept]
    if rest:
        step = max(1, len(rest) // max(1, n - len(kept)))
        kept += rest[::step][: n - len(kept)]
    return kept


def distinct(a: dict, b: dict, tol: float = 4.0) -> bool:
    return any(abs(a[k].x - b[k].x) > tol or abs(a[k].y - b[k].y) > tol or a[k].rot_z != b[k].rot_z for k in a)


def solve(inp: LayoutInputs | dict, k: int = 5, weights=None) -> list[Layout]:
    """Top-k distinct layouts (best first). Raises ValueError naming the component that cannot be placed."""
    if isinstance(inp, dict):
        inp = LayoutInputs.from_dict(inp)
    domains = {}
    for c in inp.components:
        cs = candidates(inp, c)
        if not cs:
            raise ValueError(f"no legal position for `{c.id}` (size {c.size}) inside the outline")
        domains[c.id] = cs
    if not domains:
        return [Layout({}, 0.0, {})]
    found = []
    budget = [inp.max_nodes]

    def dfs(placed, doms, depth):
        """Forward-checking DFS: branch on the most constrained component (fewest values left)."""
        if not doms:
            pls = {p.id: p for p in placed}
            score, terms = objectives.evaluate(inp, pls, weights)
            found.append(Layout(pls, score, terms))
            return
        cid = min(doms, key=lambda k: (len(doms[k]), k))
        for pl in _thin(doms[cid], BRANCH_TOP if depth == 0 else BRANCH):
            budget[0] -= 1
            if budget[0] <= 0:
                return
            rest = {}
            for k, d in doms.items():
                if k == cid:
                    continue
                rest[k] = [q for q in d if constraints.binary_ok(inp, q, [pl])]
                if not rest[k]:
                    break
            else:
                placed.append(pl)
                dfs(placed, rest, depth + 1)
                placed.pop()

    dfs([], domains, 0)
    if not found:
        raise ValueError("components do not fit together inside the outline (no layout satisfies every constraint)")
    found.sort(key=lambda l: l.score)
    best = []
    for lay in found:
        if all(distinct(lay.placements, b.placements) for b in best):
            best.append(lay)
        if len(best) >= k:
            break
    return best
