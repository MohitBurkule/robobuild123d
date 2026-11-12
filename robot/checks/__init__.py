"""The verification pipeline: one module per group of checks, all feeding one Report.

Each group module exposes `run(ctx) -> list[Finding]`. A group that is missing or raises is fail-closed: it becomes a
blocker finding (`checks.crashed`) or a warning (`checks.missing`) and is listed under NOT CHECKED, so a clean report can
never come from a check that did not run.
"""

from __future__ import annotations

import importlib
import os
import time
import traceback
from dataclasses import dataclass, field, replace

import json
import pickle
import sys

from .. import cache, world as world_mod
from ..finding import BLOCKER, WARNING, Report, fail
from ..spec import Spec

# Bumped whenever a check is added or changed. 7 = the Rust crate's revision; 8 adds belt/fork tension (python port); 9 adds
# wheel running clearance, wheel exposure, targets, fused/key/tape/press-fit evidence, stall-current battery peak.
CHECKS_REVISION = 21  # 21 adds the automated-development gates (waiver_audit, geom, dfm); 20 adds robust (one-at-a-time param / variant / COTS-swap perturbation sweep); 19 adds visual (silhouette views + depth, holes on every axis, faceting, fillet vs reference, slivers, dangling leads) and wire.render_wires; 18 adds integrity (one closed solid, volume collapse; runs first); 17 merges fix-T; 15 adds param (raw-literal lint) and sharp_corner (opt-out mfg.sharp_internal_corner); 14 adds the design-review groups (ref_map, cots_fidelity, wire_review, fastener_record, belt_wrap, print_orient); 13 adds intent (functional design-intent probes); 12 adds threat (combat failure modes CF-*); 10 adds internal (no_contact, fastener_void, wire_in_solid); 11 adds bom (reference BOM, lock part, O-ring stock, wire cut, switch dir, doc) and connection.cover_fasteners

# Every group, its kind (design | parity) and tier (inner | full | nightly) live in registry.py; GROUPS is the old
# (module, deep_only) view of it, in run order (same order as the Rust crate, plus `tension` before `assembly`).
from . import registry  # noqa: E402
from .registry import DESIGN, PARITY, TIERS  # noqa: E402,F401

GROUPS = [(g.name, g.deep_only) for g in registry.REGISTRY]

# `--only claims` is a pseudo-group: it evaluates spec claims and pulls in the groups that measure their metrics.
CLAIMS_GROUP = "claims"
# metric (exact name or "prefix.") -> group that measures it
CLAIM_METRIC_GROUPS = {"mass_": "mass", "part_mass_g.": "mass", "footprint_mm": "legal", "ground_z": "ground",
                       "com_": "mass", "cog_height_mm": "dynamics", "tip_angle_": "dynamics", "driven_weight_share": "dynamics",
                       "arch_": "architecture", "combat.": "combat", "archetype.": "archetype", "coverage.": "coverage"}


def claim_groups(spec) -> list:
    """Groups that must run so every claim's metric is measured."""
    out = []
    for c in spec.claims:
        for k, g in CLAIM_METRIC_GROUPS.items():
            if (c.metric == k or c.metric.startswith(k)) and g not in out:
                out.append(g)
    return out


def effective_only(spec, only):
    """`only` with the claim-metric groups added when the `claims` pseudo-group is requested."""
    if not only or CLAIMS_GROUP not in only:
        return only
    return list(only) + [g for g in claim_groups(spec) if g not in only]

MODULE = {"param": "param_lint", "geom": "geom_sanity"}  # group name -> module file when they differ


@dataclass
class Options:
    step_mm: float = 0.4  # grid step for sampled measures
    deep: bool = True  # run the slow sweeps (joint ranges, wiring routes, disassembly)
    strict_catalog: bool = False  # estimated catalog masses count as unverified in the pass/fail decision
    fast: bool = False  # coarse tessellation and grids (quick iteration); verdicts near limits may move
    only: list | None = None  # run only these groups (debugging); wins over `tier`
    tier: str | None = None  # inner | full | nightly (registry.py); None = every group, as before tiers existed
    parity: str = "both"  # "both" | "no" (skip parity groups) | "only" (run just the parity groups)
    combined: bool = False  # the old gate: parity blockers flip `ok` too


@dataclass
class Ctx:
    r: world_mod.Resolved
    world: world_mod.World
    opts: Options
    metrics: dict = field(default_factory=dict)
    routes: list = field(default_factory=list)
    captive: dict = field(default_factory=dict)  # part id -> blocking part ids (from interference)
    assembly: list = field(default_factory=list)
    not_checked: list = field(default_factory=list)


def tag(found, name):
    """Stamp the findings of registry group `name` with their kind (design | parity); returns them."""
    for f in found:
        f.kind = registry.kind_of(name, f.id)
    return found


