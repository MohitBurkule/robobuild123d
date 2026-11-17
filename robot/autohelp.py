"""Automatic helpers folded into every `verify`, so a model never has to remember a separate tool.

After the checks run, `enrich(rep, ctx, r)` adds to the report (and the printed output):
  * per root cause: measured context for its parts (world box, ports, gap/overlap to each neighbour), i.e. what
    `robot probe <part>` prints;
  * a mass budget (grams per part, solid-block warning) whenever a mass finding fails;
  * an automatic jiggle over the spec's declared `levers` (named masters) when collisions remain: the proposed
    master values and the violation they reach, as an info finding `solve.proposal` (never applied by itself);
  * a pointer to robot/docs/FACTS.md for check semantics.
Each helper is bounded (time / count) and can never fail the run. ROBOT_AUTOHELP=0 turns it off;
ROBOT_AUTOJIGGLE=0 skips only the jiggle.
"""

from __future__ import annotations

import os
import time

from .finding import note

MAX_ROOTS = 12
MAX_PARTS_PER_ROOT = 2
COLLIDE = ("interference.overlap", "fit.interference", "interference.sweep", "kin.sweep_static", "kin.rub_gap",
           "assembly.blocked")


def enrich(rep, ctx, r):
    if ctx is None or os.environ.get("ROBOT_AUTOHELP", "1") == "0":
        return
    rep.helpers = getattr(rep, "helpers", None) or {}
    t0 = time.time()
    try:
        if any(not f.passed and f.id.startswith("mass.") for f in rep.findings):
            from .probe import mass_report
            rep.helpers["mass_budget"] = mass_report(r.spec, r, ctx.world).splitlines()
    except Exception as e:  # noqa: BLE001
        rep.helpers["mass_error"] = str(e)
    try:
        _autojiggle(rep, ctx, r)
    except Exception as e:  # noqa: BLE001
        rep.helpers["jiggle_error"] = str(e)
    if any(f.id == "solve.proposal" for f in rep.findings):
        rep.finish()   # recount with the proposal; roots are rebuilt, so context goes on after
    try:
        _context(rep, ctx, r)
    except Exception as e:  # noqa: BLE001
        rep.helpers["context_error"] = str(e)
    rep.helpers["facts"] = "robot/docs/FACTS.md: what the checks mean and the tools behind these numbers"
    rep.timings_s["autohelp"] = round(time.time() - t0, 3)


def _context(rep, ctx, r):
    from .probe import part_report

    ids = {b.id for b in ctx.world.bodies}
    for c in (rep.roots or [])[:MAX_ROOTS]:
        lines = []
        for pid in [p for p in c.get("parts", []) if p in ids][:MAX_PARTS_PER_ROOT]:
            lines += part_report(r.spec, r, ctx.world, pid).splitlines()
        if lines:
            c["context"] = lines


def _autojiggle(rep, ctx, r):
    levers = r.spec.raw.get("levers")
    path = getattr(r.spec, "path", None)
    if not levers or not path or os.environ.get("ROBOT_AUTOJIGGLE", "1") == "0":
        return
    if not any(c.get("primary") in COLLIDE for c in rep.roots or []):
        return
    from .solve import jiggle

    lv = jiggle.parse_levers(path, [], levers)
    regen = r.spec.raw.get("generator")
    if regen:
        regen = str((r.spec.base_dir / regen).resolve())
    res = jiggle.solve_params(path, lv, iters=int(os.environ.get("ROBOT_AUTOJIGGLE_ITERS", "4")), fast=True,
                              log=lambda *_: None, regen=regen, regen_cwd=r.spec.raw.get("generator_cwd"))
    rep.helpers["jiggle"] = res
    if res["changed"]:
        txt = ", ".join(f"{k} {a:g} -> {b:g}" for k, (a, b) in res["changed"].items())
        rep.findings.append(note("solve.proposal", "solve", "Measured layout proposal",
                                 f"Jiggle over the spec levers: {txt} takes collision depth {res['start']:.2f} -> "
                                 f"{res['final']:.2f} mm (left: {len(res['left'])}). Apply with `robot jiggle "
                                 f"<spec> --write-params` or edit the masters.").on(*sorted({x[0] for x in res['left']}) or []))


def text(rep) -> str:
    h = getattr(rep, "helpers", None) or {}
    out = []
    if h.get("mass_budget"):
        out += ["MASS BUDGET:"] + [f"  {x}" for x in h["mass_budget"]]
    j = h.get("jiggle")
    if j and j.get("changed"):
        out.append(f"JIGGLE PROPOSAL (not applied): " + ", ".join(f"{k} {a:g} -> {b:g}" for k, (a, b) in j["changed"].items())
                   + f"; collision depth {j['start']:.2f} -> {j['final']:.2f} mm")
    if h.get("facts"):
        out.append(f"FACTS: {h['facts']}")
    return "\n".join(out)
