"""Internal flaws a person sees in a section or exploded view that the declarative checks miss.

- internal.solid_invalid a body whose mesh is not a valid manifold (all exact measures against it return nothing).
- internal.no_contact     a part whose solid touches no other solid (floats in the air in a section view), even when a
                         connection is declared for it (connection.floating only reads the declarations).
- internal.fastener_void a screw whose shank runs mostly through air: it clamps nothing that is drawn.
- internal.wire_in_solid a routed wire whose tube centreline passes inside a solid away from its end ports.

Fail closed: anything not evaluated goes to ctx.not_checked.
"""

from __future__ import annotations

import numpy as np

from .. import catalog, measure
from ..finding import BLOCKER, WARNING, fail, ok

G = "internal"
TOUCH_MM = 0.5  # bodies closer than this are touching (a slip fit counts)
VOID_MIN = 0.4  # at least this share of a shank's length must have drawn solid around it
PORT_ZONE = 3.0  # wire ends may sit inside their own parts within this distance


def _solids(w):
    return [b for b in w.bodies if not b.is_wire]


def _broken(b) -> str | None:
    """Why a body's solid cannot be measured (non-manifold, empty or inside-out), None when it is fine."""
    try:
        m = b.manifold
        st = m.status()
        if str(st).split(".")[-1] != "NoError":
            return f"manifold status {st}"
        if m.volume() <= 1e-6:
            return "empty solid"
    except Exception as e:  # noqa: BLE001
        return f"{type(e).__name__}: {e}"
    if b.mesh.volume < 0:
        return "inside-out mesh (negative volume)"
    return None


def solid_valid(ctx):
    out, bad = [], []
    for b in _solids(ctx.world):
        why = _broken(b)
        if why:
            bad.append(b.id)
            out.append(fail("internal.solid_invalid", G, BLOCKER, "Part is not a valid solid",
                            f"`{b.id}` is not a closed solid ({why}); overlap, gap and section measures against it come out empty, "
                            "so interference, contact and clearance checks silently pass for it.")
                       .on(b.id).here(b.center)
                       .fix("Fix the shape (a mirrored or self-intersecting profile is the usual cause) until it is watertight."))
            ctx.not_checked.append(f"Overlaps, gaps and contacts of `{b.id}`: its solid is invalid ({why})")
    ctx.invalid_solids = set(bad)
    if not bad:
        out.append(ok("internal.solid_invalid", G, "Every part is a valid solid", "All bodies are closed, outward-facing manifolds."))
    return out


def no_contact(ctx):
    w = ctx.world
    skip = getattr(ctx, "invalid_solids", set())
    sol = [b for b in _solids(w) if b.id not in skip]
    if len(sol) < 2:
        return []
    out, floating = [], []
    for b in sol:
        if b.fastener:
            continue
        near = False
        for o in sol:
            if o is b or not measure.aabb_overlap(b.aabb, o.aabb, TOUCH_MM):
                continue
            if measure.min_gap(b, o, 1.0) <= TOUCH_MM:
                near = True
                break
        if not near:
            floating.append(b)
    for b in floating:
        out.append(fail("internal.no_contact", G, BLOCKER, "Part touches nothing",
                        f"`{b.id}` is more than {TOUCH_MM} mm from every other solid; in a section view it hangs in the air.")
                   .on(b.id).here(b.center)
                   .fix("Move it onto its mount, add the bracket, pocket or screw that holds it, or close the gap."))
    if not floating:
        out.append(ok("internal.no_contact", G, "Every part touches something",
                      f"{sum(1 for b in sol if not b.fastener)} parts each touch at least one other solid."))
    return out


