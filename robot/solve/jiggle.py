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


# ---------------------------------------------------------------- named-param levers (variables, not positions)

@dataclass
class ParamLever:
    file: str          # absolute path of the params module
    name: str          # top-level master, e.g. SWITCH_BAY
    x0: float
    lo: float
    hi: float
    step: float = 0.1  # finite-difference step and output quantum

    @property
    def label(self):
        return f"{Path(self.file).name}:{self.name}"


def parse_levers(spec_path, items, raw_levers=(), max_move=5.0):
    """Levers from CLI items "path/params.py:NAME[=lo:hi[:step]]" and spec "levers" entries
    {"param": "path:NAME", "lo", "hi", "step"}; paths are relative to the spec folder."""
    from .. import params_override as po

    base = Path(spec_path).resolve().parent
    out = []
    rows = [(it, None) for it in items or []] + [(lv.get("param", ""), lv) for lv in raw_levers or []]
    for txt, lv in rows:
        ref, _, rng = txt.partition("=")
        f, _, name = ref.rpartition(":")
        fp = (base / f).resolve() if not Path(f).is_absolute() else Path(f)
        x0 = po.read(fp, name)
        if x0 is None:
            raise ValueError(f"lever {txt}: `{name}` in {fp} is not a plain number master")
        lo, hi, step = x0 - max_move, x0 + max_move, 0.1
        if rng:
            bits = [float(b) for b in rng.split(":")]
            lo, hi = bits[0], bits[1]
            step = bits[2] if len(bits) > 2 else step
        if lv:
            lo, hi, step = float(lv.get("lo", lo)), float(lv.get("hi", hi)), float(lv.get("step", step))
        out.append(ParamLever(str(fp), name, float(x0), lo, hi, step))
    return out


REGEN = {"script": None, "cwd": None}   # spec generator (e.g. robots/scythe/make_spec.py), set by solve_params


def run_generator(script, cwd=None):
    """Run a spec generator script in-process with the active param overrides (its own constants included)."""
    from .. import params_override as po

    script = Path(script).resolve()
    vals = po.current().get(str(script), {})
    code = po.transform(script.read_text(encoding="utf-8"), vals, str(script)) if vals else \
        compile(script.read_text(encoding="utf-8"), str(script), "exec")
    old = Path.cwd()
    import os
    import contextlib
    import io
    os.chdir(cwd or old)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(code, {"__name__": "__main__", "__file__": str(script)})  # noqa: S102  the robot's own generator
    finally:
        os.chdir(old)


def _eval_params(spec_path, levers, xs, clear, fast):
    """Violations of the whole robot with the levers at xs: {(a, b, what): amount}. Rebuilds what changed (cached)."""
    from .. import measure, params_override as po, spec as spec_mod, world as world_mod
    from ..checks import interference as itf

    ov = {}
    for lv, x in zip(levers, xs):
        ov.setdefault(lv.file, {})[lv.name] = float(x)
    root = Path(spec_path).resolve().parent
    with po.active(ov, purge_root=root):
        try:
            if REGEN["script"]:
                run_generator(REGEN["script"], REGEN["cwd"])
            s = spec_mod.load(spec_path)
            r = world_mod.resolve(s, fast=fast)
            if getattr(r, "load_errors", None):
                return None
            w = world_mod.World.start(r)
        except Exception:  # noqa: BLE001  a lever value that breaks the build is simply infeasible
            return None
        vs = _violations(w, {b.id for b in w.bodies}, lambda a, b: itf.allowed_depth(r, a, b), clear, measure)
    return {(a, b, what): d for a, b, d, what in vs}


def solve_params(spec_path, levers, clear=0.0, iters=12, fast=True, log=print, regen=None, regen_cwd=None):
    """See _solve_params. `regen`: spec generator script re-run at every evaluation (spec.json is restored after)."""
    sp = Path(spec_path)
    saved = sp.read_text()
    REGEN.update(script=regen, cwd=regen_cwd)
    try:
        return _solve_params(spec_path, levers, clear, iters, fast, log)
    finally:
        REGEN.update(script=None, cwd=None)
        sp.write_text(saved)


