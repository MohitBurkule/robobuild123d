"""Spring-loaded forks and belt drives: is there something holding the tension, and is it the right amount?

New in the Python port (no Rust counterpart). Rules:
- a part of kind `fork` on a joint needs a `tensioner` (not `none`) whose anchors lie on parts, one on the fork and one on
  another part, or nothing pulls it down;
- a belt (`belt` on a part) names two existing pulleys; the loop round them, from the pulley centre distance and radii, is
  compared with `length_mm`: o-rings / round / flat elastic belts must stretch 5-15 %; toothed belts (gt2, htd) do not
  stretch, so they need an adjustable tensioner and a length within the adjustment.
Anything that cannot be evaluated goes to NOT CHECKED, never a silent pass.
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "tension"
ANCHOR_TOL_MM = 1.0
STRETCH = (0.05, 0.15)
TOOTHED = {"gt2", "gt3", "htd", "t2.5", "t5", "mxl", "xl", "toothed", "timing"}
TOOTHED_SLACK = 0.02  # an adjustable tensioner takes up about 2 % of the loop
ELASTIC = {"o_ring", "oring", "round", "flat", "elastic", "stretch"}


def _active(t) -> bool:
    return t is not None and (t.kind or "none") != "none"


def _surface_hits(w, pt, skip_wires=True):
    """Ids of bodies whose surface or inside is within ANCHOR_TOL_MM of a world point."""
    P = np.asarray(pt, float)[None, :]
    hits = []
    for b in w.bodies:
        if skip_wires and b.is_wire:
            continue
        lo, hi = b.aabb
        if np.any(P[0] < lo - ANCHOR_TOL_MM) or np.any(P[0] > hi + ANCHOR_TOL_MM):
            continue
        if b.sdf(P)[0] <= ANCHOR_TOL_MM:
            hits.append(b.id)
    return hits


def pulley_radius(body, axis=None) -> float:
    """Radius of a pulley about its axis: half the mean of the two largest world extents (the axis is the thinnest)."""
    ext = sorted((float(v) for v in body.aabb[1] - body.aabb[0]), reverse=True)
    return 0.25 * (ext[0] + ext[1])


def loop_length(c, r1, r2) -> float:
    """Open-belt length round two pulleys at centre distance c."""
    if c <= abs(r1 - r2):
        return math.nan
    return 2.0 * math.sqrt(c * c - (r1 - r2) ** 2) + math.pi * (r1 + r2) + 2.0 * (r1 - r2) * math.asin((r1 - r2) / c)


def _fork(ctx, p, out):
    w = ctx.world
    t = p.tensioner
    if not _active(t):
        out.append(fail("tension.fork_untensioned", G, BLOCKER, "Pivoting fork has nothing holding it down",
                        f"`{p.id}` pivots on a joint but has no `tensioner`; it will flop up and the wedge edge will not stay on the floor.")
                   .on(p.id).fix("Add an elastic band, spring or printed flexure from the fork to the chassis and declare it as `tensioner`."))
        return False
    anchors = list(t.anchors or [])
    if t.kind in ("printed_flexure",) and not anchors:
        return True  # the flexure is the part itself
    if len(anchors) < 2:
        out.append(fail("tension.fork_anchors", G, BLOCKER, "Fork tensioner has no anchor points",
                        f"`{p.id}` tensioner `{t.kind}` declares {len(anchors)} anchor(s); need one on the fork and one on the chassis.")
                   .on(p.id).fix("List both ends of the band or spring in `tensioner.anchors` (world, start pose)."))
        return False
    hits = [_surface_hits(w, a) for a in anchors]
    on_fork = [p.id in h for h in hits]
    others = set(x for h in hits for x in h if x != p.id)
    bad = [i for i, h in enumerate(hits) if not h]
    if bad or not any(on_fork) or not others:
        a = anchors[bad[0]] if bad else anchors[0]
        why = (f"anchor {bad[0]} at ({a[0]:.1f}, {a[1]:.1f}, {a[2]:.1f}) is on no part" if bad else
               "no anchor is on the fork" if not any(on_fork) else "no anchor is on another part")
        out.append(fail("tension.fork_anchors", G, BLOCKER, "Fork tensioner is not attached at both ends",
                        f"`{p.id}`: {why}.").on(p.id).here(a)
                   .fix("Put a hook, post or hole for the band on both the fork and the chassis, and move the anchors onto them."))
        return False
    if not t.adjustable:
        out.append(fail("tension.fork_not_adjustable", G, WARNING, "Fork tension cannot be adjusted",
                        f"`{p.id}` tensioner `{t.kind}` is fixed; bands stretch and springs fatigue during an event.")
                   .on(p.id).fix("Add a second hook position, a slot or a set screw and set `adjustable: true`."))
    return True


def _belt(ctx, p, out):
    w, r = ctx.world, ctx.r
    b = p.belt
    pulleys = list(b.pulleys or [])
    if len(pulleys) != 2:
        out.append(fail("tension.belt_pulleys", G, BLOCKER, "Belt does not name two pulleys",
                        f"`{p.id}` belt lists {len(pulleys)} pulley(s); a belt runs between exactly two.").on(p.id))
        return False
    bodies = [w.body(x) for x in pulleys]
    missing = [x for x, bb in zip(pulleys, bodies) if bb is None]
    if missing:
        out.append(fail("tension.belt_pulleys", G, BLOCKER, "Belt pulley not found",
                        f"`{p.id}` names pulley(s) {', '.join(missing)} that are not parts.").on(p.id, *missing))
        return False
    c = float(np.linalg.norm(bodies[0].center - bodies[1].center))
    r1, r2 = pulley_radius(bodies[0]), pulley_radius(bodies[1])
    need = loop_length(c, r1, r2)
    ctx.metrics[f"belt_loop_mm.{p.id}"] = need
    ctx.metrics[f"belt_centres_mm.{p.id}"] = c
    if not math.isfinite(need):
        out.append(fail("tension.belt_geometry", G, BLOCKER, "Pulleys overlap",
                        f"`{p.id}`: pulley centres are {c:.1f} mm apart with radii {r1:.1f} and {r2:.1f} mm.").on(p.id, *pulleys))
        return False
    kind = (b.kind or "o_ring").lower()
    tens = [x.tensioner for x in (p, *(rp.part for rp in r.parts if rp.part.id in pulleys))]
    tens = [t for t in tens if _active(t)]
    adjustable = any(t.adjustable for t in tens)
    if b.length_mm is None:
        out.append(fail("tension.belt_length", G, WARNING, "Belt length not given",
                        f"`{p.id}` has no `length_mm`; the loop round the pulleys is {need:.1f} mm, buy or cut to suit.")
                   .on(p.id).expect("length_mm set", "none"))
        ctx.not_checked.append(f"Belt tension of `{p.id}`: no `length_mm`")
        return False
    L = float(b.length_mm)
    stretch = need / L - 1.0
    ctx.metrics[f"belt_stretch.{p.id}"] = stretch
    if kind in TOOTHED:
        if not adjustable:
            out.append(fail("tension.belt_no_tensioner", G, BLOCKER, "Toothed belt has no adjustable tensioner",
                            f"`{p.id}` ({kind}) does not stretch; without a slot, idler or eccentric it cannot be fitted or re-tensioned.")
                       .on(p.id, *pulleys).fix("Slot the motor mount or add an idler and declare `tensioner` with `adjustable: true`."))
            return False
        if abs(stretch) > TOOTHED_SLACK:
            out.append(fail("tension.belt_length", G, BLOCKER, "Toothed belt length does not fit the pulleys",
                            f"`{p.id}`: loop round the pulleys is {need:.1f} mm but the belt is {L:.1f} mm ({stretch * 100:+.1f} %).")
                       .on(p.id, *pulleys).expect(f"{L:.1f} mm +/- {TOOTHED_SLACK * 100:.0f} %", f"{need:.1f} mm")
                       .fix("Move the pulleys or pick the stock belt length nearest the loop."))
            return False
        return True
    if kind not in ELASTIC:
        ctx.not_checked.append(f"Belt tension of `{p.id}`: belt kind `{kind}` unknown")
        out.append(fail("tension.belt_kind", G, WARNING, "Belt kind unknown", f"`{p.id}` belt kind `{kind}`; tension was not judged.").on(p.id))
        return False
    lo, hi = STRETCH
    if not (lo <= stretch <= hi) and not (adjustable and stretch > 0 and stretch < hi + 0.05):
        sev = BLOCKER if stretch < -0.01 or stretch > hi + 0.10 else WARNING
        what = "slack: it will slip" if stretch < lo else "over-stretched: it will load the motor bearings and snap"
        out.append(fail("tension.belt_stretch", G, sev, "Belt stretch out of range",
                        f"`{p.id}`: loop {need:.1f} mm on a {L:.1f} mm {kind} is {stretch * 100:.1f} % stretch, {what}.")
                   .on(p.id, *pulleys).expect(f"{lo * 100:.0f}-{hi * 100:.0f} %", f"{stretch * 100:.1f} %")
                   .fix(f"Use a {need / (1 + (lo + hi) / 2):.0f} mm loop or move the pulleys."))
        return False
    return True


def run(ctx):
    r = ctx.r
    out = []
    n = good = 0
    for rp in r.parts:
        p = rp.part
        if p.kind == "fork" and p.joint is not None and p.parent:
            n += 1
            good += _fork(ctx, p, out)
        if p.belt is not None:
            n += 1
            good += _belt(ctx, p, out)
        elif p.kind == "belt":
            n += 1
            out.append(fail("tension.belt_undefined", G, BLOCKER, "Belt part has no belt definition",
                            f"`{p.id}` is a belt but has no `belt` (pulleys, kind, length_mm), so its tension cannot be judged.").on(p.id))
    if n and good == n:
        out.append(ok("tension.ok", G, "Forks and belts are tensioned", f"{n} tensioned fork(s) and belt(s) checked."))
    return out
