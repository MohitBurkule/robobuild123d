"""Checks every spinning weapon must pass: bearing support, reach, exposure, invertibility, mass share (port of spinner.rs).
Anything not judged goes into ctx.not_checked so a clean report is never read as "safe"."""

from __future__ import annotations

import numpy as np

from .. import measure
from ..finding import BLOCKER, WARNING, fail, note, ok
from . import _physics as ph
from .power import spin_axis

G = "spinner"
SPINS = ("spinner", "drum", "disc", "bar")
SUPPORT = ("structure", "plate", "fork", "armor")
MIN_HOLD_MM = 3.0
LEAD_KINDS = ("wedge", "structure", "plate", "armor", "fork")  # must sit behind the weapon unless ground game
MAX_SWEEP_HEIGHT_VERTICAL_MM = 5.0  # lowest point of a vertical disc/drum's swept rim above the floor
MAX_SWEEP_HEIGHT_HORIZONTAL_MM = 25.0  # a horizontal blade must still hit at bumper height


def hold_mm(w, shaft, weapon, origin, axis, half, sign) -> float:
    """Millimetres of shaft inside a support body on one side of the weapon (0.25 mm steps)."""
    d = half + np.arange(0, 160) * 0.25
    P = origin + np.outer(sign * d, axis)
    in_shaft = w.bodies[shaft].inside(P)
    sup = [b for j, b in enumerate(w.bodies) if j not in (weapon, shaft) and not b.fastener and (b.kind in SUPPORT or b.kind == "bearing")]
    held = measure.inside_any(sup, P)
    length = 0.0
    for s, h in zip(in_shaft, held):
        if s:
            if h:
                length += 0.25
        elif length > 0:
            break
    return length


