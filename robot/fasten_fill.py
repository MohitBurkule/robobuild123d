"""`robot fasteners SPEC --fill`: write a measured `hole` record for every fastener that has none.

grip = how far the screw runs inside its `through` parts from its bearing point `at` along `dir` (ray sampled on
the built geometry), so the record matches the model instead of a guess. `into` comes from what it threads into
(insert / nut part -> insert / nut, printed host -> tapped, nothing -> through). Head from the fastener's `head`
(socket/None -> cap, countersunk -> csk, button). Uses robot.cad.holes.hole_plan, the same rule set the seat check
uses, so the record and the check agree. Prints each record; --fill writes them back into the spec.
"""

from __future__ import annotations

import json

import numpy as np

HEAD = {None: "cap", "socket": "cap", "cap": "cap", "countersunk": "csk", "csk": "csk", "button": "button"}


def measure_grip(world, f, step=0.05) -> float:
    at, d = np.asarray(f.at, float), np.asarray(f.dir, float)
    d = d / np.linalg.norm(d)
    bodies = [world.body(t) for t in (f.through or []) if world.index(t) is not None]
    if not bodies:
        return 0.0
    from .catalog import parse_designation
    dl = parse_designation(f.designation)
    L = dl[1] if dl else 20.0
    # sample a ring just outside the clearance hole (the hole itself is empty), under the head
    r = (dl[0] if dl else 2.0) * 0.5 + 0.6
    u = np.cross(d, [1.0, 0, 0] if abs(d[0]) < 0.9 else [0, 1.0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    ang = np.linspace(0, 2 * np.pi, 8, endpoint=False)
    ring = r * (np.cos(ang)[:, None] * u + np.sin(ang)[:, None] * v)
    s = np.arange(step / 2, L + step, step)
    P = (at[None, None, :] + s[:, None, None] * d[None, None, :] + ring[None, :, :]).reshape(-1, 3)
    hit = np.zeros(len(P), bool)
    for b in bodies:
        hit |= b.inside(P)
    ins = hit.reshape(len(s), len(ang)).mean(axis=1) >= 0.5
    if f.threads_into and world.index(f.threads_into) is not None:  # clamp stops where the insert / nut / host starts
        C = (at[None, :] + s[:, None] * d[None, :])
        tb = world.body(f.threads_into)
        rw = (dl[0] if dl else 2.0) * 0.65  # inside an insert / nut wall, outside the thread
        Q = (C[:, None, :] + ring[None, :, :] * (rw / r)).reshape(-1, 3)
        host = tb.inside(C) | tb.inside(Q).reshape(len(s), len(ang)).any(axis=1)
        if host.any():
            ins &= s < s[np.nonzero(host)[0].min()]
    if not ins.any():
        return 0.0
    return float(round(s[np.nonzero(ins)[0].max()] + step / 2, 2))


def insert_len(world, f, step=0.05):
    """Length of the modelled insert body along the screw axis (None when not modelled)."""
    if not f.threads_into or world.index(f.threads_into) is None:
        return None
    b = world.body(f.threads_into)
    d = np.asarray(f.dir, float)
    d = d / np.linalg.norm(d)
    ext = b.mesh.vertices @ d
    return float(round(ext.max() - ext.min(), 2))


def _probe(world, f, hole):
    from types import SimpleNamespace
    from .cad import seat
    from .checks.fastener_seat import _inside_any
    parts = [b for b in world.bodies if not b.fastener and not b.is_wire]
    hb = [world.body(x) for x in (f.through or []) if world.index(x) is not None]
    if not hb:
        return None
    g = SimpleNamespace(**{k: getattr(f, k, None) for k in ("id", "designation", "at", "dir", "through", "threads_into", "head")})
    g.hole = hole
    try:
        return seat.probe(g, _inside_any(hb), _inside_any([b for b in parts if b.kind != "insert"]))
    except Exception:  # noqa: BLE001 - a probe failure just means "no measured counterbore"
        return None


def plan(spec, world):
    from .cad.holes import hole_plan
    out = {}
    for f in spec.fasteners:
        if getattr(f, "hole", None):
            continue
        host = spec.part(f.threads_into) if f.threads_into else None
        kind = getattr(host, "kind", None)
        into = {"insert": "insert", "nut": "nut"}.get(kind, "tapped" if host is not None else "through")
        head = HEAD.get(getattr(f, "head", None), "cap")
        grip = measure_grip(world, f)
        side = "both"  # record the thread side too (insert_d / insert_len, tap_d, nut pocket): the seat check needs it
        _, rec = hole_plan((0, 0, 0), f.dir, fastener=f.designation, head=head, into=into, grip=grip, side=side, cbore=0.0)
        if head != "csk":  # measure how deep the head sits below the outer surface (the counterbore the part really has)
            m = _probe(world, f, rec.hole)
            cb = m.get("cbore_depth") if m else None
            if cb is not None and cb > 0.05:
                # grip counts from the OUTER surface (hole_plan frame), the measured run started at the head face
                _, rec = hole_plan((0, 0, 0), f.dir, fastener=f.designation, head=head, into=into,
                                   grip=round(grip + float(cb), 2), side=side, cbore=round(float(cb), 2))
        h = dict(rec.hole)
        il = insert_len(world, f) if into == "insert" else None
        if il:  # the modelled insert's real length (catalog inserts differ: 3 vs 4 mm), so the bore check matches it
            h["insert_len"] = il
            h["insert_depth"] = round(il + 0.3, 4)
        out[f.id] = h
    return out


def main(path, fill=False):
    from . import spec as spec_mod, world as world_mod
    spec = spec_mod.load(path)
    r = world_mod.resolve(spec, fast=True)
    w = world_mod.World.build(r)
    recs = plan(spec, w)
    for k, v in recs.items():
        print(k, json.dumps(v))
    if fill and recs:
        raw = json.load(open(path))
        for f in raw.get("fasteners", []):
            if f.get("id") in recs:
                f["hole"] = recs[f["id"]]
        json.dump(raw, open(path, "w"), indent=1)
        print(f"wrote {len(recs)} hole records into {path}")
    if not recs:
        print("every fastener already has a hole record")
    return 0


def add_cli(sub):
    p = sub.add_parser("fasteners", help="measure + write missing fastener `hole` records (grip from the geometry)")
    p.add_argument("spec")
    p.add_argument("--fill", action="store_true", help="write the records into the spec (else just print them)")
    p.set_defaults(func=lambda a: main(a.spec, a.fill))
