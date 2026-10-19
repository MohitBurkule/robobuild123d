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


# A revolute part may be carried on its axis by a holder this far from the pivot (bearing plate beside a disc stack).
JOINT_AXIS_REACH_MM = 25.0


def impact_part(p) -> bool:
    return p.kind in IMPACT


def is_low_energy(p) -> bool:
    return bool(p.material) and p.material.lower() in LOW_ENERGY


FUSED_MIN_VOLUME_MM3 = 1.0  # shared volume that makes two bodies one print; faces that only touch are two prints
KEY_MIN_BLOCKED_DIRS = 5  # a mechanical key holds the part in at least 5 of the 6 axis directions without the glue
DIRS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


def fused_volume(w, a, b):
    """Shared volume of two bodies in mm3, or None when either has no body."""
    ba, bb = w.body(a), w.body(b)
    if ba is None or bb is None:
        return None
    o = measure.overlap(ba, bb, cap=0.0)
    return 0.0 if o is None else float(o.volume)


def key_blocked_dirs(ctx, a, b):
    """Directions (of 6) in which `b` cannot slide by the capture slop without running into `a`; None without bodies."""
    from .interference import allowed_depth

    w = ctx.world
    ba, bb = w.body(a), w.body(b)
    if ba is None or bb is None:
        return None
    allow = allowed_depth(ctx.r, bb, ba)
    if allow == float("inf"):
        return 6
    slop = ctx.r.profile.capture_slop_mm
    return sum(measure.overlap_exceeds(bb, ba, allow + 0.02, np.asarray(d, float) * slop) for d in DIRS)


def part_mass_g(rp, body):
    """Best mass estimate of one part (same order of sources as the mass group, without calibration)."""
    p = rp.part
    for v in (p.scale_mass_g, p.slicer_mass_g):
        if v is not None:
            return float(v)
    if rp.cat is not None:
        return float(rp.cat.mass_g)
    dens = catalog.density(p.material)
    if dens is not None and body is not None:
        printed = catalog.is_printed(p.process) if p.process else False
        frac = p.solid_fraction if p.solid_fraction is not None else (0.85 if printed else 1.0)
        return body.geom.volume * 1e-3 * dens * frac
    return float(p.mass_g) if p.mass_g is not None else None


