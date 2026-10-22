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

import numpy as np

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
    pool, env = {}, {}
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return pool

    def ev(node):   # derived params: + - * / of literals and earlier named scalars
        v = _num(node)
        if v is not None:
            return v
        if isinstance(node, ast.Name):
            return env.get(node.id)
        if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
            a, b = ev(node.left), ev(node.right)
            if a is None or b is None or (isinstance(node.op, ast.Div) and not b):
                return None
            return {ast.Add: a + b, ast.Sub: a - b, ast.Mult: a * b}.get(type(node.op), a / b if b else None)
        return None

    def add(node, name, depth=0):
        v = ev(node)
        if v is not None and depth == 0:
            env[name] = v
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


def module_literals(text):
    """{value: [lines]} of numeric literals at module level (constants, tuples, tables) outside organic regions."""
    tree, lines = ast.parse(text), text.splitlines()
    ex, _, _ = _organic(lines)
    vals = defaultdict(list)
    for st in tree.body:
        if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Import, ast.ImportFrom)):
            continue
        stack = [st]
        while stack:
            n = stack.pop()
            if isinstance(n, (ast.Lambda, ast.Subscript)):
                continue
            v = _num(n)
            if v is not None:
                if n.lineno not in ex and v not in TRIVIAL:
                    vals[v].append(n.lineno)
                continue
            stack.extend(ast.iter_child_nodes(n))
    return dict(vals)


def master_block(text):
    """Source of the master-parameter block: from a `MASTER DESIGN PARAMETERS` comment to the next `# ---` rule."""
    out, on = [], False
    for ln in text.splitlines():
        if "MASTER DESIGN PARAMETERS" in ln:
            on = True
        elif on and ln.startswith("# ---"):
            break
        elif on:
            out.append(ln)
    return "\n".join(out)


def is_param_module(path):
    return Path(path).name.startswith("params")


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
    pmods, masters = [p for p in srcs if is_param_module(p)], {}
    for path in pmods or srcs:
        text = path.read_text()
        for v, n in param_pool(text).items():
            pool.setdefault(v, n)
        for v, n in param_pool(master_block(text)).items():
            masters.setdefault(v, n)
    # A +- B only over the master design params (sums of unrelated params are coincidences, not relations)
    scalars = {v: n for v, n in (masters or pool).items() if "." not in n and abs(v) >= 1.0}
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
        vals = defaultdict(list, {v: list(l) for v, l in res["values"].items()})
        if pmods and not is_param_module(path):
            for v, l in module_literals(path.read_text()).items():
                vals[v] += l
        for v, lns in sorted(vals.items(), key=lambda kv: min(kv[1])):
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


# ------------------------------------------------------------------------------------------------ add-ons (WARNING for now)
MASTER_MAX = 40          # a master block longer than this is not a short whitelist
TAG = re.compile(r"#\s*param:\s*(organic|datasheet)\b[ \t:,-]*(.*)$")
SYM_TOL_MM = 0.05        # style.symmetry: halves mirror each other within this
SYM_SAMPLES = 1500
MIRROR_CALLS = ("mirror", "mirrored", "Mirror")