def fastener_void(ctx):
    r, w = ctx.r, ctx.world
    out, bad = [], 0
    parts = [b for b in _solids(w) if not b.fastener]
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            ctx.not_checked.append(f"internal.fastener_void: `{f.id}` designation `{f.designation}` not understood")
            continue
        d, ln = dl
        dr = np.asarray(f.dir, float)
        n = np.linalg.norm(dr)
        if n < 1e-9:
            ctx.not_checked.append(f"internal.fastener_void: `{f.id}` has a zero `dir`")
            continue
        dr = dr / n
        at = np.asarray(f.at, float)
        ts = np.linspace(0.2, max(ln - 0.2, 0.3), max(int(ln / 0.5), 3))
        # A shank sits in a clearance hole, so probe a ring just outside it: the hole wall must be there.
        a = np.array([1.0, 0, 0]) if abs(dr[0]) < 0.9 else np.array([0, 1.0, 0])
        u = np.cross(dr, a)
        u /= np.linalg.norm(u)
        v = np.cross(dr, u)
        rad = d / 2 + 0.6
        ring = [u * rad * np.cos(k * np.pi / 3) + v * rad * np.sin(k * np.pi / 3) for k in range(6)]
        P = np.array([at + t * dr + q for t in ts for q in ring])
        hit = measure.inside_any(parts, P).reshape(len(ts), len(ring))
        share = float(hit.any(axis=1).mean())
        if share < VOID_MIN:
            bad += 1
            out.append(fail("internal.fastener_void", G, BLOCKER if share < 0.1 else WARNING, "Screw runs through air",
                            f"Only {share * 100:.0f} % of the {ln:g} mm shank of `{f.id}` is inside a drawn part; it clamps nothing that is modelled.")
                       .on(f.id).here(at).expect(f">= {VOID_MIN * 100:.0f} %", f"{share * 100:.0f} %")
                       .fix("Move `at`/`dir` so the shank passes through the parts it joins, or draw the boss/nut it bites into."))
    if r.spec.fasteners and not bad:
        out.append(ok("internal.fastener_void", G, "Screw shanks pass through parts",
                      f"{len(r.spec.fasteners)} screws each run at least {VOID_MIN * 100:.0f} % through drawn solids."))
    return out


def wire_in_solid(ctx):
    r, w = ctx.r, ctx.world
    if not r.spec.wires:
        return []
    if not ctx.routes:
        ctx.not_checked.append("internal.wire_in_solid: no wire routes (wiring skipped or failed), wires vs solids not checked")
        return []
    ends = {}
    for wi in r.spec.wires:
        a = getattr(wi, "from", "") or ""
        ends[wi.id] = {a.split(".")[0], (wi.to or "").split(".")[0]}
    out, bad = [], 0
    sol = _solids(w)
    for rt in ctx.routes:
        pts = np.asarray(rt.points, float)
        if len(pts) < 2:
            continue
        S = []
        for a, b in zip(pts, pts[1:]):
            k = max(int(np.linalg.norm(b - a) / 0.5), 1)
            S.extend(a + (b - a) * t for t in np.linspace(0, 1, k, endpoint=False))
        S = np.array(S + [pts[-1]])
        keep = (np.linalg.norm(S - pts[0], axis=1) > PORT_ZONE) & (np.linalg.norm(S - pts[-1], axis=1) > PORT_ZONE)
        S = S[keep]
        if not len(S):
            continue
        own = ends.get(rt.id, set())
        for b in sol:
            if b.id in own or not measure.aabb_overlap(b.aabb, np.array([S.min(0), S.max(0)])):
                continue
            ins = b.inside(S)
            if ins.any():
                bad += 1
                out.append(fail("internal.wire_in_solid", G, BLOCKER, "Wire passes through a solid",
                                f"Routed wire `{rt.id}` runs inside `{b.id}` for about {ins.sum() * 0.5:.1f} mm away from its ends.")
                           .on(rt.id, b.id).here(S[np.argmax(ins)])
                           .fix("Cut a wire channel through that part or reroute the wire."))
                break
    if not bad:
        out.append(ok("internal.wire_in_solid", G, "Wires stay in free space",
                      f"{len(ctx.routes)} routed wires sampled every 0.5 mm stay out of every solid away from their ports."))
    return out


CHECKS = (solid_valid, no_contact, fastener_void, wire_in_solid)


def run(ctx):
    out = []
    for c in CHECKS:
        out.extend(c(ctx))
    return out
