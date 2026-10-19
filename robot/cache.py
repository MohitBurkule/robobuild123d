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
        if f not in _SRC:
            try:
                _SRC[f] = hashlib.sha256(f.read_bytes()).hexdigest()
            except OSError:
                _SRC[f] = "missing"
        out.append(_SRC[f])
    return h(*out)


def code_hash() -> str:
    """Hash of every python source the verdicts depend on (core + all check groups + catalog data)."""
    files = sorted(HERE.glob("*.py")) + sorted((HERE / "checks").glob("*.py"))
    files += sorted((HERE / "catalog_data").rglob("*")) if (HERE / "catalog_data").exists() else []
    files += sorted((HERE / "rules").rglob("*")) if (HERE / "rules").exists() else []
    return source_hash(*[f for f in files if f.is_file()])


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
