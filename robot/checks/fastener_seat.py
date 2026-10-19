"""Fastener seats (`fastener_seat.*`): the head and thread of every screw match the hole cut for it.

Uses robot.cad.seat probes. A fastener carrying a `hole` record (written by robot.cad.holes.FastenerRecord.to_spec)
is held to that record (BLOCKER on mismatch); others get the defaults of their head type (WARNING): a countersunk
head must be flush, no head may sit inside material, every head must bear on something.
"""

from __future__ import annotations

import numpy as np

from ..cad import seat
from ..finding import BLOCKER, WARNING, fail, ok

G = "fastener_seat"


def _inside_any(bodies):
    def f(P):
        P = np.atleast_2d(P)
        out = np.zeros(len(P), bool)
        for b in bodies:
            out |= b.inside(P)
        return out
    return f


def run(ctx):
    r, w = ctx.r, ctx.world
    parts = [b for b in w.bodies if not b.fastener and not b.is_wire]
    out, n = [], 0
    for f in r.spec.fasteners:
        try:
            hb = [w.body(x) for x in (f.through or []) if w.body(x) is not None]
            tb = w.body(f.threads_into) if f.threads_into else None
            host = _inside_any(hb or [b for b in parts if b is not tb] or parts)
            m = seat.probe(f, host, tb.inside if tb is not None else None)
        except ValueError as e:
            ctx.not_checked.append(f"Fastener `{f.id}` seat: {e}")
            continue
        n += 1
        for cid, good, rec, msg in seat.judge(f, m):
            if good:
                continue
            out.append(fail(f"fastener_seat.{cid}", G, BLOCKER if rec else WARNING, "Screw does not fit its hole", msg)
                       .on(f.id, *[x for x in [*(f.through or []), f.threads_into] if x]).here(f.at)
                       .fix("Cut the hole with robot.cad.holes.hole(...) and use its FastenerRecord for this fastener."))
    if n and not out:
        out.append(ok("fastener_seat.ok", G, "Screw heads and threads fit their holes", f"{n} fasteners probed."))
    return out
