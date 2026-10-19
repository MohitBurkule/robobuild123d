"""`python3 -m robot gate spec.json`: the one command to run before claiming "the model matches the reference".

WHY: "done" was claimed on partial evidence (a quick verify, a render glance, a diff run on one part). The gate
re-checks everything from scratch and prints one PASS/FAIL line per condition:
  verify        full verify (deep, fine tessellation) has 0 blockers
  ref_diff      every `reference_cad.diff` and `reference_cad.features` finding passes, and at least one ran
  support       print support: every `intent.support_free` and `printability.*` finding passes, and at least one ran
  renders       the render PNGs exist (default <spec dir>/renders/{iso,top,back}.png), non-empty and not older
                than the spec file
Exit 0 only when every line is PASS. A condition that could not be evaluated is a FAIL, never a pass.
"""

from __future__ import annotations

import sys
from pathlib import Path

from ..finding import BLOCKER

DEFAULT_RENDERS = ("iso.png", "top.png", "back.png")
REF_IDS = ("reference_cad.diff", "reference_cad.features")


def _family(rep, pred, name):
    fs = [f for f in rep.findings if pred(f.id)]
    if not fs:
        return False, f"no {name} findings (not run / not configured)"
    bad = [f for f in fs if not f.passed]
    if bad:
        return False, f"{len(bad)}/{len(fs)} failing: " + "; ".join(f"{f.id} {f.message[:90]}" for f in bad[:4])
    return True, f"{len(fs)} findings pass"


def evaluate(rep, spec_path, render_dir=None, renders=DEFAULT_RENDERS) -> list:
    """[(name, ok, detail)] for a finished full Report."""
    rows = []
    blockers = [f for f in rep.findings if not f.passed and f.severity == BLOCKER]
    rows.append(("verify", not blockers, f"{len(blockers)} blockers" + (": " + "; ".join(f.id for f in blockers[:6]) if blockers else "")))
    rows.append(("ref_diff", *_family(rep, lambda i: i in REF_IDS, "reference_cad.diff/features")))
    rows.append(("support", *_family(rep, lambda i: i == "intent.support_free" or i.startswith("printability."),
                                     "support/printability")))
    sp = Path(spec_path)
    rd = Path(render_dir) if render_dir else sp.parent / "renders"
    t_spec = sp.stat().st_mtime if sp.exists() else 0
    missing = [n for n in renders if not (rd / n).is_file() or (rd / n).stat().st_size == 0]
    stale = [n for n in renders if n not in missing and (rd / n).stat().st_mtime < t_spec]
    ok = not missing and not stale
    rows.append(("renders", ok, f"{rd}: " + ("all present" if ok else f"missing {missing} stale {stale}")))
    return rows


def gate(spec_path, render_dir=None, renders=DEFAULT_RENDERS):
    from .. import checks, spec as spec_mod

    rep = checks.verify(spec_mod.load(spec_path), checks.Options(deep=True, fast=False))
    return evaluate(rep, spec_path, render_dir, renders), rep


def cli(a):
    try:
        rows, _ = gate(a.spec, a.renders, tuple(a.views.split(",")) if a.views else DEFAULT_RENDERS)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    for name, ok, detail in rows:
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    good = all(r[1] for r in rows)
    print("GATE PASS" if good else "GATE FAIL")
    return 0 if good else 3


def add_cli(sub):
    p = sub.add_parser("gate", help="done gate: full verify 0 blockers + reference diff + support + renders")
    p.add_argument("spec")
    p.add_argument("--renders", help="render directory (default <spec dir>/renders)")
    p.add_argument("--views", help="comma list of render files to require (default iso.png,top.png,back.png)")
    p.set_defaults(func=cli)
