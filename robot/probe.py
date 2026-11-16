"""`robot probe`: measured facts about a placed robot, so an LLM looks numbers up instead of deriving them.

    python3 -m robot probe spec.json                     every part: world box, volume, mass, contacts
    python3 -m robot probe spec.json battery             one part: box, ports in world, gap to each neighbour
    python3 -m robot probe spec.json --joint flipper     sweep a joint over its range (others at default, exactly
                                                          as the verifier does): closest approach per other part
    python3 -m robot probe spec.json --at 1.3,0,33.1     what is at / near a world point

All numbers come from the same meshes the verifier uses (fast tessellation unless --fine).
"""

from __future__ import annotations

import json

import numpy as np

NEAR_MM = 3.0


def _load(spec_path, fine=False):
    from . import spec as spec_mod, world as world_mod

    s = spec_mod.load(spec_path)
    r = world_mod.resolve(s, fast=not fine)
    return s, r, world_mod.World.start(r)


def _fmt_box(b):
    lo, hi = b
    return f"x {lo[0]:.2f}..{hi[0]:.2f}  y {lo[1]:.2f}..{hi[1]:.2f}  z {lo[2]:.2f}..{hi[2]:.2f}"


def neighbours(w, body, r, near=NEAR_MM):
    """[(other id, gap mm (0 = touching), overlap depth mm)] for bodies within `near`."""
    from . import measure
    from .checks.interference import allowed_depth

    out = []
    for o in w.bodies:
        if o.id == body.id or o.is_wire or not measure.aabb_overlap(body.aabb, o.aabb, near):
            continue
        ov = measure.overlap(body, o)
        if ov is not None and ov.depth > 1e-4:
            out.append((o.id, 0.0, float(ov.depth), allowed_depth(r, body, o)))
            continue
        g = measure.min_gap(body, o, near)
        if np.isfinite(g):
            out.append((o.id, float(g), 0.0, allowed_depth(r, body, o)))
    return sorted(out, key=lambda t: (t[1], -t[2]))


def part_report(s, r, w, pid):
    b = w.body(pid)
    if b is None:
        return f"no part `{pid}`; parts: {', '.join(x.id for x in w.bodies)}"
    lines = [f"{pid}: {_fmt_box(b.aabb)}  size {' x '.join(f'{v:.2f}' for v in b.aabb[1] - b.aabb[0])} mm",
             f"  centre ({', '.join(f'{v:.2f}' for v in b.center)}), volume {b.geom.volume:.1f} mm3"]
    if b.part_idx is not None:
        rp = r.parts[b.part_idx]
        ports = dict(rp.cat.ports) if rp.cat is not None else {}
        ports.update(rp.part.ports or {})
        for name in sorted(ports):
            p = w.port(r, f"{pid}.{name}")
            if p is not None:
                lines.append(f"  port {name}: ({', '.join(f'{v:.2f}' for v in p)})")
        if rp.part.joint is not None:
            j = rp.part.joint
            lines.append(f"  joint {j.kind} axis {j.axis} pivot {j.pivot} range {j.min}..{j.max} default {j.default}")
        if rp.part.parent:
            lines.append(f"  parent {rp.part.parent} (moves with it)")
    for oid, gap, depth, allow in neighbours(w, b, r):
        if depth > 0:
            tag = "OVERLAP" if depth > allow else "overlap allowed"
            lines.append(f"  {tag} `{oid}` {depth:.2f} mm (allowed {allow:.2f})")
        else:
            lines.append(f"  gap to `{oid}` {gap:.2f} mm" + (" (touching)" if gap < 1e-3 else ""))
    return "\n".join(lines)


