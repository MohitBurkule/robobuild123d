"""Generated LLM pack (B7): SKILL.md plus worked examples for an LLM agent.

Everything is generated from the live sources (GUIDE.md, the check registry, the
explain table, the templates, the rules profiles, llm_report), so the pack cannot
drift from the verifier: `robot llm-pack <dir>` writes it, and
robot/tests/test_llm_pack.py regenerates it and compares with the checked-in
`llm/` copy - if you change the verifier, regenerate the pack in the same commit.
"""

from __future__ import annotations

import json
from pathlib import Path

PACK_DIR_DEFAULT = "llm"
CHECKED_IN = Path(__file__).parent.parent / PACK_DIR_DEFAULT


def _guide_sections() -> list[str]:
    g = (Path(__file__).parent / "GUIDE.md").read_text().splitlines()
    return [ln[3:].strip() for ln in g if ln.startswith("## ")]


def _groups_md() -> str:
    from .checks import registry
    rows = []
    for g in registry.REGISTRY:
        if g.kind != registry.DESIGN:
            continue
        note = f" - {g.note}" if g.note else ""
        rows.append(f"| `{g.name}` | {g.tier} |{note}")
    return "\n".join(rows)


def _explain_lines() -> str:
    from .checks import explain
    return "\n".join(f"- `{k}` {v}" for k, v in explain.EXPLAIN.items())


def _profiles_md() -> str:
    from . import profile as prof
    return "\n".join(f"- `{n}` - {prof.description(n)}" for n in prof.available())


def _templates() -> list[str]:
    return sorted(p.stem for p in (Path(__file__).parent / "templates").glob("*.json"))


def _example_spec() -> str:
    t = (Path(__file__).parent / "templates" / "wedge_2wd.json").read_text()
    return json.dumps(json.loads(t), indent=2, sort_keys=False) + "\n"


def _example_compact() -> str:
    from . import llm_report
    rep = {
        "ok": False, "tier": "full", "gate": "design",
        "metrics": {"mass_total_g": 152.4, "mass_lo_g": 150.1, "mass_hi_g": 154.9, "mass_limit_g": 150},
        "findings": [
            {"id": "mass.over", "pass": False, "severity": "blocker", "message": "152.4 g is over the 150 g limit",
             "expected": "<= 150 g", "actual": "152.4 g", "parts": [], "repair": ["Cut grams from the wedge or the chassis shell."]},
            {"id": "interference.static", "pass": False, "severity": "blocker",
             "message": "`battery` overlaps `chassis` by 0.6 mm", "expected": "no overlap", "actual": "0.6 mm",
             "parts": ["battery", "chassis"], "repair": ["Move battery up 1 mm or deepen the pocket."]},
            {"id": "fastener.too_long", "pass": False, "severity": "warning",
             "message": "M2x8 screw bottoms out in a 6 mm boss", "expected": "<= 6 mm", "actual": "8 mm",
             "parts": ["lid"], "repair": ["Use M2x6."]},
        ],
        "not_checked": [], "not_run": [],
    }
    return json.dumps(llm_report.compact(rep), indent=2) + "\n"


def _example_patch() -> str:
    from .design_io import patch
    design = {"name": "wedge", "profile": "aws2025", "body": {"zt": 8.0},
              "drive": {"motor": "n20_1000rpm_6v"}}
    p = [{"op": "set", "path": "drive.motor", "value": "n20_2000rpm_6v"},
         {"op": "nudge", "path": "body.zt", "delta": 2.0},
         {"op": "unset", "path": "profile"}]
    out, errors = patch.apply(design, p)
    doc = {"design_before": design, "patch": p, "design_after": out, "errors": errors}
    return json.dumps(doc, indent=2) + "\n"


def generate() -> dict[str, str]:
    """The whole pack as {relative path: text content}. Deterministic: same verifier, same pack."""
    skill = f"""# Robobuild123d: design an antweight combat robot (SKILL)

You iterate on a JSON design file until the verifier passes it. `robot` below means `python3 -m robot`.
Units are mm and degrees; X lateral (left +x), Y forward, Z up; wheel centres at z = 0.

## Workflow (the whole skill is this loop)

1. Start from a template, never a blank file: `robot template wedge_2wd > spec.json` (templates: {", ".join(_templates())}).
2. `robot verify spec.json --json report.json` - exit 0 means the design gate passed.
3. Read the failures with `robot llm-report report.json` (compact, blockers first, each with `fixes`).
   Re-run it with `--prev last_report.json` to see the delta: `fixed` / `new` / `still` finding ids, and the mass move.
4. Fix the ROOT CAUSE the finding names (wrong part, wrong size, wrong place) - do not nudge numbers until a check goes quiet.
5. Repeat until `blockers` is 0. Warnings are acceptable; blockers never are.
6. `robot render spec.json iso out.png` to look at it, `robot export spec.json <slug> <dir>` when done.

## Rules profiles (E4)

The `profile` key of the spec selects a rules profile (`robot profiles` lists them):
{_profiles_md()}

## Machine interfaces

- `robot llm-report report.json [--prev old.json]` - the compact report for your context window.
- `robot explain <finding-id>` - what one finding id means and how to act on it.
- `robot mcp` - stdio JSON-RPC server exposing the same thing as tools: schema, catalog, validate, explain, diff, guide.
- Design patch language (iterate without resending the file): ops `set` / `nudge` / `unset` on dotted paths;
  `robot design_io.patch.apply(design, patch)` returns the new design plus errors with the allowed sibling paths.
- One error envelope everywhere: `{{"ok": false, "errors": [{{"path", "message", "expected", "actual"}}]}}`.

## Finding-id discipline

Findings are stable machine ids (`group.something`), never prose. Fix by id, verify by id - the delta section is keyed on ids.
What each id prefix means (from `robot explain`):
{_explain_lines()}

## Check groups (design gate)

Later groups read the metrics of earlier ones; run order is fixed. `--tier inner` is the cheap edit loop, `full` is the merge gate.
| group | tier |
|---|---|
{_groups_md()}

## Guide sections

The full guide is `robot guide` (or `robot guide "<section>"` for one). Sections:
{", ".join(f"`{s}`" for s in _guide_sections())}

## Examples (in this pack, `examples/`)

- `examples/wedge_2wd.spec.json` - a working starter design (the template itself).
- `examples/compact_report.json` - what `robot llm-report` gives you for a failing design: blockers with fixes first.
- `examples/patch_roundtrip.json` - a design, a patch, and the result of applying it.

## Regenerate this pack

`robot llm-pack <dir>` writes this pack from the live verifier sources; the drift test
(robot/tests/test_llm_pack.py) fails if the checked-in copy is stale.
"""
    return {
        "SKILL.md": skill,
        "examples/wedge_2wd.spec.json": _example_spec(),
        "examples/compact_report.json": _example_compact(),
        "examples/patch_roundtrip.json": _example_patch(),
    }


def write(out_dir: str | Path = PACK_DIR_DEFAULT) -> list[str]:
    """Write the pack into out_dir; returns the file list (relative paths)."""
    out = Path(out_dir)
    files = []
    for rel, text in generate().items():
        f = out / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(text)
        files.append(rel)
    return sorted(files)


def add_cli(sub):
    p = sub.add_parser("llm-pack", help="generate the LLM pack (SKILL.md + examples) into a directory")
    p.add_argument("dir", nargs="?", default=PACK_DIR_DEFAULT, help=f"output directory (default: ./{PACK_DIR_DEFAULT})")
    p.set_defaults(func=_run)


def _run(a):
    files = write(a.dir)
    for f in files:
        print(f"{a.dir}/{f}")
