"""Containment by role: electronics inside the chassis envelope, wheels proud of the body for ground contact (and on both
faces when invertible), wires inside the chassis except declared external ports, and a clear tool line to the switch."""

from __future__ import annotations

import numpy as np
from scipy.spatial import Delaunay

from .. import measure
from ..finding import BLOCKER, WARNING, fail, note, ok

G = "contain"
ELECTRONICS = {"battery", "esc", "receiver", "motor", "weapon_motor", "servo"}
SHELL = {"structure", "armor", "armour", "plate", "wedge", "lid", "cover", "tub", "fork"}
DRIVEN = {"wheel", "tyre", "pulley", "weapon", "shaft"}
TOL_MM = 0.5
SWITCH_REACH_MM = 40.0
MOTOR_KINDS = {"motor", "weapon_motor", "servo"}


def _hull(bodies):
    V = np.vstack([b.mesh.vertices for b in bodies])
    return Delaunay(V), V


def _sample(b, n=600):
    V = b.mesh.vertices
    if len(V) > n:
        V = V[np.linspace(0, len(V) - 1, n).astype(int)]
    return V


def _outside(hull, P, tol):
    """Points farther than ~tol outside the hull (tested by shrinking toward the hull centroid)."""
    inside = hull.find_simplex(P) >= 0
    if inside.all():
        return ~inside
    c = hull.points.mean(0)
    d = P - c
    nd = np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    Q = P - d / nd * tol
    return ~(inside | (hull.find_simplex(Q) >= 0))


PROVEN_KEYS = ("proven_design", "reference_cad", "reference_doc")


def proven(spec) -> bool:
    """A replica of a robot that already fights (its source declared): its as-built exposures are accepted as found."""
    raw = getattr(spec, "raw", {}) or {}
    return any(raw.get(k) for k in PROVEN_KEYS)


