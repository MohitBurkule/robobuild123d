"""param.*: build code derives dimensions from named params and relations, not raw numbers.

AST-scans each build source a spec's `model` shapes reference. Numeric literals inside functions are counted per
function unless they are trivial (TRIVIAL), subscript indices, default-argument values, or inside an organic region.
Module-level assignments are the robot's named params and are never counted.

Organic exemptions (B-spline control-point tables and the like):
  * a `# param: organic <reason>` comment on, or directly above, a `def` exempts that function;
  * a `# param: organic <reason>` ... `# param: end` comment pair exempts the lines between;
  * spec `param_exempt: [{"func": name, "reason": text}]`.
An exemption without a reason is a BLOCKER (param.exempt_reason).

A function with more than `review.param.max_literals` (default 3) unexplained literals is a BLOCKER (param.literals);
a non-trivial value appearing in >= `review.param.dup_min` (default 3) places is a WARNING (param.duplicate).
Metric: `param.literal_count`. Opt out per robot with `review.param.enabled: false`.
"""

from __future__ import annotations

import ast
import re
from collections import defaultdict
from pathlib import Path

from ..finding import BLOCKER, WARNING, fail, ok
from ._review import params

G = "param"
TRIVIAL = {0, 1, 2, 0.5, -1, 90, 180, 360, -90, -180}
DEFAULTS = {"enabled": True, "max_literals": 3, "dup_min": 3}
MARK = re.compile(r"#\s*param:\s*organic\b[ \t:,-]*(.*)$")
END = re.compile(r"#\s*param:\s*end\b")


def _num(node):
    """Value of a numeric literal node (folding unary minus), else None."""
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)) and isinstance(node.operand, ast.Constant):
        v = _num(node.operand)
        return None if v is None else (-v if isinstance(node.op, ast.USub) else v)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        return node.value
    return None


def _organic(lines):
    """(exempt line numbers, {def line: reason}, [(line, problem)]) from marker comments."""
    exempt, fn_marks, bad, start = set(), {}, [], None
    for i, ln in enumerate(lines, 1):
        m = MARK.search(ln)
        if m:
            reason = m.group(1).strip()
            if not reason:
                bad.append((i, "organic marker without a reason"))
            nxt = next((j for j in range(i, len(lines) + 1) if lines[j - 1].strip() and not lines[j - 1].strip().startswith("#")) , i)
            code = lines[i - 1].split("#")[0].strip()
            tgt = i if code else nxt
            if lines[tgt - 1].lstrip().startswith(("def ", "async def ")):
                fn_marks[tgt] = reason
            else:
                start = i
        elif END.search(ln) and start is not None:
            exempt.update(range(start, i + 1))
            start = None
    if start is not None:
        bad.append((start, "organic region has no `# param: end`"))
    return exempt, fn_marks, bad


PLACE_CALLS = {"translate", "moved", "move", "located", "locate", "Location", "Pos", "Locations", "translated"}
SIDES = [("left", "right"), ("_l", "_r"), ("_lh", "_rh"), ("Left", "Right")]


def _point(node):
    if isinstance(node, (ast.Tuple, ast.List)) and len(node.elts) in (2, 3):
        vs = [_num(e) for e in node.elts]
        if all(v is not None for v in vs):
            return [float(v) for v in vs]
    return None


def _uniform(vals, tol=1e-6):
    vals = sorted(set(round(v, 6) for v in vals))
    if len(vals) < 2:
        return len(vals)
    d = [b - a for a, b in zip(vals, vals[1:])]
    return len(vals) if max(d) - min(d) <= tol + 1e-3 * abs(d[0]) else 0


def pattern_of(pts):
    """'row' | 'grid' | 'circle' | None for >= 3 literal points (2D/3D, same dim)."""
    if len(pts) < 3 or len({len(p) for p in pts}) != 1:
        return None
    dim = len(pts[0])
    if len({tuple(p) for p in pts}) != len(pts):
        return None
    counts = [_uniform([p[i] for p in pts]) for i in range(dim)]
    varying = [c for c in counts if c != 1]
    if all(counts) and len(varying) == 1 and varying[0] == len(pts):
        return "row"
    if all(counts) and len(varying) >= 2 and len(pts) == __import__("math").prod(varying) and len(pts) >= 4:
        return "grid"
    c = [sum(p[i] for p in pts) / len(pts) for i in range(dim)]
    rs = [sum((p[i] - c[i]) ** 2 for i in range(dim)) ** 0.5 for p in pts]
    if min(rs) > 1e-6 and (max(rs) - min(rs)) <= 0.01 * max(rs) and len(pts) >= 4:
        return "circle"
    if len(pts) == 3 and min(rs) > 1e-6 and (max(rs) - min(rs)) <= 0.01 * max(rs):
        import math  # equilateral triangle = 3-point bolt circle
        d = [math.dist(pts[i], pts[(i + 1) % 3]) for i in range(3)]
        if max(d) - min(d) <= 0.01 * max(d):
            return "circle"
    return None


