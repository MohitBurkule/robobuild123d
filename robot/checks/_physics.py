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


# ------------------------------------------------------------------ front lead of a spinner (shared by spinner, shape, archetype)
# Real vertical spinners run low forks / wedgelets / skirts AHEAD of the disc for the ground game. Such a part may lead the
# weapon's swept front by up to the archetype's `blade_lead_mm` maximum; chassis, body and other parts may not lead it at all.
GROUND_GAME_KINDS = ("fork", "wedgelet", "skirt", "wedge")
GROUND_LOW_TOP_MM = 6.0  # leading edge (or whole part) top at most this far above the floor
GROUND_THIN_MM = 3.0  # or a plate at most this thick (vertically) that sits on/near the floor
GROUND_EDGE_DEPTH_MM = 2.0  # the "leading edge" is the part's material within this distance of its front-most point
DEFAULT_GROUND_LEAD_MM = {"vertical_spinner": 15.0, "drum": 15.0}  # = vertical_spinner_forks blade_lead_mm max
FALLBACK_GROUND_LEAD_MM = 3.0  # other spinners without an archetype blade_lead (the former wedgelet tolerance)


def ground_lead_max(ctx):
    """Max mm a ground-game part may lead the weapon: the archetype's `blade_lead_mm` upper bound when it has one."""
    spec = ctx.r.spec
    name = spec.raw.get("archetype") if isinstance(spec.raw, dict) else None
    try:
        from .archetype import ARCHETYPES, params_for
        if name in ARCHETYPES:
            over = spec.raw.get("archetype_params") or {}
            _, P = params_for(name, over if isinstance(over, dict) else None)
            bl = P.get("blade_lead_mm")
            if bl and bl[1] is not None:
                return float(bl[1])
    except Exception:  # noqa: BLE001 - fall back to the robot-type default
        pass
    return DEFAULT_GROUND_LEAD_MM.get(spec.robot_type, FALLBACK_GROUND_LEAD_MM)


def is_ground_game(ctx, b, floor):
    """(bool, why): a low fork/wedgelet/skirt (or a part declaring `ground_game: true`) whose front works at floor level."""
    p = part(ctx, b)
    declared = bool(p is not None and getattr(p, "_extra", {}).get("ground_game"))
    if not (declared or b.kind in GROUND_GAME_KINDS):
        return False, f"`{b.id}` is a {b.kind} part"
    if floor is None:
        return False, "floor unknown"
    v = b.mesh.vertices
    if not len(v):
        return False, "no geometry"
    lo, hi = float(v[:, 2].min()) - floor, float(v[:, 2].max()) - floor
    edge = v[v[:, 1] >= float(v[:, 1].max()) - GROUND_EDGE_DEPTH_MM]
    edge_top = float(edge[:, 2].max()) - floor
    if hi <= GROUND_LOW_TOP_MM or edge_top <= GROUND_LOW_TOP_MM:
        return True, f"`{b.id}` front edge top {edge_top:.1f} mm above the floor"
    if hi - lo <= GROUND_THIN_MM and lo <= GROUND_LOW_TOP_MM:
        return True, f"`{b.id}` is a {hi - lo:.1f} mm plate on the floor"
    return False, f"`{b.id}` front edge top is {edge_top:.1f} mm above the floor (ground game needs <= {GROUND_LOW_TOP_MM:.0f})"


def swept_front_y(wb, origin, axis):
    """Front-most Y of the weapon's swept volume (the full rim circle, not the current tooth position)."""
    v = wb.mesh.vertices
    R = float(perp_radius(v, origin, axis).max()) if len(v) else 0.0
    half = float(np.abs((v - origin) @ axis).max()) if len(v) else 0.0
    a = np.asarray(axis, float)
    fwd = FRONT - (FRONT @ a) * a
    return float(origin[1] + R * np.linalg.norm(fwd) + half * abs(float(a[1])))


def front_intrusions(ctx, tip, bodies, floor, tol=0.5):
    """Parts reaching ahead of the weapon front `tip` (Y) by more than they may. Returns (bad, ground) where
    bad = [(body, lead_mm, allowed_mm, why)] and ground = [(body, lead_mm)] for ground-game parts (any lead, for reporting)."""
    mx = ground_lead_max(ctx)
    bad, ground = [], []
    for b in bodies:
        if b.fastener or b.is_wire:
            continue
        lead = float(b.mesh.vertices[:, 1].max()) - tip
        gg, why = is_ground_game(ctx, b, floor)
        if gg:
            ground.append((b, lead))
        allowed = mx if gg else tol
        if lead > allowed:
            bad.append((b, lead, allowed, why))
    return bad, ground


def blade_stack(ctx, rotor_ids, origin, axis):
    """Axial thickness (mm) of the weapon blade stack: rotor parts of kind `weapon` (or `role: blade`), excluding the motor,
    spider, hub and shaft. None when no blade body is found."""
    w = ctx.world
    ts = []
    for pid in rotor_ids:
        b = w.body(pid)
        if b is None or b.fastener:
            continue
        p = part(ctx, b)
        role = (getattr(p, "_extra", {}).get("role") or "") if p is not None else ""
        if role in ("spider", "hub", "spacer") or (b.kind != "weapon" and role != "blade"):
            continue
        ts.append((b.mesh.vertices - origin) @ axis)
    if not ts:
        return None
    t = np.concatenate(ts)
    return float(t.max() - t.min())


def rotor_mass(ctx, wid):
    """(grams, rotor part ids, bell grams) of everything that turns with weapon `wid`: the rotor parts (blade stack,
    spacer, hub, shaft, rotor nuts) plus, when an outrunner's bell carries the rotor (motor-as-hub / drisk), the bell share
    of that motor (`bell_mass_frac` catalog prop, default 0.5). None when a part mass is unknown."""
    from .archetype import _bell_carries, rotor_set

    spec = ctx.r.spec
    rot = rotor_set(spec, wid)
    masses = [ctx.metrics.get(f"part_mass_g.{x}") for x in rot]
    if any(m is None for m in masses):
        return None
    bell = 0.0
    wp = spec.part(wid)
    mid = wp.weapon.motor if wp is not None and wp.weapon is not None else None
    if mid and _bell_carries(spec, mid, rot):
        rp = next((q for q in ctx.r.parts if q.part.id == mid), None)
        if rp is not None and rp.cat is not None and rp.cat.kind == "weapon_motor":
            mm = ctx.metrics.get(f"part_mass_g.{mid}", rp.cat.mass_g)
            bell = float(rp.cat.props.get("bell_mass_frac", 0.5)) * float(mm or 0.0)
    return sum(masses) + bell, sorted(rot), bell
