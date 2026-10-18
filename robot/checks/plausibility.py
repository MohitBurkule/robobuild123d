"""Catalog/declared mass vs envelope plausibility (`plausibility.density`).

Lesson from the Revron reference audit: the "2S 350 mAh" catalog pack had a 36 x 17 x 11 mm box and 21.5 g, i.e.
3.2 g/cm3. Real LiPo packs are 1.2-2.4 g/cm3 (the real 350 mAh pack is 56 x 28 x 13 mm, 24 g). A wrong envelope hides a
packaging problem (the real pack would not fit the tub) and a wrong mass hides a budget problem. Any bought-in part whose
mass / modelled volume falls outside the physical range for its kind is a data error, not a design choice.
"""

from __future__ import annotations

from ..finding import WARNING, fail, ok

G = "plausibility"

# g/cm3 over the modelled (solid) envelope; ranges cover real parts with wrap, cans and air gaps.
RANGES = {
    "battery": (1.0, 2.6),  # LiPo incl. wrap and tabs
    "motor": (1.2, 7.0),  # gearmotor (can + gearbox)
    "weapon_motor": (1.5, 7.5),  # outrunner modelled as a solid cylinder
    "esc": (0.4, 4.0),
    "receiver": (0.3, 3.0),
    "switch": (0.3, 4.0),
}


def run(ctx):
    out = []
    for b in ctx.world.bodies:
        if b.is_wire or b.fastener or b.part_idx is None:
            continue
        rp = ctx.r.parts[b.part_idx]
        kind = rp.part.kind
        if kind not in RANGES:
            continue
        g = ctx.metrics.get(f"part_mass_g.{b.id}")
        if g is None:
            g = rp.cat.mass_g if rp.cat is not None else rp.part.mass_g
        try:
            vol = float(b.geom.volume) / 1000.0
        except Exception:  # noqa: BLE001 - fail closed
            vol = 0.0
        if g is None or vol <= 0:
            ctx.not_checked.append(f"Mass/volume plausibility of `{b.id}`")
            continue
        rho = float(g) / vol
        lo, hi = RANGES[kind]
        ctx.metrics[f"density_g_cc.{b.id}"] = round(rho, 2)
        msg = f"`{b.id}` ({kind}): {float(g):.1f} g in {vol:.2f} cm3 = {rho:.2f} g/cm3 (plausible {lo}-{hi})."
        if lo <= rho <= hi:
            out.append(ok("plausibility.density", G, "Mass fits the envelope", msg).on(b.id))
        else:
            out.append(fail("plausibility.density", G, WARNING, "Mass does not fit the modelled envelope", msg).on(b.id)
                       .fix("Check the datasheet: the envelope (fit, packaging) or the mass (budget) is wrong."))
    return out
