"""Jiggle: nudge movable parts until collisions (and optional clearance gaps) are gone, measured on the meshes.

Small LLMs burn most of a repair loop hand-computing radii and overlaps. This does it for them: it takes the spec,
moves only the parts you allow (default: every part placed by a numeric `at` that is not structure), carries each
part's children with it (linked by `parent`), and greedily applies the shortest single-axis move that lowers the
total violation without creating a new collision. Fixed parts (structure, the tub) never move.

    python3 -m robot jiggle spec.json [--move a,b] [--max-move 5] [--clear 0.3] [--write out.json]

Output: per part the world shift and the new `at` (in the part's own parent frame), plus what is still left.
It does not edit model code: a part whose placement comes from a model param is reported with its world shift so
the param can be changed by that amount (e.g. SWITCH_BAY +0.62). Re-run `robot verify` afterwards: jiggle only
scores overlaps and gaps, the full check set decides.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

FIXED_KINDS = {"structure", "chassis", "armour", "armor", "panel"}


@dataclass
class JiggleResult:
    start: float
    final: float
    moves: list = field(default_factory=list)        # [{part, axis, mm, vec}] in order
    shift: dict = field(default_factory=dict)        # part -> total world shift
    new_at: dict = field(default_factory=dict)       # part -> new `at` in its parent frame
    left: list = field(default_factory=list)         # [(a, b, depth or shortfall, what)]
    spec: dict | None = None

    def report(self) -> str:
        lines = [f"violation {self.start:.3f} -> {self.final:.3f} mm ({len(self.moves)} moves)"]
        for p, v in self.shift.items():
            at = self.new_at.get(p)
            lines.append(f"  {p}: shift ({v[0]:+.2f}, {v[1]:+.2f}, {v[2]:+.2f}) mm" + (f" -> at {at}" if at else " (placed by model code: change its param by this)"))
        lines += [f"  still: `{a}` / `{b}` {what} {d:.2f} mm" for a, b, d, what in self.left] or ["  nothing left"]
        return "\n".join(lines)


def _violations(world, ids, allow_fn, clear, measure):
    """[(a, b, amount, what)] for pairs involving a body in `ids`."""
    out = []
    bs = [b for b in world.bodies if not b.is_wire]
    for i, a in enumerate(bs):
        for b in bs[i + 1:]:
            if a.id not in ids and b.id not in ids:
                continue
            allow = allow_fn(a, b)
            if not np.isfinite(allow):
                continue
            if measure.aabb_overlap(a.aabb, b.aabb, clear):
                o = measure.overlap(a, b, cap=allow)
                if o is not None and o.depth > allow:
                    out.append((a.id, b.id, float(o.depth - allow), "overlap"))
                    continue
                if clear > 0:
                    g = measure.min_gap(a, b, clear * 2)
                    if 1e-6 < g < clear:   # touching (0) is a deliberate contact, not a clearance problem
                        out.append((a.id, b.id, float(clear - g), "gap short"))
    return out


def solve(spec_path, move=None, max_move=5.0, clear=0.0, max_iter=40, fast=True, log=print):
    from .. import escape, measure, spec as spec_mod, world as world_mod
    from ..checks import interference as itf

    s = spec_mod.load(spec_path)
    r = world_mod.resolve(s, fast=fast)
    w = world_mod.World.start(r)
    parts = {p.id: p for p in s.parts}

    def numeric_at(p):
        return isinstance(p.at, (list, tuple)) and len(p.at) == 3 and not p._extra.get("mate")

    movable = set(move) if move else {p.id for p in s.parts if numeric_at(p) and p.kind not in FIXED_KINDS}
    carry = {pid: itf.descendants(r, pid) for pid in movable}
    allow_fn = lambda a, b: itf.allowed_depth(r, a, b)  # noqa: E731
    shift = {pid: np.zeros(3) for pid in movable}

    def total(vs):
        return float(sum(v[2] for v in vs))

    vs = _violations(w, movable | {x for c in carry.values() for x in c}, allow_fn, clear, measure)
    start = cur = total(vs)
    moves = []
    tried = set()
    for _ in range(max_iter):
        if not vs:
            break
        vs.sort(key=lambda v: -v[2])
        best = None
        for a_id, b_id, amt, what in vs:
            a, b = w.body(a_id), w.body(b_id)
            mv = [x for x in (a_id, b_id) if x in movable]
            if not mv:
                continue
            allow = allow_fn(a, b) + (clear if what == "gap short" else 0.0)
            for m in escape.options(w, a, b, allow, allow_fn, movers=set(mv), carry=lambda p: carry[p]):
                key = (m.part, m.axis, round(m.mm, 2))
                if key in tried or np.linalg.norm(shift[m.part] + m.vec) > max_move:
                    continue
                tried.add(key)
                w2 = _shifted(w, carry[m.part], np.asarray(m.vec))
                vs2 = _violations(w2, movable | set(carry[m.part]), allow_fn, clear, measure)
                t2 = total(vs2)
                if t2 < cur - 1e-4 and (best is None or t2 < best[0]):
                    best = (t2, m, w2, vs2)
                if best is not None and not m.new_hits:
                    break
            if best is not None:
                break
        if best is None:
            break
        cur, m, w, vs = best
        shift[m.part] = shift[m.part] + np.asarray(m.vec)
        moves.append(m.to_dict())
        log(f"  {m.text()}  -> violation {cur:.3f} mm")
    raw = copy.deepcopy(s.raw)
    by_id = {p["id"]: p for p in raw.get("parts", []) if isinstance(p, dict) and "id" in p}
    res = JiggleResult(start, cur, moves, {}, {}, [(a, b, d, what) for a, b, d, what in vs], raw)
    for pid, v in shift.items():
        if not np.any(np.abs(v) > 1e-9):
            continue
        res.shift[pid] = [round(float(x), 3) for x in v]
        p = parts[pid]
        local = v
        if p.parent and p.parent in {q.id for q in s.parts}:
            R = np.asarray(w.body(p.parent).M, float)[:3, :3]   # parents never move with this part
            local = R.T @ v
        if numeric_at(p) and pid in by_id:
            new = [round(float(a) + float(d), 3) for a, d in zip(p.at, local)]
            by_id[pid]["at"] = new
            res.new_at[pid] = new
    return res


def _shifted(world, ids, vec):
    """Copy of the world with the bodies in `ids` moved by vec (fasteners stay: re-check them in verify)."""
    w2 = world.copy()
    w2.bodies = [b.moved(vec) if b.id in ids else b for b in world.bodies]
    w2._idx = {b.id: i for i, b in enumerate(w2.bodies)}
    return w2


def add_cli(sub):
    p = sub.add_parser("jiggle", help="nudge movable parts until collisions/clearances clear (measured, not guessed)")
    p.add_argument("spec")
    p.add_argument("--move", help="comma-separated part ids allowed to move (default: non-structure parts with a numeric `at`)")
    p.add_argument("--max-move", type=float, default=5.0, help="max total shift per part, mm")
    p.add_argument("--clear", type=float, default=0.0, help="also open gaps smaller than this (mm) between non-touching parts")
    p.add_argument("--iters", type=int, default=40)
    p.add_argument("--fine", action="store_true", help="fine tessellation (slower, exact like verify)")
    p.add_argument("--write", help="write the moved spec here (never overwrites the input unless you pass its path)")
    p.add_argument("--json", help="write the result as JSON here")
    p.set_defaults(func=_cli)


def _cli(a):
    move = [x.strip() for x in a.move.split(",")] if a.move else None
    res = solve(a.spec, move, a.max_move, a.clear, a.iters, fast=not a.fine)
    print(res.report())
    if a.write:
        if Path(a.write).resolve().parent != Path(a.spec).resolve().parent:
            print("note: --write path is in another folder; relative model paths in the spec resolve from there")
        Path(a.write).write_text(json.dumps(res.spec, indent=2))
        print(f"wrote {a.write}; now run: python3 -m robot verify {a.write}")
    if a.json:
        d = {k: v for k, v in res.__dict__.items() if k != "spec"}
        Path(a.json).write_text(json.dumps(d, indent=2, default=list))
    return 0 if not res.left else 3

