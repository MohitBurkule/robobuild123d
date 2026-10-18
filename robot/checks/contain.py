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
        if p is None or p.kind not in ELECTRONICS or p._extra.get("exposed"):
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
                       .fix("Move it inside the chassis/armour, or declare `exposed: true` with a reason if it is a deliberately exposed drive/weapon part."))
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
        c = (lo + hi) / 2
        best = None
        for ax in range(3):
            for s in (-1, 1):
                d = np.zeros(3)
                d[ax] = s
                face = c.copy()
                face[ax] = (hi if s > 0 else lo)[ax] + 0.05 * s
                ax2 = [i for i in range(3) if i != ax]
                pts = [face] + [face + np.eye(3)[i] * k for i in ax2 for k in (-0.8, 0.8)]
                pts = np.array(pts)
                if measure.inside_any(others, pts).any():
                    continue
                dist, _ = sc.first_hit(pts, np.tile(d, (len(pts), 1)), SWITCH_REACH_MM)
                if np.all(~np.isfinite(dist)):
                    best = "+-"[s < 0] + "xyz"[ax]
                    break
            if best:
                break
        if best:
            out.append(ok("contain.switch_access", G, "Switch reachable from outside", f"`{b.id}` has a clear 1.6 mm tool line out along {best}."))
        else:
            out.append(fail("contain.switch_access", G, BLOCKER, "Switch cannot be reached from outside",
                            f"No straight 1.6 mm wide tool line from `{b.id}` leaves the robot within {SWITCH_REACH_MM:.0f} mm on any axis.")
                       .on(b.id).here(c).fix("Open a slot in the armour over the switch actuator."))
    return out
