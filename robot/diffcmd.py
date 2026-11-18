"""Diff two verify reports (E2): `robot diff report_a.json report_b.json`.

Answers "what did my change do": mass delta, findings newly failing / newly
passing / still failing, metric deltas. Exit code 3 when the change regressed
(a new blocker, or a passed check that now fails), 0 otherwise - so a CI job or
an LLM loop can gate on it.
"""

from __future__ import annotations


def _findings(d):
    out = {}
    for f in d.get("findings", []):
        if not f.get("pass", True):
            out[f["id"]] = f
    return out


def diff_reports(a: dict, b: dict) -> dict:
    """Machine-readable diff of two report dicts (as written by report.json)."""
    fa, fb = _findings(a), _findings(b)
    fixed = sorted(set(fa) - set(fb))
    new = sorted(set(fb) - set(fa))
    still = sorted(set(fa) & set(fb))
    ma = (a.get("metrics") or {}).get("mass_total_g")
    mb = (b.get("metrics") or {}).get("mass_total_g")
    metrics = {}
    for k in sorted(set(a.get("metrics") or {}) | set(b.get("metrics") or {})):
        va, vb = (a.get("metrics") or {}).get(k), (b.get("metrics") or {}).get(k)
        if isinstance(va, (int, float)) and isinstance(vb, (int, float)) and va != vb:
            metrics[k] = {"a": va, "b": vb, "delta": round(vb - va, 4)}
    mass_delta = None if ma is None or mb is None else round(mb - ma, 3)
    return {"fixed": fixed, "new": new, "still": still,
            "mass_total_g": {"a": ma, "b": mb, "delta": mass_delta},
            "ok_a": a.get("ok"), "ok_b": b.get("ok"),
            "regressed": bool(new) or (a.get("ok") and not b.get("ok")),
            "metrics": metrics}


def summarize(d: dict) -> list:
    """Human lines for a diff_reports result."""
    out = []
    md = d.get("mass_total_g") or {}
    if md.get("delta") is not None:
        out.append(f"mass: {md['a']:.1f} g -> {md['b']:.1f} g ({md['delta']:+.1f} g)")
    if d["fixed"]:
        out.append(f"fixed ({len(d['fixed'])}): " + ", ".join(d["fixed"]))
    if d["new"]:
        out.append(f"NEW failures ({len(d['new'])}): " + ", ".join(d["new"]))
    if d["still"]:
        out.append(f"still failing ({len(d['still'])}): " + ", ".join(d["still"]))
    if not d["fixed"] and not d["new"] and not d["still"]:
        out.append("no failed findings on either side")
    if d["regressed"]:
        out.append("REGRESSION")
    elif d["ok_b"]:
        out.append("no regressions")
    return out


def add_cli(sub):
    p = sub.add_parser("diff", help="diff two report.json files (exit 3 on regressions)")
    p.add_argument("a")
    p.add_argument("b")
    p.add_argument("--json", action="store_true", help="print the machine-readable diff")
    p.set_defaults(func=_run)


def _run(a):
    import json
    import sys
    from pathlib import Path

    try:
        ra = json.loads(Path(a.a).read_text())
        rb = json.loads(Path(a.b).read_text())
    except (OSError, ValueError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    d = diff_reports(ra, rb)
    if a.json:
        print(json.dumps(d, indent=2))
    else:
        print("\n".join(summarize(d)))
    return 3 if d["regressed"] else 0
