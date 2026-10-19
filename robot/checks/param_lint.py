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
    return {"funcs": funcs, "values": dict(values), "problems": problems}


def sources(spec):
    seen = []
    for p in spec.parts:
        sh = p.shape if isinstance(p.shape, dict) else None
        f = (sh or {}).get("file") if (sh or {}).get("type") == "model" else None
        if f:
            path = (Path(spec.base_dir) / f).resolve()
            if path.suffix == ".py" and path not in seen:
                seen.append(path)
    return seen


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
