"""Per-fastener and per-part waivers: `"waive": {"<check id or prefix>": "<reason>"}` on a fastener or part entry.

A failing BLOCKER whose id matches a waive key and whose parts list that fastener (or part) drops to WARNING with
"waived: <reason>". The reason must be at least MIN_REASON characters and cite the reference (CITE: "RVRN" or "ELVRN", an
RVnn or FSn part id); otherwise the finding stays a BLOCKER with INVALID appended. Never applies to FORBIDDEN groups.
Every waiver used is listed in the report summary under "waivers".
"""

from __future__ import annotations

import re

from ..finding import BLOCKER, WARNING

MIN_REASON = 20
CITE = re.compile(r"RVRN|ELVRN|\bRV\d{2}\b|\bFS\d+\b")
FORBIDDEN = {"assembly", "interference", "reference_cad"}
INVALID = "invalid waiver: needs reason + reference citation"


def valid(reason) -> bool:
    reason = str(reason or "").strip()
    return len(reason) >= MIN_REASON and bool(CITE.search(reason))


def _matches(fid, key) -> bool:
    return fid == key or fid.startswith(key.rstrip(".") + ".")


def apply(spec, findings) -> list:
    """Downgrade waived findings in place; return the waivers used as dicts."""
    used = []
    part_ids = {p.id for p in spec.parts}
    waives = {f.id: (getattr(f, "waive", None) or {}) for f in spec.fasteners}
    for p in spec.parts:
        w = (getattr(p, "_extra", None) or {}).get("waive") or getattr(p, "waive", None)
        if w:
            waives.setdefault(p.id, w)
    for fd in findings:
        if fd.passed or fd.severity != BLOCKER or fd.group in FORBIDDEN:
            continue
        for fid, w in waives.items():
            hit = next((k for k in w if fid in fd.parts and _matches(fd.id, k)), None)
            if hit is None:
                continue
            ok = valid(w[hit])
            if ok:
                fd.severity = WARNING
                fd.message = f"{fd.message} waived: {w[hit]}"
            else:
                fd.message = f"{fd.message} {INVALID}"
            used.append({"fastener" if fid not in part_ids else "part": fid, "check": fd.id, "reason": w[hit], "valid": ok})
            break
    return used