def rim(pts, origin, axis) -> float:
    q = pts - origin
    return float(np.linalg.norm(q - np.outer(q @ axis, axis), axis=1).max()) if len(q) else 0.0


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    vertical = r.spec.robot_type in ("vertical_spinner", "drum")
    total = max(ctx.metrics.get("mass_total_g", 150.0), 1.0)
    for rp in r.parts:
        wd = rp.part.weapon
        if rp.part.kind != "weapon" or wd is None or wd.kind not in SPINS:
            continue
        pid = rp.part.id
        i = w.index(pid)
        sa = spin_axis(w, r, i) if i is not None else None
        if sa is None:
            ctx.not_checked.append(f"Spinner `{pid}`: no body or spin axis, bearing/reach/invert checks skipped")
            continue
        origin, axis = sa
        wb = w.bodies[i]
        pts = wb.mesh.vertices  # extremes of a polyhedron are at its vertices
        half = float(np.abs((pts - origin) @ axis).max())
        energy = ctx.metrics.get("weapon_energy_j")

        # Bearing support: one shaft through the weapon centre, gripped by structure on both sides.
        best = (0.0, 0.0, "")
        for j, b in enumerate(w.bodies):
            if b.fastener or b.kind != "shaft" or not b.inside(origin)[0]:
                continue
            a, c = hold_mm(w, j, i, origin, axis, half, 1.0), hold_mm(w, j, i, origin, axis, half, -1.0)
            if min(a, c) >= min(best[0], best[1]):
                best = (a, c, b.id)
        if best[0] >= MIN_HOLD_MM and best[1] >= MIN_HOLD_MM:
            ctx.metrics["weapon_shaft_hold_mm"] = min(best[0], best[1])
            out.append(ok("spinner.bearing", G, "Weapon on a shaft gripped on both sides",
                          f"`{pid}` turns on `{best[2]}`, which sits {best[0]:.1f} mm and {best[1]:.1f} mm in structure or bearings either side (need {MIN_HOLD_MM:.0f})."))
        else:
            escalate = vertical or wd.supported_both_ends or (energy is not None and energy > 20.0)
            why = ("no shaft passes through the weapon centre" if not best[2] else
                   f"shaft `{best[2]}` is held only {best[0]:.1f} mm on one side and {best[1]:.1f} mm on the other (need {MIN_HOLD_MM:.0f} mm each)")
            out.append(fail("spinner.bearing", G, BLOCKER if escalate else WARNING, "Weapon is cantilevered or loosely held",
                            f"`{pid}`: {why}. A hit's side load goes into a hobby motor bearing or a loose shaft.")
                       .on(pid).fix("Run one `shaft` part through the weapon bore and into a hole or bearing seat in structure on both sides (3 mm or more each), forks thick enough to stay stiff (5-6 mm)."))

        # Reach within 30 degrees of straight ahead. Low forks / wedgelets / skirts (ground game) may lead the weapon's
        # swept front by up to the archetype's blade_lead max (one rule shared with shape.weapon_leads and
        # archetype.blade_lead, see _physics.front_intrusions); every other part must stay behind the weapon.
        floor0 = ph.floor_z(ctx)
        cands = [b for j, b in enumerate(w.bodies) if j != i and not b.fastener and not b.is_wire
                 and (b.kind in LEAD_KINDS or ph.is_ground_game(ctx, b, floor0)[0])]
        gg = [b for b in cands if ph.is_ground_game(ctx, b, floor0)[0]]
        gbad, _ = ph.front_intrusions(ctx, ph.swept_front_y(wb, origin, axis), gg, floor0)
        others = [b for b in cands if b not in gg]
        ov = np.vstack([b.mesh.vertices for b in others]) if others else np.zeros((0, 3))
        worst, worst_deg = np.inf, 0.0
        for deg in range(-30, 31, 10):
            a = np.radians(deg)
            dvec = np.array([np.sin(a), np.cos(a), 0.0])
            wr = float((pts @ dvec).max())
            orr = float((ov @ dvec).max()) if len(ov) else -np.inf
            if wr - orr < worst:
                worst, worst_deg = wr - orr, float(deg)
        if np.isfinite(worst):
            ctx.metrics["weapon_reach_lead_mm"] = worst
        if worst < 3.0:
            behind = worst < 0.0
            out.append(fail("spinner.reach", G, BLOCKER if behind else WARNING, "Weapon does not lead the front",
                            f"Looking {worst_deg:.0f} degrees off straight ahead the chassis or a non-ground-game part is {-worst:.1f} mm ahead of `{pid}`; the opponent meets it first.")
                       .on(pid).expect(">= 3 mm lead across +/-30 degrees", f"{worst:.1f} mm")
                       .fix("Cut the wedge back or move the weapon forward until it leads by 5-10 mm across plus or minus 30 degrees."))
        for b, lead, allowed, _ in gbad[:1]:
            out.append(fail("spinner.reach", G, WARNING, "Ground-game part leads the weapon too far",
                            f"`{b.id}` is a low fork/wedgelet but reaches {lead:.1f} mm ahead of `{pid}`'s swept front (allowed {allowed:.0f} mm); "
                            "an opponent rides it without ever meeting the weapon.")
                       .on(b.id, pid).expect(f"<= {allowed:.0f} mm ahead", f"{lead:.1f} mm")
                       .fix("Shorten the fork/wedgelet so it leads the disc by 5-15 mm."))
        # Reach toward the floor: the swept rim must come down to where opponents are (a disc that rides high misses
        # wedges and low robots entirely).
        floor = min(float(b.aabb[0][2]) for b in w.bodies if not b.fastener and not b.is_wire)
        if r.spec.ground_z is not None:
            floor = float(r.spec.ground_z)
        rmax_w = rim(pts, origin, axis)
        az = abs(float(axis[2]))
        swept_low = float(origin[2]) - rmax_w * float(np.sqrt(max(0.0, 1.0 - az * az))) - half * az
        high = swept_low - floor
        ctx.metrics["weapon_sweep_floor_gap_mm"] = high
        lim = MAX_SWEEP_HEIGHT_VERTICAL_MM if vertical else MAX_SWEEP_HEIGHT_HORIZONTAL_MM
        if high > lim:
            out.append(fail("spinner.reach", G, BLOCKER, "Weapon sits too high",
                            f"The lowest point of `{pid}`'s swept rim is {high:.1f} mm above the floor (allowed {lim:.0f} mm); "
                            f"it passes over wedges and low robots.")
                       .on(pid).expect(f"<= {lim:.0f} mm above the floor", f"{high:.1f} mm")
                       .fix("Lower the weapon axle or enlarge the weapon so its rim comes down to the floor plane."))
        elif worst >= 3.0 and not gbad:
            out.append(ok("spinner.reach", G, "Weapon leads and reaches low",
                          f"`{pid}` leads the body by {worst:.1f} mm across +/-30 degrees and its rim comes within {high:.1f} mm of the floor."))

        # Mass share and stored energy.
        wm = ctx.metrics.get(f"part_mass_g.{pid}", 0.0)
        ctx.metrics["weapon_mass_g"] = wm
        ctx.metrics["weapon_mass_fraction"] = wm / total
        if wm / total < 0.20:
            out.append(fail("spinner.mass_share", G, WARNING, "Weapon is a small share of the robot",
                            f"`{pid}` is {wm:.1f} g, {100 * wm / total:.0f}% of {total:.0f} g; spinners that win put 25-40% of the mass into the weapon (warns below 20%).").on(pid))
        if energy is not None:
            per_g = energy / total
            ctx.metrics["weapon_energy_per_robot_g"] = per_g
            if per_g < 0.10:
                out.append(fail("spinner.energy_low", G, WARNING, "Weapon stores little energy",
                                f"`{pid}` stores {energy:.1f} J at 85% speed ({per_g:.2f} J per gram of robot; warns below 0.10, i.e. 15 J at 150 g).")
                           .on(pid).fix("Raise the moment of inertia (larger radius, mass at the rim) before raising rpm."))
            elif per_g < 0.20:
                out.append(note("spinner.energy_modest", G, "Weapon energy is modest", f"`{pid}` stores {energy:.1f} J; top antweight spinners carry 30 J or more.").on(pid))
        else:
            ctx.not_checked.append(f"Spinner `{pid}` stored energy per gram: weapon energy unknown")

        # Invertibility.
        if vertical:
            rest = [b for j, b in enumerate(w.bodies) if j != i and not b.fastener and not b.is_wire and b.kind != "wheel"]
            bot = min(b.aabb[0][2] for b in w.bodies if not b.fastener)
            tops = [b.aabb[1][2] for b in rest] + [b.aabb[1][2] for b in w.bodies if b.kind == "wheel"]
            top = max(tops) if tops else bot
            wlo, whi = float(pts[:, 2].min()), float(pts[:, 2].max())
            upright, flipped = wlo - bot, top - whi
            ctx.metrics["weapon_floor_gap_upright_mm"] = upright
            ctx.metrics["weapon_floor_gap_inverted_mm"] = flipped
            if upright > 2.0 or (r.spec.can_run_inverted and flipped > 2.0):
                out.append(fail("spinner.invert", G, WARNING, "Weapon does not reach the floor both ways up",
                                f"`{pid}` is {upright:.1f} mm above the floor upright and {flipped:.1f} mm below the floor plane when inverted; it must be within 2 mm either way.")
                           .on(pid).fix("Centre the weapon on the body mid-plane and size it so its rim just touches the floor plane either way up."))
            if not r.spec.can_run_inverted:
                out.append(fail("spinner.invert", G, WARNING, "Robot cannot run upside down",
                                "A vertical spinner gets flipped often; if it cannot drive inverted it is out of the fight the first time that happens."))
        out += sweep_near(ctx, i, pid, origin, axis, half, pts)
    out += exposure(ctx)
    return out


