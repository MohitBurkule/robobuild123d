"""Compact LLM report with iteration delta (B2): the full report does not fit a context window.

`compact(rep, prev=None, budget_chars=6000)` returns a dict sized for an LLM:
blockers first (each with its machine-readable repair hints), then warnings,
counts, mass, the not_checked/not_run lists, and - when `prev` (a previous
report dict) is given - a delta so the model can see whether its edit helped.
Repeated ids are deduped by part; findings are ordered by root cause
(validity, legal, mass, fit/interference, everything else).
"""

from __future__ import annotations

import json

ROOT_CAUSE_ORDER = ("validity.", "legal.", "mass.", "fit.", "interference.", "contain.", "assembly.", "disasm.")
BUDGET_SECTIONS = ("blockers", "warnings", "delta", "counts", "mass", "not_checked", "not_run")


def _rank(f):
    idd = f.get("id", "")
    return next((i for i, p in enumerate(ROOT_CAUSE_ORDER) if idd.startswith(p)), len(ROOT_CAUSE_ORDER))


def compact(rep: dict, prev: dict | None = None, budget_chars: int = 6000) -> dict:
    """rep/prev: report dicts (report.json form). Returns the compact dict; oversized
    sections drop their least important entries (warnings first) to stay in budget."""
    failed = [f for f in rep.get("findings", []) if not f.get("pass", True)]
    failed.sort(key=lambda f: (_rank(f), f.get("id", ""), f.get("parts") or []))
    blockers = [f for f in failed if f.get("severity") == "blocker"]
    warnings = [f for f in failed if f.get("severity") != "blocker"]
    m = rep.get("metrics") or {}
    mass = None
    if "mass_total_g" in m:
        mass = {"total": m["mass_total_g"], "lo": m.get("mass_lo_g"), "hi": m.get("mass_hi_g"),
                "limit": m.get("mass_limit_g", 150)}
    out = {"ok": rep.get("ok"), "tier": rep.get("tier"), "gate": rep.get("gate"),
           "blockers": [], "warnings": [], "counts": {"blockers": len(blockers), "warnings": len(warnings),
                                                      "passed": sum(1 for f in rep.get("findings", []) if f.get("pass", True))},
           "mass": mass, "not_checked": rep.get("not_checked", []), "not_run": rep.get("not_run", [])}
    seen = set()
    for f in blockers:
        key = (f.get("id"), tuple(f.get("parts") or []))
        if key in seen:
            continue
        seen.add(key)
        out["blockers"].append({"id": f.get("id"), "msg": f.get("message"), "expected": f.get("expected"),
                                "actual": f.get("actual"), "parts": f.get("parts") or [],
                                "fixes": f.get("repair") or []})
    for f in warnings:
        if len(out["warnings"]) < 20:
            out["warnings"].append({"id": f.get("id"), "msg": f.get("message"), "parts": f.get("parts") or []})
    if prev is not None:
        pf = {f.get("id") for f in prev.get("findings", []) if not f.get("pass", True)}
        cf = {f.get("id") for f in failed}
        pm = (prev.get("metrics") or {}).get("mass_total_g")
        out["delta"] = {"fixed": sorted(pf - cf), "new": sorted(cf - pf), "still": sorted(pf & cf),
                        "mass_g": None if pm is None or "mass_total_g" not in m else round(m["mass_total_g"] - pm, 3)}
    out = _trim(out, budget_chars)
    return out


def _trim(out, budget_chars):
    """Drop warnings, then not_checked entries, until inside the budget (blockers never drop)."""
    while len(json.dumps(out)) > budget_chars:
        if out["warnings"]:
            out["warnings"].pop()
        elif out["not_checked"]:
            out["not_checked"].pop()
        else:
            break
    return out


def add_cli(sub):
    p = sub.add_parser("llm-report", help="compact report.json for an LLM context window")
    p.add_argument("report")
    p.add_argument("--prev", help="the previous report.json (adds a delta section)")
    p.add_argument("--budget", type=int, default=6000, help="character budget")
    p.add_argument("-o", "--out", help="write JSON here (default: stdout)")
    p.set_defaults(func=_run)


def _run(a):
    import sys
    from pathlib import Path

    try:
        rep = json.loads(Path(a.report).read_text())
        prev = json.loads(Path(a.prev).read_text()) if a.prev else None
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    c = compact(rep, prev, a.budget)
    text = json.dumps(c, indent=2)
    if a.out:
        Path(a.out).write_text(text)
    else:
        print(text)
    return 0