def _exposed_ok(spec, p) -> bool:
    """`exposed: true` is honoured for a motor only on a proven replica; a new design must armour its motors (user
    2026-11-17: Disector, a real fighting robot, needs no added cover; a generated robot does)."""
    if not p._extra.get("exposed"):
        return False
    return p.kind not in MOTOR_KINDS or proven(spec)


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    kind = {p.id: p.kind for p in r.spec.parts}
    shell = [b for b in w.bodies if b.part_idx is not None and kind.get(b.id) in SHELL]
    if not shell:
        ctx.not_checked.append("contain: no chassis/armour parts, so containment was not checked")
        return [note("contain.no_shell", G, "No chassis envelope", "No structure/armour parts to contain the electronics.")]
    hull, V = _hull(shell)
    driven = [b for b in w.bodies if kind.get(b.id) in DRIVEN]
    # 1. electronics inside the envelope
    bad = 0
    for b in w.bodies:
        p = r.spec.part(b.id) if b.part_idx is not None else None
        if p is None or p.kind not in ELECTRONICS or _exposed_ok(r.spec, p):
            continue
        P = _sample(b)
        o = _outside(hull, P, TOL_MM)
        if o.any() and driven:
            o[o] = ~measure.inside_any(driven, P[o])  # a shaft inside its own wheel/hub/weapon is fine
        if o.any():
            bad += 1
            out.append(fail("contain.electronics_exposed", G, BLOCKER, "Electronics outside the armour",
                            f"`{p.id}` has {o.mean() * 100:.0f} % of its surface outside the chassis envelope; a hit lands on it directly.")
                       .on(p.id).here(P[o][0])
                       .fix("Move it inside the chassis/armour. `exposed: true` is accepted for a motor only on a replica of a robot that "
                            "already fights (spec `proven_design: {robot, source}`); a new design must armour it."))
    if not bad:
        out.append(ok("contain.electronics", G, "Electronics are inside the armour", "Every battery, ESC, receiver and motor sits inside the chassis envelope."))
    # 2. wheels proud of the body
    wheels = [b for b in w.bodies if kind.get(b.id) == "wheel"]
    if wheels:
        body_lo, body_hi = V.min(0), V.max(0)
        wlo = min(b.aabb[0][2] for b in wheels)
        whi = max(b.aabb[1][2] for b in wheels)
        if wlo > body_lo[2] - 0.1:
            out.append(fail("contain.wheel_ground", G, BLOCKER, "Wheels do not stick out below the body",
                            f"Lowest wheel point z={wlo:.2f} is not below the body bottom z={body_lo[2]:.2f}; the body, not the wheels, rests on the floor.")
                       .on(*[b.id for b in wheels]))
        if r.spec.can_run_inverted and whi < body_hi[2] + 0.1:
            out.append(fail("contain.wheel_invert", G, BLOCKER, "Wheels do not reach the floor when inverted",
                            f"The robot is declared invertible but the top wheel point z={whi:.2f} is not above the body top z={body_hi[2]:.2f}.")
                       .on(*[b.id for b in wheels]).fix("Use larger wheels or lower the top armour so the wheels protrude on both faces."))
        if wlo <= body_lo[2] - 0.1 and (not r.spec.can_run_inverted or whi >= body_hi[2] + 0.1):
            out.append(ok("contain.wheels", G, "Wheels protrude as declared",
                          f"Wheels reach {body_lo[2] - wlo:.1f} mm below the body" + (f" and {whi - body_hi[2]:.1f} mm above it." if r.spec.can_run_inverted else ".")))
    # 3. wires inside
    if r.spec.wires:
        if not ctx.routes:
            ctx.not_checked.append("contain.wire_exposed: no wire routes (wiring skipped or failed)")
        else:
            ext = {wi.id for wi in r.spec.wires if wi._extra.get("external")}
            nb = 0
            for rt in ctx.routes:
                if rt.id in ext:
                    continue
                P = np.asarray(rt.points, float)
                if len(P) < 2:
                    continue
                S = np.vstack([a + (b2 - a) * t for a, b2 in zip(P, P[1:]) for t in np.linspace(0, 1, max(int(np.linalg.norm(b2 - a) / 0.5), 1), endpoint=False)] + [P[-1:]])
                o = _outside(hull, S, TOL_MM)
                if o.any():
                    nb += 1
                    out.append(fail("contain.wire_exposed", G, BLOCKER, "Wire runs outside the chassis",
                                    f"Wire `{rt.id}` leaves the chassis envelope for about {o.sum() * 0.5:.1f} mm.")
                               .on(rt.id).here(S[o][0]).fix("Route it inside, or mark the wire `external: true` if it is a deliberate outside port."))
            if not nb:
                out.append(ok("contain.wires", G, "Wires stay inside the chassis", f"{len(ctx.routes)} routes checked against the chassis envelope."))
    # 4. switch tool line
    for b in w.bodies:
        if kind.get(b.id) != "switch":
            continue
        others = [o for o in w.bodies if o is not b and not o.is_wire]
        sc = measure.Scene(others)
        lo, hi = b.aabb
        # aim from the part origin (the actuator body) first: the box centre is skewed by terminal tabs
        centres = [np.clip(b.M[:3, 3], lo, hi), (lo + hi) / 2]
        best, c, why = None, centres[0], {}
        for c in centres:
            for ax in range(3):
                for s in (-1, 1):
                    d = np.zeros(3)
                    d[ax] = s
                    face = c.copy()
                    face[ax] = (hi if s > 0 else lo)[ax] + 0.05 * s
                    ax2 = [i for i in range(3) if i != ax]
                    pts = np.array([face] + [face + np.eye(3)[i] * k for i in ax2 for k in (-0.8, 0.8)])
                    name = "+-"[s < 0] + "xyz"[ax]
                    if measure.inside_any(others, pts).any():
                        why.setdefault(name, f"starts inside another part at ({', '.join(f'{v:.1f}' for v in face)})")
                        continue
                    dist, _ = sc.first_hit(pts, np.tile(d, (len(pts), 1)), SWITCH_REACH_MM)
                    if np.all(~np.isfinite(dist)):
                        best = name
                        break
                    k = int(np.nanargmin(np.where(np.isfinite(dist), dist, np.inf)))
                    hp = pts[k] + d * dist[k]
                    who = next((o.id for o in others if o.sdf(hp[None] + d * 0.05)[0] < 0.1), "?")
                    hole = [f"{'xyz'[i]} {face[i]:.1f}" for i in ax2]
                    why.setdefault(name, f"hits `{who}` after {dist[k]:.1f} mm at ({', '.join(f'{v:.1f}' for v in hp)}); "
                                         f"a hole r >= 1.2 centred at {', '.join(hole)} clears it")
                if best:
                    break
            if best:
                break
        if best:
            out.append(ok("contain.switch_access", G, "Switch reachable from outside", f"`{b.id}` has a clear 1.6 mm tool line out along {best}."))
        else:
            out.append(fail("contain.switch_access", G, BLOCKER, "Switch cannot be reached from outside",
                            f"No straight 1.6 mm wide tool line from `{b.id}` leaves the robot within {SWITCH_REACH_MM:.0f} mm on any axis. "
                            + "; ".join(f"{k}: {v}" for k, v in why.items()))
                       .on(b.id).here(c).fix("Open a slot in the armour over the switch actuator."))
    out.extend(line_of_sight(ctx))
    return out


