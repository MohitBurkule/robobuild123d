"""Incremental run cache: memoised geometry queries, per-group check results and renders.

Everything lives in one SQLite file under the geometry cache directory (`$ROBOT_CACHE`, default ~/.cache/robot).
Keys are content hashes, so a stale entry can never be returned for changed inputs:

  * query memos (overlap, min_gap, inside, distance): key = query name + each body's geometry key and placement matrix
    + the arguments. A pairwise query therefore only re-runs when one of its two parts (or their placement) changed.
  * group results: key = the group's source + the core/check sources + the spec JSON + every part geometry key +
    options. A hit restores the group's findings and every context field it wrote.
  * renders: key = scene hash (body geometry keys, matrices, colours) + view + markers.

`ROBOT_NO_CACHE=1` (or `--no-cache`) turns it off; `stats()` reports hits and misses per kind.
"""

from __future__ import annotations

import hashlib
import os
import pickle
import sqlite3
import threading
from collections import Counter
from pathlib import Path

import numpy as np

VERSION = "1"
HERE = Path(__file__).parent
_enabled = not os.environ.get("ROBOT_NO_CACHE")
_db = None
_db_pid = None
_lock = threading.Lock()
hits: Counter = Counter()
misses: Counter = Counter()


def enabled() -> bool:
    return _enabled


def set_enabled(on: bool) -> None:
    global _enabled
    _enabled = bool(on)
    if not on:
        os.environ["ROBOT_NO_CACHE"] = "1"
    else:
        os.environ.pop("ROBOT_NO_CACHE", None)


def reset_stats() -> None:
    hits.clear()
    misses.clear()


def stats() -> dict:
    kinds = sorted(set(hits) | set(misses))
    return {k: {"hits": hits[k], "misses": misses[k]} for k in kinds}


def stats_line() -> str:
    s = stats()
    if not s:
        return "cache: no lookups" + ("" if _enabled else " (disabled)")
    return "cache: " + ", ".join(f"{k} {v['hits']} hit / {v['misses']} miss" for k, v in s.items())


def _conn():
    global _db, _db_pid
    if _db is None or _db_pid != os.getpid():
        from .geom import cache_dir

        _db = sqlite3.connect(str(cache_dir() / f"runs-v{VERSION}.sqlite"), timeout=60, check_same_thread=False)
        _db.execute("PRAGMA journal_mode=WAL")
        _db.execute("PRAGMA synchronous=NORMAL")
        _db.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v BLOB)")
        _db_pid = os.getpid()
    return _db


_MISSING = object()


def get(kind: str, key: str):
    if not _enabled:
        return _MISSING
    with _lock:
        row = _conn().execute("SELECT v FROM kv WHERE k=?", (f"{kind}:{key}",)).fetchone()
    if row is None:
        misses[kind] += 1
        return _MISSING
    try:
        v = pickle.loads(row[0])
    except Exception:  # noqa: BLE001 - a corrupt entry is a miss
        misses[kind] += 1
        return _MISSING
    hits[kind] += 1
    return v


def put(kind: str, key: str, value) -> None:
    if not _enabled:
        return
    try:
        blob = pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as e:  # noqa: BLE001 - unpicklable results are just not cached
        print(f"  [not cached] {kind}: {type(e).__name__}: {e}", flush=True)
        return
    with _lock:
        c = _conn()
        c.execute("INSERT OR REPLACE INTO kv VALUES (?, ?)", (f"{kind}:{key}", blob))
        c.commit()


def is_missing(v) -> bool:
    return v is _MISSING


# ---------------------------------------------------------------------------- hashing


def h(*parts) -> str:
    d = hashlib.sha256()
    for p in parts:
        _feed(d, p)
    return d.hexdigest()[:32]


def _feed(d, p):
    if isinstance(p, np.ndarray):
        a = np.ascontiguousarray(p)
        d.update(str(a.dtype).encode() + str(a.shape).encode())
        d.update(a.tobytes())
    elif isinstance(p, (bytes, bytearray)):
        d.update(p)
    elif isinstance(p, (list, tuple)):
        d.update(b"[")
        for x in p:
            _feed(d, x)
        d.update(b"]")
    elif isinstance(p, float):
        d.update(repr(round(p, 9)).encode())
    else:
        d.update(repr(p).encode())
    d.update(b"|")


def body_sig(b) -> tuple:
    """Geometry key + placement of a body (all a mesh query depends on)."""
    return (b.geom.key, np.round(np.asarray(b.M, float), 9))


_SRC: dict = {}


def source_hash(*files) -> str:
    out = []
    for f in files:
        f = Path(f)
        try:
            st = f.stat()
            k = (f, st.st_mtime_ns, st.st_size)  # stat only invalidates this in-process memo; the key is the content
        except OSError:
            out.append("missing")
            continue
        if k not in _SRC:
            try:
                _SRC[k] = hashlib.sha256(f.read_bytes()).hexdigest()
            except OSError:
                _SRC[k] = "missing"
        out.append(_SRC[k])
    return h(*out)


_LIBS = ("manifold3d", "trimesh", "numpy", "scipy", "shapely")
_LIBV = None


def _ocp_version() -> str:
    """OCCT binding version from the imported OCP module itself (pip metadata is missing on some installs)."""
    try:
        import OCP

        return str(getattr(OCP, "__version__", "") or "-")
    except Exception:  # noqa: BLE001 - not installed
        return "-"