def contact_area_mm2(me, o, gap):
    """Area of `me`'s surface lying within `gap` of `o` (surface sampling at about 0.5 mm)."""
    if not measure.aabb_overlap(me.aabb, o.aabb, gap):
        return 0.0
    pts, _ = me.surface(0.5)
    n = len(pts) - len(me.mesh.vertices)  # sample_surface appends the vertices after the area samples
    if n <= 0:
        return 0.0
    P = pts[:n]
    lo, hi = o.aabb[0] - gap, o.aabb[1] + gap
    m = np.all((P >= lo) & (P <= hi), axis=1)
    if not m.any():
        return 0.0
    near = int((o.distance(P[m]) <= gap).sum())
    return near * float(me.mesh.area) / n


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
        if f.threads_into:   # the screw clamps its whole stack: every part it passes through is joined to its thread
            for a in f.through:
                if a != f.threads_into:
                    _link(edges, a, f.threads_into)
    for p in r.spec.parts:
        if p.fused_with:
            fw = p.fused_with
            o = r.spec.part(fw)
            if o is not None and o.material == p.material and catalog.part_is_printed(p.process, p.material):
                vol = fused_volume(w, p.id, fw)
                if vol is None:
                    ctx.not_checked.append(f"Fused join `{p.id}`-`{fw}`: no geometry to measure shared volume")
                    _link(edges, p.id, fw)
                elif vol >= FUSED_MIN_VOLUME_MM3:
                    _link(edges, p.id, fw)
                else:
                    out.append(fail("connection.fused_mismatch", G, BLOCKER, "Fused parts only touch",
                                    f"`{p.id}` is fused to `{fw}` but they share {vol:.2f} mm3 (need >= {FUSED_MIN_VOLUME_MM3:.0f} mm3); "
                                    f"faces that only touch print as two pieces or a paper-thin seam.")
                               .on(p.id, fw).fix("Overlap the two bodies by at least a wall thickness so they print as one solid, or bolt them."))
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

            jax = xform.apply_dir(pb.M, np.asarray(p.joint.axis, float)) if pb is not None else np.asarray(p.joint.axis, float)
            jax = jax / (np.linalg.norm(jax) or 1.0)

            def near(bid, along=0.0):
                """Material within 1 mm of the pivot, or a bore round it: a part whose hole encircles the joint axis at the
                pivot (a hub on a shaft, a disc on a spigot, a tube on a pin) holds the pivot as surely as solid material.
                `along` > 0 also accepts the same test at points up to that far along a revolute joint's axis: a holder that
                carries the axle in its own bore (a bearing plate beside a disc stack) holds the axis, not one point."""
                b = w.body(bid)
                if pivot is None or b is None:
                    return False
                if along > 0:
                    return any(_near_at(b, pivot + t * jax) for t in np.arange(-along, along + 0.01, 0.5))
                return _near_at(b, pivot)

            def _near_at(b, pivot):
                d0 = float(b.sdf(pivot)[0])
                if d0 <= 1.0:
                    return True
                if d0 > 6.0:
                    return False
                u = np.cross(jax, [1.0, 0.0, 0.0] if abs(jax[0]) < 0.9 else [0.0, 1.0, 0.0])
                u /= np.linalg.norm(u)
                v = np.cross(jax, u)
                ring = np.array([pivot + (d0 + 0.3) * (np.cos(t) * u + np.sin(t) * v) for t in np.linspace(0, 2 * np.pi, 12, endpoint=False)])
                return float(np.mean(b.inside(ring))) >= 0.75

            rev = (getattr(p.joint, "kind", "") or "") == "revolute"
            if near(p.id) and near(par, JOINT_AXIS_REACH_MM if rev else 0.0):
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
            keyed = False
            if c.mechanical_key:
                nb = key_blocked_dirs(ctx, c.a, c.b)
                if nb is None:
                    ctx.not_checked.append(f"Mechanical key of `{c.a}`-`{c.b}`: no geometry, so the key is not credited")
                else:
                    keyed = nb >= KEY_MIN_BLOCKED_DIRS
                    if not keyed:
                        out.append(fail("connection.key_unproven", G, WARNING, "Declared mechanical key is not in the geometry",
                                        f"`{c.a}`-`{c.b}` sets `mechanical_key` but `{c.b}` is held in only {nb} of 6 directions "
                                        f"by `{c.a}` (a key needs {KEY_MIN_BLOCKED_DIRS}).").on(c.a, c.b)
                                   .fix("Model the slot, dovetail or undercut so the part cannot slide out without the glue."))
            if (is_low_energy(pa) or is_low_energy(pb)) and not keyed:
                out.append(fail("connection.glue_low_energy", G, BLOCKER, "Glue will not stick to this plastic",
                                f"`{c.a}`-`{c.b}`: HDPE, polypropylene and nylon barely take adhesive or tape; set `mechanical_key` only if geometry holds it without the glue.")
                           .on(c.a, c.b).fix("Use screws, a press fit or an interlock, or add a keyed slot and set `mechanical_key`."))
                continue
        elif m == "press_fit":
            d = c.interference_mm
            (lo, hi), pair = catalog.press_fit_range(pa.material, pb.material)
            if d is None or not (lo <= float(d) <= hi):
                out.append(fail("connection.press_fit_interference", G, WARNING, "Press fit has no sensible interference",
                                f"`{c.a}`-`{c.b}`: give `interference_mm` between {lo:g} and {hi:g} for a {pair} press fit"
                                + (f" (got {float(d):g})." if d is not None else ".")).on(c.a, c.b))
        _link(edges, c.a, c.b)

    for p in r.spec.parts:
        i = w.index(p.id)
        if i is None:
            continue
        for b in ctx.captive.get(p.id, ()):
            _link(edges, p.id, b)
        if p.retained is not None:
            me = w.bodies[i]
            tape = str(p.retained).lower() in catalog.TAPE_LIKE
            linked = []
            for j, o in enumerate(w.bodies):
                if j == i or o.fastener or o.part_idx is None:
                    continue
                op = r.spec.part(o.id)
                if op is None or op.kind not in ("structure", "plate"):
                    continue
                if measure.min_gap(me, o, 1.0) <= 0.5:
                    linked.append(o)
            if tape and linked:
                gap = catalog.TAPE_CONTACT_GAP_MM
                area_cm2 = sum(contact_area_mm2(me, o, gap) for o in linked) / 100.0
                grams = part_mass_g(r.parts[me.part_idx], me) if me.part_idx is not None else None
                lim = catalog.TAPE_MAX_G_PER_CM2
                if grams is None:
                    ctx.not_checked.append(f"Tape hold of `{p.id}`: part mass unknown")
                elif area_cm2 <= 0.0 or grams / area_cm2 > lim:
                    load = grams / area_cm2 if area_cm2 > 0 else float("inf")
                    out.append(fail("connection.tape_overload", G, BLOCKER, "Tape cannot hold this part",
                                    f"`{p.id}` weighs {grams:.1f} g on {area_cm2:.2f} cm2 of contact ({load:.1f} g/cm2); "
                                    f"{p.retained} holds at most {lim:g} g/cm2 through a hit.").on(p.id)
                               .expect(f"<= {lim:g} g/cm2", f"{load:.1f} g/cm2")
                               .fix("Screw it down, capture it in a pocket, or give the tape a much larger flat contact face."))
                    linked = []
            for o in linked:
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
    out += cover_retention(r)
    if loose == 0:
        out.append(ok("connection.joined", G, "Every part is attached",
                      f"All {len(r.spec.parts)} parts lead back to the chassis through screws, shared prints, captive pockets, joints or declared connections."))
    return out


