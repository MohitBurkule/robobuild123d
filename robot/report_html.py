"""HTML report with an embedded 3D viewer (E1): one self-contained file per verify run.

`build_html(report_dict, glb_bytes=None)` renders mass, verdict, every failing
finding (with its fix hint), metrics and the not_checked list; the GLB (from
robot/glb.py) is embedded as a base64 data URI that <model-viewer> loads - no
server, no external files. `robot report spec.json -o report.html` runs verify
first (or reads an existing report with --from-report).
"""

from __future__ import annotations

import base64
import html
import json

MODEL_VIEWER = ("https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js",)


def _esc(s):
    return html.escape(str(s if s is not None else ""))


def build_html(rep: dict, glb: bytes | None = None, title: str = "") -> str:
    s = rep.get("summary") or {}
    m = rep.get("metrics") or {}
    rows = []
    for f in rep.get("findings", []):
        if f.get("pass", True):
            continue
        cls = "blocker" if f.get("severity") == "blocker" else "warning"
        fix = f"<div class='fix'>fix: {_esc(f.get('fix'))}</div>" if f.get("fix") else ""
        rows.append(f"<tr class='{cls}'><td><code>{_esc(f.get('id'))}</code></td><td>{_esc(f.get('message'))}"
                    f"<br><small>{_esc(f.get('parts'))}</small>{fix}</td></tr>")
    glb_block = ""
    if glb:
        b64 = base64.b64encode(glb).decode()
        glb_block = ("<model-viewer style='width:100%;height:420px' camera-controls auto-rotate "
                     f"src='data:model/gltf-binary;base64,{b64}'></model-viewer>")
    mass = ""
    if "mass_total_g" in m:
        mass = (f"<div class='mass'>{m['mass_total_g']:.1f} g "
                f"<small>({m.get('mass_lo_g', 0):.1f}-{m.get('mass_hi_g', 0):.1f} g, limit {m.get('mass_limit_g', 150):.0f})</small></div>")
    not_checked = ""
    if rep.get("not_checked"):
        items = "".join(f"<li>{_esc(x)}</li>" for x in rep["not_checked"][:30])
        not_checked = f"<h3>Not checked</h3><ul>{items}</ul>"
    verdict = "PASS" if rep.get("ok") else "FAIL"
    vcls = "pass" if rep.get("ok") else "fail"
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{_esc(title or rep.get('name', 'report'))}</title>
<script type='module' src='{MODEL_VIEWER[0]}'></script><style>
body{{font-family:system-ui,sans-serif;margin:24px;max-width:900px}}
.verdict{{padding:6px 14px;border-radius:6px;color:#fff;font-weight:700;display:inline-block}}
.pass{{background:#2a9d8f}}.fail{{background:#e76f51}}
tr.blocker td{{background:#fdecea}}tr.warning td{{background:#fff7e0}}
.fix{{color:#555;font-size:0.9em;margin-top:4px}}.mass{{font-size:1.4em;margin:8px 0}}
table{{border-collapse:collapse;width:100%}}td{{padding:8px;border-bottom:1px solid #ddd;vertical-align:top}}
</style></head><body>
<h1>{_esc(rep.get('name', 'robot'))} <span class='verdict {vcls}'>{verdict}</span></h1>
{mass}{glb_block}
<p>{s.get('blockers', 0)} blockers, {s.get('warnings', 0)} warnings, {s.get('passed', 0)} passed
(gate {rep.get('gate', 'design')}{', tier ' + rep.get('tier') if rep.get('tier') else ''})</p>
<table>{''.join(rows)}</table>
{not_checked}
</body></html>"""


def world_to_glb_bytes(world) -> bytes:
    """The built world as GLB bytes (robot/glb.py builds the scene)."""
    from .glb import world_to_glb

    return world_to_glb(world)


def add_cli(sub):
    p = sub.add_parser("report", help="self-contained HTML report (with 3D viewer) for a spec")
    p.add_argument("spec", nargs="?")
    p.add_argument("-o", "--out", default="report.html")
    p.add_argument("--from-report", help="build the HTML from an existing report.json (no verify run)")
    p.add_argument("--no-glb", action="store_true")
    p.set_defaults(func=_run)


def _run(a):
    import sys
    from pathlib import Path

    if a.from_report:
        rep = json.loads(Path(a.from_report).read_text())
        glb = None
    else:
        if not a.spec:
            print("error: report needs a spec path (or --from-report)", file=sys.stderr)
            return 1
        from . import checks, spec as spec_mod

        try:
            s = spec_mod.load(a.spec)
        except ValueError as e:
            print(f"error: {e}", file=sys.stderr)
            return 1
        rep = checks.verify(s).to_dict()
        glb = None
        if not a.no_glb:
            try:
                from . import world as world_mod

                glb = world_to_glb_bytes(world_mod.build(s))
            except Exception as e:  # the report must survive a viewer failure
                print(f"note: no 3D viewer ({e})", file=sys.stderr)
    Path(a.out).write_text(build_html(rep, glb))
    print(f"wrote {a.out}")
    return 0
