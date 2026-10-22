"""Markdown report of a robustness sweep: which params, variants and swaps break what."""

from __future__ import annotations

from collections import Counter

from . import describe


def markdown(name: str, sha: str, out: dict, jobs, skipped, cfg: dict) -> str:
    res = out["results"]
    broken = [(jid, j, r, d) for jid, (j, r, d) in res.items() if d["broken"]]
    held = [(jid, j, r, d) for jid, (j, r, d) in res.items() if not d["broken"] and not d["timeout"]]
    tout = [jid for jid, (j, r, d) in res.items() if d["timeout"]]
    disc = out.get("discovery")
    L = [f"# Robustness sweep: {name} @ {sha}", "",
         f"Group `robust` (robot/checks/robust). One-at-a-time perturbations, each rebuilt on the per-part cache "
         f"(only parts whose build reads the edit, or whose spec entry changed) and checked with the fast groups "
         f"(integrity, interference, connections, assembly, fastener_seat). A perturbation **breaks** when the build "
         f"fails or it adds a blocker that the baseline does not have. Severity: WARNING (BLOCKER with "
         f"`review.robust.blocker: true`).", "",
         f"- run time: {out['seconds']:.0f} s (budget {cfg['budget_s']:.0f} s, {cfg['workers']} workers); "
         f"baseline {out['baseline'].get('seconds', '?')} s with {len(out['baseline'].get('blockers', []))} blockers",
         f"- discovered: {len(disc.params) if disc else '?'} numeric params "
         f"({sum(p.master for p in disc.params) if disc else '?'} masters), {len(disc.relations) if disc else '?'} relations, "
         f"{len(disc.switches) if disc else '?'} variant / catalog switches",
         f"- planned {len(jobs)} perturbations (top {cfg['top_n']} params by parts reading them, +-10 % first, +-5 % where "
         f"+-10 % broke); ran {len(res)}; **{len(broken)} break**; {len(held)} hold; {len(tout)} timed out; "
         f"{len(out['not_run'])} not run", ""]
    by_target = Counter(j.target for _, j, _, _ in broken)
    if broken:
        L += ["## Top breaking params / switches", "", "| param or switch | breaking edits | checks hit |", "|---|---|---|"]
        for t, n in by_target.most_common():
            checks = Counter(b[0] for _, j, _, d in broken if j.target == t for b in d["new"])
            errs = sum(1 for _, j, _, d in broken if j.target == t and d["build_error"])
            cs = ", ".join(f"{c} x{k}" for c, k in checks.most_common(6)) + (f"; build fails x{errs}" if errs else "")
            L.append(f"| `{t}` | {n} | {cs} |")
        L += ["", "## Breaking perturbations", ""]
        for jid, j, r, d in broken:
            L.append(f"- **{jid}** ({j.kind}; rebuilt {len(r.get('rebuilt') or [])} parts, {r.get('seconds', '?')} s): {describe(j, d)}")
            for b in d["new"][:6]:
                L.append(f"  - `{b[0]}` on {b[1] or '-'}: {b[2][:160]}")
            if len(d["new"]) > 6:
                L.append(f"  - ... {len(d['new']) - 6} more")
        L.append("")
    L += ["## Holding perturbations", "", ", ".join(f"`{jid}`" for jid, *_ in held) or "none", ""]
    if tout or out["not_run"]:
        L += ["## Not finished / not run", ""] + [f"- `{x}` timed out" for x in tout] + [f"- `{x}`" for x in out["not_run"]] + [""]
    if skipped:
        L += ["## Params outside the sample", "", "Ranked below the top N by parts reading them: " +
              ", ".join(f"`{p}` ({n})" for p, n in skipped[:40]) + (f", ... {len(skipped) - 40} more" if len(skipped) > 40 else ""), ""]
    L += ["## Baseline blockers (excluded from the diff)", ""] + [f"- `{b[0]}` on {b[1] or '-'}" for b in out["baseline"].get("blockers", [])] + [""]
    return "\n".join(L)
