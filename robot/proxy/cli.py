"""`robot verify SPEC --proxy`: run the fast proxies and print a report like a full verify."""

from __future__ import annotations

import json
import time
from pathlib import Path

from . import GROUPS, load_baseline, run


def _split(s):
    return [x.strip() for x in s.split(",") if x.strip()] if s else None


def verify(a, print_report):
    from .. import spec as spec_mod, world as world_mod
    from ..checks import Ctx, Options
    from ..finding import Report

    groups = _split(a.only) or list(GROUPS)
    bad = [g for g in groups if g not in GROUPS]
    if bad:
        print(f"error: no proxy for {', '.join(bad)}; proxies: {', '.join(GROUPS)}")
        return 1
    t0 = time.time()
    s = spec_mod.load(a.spec)
    r = world_mod.resolve(s, fast=a.fast)
    ctx = Ctx(r, world_mod.World.start(r), Options(fast=a.fast))
    rep = Report(name=s.name, profile=r.profile.name)
    rep.timings_s["build"] = round(time.time() - t0, 3)
    rep.findings, t = run(ctx, groups, _split(a.parts), load_baseline(s.name, a.baseline))
    rep.timings_s.update(t)
    rep.metrics = ctx.metrics
    rep.not_checked = ["Proxy run: a pass is a strong hint, not a verdict; run the full groups before merging"] + ctx.not_checked
    rep.finish()
    print_report(rep, a.full)
    print("proxy timings: " + ", ".join(f"{k} {v:.1f} s" for k, v in rep.timings_s.items()))
    if a.json:
        Path(a.json).write_text(json.dumps(rep.to_dict(), indent=2))
    return 0 if rep.ok else 2
