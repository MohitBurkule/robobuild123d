"""Between-fight serviceability (`service.*`, F6).

WHY: between fights you have minutes: swap the battery, change a bent weapon, replace a
torn wheel. The disassembly graph (`disasm.*`, full tier) knows how many removals a part
needs; this group answers the cheaper question first - can the part come out along one
straight line without taking anything else off? A battery that pulls straight up out of
an open hatch is a 10-second swap; one that needs the lid unscrewed costs a match.

Straight line means: rays from the part's own surface along the direction reach open air
without hitting any other solid body (screws included - a screw through the strap blocks
the pull). The candidate directions are the 6 axis directions and the 8 space diagonals.
"""

from __future__ import annotations

import numpy as np

from .. import measure
from ..finding import WARNING, fail, ok

G = "service"
MAX_RAY_MM = 400.0
SURF_STEP_MM = 1.5
SERVICE_KINDS = ("battery", "weapon", "wheel")


def _dirs():
    out = [np.array([s, 0, 0], float) for s in (1, -1)]
    out += [np.array([0, s, 0], float) for s in (1, -1)]
    out += [np.array([0, 0, s], float) for s in (1, -1)]
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                out.append(np.array([sx, sy, sz], float) / np.sqrt(3.0))
    return out


DIRS = _dirs()


def extract_dir(ctx, bodies, others):
    """First direction along which the bodies come out without hitting another solid, or None."""
    pts = []
    for b in bodies:
        p = b.surface(SURF_STEP_MM)[0]
        pts.append(np.asarray(p, float)[:: max(len(p) // 60, 1)])
    if not pts:
        return None
    pts = np.vstack(pts)
    scene = measure.Scene(others)
    for d in DIRS:
        o = pts + d * 0.6
        inside = np.zeros(len(o), bool)
        for b in bodies:
            inside |= b.inside(o)
        if inside.all():
            continue
        o = o[~inside]
        dist, _ = scene.first_hit(o, np.tile(d, (len(o), 1)), MAX_RAY_MM)
        if not np.isfinite(dist).any():
            return d
    return None


def _targets(ctx):
    """{part kind: [(part, bodies)]} of the service-relevant parts that were built."""
    out = {}
    for rp in ctx.r.parts:
        kind = rp.part.kind
        if kind not in SERVICE_KINDS:
            continue
        bodies = [b for b in ctx.world.bodies
                  if b.part_idx is not None and ctx.r.parts[b.part_idx].part is rp.part and not b.is_wire]
        if bodies:
            out.setdefault(kind, []).append((rp.part, bodies))
    return out


def run(ctx):
    w = ctx.world
    out = []
    targets = _targets(ctx)
    if not targets:
        ctx.not_checked.append("Service: no battery, weapon or wheel parts built, straight-line extraction not judged")
        return out
    blocked = 0
    for kind, entries in targets.items():
        stuck = []
        for p, bodies in entries:
            others = [b for b in w.bodies if not b.is_wire and not any(b is x for x in bodies)]
            d = extract_dir(ctx, bodies, others)
            if d is None:
                stuck.append(p.id)
            else:
                ctx.metrics[f"service.extract.{p.id}"] = [round(float(x), 2) for x in d]
        if not stuck:
            continue
        blocked += 1
        detail = (f"`{', '.join(stuck)}` has no straight extraction path: every direction is blocked by another "
                  f"part, so the swap needs other parts removed first.")
        hint = "Give it an open hatch or slot on one face so it slides out without disassembly; between-fight swaps must be quick."
        if kind == "battery":
            out.append(fail("service.battery_pull", G, WARNING, "Battery cannot be pulled out straight", detail)
                       .on(*stuck).fix("Give the battery an open hatch or slot on one face so it slides out without "
                                       "disassembly; a pack swap between fights must take seconds, not minutes."))
        elif kind == "weapon":
            out.append(fail("service.weapon_pull", G, WARNING, "Weapon cannot be pulled out straight", detail)
                       .on(*stuck).fix(hint))
        else:
            out.append(fail("service.wheel_pull", G, WARNING, "Wheel cannot be pulled out straight", detail)
                       .on(*stuck).fix(hint))
    if not blocked:
        kinds = ", ".join(sorted(targets))
        out.append(ok("service.ok", G, "Service parts come out along a straight line",
                      f"Every {kinds} part has at least one unobstructed straight extraction direction."))
    return out