def joint_sweep(s, r, jid, n=24):
    """Closest approach of the joint's moving set to every other body over the joint range."""
    from . import measure, world as world_mod
    from .checks.interference import allowed_depth, descendants

    p = next((x for x in s.parts if x.id == jid), None)
    if p is None or p.joint is None:
        return f"`{jid}` has no joint"
    j = p.joint
    moving = descendants(r, jid)
    best = {}
    for k in range(n + 1):
        v = j.min + (j.max - j.min) * k / n
        w = world_mod.World.build(r, {jid: v})
        for a in w.bodies:
            if a.id not in moving:
                continue
            for o in w.bodies:
                if o.id in moving or o.is_wire or not measure.aabb_overlap(a.aabb, o.aabb, NEAR_MM):
                    continue
                ov = measure.overlap(a, o)
                if ov is not None and ov.depth > 1e-4:
                    m = -float(ov.depth)
                else:
                    g = measure.min_gap(a, o, NEAR_MM)
                    if not np.isfinite(g):
                        continue
                    m = float(g)
                if o.id not in best or m < best[o.id][0]:
                    best[o.id] = (m, v, a.id, allowed_depth(r, a, o))
    lines = [f"joint `{jid}` {j.kind} {j.min}..{j.max} ({n + 1} poses), moving: {', '.join(sorted(moving))}"]
    if not best:
        lines.append(f"  nothing comes within {NEAR_MM} mm")
    for oid, (m, v, aid, allow) in sorted(best.items(), key=lambda t: t[1][0]):
        what = f"HITS {-m:.2f} mm deep" if m < -allow else (f"overlap {-m:.2f} mm (allowed)" if m < 0 else f"closest {m:.2f} mm")
        lines.append(f"  `{oid}` vs `{aid}`: {what} at {v:.1f}")
    return "\n".join(lines)


def point_report(w, P):
    P = np.asarray(P, float)
    rows = []
    for b in w.bodies:
        if b.is_wire:
            continue
        lo, hi = b.aabb
        if np.all(P >= lo - NEAR_MM) and np.all(P <= hi + NEAR_MM):
            d = float(b.sdf(P[None])[0])
            rows.append((d, b.id))
    rows.sort()
    return "\n".join([f"point ({', '.join(f'{v:.2f}' for v in P)}):"] +
                     [f"  {'inside' if d < 0 else 'from'} `{i}` {abs(d):.2f} mm" for d, i in rows] or ["  nothing near"])


def mass_report(s, r, w):
    """Mass per part (same rules as the mass check), biggest first, plus parts that look like solid blocks."""
    from .checks import Ctx, Options
    from .checks import mass as mass_chk

    ctx = Ctx(r, w, Options(fast=True))
    fs = mass_chk.run(ctx)
    rows = sorted(((k.split(".", 1)[1], v) for k, v in ctx.metrics.items() if k.startswith("part_mass_g.")), key=lambda t: -t[1])
    total = ctx.metrics.get("mass_total_g", sum(v for _, v in rows))
    limit = ctx.metrics.get("mass_limit_g", 150)
    lines = [f"mass {total:.1f} g of {limit:.0f} g ({limit - total:+.1f} g margin)"]
    for pid, g in rows:
        b = w.body(pid)
        fill = ""
        if b is not None:
            bv = float(np.prod(b.aabb[1] - b.aabb[0]))
            frac = b.geom.volume / bv if bv > 0 else 0
            fill = f"  fills {frac:.0%} of its box" + ("  <- solid block? a tub should be a shell" if frac > 0.55 and g > 15 else "")
        lines.append(f"  {pid:<24} {g:7.2f} g{fill}")
    lines += [f"  {f.id}: {f.message}" for f in fs if not f.passed]
    return "\n".join(lines)


def overview(s, r, w):
    out = []
    for b in w.bodies:
        if b.is_wire:
            continue
        out.append(f"{b.id:<24} {_fmt_box(b.aabb)}  vol {b.geom.volume:8.1f} mm3")
    return "\n".join(out)


def add_cli(sub):
    p = sub.add_parser("probe", help="measured boxes, ports, gaps and joint sweeps (look numbers up, don't derive them)")
    p.add_argument("spec")
    p.add_argument("part", nargs="?")
    p.add_argument("--joint", help="sweep this part's joint over its range")
    p.add_argument("--at", help="x,y,z world point: which parts contain / are near it")
    p.add_argument("--mass", action="store_true", help="mass budget per part (flags solid blocks)")
    p.add_argument("--fine", action="store_true")
    p.add_argument("--json", action="store_true", help="(overview) JSON boxes")
    p.set_defaults(func=_cli)


def _cli(a):
    s, r, w = _load(a.spec, a.fine)
    if a.mass:
        print(mass_report(s, r, w))
    elif a.joint:
        print(joint_sweep(s, r, a.joint))
    elif a.at:
        print(point_report(w, [float(v) for v in a.at.split(",")]))
    elif a.part:
        print(part_report(s, r, w, a.part))
    elif a.json:
        print(json.dumps({b.id: [list(map(float, b.aabb[0])), list(map(float, b.aabb[1]))] for b in w.bodies}, indent=1))
    else:
        print(overview(s, r, w))
    return 0
