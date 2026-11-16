"""Rest / dead-pose analysis (`rest.*`, F3).

WHY: when power is cut - the match ends, the link drops, an ESC faults - the weapon coasts
to a stop at an unknowable angle. If some rotation of the weapon reaches the floor, the
dead robot props itself on its own blade: the wheels lift, it cannot be driven off, and
the tip digs into an arena seam. The sweep is exact and cheap: rotating about its spin
axis, each vertex of a weapon body traces a circle of radius r in a plane normal to the
axis, centred at c; that circle's lowest point is c_z - r*sqrt(1 - a_z^2), so the weapon's
lowest possible rest height is the minimum over vertices - no angular stepping needed.
"""

from __future__ import annotations

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from . import _physics as ph

G = "rest"


def swept_lowest(body, origin, axis) -> float:
    """Lowest z the body can reach at some rotation angle about (origin, axis)."""
    ax = np.asarray(axis, float)
    tilt = float(np.sqrt(max(1.0 - ax[2] * ax[2], 0.0)))
    q = np.asarray(body.mesh.vertices, float) - origin
    t = q @ ax
    perp = np.linalg.norm(q - np.outer(t, ax), axis=1) if len(q) else np.zeros(0)
    cz = origin[2] + t * ax[2]
    return float(np.min(cz - perp * tilt)) if len(q) else float("inf")


def weapon_bodies(ctx):
    """[(body_index, body, (origin, axis))] of every body whose part is a weapon."""
    out = []
    for i, b in enumerate(ctx.world.bodies):
        p = ph.part(ctx, b)
        if p is not None and p.weapon is not None:
            from .power import spin_axis

            sa = spin_axis(ctx.world, ctx.r, i)
            if sa is not None:
                out.append((i, b, sa))
    return out


def run(ctx):
    r = ctx.r
    out = []
    weapons = weapon_bodies(ctx)
    if not weapons:
        ctx.not_checked.append("Rest pose: no weapon body with a spin axis, the dead-pose sweep is not judged")
        return out
    floor = ph.floor_z(ctx)
    worst = None
    for _i, b, (origin, axis) in weapons:
        z = swept_lowest(b, origin, axis)
        if worst is None or z < worst[1]:
            worst = (b, z)
    b, z = worst
    gap = z - floor
    ctx.metrics["rest.weapon_min_z_mm"] = round(z, 2)
    ctx.metrics["rest.weapon_gap_mm"] = round(gap, 2)
    mc = float(r.profile.min_ground_clearance_mm)
    if gap < -0.1:
        out.append(fail("rest.weapon_drag", G, BLOCKER, "Weapon can prop the robot on the floor",
                        f"`{b.id}` reaches {z:.2f} mm at some rest angle, {abs(gap):.2f} mm below the floor plane "
                        f"(z = {floor:.2f} mm): the dead robot rests on its own weapon, the wheels lift and the tip digs in.")
                   .on(b.id).expect("above the floor at every rest angle", f"{gap:.2f} mm")
                   .fix("Raise the weapon on its shaft, or move the spin axis up; a weapon that reaches the floor "
                        "at some rest angle props the dead robot on its blade."))
    elif gap < mc:
        out.append(fail("rest.weapon_graze", G, WARNING, "Weapon sweeps close to the floor",
                        f"`{b.id}` comes within {gap:.2f} mm of the floor at some rest angle (want >= {mc:.1f} mm); "
                        f"parked on a seam or a bump, the dead weapon scrapes and snags.")
                   .on(b.id).expect(f">= {mc:.1f} mm", f"{gap:.2f} mm")
                   .fix("Raise the weapon a little, or accept the scrape only if the arena is flat where you fight."))
    else:
        out.append(ok("rest.ok", G, "Weapon clears the floor at every rest angle",
                      f"Lowest weapon point over the full sweep is {gap:.2f} mm above the floor "
                      f"({len(weapons)} weapon bod{'y' if len(weapons) == 1 else 'ies'})."))
    return out