def copied_params(text):
    """[(line, name, value)] of params_*.py raw decimals: module-level constants (and tuple / list / dict members) whose
    value is a bare literal, not an expression of other params. Exempt: the MASTER DESIGN PARAMETERS block, organic
    regions, and lines tagged (on the line or the line above) `# param: organic <why>` / `# param: datasheet <src>`."""
    lines = text.splitlines()
    tree = ast.parse(text)
    ex, _, _ = _organic(lines)
    mb, on = set(), False
    for i, ln in enumerate(lines, 1):
        if "MASTER DESIGN PARAMETERS" in ln:
            on = True
        elif on and ln.startswith("# ---"):
            on = False
        elif on:
            mb.add(i)

    def tagged(i):
        return any(TAG.search(lines[j - 1]) and TAG.search(lines[j - 1]).group(2).strip() for j in (i, i - 1) if 1 <= j <= len(lines))

    out = []

    def walk(node, name, ln):
        v = _num(node)
        if v is not None:
            if isinstance(v, float) and v not in TRIVIAL:
                out.append((ln, name, v))
            return
        if isinstance(node, (ast.Tuple, ast.List)):
            for k, e in enumerate(node.elts):
                walk(e, f"{name}[{k}]", getattr(e, "lineno", ln))
        elif isinstance(node, ast.Dict):
            for k, e in zip(node.keys, node.values):
                key = k.value if isinstance(k, ast.Constant) else "?"
                walk(e, f"{name}[{key!r}]", getattr(e, "lineno", ln))
        elif isinstance(node, ast.Call) and getattr(node.func, "id", None) == "dict":
            for kw in node.keywords:
                walk(kw.value, f"{name}.{kw.arg}", getattr(kw.value, "lineno", ln))
        # anything else (BinOp of names, calls) is an expression built from other params

    for st in tree.body:
        if not isinstance(st, (ast.Assign, ast.AnnAssign)) or st.lineno in mb or st.lineno in ex or tagged(st.lineno):
            continue
        tg = st.targets if isinstance(st, ast.Assign) else [st.target]
        for t in tg:
            if isinstance(t, ast.Name):
                walk(st.value, t.id, st.lineno)
            elif isinstance(t, ast.Tuple) and isinstance(st.value, ast.Tuple) and len(t.elts) == len(st.value.elts):
                for n, v in zip(t.elts, st.value.elts):
                    if isinstance(n, ast.Name):
                        walk(v, n.id, st.lineno)
    return [x for x in out if x[0] not in ex and not tagged(x[0])], len({i for i in mb if lines[i - 1].split("#")[0].strip()})


def point_tables(text):
    """[(line, name, kind)] of params point tables: a module-level tuple / list of >= 4 coordinate pairs (or triples),
    or a dict (literal or dict()) whose values are tuples. Exempt: organic regions and `# param: organic <why>` tags."""
    lines = text.splitlines()
    ex, _, _ = _organic(lines)

    def organic(i):
        return any(TAG.search(lines[j - 1]) and TAG.search(lines[j - 1]).group(1) == "organic" and TAG.search(lines[j - 1]).group(2).strip()
                   for j in (i, i - 1) if 1 <= j <= len(lines))

    def is_pt(e):
        return isinstance(e, (ast.Tuple, ast.List)) and len(e.elts) in (2, 3)

    out = []
    for st in ast.parse(text).body:
        if not isinstance(st, ast.Assign) or st.lineno in ex or organic(st.lineno):
            continue
        names = [t.id for t in st.targets if isinstance(t, ast.Name)]
        if not names:
            continue
        v = st.value
        if isinstance(v, (ast.Tuple, ast.List)) and len(v.elts) >= 4 and all(is_pt(e) for e in v.elts):
            out.append((st.lineno, names[0], f"{len(v.elts)} coordinate points"))
        elif isinstance(v, ast.Dict) and v.values and any(isinstance(e, ast.Tuple) for e in v.values):
            out.append((st.lineno, names[0], "dict of tuples"))
        elif isinstance(v, ast.Call) and getattr(v.func, "id", None) == "dict" and any(isinstance(k.value, ast.Tuple) for k in v.keywords):
            out.append((st.lineno, names[0], "dict of tuples"))
    return out


def star_imports(text):
    """[(line, module)] of `from .x import *`."""
    return [(n.lineno, "." * n.level + (n.module or "")) for n in ast.walk(ast.parse(text))
            if isinstance(n, ast.ImportFrom) and any(a.name == "*" for a in n.names)]


