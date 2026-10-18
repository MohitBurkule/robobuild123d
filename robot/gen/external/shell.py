"""The printed clamshell: outline extruded per half, hollowed to a wall + floor/roof, plus housings, minus cavities.

Order (each a separate step so the generators stay independent):
  outer prism - inner prism  ->  + housings and added solids  ->  - cavities and cuts  ->  - late cuts (bolt bores).
"""

from __future__ import annotations

from ..layout import geom
from . import pockets as pk_mod
from . import sh


def _outline_prism(points, z0, z1, spline):
    return sh.prism(points, z1 - z0, (0, 0, (z0 + z1) / 2), spline=spline)


def inner_outline(frame) -> list:
    poly = geom.inset(frame.outline, frame.wall)
    pts = list(poly.exterior.coords)[:-1]
    if poly.exterior.is_ccw is False:
        pts.reverse()
    return [(round(x, 3), round(y, 3)) for x, y in pts]


def half_shape(plan, half: str) -> dict:
    f = plan.frame
    if half == "bottom":
        z0, z1, iz0, iz1 = f.zb, f.split, f.zb + f.floor, f.split + 0.5
    else:
        z0, z1, iz0, iz1 = f.split, f.zt, f.split - 0.5, f.zt - f.floor
    tub = sh.S(_outline_prism(f.outline, z0, z1, f.spline), _outline_prism(inner_outline(f), iz0, iz1, f.spline))
    housings = []
    for p in plan.pockets:
        if p.housing > 0 and half in p.halves:
            x0_, x1_, y0_, y1_ = p.outer()
            hz0, hz1 = z0, z1
            if half == "top" and p.z1 + p.housing < z1 - f.floor - 1.0:  # short part: a lid over it, no solid block to the roof
                hz1 = p.z1 + p.housing
            if half == "bottom" and p.z0 - p.housing > z0 + f.floor + 1.0:
                hz0 = p.z0 - p.housing
            housings.append(sh.boxr(x0_, x1_, y0_, y1_, hz0, hz1))
    body = sh.U(tub, *housings, *plan.adds[half])
    cavities = [pk_mod.cavity(p) for p in plan.pockets]
    body = sh.S(body, *cavities, *plan.cuts[half])
    return sh.S(body, *plan.late_cuts[half])


def add_shell(plan, material="nylon", color="#23262b"):
    """Turn the plan's chassis features into the two printed halves (first structure part = chassis root)."""
    bottom = {"id": "chassis_bottom", "kind": "structure", "material": material, "process": "fdm",
              "shape": half_shape(plan, "bottom"), "color": color, "print_orientation": "+z"}
    top = {"id": "chassis_top", "kind": "structure", "material": material, "process": "fdm",
           "shape": half_shape(plan, "top"), "color": color, "print_orientation": "-z"}
    for p in (top, bottom):
        p.setdefault("at", [0.0, 0.0, 0.0])
        p.setdefault("rot", [0.0, 0.0, 0.0])
    plan.parts[:0] = [bottom, top]
