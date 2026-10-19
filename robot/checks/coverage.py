"""Coverage sweep: which check groups evaluate each part kind and each part pair in contact/proximity.

Per-kind coverage is read from the check sources (a group covers a kind when its module names that kind; a few groups
evaluate every part). Pair coverage asks for a declared relation that some check verifies: a screw through both, a
declared connection, allow_overlap, parent/fused, a captive (pocket) relation, a belt over a pulley, or a shared joint.
Anything with no applicable check is listed in `coverage.uncovered` (WARNING) so gaps stay visible, and the generic
invariants below run on it.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from .. import catalog, measure
from ..finding import WARNING, fail, ok

G = "coverage"
UNIVERSAL = {"validity", "mass", "interference", "internal", "connections", "material", "plausibility"}
PROX_MM = 0.5
MADE_EXEMPT = {"motor", "weapon_motor", "esc", "receiver", "battery", "switch", "servo", "bearing", "insert", "nut", "belt", "tyre"}


@lru_cache(maxsize=1)
def kind_map():
    from . import GROUPS
    here = Path(__file__).parent
    m = {}
    for name, _ in GROUPS:
        f = here / f"{name}.py"
        if name in ("coverage",) or not f.exists():
            continue
        m[name] = set(re.findall(r'"([a-z_]+)"', f.read_text()))
    return m


def matrix(r):
    km = kind_map()
    kinds = {p.kind for p in r.spec.parts}
    return {k: sorted(UNIVERSAL | {g for g, words in km.items() if k in words}) for k in kinds}


def _related(r, a, b, captive):
    sp = r.spec
    pa, pb = sp.part(a), sp.part(b)
    if pa.parent == b or pb.parent == a or pa.fused_with == b or pb.fused_with == a or pa.cover == b or pb.cover == a:
        return True
    for f in sp.fasteners:
        held = set(f.through or []) | ({f.threads_into} if f.threads_into else set())
        for h in list(held):
            hp = sp.part(h)
            if hp is not None and hp.kind in ("insert", "nut"):
                held |= set(captive.get(h, ())) | ({hp.parent} if hp.parent else set())
        if {a, b} <= held:
            return True
    if any({c.a, c.b} == {a, b} for c in sp.connections) or any({x.a, x.b} == {a, b} for x in sp.allow_overlap):
        return True
    if b in captive.get(a, ()) or a in captive.get(b, ()):
        return True
    for p, q in ((pa, pb), (pb, pa)):
        if p.belt is not None and q.id in (p.belt.pulleys or []):
            return True
        if p.tyre_of == q.id or p.actuated_by == q.id or (p.rotates_with and p.rotates_with in (q.id, q.rotates_with)):
            return True
        if p.retained and q.kind in ("structure", "armor", "plate", "wedge", "tub"):
            return True
    return False


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    mx = matrix(r)
    ctx.metrics["coverage.kinds"] = mx
    unc = []
    # per-part invariants
    for p in r.spec.parts:
        if p.kind not in MADE_EXEMPT and not p.catalog and (not p.material or not p.process):
            unc.append(f"part `{p.id}`: made part with no {'material' if not p.material else 'process'}")
        jointed = {q.id for q in r.spec.parts if q.joint is not None}
        if (p.joint is not None or p.rotates_with in jointed) and p.kind not in ("wheel", "weapon", "pulley", "shaft", "weapon_motor", "motor", "tyre", "belt"):
            unc.append(f"part `{p.id}` ({p.kind}): rotates but no balance/clearance check knows its kind")
    for k, groups in mx.items():
        if set(groups) <= UNIVERSAL:
            unc.append(f"kind `{k}`: only generic checks apply ({', '.join(groups)})")
    # pairs in contact / proximity
    bodies = [b for b in w.bodies if b.part_idx is not None]
    n_pairs = 0
    for i, a in enumerate(bodies):
        for b in bodies[i + 1:]:
            if not measure.aabb_overlap(a.aabb, b.aabb, PROX_MM):
                continue
            try:
                gap = measure.min_gap(a, b, PROX_MM + 0.5)
            except Exception:  # noqa: BLE001
                gap = 0.0
            if gap > PROX_MM:
                continue
            n_pairs += 1
            if not _related(r, a.id, b.id, ctx.captive):
                unc.append(f"pair `{a.id}`/`{b.id}` ({gap:.2f} mm): touching with no declared joint, connection or allowed contact")
    ctx.metrics["coverage.pairs"] = n_pairs
    ctx.metrics["coverage.uncovered"] = len(unc)
    if unc:
        out.append(fail("coverage.uncovered", G, WARNING, "Parts or contacts no specific check covers",
                        f"{len(unc)} gap(s): " + "; ".join(unc[:40]) + (" ..." if len(unc) > 40 else ""))
                   .fix("Declare the relation (fastener, `connections`, `allow_overlap`, `retained`) or the material/process, so a check can verify it."))
    else:
        out.append(ok("coverage.uncovered", G, "Every part and contact is covered", f"{len(r.spec.parts)} parts, {n_pairs} contact pairs, all with an applicable check."))
    return out
