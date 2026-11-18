"""Builder profile check (`builder.*`, group `builder`, E3).

WHY: a design is only as buildable as the person building it. A spec may
declare a top-level `builder` key (a `robot/builders/*.json` preset id, or the
object itself: printer, materials, processes, tools, budget_gbp, skill). This
group judges the design against that bench: every printed part must fit the
declared printer's bed in its declared print orientation, part materials and
processes must be on the shelf, heat-set inserts need a soldering iron and
more than novice skill, machined processes need expert skill, and the
purchasable BOM cost must fit the budget. No `builder` key: NOT CHECKED, the
report is unchanged.
"""

from __future__ import annotations

import numpy as np

from .. import bom_out, builder as builder_mod, mfg_profiles
from ..finding import WARNING, fail, ok
from ._review import x
from .printability import UPS, fdm

G = "builder"


def _oriented_footprint(bounds, up_axis):
    """(bed_x, bed_y, height) of a part printed with `up` pointing at the ceiling."""
    up = UPS.get(up_axis, UPS["+z"])
    flat = [i for i in range(3) if up[i] == 0]
    tall = up.index(next(v for v in up if v != 0))
    lo, hi = np.asarray(bounds, float)
    return float(hi[flat[0]] - lo[flat[0]]), float(hi[flat[1]] - lo[flat[1]]), float(hi[tall] - lo[tall])


def run(ctx):
    key = (getattr(ctx.r.spec, "raw", None) or {}).get("builder")
    out = []
    if not key:
        ctx.not_checked.append("Builder: the spec declares no `builder` profile; machine fit, shelf materials, tools, budget and skill not judged")
        return out
    try:
        b = builder_mod.load(key)
    except KeyError as e:
        out.append(fail("builder.unknown", G, WARNING, "Unknown builder profile", str(e).strip("'")
                       .replace("unknown builder ", "the spec declares builder ")
                       + "; the design was not judged against any bench.")
                   .fix("Use one of the robot/builders/*.json preset ids, or declare the builder object inline."))
        return out
    printer = None
    try:
        printer = mfg_profiles.printer(b.printer) if b.printer else None
    except KeyError:
        out.append(fail("builder.unknown", G, WARNING, "Builder names an unknown printer",
                        f"builder `{b.id}` names printer `{b.printer}`, which is not in robot/mfg_profiles.py.")
                   .fix(f"Set `printer` to one of {[p.id for p in mfg_profiles.PRINTERS]}."))
    inserts = [rp for rp in ctx.r.parts if rp.part.kind == "insert"]

    for rp in ctx.r.parts:
        p = rp.part
        # bed fit of every printed part, in its declared print orientation
        if printer is not None and rp.cat is None and fdm(p):
            po = str(x(p, "print_orientation") or "+z").lower()
            fx, fy, h = _oriented_footprint(rp.geom.bounds, po if po in UPS else "+z")
            if fx > printer.bed_mm[0] or fy > printer.bed_mm[1] or h > printer.z_mm:
                out.append(fail("builder.bed_fit", G, WARNING, f"Part does not fit the builder's printer",
                                f"`{p.id}` printed {po} needs {fx:.0f} x {fy:.0f} x {h:.0f} mm; `{printer.id}` "
                                f"({printer.make}) is {printer.bed_mm[0]} x {printer.bed_mm[1]} x {printer.z_mm:.0f} mm.")
                           .on(p.id)
                           .fix("Split the part, print it in sections with joints, or move to a bigger machine."))
        # shelf materials
        if b.materials and p.material is not None and p.material not in b.materials:
            out.append(fail("builder.material_unavailable", G, WARNING, "Material not on the builder's shelf",
                            f"`{p.id}` is `{p.material}`; builder `{b.id}` stocks {', '.join(b.materials)}.")
                       .on(p.id)
                       .fix(f"Print it in a stocked material, or add a `{p.material}` spool to the builder profile."))
        # processes the builder can run
        proc = p.process or ("fdm" if fdm(p) else None)
        if b.processes and proc is not None and proc not in b.processes:
            out.append(fail("builder.process_unavailable", G, WARNING, "Process the builder cannot run",
                            f"`{p.id}` needs `{proc}`; builder `{b.id}` can {', '.join(b.processes)}.")
                       .on(p.id)
                       .fix("Redesign the part for a stocked process, or send it out to someone with the machine."))

    # tools: heat-set inserts need a soldering iron
    if inserts and "soldering_iron" not in b.tools:
        out.append(fail("builder.tool_missing", G, WARNING, "Heat-set inserts with no soldering iron on the bench",
                        f"The build uses {len(inserts)} heat-set insert(s) ({', '.join(rp.part.id for rp in inserts[:4])}); "
                        f"builder `{b.id}` has {', '.join(b.tools) or 'no tools listed'}.")
                   .on(*[rp.part.id for rp in inserts[:4]])
                   .fix("Add a soldering iron (and the right tip) to the bench, or switch to captive nuts / self-tap screws."))
    # skill: heat-set inserts need temperature control; machined parts need expert hands
    needs = []
    if inserts:
        needs.append(("intermediate", "heat-set inserts"))
    machined = [rp.part.id for rp in ctx.r.parts if rp.part.process in ("cnc", "turned", "waterjet")]
    if machined:
        needs.append(("expert", "machined parts"))
    for want, what in needs:
        if b.skill_index() < builder_mod.skill_of(want):
                out.append(fail("builder.skill", G, WARNING, "Build needs more skill than the builder has",
                            f"The design needs {what} ({want}); builder `{b.id}` is {b.skill}.")
                       .fix("Practice on scrap first, switch to a simpler fastening, or hand the part to a club member."))
    # budget
    if b.budget_gbp is not None:
        cost = bom_out.cost(bom_out.build(ctx.r))
        ctx.metrics["bom_cost_gbp"] = cost
        if cost > float(b.budget_gbp):
                out.append(fail("builder.budget", G, WARNING, "BOM over the builder's budget",
                            f"The purchasable BOM costs GBP {cost:.2f}; builder `{b.id}` has GBP {float(b.budget_gbp):.2f}.")
                       .fix("Reuse parts you own (set `printed: true` / vendor rows), drop spares, or raise the budget."))
    if not out:
        out.append(ok("builder.ok", G, f"Design fits the builder's bench",
                      f"Every part fits `{printer.id}` ({printer.make}), materials and processes are stocked, tools and skill "
                      f"match, and the BOM is within GBP {b.budget_gbp:.2f}." if b.budget_gbp is not None else
                      f"Every part fits `{printer.make}`, materials and processes are stocked, tools and skill match."))
    return out