def group_stats(rep, owned, sel=None):
    """Fill rep.groups (kind, tier, time, how it ran, counts) from [(group, how, findings)], and rep.not_run."""
    for name, how, found in owned:
        g = registry.INFO.get(name)
        t = rep.timings_s.get(f"proxy.{name}" if how == "proxy" else name)
        rep.groups[name] = {"kind": g.kind if g else DESIGN, "tier": g.tier if g else None, "time_s": t, "how": how,
                            "blockers": sum(1 for f in found if not f.passed and f.severity == BLOCKER),
                            "warnings": sum(1 for f in found if not f.passed and f.severity == WARNING),
                            "passed": sum(1 for f in found if f.passed)}
    if sel is not None:
        rep.not_run = [x for x in sel.not_run if x["group"] not in rep.groups]


def _proxy(ctx, name, rep, sel):
    """Inner tier: judge slow group `name` with its robot.proxy stand-in. None when it cannot run (no baseline)."""
    from .. import proxy

    pg = registry.INFO[name].proxy
    base = proxy.load_baseline(ctx.r.spec.name) if pg in ("assembly", "wiring") else {}
    if pg in ("assembly", "wiring") and not base.get("routes" if pg == "wiring" else "assembly"):
        if pg == "wiring" and not ctx.r.spec.wires:
            rep.timings_s[f"proxy.{pg}"] = 0.0
            return []  # nothing to route: the full group would judge nothing either
        sel.not_run.append({"group": name, "kind": DESIGN, "tier": registry.INFO[name].tier,
                            "reason": "its proxy replays the last full run and there is none yet: run --tier full once"})
        return None
    found, t = proxy.run(ctx, [pg], None, base)
    rep.timings_s.update(t)
    return found


def verify(spec: Spec, opts: Options | None = None) -> Report:
    opts = opts or Options()
    r = world_mod.resolve(spec, fast=opts.fast)
    return verify_resolved(r, opts)


def verify_resolved(r, opts: Options) -> Report:
    from . import validity

    rep = Report(name=r.spec.name, profile=r.profile.name)
    findings = []
    from .. import progress as _pg
    _pg.reset()
    t0 = time.time()
    valid = validity.run(r, findings)
    rep.timings_s["validity"] = round(time.time() - t0, 3)
    ctx = None
    base_key = _base_key(r, opts) if cache.enabled() else None
    sel = registry.select(opts.tier, opts.parity, effective_only(r.spec, opts.only), opts.deep)
    rep.tier, rep.gate = (None if opts.only else opts.tier), ("combined" if opts.combined else "design")
    owned = []  # (group, how it ran, its findings) for the per-group table
    # a group listed in GROUPS but not registered (a build without it) still runs fail-closed, as it always did
    unregistered = {n for n, _ in GROUPS if n not in registry.INFO and (not opts.only or n in opts.only)}
    if sel.filtered and not opts.only:  # a tier is an `only` list: claims and disasm already know how to read one
        opts = replace(opts, only=list(sel.run))
    if valid:
        ctx = Ctx(r, world_mod.World.start(r), opts)
        for name, _deep_only in GROUPS:
            if name in sel.proxies:
                t0 = time.time()
                try:
                    found = _proxy(ctx, name, rep, sel)
                except Exception as e:  # noqa: BLE001 - fail closed, as a full group does
                    found = [fail("checks.crashed", "checks", BLOCKER, "A check crashed",
                                  f"the fast proxy of `{name}` raised {type(e).__name__}: {e}. Its verdicts are unknown.")]
                    rep.timings_s[f"proxy.{name}"] = round(time.time() - t0, 3)
                if found is not None:
                    findings.extend(tag(found, name))
                    owned.append((name, "proxy", found))
                    ctx.not_checked.append(f"`{name}`: judged by its fast proxy only (inner tier); a pass is a strong hint, "
                                           f"not a verdict. Run --tier full for the real group")
                    _progress(name, t0, "proxy", findings)
                continue
            if name not in sel.run and name not in unregistered:
                continue
            t0 = time.time()
            try:
                mod = importlib.import_module(f".{MODULE.get(name, name)}", __name__)
            except ModuleNotFoundError:
                findings.append(fail("checks.missing", "checks", WARNING, "Check group not available",
                                     f"The `{name}` checks are not in this build; nothing in that group was judged."))
                ctx.not_checked.append(f"Check group `{name}` is not available in this build")
                continue
            gkey = _group_key(name, r, opts, base_key)
            hit = cache.get("group", gkey) if gkey else None
            if hit is not None and not cache.is_missing(hit):
                found, delta = hit
                findings.extend(tag(found, name))
                owned.append((name, "cached", found))
                for k, v in delta.items():
                    setattr(ctx, k, v)
                rep.timings_s[name] = round(time.time() - t0, 3)
                _progress(name, t0, "cached", findings)
                continue
            before = _snapshot(ctx) if gkey else None
            try:
                found = mod.run(ctx)
                findings.extend(tag(found, name))
                owned.append((name, "ran", found))
                if gkey:
                    after = _snapshot(ctx)
                    delta = {k: getattr(ctx, k) for k, v in after.items() if before.get(k) != v}
                    bad = [k for k in delta if isinstance(after[k], tuple)]
                    if bad:
                        print(f"  [not cached] {name}: writes unpicklable {', '.join(bad)}", flush=True)
                    else:
                        cache.put("group", gkey, (found, delta))
            except Exception as e:  # noqa: BLE001 - fail closed, never crash the report
                findings.append(fail("checks.crashed", "checks", BLOCKER, "A check crashed",
                                     f"`{name}` raised {type(e).__name__}: {e}. Its verdicts are unknown.")
                                .fix("Report this; the spec may hold geometry the check cannot handle."))
                ctx.not_checked.append(f"Check group `{name}` crashed: {type(e).__name__}")
                tag(findings[-1:], name)  # a crashed parity group is a parity blocker, a crashed design group a design one
                owned.append((name, "crashed", findings[-1:]))
                if os.environ.get("ROBOT_DEBUG"):
                    traceback.print_exc()
            rep.timings_s[name] = round(time.time() - t0, 3)
            _progress(name, t0, "ran", findings)
        findings.extend(validity.claims(ctx))
        rep.routes = ctx.routes
        rep.assembly = ctx.assembly
        rep.mass = getattr(ctx, "mass_lines", [])
    rep.findings = findings
    from . import waiver as _waiver
    waivers = _waiver.apply(r.spec, findings)
    rep.metrics = ctx.metrics if ctx else {}
    rep.checks_revision = CHECKS_REVISION
    rep.not_checked = not_checked(r, opts) + (ctx.not_checked if ctx else ["Every geometric check: the spec is not valid"])
    rep.bench_checklist = []
    group_stats(rep, owned, sel if sel.filtered else None)
    if sel.filtered and rep.not_run and not (opts.tier is None and opts.parity == "both"):
        rep.not_checked.append(f"NOT RUN in this tier: {len(rep.not_run)} check groups (listed under `not_run`): "
                               + ", ".join(x["group"] for x in rep.not_run))
    rep.finish()
    if ctx is not None and (rep.routes or rep.assembly) and not r.fast and cache.enabled():
        _store_baseline(r.spec.name, rep)
    if waivers:
        rep.summary["waivers"] = waivers
    return rep


