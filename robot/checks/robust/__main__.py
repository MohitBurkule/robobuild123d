"""python -m robot.checks.robust <spec.json> [--out report.md] [--budget S] [--top N] [--workers W] [--all-steps] [--blocker]"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from . import config, findings, sweep
from .report import markdown


def main(argv=None):
    ap = argparse.ArgumentParser(prog="robot.checks.robust")
    ap.add_argument("spec")
    ap.add_argument("--out")
    ap.add_argument("--budget", type=float)
    ap.add_argument("--top", type=int)
    ap.add_argument("--workers", type=int)
    ap.add_argument("--all-steps", action="store_true")
    ap.add_argument("--blocker", action="store_true", help="breaking perturbations are BLOCKERs, not WARNINGs")
    a = ap.parse_args(argv)
    raw = json.loads(Path(a.spec).read_text())
    cfg = config(raw)
    for k, v in (("budget_s", a.budget), ("top_n", a.top), ("workers", a.workers)):
        if v is not None:
            cfg[k] = v
    if a.all_steps:
        cfg["steps"] = "all"
    if a.blocker:
        cfg["blocker"] = True
    jobs, skipped, out = sweep(Path(a.spec), raw, cfg)
    if jobs is None:
        print("no model build sources: nothing to perturb")
        return 0
    sev = "blocker" if cfg["blocker"] else "warning"
    for f in findings(out, sev):
        print(f"[{sev.upper()}] {f.id} - {f.message}")
    try:
        sha = subprocess.run(["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip() or "?"
    except OSError:
        sha = "?"
    md = markdown(raw.get("name", "robot"), sha, out, jobs, skipped, cfg)
    if a.out:
        Path(a.out).write_text(md)
        print("wrote", a.out)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
