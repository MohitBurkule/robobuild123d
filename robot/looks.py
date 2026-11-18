"""`robot looks SPEC_OR_KIT [...]`: the whole looks loop in one call, batchable.

For each argument: a kit JSON (has "body"/"weapon"/"wheels" and no "parts") is first built with `robot kit` into
<stem>_spec.json next to it. Then: iso + top renders, the `likeness` gate (with overlays) and the `diff-photo` sheet,
all into <spec dir>/renders/. Prints one summary line per robot. Exit code 1 if any likeness gate fails.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path


def one(path: Path) -> tuple[str, bool]:
    from . import kit
    d = json.loads(path.read_text())
    if "parts" not in d and any(k in d for k in ("body", "weapon", "wheels", "legs")):
        sp = path.with_name(path.stem + "_spec.json")
        sp.write_text(json.dumps(kit.build(d), indent=1))
        path = sp
    out = path.parent / "renders"
    out.mkdir(parents=True, exist_ok=True)
    from . import render as R
    from .checks import likeness as L
    from . import diff_photo as D
    for v in ("iso", "top"):
        R.cli(_ns(spec=str(path), view=v, out=str(out / f"{path.stem}_{v}.png")))
    ok = L.cli_main(str(path), str(out)) == 0
    try:
        D.main(str(path), str(out))
    except Exception as e:  # noqa: BLE001  (no photos / no masks: the sheet is optional)
        print(f"diff-photo skipped: {e}")
    return str(path), ok


def _ns(**kw):
    from types import SimpleNamespace
    base = dict(markers=False, width=1100, fast=True, quick=True, palette=None, section_z=None, no_checks=True,
                checks=False, harness=False, no_lid=False, no_cache=False, cache_stats=False, jobs=None)
    return SimpleNamespace(**{**base, **kw})


def main(paths):
    rows = []
    for p in paths:
        t0 = time.time()
        try:
            sp, ok = one(Path(p))
            rows.append(f"{'PASS' if ok else 'FAIL'} {sp} ({time.time() - t0:.0f}s)")
        except Exception as e:  # noqa: BLE001  (keep going through a batch)
            rows.append(f"ERROR {p}: {e}")
    print("\n".join(["looks summary:"] + rows))
    return 0 if all(r.startswith("PASS") for r in rows) else 1


def add_cli(sub):
    p = sub.add_parser("looks", help="kit -> renders (iso, top) -> likeness -> diff-photo, for one or many robots")
    p.add_argument("paths", nargs="+", help="spec.json or kit.json files")
    p.set_defaults(func=lambda a: main(a.paths))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
