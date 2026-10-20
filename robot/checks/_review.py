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


# Per-threshold bounds a spec override is clamped to (lo, hi); None = unbounded on that side.
BOUNDS = {
    "param": {"max_literals": (0, 10), "dup_min": (2, 6)},
    "sharp_corner": {"min_r_mm": (0.3, None), "load_min_r_mm": (0.6, None), "load_dist_mm": (1.0, None),
                     "ref_tol_mm": (0.0, 0.5), "window_mm": (1.0, 8.0), "grid_mm": (0.5, 3.0), "link_mm": (0.5, 5.0),
                     "min_turn_deg": (10.0, 90.0)},
}


def resolve(section, defaults, bounds=None):
    """Merge a spec override `section` over `defaults`. Overrides need a non-empty `reason` (else ignored) and numeric
    ones are clamped to `bounds`. Returns (merged, problems [str], active {k: v})."""
    got = dict(section or {})
    reason = str(got.pop("reason", "") or "").strip()
    got = {k: v for k, v in got.items() if k in defaults}
    if not got:
        return dict(defaults), [], {}
    if not reason:
        return dict(defaults), [f"overrides {got} have no `reason`; ignored"], {}
    merged, probs = dict(defaults), []
    for k, v in got.items():
        lo, hi = (bounds or {}).get(k, (None, None))
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            c = v if lo is None else max(lo, v)
            c = c if hi is None else min(hi, c)
            if c != v:
                probs.append(f"`{k}: {v}` outside [{lo}, {hi}]; clamped to {c}")
            v = c
        merged[k] = v
    return merged, probs, {k: merged[k] for k in got} | {"reason": reason}


def _section(spec, key):
    return ((spec.raw or {}).get("review") or {}).get(key) or {}


def params(spec, key, defaults):
    """`spec.review[key]` merged over `defaults` (per-robot thresholds; needs a `reason`, clamped to BOUNDS)."""
    return resolve(_section(spec, key), defaults, BOUNDS.get(key))[0]


def override_findings(section, defaults, key, cid, group):
    """Findings echoing a spec's threshold overrides: WARNING for ignored / clamped ones, INFO note for active ones."""
    from ..finding import WARNING, fail, note

    _, probs, active = resolve(section, defaults, BOUNDS.get(key))
    out = [fail(cid, group, WARNING, "Threshold override not applied as written", f"`{key}`: {p}.")
           .fix("Give the override a `reason` and keep it inside the bounds.") for p in probs]
    if active:
        out.append(note(cid, group, "Threshold override active", f"`{key}`: {active}."))
    return out


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
