"""Fast proxies for the slow check groups: a fixer checks a change in seconds before the full run.

`python3 -m robot verify SPEC --proxy [--parts a,b] [--baseline report.json] [--only reference_cad,...]`

  group          proxy (module)                                           full group it stands in for
  reference_cad  refcad: fingerprint checks + sliced section outlines     boolean diff, features, silhouette raster
  interference   interference: AABB pre-pass, depth bound, revolved hull  inscribed depth, 3-degree joint sweeps
  assembly       assembly: replay the baseline teardown order             greedy take-apart search
  wiring         wiring: replay baseline routes, point-to-surface bands   voxel grid + A* per wire

Every proxy is conservative: it flags whatever the full group would likely flag (false alarms are fine, misses are
not). Assembly and wiring replay the last full run's report (`assembly`, `routes`); the baseline given with
`--baseline` is stored in the cache (BASELINE_NAME) so later runs find it on their own.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

GROUPS = ("reference_cad", "interference", "assembly", "wiring")
BASELINE_NAME = "baseline_{name}.json"


def baseline_path(spec_name: str) -> Path:
    from ..geom import cache_dir

    return cache_dir() / "proxy" / BASELINE_NAME.format(name=spec_name)


def load_baseline(spec_name: str, path=None) -> dict:
    """{routes, assembly} from a full report (stored for later runs), else the stored one, else empty."""
    keep = baseline_path(spec_name)
    if path:
        d = json.loads(Path(path).read_text())
        b = {k: d.get(k) or [] for k in ("routes", "assembly")}
        if keep.is_file():  # a report from one group only keeps the other group's stored baseline
            old = json.loads(keep.read_text())
            b = {k: b[k] or old.get(k) or [] for k in b}
        keep.parent.mkdir(parents=True, exist_ok=True)
        keep.write_text(json.dumps(b))
        return b
    return json.loads(keep.read_text()) if keep.is_file() else {"routes": [], "assembly": []}


def run(ctx, groups=GROUPS, parts=None, baseline=None):
    """Findings of the selected proxies, and seconds per proxy."""
    from . import assembly, interference, refcad, wiring

    baseline = baseline or {}
    fns = {"reference_cad": lambda: refcad.run(ctx, parts),
           "interference": lambda: interference.run(ctx, parts),
           "assembly": lambda: assembly.run(ctx, baseline.get("assembly"), parts),
           "wiring": lambda: wiring.run(ctx, baseline.get("routes"), parts)}
    out, timings = [], {}
    for g in groups:
        t0 = time.time()
        out += fns[g]()
        timings[f"proxy.{g}"] = round(time.time() - t0, 3)
    return out, timings
