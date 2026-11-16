"""Group failed findings by root cause, so one physical problem reads as ONE item, not five.

One collision between two parts shows up as interference.overlap, fit.interference, interference.sweep,
assembly.blocked (trapped by the overlapping part) and kin.rub_gap / kin.sweep_*. A small LLM fixing blockers one
by one counts them as five problems and fixes the symptoms. Here findings in the collision family that name the
same pair of parts are merged; the "primary" is the finding that says what to change (the overlap, with its
measured escape moves), the rest are listed as consequences that disappear with it. Other findings with the same id
on the same parts are merged too (repeated reports).
"""

from __future__ import annotations

import re

from .finding import BLOCKER

COLLISION = ("interference.overlap", "fit.interference", "interference.sweep", "assembly.blocked",
             "kin.rub_gap", "kin.sweep_static", "kin.sweep_fastener", "interference.captive")
PRIMARY_ORDER = ("interference.overlap", "fit.interference", "kin.sweep_static", "kin.sweep_fastener",
                 "interference.sweep", "kin.rub_gap", "assembly.blocked", "interference.captive")
_TICK = re.compile(r"`([^`\s]+)`")


def named_parts(f, known=None) -> list:
    """Parts a finding is about: its `parts` list plus every `id` quoted in the message (assembly.blocked names its
    blocker only in the text)."""
    out = list(f.parts or [])
    for m in _TICK.findall(f.message or ""):
        if (known is None or m in known) and m not in out:
            out.append(m)
    return out


def _pair_keys(f, known):
    ps = named_parts(f, known)
    if f.id == "assembly.blocked" and len(ps) >= 2:
        return [frozenset(ps[:2])]
    if len(ps) == 2:
        return [frozenset(ps)]
    if len(ps) > 2:   # a rotor group vs one static part: key on the static part with each member
        return [frozenset((ps[0], p)) for p in ps[1:]]
    return []


def group(findings, known=None, severities=(BLOCKER,)):
    """[{root, primary, parts, findings:[ids], consequences:[...], fix, repair}] most findings first."""
    bad = [f for f in findings if not f.passed and f.severity in severities]
    parent = list(range(len(bad)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        parent[find(i)] = find(j)

    by_key = {}
    for i, f in enumerate(bad):
        keys = _pair_keys(f, known) if f.id in COLLISION else [("same", f.id, tuple(sorted(named_parts(f, known))))]
        for k in keys:
            if k in by_key:
                union(i, by_key[k])
            else:
                by_key[k] = i
    clusters = {}
    for i in range(len(bad)):
        clusters.setdefault(find(i), []).append(bad[i])
    out = []
    for fs in clusters.values():
        fs.sort(key=lambda f: PRIMARY_ORDER.index(f.id) if f.id in PRIMARY_ORDER else len(PRIMARY_ORDER))
        p = fs[0]
        parts = []
        for f in fs:
            parts += [x for x in named_parts(f, known) if x not in parts]
        out.append({"root": f"{p.id}:{'+'.join(sorted(named_parts(p, known))) or '-'}", "primary": p.id,
                    "message": p.message, "parts": parts, "at": p.at, "fix": p.fix_hint,
                    "findings": [f.id for f in fs],
                    "consequences": [f"{f.id}: {f.message}" for f in fs[1:]],
                    "repair": list(p.repair or [])})
    out.sort(key=lambda c: -len(c["findings"]))
    return out


def text(roots) -> str:
    """Short block printed before the per-finding list."""
    n = sum(len(c["findings"]) for c in roots)
    lines = [f"ROOT CAUSES: {len(roots)} (from {n} blockers). Fix these; the consequences go away with them."]
    for k, c in enumerate(roots, 1):
        more = f" [+{len(c['findings']) - 1} consequences: {', '.join(sorted(set(c['findings'][1:])))}]" if len(c["findings"]) > 1 else ""
        lines.append(f" {k}. {c['primary']} - {c['message']}{more}")
    return "\n".join(lines)
