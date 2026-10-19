"""print.orientation_declared: every printed (FDM) part declares `print_orientation` (the part-frame axis pointing up
from the bed), and the overhang / bridge analysis runs in THAT orientation, not the best of six. A part whose declared
orientation leaves more than `review.print.max_overhang_mm2` (default printability.MAX_OVERHANG_MM2) of unsupported
overhang fails, naming the better orientation when there is one. `printability` keeps reporting the best-case.
"""

from __future__ import annotations

from ..finding import BLOCKER, WARNING, fail, ok
from ._review import params, x
from .printability import MAX_BRIDGE_MM, MAX_OVERHANG_MM2, OVERHANG_DEG, UPS, analyse, fdm

G = "print_orient"


def run(ctx):
    r, w = ctx.r, ctx.world
    lim = float(params(r.spec, "print", {"max_overhang_mm2": MAX_OVERHANG_MM2})["max_overhang_mm2"])
    out, n = [], 0
    for rp in r.parts:
        p = rp.part
        if rp.cat is not None or not fdm(p):
            continue
        po = str(x(p, "print_orientation") or "").lower()
        if po not in UPS:
            out.append(fail("print.orientation_declared", G, BLOCKER, "Printed part has no print orientation",
                            f"`{p.id}` is printed but declares no valid `print_orientation` ({po or 'none'}), so its overhangs "
                            "and layer direction are guesses.").on(p.id)
                       .fix("Add `print_orientation`: +x/-x/+y/-y/+z/-z, the part-frame axis pointing up from the bed."))
            continue
        mesh = rp.geom.mesh
        area, span, pt = analyse(mesh, UPS[po])
        ctx.metrics[f"print_declared_overhang_mm2.{p.id}"] = area
        if area > lim or span > MAX_BRIDGE_MM:
            best = min(UPS, key=lambda k: analyse(mesh, UPS[k])[0])
            ba = analyse(mesh, UPS[best])[0]
            b = w.body(p.id)
            wpt = b.M[:3, :3] @ pt + b.M[:3, 3] if (pt is not None and b is not None) else None
            out.append(fail("print.orientation_declared", G, WARNING, "Declared print orientation needs support",
                            f"`{p.id}` printed build-up {po} (as declared) leaves {area:.0f} mm² of overhang steeper than "
                            f"{OVERHANG_DEG:.0f}°{f' and a {span:.1f} mm bridge' if span > MAX_BRIDGE_MM else ''}"
                            + (f"; build-up {best} would leave {ba:.0f} mm²." if best != po else "."))
                       .on(p.id).here(wpt).expect(f"<= {lim:.0f} mm²", f"{area:.0f} mm²")
                       .fix("Chamfer the overhangs for the declared orientation, or change `print_orientation`."))
        else:
            n += 1
    if n:
        out.append(ok("print.orientation_declared", G, "Print orientations declared",
                      f"{n} printed parts declare an orientation that prints without support."))
    return out