def addon_findings(spec):
    out, counts = [], {"copied": 0, "star_import": 0, "point_table": 0}
    for path in sources(spec):
        text = path.read_text()
        name = path.name
        if is_param_module(path):
            cp, nmaster = copied_params(text)
            counts["copied"] += len(cp)
            if cp:
                out.append(fail("param.copied", G, WARNING, "Param is a copied raw decimal",
                                f"{name}: {len(cp)} constants are bare decimals, not built from other params: "
                                + ", ".join(f"L{ln} {n}={v:g}" for ln, n, v in cp[:12]) + (" ..." if len(cp) > 12 else ""))
                           .fix("Derive it from the masters (relation), or tag `# param: datasheet <source>` / `# param: organic <why>`."))
            pt = point_tables(text)
            counts["point_table"] = counts.get("point_table", 0) + len(pt)
            if pt:
                out.append(fail("param.point_table", G, WARNING, "Coordinate table in params",
                                f"{name}: {len(pt)} point tables: " + ", ".join(f"L{ln} {n} ({k})" for ln, n, k in pt[:15]))
                           .fix("Derive the points from features (radius, pitch, offsets from masters), or tag `# param: organic <why>`."))
            if nmaster > MASTER_MAX:
                out.append(fail("param.copied", G, WARNING, "Master block is not a short whitelist",
                                f"{name}: {nmaster} master lines (> {MASTER_MAX})."))
        else:
            st = star_imports(text)
            if st and path.name != "__init__.py":
                counts["star_import"] += len(st)
                out.append(fail("style.star_import", G, WARNING, "Star import in a part file",
                                f"{name}: " + ", ".join(f"L{ln} from {m} import *" for ln, m in st))
                           .fix("Import the names the part uses (`from .params import CH_WALL, ...`)."))
    return out, counts


def _part_module(spec, key):
    """Source file defining the build function a model part `params.part` names (via a {'key': fn} table), or None."""
    srcs = [p for p in sources(spec) if not is_param_module(p)]
    fname = None
    for p in srcs:
        for n in ast.walk(ast.parse(p.read_text())):
            if isinstance(n, ast.Dict):
                for k, v in zip(n.keys, n.values):
                    if isinstance(k, ast.Constant) and k.value == key:
                        if isinstance(v, ast.Lambda) and isinstance(v.body, ast.Call):
                            v = v.body.func
                        if isinstance(v, ast.Name):
                            fname = v.id
    fname = fname or key
    for p in srcs:
        if any(isinstance(n, ast.FunctionDef) and n.name == fname for n in ast.walk(ast.parse(p.read_text()))):
            return p, fname
    return None, fname


def mirror_count(text, fname=None):
    """mirror() / mirrored() calls in the module that builds the part (the build function often calls helpers there)."""
    del fname
    return sum(1 for c in ast.walk(ast.parse(text)) if isinstance(c, ast.Call)
               and (getattr(c.func, "attr", None) or getattr(c.func, "id", "")) in MIRROR_CALLS)


def mirror_symmetric(mesh, axis=0, tol=SYM_TOL_MM, n=SYM_SAMPLES):
    """True when the mesh's half on one side of its bbox mid-plane (normal `axis`) mirrors the other within tol."""
    import trimesh

    c = float((mesh.bounds[0][axis] + mesh.bounds[1][axis]) / 2)
    pts = trimesh.sample.sample_surface(mesh, n, seed=3)[0]
    q = pts.copy()
    q[:, axis] = 2 * c - q[:, axis]
    d = trimesh.proximity.ProximityQuery(mesh).on_surface(q)[1]
    return float(np.quantile(d, 0.99)) <= tol