def _solve_params(spec_path, levers, clear=0.0, iters=12, fast=True, log=print):
    """Damped least squares on the violation vector over named masters (finite-difference Jacobian), with a
    backtracking line search on the total and a coordinate-search fallback. Every relation that reads a master
    (pockets, hole patterns, slots, `{"expr"}` placements) moves with it, so dependents stay consistent."""
    from .. import world as world_mod

    world_mod.JOBS = 1   # overrides must reach the builds; in-process keeps imports purgeable
    x = np.array([lv.x0 for lv in levers], float)
    lo = np.array([lv.lo for lv in levers]); hi = np.array([lv.hi for lv in levers])
    st = np.array([lv.step for lv in levers])
    snap = lambda v: np.round(np.clip(np.round(v / st) * st, lo, hi), 6)  # noqa: E731
    v = _eval_params(spec_path, levers, x, clear, fast)
    if v is None:
        raise ValueError("the robot does not build at the current param values")
    tot = lambda vv: float("inf") if vv is None else float(sum(vv.values()))  # noqa: E731
    start = cur = tot(v)
    hist = []
    for it in range(iters):
        if cur <= 1e-6:
            break
        keys = sorted(v)
        J = np.zeros((len(keys), len(levers)))
        for j in range(len(levers)):
            xp = x.copy(); xp[j] = min(hi[j], x[j] + st[j]) if x[j] + st[j] <= hi[j] else max(lo[j], x[j] - st[j])
            dxj = xp[j] - x[j]
            vp = _eval_params(spec_path, levers, xp, clear, fast)
            if vp is None or abs(dxj) < 1e-12:
                continue
            for i, k in enumerate(keys):
                J[i, j] = (vp.get(k, 0.0) - v[k]) / dxj
        r0 = np.array([v[k] for k in keys])
        lam = 1e-3 * (np.trace(J.T @ J) + 1e-9)
        dx = -np.linalg.solve(J.T @ J + lam * np.eye(len(levers)), J.T @ r0) if J.any() else np.zeros(len(levers))
        moved = False
        for a in (1.0, 1.5, 0.5, 0.25):   # overshoot a little first: hinge losses flatten at zero
            xn = snap(x + a * dx)
            if np.allclose(xn, x):
                continue
            vn = _eval_params(spec_path, levers, xn, clear, fast)
            if tot(vn) < cur - 1e-4:
                x, v, cur, moved = xn, vn, tot(vn), True
                break
        if not moved:  # fallback: coordinate pattern search, growing steps
            for j in range(len(levers)):
                for k in (1, 2, 4, 8, 16):
                    for sgn in (1, -1):
                        xn = x.copy(); xn[j] = x[j] + sgn * k * st[j]; xn = snap(xn)
                        vn = _eval_params(spec_path, levers, xn, clear, fast)
                        if tot(vn) < cur - 1e-4:
                            x, v, cur, moved = xn, vn, tot(vn), True
                            break
                    if moved:
                        break
                if moved:
                    break
        if not moved:
            break
        hist.append({lv.label: float(xi) for lv, xi in zip(levers, x)})
        log(f"  iter {it + 1}: " + ", ".join(f"{lv.name}={xi:g}" for lv, xi in zip(levers, x)) + f" -> violation {cur:.3f} mm")
    return {"start": start, "final": cur, "values": {lv.label: float(xi) for lv, xi in zip(levers, x)},
            "changed": {lv.label: (lv.x0, float(xi)) for lv, xi in zip(levers, x) if abs(xi - lv.x0) > 1e-9},
            "left": [[a, b, what, round(d, 3)] for (a, b, what), d in sorted(v.items())], "history": hist,
            "files": {lv.label: lv.file for lv in levers}, "names": {lv.label: lv.name for lv in levers}}


def add_cli(sub):
    p = sub.add_parser("jiggle", help="nudge movable parts until collisions/clearances clear (measured, not guessed)")
    p.add_argument("spec")
    p.add_argument("--move", help="comma-separated part ids allowed to move (default: non-structure parts with a numeric `at`)")
    p.add_argument("--max-move", type=float, default=5.0, help="max total shift per part, mm")
    p.add_argument("--clear", type=float, default=0.0, help="also open gaps smaller than this (mm) between non-touching parts")
    p.add_argument("--iters", type=int, default=40)
    p.add_argument("--param", action="append", default=[], metavar="FILE:NAME[=lo:hi[:step]]",
                   help="solve over this model master too (repeatable); spec `levers` entries are added. Parts, pockets,"
                        " holes and slots derived from it all move together")
    p.add_argument("--regen", help="spec generator script (python) re-run at every evaluation, e.g. make_spec.py; its"
                   " own top-level numbers can be levers too (--param make_spec.py:BAT_Y)")
    p.add_argument("--regen-cwd", help="working dir for --regen (default: current)")
    p.add_argument("--params-only", action="store_true", help="only solve the named params, do not move spec `at`s")
    p.add_argument("--write-params", action="store_true", help="write the solved values into the params source files")
    p.add_argument("--fine", action="store_true", help="fine tessellation (slower, exact like verify)")
    p.add_argument("--write", help="write the moved spec here (never overwrites the input unless you pass its path)")
    p.add_argument("--json", help="write the result as JSON here")
    p.set_defaults(func=_cli)


def _cli(a):
    from .. import params_override as po, spec as spec_mod

    raw = spec_mod.load(a.spec).raw
    levers = parse_levers(a.spec, a.param, raw.get("levers"), a.max_move)
    if levers:
        pr = solve_params(a.spec, levers, a.clear, max(4, a.iters // 4), fast=not a.fine,
                          regen=a.regen, regen_cwd=a.regen_cwd)
        print(f"params: violation {pr['start']:.3f} -> {pr['final']:.3f} mm")
        for lab, (o, n) in pr["changed"].items():
            print(f"  {lab}: {o:g} -> {n:g}")
        if a.write_params and pr["changed"]:
            by_file = {}
            for lab, (_, n) in pr["changed"].items():
                by_file.setdefault(pr["files"][lab], {})[pr["names"][lab]] = n
            for f, vals in by_file.items():
                po.write(f, vals)
                print(f"wrote {f}")
            if a.regen:
                run_generator(a.regen, a.regen_cwd)
                print(f"regenerated {a.spec}")
        if a.json:
            Path(a.json).with_suffix(".params.json").write_text(json.dumps(pr, indent=2, default=list))
        if a.params_only or pr["final"] <= 1e-6:
            return 0 if pr["final"] <= 1e-6 else 3
        if pr["changed"] and not a.write_params:
            print("note: spec moves below are computed at the ORIGINAL param values (pass --write-params to chain)")
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

