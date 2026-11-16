"""Override model master params (module-level `NAME = <number>`) without editing code, so derived relations follow.

A robot's params module (e.g. robots/scythe/src/scythe/params.py) holds masters and relations evaluated at import.
Patching a constant after import would leave every derived value stale. Instead, while overrides are active, any
module whose FILE is named in the overrides is compiled with those top-level assignments replaced by the given
values; everything computed from them (pocket positions, bolt-hole patterns, wire slots, part placements that the
spec reads with {"expr": ...}) is then recomputed on import. That is what lets the jiggle solver move a part TOGETHER
with its pocket, holes and cutouts: they are all relations of the same master.

Overrides travel in the environment variable ROBOT_PARAM_OVERRIDES (JSON {"<file path>": {"NAME": value}}) so part
builds in worker processes see them, and they are part of every geometry cache key (robot/geom.py key_for).

    with active({"/abs/robots/scythe/src/scythe/params.py": {"SWITCH_BAY": 9.2}}):
        ...  # resolve / build / verify here

`write(path, {"NAME": v})` edits the literal in the source file (only a plain number on a top-level assignment).
"""

from __future__ import annotations

import ast
import contextlib
import importlib.abc
import importlib.machinery
import importlib.util
import json
import os
import sys
from pathlib import Path

ENV = "ROBOT_PARAM_OVERRIDES"


def current() -> dict:
    """{resolved file path: {name: value}} from the environment."""
    raw = os.environ.get(ENV, "")
    if not raw:
        return {}
    try:
        d = json.loads(raw)
    except ValueError:
        return {}
    return {str(Path(k).resolve()): v for k, v in d.items() if isinstance(v, dict)}


def key() -> str:
    """Stable text for cache keys ('' when no overrides)."""
    d = current()
    return json.dumps(d, sort_keys=True) if d else ""


def transform(src: str, values: dict, filename="<params>"):
    """Code object of `src` with top-level `NAME = ...` (and `NAME: T = ...`) for NAME in values replaced."""
    tree = ast.parse(src, filename)
    seen = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            n = node.targets[0].id
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            n = node.target.id
        else:
            continue
        if n in values:
            node.value = ast.copy_location(ast.Constant(values[n]), node.value)
            seen.add(n)
    missing = set(values) - seen
    if missing:
        raise KeyError(f"{filename}: no top-level assignment for {', '.join(sorted(missing))}")
    return compile(ast.fix_missing_locations(tree), filename, "exec")


class _Loader(importlib.machinery.SourceFileLoader):
    def __init__(self, name, path, values):
        super().__init__(name, path)
        self._values = values

    def get_code(self, fullname):
        return transform(Path(self.path).read_text(encoding="utf-8"), self._values, self.path)


class _Finder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        ov = current()
        if not ov:
            return None
        for f in sys.meta_path:
            if f is self or not hasattr(f, "find_spec"):
                continue
            try:
                s = f.find_spec(fullname, path, target)
            except Exception:  # noqa: BLE001
                continue
            if s is None:
                continue
            o = s.origin and ov.get(str(Path(s.origin).resolve()))
            if o:
                s.loader = _Loader(fullname, s.origin, o)
            return s
        return None


_FINDER = _Finder()


def install():
    if _FINDER not in sys.meta_path:
        sys.meta_path.insert(0, _FINDER)


def load_file(path, name=None):
    """Import a python file by path with the active overrides applied (fresh every call)."""
    install()
    path = Path(path).resolve()
    name = name or f"robot_params_{abs(hash(str(path))) & 0xffffffff:x}"
    vals = current().get(str(path))
    spec = importlib.util.spec_from_file_location(name, path, loader=_Loader(name, str(path), vals) if vals else None)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def purge(root):
    """Drop imported modules whose file is under `root`, so the next import re-derives under new overrides."""
    root = str(Path(root).resolve())
    for n, m in list(sys.modules.items()):
        f = getattr(m, "__file__", None)
        if f and str(Path(f).resolve()).startswith(root + os.sep):
            del sys.modules[n]


@contextlib.contextmanager
def active(overrides: dict, purge_root=None):
    """Set overrides (merged over any already active) for the duration; purges `purge_root` modules on entry/exit."""
    install()
    old = os.environ.get(ENV)
    merged = current()
    for k, v in overrides.items():
        merged.setdefault(str(Path(k).resolve()), {}).update(v)
    os.environ[ENV] = json.dumps(merged, sort_keys=True)
    if purge_root:
        purge(purge_root)
    try:
        yield
    finally:
        if old is None:
            os.environ.pop(ENV, None)
        else:
            os.environ[ENV] = old
        if purge_root:
            purge(purge_root)


def read(path, name):
    """Current literal value of a top-level `name = <number>` in a file (None if not a plain number)."""
    for node in ast.parse(Path(path).read_text(encoding="utf-8")).body:
        tgt = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
        if isinstance(tgt, ast.Name) and tgt.id == name:
            v = node.value
            if isinstance(v, ast.UnaryOp) and isinstance(v.op, ast.USub) and isinstance(v.operand, ast.Constant):
                return -v.operand.value
            return v.value if isinstance(v, ast.Constant) and isinstance(v.value, (int, float)) else None
    return None


def write(path, values: dict):
    """Rewrite the literal of each top-level `NAME = <number>` in place (keeps the trailing comment)."""
    p = Path(path)
    src = p.read_text(encoding="utf-8")
    lines = src.splitlines(keepends=True)
    todo = dict(values)
    for node in ast.parse(src).body:
        tgt = node.targets[0] if isinstance(node, ast.Assign) and len(node.targets) == 1 else getattr(node, "target", None)
        if not (isinstance(tgt, ast.Name) and tgt.id in todo):
            continue
        v = node.value
        if not (v.lineno == v.end_lineno and read(path, tgt.id) is not None):
            raise ValueError(f"{path}: `{tgt.id}` is not a plain number literal; change it by hand")
        i = v.lineno - 1
        ln = lines[i]
        b = len(ln.encode("utf-8")[:v.col_offset].decode("utf-8"))
        e = len(ln.encode("utf-8")[:v.end_col_offset].decode("utf-8"))
        nv = todo.pop(tgt.id)
        lines[i] = ln[:b] + (repr(round(nv, 4)) if isinstance(nv, float) else repr(nv)) + ln[e:]
    if todo:
        raise KeyError(f"{path}: no top-level number for {', '.join(sorted(todo))}")
    p.write_text("".join(lines), encoding="utf-8")
