"""Ground clearance at rest with tyre squash and wedge deflection (`clearance.*`, G8).

WHY: `ground.clearance` measures the robot as built, but at rest the tyres carry the whole
weight and squash, the floor effectively rises and the belly that cleared 1 mm on the bench
scrapes on the flat. A wedge carrying part of the weight (the `ground` group's
`wedge_load_frac`) bends down on its slope; a tip that sat at 0.5 mm digs in.

Models (deliberately simple and stated in the finding): tyre squash is a fraction of the
wheel radius - 8 % for elastomer tyres (TPU/silicone/rubber), 2 % for rigid wheels - from
`rest.tire_squash_mm` in the spec or `tire_squash_mm` on the wheel part. Wedge deflection is
a cantilever: `d = f W L^3 / (3 E I)` with the root section taken from the wedge's own
geometry (width x thickness^3/12 at the back of the slope) and E from the material table.
"""

from __future__ import annotations

import numpy as np

from .. import catalog
from ..finding import WARNING, fail, ok
from . import _physics as ph

G = "clearance"
SQUASH_FRAC = {"elastomer": 0.08, "printed": 0.02}
DEFAULT_SQUASH_FRAC = 0.02
WEDGE_KINDS = ("wedge", "fork")


def tyre_squash(ctx, wheels) -> float:
    """Worst-case squash (mm) among the wheels that carry the robot."""
    forced = (ctx.r.spec.raw.get("rest") or {}).get("tire_squash_mm")
    if forced is not None:
        return float(forced)
    worst = 0.0
    for b in wheels:
        p = ph.part(ctx, b)
        own = (p._extra.get("tire_squash_mm") if p is not None and isinstance(getattr(p, "_extra", None), dict) else None)
        if own is not None:
            worst = max(worst, float(own))
            continue
        radius = float(b.aabb[1][2] - b.aabb[0][2]) / 2.0
        m = catalog.material(ph.material_of(ctx, b))
        frac = SQUASH_FRAC.get(m.cls if m is not None else "", DEFAULT_SQUASH_FRAC)
        worst = max(worst, frac * radius)
    return worst


def root_section(b) -> tuple:
    """(width, thickness, length) of a wedge at the back of its slope (world mm)."""
    lo, hi = b.aabb
    v = np.asarray(b.mesh.vertices, float)
    front = lo[1] + 0.9 * (hi[1] - lo[1])
    back = v[v[:, 1] >= front]
    t = float(back[:, 2].max() - back[:, 2].min()) if len(back) else float(hi[2] - lo[2])
    w = float(hi[0] - lo[0])
    return w, t, float(hi[1] - lo[1])


def wedge_deflection(ctx, mass_g, load_frac, b) -> float:
    """Tip drop (mm) of a loaded wedge, cantilever from the back of its slope."""
    p = ph.part(ctx, b)
    mp = catalog.mech(p.material if p is not None else None)
    if mp is None:
        return float("nan")
    w, t, ln = root_section(b)
    if w <= 0 or t <= 0 or ln <= 0:
        return float("nan")
    i = w * t ** 3 / 12.0
    e_mpa = mp[2] * 1000.0
    force_n = load_frac * mass_g / 1000.0 * ph.G0
    return float(force_n * ln ** 3 / (3.0 * e_mpa * i))


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    wheels = [b for b in w.bodies if b.kind == "wheel" and not b.fastener and not b.is_wire]
    if not wheels:
        ctx.not_checked.append("Clearance at rest: no wheel parts, tyre squash is not judged")
        return out
    mass_g = ctx.metrics.get("mass_total_g")
    if mass_g is None:
        ctx.not_checked.append("Clearance at rest: no total mass from the mass group, squash and wedge load are not judged")
        return out
    floor = ph.floor_z(ctx)
    squash = tyre_squash(ctx, wheels)
    ctx.metrics["clearance.tire_squash_mm"] = round(squash, 2)

    worst = None
    for b in w.bodies:
        p = ph.part(ctx, b)
        if b.is_wire or b.fastener or b.kind in ("wheel", "tyre") or b.kind in WEDGE_KINDS:
            continue
        if p is not None and p.kind in WEDGE_KINDS:
            continue
        z = float(np.asarray(b.mesh.vertices, float)[:, 2].min())
        if worst is None or z < worst[1]:
            worst = (b, z)
    if worst is not None:
        b, z = worst
        gap = z - floor - squash
        ctx.metrics["clearance.body_gap_mm"] = round(gap, 2)
        mc = float(r.profile.min_ground_clearance_mm)
        if gap < mc:
            out.append(fail("clearance.squash", G, WARNING, "Body scrapes the floor once the tyres squash",
                            f"`{b.id}` clears {z - floor:.2f} mm as built, but the tyres squash {squash:.2f} mm under "
                            f"the robot's weight and only {gap:.2f} mm is left (want >= {mc:.1f} mm); it rides on the floor at rest.")
                       .on(b.id).expect(f">= {mc:.1f} mm", f"{gap:.2f} mm")
                       .fix("Raise the chassis, use bigger wheels, or firmer tyres (a printed rim squashes less than a soft one)."))
        else:
            out.append(ok("clearance.squash", G, "Body clears the floor with the tyres squashed",
                          f"Lowest body point keeps {gap:.2f} mm with {squash:.2f} mm of tyre squash (want >= {mc:.1f} mm)."))

    wedges = [b for b in w.bodies if b.kind in WEDGE_KINDS and not b.is_wire]
    if not wedges:
        ctx.not_checked.append("Clearance at rest: no wedge parts, tip deflection is not judged")
        return out
    load_frac = ctx.metrics.get("wedge_load_frac")
    if not load_frac:
        ctx.not_checked.append("Clearance at rest: no wedge load from the ground group, tip deflection is not judged")
        return out
    worst_tip = None
    for b in wedges:
        tip = float(np.asarray(b.mesh.vertices, float)[:, 2].min())
        d = wedge_deflection(ctx, mass_g, load_frac, b)
        if np.isnan(d):
            ctx.not_checked.append(f"Clearance at rest: wedge `{b.id}` material or section unknown, deflection not judged")
            continue
        gap = tip - floor - d
        ctx.metrics[f"clearance.wedge_tip_gap_mm.{b.id}"] = round(gap, 2)
        ctx.metrics[f"clearance.wedge_deflection_mm.{b.id}"] = round(d, 2)
        if worst_tip is None or gap < worst_tip[2]:
            worst_tip = (b, tip, gap, d)
    if worst_tip is None:
        return out
    b, tip, gap, d = worst_tip
    if gap < 0.0:
        out.append(fail("clearance.wedge_deflection", G, WARNING, "Wedge tip digs in under its rest load",
                        f"`{b.id}` sits {tip - floor:.2f} mm up as built, but carries {load_frac * 100:.0f}% of the weight "
                        f"and bends {d:.2f} mm down, {abs(gap):.2f} mm below the floor; the tip ploughs and the drive wheels lift.")
                   .on(b.id).expect("tip stays above the floor", f"{gap:.2f} mm")
                   .fix("Thicken or shorten the wedge, move its support forward, or move mass back off the tip."))
    else:
        out.append(ok("clearance.wedge_deflection", G, "Wedge tip stays up under its rest load",
                      f"Worst tip keeps {gap:.2f} mm above the floor with {d:.2f} mm of deflection under "
                      f"{load_frac * 100:.0f}% of the weight."))
    return out
