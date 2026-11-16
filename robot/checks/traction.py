"""COM over the drive contact patch (`traction.*`, G9).

WHY: `dynamics.traction` splits the static weight between the wheel contacts
and the skids, but push balance needs more: the centre of mass must project
INSIDE the polygon of the driven wheels' floor contacts, with margin. A COM
over the skid or at the patch edge means the first hard push tips the robot
onto its nose or tail, the driven wheels unload, and it spins in place.
"""

from __future__ import annotations

import numpy as np

from ..finding import WARNING, fail, ok
from ._physics import floor_z, part
from .ground import hull, margin

G = "traction"
CONTACT_MM = 2.0  # same as dynamics: wheel vertices this close to the floor carry load
MIN_MARGIN_MM = 5.0
MIN_MARGIN_FRAC = 0.1  # of the patch's smaller half-extent


def _driven_contacts(ctx, floor):
    """[(x, y)] floor-contact points of the driven wheels."""
    pts = []
    for b in ctx.world.bodies:
        if b.fastener or b.kind != "wheel":
            continue
        p = part(ctx, b)
        if p is not None and not p._extra.get("driven", True):
            continue
        v = b.mesh.vertices
        low = v[v[:, 2] <= floor + CONTACT_MM]
        if len(low):
            pts.extend((float(q[0]), float(q[1])) for q in low)
    return pts


def run(ctx):
    out = []
    if "com_x" not in ctx.metrics or "com_y" not in ctx.metrics:
        ctx.not_checked.append("Traction patch: no centre of mass from the mass group; COM over the drive patch not judged")
        return out
    floor = floor_z(ctx)
    pts = _driven_contacts(ctx, floor)
    if not pts:
        ctx.not_checked.append("Traction patch: no driven wheel touches the floor; COM over the drive patch not judged")
        return out
    hl = hull(pts)
    if len(hl) < 3:
        ctx.not_checked.append("Traction patch: the driven-wheel contacts do not form a patch (fewer than 3 distinct points)")
        return out
    com = (float(ctx.metrics["com_x"]), float(ctx.metrics["com_y"]))
    m = margin(hl, com)
    xs = [p[0] for p in hl]
    ys = [p[1] for p in hl]
    half = min(max(xs) - min(xs), max(ys) - min(ys)) / 2.0
    ctx.metrics["drive_patch_margin_mm"] = round(m, 2)
    ctx.metrics["com_in_drive_patch"] = m >= 0.0
    if m < 0.0:
        out.append(fail("traction.com_outside_patch", G, WARNING, "Centre of mass outside the drive contact patch",
                        f"The COM projects {abs(m):.1f} mm outside the polygon of the driven wheels' floor contacts; the weight "
                        f"rests on the skid or wedge instead, so the driven wheels grip only with the load they have left and "
                        f"the robot pivots under a hard push.")
                   .fix("Move mass (battery, weapon) over the driven wheels, or lift the skid so only the wheels touch at rest."))
    elif m < max(MIN_MARGIN_MM, MIN_MARGIN_FRAC * half):
        out.append(fail("traction.patch_margin", G, WARNING, "Centre of mass at the edge of the drive contact patch",
                        f"The COM is only {m:.1f} mm inside the driven-wheel patch (patch half-extent {half:.1f} mm); the first "
                        f"hard push unloads the driven wheels.")
                   .fix("Shift heavy parts toward the patch centre, or widen the wheel stance for more margin."))
    else:
        out.append(ok("traction.ok", G, "Centre of mass sits over the drive contact patch",
                     f"COM is {m:.1f} mm inside the driven-wheel contact patch (half-extent {half:.1f} mm); pushing keeps the "
                     f"load on the driven wheels."))
    return out
