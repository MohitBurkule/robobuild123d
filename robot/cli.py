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
    combined = getattr(rep, "gate", "combined") == "combined"
    par = getattr(rep, "parity", None) or {}
    print(f"gate: {'combined (design + parity blockers decide ok)' if combined else 'design (parity never decides ok)'}"
          f"{f', tier {rep.tier}' if getattr(rep, 'tier', None) else ''}")
    if par.get("total"):
        print(f"parity vs reference: {par['passed']}/{par['total']} checks passed (score {par['score']:.2f}), "
              f"{par['blockers']} parity blockers, {par['warnings']} warnings, {par['groups_clean']}/{par['groups_total']} "
              f"parity groups clean{'' if combined else ' [not gating]'}")
    else:
        print("parity vs reference: not run" if not par.get("run") else "parity vs reference: nothing to compare")
    m = rep.metrics
    if "mass_total_g" in m:
        print(f"mass {m['mass_total_g']:.1f} g (range {m['mass_lo_g']:.1f} to {m['mass_hi_g']:.1f} g, limit {m.get('mass_limit_g', 150):.0f})")
    if "footprint_mm" in m:
        print(f"footprint {m['footprint_mm']:.1f} mm square")
    roots = getattr(rep, "roots", None) or []
    if roots:
        from .rootcause import text as roots_text
        print(roots_text(roots, context=True))
        from .autohelp import text as help_text
        h = help_text(rep)
        if h:
            print(h)
        print("ALL FINDINGS:")
    n = 0
    for f in rep.findings:
        if f.passed and not full:
            continue
        n += 1
        tag = "pass" if f.passed else ("BLOCKER" if f.severity == BLOCKER else "warning")
        if not combined and getattr(f, "kind", "design") == "parity":
            tag = f"parity {tag.lower()}"  # never "[BLOCKER]": log scrapers count those as gate blockers
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
    groups = getattr(rep, "groups", None) or {}
    if groups:
        print(f"groups run ({len(groups)}, {sum(g['time_s'] or 0 for g in groups.values()):.1f} s of checks):")
        for name, g in groups.items():
            print(f"  {name:<17}{g['kind']:<7} {g['tier'] or '-':<8}{g['time_s'] or 0:>8.1f} s  {g['how']:<7} "
                  f"{g['blockers']} blockers, {g['warnings']} warnings")
    skipped = getattr(rep, "not_run", None) or []
    if skipped and getattr(rep, "tier", None) or any("parity" in x["reason"] for x in skipped):
        print(f"NOT RUN in this tier ({len(skipped)} groups; a pass says nothing about them):")
        for x in skipped:
            print(f"  - {x['group']} ({x['kind']}, {x['tier']}): {x['reason']}")
    elif skipped:
        print(f"NOT RUN: {len(skipped)} other groups (--only)")


LLM_ROOTS, LLM_CONTEXT = 12, 5


def print_llm(rep):
    """Root causes only: what is wrong, the measured numbers, the edit. A model reads this instead of 100+ findings."""
    s = rep.summary
    m = rep.metrics
    head = f"{rep.name}: ok={rep.ok} {s['blockers']} blockers in {len(rep.roots)} root causes"
    if "mass_total_g" in m:
        head += f", mass {m['mass_total_g']:.1f}/{m.get('mass_limit_g', 150):.0f} g"
    print(head)
    for k, c in enumerate(rep.roots[:LLM_ROOTS], 1):
        n = len(c["findings"]) - 1
        print(f"{k}. [{c['primary']}] {c['message']}" + (f" (+{n} consequences)" if n else ""))
        if c.get("fix"):
            print(f"   fix: {c['fix']}")
        for x in (c.get("context") or [])[:LLM_CONTEXT]:
            print(f"   | {x}")
    if len(rep.roots) > LLM_ROOTS:
        print(f"... {len(rep.roots) - LLM_ROOTS} more root causes (fix these first, then re-run)")
    from .autohelp import text as help_text
    h = help_text(rep)
    if h:
        print(h)


def opts_from(a):
    o = checks.Options(deep=not getattr(a, "quick", False), fast=getattr(a, "fast", False))
    only = getattr(a, "only", None)
    if only:
        o.only = [g.strip() for g in only.split(",") if g.strip()]
    # gate and tier (checks/registry.py). Default: the full design tier, parity reported apart. --combined is the
    # old run: every group, every blocker decides ok.
    o.combined = bool(getattr(a, "combined", False))
    o.parity = "only" if getattr(a, "parity_only", False) else "no" if getattr(a, "no_parity", False) else "both"
    o.tier = getattr(a, "tier", None) or (None if o.combined or o.only or o.parity == "only" else "full")
    return o


def catalog_size(e) -> tuple:
    """Bounding box (x, y, z) mm of a catalogue entry's model, ports/leads included."""
    from . import shapes
    bb = shapes.to_solid(e.shape).bounding_box()
    return (round(bb.size.X, 2), round(bb.size.Y, 2), round(bb.size.Z, 2))


