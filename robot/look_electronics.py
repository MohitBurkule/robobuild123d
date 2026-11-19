"""`robot electronics SPEC [--kinds battery,esc,receiver] [--face +z] [--lip 2] [--only id,..] [--dry]`: windows that
show the real battery / ESC / receiver where the photo shows them through an open top.

WHY: the photo review keeps reporting "photo shows the battery / ESC / wires through the open top; model is a closed
box". The parts are already in the spec (catalog battery, esc, receiver and routed wires); they are only hidden.

For each such component it looks straight out along `--face` (rays over the component's footprint) and lists the
static printed parts that cover it (a tub's deck, then a `top_plate` ...). It cuts one box through all of them: the
component's footprint shrunk by `--lip` on every side (the rim keeps the component captive and the outline intact),
from 0.3 mm off the component to past the outermost cover. A component is skipped, with the reason, when a moving
part, a bought part, a screw or any other body lies in that box, or when it is smaller than the rim allows.
After a run, run `robot verify` and `robot compare`: keep the window only when blockers do not rise and likeness
does not drop.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

KINDS = ("battery", "esc", "receiver")
AX = {"x": 0, "y": 1, "z": 2}


def covers(Bd, raw, comp, face="+z"):
    """Ids of the static printed parts over `comp` along `face`, nearest first."""
    k = AX[face[1]]
    s = -1.0 if face[0] == "-" else 1.0
    lo, hi = Bd[comp].aabb
    u, v = [i for i in range(3) if i != k]
    us = np.linspace(lo[u] + 1, hi[u] - 1, 5)
    vs = np.linspace(lo[v] + 1, hi[v] - 1, 5)
    O = np.zeros((25, 3))
    O[:, u] = np.repeat(us, 5)
    O[:, v] = np.tile(vs, 5)
    O[:, k] = (hi[k] + 0.05) if s > 0 else (lo[k] - 0.05)
    D = np.zeros_like(O)
    D[:, k] = s
    byid = {p["id"]: p for p in raw["parts"]}
    dist = {}
    for bid, b in Bd.items():
        if bid == comp or getattr(b, "fastener", False) or getattr(b, "is_wire", False):
            continue
        blo, bhi = b.aabb
        if np.any(blo[[u, v]] > hi[[u, v]]) or np.any(bhi[[u, v]] < lo[[u, v]]):
            continue
        if (s > 0 and bhi[k] < hi[k]) or (s < 0 and blo[k] > lo[k]):
            continue
        loc, ri, _ = b.mesh.ray.intersects_location(O, D, multiple_hits=False)
        if len(loc):
            dist[bid] = float(np.min((loc[:, k] - O[0, k]) * s))
    out = sorted(dist, key=dist.get)
    bad = [i for i in out if "catalog" in byid.get(i, {}) or "shape" not in byid.get(i, {})
           or byid[i].get("joint") or byid[i].get("parent") or byid[i].get("rotates_with")]
    return out, bad


def window_through(raw, Bd, comp, parts, face="+z", lip=2.0):
    """Cut one box over `comp` (its footprint less `lip`) through every part in `parts`. Returns (mm2, notes)."""
    from .look_outline import E, _add_cut, _grid, _local_place

    k = AX[face[1]]
    s = -1.0 if face[0] == "-" else 1.0
    clo, chi = Bd[comp].aabb
    lo, hi = clo.copy(), chi.copy()
    for j in range(3):
        if j != k:
            lo[j] += lip
            hi[j] -= lip
    if np.any(np.delete(hi - lo, k) <= 1.0):
        return 0, f"too small for a {lip:g} mm rim"
    far = max(Bd[q].aabb[1][k] for q in parts) + E if s > 0 else min(Bd[q].aabb[0][k] for q in parts) - E
    if s > 0:
        lo[k], hi[k] = chi[k] + 0.3, far
    else:
        lo[k], hi[k] = far, clo[k] - 0.3
    G = _grid(lo, hi, 0.7)
    hit = sorted({b.id for i, b in Bd.items() if i != comp and i not in parts and not getattr(b, "is_wire", False)
                  and b.inside(G).any()})
    if hit:
        return 0, f"{hit} lie in the window (screws, moving or bought parts)"
    byid = {q["id"]: q for q in raw["parts"]}
    for q in parts:
        if not Bd[q].inside(G).any():
            continue
        box = {"type": "box", "size": [round(float(v), 3) for v in hi - lo]}
        _add_cut(byid[q], _local_place(byid[q], box, np.eye(3), (lo + hi) / 2))
    return float(np.prod(np.delete(hi - lo, k))), None


def run(path, kinds=KINDS, face="+z", lip=2.0, only=None, dry=False):
    from . import spec as spec_mod
    from . import world as world_mod

    p = Path(path)
    txt = p.read_text()
    raw = json.loads(txt)
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(path), fast=True))
    Bd = {b.id: b for b in w.bodies}
    comps = [q["id"] for q in raw["parts"] if q.get("kind") in kinds and q["id"] in Bd and (not only or q["id"] in only)]
    done, notes = [], []
    for c in comps:
        out, bad = covers(Bd, raw, c, face)
        if not out:
            notes.append(f"{c}: already open on {face}")
            continue
        if bad:
            notes.append(f"{c}: {bad} lie over it (not static prints)")
            continue
        area, why = window_through(raw, Bd, c, out, face, lip)
        if why:
            notes.append(f"{c}: {why}")
            continue
        done.append(f"{c}: {area:.0f} mm2 window through {', '.join(out)} on {face}, rim {lip:g} mm")
    if done and not dry:
        ind = 1 if txt.startswith("{\n ") and not txt.startswith("{\n  ") else 2
        p.write_text(json.dumps(raw, indent=ind) + "\n")
    return done, notes


def main(a):
    kinds = tuple(a.kinds.split(","))
    only = set(a.only.split(",")) if a.only else None
    done, notes = run(a.spec, kinds, a.face, a.lip, only, a.dry)
    for n in notes:
        print("  skipped " + n)
    for d in done:
        print(("would cut " if a.dry else "") + d)
    print(f"{len(done)} window(s){' (dry run)' if a.dry else ''}")
    return 0 if done else 1


def add_cli(sub):
    p = sub.add_parser("electronics", help="see-through windows over the battery / ESC / receiver (photo shows them)")
    p.add_argument("spec")
    p.add_argument("--kinds", default=",".join(KINDS), help="part kinds to show (comma separated)")
    p.add_argument("--face", default="+z")
    p.add_argument("--lip", type=float, default=2.0, help="rim kept on every side so the component stays captive")
    p.add_argument("--only", help="only these component ids (comma separated)")
    p.add_argument("--dry", action="store_true")
    p.set_defaults(func=main)