def symmetry_findings(ctx):
    """style.symmetry: a part centred on the robot's X = 0 plane that is mirror-symmetric there, whose build module
    makes no mirror() call (proxy: both sides are built)."""
    spec, w = ctx.r.spec, ctx.world
    out, flagged, n_sym = [], [], 0
    for p in spec.parts:
        sh = p.shape if isinstance(p.shape, dict) else {}
        key = (sh.get("params") or {}).get("part") if sh.get("type") == "model" else None
        b = w.body(p.id) if (key and w is not None) else None
        if b is None or b.mesh is None or len(b.mesh.faces) < 4:
            continue
        lo, hi = b.mesh.bounds
        if abs((lo[0] + hi[0]) / 2) > 1.0 or hi[0] - lo[0] < 2.0:
            continue
        try:
            if not mirror_symmetric(b.mesh, 0):
                continue
        except Exception:  # noqa: BLE001
            continue
        n_sym += 1
        mod, fname = _part_module(spec, key)
        if mod is None:
            continue
        k = mirror_count(mod.read_text(), fname)
        if k == 0:
            flagged.append(f"`{p.id}` ({mod.name}:{fname})")
    ctx.metrics["style.symmetry"] = {"symmetric_parts": n_sym, "built_both_sides": len(flagged)}
    if flagged:
        out.append(fail("style.symmetry", G, WARNING, "Symmetric part built side by side",
                        f"{len(flagged)} of {n_sym} parts mirror-symmetric about X = 0 (within {SYM_TOL_MM} mm) have no mirror() "
                        f"in their build code: " + ", ".join(flagged))
                   .fix("Build one half and mirror() it about the centre plane."))
    return out


BUDGET_FRAC = 1.0   # param.budget: our numeric tokens may not exceed the reference's dimension count (beat the designer)


def numeric_tokens(text, names=None):
    """Non-trivial numeric literals in a source; with `names`, only those in module-level assignments to those names."""
    tree = ast.parse(text)
    nodes = tree.body if names is None else [st for st in tree.body if isinstance(st, ast.Assign) and any(
        isinstance(t, ast.Name) and t.id in names or isinstance(t, ast.Tuple) and any(getattr(e, "id", None) in names for e in t.elts)
        for t in st.targets)]
    n = 0
    for st in nodes:
        stack = [st]
        while stack:
            x = stack.pop()
            v = _num(x)
            if v is not None:
                n += v not in TRIVIAL
                continue
            stack.extend(ast.iter_child_nodes(x))
    return n


def dump_dims(text):
    """Unique DIM names (`D1@Sketch3`) of the non-suppressed top-level features of a SolidWorks part dump."""
    names, on = set(), False
    for ln in text.splitlines():
        if ln.startswith("FEATURE "):
            on = "suppressed=False" in ln
        elif ln.startswith("  FEATURE "):
            on = False
        elif on and ln.startswith("  DIM "):
            names.add("@".join(ln[6:].split(" = ")[0].split("@")[:2]))
    return len(names)


def _closure(start, defs):
    """(module, name) keys reachable from `start` through calls inside the package: `f(...)` resolves in the same
    module first, then any module; `mod.f(...)` in module `mod`. defs: {(module stem, name): FunctionDef}."""
    by_name = {}
    for (m, n) in defs:
        by_name.setdefault(n, []).append((m, n))
    seen, todo = set(), [start]
    while todo:
        k = todo.pop()
        if k in seen or k not in defs:
            continue
        seen.add(k)
        for c in ast.walk(defs[k]):
            if not isinstance(c, ast.Call):
                continue
            f = c.func
            if isinstance(f, ast.Name):
                todo.append((k[0], f.id) if (k[0], f.id) in defs else (by_name.get(f.id) or [None])[0])
            elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                todo.append((f.value.id, f.attr))
    return seen