COVER_KINDS = {"armor", "armour", "cover", "lid", "panel"}
COVER_WORDS = ("armour", "armor", "cover", "lid", "hood", "panel")
SCREWED_RETAINED = {"screw", "screws", "bolted", "bolt"}
COVER_MIN_FASTENERS = 2


def is_cover(p) -> bool:
    """Armour and cover panels: kind armor/cover/lid/panel, or a plate/structure whose id names it a lid, hood or panel."""
    if p.kind in COVER_KINDS:
        return True
    return p.kind in ("structure", "plate") and any(w in p.id.lower() for w in COVER_WORDS) and p.id.lower() != "tub"


def needs_screws(p) -> bool:
    """Bought-in parts the reference says are screwed (`retained: screws`)."""
    return isinstance(p.retained, str) and p.retained.lower() in SCREWED_RETAINED


def cover_retention(r):
    """Every armour / cover panel (and every part declared `retained: screws`) is held by >= 2 real fasteners; a snap,
    press fit or tape alone pops off on the first hit."""
    count = {}
    for f in r.spec.fasteners:
        for pid in set(list(f.through) + ([f.threads_into] if f.threads_into else [])):
            count[pid] = count.get(pid, 0) + 1
    out, good = [], 0
    for p in r.spec.parts:
        if not (is_cover(p) or needs_screws(p)):
            continue
        n = count.get(p.id, 0)
        if n >= COVER_MIN_FASTENERS:
            good += 1
            continue
        what = "armour / cover panel" if is_cover(p) else "part declared `retained: screws`"
        out.append(fail("connection.cover_fasteners", G, BLOCKER, "Panel not bolted down",
                        f"`{p.id}` is an {what} held by {n} fastener(s); it needs >= {COVER_MIN_FASTENERS} real screws. "
                        f"Snap, press-fit or tape retention alone lets it peel off on the first hit.")
                   .on(p.id).fix("Bolt it with >= 2 screws into inserts, nuts or tapped bosses and declare them in `fasteners`."))
    if good and not out:
        out.append(ok("connection.cover_fasteners", G, "Panels bolted down",
                      f"All {good} armour / cover panels and screw-retained parts are held by >= {COVER_MIN_FASTENERS} fasteners."))
    return out
