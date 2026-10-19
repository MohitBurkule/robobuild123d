"""Command line: `python3 -m robot guide|catalog|materials|templates|template|verify ...` (render/export added by their modules)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from . import catalog, checks, spec as spec_mod
from .finding import BLOCKER

HERE = Path(__file__).parent


def print_report(rep, full=False):
    s = rep.summary
    print(f"{rep.name}: {s['blockers']} blockers, {s['warnings']} warnings, {s['passed']} checks passed. ok={rep.ok}")
    print(f"check set revision {rep.checks_revision} (engine {rep.engine})")
    m = rep.metrics
    if "mass_total_g" in m:
        print(f"mass {m['mass_total_g']:.1f} g (range {m['mass_lo_g']:.1f} to {m['mass_hi_g']:.1f} g, limit {m.get('mass_limit_g', 150):.0f})")
    if "footprint_mm" in m:
        print(f"footprint {m['footprint_mm']:.1f} mm square")
    n = 0
    for f in rep.findings:
        if f.passed and not full:
            continue
        n += 1
        tag = "pass" if f.passed else ("BLOCKER" if f.severity == BLOCKER else "warning")
        at = f" at ({f.at[0]:.1f}, {f.at[1]:.1f}, {f.at[2]:.1f})" if f.at else ""
        parts = f" parts: {', '.join(f.parts)}" if f.parts else ""
        print(f"[{tag}] {f.id} - {f.message}{parts}{at}")
        if not f.passed and f.fix_hint:
            print(f"    fix: {f.fix_hint}")
    if n == 0:
        print("nothing to fix.")
    if rep.not_checked:
        print("NOT CHECKED (a pass says nothing about these):")
        for x in rep.not_checked:
            print(f"  - {x}")


def opts_from(a):
    return checks.Options(deep=not getattr(a, "quick", False), fast=getattr(a, "fast", False))


def main(argv=None):
    ap = argparse.ArgumentParser(prog="robot", description="Antweight robot builder and verifier (build123d)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("guide")
    c = sub.add_parser("catalog")
    c.add_argument("id", nargs="?")
    sub.add_parser("materials")
    sub.add_parser("templates")
    t = sub.add_parser("template")
    t.add_argument("name")
    v = sub.add_parser("verify")
    v.add_argument("spec")
    v.add_argument("--full", action="store_true")
    v.add_argument("--fast", action="store_true", help="coarse tessellation for quick iteration")
    v.add_argument("--quick", action="store_true", help="skip the slow sweeps (wiring, assembly)")
    v.add_argument("--json", help="also write report.json here")
    for name in ("render", "export", "gen.cli", "cad.cli"):
        try:
            mod = __import__(f"robot.{name}", fromlist=["add_cli"])
            mod.add_cli(sub)
        except ImportError:
            pass
    for name, sp in sub.choices.items():
        if name in ("verify", "render", "export"):
            sp.add_argument("--no-cache", action="store_true", help="ignore and do not use the run cache")
            sp.add_argument("--cache-stats", action="store_true", help="print cache hits and misses at the end")
            sp.add_argument("--jobs", type=int, default=0, help="processes for part builds (default: cpu count)")
    a = ap.parse_args(argv)
    if a.cmd in ("verify", "render", "export"):
        from . import cache, world as world_mod

        os.environ["ROBOT_PROGRESS"] = "1"
        if a.no_cache:
            cache.set_enabled(False)
        if a.jobs:
            world_mod.JOBS = a.jobs
        import atexit

        def _stats():
            print(cache.stats_line(), flush=True)
            if a.cache_stats:
                print(json.dumps(cache.stats(), indent=2), flush=True)

        atexit.register(_stats)
    if a.cmd in (None, "guide"):
        g = HERE / "GUIDE.md"
        print(g.read_text() if g.exists() else ap.format_help())
    elif a.cmd == "catalog":
        for e in catalog.catalog():
            if a.id and e.id != a.id:
                continue
            print(f"{e.id} | {e.kind} | {e.name} | {e.mass_g:.1f} g ({e.confidence}) | ports: {', '.join(e.ports)}"
                  + (f" | props: {e.props} | shape: {json.dumps(e.shape)} | source: {e.source}" if a.id else ""))
    elif a.cmd == "materials":
        for mid in catalog.MATERIAL_LIST:
            m = catalog.material(mid)
            print(f"{mid}: {m.density:.2f} g/cm3, {m.cls}, min wall {m.min_wall_mm:.1f} mm{', brittle' if m.brittle else ''}")
    elif a.cmd == "templates":
        for p in sorted((HERE / "templates").glob("*.json")):
            print(p.stem)
    elif a.cmd == "template":
        p = HERE / "templates" / f"{a.name}.json"
        if not p.exists():
            print(f"unknown template {a.name}; try `robot templates`", file=sys.stderr)
            return 1
        print(p.read_text())
    elif a.cmd == "verify" and getattr(a, "changed", False):
        from .cad import incremental  # incremental verify (robot/cad/incremental.py)

        return incremental.cli(a)
    elif a.cmd == "verify":
        try:
            s = spec_mod.load(a.spec)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        rep = checks.verify(s, opts_from(a))
        print_report(rep, a.full)
        if a.json:
            Path(a.json).write_text(json.dumps(rep.to_dict(), indent=2))
        return 0 if rep.ok else 2
    elif hasattr(a, "func"):
        return a.func(a)
    return 0
