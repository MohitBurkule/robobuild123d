"""Standing on the floor: wheels touch it, nothing else drags, the wedge sits at the right height and the centre of mass
is supported (port of ground.rs)."""

from __future__ import annotations

import math

from .. import measure
from ..finding import BLOCKER, WARNING, fail, note, ok

G = "ground"


def _cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull(pts):
    p = sorted(set((float(x), float(y)) for x, y in pts))
    if len(p) < 3:
        return p
    h = []
    for seq in (p, p[::-1]):
        start = len(h)
        for q in seq:
            while len(h) >= start + 2 and _cross(h[-2], h[-1], q) <= 1e-9:
                h.pop()
            h.append(q)
        h.pop()
    return h


def margin(h, c):
    """Smallest distance from `c` to the edges of a convex hull (CCW), negative when outside."""
    if len(h) < 3:
        return -math.inf
    m = math.inf
    for i, a in enumerate(h):
        b = h[(i + 1) % len(h)]
        ln = max(math.hypot(b[0] - a[0], b[1] - a[1]), 1e-9)
        m = min(m, _cross(a, b, c) / ln)
    return m


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    wheels = [b for b in w.bodies if b.kind == "wheel"]
    if not wheels:
        out.append(note("ground.no_wheels", G, "No wheels", "No wheel parts, so ground contact is not checked."))
        ctx.not_checked.append("Ground contact, clearance, wedge height and stance: no wheel parts")
        return out
    lows = [(b, measure.lowest_point(b)) for b in wheels]
    floor = float(r.spec.ground_z) if r.spec.ground_z is not None else min(float(p[2]) for _, p in lows)
    ctx.metrics["ground_z"] = floor
    floating = [(b, float(p[2]) - floor) for b, p in lows if float(p[2]) - floor > 0.5]
    if not floating:
        out.append(ok("ground.wheels_touch", G, "Wheels touch the floor", f"All {len(lows)} wheels reach the floor plane (z = {floor:.2f} mm)."))
    for b, gap in floating:
        out.append(fail("ground.wheel_floating", G, BLOCKER, "Wheel does not touch the floor",
                        f"`{b.id}` is {gap:.2f} mm above the floor; with the other wheels down it would never drive.")
                   .on(b.id).expect("0 mm (within 0.5)", f"{gap:.2f} mm")
                   .fix("Use the same wheel diameter and axle height on every wheel, or add a tyre; a lower wheel carries all the weight."))

    worst, tips = None, []
    for b in w.bodies:
        if b.is_wire or b.kind in ("wheel", "tyre"):
            continue
        p = measure.lowest_point(b)
        if b.kind in ("wedge", "fork"):
            tips.append((b, p))
            continue
        h = float(p[2]) - floor
        if worst is None or h < worst[1]:
            worst = (b.id, h)
    mc = r.profile.min_ground_clearance_mm
    if worst is not None:
        bid, h = worst
        ctx.metrics["min_ground_clearance_mm"] = h
        if h < mc:
            out.append(fail("ground.clearance", G, WARNING, "Body is close to the floor",
                            f"`{bid}` is {h:.2f} mm above the floor; it will scrape on arena seams and ride on the ground when a tyre compresses.")
                       .on(bid).expect(f">= {mc:.1f} mm", f"{h:.2f} mm").fix("Raise the chassis or use a bigger wheel; wedges and forks may go lower."))
        else:
            out.append(ok("ground.clearance", G, "Body clears the floor", f"Lowest body part is {h:.1f} mm above the floor."))
    glo, ghi = r.profile.wedge_gap_mm
    for b, p in tips:
        gap = float(p[2]) - floor
        if gap < glo or gap > ghi:
            out.append(fail("ground.wedge_gap", G, WARNING, "Wedge tip at the wrong height",
                            f"`{b.id}` tip is {gap:.2f} mm above the floor; it should be {glo:.1f} to {ghi:.1f} mm so it slides under opponents without digging in or dragging.")
                       .on(b.id).expect(f"{glo:.1f} to {ghi:.1f} mm", f"{gap:.2f} mm").here(p))
        else:
            out.append(ok("ground.wedge_gap", G, "Wedge tip height is right", f"`{b.id}` tip is {gap:.2f} mm above the floor."))

    if "com_x" not in ctx.metrics:
        ctx.not_checked.append("Stance: no centre of mass from the mass group; the origin was used")
    com = (ctx.metrics.get("com_x", 0.0), ctx.metrics.get("com_y", 0.0))
    support = [(float(b.M[0, 3]), float(p[1])) for b, p in lows]
    wheel_y = sum(float(p[1]) for _, p in lows) / max(len(lows), 1)
    share = None
    for b, p in tips:
        if float(p[2]) - floor <= 2.0:
            support += [(float(b.aabb[0][0]) + 1.0, float(p[1])), (float(b.aabb[1][0]) - 1.0, float(p[1]))]
            span = float(p[1]) - wheel_y
            if abs(span) > 1.0:
                share = min(max((com[1] - wheel_y) / span, 0.0), 1.0)
    h = hull(support)
    m = margin(h, com)
    ctx.metrics["stance_margin_mm"] = m
    if len(h) < 3:
        out.append(fail("ground.stance", G, WARNING, "Robot has no support polygon",
                        "Only two wheel contacts and nothing else can reach the floor; the robot will pitch onto whatever touches first.")
                   .fix("Add a skid, a third wheel, or lower the wedge to within 2 mm of the floor."))
    elif m < 2.0:
        out.append(fail("ground.stance", G, BLOCKER, "Centre of mass is outside the support",
                        f"Centre of mass ({com[0]:.1f}, {com[1]:.1f}) is {m:.1f} mm from the support polygon edge; the robot tips over at rest.")
                   .expect(">= 2 mm inside", f"{m:.1f} mm"))
    else:
        out.append(ok("ground.stance", G, "Stable on the floor", f"Centre of mass is {m:.1f} mm inside the support polygon of wheels and wedge."))
    if share is not None:
        ctx.metrics["wedge_load_frac"] = share
        if share > 0.25:
            out.append(fail("ground.wedge_load", G, WARNING, "Front rests on the wedge",
                            f"About {share * 100:.0f}% of the weight sits on the wedge tip because the centre of mass is ahead of the axle; the tip drags and wears and the drive loses traction.")
                       .fix("Move the battery and motors back, or add a front skid wheel, or put the axle forward."))
    cz = ctx.metrics.get("com_z", 0.0) - floor
    if m > 0.0 and cz > 0.1:
        ctx.metrics["tip_angle_deg"] = math.degrees(math.atan(m / cz))
    return out