def _store_baseline(name, rep):
    """Keep this run's routes / teardown order where the inner tier's proxies find them (robot.proxy.baseline_path)."""
    from dataclasses import asdict

    from .. import proxy

    try:
        p = proxy.baseline_path(name)
        old = json.loads(p.read_text()) if p.is_file() else {}
        new = {"routes": [asdict(x) for x in rep.routes] or old.get("routes") or [],
               "assembly": [asdict(x) for x in rep.assembly] or old.get("assembly") or []}
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(new))
    except Exception:  # noqa: BLE001 - a convenience for later inner runs, never a reason to fail this one
        pass


_SKIP = ("r", "world", "opts", "_hub_kin")  # _hub_kin: lazy kinematics cache, rebuilt on demand


def _snapshot(ctx) -> dict:
    """Pickled bytes of every context field a group may write (None when a field cannot be pickled)."""
    out = {}
    for k, v in vars(ctx).items():
        if k in _SKIP:
            continue
        try:
            out[k] = pickle.dumps(v, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:  # noqa: BLE001 - tracked by identity; a group that replaces it is not cached
            out[k] = ("unpicklable", id(v))
    return out


def _base_key(r, opts) -> str:
    """Everything every group can read: all sources, the spec, every part's geometry key, options."""
    o = dict(vars(opts))  # includes `only`: a group's verdicts depend on which groups ran before it
    return cache.h(cache.code_hash(), json.dumps(r.spec.raw, sort_keys=True, default=str), cache.referenced_hash(r.spec.raw, r.spec.base_dir),
                   [p.geom.key for p in r.parts], r.load_errors, json.dumps(o, sort_keys=True, default=str), r.fast)


def _group_key(name, r, opts, base_key):
    return cache.h("group", name, base_key) if base_key else None


def _progress(name, t0, how, findings=()):
    from .. import progress
    nb = sum(1 for f in findings if not f.passed and str(f.severity).lower() == "blocker")
    progress.log(f"check {name} {how} in {time.time() - t0:.1f}s; blockers so far {nb}")
    progress.blockers(name, findings)
    if os.environ.get("ROBOT_TIMING") or os.environ.get("ROBOT_PROGRESS") == "1":
        print(f"  [{how}] {name} {time.time() - t0:.2f}s", file=sys.stdout, flush=True)


def not_checked(r, opts) -> list:
    v = [
        "Strength: arm, fork and shell bending under impact (no stress or stiffness model; load path is not traced)",
        "Battery access and field service: swap time, number of fasteners to reach the battery or change a wheel",
        "Wire tether in assembly order: soldered wires between parts are not part of the disassembly sweep",
        "Heat-set insert iron clearance and soldering-iron access",
        "Gyro, spin-up time and ESC current limits of the weapon",
        "Thermal limits and glue or tape strength (declared only)",
    ]
    if not opts.deep:
        v.append("Wire routing, wire mass and the assembly/disassembly sweep (fast mode skipped them)")
    if r.spec.is_spinner:
        v.append("Spinner balance and vibration at speed (mass centre of the weapon is not compared with its axis)")
    return v