def sweep_near(ctx, weapon, pid, origin, axis, half, wpts):
    """Electronics, motors and wires within 3 mm of the weapon's swept volume."""
    w = ctx.world
    rmax = rim(wpts, origin, axis)

    def inside(P):
        q = np.atleast_2d(P) - origin
        ax = q @ axis
        rad = np.linalg.norm(q - np.outer(ax, axis), axis=1)
        return (np.abs(ax) <= half + 3.0) & (rad <= rmax + 3.0)

    out = []
    for j, b in enumerate(w.bodies):
        if j == weapon or b.fastener or b.kind not in ("esc", "battery", "receiver", "servo", "switch", "motor"):
            continue
        ps = b.surface(2.0)[0]
        hit = np.nonzero(inside(ps))[0]
        if len(hit):
            out.append(fail("spinner.sweep_near", G, WARNING, "Part inside the weapon's reach",
                            f"`{b.id}` comes within 3 mm of the swept volume of `{pid}`.")
                       .on(b.id, pid).here(ps[hit[0]]).fix("Move it away from the disc or put an armour wall between."))
    for rt in ctx.routes:
        P = np.asarray(rt.points, float).reshape(-1, 3)
        hit = np.nonzero(inside(P))[0] if len(P) else []
        if len(hit):
            out.append(fail("spinner.sweep_near", G, WARNING, "Wire inside the weapon's reach",
                            f"Wire `{rt.id}` passes within 3 mm of the swept volume of `{pid}`; one hit cuts it.")
                       .on(rt.id, pid).here(P[hit[0]]).fix("Route it inside the chassis, away from the disc."))
    return out


