"""Which parts read which params: a static name graph over the build package (AST only, no build).

Every module-level statement and def links the names it defines to the names (and string literals) it reads; modules
that share one namespace (star imports) merge by name. A part's entry is the value of its key in a module-level `PARTS`
dict (or `build` when there is none); the part reads a param when the param's name is in the entry's closure, and a
variant when its name string is.
"""

from __future__ import annotations

import ast
from collections import defaultdict
from pathlib import Path


class Graph:
    def __init__(self):
        self.deps: dict = defaultdict(set)  # name -> names it reads
        self.strs: dict = defaultdict(set)  # name -> string literals in its definition
        self.parts: dict = {}  # part key -> (names, strings) of its PARTS entry

    def closure(self, names) -> tuple:
        seen, todo = set(), list(names)
        while todo:
            n = todo.pop()
            if n in seen:
                continue
            seen.add(n)
            todo += [m for m in self.deps.get(n, ()) if m not in seen]
        strs = set().union(*(self.strs.get(n, set()) for n in seen)) if seen else set()
        return seen, strs


def _local_names(node) -> set:
    """Names bound inside functions / lambdas / comprehensions of `node` (args and stores), minus `global` ones."""
    out, glob = set(), set()
    for n in ast.walk(node):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            a = n.args
            out |= {x.arg for x in a.posonlyargs + a.args + a.kwonlyargs}
            out |= {x.arg for x in (a.vararg, a.kwarg) if x}
            for m in ast.walk(n):
                if isinstance(m, ast.Name) and isinstance(m.ctx, ast.Store):
                    out.add(m.id)
                elif isinstance(m, ast.Global):
                    glob |= set(m.names)
        elif isinstance(n, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            for gen in n.generators:
                out |= {m.id for m in ast.walk(gen.target) if isinstance(m, ast.Name)}
    return out - glob


def _loads_strs(node):
    """(global names read, string literals) of a top-level statement; function-local names are not reads."""
    names, strs = set(), set()
    for n in ast.walk(node):
        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
            names.add(n.id)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str) and len(n.value) < 64:
            strs.add(n.value)
    return names - _local_names(node), strs


def _stores(st):
    if isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return {st.name}
    return {n.id for n in ast.walk(st) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}


def build_graph(files) -> Graph:
    g = Graph()
    for f in files:
        try:
            tree = ast.parse(Path(f).read_text())
        except SyntaxError:
            continue
        for st in tree.body:
            if isinstance(st, (ast.Import, ast.ImportFrom)):
                continue
            outs = _stores(st)
            names, strs = _loads_strs(st)
            for o in outs:
                g.deps[o] |= names - {o}
                g.strs[o] |= strs
            if isinstance(st, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PARTS" for t in st.targets) \
                    and isinstance(st.value, ast.Dict):
                for k, v in zip(st.value.keys, st.value.values):
                    if isinstance(k, ast.Constant) and isinstance(k.value, str):
                        g.parts[k.value] = _loads_strs(v)
    return g


def part_reads(g: Graph, key: str) -> tuple:
    """(names, strings) in the closure of one part key (all of `build` when the key is not in PARTS)."""
    names, strs = g.parts.get(key) or ({"build"}, set())
    seen, s2 = g.closure(names)
    return seen, s2 | strs


def model_keys(shape) -> list:
    """`params.part` of every model node in a shape tree (None for a model without one)."""
    out = []
    if isinstance(shape, dict):
        if shape.get("type") == "model":
            out.append((shape.get("params") or {}).get("part"))
        for v in shape.values():
            if isinstance(v, (dict, list)):
                out += model_keys(v)
    elif isinstance(shape, list):
        for v in shape:
            out += model_keys(v)
    return out


def spec_part_keys(raw) -> dict:
    """{spec part id: [model part keys]} for parts built from model files."""
    out = {}
    for p in raw.get("parts", []):
        ks = model_keys(p.get("shape")) if p.get("shape") else []
        if p.get("model"):
            ks.append((p.get("params") or {}).get("part"))
        if ks:
            out[p["id"]] = ks
    return out


class Usage:
    """Per spec part: the set of names / strings its build reads."""

    def __init__(self, g: Graph, raw: dict):
        self.reads = {}
        cache = {}
        for pid, keys in spec_part_keys(raw).items():
            ns, ss = set(), set()
            for k in keys:
                if k not in cache:
                    cache[k] = part_reads(g, k)
                ns |= cache[k][0]
                ss |= cache[k][1]
            self.reads[pid] = (ns, ss)

    def parts_reading(self, symbol: str, string: bool = False) -> list:
        i = 1 if string else 0
        return sorted(pid for pid, r in self.reads.items() if symbol in r[i])
