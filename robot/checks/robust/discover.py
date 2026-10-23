"""Find a robot's master params, their relations and its variant switches by reading the build sources (AST only).

* numeric params: module-level `NAME = <number>` / `A, B = 1.0, 2.0` / `T = (1.0, 2.0)` in params modules
  (`params*.py`, `*_params.py`). Tuple elements are separate params `T[i]`. Optional declared bounds:
  a `# bounds: lo..hi` comment on the line, or spec `review.robust.bounds: {NAME: [lo, hi]}`.
* relations: module-level assignments in those modules whose value is an expression of other names.
* variant switches: a `VARIANTS` dict with `set_variants` (each named switch on/off), `X = os.environ.get("ENV", "d")`
  catalog / model choices (alternatives from an `XS` dict, or string comparisons with X or the env call), and
  module-level bool params (`FLAG = False`).
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

BOUNDS_RE = re.compile(r"#.*\bbounds:\s*(-?[\d.]+)\s*\.\.\s*(-?[\d.]+)")
MASTER_RE = re.compile(r"MASTER DESIGN PARAM", re.I)


@dataclass
class Param:
    name: str  # NAME or NAME[i]
    symbol: str  # NAME (what code reads)
    value: float
    file: Path
    line: int  # 1-based
    col: int
    end_col: int
    is_int: bool = False
    master: bool = False
    bounds: tuple | None = None


@dataclass
class Switch:
    name: str  # variant name, env var, or flag name
    kind: str  # "variant" | "choice" | "flag"
    symbol: str  # what code reads (variant: the name string; choice/flag: the module constant)
    default: object
    alternatives: list
    file: Path
    line: int = 0
    col: int = 0
    end_col: int = 0


@dataclass
class Discovery:
    params: list = field(default_factory=list)
    switches: list = field(default_factory=list)
    relations: dict = field(default_factory=dict)  # derived name -> [names it reads]
    package: Path | None = None


def is_params_file(p: Path) -> bool:
    return p.suffix == ".py" and (p.stem.startswith("params") or p.stem.endswith("_params"))


def _num(node):
    """(value, is_int) of a numeric literal (with unary minus), else None."""
    neg = False
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        neg, node = isinstance(node.op, ast.USub), node.operand
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
        v = -node.value if neg else node.value
        return float(v), isinstance(node.value, int)
    return None


def _span(node):
    """(line, col, end_col) of a literal including its sign; single-line only."""
    if node.lineno != node.end_lineno:
        return None
    return node.lineno, node.col_offset, node.end_col_offset


def _names(node) -> list:
    return sorted({n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)})


def _master_lines(lines) -> tuple:
    """Line range (1-based, inclusive) of a `MASTER DESIGN PARAMETERS` block, ended by the next `# ----` rule."""
    for i, ln in enumerate(lines):
        if MASTER_RE.search(ln):
            for j in range(i + 1, len(lines)):
                if lines[j].lstrip().startswith("# ---"):
                    return i + 1, j + 1
            return i + 1, len(lines)
    return 0, -1


def params_in_file(f: Path, bounds: dict | None = None) -> tuple:
    """(params, relations, flags) of one params module."""
    src = f.read_text()
    lines = src.splitlines()
    tree = ast.parse(src)
    m0, m1 = _master_lines(lines)
    bounds = bounds or {}
    out, rel, flags = [], {}, []

    def add(name, sym, node):
        nv, sp = _num(node), _span(node)
        if nv is None or sp is None:
            return False
        b = bounds.get(name) or bounds.get(sym)
        m = BOUNDS_RE.search(lines[sp[0] - 1])
        if b is None and m:
            b = (float(m.group(1)), float(m.group(2)))
        out.append(Param(name, sym, nv[0], f, sp[0], sp[1], sp[2], nv[1], m0 <= sp[0] <= m1, tuple(b) if b else None))
        return True

    for st in tree.body:
        if not isinstance(st, ast.Assign) or len(st.targets) != 1:
            continue
        t, v = st.targets[0], st.value
        if isinstance(t, ast.Name):
            if isinstance(v, ast.Constant) and isinstance(v.value, bool) and _span(v):
                ln, c0, c1 = _span(v)
                flags.append(Switch(t.id, "flag", t.id, v.value, [not v.value], f, ln, c0, c1))
            elif add(t.id, t.id, v):
                pass
            elif isinstance(v, ast.Tuple) and all(_num(e) is not None for e in v.elts):
                for i, e in enumerate(v.elts):
                    add(f"{t.id}[{i}]", t.id, e)
            else:
                ns = _names(v)
                if ns:
                    rel[t.id] = ns
        elif isinstance(t, ast.Tuple) and isinstance(v, ast.Tuple) and len(t.elts) == len(v.elts):
            for te, ve in zip(t.elts, v.elts):
                if not isinstance(te, ast.Name):
                    continue
                if not add(te.id, te.id, ve):
                    ns = _names(ve)
                    if ns:
                        rel[te.id] = ns
    return out, rel, flags


def _env_get(node):
    """('ENV', default node) for os.environ.get("ENV", "default") / os.getenv(...), else None."""
    if not isinstance(node, ast.Call) or len(node.args) != 2:
        return None
    fn = ast.unparse(node.func)
    a, d = node.args
    if fn in ("os.environ.get", "os.getenv", "environ.get", "getenv") and isinstance(a, ast.Constant) and isinstance(d, ast.Constant) \
            and isinstance(d.value, str):
        return a.value, d
    return None


def switches_in_package(files) -> list:
    """Variant switches (VARIANTS + set_variants) and env-var choices across the package files."""
    trees = {f: ast.parse(f.read_text()) for f in files}
    out = []
    compares: dict = {}  # name -> string constants it is compared with
    dicts: dict = {}  # NAME -> keys of a module-level dict literal
    for f, tree in trees.items():
        for n in ast.walk(tree):
            if isinstance(n, ast.Compare) and len(n.comparators) == 1 and isinstance(n.ops[0], (ast.Eq, ast.NotEq)):
                left, right = n.left, n.comparators[0]
                for a, b in ((left, right), (right, left)):
                    if isinstance(b, ast.Constant) and isinstance(b.value, str):
                        compares.setdefault(ast.unparse(a), set()).add(b.value)
        for st in tree.body:
            if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) and isinstance(st.value, ast.Dict):
                ks = [k.value for k in st.value.keys if isinstance(k, ast.Constant) and isinstance(k.value, str)]
                if ks:
                    dicts[st.targets[0].id] = ks
    for f, tree in trees.items():
        top = {type(s).__name__ + ":" + getattr(s, "name", "") for s in tree.body}
        names = None
        for st in tree.body:
            if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name):
                tn = st.targets[0].id
                if tn == "NAMES" and isinstance(st.value, ast.Tuple):
                    names = [e.value for e in st.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
                v = st.value
                cmp_on = None
                if isinstance(v, ast.Compare) and _env_get(v.left):
                    cmp_on = [c.value for c in v.comparators if isinstance(c, ast.Constant) and isinstance(c.value, str)]
                    v = v.left
                eg = _env_get(v)
                if eg:
                    env, d = eg
                    alts = set(cmp_on or ()) | set(dicts.get(tn + "S", ())) | compares.get(tn, set()) | compares.get(ast.unparse(v), set())
                    if cmp_on:
                        alts |= {"on", "off"} if set(cmp_on) <= {"on", "off"} else set()
                    alts.discard(d.value)
                    if alts:
                        out.append(Switch(env, "choice", tn, d.value, sorted(alts), f, d.lineno, d.col_offset, d.end_col_offset))
        if names and "FunctionDef:set_variants" in top:
            for nm in names:
                out.append(Switch(nm, "variant", nm, False, [True], f))
    return out


def package_files(model_file: Path) -> list:
    """The python sources a model file builds from: its own folder and sub-packages (no tests, no caches)."""
    root = Path(model_file).resolve().parent
    return sorted(p for p in root.rglob("*.py") if "test" not in p.parts[-1] and "__pycache__" not in p.parts)


def discover(model_file: Path, bounds: dict | None = None) -> Discovery:
    files = package_files(model_file)
    d = Discovery(package=Path(model_file).resolve().parent)
    flags = []
    for f in files:
        if is_params_file(f):
            ps, rel, fl = params_in_file(f, bounds)
            d.params += ps
            d.relations.update(rel)
            flags += fl
    d.switches = switches_in_package(files) + flags
    return d


def _str_consts(tree) -> dict:
    """Module-level NAME = "string" constants (an env name kept in a constant)."""
    out = {}
    for st in tree.body:
        if isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name) \
                and isinstance(st.value, ast.Constant) and isinstance(st.value.value, str):
            out[st.targets[0].id] = st.value.value
    return out


def _str_of(node, consts):
    """The string a node evaluates to when it is a constant, a constant name, or a +/f-string of those, else None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        a, b = _str_of(node.left, consts), _str_of(node.right, consts)
        return a + b if a is not None and b is not None else None
    if isinstance(node, ast.JoinedStr):
        parts = [v.value if isinstance(v, ast.Constant) else _str_of(v.value, consts) if isinstance(v, ast.FormattedValue) else None
                 for v in node.values]
        return "".join(parts) if all(isinstance(x, str) for x in parts) else None
    return None


