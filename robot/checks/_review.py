"""Shared helpers for the design-review groups (ref_map, cots_fidelity, wire_review, fastener_record, belt_wrap,
print_orient). Not a check group itself."""

from __future__ import annotations

import numpy as np


def x(o, k, default=None):
    """Spec field `k` of a part / fastener / wire, whether it is a declared attribute or an extra key."""
    v = getattr(o, k, None)
    if v is None:
        v = (getattr(o, "_extra", None) or {}).get(k, default)
    return v if v is not None else default


def params(spec, key, defaults):
    """`spec.review[key]` merged over `defaults` (per-robot thresholds)."""
    got = ((spec.raw or {}).get("review") or {}).get(key) or {}
    return {**defaults, **got}


def rotating(spec, pid, group="weapon", _seen=None):
    """True when part `pid` turns with the `group` rotor: declared `rotates_with`, a weapon part, or a child of one."""
    _seen = _seen or set()
    p = spec.part(pid) if pid else None
    if p is None or pid in _seen:
        return False
    _seen.add(pid)
    rw = p.rotates_with
    if rw is not None:
        return rw == group
    if group == "weapon" and p.kind == "weapon":
        return True
    return rotating(spec, p.parent, group, _seen) if p.parent else False


def fastener_rotates(spec, f, group="weapon"):
    """A fastener turns with the rotor when every part it passes through (and its nut, if any) does."""
    ids = list(f.through or [])
    host = spec.part(f.threads_into) if f.threads_into else None
    if host is not None and host.kind in ("nut", "insert"):
        ids.append(host.id)
    return bool(ids) and all(rotating(spec, i, group) for i in ids)


def polyline_dist(points, P):
    """Distance from points P (k,3) to the polyline `points`."""
    P = np.atleast_2d(np.asarray(P, float))
    pts = np.asarray(points, float)
    if len(pts) == 1:
        return np.linalg.norm(P - pts[0], axis=1)
    a, b = pts[:-1], pts[1:]
    ab = b - a
    L2 = np.maximum((ab * ab).sum(1), 1e-18)
    ap = P[:, None, :] - a[None]
    t = np.clip((ap * ab[None]).sum(2) / L2[None], 0, 1)
    d = ap - t[..., None] * ab[None]
    return np.sqrt((d * d).sum(2)).min(1)