def _structure(tree, funcs):
    """Literal point patterns, L/R pairs not using mirror, literal placements."""
    patterns, placements = [], []
    for n in ast.walk(tree):
        if isinstance(n, (ast.List, ast.Tuple)) and len(n.elts) >= 3:
            pts = [_point(e) for e in n.elts]
            if all(pts):
                k = pattern_of(pts)
                if k:
                    patterns.append((n.lineno, k, len(pts)))
    owner = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for n in ast.walk(fn):
                owner.setdefault(id(n), fn.name)
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            nm = n.func.attr if isinstance(n.func, ast.Attribute) else getattr(n.func, "id", None)
            if nm in PLACE_CALLS and n.args:
                a = n.args[0]
                pt = _point(a) or ([_num(x) for x in n.args] if len(n.args) in (2, 3) and all(_num(x) is not None for x in n.args) else None)
                if pt and any(v not in TRIVIAL for v in pt):
                    placements.append((n.lineno, owner.get(id(n), "<module>"), nm))
    srcs = {}
    for fn in ast.walk(tree):
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            srcs[fn.name] = any(isinstance(c, ast.Call) and (getattr(c.func, "attr", None) or getattr(c.func, "id", "")) in
                                ("mirror", "mirrored", "Mirror") for c in ast.walk(fn))
    pairs = []
    for a in srcs:
        for l, r in SIDES:
            if l in a:
                b = a.replace(l, r)
                if b in srcs and not (srcs[a] or srcs[b]) and funcs.get(a, {}).get("count") and funcs.get(b, {}).get("count"):
                    pairs.append((a, b))
    return patterns, sorted(set(pairs)), placements


def lint_source(text, exempt_funcs=None):
    """Scan one source. Returns {"funcs": {name: {"count", "lines", "density", "worst", "exempt"}}, "values": {v: [lines]},
    "problems": [(line, msg)]}."""
    exempt_funcs = dict(exempt_funcs or {})
    lines = text.splitlines()
    tree = ast.parse(text)
    ex_lines, fn_marks, problems = _organic(lines)
    funcs, values = {}, defaultdict(list)

    def visit_fn(fn, qual, organic):
        organic = organic or fn.name in exempt_funcs or fn.lineno in fn_marks or \
            any(d.lineno in fn_marks for d in fn.decorator_list)
        skip = set()
        for d in list(fn.args.defaults) + [d for d in fn.args.kw_defaults if d is not None]:
            skip |= {id(n) for n in ast.walk(d)}
        for n in ast.walk(fn):
            if isinstance(n, ast.Subscript):
                skip |= {id(m) for m in ast.walk(n.slice) if _num(m) is not None and isinstance(_num(m), int)}
        per = defaultdict(int)
        nested = []
        stack = list(ast.iter_child_nodes(fn))
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nested.append(n)
                continue
            v = _num(n)
            if v is not None:
                if id(n) in skip or v in TRIVIAL or organic or n.lineno in ex_lines:
                    continue
                per[n.lineno] += 1
                values[v].append(n.lineno)
                continue  # don't double count -x's operand
            stack.extend(ast.iter_child_nodes(n))
        span = max(1, (fn.end_lineno or fn.lineno) - fn.lineno + 1)
        cnt = sum(per.values())
        funcs[qual] = {"count": cnt, "lines": span, "density": cnt / span, "line": fn.lineno, "exempt": organic,
                       "worst": sorted(per.items(), key=lambda kv: (-kv[1], kv[0]))[:3]}
        for c in nested:
            visit_fn(c, f"{qual}.{c.name}", organic)

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for c in node.body:
                if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    visit_fn(c, f"{node.name}.{c.name}", False)
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visit_fn(node, node.name, False)
    patterns, pairs, placements = _structure(tree, funcs)
    patterns = [p for p in patterns if p[0] not in ex_lines]
    return {"funcs": funcs, "values": dict(values), "problems": problems, "patterns": patterns, "mirror_pairs": pairs,
            "placements": [p for p in placements if p[0] not in ex_lines]}


def sources(spec):
    seen = []
    for p in spec.parts:
        sh = p.shape if isinstance(p.shape, dict) else None
        f = (sh or {}).get("file") if (sh or {}).get("type") == "model" else None
        if f:
            path = (Path(spec.base_dir) / f).resolve()
            if path.suffix == ".py" and path not in seen:
                seen.append(path)
                seen.extend(q for q in _package_modules(path) if q not in seen)
    return seen