def env_setting(files, env: str):
    """A module-level build setting read from env var `env`, as a choice Switch whose default literal can be edited,
    or None. The read may be os.environ.get / os.getenv / environ.get, or any helper called as
    helper(<env>, "<default>", ...); the env name may be a literal, a module string constant or a +/f-string of them."""
    for f in files:
        tree = ast.parse(Path(f).read_text())
        consts = _str_consts(tree)
        for st in tree.body:
            if not (isinstance(st, ast.Assign) and len(st.targets) == 1 and isinstance(st.targets[0], ast.Name)):
                continue
            for n in ast.walk(st.value):
                if isinstance(n, ast.Call) and len(n.args) >= 2 and _str_of(n.args[0], consts) == env \
                        and isinstance(n.args[1], ast.Constant) and isinstance(n.args[1].value, str) and _span(n.args[1]):
                    d = n.args[1]
                    return Switch(env, "choice", st.targets[0].id, d.value, [], Path(f), d.lineno, d.col_offset, d.end_col_offset)
    return None


def reads_env(files, env: str) -> bool:
    """True when the build sources name env var `env` anywhere (a literal, a constant, or a +/f-string of constants),
    e.g. inside a helper that reads os.environ at call time: the setting is real even without an editable default."""
    for f in files:
        tree = ast.parse(Path(f).read_text())
        consts = _str_consts(tree)
        for n in ast.walk(tree):
            if isinstance(n, (ast.Constant, ast.Name, ast.BinOp, ast.JoinedStr)) and _str_of(n, consts) == env:
                return True
    return False
