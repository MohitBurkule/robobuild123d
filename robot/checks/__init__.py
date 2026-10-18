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
from dataclasses import dataclass, field

from .. import world as world_mod
from ..finding import BLOCKER, WARNING, Report, fail
from ..spec import Spec

# Bumped whenever a check is added or changed. 7 = the Rust crate's revision; 8 adds belt/fork tension (python port).
CHECKS_REVISION = 8

# (module, deep_only) in run order; same order as the Rust crate, plus `tension` before `assembly`.
GROUPS = [
    ("wiring", True), ("mass", False), ("interference", False), ("connections", False), ("ground", False),
    ("legal", False), ("fasteners", False), ("power", False), ("mfg", False), ("spinner", False), ("tension", False),
    ("assembly", True),
]


@dataclass
class Options:
    step_mm: float = 0.4  # grid step for sampled measures
    deep: bool = True  # run the slow sweeps (joint ranges, wiring routes, disassembly)
    strict_catalog: bool = False  # estimated catalog masses count as unverified in the pass/fail decision
    fast: bool = False  # coarse tessellation and grids (quick iteration); verdicts near limits may move
    only: list | None = None  # run only these groups (debugging)


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


def verify(spec: Spec, opts: Options | None = None) -> Report:
    opts = opts or Options()
    r = world_mod.resolve(spec, fast=opts.fast)
    return verify_resolved(r, opts)


def verify_resolved(r, opts: Options) -> Report:
    from . import validity

    rep = Report(name=r.spec.name, profile=r.profile.name)
    findings = []
    t0 = time.time()
    valid = validity.run(r, findings)
    rep.timings_s["validity"] = round(time.time() - t0, 3)
    ctx = None
    if valid:
        ctx = Ctx(r, world_mod.World.start(r), opts)
        for name, deep_only in GROUPS:
            if deep_only and not opts.deep:
                continue
            if opts.only and name not in opts.only:
                continue
            t0 = time.time()
            try:
                mod = importlib.import_module(f".{name}", __name__)
            except ModuleNotFoundError:
                findings.append(fail("checks.missing", "checks", WARNING, "Check group not available",
                                     f"The `{name}` checks are not in this build; nothing in that group was judged."))
                ctx.not_checked.append(f"Check group `{name}` is not available in this build")
                continue
            try:
                findings.extend(mod.run(ctx))
            except Exception as e:  # noqa: BLE001 - fail closed, never crash the report
                findings.append(fail("checks.crashed", "checks", BLOCKER, "A check crashed",
                                     f"`{name}` raised {type(e).__name__}: {e}. Its verdicts are unknown.")
                                .fix("Report this; the spec may hold geometry the check cannot handle."))
                ctx.not_checked.append(f"Check group `{name}` crashed: {type(e).__name__}")
                if os.environ.get("ROBOT_DEBUG"):
                    traceback.print_exc()
            rep.timings_s[name] = round(time.time() - t0, 3)
            if os.environ.get("ROBOT_TIMING"):
                print(f"{name} {time.time() - t0:.2f}s")
        findings.extend(validity.claims(ctx))
        rep.routes = ctx.routes
        rep.assembly = ctx.assembly
    rep.findings = findings
    rep.metrics = ctx.metrics if ctx else {}
    rep.checks_revision = CHECKS_REVISION
    rep.not_checked = not_checked(r, opts) + (ctx.not_checked if ctx else ["Every geometric check: the spec is not valid"])
    rep.bench_checklist = []
    rep.finish()
    return rep


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
