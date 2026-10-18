"""Mass and balance, from the B-rep volumes and the catalog, with an honest uncertainty range."""

from __future__ import annotations

import numpy as np

from .. import catalog, xform
from ..finding import BLOCKER, WARNING, MassLine, fail, ok

G = "mass"


def run(ctx):
    r, w = ctx.r, ctx.world
    lines, out, missing = [], [], []
    com, total = np.zeros(3), 0.0
    for b in w.bodies:
        if b.is_wire:
            continue
        if b.fastener:
            grams, tol, source, kind = b.geom.volume * 7.85e-3, 0.05, "fastener", "fastener"
        else:
            if b.part_idx is None:
                continue
            rp = r.parts[b.part_idx]
            p = rp.part
            kind = p.kind
            cal = float(r.spec.calibration.get(kind, 1.0))
            if p.scale_mass_g is not None:
                g, t, src = float(p.scale_mass_g), 0.005, "scale"
            elif p.slicer_mass_g is not None:
                g, t, src = float(p.slicer_mass_g), 0.06, "slicer"
            elif rp.cat is not None:
                g, t, src = rp.cat.mass_g, {"measured": 0.015, "datasheet": 0.03}.get(rp.cat.confidence, 0.15), "catalog"
            elif catalog.density(p.material) is not None:
                printed = catalog.is_printed(p.process) if p.process else False
                frac = p.solid_fraction if p.solid_fraction is not None else (0.85 if printed else 1.0)
                g, t, src = b.geom.volume * 1e-3 * catalog.density(p.material) * frac, (0.2 if printed else 0.04), "computed"
            elif p.mass_g is not None:
                g, t, src = float(p.mass_g), 0.15, "declared"
            else:
                missing.append(p.id)
                continue
            if p.mass_g is not None and rp.cat is not None and abs(p.mass_g - rp.cat.mass_g) > 0.1 * max(rp.cat.mass_g, 0.1):
                out.append(fail("mass.declared_vs_catalog", G, WARNING, "Declared mass disagrees with the catalog",
                                f"`{p.id}`: declared {p.mass_g:.1f} g, catalog {rp.cat.mass_g:.1f} g; the catalog value is used.").on(p.id))
            grams, tol, source = g * cal, t, src
        com += xform.apply(b.M, b.geom.centroid) * grams
        total += grams
        ctx.metrics[f"part_mass_g.{b.id}"] = grams
        lines.append(MassLine(b.id, kind, grams, grams * tol, source))
    for pid in missing:
        out.append(fail("mass.unknown", G, BLOCKER, "Mass cannot be determined", f"`{pid}` has no catalog entry, material or `mass_g`.").on(pid)
                   .fix("Set `material` (and `process`), or `slicer_mass_g` / `scale_mass_g`."))
    wire_g = ctx.metrics.get("wire_mass_g")
    if wire_g is None:
        wire_g = estimate_wire_length(ctx) * 0.0022
    if wire_g > 0:
        lines.append(MassLine("wires", "wire", wire_g, wire_g * 0.3, "wire"))
        total += wire_g
    allow = r.profile.allowance_g
    lines.append(MassLine("allowance", "allowance", allow, allow * 0.5, "declared"))
    total += allow
    tol = sum(l.tol_g for l in lines)
    limit = r.profile.mass_limit(r.spec.locomotion == "roller")
    lo, hi = total - tol, total + tol
    ctx.metrics.update({"mass_total_g": total, "mass_lo_g": lo, "mass_hi_g": hi, "mass_limit_g": limit})
    body = total - allow - wire_g
    if body > 1e-9:
        c = com / body
        ctx.metrics.update({"com_x": float(c[0]), "com_y": float(c[1]), "com_z": float(c[2])})
    est = sum(l.tol_g for l in lines if l.source in ("catalog", "declared"))
    msg = (f"{total:.1f} g (range {lo:.1f} to {hi:.1f} g) against the {limit:.0f} g limit; {est:.1f} g of the uncertainty is catalog "
           "estimates, weigh the real parts and set `scale_mass_g`.")
    if lo > limit or total > limit:
        out.append(fail("mass.over", G, BLOCKER, "Over the weight limit", msg).expect(f"<= {limit:.0f} g", f"{total:.1f} g")
                   .fix("Hollow structure, thin walls, smaller battery or motor; biggest masses are listed in the report."))
    elif hi > limit:
        out.append(fail("mass.may_be_over", G, BLOCKER if ctx.opts.strict_catalog else WARNING, "May be over the weight limit", msg)
                   .expect(f"<= {limit:.0f} g", f"{total:.1f} g (up to {hi:.1f})")
                   .fix("Weigh real parts and set `scale_mass_g`, or remove mass until the upper bound fits."))
    else:
        out.append(ok("mass.ok", G, "Within the weight limit", msg).expect(f"<= {limit:.0f} g", f"{total:.1f} g"))
    ctx.mass_lines = lines
    return out


def estimate_wire_length(ctx):
    total = 0.0
    for wdef in ctx.r.spec.wires:
        a, b = ctx.world.port(ctx.r, getattr(wdef, "from")), ctx.world.port(ctx.r, wdef.to)
        if a is not None and b is not None:
            total += float(np.abs(b - a).sum()) * 1.15 + (wdef.slack_mm if wdef.slack_mm is not None else 8.0)
    return total
