"""`python3 -m robot build design.json [out_dir]`: the LLM front door. UNTESTED (written without running).

Steps, each failing closed with a machine-readable error an LLM can act on:
  1. parse   design.json (bad_json)
  2. validate via robot.design_io.validate (codes: bad_type, unknown_key, not_configurable, bad_enum, ...)
  3. generate spec via robot.gen.build.build(hypothesis, user overrides) (build_failed)
  4. verify  fast tier (checks.Options(fast=True, tier="fast")) -> blockers with fix hints
  5. export  STEP/STL/DXF/renders/REPORT.md via robot.export.write_all (export_failed)
Always writes <out>/<slug>/build_result.json: {ok, stage, errors[], blockers[], files[], next_steps[]}.
Exit codes: 0 ok, 1 invalid design, 2 verify blockers, 3 build/export crash.
"""

from __future__ import annotations

import json
import re
import traceback
from pathlib import Path

STAGES = ("parse", "validate", "generate", "verify", "export")


def slug_of(design: dict, path: str | Path) -> str:
    raw = str(design.get("name") or Path(path).stem or "robot")
    return re.sub(r"[^a-z0-9_-]+", "_", raw.lower()).strip("_") or "robot"


def result(stage, ok, errors=(), blockers=(), files=(), metrics=None, next_steps=()):
    return {"ok": ok, "stage": stage, "errors": list(errors), "blockers": list(blockers), "files": list(files),
            "metrics": metrics or {}, "next_steps": list(next_steps)}


def next_steps_for(errors) -> list:
    """Plain-language edits for the LLM, one per error, using the validator's suggestion/allowed lists."""
    out = []
    for e in errors:
        f = e.get("field") or "?"
        if e.get("suggestion"):
            out.append(f"set {f} to {e['suggestion']!r} (closest allowed value)")
        elif e.get("allowed"):
            out.append(f"set {f} to one of {e['allowed']}")
        elif e.get("code") == "unknown_key":
            out.append(f"remove {f}")
        elif e.get("hint"):
            out.append(f"{f}: {e['hint']}")
        else:
            out.append(f"{f}: {e.get('message')}")
    return out


def blocker_rows(rep) -> list:
    from .finding import BLOCKER
    return [{"id": f.id, "message": f.message, "parts": list(f.parts or []), "fix": f.fix_hint, "at": f.at}
            for f in rep.findings if not f.passed and f.severity == BLOCKER]


def run(design_path, out_dir="robots", *, export=True, step=True, tier="fast", width=900) -> dict:
    """Whole pipeline; never raises. Returns the build_result dict (also written to disk when possible)."""
    design_path = Path(design_path)
    try:
        design = json.loads(design_path.read_text())
        if not isinstance(design, dict):
            raise ValueError("top level must be a JSON object")
    except (OSError, ValueError) as e:
        return result("parse", False, [{"code": "bad_json", "field": "", "message": str(e)}],
                      next_steps=["send one JSON object; see `python3 -m robot build --schema`"])
    slug = slug_of(design, design_path)
    root = Path(out_dir) / slug

    def done(res):
        try:
            root.mkdir(parents=True, exist_ok=True)
            (root / "build_result.json").write_text(json.dumps(res, indent=2, default=str))
        except OSError:
            pass
        return res

    from . import design_io
    h, user, errors = design_io.validate(design)
    if errors:
        return done(result("validate", False, errors, next_steps=next_steps_for(errors)))
    try:
        from .gen import build as gen_build
        spec_d = gen_build.build(h, user)
        spec_d.setdefault("name", design.get("name") or slug)
        spec_d.setdefault("generator", {})["design"] = design
    except Exception as e:  # noqa: BLE001 - BuildError and crashes both go back to the LLM
        return done(result("generate", False, [{"code": "build_failed", "field": "", "message": f"{type(e).__name__}: {e}",
                                                "hint": "relax body dims or pick another layout; see errors"}],
                           next_steps=["try a different drive/front/battery combination"]))
    from . import checks, spec as spec_mod
    try:
        spec = spec_mod.Spec(spec_d, root)
        opts = checks.Options(fast=True, deep=False)
        opts.tier = tier
        rep = checks.verify(spec, opts)
    except Exception as e:  # noqa: BLE001
        return done(result("verify", False, [{"code": "verify_crashed", "field": "", "message": f"{type(e).__name__}: {e}",
                                              "trace": traceback.format_exc(limit=3)}]))
    metrics = {k: rep.metrics.get(k) for k in ("mass_total_g", "mass_hi_g", "footprint_mm") if k in rep.metrics}
    blockers = blocker_rows(rep)
    files = []
    if export:
        try:
            from . import export as export_mod
            rep2, files = export_mod.write_all(slug, spec, out_dir, opts, step=step, width=width)
            blockers = blocker_rows(rep2) or blockers
        except Exception as e:  # noqa: BLE001
            return done(result("export", False, [{"code": "export_failed", "field": "", "message": f"{type(e).__name__}: {e}"}],
                               blockers, metrics=metrics))
    else:
        root.mkdir(parents=True, exist_ok=True)
        (root / "spec.json").write_text(json.dumps(spec_d, indent=1))
        files = ["spec.json"]
    steps = [f"{b['id']}: {b['fix'] or b['message']}" for b in blockers]
    return done(result("export" if export else "verify", not blockers, blockers=blockers, files=files,
                       metrics=metrics, next_steps=steps))


def exit_code(res) -> int:
    if res["ok"]:
        return 0
    return {"parse": 1, "validate": 1}.get(res["stage"], 2 if res["blockers"] and not res["errors"] else 3)


def cli(a):
    from . import design_io
    if a.schema:
        print(json.dumps(design_io.schema(buildable_only=True), indent=1))
        return 0
    if not a.design:
        print("usage: robot build design.json [out_dir]  (or --schema)")
        return 1
    res = run(a.design, a.out, export=not a.no_export, step=not a.no_step, tier=a.tier)
    if a.json:
        print(json.dumps(res, indent=1, default=str))
    else:
        print(f"build {'OK' if res['ok'] else 'FAILED'} at stage {res['stage']}; "
              f"{len(res['errors'])} errors, {len(res['blockers'])} blockers, {len(res['files'])} files")
        for e in res["errors"]:
            print(f"  [error {e['code']}] {e.get('field')}: {e['message']}")
        for b in res["blockers"]:
            print(f"  [BLOCKER] {b['id']}: {b['message']}")
        for s in res["next_steps"]:
            print(f"  next: {s}")
    return exit_code(res)


def add_cli(sub):
    p = sub.add_parser("build", help="design.json -> validated, verified, exported robot (LLM front door)")
    p.add_argument("design", nargs="?")
    p.add_argument("out", nargs="?", default="robots")
    p.add_argument("--schema", action="store_true", help="print the buildable design.json JSON Schema and exit")
    p.add_argument("--json", action="store_true", help="print build_result.json to stdout")
    p.add_argument("--no-export", action="store_true", help="validate + generate + verify only (fast)")
    p.add_argument("--no-step", action="store_true")
    p.add_argument("--tier", default="fast", help="verify tier (default fast)")
    p.set_defaults(func=cli)
