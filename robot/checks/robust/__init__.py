"""robust.*: a parametric model survives one-at-a-time changes to its params, variants and COTS swaps.

Discovers the robot's params modules (discover.py), ranks params by how many parts read them (usage.py), plans
+-5 / +-10 % edits, variant flips and catalog swaps (plan.py), runs each in its own process that rebuilds only the
affected parts on the per-part geometry cache and runs the fast groups (worker.py: integrity, interference,
connections, assembly, fastener_seat), and reports every edit that fails the build or adds a blocker vs the baseline
(runner.py). Results are cached per edit (key: edit + build sources + checks code + spec).

  robust.param_breaks  WARNING per breaking edit (BLOCKER with `review.robust.blocker: true` or ROBOT_ROBUST_BLOCKER=1)
  robust.sweep         pass/summary; edits not run inside the budget are listed under NOT CHECKED

Spec `review.robust`: enabled (true), budget_s (900), top_n (8), workers (3), steps ("adaptive" | "all"),
bounds {NAME: [lo, hi]}, blocker (false). Env: ROBOT_ROBUST=0 skips, ROBOT_ROBUST_BUDGET / _TOP override.
"""

from __future__ import annotations

import os
from pathlib import Path

from ...finding import BLOCKER, WARNING, fail, ok

G = "robust"
DEFAULTS = {"enabled": True, "budget_s": 900.0, "top_n": 8, "workers": 3, "steps": "adaptive", "bounds": {}, "blocker": False}


def config(raw: dict) -> dict:
    c = dict(DEFAULTS)
    c.update(((raw or {}).get("review") or {}).get("robust") or {})
    if os.environ.get("ROBOT_ROBUST_BUDGET"):
        c["budget_s"] = float(os.environ["ROBOT_ROBUST_BUDGET"])
    if os.environ.get("ROBOT_ROBUST_TOP"):
        c["top_n"] = int(os.environ["ROBOT_ROBUST_TOP"])
    if os.environ.get("ROBOT_ROBUST_BLOCKER") == "1":
        c["blocker"] = True
    return c


def model_file(raw: dict) -> str | None:
    """Relative path of the first model file the spec builds from."""
    from .usage import model_keys  # noqa: F401 - same walk

    def walk(s):
        if isinstance(s, dict):
            if s.get("type") == "model" and s.get("file"):
                return s["file"]
            for v in s.values():
                r = walk(v)
                if r:
                    return r
        elif isinstance(s, list):
            for v in s:
                r = walk(v)
                if r:
                    return r
        return None

    for p in raw.get("parts", []):
        if p.get("model"):
            return p["model"]
        r = walk(p.get("shape"))
        if r:
            return r
    return None


def describe(job, d) -> str:
    what = f"`{job.target}` {job.base!r} -> {job.value!r}" if job.kind == "param" else f"`{job.id}`"
    if d["build_error"]:
        return f"{what}: build fails ({d['build_error']})"
    checks = sorted({b[0] for b in d["new"]})
    parts = sorted({p for b in d["new"] for p in b[1].split(",") if p})
    return f"{what}: adds {len(d['new'])} blocker(s) [{', '.join(checks)}] on {', '.join(parts[:8]) or '-'}"


def findings(out: dict, severity) -> list:
    res = []
    for jid, (job, r, d) in out["results"].items():
        if not d["broken"]:
            continue
        f = fail("robust.param_breaks", G, severity, f"Perturbing `{job.target}` breaks the model", describe(job, d))
        f.on(*sorted({p for b in d["new"] for p in b[1].split(",") if p}))
        f.expected, f.actual = "no new blocker", jid
        res.append(f.fix("Derive the feature from the param (a relation) instead of a fixed number, or declare "
                         "`# bounds: lo..hi` on the param if the range is intentionally narrow."))
    return res


def sweep(spec_path: Path, raw: dict, cfg: dict, log=print, execute=None) -> tuple:
    """(plan, skipped params, runner output) for one spec; None plan when the robot has no model build sources."""
    from ... import cache
    from . import discover as D, plan as P, runner as R, usage as U

    mrel = model_file(raw)
    if not mrel:
        return None, [], None
    mf = Path(spec_path).resolve().parent / mrel
    disc = D.discover(mf, cfg.get("bounds"))
    files = D.package_files(mf)
    use = U.Usage(U.build_graph(files), raw)
    jobs, skipped = P.make_plan(disc, use, int(cfg["top_n"]), cfg["steps"])
    src = cache.h([f.read_bytes() for f in files])
    kw = {"execute": execute} if execute else {}
    out = R.run(jobs, spec_path, mrel, float(cfg["budget_s"]), int(cfg["workers"]), src_hash=src, log=log, **kw)
    out["discovery"] = disc
    return jobs, skipped, out


def run(ctx):
    sp = ctx.r.spec
    raw = sp.raw or {}
    cfg = config(raw)
    if os.environ.get("ROBOT_ROBUST_CHILD") or os.environ.get("ROBOT_ROBUST") == "0" or not cfg["enabled"]:
        return []
    spec_path = Path(sp.base_dir) / "spec.json"
    if not model_file(raw) or not spec_path.exists():
        return [ok("robust.sweep", G, "No parametric build sources", "The spec builds no part from a model file; nothing to perturb.")]
    jobs, skipped, out = sweep(spec_path, raw, cfg)
    sev = BLOCKER if cfg["blocker"] else WARNING
    if out["baseline"].get("error"):
        ctx.not_checked.append(f"robust: baseline failed: {out['baseline']['error']}")
        return [fail("robust.sweep", G, WARNING, "Robustness sweep had no baseline", out["baseline"]["error"])]
    found = findings(out, sev)
    for jid in out["not_run"]:
        ctx.not_checked.append(f"robust: `{jid}` not run within the {cfg['budget_s']:.0f} s budget")
    for p, n in skipped:
        ctx.not_checked.append(f"robust: param `{p}` (read by {n} parts) outside the top {cfg['top_n']}")
    ctx.metrics["robust.perturbations_run"] = len(out["results"])
    ctx.metrics["robust.breaking"] = len(found)
    ctx.metrics["robust.seconds"] = out["seconds"]
    msg = f"{len(out['results'])} perturbations in {out['seconds']:.0f} s; {len(found)} break the model"
    return found + [ok("robust.sweep", G, "Robustness sweep ran", msg)]
