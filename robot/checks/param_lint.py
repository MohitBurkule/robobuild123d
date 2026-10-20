"""param.*: build code derives dimensions from named params and relations, not raw numbers.

AST-scans each build source a spec's `model` shapes reference. Numeric literals inside functions are counted per
function unless they are trivial (TRIVIAL), subscript indices, or inside an organic region. Default-argument values
count against their function (moving numbers into defaults does not make them parameters). Module-level lambdas count
as a function named after their target (or `<lambda>@L<line>`), and class-body statements count as `Class.<body>`.
Module-level numeric assignments are the robot's named params and are never counted.

Organic exemptions (B-spline control-point tables and the like):
  * a `# param: organic <reason>` comment on, or directly above, a `def` exempts that function;
  * a `# param: organic <reason>` ... `# param: end` comment pair exempts the lines between;
  * spec `param_exempt: [{"func": "file.py:Qual.name", "reason": text}]` (matched by file and exact qualified name;
    an unqualified name is ignored with a WARNING, and an entry that matches no function is a WARNING).
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
from ._review import _section, override_findings, params

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

    used = set()

    def visit_fn(fn, qual, organic):
        if qual in exempt_funcs:
            used.add(qual)
        organic = organic or qual in exempt_funcs or fn.lineno in fn_marks or \
            any(d.lineno in fn_marks for d in getattr(fn, "decorator_list", []))
        skip = set()
        for n in ast.walk(fn):
            if isinstance(n, ast.Subscript):
                skip |= {id(m) for m in ast.walk(n.slice) if _num(m) is not None and isinstance(_num(m), int)}
        per = defaultdict(int)
        nested = []
        stack = list(fn.body) if isinstance(fn, ast.ClassDef) else list(ast.iter_child_nodes(fn))
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                nested.append(n)
                continue
            if isinstance(fn, ast.ClassDef) and isinstance(n, ast.ClassDef):
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
        for c in ([] if isinstance(fn, ast.ClassDef) else nested):   # class methods are visited by visit_class
            visit_fn(c, f"{qual}.{c.name}", organic)

    def visit_class(node, qual):
        visit_fn(node, f"{qual}.<body>", qual in exempt_funcs or node.lineno in fn_marks)   # class attributes / tables
        for c in node.body:
            if isinstance(c, (ast.FunctionDef, ast.AsyncFunctionDef)):
                visit_fn(c, f"{qual}.{c.name}", qual in exempt_funcs)
            elif isinstance(c, ast.ClassDef):
                visit_class(c, f"{qual}.{c.name}")
        if qual in exempt_funcs:
            used.add(qual)

    def lambdas(stmt):
        """Lambdas outside any def (module level / class body): yield (lambda, name)."""
        tgt = stmt.targets[0] if isinstance(stmt, ast.Assign) and len(stmt.targets) == 1 else \
            stmt.target if isinstance(stmt, ast.AnnAssign) else None
        for n in ast.walk(stmt):
            if isinstance(n, ast.Lambda):
                nm = tgt.id if isinstance(tgt, ast.Name) and stmt.value is n else f"<lambda>@L{n.lineno}"
                yield n, nm

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visit_fn(node, node.name, False)
        elif isinstance(node, ast.ClassDef):
            visit_class(node, node.name)
        else:
            for lam, nm in lambdas(node):
                visit_fn(lam, nm, False)
    patterns, pairs, placements = _structure(tree, funcs)
    patterns = [p for p in patterns if p[0] not in ex_lines]
    return {"funcs": funcs, "values": dict(values), "problems": problems, "patterns": patterns, "mirror_pairs": pairs,
            "exempt_used": sorted(used),
            "placements": [p for p in placements if p[0] not in ex_lines]}


def param_pool(text):
    """{value: name} of module-level named params: scalars, tuple/list/dict members (`NAME[i]`, `NAME.key`)."""
    pool = {}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return pool

    def add(node, name, depth=0):
        v = _num(node)
        if v is not None:
            if v not in TRIVIAL:
                pool.setdefault(float(v), name)
        elif depth < 2 and isinstance(node, (ast.Tuple, ast.List)):
            for i, e in enumerate(node.elts):
                add(e, f"{name}[{i}]", depth + 1)
        elif depth < 2 and isinstance(node, ast.Call) and getattr(node.func, "id", None) == "dict":
            for k in node.keywords:
                if k.arg:
                    add(k.value, f"{name}.{k.arg}", depth + 1)
    for st in tree.body:
        if isinstance(st, ast.Assign):
            for t in st.targets:
                if isinstance(t, ast.Name):
                    add(st.value, t.id)
                elif isinstance(t, ast.Tuple) and isinstance(st.value, ast.Tuple) and len(t.elts) == len(st.value.elts):
                    for n, v in zip(t.elts, st.value.elts):
                        if isinstance(n, ast.Name):
                            add(v, n.id)
    return pool


def unlinked(v, pool, scalars=None, tol=1e-6):
    """Relation a raw literal duplicates: a named param equal to it, or `A + B` / `A - B` of two named scalars."""
    v = float(v)
    for p, n in pool.items():
        if abs(p - v) <= tol:
            return n
    sc = scalars if scalars is not None else pool
    items = sorted(sc.items())
    for i, (a, na) in enumerate(items):
        for b, nb in items[i:]:
            if abs(a + b - v) <= tol:
                return f"{na} + {nb}"
        for b, nb in items:
            if b != a and abs(a - b - v) <= tol:
                return f"{na} - {nb}"
    return None


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
    ex, out = exemptions(spec)
    matched = set()
    nmax, dmin = int(cfg["max_literals"]), int(cfg["dup_min"])
    srcs, pool = sources(spec), {}
    for path in srcs:
        for v, n in param_pool(path.read_text()).items():
            pool.setdefault(v, n)
    scalars = {v: n for v, n in pool.items() if "[" not in n and "." not in n and abs(v) >= 1.0}
    for path in srcs:
        name = path.name
        res = lint_source(path.read_text(), ex.get(name, {}))
        matched |= {f"{name}:{q}" for q in res["exempt_used"]}
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
        for v, lns in sorted(res["values"].items(), key=lambda kv: min(kv[1])):
            # dimensions only: an int is a count / angle / segment number, a whole float < 10 is too common to mean much
            dim = isinstance(v, float) and abs(v) >= 1.0 and (v % 1 or abs(v) >= 10)
            rel = unlinked(v, pool, scalars if v % 1 else {}) if dim else None
            if rel:
                out.append(fail("param.unlinked", G, WARNING, "Unlinked duplicate of a param",
                                f"{name}: literal {v!r} (lines {', '.join(map(str, sorted(lns)[:8]))}) equals `{rel}`.")
                           .fix("Write the relation (`" + rel + "`) instead of retyping its value."))
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
    for f, qs in ex.items():
        for q in qs:
            if f"{f}:{q}" not in matched:
                out.append(fail("param.exempt_unused", G, WARNING, "Exemption matches no function",
                                f"`param_exempt` entry `{f}:{q}` matches no function in the linted sources.")
                           .fix("Fix the file / qualified name, or delete the stale entry."))
    return out, total


def exemptions(spec):
    """spec `param_exempt` -> ({file name: {qualname: reason}}, findings). Keys are `file.py:Qual.name`."""
    ex, out = defaultdict(dict), []
    for e in (spec.raw or {}).get("param_exempt") or []:
        e = e if isinstance(e, dict) else {"func": str(e)}
        key = str(e.get("func") or "")
        if not str(e.get("reason") or "").strip():
            out.append(fail("param.exempt_reason", G, BLOCKER, "Organic exemption without a reason",
                            f"`param_exempt` entry for `{key}` gives no reason.")
                       .fix("Add `reason`: why this function's numbers are organic (e.g. B-spline control points)."))
            continue
        f, sep, q = key.partition(":")
        if not sep or not f or not q:
            out.append(fail("param.exempt_unused", G, WARNING, "Unqualified exemption ignored",
                            f"`param_exempt` entry `{key}` is not `file.py:Qual.name`; a bare name would exempt every "
                            f"function of that name in every file, so it is not applied.")
                       .fix("Write the entry as `file.py:qualified.name`."))
            continue
        ex[f][q] = e.get("reason")
    return dict(ex), out


def run(ctx):
    spec = ctx.r.spec
    ov = override_findings(_section(spec, "param"), DEFAULTS, "param", "param.override", G)
    if not params(spec, "param", DEFAULTS)["enabled"]:
        return ov
    out, total = lint_spec(spec)
    out += ov
    ctx.metrics["param.literal_count"] = total
    return out


if __name__ == "__main__":  # python -m robot.checks.param_lint spec.json : per-function table
    import sys
    from ..spec import load
    sp = load(sys.argv[1])
    ex, _ = exemptions(sp)
    for path in sources(sp):
        res = lint_source(path.read_text(), ex.get(path.name, {}))
        fs = sorted(res["funcs"].items(), key=lambda kv: -kv[1]["count"])
        print(f"{path.name}: total {sum(f['count'] for _, f in fs)} literals in {len(fs)} functions")
        for q, f in fs[:int(sys.argv[2]) if len(sys.argv) > 2 else 20]:
            print(f"  {f['count']:4d}  {f['density']:.2f}/ln  L{f['line']:<5d} {q}  worst {f['worst']}")
