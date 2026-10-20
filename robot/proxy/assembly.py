"""Fast proxy for `assembly`: replay the take-apart order of the last full run instead of searching for one.

The full group tries every present part along every axis, repeatedly, until nothing more leaves (O(n^2 * dirs)
slides). Here each baseline step (report.json `assembly`: id, dir) is one slide of that part's group along its
recorded direction, in the recorded order, with the same collision test (assembly.slide). A step that now hits, or a
part with no baseline step, flags `proxy.assembly`; the full sweep might still find another way out (false alarm).
Steps of a declared module's bench teardown restart from that module's parts alone, as the full group does.
"""

from __future__ import annotations

import numpy as np

from ..checks import assembly as asm
from ..finding import BLOCKER, fail, ok

G = "proxy"


def _module_of(spec, pid):
    for m in (spec.raw or {}).get("modules") or []:
        if pid == m.get("root") or pid in (m.get("parts") or []):
            return m
    return None


def _bench(ctx, m):
    w, n = ctx.world, len(ctx.world.bodies)
    rk = w.index(m.get("root"))
    ids = {rk} | {k for k in (w.index(x) for x in m.get("parts") or []) if k is not None}
    ids |= set(asm.group(ctx, m["root"], [True] * n))
    return [k in ids and not w.bodies[k].is_wire for k in range(n)], rk


def replay(ctx, steps):
    """[(part id, reason)] for every step that is blocked now, plus parts the baseline never took off."""
    w = ctx.world
    n = len(w.bodies)
    present = [not b.is_wire for b in w.bodies]
    rootp = next((p for p in ctx.r.spec.parts if p.kind == "structure"), None)
    root = w.index(rootp.id) if rootp else None
    bad, seen, bench = [], set(), None
    restore = asm.apply_service_pose(ctx)
    try:
        for s in steps:
            i = w.index(s["id"])
            if i is None:
                continue
            seen.add(i)
            if not present[i]:
                m = _module_of(ctx.r.spec, s["id"])
                if m is None or bench == m.get("id"):
                    continue
                restore()
                restore = lambda: None  # noqa: E731 - the service pose holds for the full-robot teardown only
                present, root = _bench(ctx, m)
                bench = m.get("id")
                if not present[i]:
                    continue
            d = np.asarray(s.get("dir") or [0, 0, 0], float)
            if not np.linalg.norm(d):  # stretched off (elastic), no slide
                present[i] = False
                continue
            b = w.bodies[i]
            members = [i] if b.fastener else [k for k in asm.group(ctx, b.id, present) if present[k]]
            res = asm.slide(ctx, members, present, d / np.linalg.norm(d))
            if res[0] != "ok":
                bad.append((b.id, f"its recorded way out ({', '.join(f'{x:.0f}' for x in d)}) now hits `{w.bodies[res[1]].id}` after {res[2]:.1f} mm"))
            for k in members:
                present[k] = False
    finally:
        restore()
    for k, b in enumerate(w.bodies):
        if k not in seen and k != w.index(rootp.id if rootp else None) and not b.is_wire:
            bad.append((b.id, "the baseline teardown never took it off"))
    return bad


def run(ctx, steps, parts=None):
    """`parts` is accepted for a uniform interface but not applied: moving one part can trap any other."""
    if not steps:
        return [fail("proxy.assembly", G, BLOCKER, "No baseline teardown to replay",
                     "Pass a full report (with `assembly` steps) as the baseline.")]
    out = []
    for pid, why in replay(ctx, steps):
        out.append(fail("proxy.assembly", G, BLOCKER, "Part likely cannot be assembled", f"`{pid}`: {why}.").on(pid)
                   .fix("Run the full `assembly` group to search other ways out."))
    if not out:
        out.append(ok("proxy.assembly", G, "Baseline teardown order still works", f"{len(steps)} recorded slides replayed clear."))
    return out
