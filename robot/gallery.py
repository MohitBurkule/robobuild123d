"""Gallery page (E6): one self-contained HTML page of every robot in a directory.

`build_gallery(root)` scans `<root>/<slug>/` for a spec.json (name, robot_type,
profile) and an optional report.json (verdict, blockers/warnings, mass) plus
renders/iso.png, and renders each robot as a card with the iso render embedded
as a base64 data URI - no server, no external files. Dirs without a spec are
skipped; a robot without a report shows "not verified" instead of failing.
`robot gallery robots -o gallery.html` writes the page.
"""

from __future__ import annotations

import base64
import html
import json
from pathlib import Path


def _esc(s):
    return html.escape(str(s if s is not None else ""))


def _load(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def _iso_png(robot_dir: Path) -> Path | None:
    r = robot_dir / "renders" / "iso.png"
    if r.exists():
        return r
    if (robot_dir / "renders").is_dir():
        pngs = sorted((robot_dir / "renders").glob("*.png"))
        return pngs[0] if pngs else None
    return None


def card(robot_dir: Path) -> dict:
    """The gallery facts of one robot dir: slug, name, type, profile, verdict, counts, mass, iso png bytes (or None)."""
    spec = _load(robot_dir / "spec.json")
    if spec is None:
        return {}
    rep = _load(robot_dir / "report.json") or {}
    m = rep.get("metrics") or {}
    s = rep.get("summary") or {}
    return {
        "slug": robot_dir.name,
        "name": spec.get("name") or robot_dir.name,
        "type": spec.get("robot_type") or "",
        "profile": rep.get("profile") or spec.get("profile") or "",
        "ok": rep.get("ok"),
        "blockers": s.get("blockers"),
        "warnings": s.get("warnings"),
        "mass": m.get("mass_total_g"),
        "mass_limit": m.get("mass_limit_g", 150),
        "png": _iso_png(robot_dir),
    }


def robots_in(root: str | Path) -> list[dict]:
    """A card dict for every subdir of root that has a spec.json, sorted by name."""
    root = Path(root)
    out = []
    if not root.is_dir():
        return out
    for d in sorted(p for p in root.iterdir() if p.is_dir()):
        c = card(d)
        if c:
            out.append(c)
    return out


def build_gallery(root: str | Path, title: str = "Robot gallery") -> str:
    cards = robots_in(root)
    items = []
    for c in cards:
        img = ""
        if c["png"]:
            b64 = base64.b64encode(c["png"].read_bytes()).decode()
            img = f"<img src='data:image/png;base64,{b64}' alt='{_esc(c['name'])} iso render'>"
        else:
            img = "<div class='norender'>no render</div>"
        if c["ok"] is None:
            verdict = "<span class='verdict none'>not verified</span>"
        else:
            verdict = (f"<span class='verdict {'pass' if c['ok'] else 'fail'}'>"
                       f"{'PASS' if c['ok'] else 'FAIL'}</span>")
        counts = ""
        if c["blockers"] is not None:
            counts = f"<small>{c['blockers']} blockers, {c['warnings']} warnings</small>"
        mass = ""
        if c["mass"] is not None:
            mass = f"<div class='mass'>{c['mass']:.1f} g <small>/ {c['mass_limit']:.0f} g</small></div>"
        items.append(
            f"<div class='card'><h3><code>{_esc(c['slug'])}</code> {_esc(c['name'])} {verdict}</h3>"
            f"{img}<p class='meta'>{_esc(c['type'])} · profile {_esc(c['profile'])}</p>{mass}{counts}</div>")
    body = "\n".join(items) or "<p>no robots found (no spec.json in any subdir)</p>"
    return f"""<!doctype html><html><head><meta charset='utf-8'><title>{_esc(title)}</title><style>
body{{font-family:system-ui,sans-serif;margin:24px}}
h1{{margin-top:0}}
.gallery{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.card{{border:1px solid #ddd;border-radius:8px;padding:12px}}
.card img{{width:100%;border-radius:6px;background:#f4f4f4}}
.norender{{height:160px;display:flex;align-items:center;justify-content:center;color:#999;background:#f4f4f4;border-radius:6px}}
.verdict{{padding:2px 10px;border-radius:6px;color:#fff;font-weight:700;font-size:0.8em;vertical-align:middle}}
.pass{{background:#2a9d8f}}.fail{{background:#e76f51}}.none{{background:#999}}
.meta{{color:#555;font-size:0.9em}}.mass{{font-size:1.2em;margin:4px 0}}
</style></head><body>
<h1>{_esc(title)}</h1>
<p>{len(cards)} robot{'s' if len(cards) != 1 else ''}</p>
<div class='gallery'>
{body}
</div></body></html>
"""


def add_cli(sub):
    p = sub.add_parser("gallery", help="one self-contained HTML gallery page of every robot in a directory")
    p.add_argument("dir", nargs="?", default="robots", help="directory of robot subdirs (default: robots)")
    p.add_argument("-o", "--out", default="gallery.html", help="output html (default: gallery.html)")
    p.set_defaults(func=_run)


def _run(a):
    html_text = build_gallery(a.dir, title=f"Robot gallery - {Path(a.dir).name}")
    Path(a.out).write_text(html_text)
    print(f"{a.out}: {len(robots_in(a.dir))} robots")
