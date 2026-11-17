"""`robot field NAME`: how a spec field is written and which checks read it (copy a working example, don't guess).

Searches the verified example specs (robots/revron first, then templates and other robots) for the key, prints up to
3 short real examples with the part they sit on, and the check files that mention the key. With no name, lists every
key used in the examples with a count.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# verified first: an example that passes the verifier is the one to copy
SOURCES = ["robots/revron/spec.json", "robot/templates/revron.json", "robot/templates/wedge_2wd.json",
           "robots/wedge_2wd/spec.json", "robots/expandabot/spec.json"]
MAX_EXAMPLES = 3
MAX_CHARS = 300


def _walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            out.append((k, v, path, node))
            _walk(v, path + [k], out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk(v, path + [i], out)


def _entries():
    for rel in SOURCES:
        p = ROOT / rel
        if p.exists():
            try:
                out = []
                _walk(json.loads(p.read_text()), [], out)
                yield rel, out
            except (OSError, ValueError):
                continue


def readers(name: str) -> list[str]:
    pat = re.compile(r"[\"'.]" + re.escape(name) + r"\b")
    hits = []
    for f in sorted((HERE / "checks").rglob("*.py")):
        if pat.search(f.read_text(errors="ignore")):
            hits.append(str(f.relative_to(ROOT)))
    return hits


def examples(name: str) -> list[str]:
    rows = []
    for rel, ents in _entries():
        for k, v, path, owner in ents:
            if k != name:
                continue
            where = owner.get("id") or "/".join(map(str, path)) or "top level"
            txt = json.dumps({k: v})
            rows.append(f"{rel} [{where}]: {txt[:MAX_CHARS]}{' ...' if len(txt) > MAX_CHARS else ''}")
            if len(rows) >= MAX_EXAMPLES:
                return rows
    return rows


def all_keys() -> Counter:
    c = Counter()
    for _, ents in _entries():
        c.update(k for k, *_ in ents if isinstance(k, str))
    return c


def add_cli(sub):
    p = sub.add_parser("field", help="how a spec field is written (real examples) and which checks read it")
    p.add_argument("name", nargs="?", help="field name, e.g. weapon, secondary_ops, retained, locking_bar")
    p.set_defaults(func=run)


def run(a) -> int:
    if not a.name:
        for k, n in sorted(all_keys().items()):
            print(f"{k} ({n})")
        return 0
    ex, rd = examples(a.name), readers(a.name)
    if not ex and not rd:
        close = [k for k in all_keys() if a.name in k or k in a.name][:8]
        print(f"`{a.name}`: no example and no check reads it." + (f" Close: {', '.join(close)}" if close else ""))
        return 1
    print(f"`{a.name}` examples (copy one):" if ex else f"`{a.name}`: no example in the reference specs.")
    for r in ex:
        print("  " + r)
    if rd:
        print("read by: " + ", ".join(rd))
    return 0