SIGHT_KINDS = {"battery", "esc", "receiver", "motor", "servo"}  # shielded from every side, not just inside the hull
# a weapon motor is often the spinning hub itself (exposed by design); drive motors and servos are not
SHIELD_SKIP = {"battery", "esc", "receiver", "wire"}  # never armour; motors/servos/wheels/the switch body do shield (a wire under the switch in its slot is covered)
SIGHT_FRAC = 0.10                                  # more than this share of the surface seen straight from outside
WIRE_FRAC = 0.15


def _dirs():
    D = [np.array(v, float) for v in np.ndindex(3, 3, 3)]
    D = [d - 1 for d in D if np.any(d != 1)]
    D = [d / np.linalg.norm(d) for d in D]
    return [d for d in D if d[2] > -0.7]          # straight down is the floor


def _seen(shields, P, dirs):
    """(fraction of points with a clear straight line out, best direction, its fraction). Casts body by body, only
    the rays still escaping and only into bodies whose box they touch (low memory: no merged scene)."""
    if not shields:
        return 1.0, dirs[0], 1.0
    any_out = np.zeros(len(P), bool)
    best = (0.0, dirs[0])
    for d in dirs:
        O = P + d * 0.05
        D = np.tile(d, (len(P), 1))
        esc = np.ones(len(P), bool)
        for sb in shields:
            idx = np.nonzero(esc)[0]
            if not len(idx):
                break
            lo, hi = sb.aabb
            m = measure._rays_touch_box(lo, hi, O[idx], D[idx])
            if not m.any():
                continue
            j = idx[m]
            esc[j[sb.mesh.ray.intersects_any(O[j], D[j])]] = False
        any_out |= esc
        if esc.mean() > best[0]:
            best = (float(esc.mean()), d)
    return float(any_out.mean()), best[1], best[0]


def line_of_sight(ctx):
    """Electronics and wires visible straight from outside through an opening (an open top window passes the hull
    test but a hit or a pit hazard lands right on them). Rays from the part's surface in 21 directions (not down)
    must hit armour; electronics/switch/wires never shield each other. Ripsaw, 2026-11-16: top-plate window over
    battery, ESC and wires passed contain.electronics."""
    r, w = ctx.r, ctx.world
    kind = {p.id: p.kind for p in r.spec.parts}
    out, dirs = [], _dirs()

    def shield_for(skip):
        bs = [b for b in w.bodies if not b.is_wire and b.id not in skip and kind.get(b.id) not in SHIELD_SKIP]
        return sorted(bs, key=lambda b: -float(np.prod(b.aabb[1] - b.aabb[0])))   # big armour first: fewer casts

    bad = 0
    for b in w.bodies:
        p = r.spec.part(b.id) if b.part_idx is not None else None
        if p is None or p.kind not in SIGHT_KINDS or _exposed_ok(r.spec, p):
            continue
        V = _sample(b, 200)
        c = b.mesh.centroid
        P = V + (V - c) / (np.linalg.norm(V - c, axis=1, keepdims=True) + 1e-9) * 0.1
        frac, d, fd = _seen(shield_for({b.id}), P, dirs)
        if fd > SIGHT_FRAC:
            bad += 1
            out.append(fail("contain.line_of_sight", G, BLOCKER, "Electronics visible through an opening",
                            f"`{b.id}`: {fd * 100:.0f} % of its surface has a clear straight line out along "
                            f"({d[0]:+.1f}, {d[1]:+.1f}, {d[2]:+.1f}) ({frac * 100:.0f} % from some direction); nothing "
                            f"armours it there.").on(b.id).here(P[0])
                       .fix("Close the opening over it (lid / cover plate), or move it behind a wall; a deliberately "
                            "open bay needs `exposed: true` with a reason."))
    routes = {rt.id: rt for rt in (ctx.routes or [])}
    ext = {wi.id for wi in r.spec.wires if wi._extra.get("external")}
    shield = shield_for(set()) if routes else None
    for wid, rt in routes.items():
        if wid in ext:
            continue
        P = np.asarray(rt.points, float)
        if len(P) < 2:
            continue
        S = np.vstack([a + (b2 - a) * t for a, b2 in zip(P, P[1:]) for t in np.linspace(0, 1, max(int(np.linalg.norm(b2 - a) / 1.0), 1), endpoint=False)])
        frac, d, fd = _seen(shield, S, dirs)
        if fd > WIRE_FRAC:
            bad += 1
            out.append(fail("contain.wire_line_of_sight", G, BLOCKER, "Wire visible through an opening",
                            f"Wire `{wid}`: {fd * 100:.0f} % of its run is in straight view from outside along "
                            f"({d[0]:+.1f}, {d[1]:+.1f}, {d[2]:+.1f}).").on(wid).here(S[0])
                       .fix("Route it under a cover or close the opening above it."))
    if not bad:
        out.append(ok("contain.line_of_sight", G, "Electronics and wires are shielded",
                      "No battery, ESC, receiver or wire run is in straight view from outside."))
    return out