def _catalog_filter(a) -> int:
    """`robot catalog --kind battery --fits 40x20x12 --max-mass 15`: catalogue parts that fit a measured free box
    (e.g. a `probe --place` box), smallest first. Look parts up; don't guess and retry."""
    box = None
    if a.fits:
        try:
            box = sorted(float(v) for v in a.fits.lower().split("x"))
        except ValueError:
            print("--fits takes LxWxH in mm, e.g. 40x20x12", file=sys.stderr)
            return 1
    rows = []
    for e in catalog.catalog():
        if a.kind and e.kind != a.kind:
            continue
        if a.max_mass is not None and e.mass_g > a.max_mass:
            continue
        try:
            size = catalog_size(e)
        except Exception:  # noqa: BLE001 - an entry without a buildable model cannot be judged
            continue
        sx, sy, sz = size
        fits = True
        if box:
            bx, by, bz = a.fits.lower().split("x")
            bx, by, bz = float(bx), float(by), float(bz)
            fits = sz <= bz and ((sx <= bx and sy <= by) or (sy <= bx and sx <= by))
        if fits:
            key = e.mass_g if a.sort == "mass" else -float((e.props or {}).get(a.sort, 0) or 0)
            rows.append((key, e, size))
    if not rows:
        print("nothing in the catalogue fits; make room (`robot probe --place PART`) or relax --fits/--max-mass")
        return 1
    for _, e, (sx, sy, sz) in sorted(rows, key=lambda t: t[0]):
        props = {k: v for k, v in (e.props or {}).items() if k in ("cells", "capacity_mah", "c_rating", "kv", "stall_a")}
        print(f"{e.id} | {e.kind} | {sx} x {sy} x {sz} mm | {e.mass_g:.1f} g | {props}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="robot", description="Antweight robot builder and verifier (build123d)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("guide")
    from . import doctor  # stdlib only: must load even when extras are missing

    doctor.add_cli(sub)
    from . import fieldhelp

    fieldhelp.add_cli(sub)
    c = sub.add_parser("catalog")
    c.add_argument("id", nargs="?")
    c.add_argument("--kind", help="only this kind (battery, motor, esc, receiver, switch, wheel, ...)")
    c.add_argument("--fits", help="LxWxH mm box the part must fit (any yaw about z), e.g. 40x20x12")
    c.add_argument("--max-mass", type=float, help="grams")
    c.add_argument("--sort", default="mass", help="mass | capacity_mah | kv | any numeric prop")
    sub.add_parser("materials")
    sub.add_parser("templates")
    t = sub.add_parser("template")
    t.add_argument("name")
    v = sub.add_parser("verify")
    v.add_argument("spec", nargs="?")
    v.add_argument("--full", action="store_true")
    v.add_argument("--only", metavar="GROUP[,GROUP...]", help="run only these check groups (parts are still built and cached)")
    v.add_argument("--list-groups", action="store_true", help="print the check group names and exit")
    v.add_argument("--fast", action="store_true", help="coarse tessellation for quick iteration")
    v.add_argument("--quick", action="store_true", help="skip the slow sweeps (wiring, assembly)")
    v.add_argument("--json", help="also write report.json here")
    v.add_argument("--llm", action="store_true", help="short output for a model: root causes with measured numbers and "
                   "the edit to make, nothing else (about 40 lines)")
    v.add_argument("--tier", choices=checks.TIERS, help="inner: cheap groups + fast proxies of the slow ones; full (default): "
                   "every design group; nightly: full + robust sweep + parity groups. --only wins over --tier")
    pg = v.add_mutually_exclusive_group()
    pg.add_argument("--no-parity", action="store_true", help="skip the groups that compare with a reference design")
    pg.add_argument("--parity-only", action="store_true", help="run only the reference-comparison groups (exit code still the design gate)")
    v.add_argument("--combined", action="store_true", help="old behaviour: run every group (unless --tier/--only) and let parity blockers decide ok too")
    v.add_argument("--list-tiers", action="store_true", help="print group, kind, tier, logged Revron seconds, proxy and exit")
    v.add_argument("--proxy", action="store_true", help="fast proxies of the slow groups (robot/proxy); --only picks among them")
    v.add_argument("--parts", help="with --proxy: only check these part ids (comma separated)")
    v.add_argument("--baseline", help="with --proxy: a full report.json whose routes / assembly order the proxies replay")
    for name in ("render", "export", "gen.cli", "cad.cli", "build_cmd", "evals.run", "solve.jiggle", "probe"):
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
        if a.kind or a.fits or a.max_mass is not None:
            return _catalog_filter(a)
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
    elif a.cmd == "verify" and getattr(a, "proxy", False):
        from .proxy import cli as proxy_cli

        if not a.spec:
            print("error: verify needs a spec path", file=sys.stderr)
            return 1
        return proxy_cli.verify(a, print_report)
    elif a.cmd == "verify":
        names = [n for n, _ in checks.GROUPS]
        if a.list_tiers:
            for g in checks.registry.REGISTRY:
                print(f"{g.name:<17}{g.kind:<7} {g.tier:<8}{'' if g.ref_s is None else f'{g.ref_s:.1f}':>7}  {g.proxy or '-'}")
            return 0
        if a.list_groups:
            print("\n".join(names + [checks.CLAIMS_GROUP]))
            return 0
        if not a.spec:
            print("error: verify needs a spec path", file=sys.stderr)
            return 1
        bad = [g for g in (opts_from(a).only or []) if g not in names and g != checks.CLAIMS_GROUP]
        if bad:
            print(f"error: unknown check group(s) {', '.join(bad)}; see `robot verify --list-groups`", file=sys.stderr)
            return 1
        try:
            s = spec_mod.load(a.spec)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        rep = checks.verify(s, opts_from(a))
        if getattr(a, "llm", False):
            print_llm(rep)
        else:
            print_report(rep, a.full)
        if a.json:
            Path(a.json).write_text(json.dumps(rep.to_dict(), indent=2))
            from .fix_hints import suggest_fixes  # UNTESTED: repair summary next to the report
            Path(a.json).with_suffix(".fixes.json").write_text(json.dumps(suggest_fixes(rep), indent=2, default=list))
        return 0 if rep.ok else 2
    elif hasattr(a, "func"):
        return a.func(a)
    return 0
