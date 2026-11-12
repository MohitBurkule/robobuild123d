from __future__ import annotations


def x(o, k, default=None):
    """Spec field or `_extra` key (spec objects keep unknown keys there)."""
    v = getattr(o, k, None)
    if v is None:
        v = (getattr(o, "_extra", None) or {}).get(k, default)
    return v if v is not None else default


def size_of(designation: str) -> str:
    """'M3x8 DIN7991' -> 'M3'."""
    d = (designation or "").upper().replace(" ", "")
    return d.split("X")[0] if d.startswith("M") else (d or "?")