def _package_modules(path):
    """[fix-S] A model file may be a thin shim over a sibling package (`import revron`): lint every module of it too."""
    import ast
    out = []
    try:
        tree = ast.parse(path.read_text())
    except (OSError, SyntaxError):
        return out
    for node in ast.walk(tree):
        names = [a.name for a in node.names] if isinstance(node, ast.Import) else \
            [node.module] if isinstance(node, ast.ImportFrom) and node.module and not node.level else []
        for n in names:
            pkg = path.parent / n.split(".")[0]
            if (pkg / "__init__.py").is_file():
                out += sorted(q.resolve() for q in pkg.glob("*.py"))
    return out


def lint_spec(spec):
    cfg = params(spec, "param", DEFAULTS)
    out, total = [], 0
    ex = {}
    for e in (spec.raw or {}).get("param_exempt") or []:
        e = e if isinstance(e, dict) else {"func": str(e)}
        if not str(e.get("reason") or "").strip():
            out.append(fail("param.exempt_reason", G, BLOCKER, "Organic exemption without a reason",
                            f"`param_exempt` entry for `{e.get('func')}` gives no reason.")
                       .fix("Add `reason`: why this function's numbers are organic (e.g. B-spline control points)."))
        ex[e.get("func")] = e.get("reason")
    nmax, dmin = int(cfg["max_literals"]), int(cfg["dup_min"])
    for path in sources(spec):
        res = lint_source(path.read_text(), ex)
        name = path.name
        for ln, msg in res["problems"]:
            out.append(fail("param.exempt_reason", G, BLOCKER, "Bad organic marker", f"{name}:{ln}: {msg}.")
                       .fix("Write `# param: organic <reason>` and close regions with `# param: end`."))
        n_bad = 0
        for q, f in sorted(res["funcs"].items(), key=lambda kv: -kv[1]["count"]):
            total += f["count"]
            if f["count"] > nmax:
                n_bad += 1
                worst = ", ".join(f"L{l}×{c}" for l, c in f["worst"])
                out.append(fail("param.literals", G, BLOCKER, "Raw numbers in geometry code",
                                f"{name}:{f['line']} `{q}` has {f['count']} unexplained numeric literals "
                                f"({f['density']:.2f}/line; worst {worst}).")
                           .expect(f"<= {nmax}", f["count"])
                           .fix("Build from named params and relations (center of X, offset from face of Y, mirror); "
                                "mark genuinely organic tables `# param: organic <reason>`."))
        for v, lns in sorted(res["values"].items(), key=lambda kv: -len(kv[1])):
            if len(lns) >= dmin:
                out.append(fail("param.duplicate", G, WARNING, "Repeated raw number",
                                f"{name}: {v!r} appears {len(lns)}× (lines {', '.join(map(str, sorted(lns)[:8]))}"
                                f"{'…' if len(lns) > 8 else ''}).")
                           .fix("Make it one named param (or derive it from one)."))
        for ln, k, npt in res["patterns"]:
            loc = {"circle": "PolarLocations", "grid": "GridLocations", "row": "GridLocations (one row) / a loop"}[k]
            out.append(fail("param.pattern", G, WARNING, "Literal coordinates form a regular pattern",
                            f"{name}:{ln}: {npt} literal points lie on a {k}.")
                       .fix(f"Generate them with {loc} from a named pitch/radius/count."))
        for a, b in res["mirror_pairs"]:
            out.append(fail("param.mirror", G, WARNING, "Left/right pair built twice from literals",
                            f"{name}: `{a}` and `{b}` are both built from raw numbers; neither uses mirror().")
                       .fix("Build one side and mirror() it about the centre plane."))
        for ln, fn, call in res["placements"]:
            out.append(fail("param.placement", G, WARNING, "Placed by literal world coordinates",
                            f"{name}:{ln} `{fn}` places geometry with {call}(<literal coords>).")
                       .fix("Place by Joint/mate or relative to a named feature (face, axis, centre) instead."))
        if not n_bad:
            out.append(ok("param.literals", G, "Build code is parametric", f"{name}: no function over {nmax} raw literals."))
    return out, total


def run(ctx):
    spec = ctx.r.spec
    if not params(spec, "param", DEFAULTS)["enabled"]:
        return []
    out, total = lint_spec(spec)
    ctx.metrics["param.literal_count"] = total
    return out


if __name__ == "__main__":  # python -m robot.checks.param_lint spec.json : per-function table
    import sys
    from ..spec import load
    sp = load(sys.argv[1])
    ex = {e.get("func"): e.get("reason") for e in (sp.raw.get("param_exempt") or []) if isinstance(e, dict)}
    for path in sources(sp):
        res = lint_source(path.read_text(), ex)
        fs = sorted(res["funcs"].items(), key=lambda kv: -kv[1]["count"])
        print(f"{path.name}: total {sum(f['count'] for _, f in fs)} literals in {len(fs)} functions")
        for q, f in fs[:int(sys.argv[2]) if len(sys.argv) > 2 else 20]:
            print(f"  {f['count']:4d}  {f['density']:.2f}/ln  L{f['line']:<5d} {q}  worst {f['worst']}")
