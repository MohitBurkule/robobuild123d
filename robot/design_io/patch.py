"""Design patch language (B4): iterate on a design.json without resending the whole file.

A patch is a list of ops on dotted paths into the design dict:
  {"op": "set",   "path": "drive.motor", "value": "n20_1000rpm_6v"}
  {"op": "nudge", "path": "body.zt",     "delta": 1.5}
  {"op": "unset", "path": "skirts"}
`apply(design, patch) -> (design, errors)` never mutates the input; `diff(a, b)`
returns the patch that turns `a` into `b` (so `apply(a, diff(a, b)) == b` for
JSON-native values). Unknown paths come back as errors with the allowed sibling
paths, so an LLM can correct itself in one round trip.
"""

from __future__ import annotations

import copy


def _get(d, path):
    cur = d
    for p in path.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def _set(d, path, value):
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    cur[parts[-1]] = value


def _unset(d, path):
    parts = path.split(".")
    cur = d
    for p in parts[:-1]:
        if not isinstance(cur, dict) or p not in cur:
            return
        cur = cur[p]
    if isinstance(cur, dict):
        cur.pop(parts[-1], None)


def _allowed_paths(d, prefix=""):
    out = set()
    for k, v in (d or {}).items():
        p = f"{prefix}{k}"
        out.add(p)
        if isinstance(v, dict):
            out |= _allowed_paths(v, p + ".")
    return out


def _err(code, field, message, value=None, allowed=None, hint=None):
    e = {"code": code, "field": field, "message": message}
    if value is not None:
        e["value"] = value
    if allowed is not None:
        e["allowed"] = sorted(allowed)
    if hint:
        e["hint"] = hint
    return e


def apply(design, patch):
    """(new design dict, errors). Ops: set (value), nudge (delta on a number), unset."""
    out = copy.deepcopy(design if isinstance(design, dict) else {})
    errors = []
    if not isinstance(patch, list):
        return out, [_err("bad_type", "", "a patch is a list of ops")]
    for i, op in enumerate(patch):
        if not isinstance(op, dict) or op.get("op") not in ("set", "nudge", "unset"):
            errors.append(_err("bad_op", f"patch[{i}]", "op must be set, nudge or unset", (op or {}).get("op")))
            continue
        path = op.get("path")
        if not isinstance(path, str) or not path:
            errors.append(_err("bad_path", f"patch[{i}]", "path must be a non-empty dotted string", path))
            continue
        known = _allowed_paths(design)
        if path not in known and op["op"] != "set":
            errors.append(_err("unknown_path", path, f"no value at {path!r}", path, known,
                               "paths of the current design; use set to create a new key"))
            continue
        if op["op"] == "set":
            if "value" not in op:
                errors.append(_err("bad_op", path, "set needs a value"))
                continue
            _set(out, path, op["value"])
        elif op["op"] == "nudge":
            cur = _get(out, path)
            delta = op.get("delta")
            if not isinstance(delta, (int, float)) or isinstance(delta, bool):
                errors.append(_err("bad_op", path, "nudge needs a numeric delta"))
                continue
            if not isinstance(cur, (int, float)) or isinstance(cur, bool):
                errors.append(_err("bad_type", path, "nudge applies to a number", cur))
                continue
            _set(out, path, round(cur + delta, 6))
        else:
            _unset(out, path)
    return out, errors


def diff(a, b, prefix=""):
    """Patch (list of ops) turning design `a` into `b`. New keys become set; changed
    numbers become nudge when the delta is exact, else set; removals become unset."""
    ops = []
    for k in sorted(set(a or {}) | set(b or {})):
        path = f"{prefix}{k}"
        va, vb = (a or {}).get(k), (b or {}).get(k)
        if va == vb:
            continue
        if isinstance(va, dict) and isinstance(vb, dict):
            ops += diff(va, vb, path + ".")
        elif k not in (a or {}):
            ops.append({"op": "set", "path": path, "value": vb})
        elif k not in (b or {}):
            ops.append({"op": "unset", "path": path})
        elif isinstance(va, (int, float)) and isinstance(vb, (int, float)) and not isinstance(va, bool) \
                and not isinstance(vb, bool):
            ops.append({"op": "nudge", "path": path, "delta": round(vb - va, 6)})
        else:
            ops.append({"op": "set", "path": path, "value": vb})
    return ops