def dirs26():
    v = [np.array([x, y, z], float) for x in (-1, 0, 1) for y in (-1, 0, 1) for z in (-1, 0, 1) if (x, y, z) != (0, 0, 0)]
    return np.array([d / np.linalg.norm(d) for d in v])


def exposure(ctx):
    """Parts and wires that see open air from a surface point in any of 26 directions are not armoured."""
    w = ctx.world
    out = []
    dirs = dirs26()
    solid = [b for b in w.bodies if not b.is_wire]
    for i, b in enumerate(w.bodies):
        if b.fastener or b.kind not in ("weapon_motor", "esc", "battery", "receiver"):
            continue
        pts = b.surface(2.5)[0]
        pts = pts[:: max(len(pts) // 24, 1)]
        O = (pts[:, None, :] + dirs[None, :, :] * 0.6).reshape(-1, 3)
        D = np.tile(dirs, (len(pts), 1))
        src = np.repeat(np.arange(len(pts)), len(dirs))
        leave = ~b.inside(O)  # only rays that leave the part itself
        if not leave.any():
            ctx.not_checked.append(f"Armour exposure of `{b.id}`: no outward rays")
            continue
        O, D, src = O[leave], D[leave], src[leave]
        scene = measure.Scene([o for o in solid if o is not b])
        dist, _ = scene.first_hit(O, D, 400.0)
        open_ = ~np.isfinite(dist)
        frac = open_.sum() / len(O)
        if frac > 0.02:
            f = (fail("spinner.exposed", G, WARNING, "Part sits outside the armour",
                      f"`{b.id}` has a clear path to open air from {frac * 100:.0f}% of its outward rays; a hit or the floor reaches it directly.")
                 .on(b.id).fix("Move it inside the shell or add an armour wall (1.2 mm nylon, or 0.8 mm steel or titanium) on the open side."))
            f.here(pts[src[np.nonzero(open_)[0][0]]])
            out.append(f)
    if ctx.routes:
        scene = measure.Scene(solid)
        side = dirs[np.abs(dirs[:, 2]) < 0.9]
        for rt in ctx.routes:
            P = np.asarray(rt.points, float).reshape(-1, 3)[::2]
            if not len(P):
                continue
            O = (P[:, None, :] + side[None] * 0.8).reshape(-1, 3)
            dist, _ = scene.first_hit(O, np.tile(side, (len(P), 1)), 400.0)
            opened = np.nonzero((~np.isfinite(dist.reshape(len(P), len(side)))).any(axis=1))[0]
            if len(opened):
                out.append(fail("spinner.wire_exposed", G, WARNING, "Wire runs outside the armour",
                                f"Wire `{rt.id}` has a clear line to open air at this point; a hit or the weapon can cut it.")
                           .on(rt.id).here(P[opened[0]]).fix("Route it through the chassis interior or add a wall on the open side."))
    return out