def lib_versions() -> str:
    """Versions of the geometry libraries verdicts depend on (a library upgrade can change a mesh or a query)."""
    global _LIBV
    if _LIBV is None:
        from importlib import metadata

        out = [f"OCP={_ocp_version()}"]  # build123d is left out: the repo code is hashed, and its scm suffix differs per install
        for n in _LIBS:
            try:
                out.append(f"{n}={metadata.version(n)}")
            except Exception:  # noqa: BLE001 - not installed
                out.append(f"{n}=-")
        _LIBV = ";".join(out)
    return _LIBV


def code_hash() -> str:
    """Hash of every python source the verdicts depend on (the whole robot package incl. robot/cad and check
    subpackages, catalog data, rules) + library versions. Content only: the install path never enters the key."""
    files = [f for f in HERE.rglob("*.py") if "tests" not in f.relative_to(HERE).parts]
    files += list((HERE / "catalog_data").rglob("*")) if (HERE / "catalog_data").exists() else []
    files += list((HERE / "rules").rglob("*")) if (HERE / "rules").exists() else []
    files = sorted({f for f in files if f.is_file() and "__pycache__" not in f.parts})
    return h(VERSION, lib_versions(), [(f.relative_to(HERE).as_posix(), source_hash(f)) for f in files])


# ---------------------------------------------------------------------------- model-file dependency closure

_DATA_EXT = (".json", ".csv", ".yaml", ".yml", ".txt", ".stl", ".step", ".stp", ".dxf", ".svg")


def _resolve_module(name: str, roots) -> list[Path]:
    parts = name.split(".")
    for root in roots:
        base = root.joinpath(*parts)
        for c in (base.with_suffix(".py"), base / "__init__.py"):
            if c.is_file():
                return [c]
    return []


def _imports(f: Path) -> tuple[list[str], list[str]]:
    """(module names imported anywhere in f, incl. inside functions; string literals naming data files)."""
    import ast

    try:
        tree = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
    except SyntaxError:
        return [], []
    mods, data = [], []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative: resolve against f's package directory
                d = f.parent
                for _ in range(node.level - 1):
                    d = d.parent
                for a in node.names:
                    mods.append(("rel", d, ((node.module + ".") if node.module else "") + a.name))
                    if node.module:
                        mods.append(("rel", d, node.module))
            elif node.module:
                mods.append(node.module)
                mods += [f"{node.module}.{a.name}" for a in node.names]  # `from pkg import submodule`
        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and len(node.value) < 200 \
                and node.value.lower().endswith(_DATA_EXT):
            data.append(node.value)
    return mods, data


def model_closure(f, roots=()) -> list[tuple[str, Path]]:
    """Every local file a model file depends on: itself, the python modules it imports (transitively: sibling
    params/helper modules next to it and the robot package's own modules) and data files it names by a relative
    literal. Returned as (path-independent label, path); stdlib/site-packages modules are covered by lib_versions."""
    f = Path(f).resolve()
    roots = [f.parent, HERE.parent, *[Path(r) for r in roots]]
    seen: dict[Path, str] = {}
    todo = [(f, "main")]
    while todo:
        cur, label = todo.pop()
        if cur in seen:
            continue
        seen[cur] = label
        if cur.suffix != ".py":
            continue
        mods, data = _imports(cur)
        for m in mods:
            if isinstance(m, tuple):
                _, d, name = m
                hits = _resolve_module(name, [d])
            else:
                ps = m.split(".")  # importing a.b.c also runs a/__init__ and a/b/__init__
                hits = [x for i in range(1, len(ps) + 1) for x in _resolve_module(".".join(ps[:i]), roots + [cur.parent])]
            for p in hits:
                p = p.resolve()
                todo.append((p, _label(p, f.parent)))
        for s in data:
            p = (cur.parent / s)
            if p.is_file():
                todo.append((p.resolve(), _label(p.resolve(), f.parent)))
    return sorted(((lab, p) for p, lab in seen.items()), key=lambda t: t[0])


def _label(p: Path, model_dir: Path) -> str:
    for base, tag in ((HERE.parent, "pkg"), (model_dir, "local")):
        try:
            return f"{tag}:{p.relative_to(base).as_posix()}"
        except ValueError:
            pass
    return f"abs:{p.name}"


def model_hash(f, roots=()) -> str:
    """Content hash of a model file and everything it depends on (see model_closure)."""
    f = Path(f)
    if not f.is_file():
        return h("missing", f.name)
    return h("model", [(lab, source_hash(p)) for lab, p in model_closure(f, roots)])


def referenced_hash(raw, base_dir) -> str:
    """Content hash of every file or directory the spec names by a path relative to its folder (reference CAD dirs,
    photos, model files...). Replaces the folder path in group keys: same content in two folders = same key."""
    if base_dir is None:
        return "nobase"
    base_dir = Path(base_dir)
    strs: set = set()

    def walk(v):
        if isinstance(v, dict):
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)
        elif isinstance(v, str) and 0 < len(v) < 300 and "\n" not in v and v not in (".", "./"):
            strs.add(v)

    walk(raw)
    out = []
    for s in sorted(strs):
        try:
            p = base_dir / s
            if p.is_file():
                out.append((s, model_hash(p) if p.suffix == ".py" else source_hash(p)))
            elif p.is_dir() and p.resolve() != base_dir.resolve():
                fs = sorted(x for x in p.rglob("*") if x.is_file())
                out.append((s, [(x.relative_to(p).as_posix(), source_hash(x)) for x in fs]))
        except (OSError, ValueError):
            continue
    return h("refs", out)


def memo(kind: str, key_parts, compute):
    """Return the cached value for `key_parts`, else compute and store it."""
    if not _enabled:
        return compute()
    k = h(*key_parts)
    v = get(kind, k)
    if v is not _MISSING:
        return v
    v = compute()
    put(kind, k, v)
    return v
