"""Change hypotheses through the robust runner: swap / dimension / architecture changes (robot/gen/changes.py), each
expressed as settings (overlay ops, declared hooks, params literals), built and verified one at a time, and scored by
how many hold with zero code change.

  python3 -m robot.checks.robust.hyp robots/revron/spec.json --out hypotheses_report.md [--budget S --workers W --top N]

A change is
  holds            expressible through settings, builds, and adds no blocker vs the baseline (zero code change)
  breaks           expressible, but the build fails or new blockers appear: the report names the builder files
  not expressible  no settings hook can say it: the report names the missing hook and estimates the code diff
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

from .worker import FAST_GROUPS

HYP_GROUPS = FAST_GROUPS + ["electrical", "retention"]


def resolve(changes, raw, hooks, disc, use):
    """(jobs, not_expressible) - each change becomes a plan.Job (overlay + optional build-setting edit) or a record."""
    from ... import overlay as O
    from . import plan as P

    jobs, nx = [], []
    for c in changes:
        if c.job is not None:
            jobs.append((c, c.job))
            continue
        try:
            prim = []
            for op in c.ops:
                prim += O.expand(op, hooks)
            sets = [o for o in prim if o.get("op") == "build_setting"]
            ops = [o for o in prim if o.get("op") != "build_setting"]
            O.apply(raw, ops, hooks)  # statically valid against the current spec
        except O.MissingHook as e:
            nx.append((c, str(e), e.name))
            continue
        except (ValueError, KeyError) as e:
            nx.append((c, f"overlay cannot apply: {e}", c.hook or "spec overlay"))
            continue
        job = P.Job(c.id, c.hook or c.id.split(":")[1], "hyp", overlay=ops)
        if len(sets) > 1:
            nx.append((c, "more than one build setting in one change", c.hook))
            continue
        if sets:
            s = sets[0]
            key = s.get("env") or s.get("variant")
            sw = next((x for x in disc.switches if x.name == key), None)
            alt = s["value"] if not s.get("variant") else bool(s["value"])
            sj = [j for j in P.switch_jobs(sw, use.parts_reading(sw.symbol, sw.kind == "variant"))
                  if j.value == alt] if sw else []
            if not sj:
                nx.append((c, f"hook `{c.hook}` names build setting `{key}` that the build sources do not read", c.hook))
                continue
            job = sj[0]
            job.id, job.overlay = c.id, ops
        jobs.append((c, job))
    return jobs, nx


def evaluate(spec_path: Path, budget_s=3600.0, workers=3, top_n=8, log=print, execute=None):
    from ... import cache, overlay as O
    from ...gen import changes as C
    from . import discover as D, model_file, plan as P, runner as R, usage as U

    raw = json.loads(Path(spec_path).read_text())
    mrel = model_file(raw)
    mf = Path(spec_path).resolve().parent / mrel
    disc = D.discover(mf, None)
    files = D.package_files(mf)
    graph = U.build_graph(files)
    use = U.Usage(graph, raw)
    hooks = O.load_hooks(raw, Path(spec_path).resolve().parent)
    changes = C.change_hypotheses(raw, hooks)
    pj, _ = P.make_plan(D.Discovery(params=disc.params), use, top_n, "adaptive")
    for j in pj:
        if j.phase == 0:
            changes.append(C.Change(f"dim:{j.id}", "dimension", f"{j.target} {j.base:g} -> {j.value:g} ({j.step:+.0%})", job=j))
    jobs, nx = resolve(changes, raw, hooks, disc, use)
    for j in (j for _, j in jobs):
        j.phase = 0
    order = {"swap": 0, "architecture": 1, "dimension": 2}  # cheap overlay-only jobs first, rebuild-heavy params last
    jobs.sort(key=lambda cj: (order[cj[0].family], cj[1].kind != "hyp"))
    src = "" if execute else cache.h([f.read_bytes() for f in files])  # an injected executor (tests) is never cached
    kw = {"execute": execute} if execute else {}
    out = R.run([j for _, j in jobs], spec_path, mrel, budget_s, workers, src_hash=src, log=log, groups=HYP_GROUPS, **kw)
    return dict(raw=raw, changes=changes, jobs=jobs, nx=nx, out=out, files=files, graph=graph, hooks=hooks, disc=disc)


def verdicts(ev) -> list:
    """One row per change: dict(change, verdict, builds, blockers, diff, hook, why)."""
    from ... import overlay as O
    from ...gen import changes as C

    res = ev["out"]["results"]
    owners = ev["hooks"].get("owners") or {}
    rows = []
    for c, j in ev["jobs"]:
        r = res.get(j.id)
        if r is None:
            rows.append(dict(change=c, verdict="not run", builds=None, blockers=[], diff=None, hook=c.hook, why="outside the time budget"))
            continue
        _, rr, d = r
        if d["timeout"]:
            rows.append(dict(change=c, verdict="timeout", builds=None, blockers=[], diff=None, hook=c.hook, why=rr.get("error") or ""))
            continue
        settings = len(j.overlay) + (0 if j.kind == "hyp" else 1)
        if not d["broken"]:
            rows.append(dict(change=c, verdict="holds", builds=True, blockers=[], diff={"files": {}, "lines": 0, "by_owner": {}, "settings": settings},
                             hook=c.hook, why=""))
            continue
        parts = sorted({p for b in d["new"] for p in b[1].split(",") if p})
        if d["build_error"] and not parts:
            parts = list(j.reads or []) or [p["id"] for p in O.select(ev["raw"], dict(c.touches or {"id": []}))]
        diff = C.estimate_diff(ev["files"], ev["graph"], ev["raw"], {"id": parts}, None, owners)
        diff["settings"] = settings
        rows.append(dict(change=c, verdict="breaks", builds=not d["build_error"], blockers=d["new"], diff=diff, hook=c.hook,
                         why=d["build_error"] or ""))
    for c, why, hook in ev["nx"]:
        diff = C.estimate_diff(ev["files"], ev["graph"], ev["raw"], c.touches or {"id": []}, c.keywords, owners)
        rows.append(dict(change=c, verdict="not expressible", builds=None, blockers=[], diff=diff, hook=hook, why=why))
    fam = {"swap": 0, "dimension": 1, "architecture": 2}
    rows.sort(key=lambda r: (fam[r["change"].family], r["change"].id))
    return rows


def score(rows) -> dict:
    n = len(rows)
    held = sum(r["verdict"] == "holds" for r in rows)
    decided = [r for r in rows if r["verdict"] in ("holds", "breaks", "not expressible")]
    by = {}
    for f in ("swap", "dimension", "architecture"):
        rs = [r for r in decided if r["change"].family == f]
        by[f] = (sum(r["verdict"] == "holds" for r in rs), len(rs))
    return dict(total=n, decided=len(decided), held=held, pct=100.0 * held / len(decided) if decided else 0.0,
                pct_all=100.0 * held / n if n else 0.0, by_family=by, counts=Counter(r["verdict"] for r in rows))


def missing_hooks(rows) -> dict:
    """{owner: [(hook or fix, count, example ids)]}: what each owner would add so more changes hold."""
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        if r["verdict"] not in ("not expressible", "breaks") or not r["diff"]:
            continue
        owners = list(r["diff"]["by_owner"]) or ["spec/framework"]
        if r["verdict"] == "not expressible":
            key = f"hook `{r['hook']}`"
        else:
            checks = sorted({b[0] for b in r["blockers"]}) or ["build fails"]
            key = f"{r['change'].family} fit: {', '.join(checks[:3])}"
        for o in owners:
            acc[o][key].append(r["change"].id)
    return {o: sorted(((k, len(v), v) for k, v in d.items()), key=lambda x: -x[1]) for o, d in acc.items()}


def _diff_text(d) -> str:
    if not d:
        return "-"
    if not d["files"]:
        return f"0 code lines ({d.get('settings', 0)} setting(s))"
    fs = ", ".join(f"{k}" + (f" ~{v}" if v else "") for k, v in sorted(d["files"].items(), key=lambda x: -x[1])[:5])
    more = f" +{len(d['files']) - 5} more" if len(d["files"]) > 5 else ""
    return f"{len(d['files'])} file(s): {fs}{more}"


def markdown(ev, rows, sha="?", cfg=None) -> str:
    s = score(rows)
    out = ev["out"]
    cfg = cfg or {}
    L = [f"# Change hypotheses: {ev['raw'].get('name', 'robot')} @ {sha}", "",
         "Generator `robot/gen/changes.py` (swap / dimension / architecture), settings layer `robot/overlay.py` + "
         "the robot's `hooks.json`, run through the robust runner (`robot/checks/robust/hyp.py`): each change rebuilt "
         f"on the per-part cache and checked with {', '.join(HYP_GROUPS)}. A change **holds** when it is expressible "
         "through settings, builds, and adds no blocker the baseline lacks.", "",
         f"## Versatility score: **{s['pct']:.0f} %** of decided hypotheses hold with zero code change "
         f"({s['held']} / {s['decided']}; {s['pct_all']:.0f} % of all {s['total']} generated)", "",
         "| family | hold / decided |", "|---|---|"]
    for f, (h, n) in s["by_family"].items():
        L.append(f"| {f} | {h} / {n} |")
    L += ["", "Verdicts: " + ", ".join(f"{k} {v}" for k, v in s["counts"].most_common()),
          f"Run: {out['seconds']:.0f} s (budget {cfg.get('budget_s', '?')} s, {cfg.get('workers', '?')} workers); baseline "
          f"{out['baseline'].get('seconds', '?')} s with {len(out['baseline'].get('blockers', []))} blockers (excluded from the diff)."
          + (f" Baseline error: {out['baseline']['error']}" if out["baseline"].get("error") else ""), ""]
    mh = missing_hooks(rows)
    if mh:
        L += ["## Top missing hooks / fixes per owner", ""]
        for o in sorted(mh):
            L.append(f"**{o}**")
            for k, n, ids in mh[o][:6]:
                L.append(f"- {k}: {n} hypothesis(es), e.g. `{ids[0]}`")
            L.append("")
    for fam in ("swap", "dimension", "architecture"):
        rs = [r for r in rows if r["change"].family == fam]
        if not rs:
            continue
        L += [f"## {fam.capitalize()} hypotheses", "", "| hypothesis | verdict | builds | new blockers | diff needed |", "|---|---|---|---|---|"]
        for r in rs:
            c = r["change"]
            b = Counter(x[0] for x in r["blockers"])
            bl = ", ".join(f"{k} x{v}" for k, v in b.most_common(3)) or ("-" if r["verdict"] != "breaks" else r["why"][:80])
            if r["verdict"] == "not expressible":
                bl = r["why"][:120]
            bu = {True: "yes", False: "no", None: "-"}[r["builds"]]
            L.append(f"| {c.title}{' (' + c.note + ')' if c.note else ''} | {r['verdict']} | {bu} | {bl} | {_diff_text(r['diff'])} |")
        L.append("")
    det = [r for r in rows if r["verdict"] == "breaks"]
    if det:
        L += ["## Breaking hypotheses: blockers", ""]
        for r in det:
            L.append(f"- **{r['change'].id}**" + (f": {r['why'][:200]}" if r["why"] else ""))
            for x in r["blockers"][:4]:
                L.append(f"  - `{x[0]}` on {x[1] or '-'}: {x[2][:150]}")
            if len(r["blockers"]) > 4:
                L.append(f"  - ... {len(r['blockers']) - 4} more")
        L.append("")
    L += ["## How to add a hypothesis", "",
          "- a part swap: add the entry to `robot/catalog_data/components.json` (or the built-in catalog); it is picked up by role.",
          "- a layout change: append to `ARCH` in `robot/gen/changes.py` (hook name, values, keywords).",
          "- make one expressible: declare the hook in the robot's `hooks.json` (overlay ops per value, or an env "
          "setting the build reads), or a named location under `anchors`.", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="robot.checks.robust.hyp")
    ap.add_argument("spec")
    ap.add_argument("--out")
    ap.add_argument("--budget", type=float, default=3600.0)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--top", type=int, default=8)
    a = ap.parse_args(argv)
    ev = evaluate(Path(a.spec), a.budget, a.workers, a.top)
    rows = verdicts(ev)
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "?"
    except OSError:
        sha = "?"
    md = markdown(ev, rows, sha, {"budget_s": a.budget, "workers": a.workers})
    if a.out:
        Path(a.out).write_text(md)
        print("wrote", a.out)
    else:
        print(md)
    s = score(rows)
    print(f"versatility {s['pct']:.0f}% ({s['held']}/{s['decided']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
