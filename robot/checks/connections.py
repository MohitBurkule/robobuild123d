"""Join graph: every part must be held to the chassis by a screw, a shared print, a pocket that captures it, a joint
or a stated connection, and each stated connection has to be believable for the load and the materials (port of connections.rs)."""

from __future__ import annotations

from collections import deque

import numpy as np

from .. import catalog, measure, xform
from ..finding import BLOCKER, WARNING, fail, note, ok

G = "connections"
METHODS = ["screw", "shaft", "pin", "press_fit", "glue", "tape", "snap", "interlock", "velcro", "none"]
LOW_ENERGY = {"hdpe", "pp", "polypropylene", "pe", "uhmwpe", "nylon", "pa12", "taulman910"}
IMPACT = {"wedge", "weapon", "armor", "fork", "locking_bar"}


def impact_part(p) -> bool:
    return p.kind in IMPACT


def is_low_energy(p) -> bool:
    return bool(p.material) and p.material.lower() in LOW_ENERGY


def _link(edges, a, b):
    edges.setdefault(a, set()).add(b)
    edges.setdefault(b, set()).add(a)


def run(ctx):
    r, w = ctx.r, ctx.world
    out, edges, floating_ok = [], {}, set()

    for f in r.spec.fasteners:
        ids = list(f.through) + ([f.threads_into] if f.threads_into else [])
        for a, b in zip(ids, ids[1:]):
            _link(edges, a, b)
    for p in r.spec.parts:
        if p.fused_with:
            fw = p.fused_with
            o = r.spec.part(fw)
            if o is not None and o.material == p.material and catalog.part_is_printed(p.process, p.material):
                _link(edges, p.id, fw)
            else:
                out.append(fail("connection.fused_mismatch", G, BLOCKER, "Fused parts are not one print",
                                f"`{p.id}` is fused to `{fw}` but they differ in material or are not both printed; they cannot be one piece.")
                           .on(p.id, fw).fix("Print both in one material, or declare screws instead of `fused_with`."))
        if p.tyre_of:
            _link(edges, p.id, p.tyre_of)
        if p.belt is not None:
            for pu in p.belt.pulleys:
                _link(edges, p.id, pu)
        if p.weapon is not None:
            for x in (p.weapon.motor, p.weapon.locking_bar):
                if x:
                    _link(edges, p.id, x)
        if p.joint is not None and p.parent:
            par = p.parent
            pb = w.body(par)
            pivot = xform.apply(pb.M, np.asarray(p.joint.pivot, float)) if pb is not None else None

            def near(bid):
                b = w.body(bid)
                return pivot is not None and b is not None and float(b.sdf(pivot)[0]) <= 1.0

            if near(p.id) and near(par):
                _link(edges, p.id, par)
            else:
                out.append(fail("connection.joint_pivot", G, BLOCKER, "Joint pivot is not on the parts",
                                f"`{p.id}` pivots about a point that is more than 1 mm from `{p.id}` or from `{par}`; nothing holds the pivot pin.")
                           .on(p.id, par).fix("Put the pivot on the pin that passes through both parts and add that pin as a part."))

    for c in r.spec.connections:
        pa, pb = r.spec.part(c.a), r.spec.part(c.b)
        if pa is None or pb is None:
            out.append(fail("connection.ref", G, BLOCKER, "Connection names a missing part", f"`{c.a}`-`{c.b}`.").on(c.a, c.b))
            continue
        if c.method not in METHODS:
            out.append(fail("connection.method", G, BLOCKER, "Unknown connection method",
                            f"`{c.a}`-`{c.b}` uses `{c.method}`; use one of {', '.join(METHODS)}.").on(c.a, c.b))
            continue
        reason = c.reason or ""
        if len(reason.strip()) < 30 or len(reason.split()) < 6:
            out.append(fail("connection.reason", G, BLOCKER, "Connection needs real reasoning",
                            f"`{c.a}`-`{c.b}` ({c.method}): the reason is too short to be an argument.").on(c.a, c.b)
                       .fix("Say what load the join carries, why this method suits the two materials, and how it is assembled."))
            continue
        m = c.method
        if m == "none":
            floating_ok.update([c.a, c.b])
            out.append(note("connection.free", G, "Parts deliberately unjoined", f"`{c.a}` and `{c.b}`: {reason}").on(c.a, c.b))
            continue
        if m == "screw":
            if c.b not in edges.get(c.a, set()):
                out.append(fail("connection.screw_missing", G, BLOCKER, "Declared screw join has no screw",
                                f"`{c.a}`-`{c.b}` says screw but no fastener passes through both.").on(c.a, c.b)
                           .fix("Add a fastener whose `through` or `threads_into` lists both parts."))
            continue
        if m in ("glue", "tape"):
            if impact_part(pa) or impact_part(pb):
                out.append(fail("connection.glue_on_impact", G, BLOCKER, "Adhesive on a part that takes hits",
                                f"`{c.a}`-`{c.b}` is held by {m} but one side is a wedge, weapon, armour or fork; hits peel adhesive on the first strike.")
                           .on(c.a, c.b).fix("Bolt it: add M2 screws into inserts, or an interlocking tab plus screws. Use glue only as a secondary."))
                continue
            if (is_low_energy(pa) or is_low_energy(pb)) and not c.mechanical_key:
                out.append(fail("connection.glue_low_energy", G, BLOCKER, "Glue will not stick to this plastic",
                                f"`{c.a}`-`{c.b}`: HDPE, polypropylene and nylon barely take adhesive or tape; set `mechanical_key` only if geometry holds it without the glue.")
                           .on(c.a, c.b).fix("Use screws, a press fit or an interlock, or add a keyed slot and set `mechanical_key`."))
                continue
        elif m == "press_fit":
            d = c.interference_mm
            if d is None or not (0.05 <= float(d) <= 0.4):
                out.append(fail("connection.press_fit_interference", G, WARNING, "Press fit has no sensible interference",
                                f"`{c.a}`-`{c.b}`: give `interference_mm` between 0.05 and 0.4 for a printed part.").on(c.a, c.b))
        _link(edges, c.a, c.b)

    for p in r.spec.parts:
        i = w.index(p.id)
        if i is None:
            continue
        for b in ctx.captive.get(p.id, ()):
            _link(edges, p.id, b)
        if p.retained is not None:
            me = w.bodies[i]
            for j, o in enumerate(w.bodies):
                if j == i or o.fastener or o.part_idx is None:
                    continue
                op = r.spec.part(o.id)
                if op is None or op.kind not in ("structure", "plate"):
                    continue
                if measure.min_gap(me, o, 1.0) <= 0.5:
                    _link(edges, p.id, o.id)

    root = next((p.id for p in r.spec.parts if p.kind == "structure"), None)
    if root is None:
        ctx.not_checked.append("Join graph: no `structure` part to act as the chassis root, so attachment was not traced")
        return out
    seen, q = set(), deque([root])
    while q:
        pid = q.popleft()
        if pid in seen:
            continue
        seen.add(pid)
        q.extend(n for n in sorted(edges.get(pid, ())) if n not in seen)
    loose = 0
    for p in r.spec.parts:
        if p.id in seen or p.id in floating_ok:
            continue
        loose += 1
        me = w.body(p.id)
        hint, at = "", None
        if me is not None:
            at = me.center
            best = None
            for o in w.bodies:
                if o is me or o.fastener or o.part_idx is None:
                    continue
                g = measure.min_gap(me, o, 50.0)
                if best is None or g < best[0]:
                    best = (g, o.id)
            if best is not None:
                hint = (f" Nearest part is `{best[1]}`, {best[0]:.1f} mm away." if np.isfinite(best[0])
                        else " No other part is within 50 mm.")
        out.append(fail("connection.floating", G, BLOCKER, "Part is not attached to anything",
                        f"`{p.id}` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis.{hint}")
                   .on(p.id).here(at)
                   .fix("Add a fastener through it, or list it in `connections` with a method and a reason; use `none` with a reason only if it is meant to be loose."))
    if loose == 0:
        out.append(ok("connection.joined", G, "Every part is attached",
                      f"All {len(r.spec.parts)} parts lead back to the chassis through screws, shared prints, captive pockets, joints or declared connections."))
    return out
