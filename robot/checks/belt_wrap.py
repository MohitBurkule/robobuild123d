"""cots.belt_wrap: an O-ring (or any round) belt must be modelled as a closed loop that wraps both pulleys, not a flat
strip between them. The belt solid must be one ring (Euler number 0: a torus-like loop), and from each pulley centre,
in the pulley plane, the belt must lie on both sides of the centre line (top and bottom runs), within the pulley radius
plus `review.belt.wrap_tol_mm` (default 2). The runs are looked for in the belt's own plane
(a groove sits off the hub's mid-plane).
"""

from __future__ import annotations

import numpy as np

from .. import xform
from ..finding import BLOCKER, fail, ok
from ._review import params

G = "belt_wrap"
DEFAULTS = {"wrap_tol_mm": 2.0}
ROUND = ("o_ring", "round", "oring")


def _axis(b, part):
    if part.joint is not None and part.joint.axis is not None:
        a = xform.apply_dir(b.M, np.asarray(part.joint.axis, float))
    else:
        a = np.zeros(3)
        a[int(np.argmin(np.ptp(b.mesh.bounds, axis=0)))] = 1.0
    return a / np.linalg.norm(a)


def wraps(belt_b, pulleys, tol):
    """List of problems (empty when the belt wraps every pulley)."""
    probs = []
    m = belt_b.mesh
    if m.body_count != 1 or m.euler_number != 0:
        probs.append(f"the belt solid is not one closed loop (Euler number {m.euler_number}, {m.body_count} bodies): a strip, not a ring")
    cs = [pb.mesh.bounds.mean(axis=0) for pb, _ in pulleys]
    for k, (pb, part) in enumerate(pulleys):
        ax = _axis(pb, part)
        c = cs[k]
        c = c - ((c - belt_b.mesh.bounds.mean(axis=0)) @ ax) * ax   # a groove sits off the hub's mid-plane: look in the belt's own plane
        other = cs[1 - k] if len(cs) > 1 else c + np.cross(ax, [0, 0, 1.0])
        line = other - c
        line -= (line @ ax) * ax
        n = np.cross(ax, line)
        n /= max(np.linalg.norm(n), 1e-9)
        q = pb.mesh.vertices - c
        rad = float(np.linalg.norm(q - np.outer(q @ ax, ax), axis=1).max())
        for sgn, side in ((1, "one side"), (-1, "the other side")):
            s = np.linspace(0, rad + tol, 40)
            P = c + sgn * np.outer(s, n)
            if float(np.abs(belt_b.distance(P)).min()) > 0.3 and not belt_b.inside(P).any():
                probs.append(f"no belt run on {side} of `{part.id}` (within r{rad + tol:.1f} of its centre)")
    return probs


def run(ctx):
    r, w = ctx.r, ctx.world
    tol = float(params(r.spec, "belt", DEFAULTS)["wrap_tol_mm"])
    out, n = [], 0
    for rp in r.parts:
        p = rp.part
        if p.belt is None or str(p.belt.kind).lower() not in ROUND:
            continue
        bb = w.body(p.id)
        pul = [(w.body(i), r.spec.part(i)) for i in (p.belt.pulleys or [])]
        pul = [(b, q) for b, q in pul if b is not None and q is not None]
        if bb is None or len(pul) < 2:
            continue
        probs = wraps(bb, pul, tol)
        if probs:
            out.append(fail("cots.belt_wrap", G, BLOCKER, "O-ring belt does not wrap its pulleys",
                            f"`{p.id}`: " + "; ".join(probs) + ".").on(p.id, *[q.id for _, q in pul])
                       .fix("Model the O-ring as a closed loop (round section of the stock cs) tangent to both pulley grooves."))
        else:
            n += 1
    if n:
        out.append(ok("cots.belt_wrap", G, "Belts wrap their pulleys", f"{n} O-ring belt(s) are closed loops around both pulleys."))
    return out
