"""`python3 -m robot gen ...`: enumerate hypotheses, solve layouts, build verified robots."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def add_cli(sub):
    g = sub.add_parser("gen", help="template engine: hypotheses -> layouts -> verified robot specs")
    gs = g.add_subparsers(dest="gen_cmd")

    lh = gs.add_parser("list-hypotheses", help="count / list valid hypotheses (rules applied)")
    lh.add_argument("--fix", action="append", default=[], help="axis=value (repeatable), e.g. --fix weapon=vspin_drisk")
    lh.add_argument("--limit", type=int, default=20, help="list at most this many (0 = counts only)")
    lh.add_argument("--buildable", action="store_true", help="only hypotheses the assembler can build")
    lh.add_argument("--json", action="store_true")

    b = gs.add_parser("build", help="build one hypothesis into a spec that passes `robot verify` (or fail)")
    b.add_argument("--hypothesis", required=True,
                   help="preset name (wedge, vspin_drisk, hspin_bar, lifter, ...) or axis=value,... list")
    b.add_argument("--out", required=True, help="output directory")
    b.add_argument("--name", help="file stem (default: the weapon type)")
    b.add_argument("--layout", type=int, default=0, help="use the n-th best wireable layout")
    b.add_argument("--fast", action="store_true", help="gate with the verifier's fast mode")
    b.add_argument("--no-gate", action="store_true", help="write the spec without verifying it")

    lo = gs.add_parser("layouts", help="top-K internal layouts for a layout-inputs JSON (or a hypothesis)")
    lo.add_argument("inputs", help="spec_inputs.json (LayoutInputs fields) or a hypothesis string")
    lo.add_argument("-k", type=int, default=5)
    lo.add_argument("--json", help="write the layouts here")
    g.set_defaults(func=run)


def _hyp(text):
    from . import hypothesis as H
    if "=" in text:
        return H.Hypothesis.parse(text)
    return H.preset(text)


def run(a):
    from . import hypothesis as H
    cmd = getattr(a, "gen_cmd", None)
    if cmd == "list-hypotheses":
        fixed = dict(kv.split("=", 1) for kv in a.fix)
        for k, v in list(fixed.items()):
            if k not in H.AXES:
                print(f"unknown axis {k}; axes: {', '.join(H.AXIS_ORDER)}", file=sys.stderr)
                return 1
            fixed[k] = H.coerce(k, v)
        n = H.count_hypotheses(fixed)
        print(f"{n} valid hypotheses" + (f" with {fixed}" if fixed else ""))
        if not fixed:
            for w, c in sorted(H.count_by_weapon().items(), key=lambda t: -t[1]):
                print(f"  {w:22s} {c:8d}{'  (buildable)' if w in H.BUILDABLE else ''}")
        shown = 0
        for h in H.enumerate_hypotheses(fixed):
            if a.limit and shown >= a.limit:
                break
            if a.buildable and not H.buildable(h):
                continue
            print(json.dumps(h.to_dict()) if a.json else h.slug)
            shown += 1
        return 0
    if cmd == "build":
        from . import build as B
        from .gate import Rejected, gate
        h = _hyp(a.hypothesis)
        out = Path(a.out)
        out.mkdir(parents=True, exist_ok=True)
        name = a.name or h.weapon
        if a.no_gate:
            d = B.build(h, layout_index=a.layout)
            n_block = None
        else:
            try:
                res = gate(h, fast=a.fast, log=print)
            except Rejected as e:
                print(f"rejected: {e}", file=sys.stderr)
                return 2
            d = res.spec
            n_block = 0
        p = out / f"{name}.json"
        p.write_text(json.dumps(d, indent=1))
        print(f"wrote {p}" + ("" if n_block is None else " (verify: 0 blockers)"))
        return 0
    if cmd == "layouts":
        from .layout import solve
        src = Path(a.inputs)
        if src.exists():
            d = json.loads(src.read_text())
            lays = solve(d.get("layout_inputs", d), k=a.k)
        else:
            from . import build as B
            lays = B.layouts(_hyp(a.inputs), k=a.k)
        rows = []
        for i, L in enumerate(lays):
            row = {"rank": i, "score": round(L.score, 2), "terms": {k: round(v, 2) for k, v in L.terms.items()},
                   "placements": {k: [p.x, p.y, p.rot_z] for k, p in L.placements.items()}}
            rows.append(row)
            print(f"#{i} score {row['score']}: " + ", ".join(f"{k}@({v[0]:g},{v[1]:g},{v[2]:g})" for k, v in row["placements"].items()))
        if a.json:
            Path(a.json).write_text(json.dumps(rows, indent=1))
        return 0
    print("usage: robot gen {list-hypotheses,build,layouts} ...", file=sys.stderr)
    return 1