def budget_rows(spec):
    """[{function, parts, ours, ref, dump, ratio}] per build function (an RH / mirrored part built by the same function
    as its LH part is counted once, so it adds nothing): non-trivial numeric tokens in the function and every package
    function it calls, plus the literals of the params it reads, vs the unique dimensions of the matching SolidWorks
    dump (its LH part's)."""
    from .reference_cad import _cfg
    from .sldprt_dump import DEFAULT_ROOT, dumps_dir, find_dump

    srcs = sources(spec)
    pmods = [p for p in srcs if is_param_module(p)]
    defs = {}
    for p in srcs:
        if not is_param_module(p):
            for n in ast.walk(ast.parse(p.read_text())):
                if isinstance(n, ast.FunctionDef):
                    defs.setdefault((p.stem, n.name), n)
    pnames = set()
    for pm in pmods:
        for st in ast.parse(pm.read_text()).body:
            if isinstance(st, ast.Assign):
                for t in st.targets:
                    pnames |= {e.id for e in ([t] if isinstance(t, ast.Name) else getattr(t, "elts", [])) if isinstance(e, ast.Name)}
    root = (spec.raw or {}).get("sldprt_dumps") or DEFAULT_ROOT
    entries = {e.get("part"): e for e in _cfg(spec).get("parts") or []}
    groups = {}
    for p in spec.parts:
        sh = p.shape if isinstance(p.shape, dict) else {}
        key = (sh.get("params") or {}).get("part") if sh.get("type") == "model" else None
        if not key:
            continue
        _mod, fname = _part_module(spec, key)
        if _mod is None or (_mod.stem, fname) not in defs:
            continue
        g = groups.setdefault(fname, {"parts": [], "dumps": [], "key": (_mod.stem, fname)})
        g["parts"].append(p.id)
        d = find_dump(root, entries[p.id]) if p.id in entries else None
        if d:
            g["dumps"].append(d)
    rows = []
    for fname, g in groups.items():
        fns = _closure(g["key"], defs)
        ours, used = 0, set()
        for f in fns:
            for x in ast.walk(defs[f]):
                v = _num(x)
                if v is not None and v not in TRIVIAL and not (isinstance(x, ast.Constant) and isinstance(getattr(x, "_parent", None), ast.UnaryOp)):
                    ours += 1
                if isinstance(x, ast.Name) and x.id in pnames:
                    used.add(x.id)
        ours += sum(numeric_tokens(pm.read_text(), used) for pm in pmods)
        lh = sorted(set(g["dumps"]), key=lambda d: (d.lower().startswith("mirror") or " rh" in d.lower() or "right" in d.lower(), d))
        ref = dump_dims((dumps_dir(root) / f"{lh[0]}.dump.txt").read_text(errors="replace")) if lh else None
        rows.append({"function": fname, "parts": g["parts"], "ours": ours, "ref": ref, "dump": lh[0] if lh else None,
                     "ratio": round(ours / ref, 2) if ref else None})
    return sorted(rows, key=lambda r: (r["ratio"] is None, -(r["ratio"] or 0)))


def budget_findings(spec):
    try:
        rows = budget_rows(spec)
    except Exception as ex:  # noqa: BLE001
        return [fail("param.budget", G, WARNING, "Dimension budget could not be computed", str(ex))], []
    over = [r for r in rows if r["ratio"] is not None and r["ratio"] > BUDGET_FRAC]
    msg = "; ".join(f"{r['function']} ({', '.join(r['parts'][:4])}) {r['ours']} vs {r['dump']} {r['ref']} (x{r['ratio']})" for r in over)
    return ([fail("param.budget", G, WARNING, "More numbers than the reference design has dimensions",
                  f"{len(over)} build functions exceed {BUDGET_FRAC}x the SolidWorks dimension count: {msg}")
             .fix("Derive from fewer masters (relations, patterns, mirror) - the reference needs only its DIM count.")] if over else
            [ok("param.budget", G, "Within the reference dimension budget", f"{len(rows)} build functions checked")]), rows


def run(ctx):
    spec = ctx.r.spec
    ov = override_findings(_section(spec, "param"), DEFAULTS, "param", "param.override", G)
    if not params(spec, "param", DEFAULTS)["enabled"]:
        return ov
    out, total = lint_spec(spec)
    out += ov
    ctx.metrics["param.literal_count"] = total
    add, counts = addon_findings(spec)
    out += add
    ctx.metrics["param.copied_count"] = counts["copied"]
    ctx.metrics["style.star_import_count"] = counts["star_import"]
    ctx.metrics["param.point_table_count"] = counts["point_table"]
    bf, rows = budget_findings(spec)
    out += bf
    ctx.metrics["param.budget"] = rows
    if getattr(ctx, "world", None) is not None:
        out += symmetry_findings(ctx)
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
