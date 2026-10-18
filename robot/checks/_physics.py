"""Shared helpers for the shape, dynamics and strength groups (not a check group itself).

Conventions: world mm, +Y is the front, +Z is up, the floor is `ctx.metrics["ground_z"]` (from `ground`) or the lowest
wheel point. Loads are in newtons, stresses in MPa (N/mm^2).
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from .power import spin_axis

FRONT = np.array([0.0, 1.0, 0.0])
G0 = 9.81
SPINS = ("spinner", "drum", "disc", "bar")
SUPPORT = ("structure", "plate", "fork", "armor")
# Design impact: the whole robot decelerated at this many g (a big hit from an antweight spinner is 50 to 200 g).
IMPACT_G = 100.0

# Deep-groove ball bearings by (bore, OD) mm: (name, dynamic C N, static C0 N). Typical catalog values (NSK/SKF class).
BEARINGS = {
    (3, 7): ("MR73", 390, 120), (3, 8): ("693", 560, 180), (3, 10): ("623", 630, 220),
    (4, 7): ("MR74", 330, 100), (4, 8): ("MR84", 400, 130), (4, 9): ("684", 640, 220), (4, 10): ("MR104", 700, 240),
    (4, 12): ("604", 970, 350), (4, 13): ("624", 1300, 490), (4, 16): ("634", 1730, 670),
    (5, 8): ("MR85", 310, 110), (5, 10): ("MR105", 430, 165), (5, 11): ("685", 715, 280), (5, 13): ("695", 1080, 430),
    (5, 14): ("605", 1330, 505), (5, 16): ("625", 1730, 670), (6, 10): ("MR106", 495, 220), (6, 13): ("686", 1080, 440),
    (6, 15): ("696", 1730, 670), (6, 19): ("626", 2600, 1050), (7, 14): ("687", 1170, 510), (7, 22): ("627", 3300, 1370),
    (8, 12): ("678", 560, 270), (8, 16): ("688", 1610, 710), (8, 22): ("608", 3300, 1370), (10, 15): ("6700", 855, 435),
    (10, 26): ("6000", 4550, 1960),
}


def floor_z(ctx):
    if "ground_z" in ctx.metrics:
        return float(ctx.metrics["ground_z"])
    if ctx.r.spec.ground_z is not None:
        return float(ctx.r.spec.ground_z)
    wheels = [b for b in ctx.world.bodies if b.kind == "wheel"]
    src = wheels or [b for b in ctx.world.bodies if not b.is_wire]
    return float(min(b.aabb[0][2] for b in src))


def solids(w):
    return [b for b in w.bodies if not b.is_wire]


def part(ctx, b):
    return ctx.r.parts[b.part_idx].part if b.part_idx is not None else None


def material_of(ctx, b):
    p = part(ctx, b)
    if p is None:
        return "steel" if b.fastener else None
    return p.material


def printed(ctx, b):
    p = part(ctx, b)
    return bool(p is not None and catalog.part_is_printed(p.process, p.material))


def mass_g(ctx, b):
    return ctx.metrics.get(f"part_mass_g.{b.id}")


def robot_mass_g(ctx):
    return float(ctx.metrics.get("mass_total_g", ctx.r.profile.mass_limit(ctx.r.spec.locomotion == "roller")))


def impact_n(ctx):
    return robot_mass_g(ctx) * 1e-3 * IMPACT_G * G0


def weapons(ctx):
    """[(part, body, origin, unit axis)] for every spinning weapon with a resolvable spin axis."""
    w, r = ctx.world, ctx.r
    out = []
    for rp in r.parts:
        wd = rp.part.weapon
        if rp.part.kind != "weapon" or wd is None or wd.kind not in SPINS:
            continue
        i = w.index(rp.part.id)
        sa = spin_axis(w, r, i) if i is not None else None
        if sa is None:
            continue
        out.append((rp.part, w.bodies[i], sa[0], sa[1]))
    return out


def perp_radius(pts, origin, axis):
    q = np.asarray(pts, float) - origin
    return np.linalg.norm(q - np.outer(q @ axis, axis), axis=1)


def bearing_rating(bore, od):
    for (d, D), v in BEARINGS.items():
        if abs(d - bore) <= 0.3 and abs(D - od) <= 0.3:
            return v
    return None


def shaft_layout(ctx, wb, origin, axis):
    """How the weapon shaft is supported: the shaft body through the weapon centre, its diameter, and each side's support
    (signed distance along the axis from the weapon centre, the bearing or structure body that holds it). None when no
    shaft passes through the weapon centre."""
    w = ctx.world
    shaft = next((b for b in w.bodies if b.kind == "shaft" and not b.fastener and b.inside(origin)[0]), None)
    if shaft is None:
        return None
    t = (shaft.mesh.vertices - origin) @ axis
    d = 2.0 * float(np.percentile(perp_radius(shaft.mesh.vertices, origin, axis), 99))
    ts = np.arange(float(t.min()) + 0.1, float(t.max()) - 0.1, 0.25)
    P = origin + np.outer(ts, axis)
    bearings = [b for b in w.bodies if b.kind == "bearing" and not b.fastener]
    holders = [b for b in w.bodies if b not in (wb, shaft) and not b.fastener and b.kind in SUPPORT]
    sides = {}
    for sign in (1.0, -1.0):
        m = (ts * sign) > 0
        best = None
        for b in bearings:
            hit = b.inside(P[m])
            if hit.any():
                tc = float(ts[m][hit].mean())
                if best is None or abs(tc) < abs(best[0]):
                    best = (tc, b)
        if best is None:
            for b in holders:
                hit = b.inside(P[m])
                if hit.any():
                    tc = float(ts[m][hit].mean())
                    if best is None or abs(tc) < abs(best[0]):
                        best = (tc, b)
        if best is not None:
            sides[sign] = best
    return {"shaft": shaft, "d": d, "sides": sides}


def reactions(F, sides):
    """Bearing reactions and the shaft bending moment for a point load F at t = 0 between supports at ta < 0 < tb; a
    one-sided support is a cantilever. Returns (moment N mm, {sign: reaction N}, a, b, simply_supported)."""
    if 1.0 in sides and -1.0 in sides:
        a, b = -sides[-1.0][0], sides[1.0][0]
        L = a + b
        return F * a * b / L, {-1.0: F * b / L, 1.0: F * a / L}, a, b, True
    s = next(iter(sides))
    a = abs(sides[s][0])
    return F * a, {s: F}, a, 0.0, False
