"""The printed clamshell: outline extruded per half, hollowed to a wall + floor/roof, plus housings, minus cavities.

Order (each a separate step so the generators stay independent):
  outer prism - inner prism  ->  + housings and added solids  ->  - cavities and cuts  ->  - late cuts (bolt bores).
"""

from __future__ import annotations

from ..intent import I, chamfer_for
from ..layout import geom
from . import pockets as pk_mod
from . import sh


def _outline_prism(points, z0, z1, spline):
    return sh.prism(points, z1 - z0, (0, 0, (z0 + z1) / 2), spline=spline)


EDGE_CHAMFER = chamfer_for("print")  # belly and roof perimeter bevel (wall 1.6 + floor >= 1.1 keeps >= 1 mm through the corner)


def _ccw(poly) -> list:
    pts = list(poly.exterior.coords)[:-1]
    if poly.exterior.is_ccw is False:
        pts.reverse()
    return [(round(x, 3), round(y, 3)) for x, y in pts]


def _outer_body(f, z0, z1, bevel_low: bool):
    """The half's outer solid: the outline extruded, with the outside face (belly or roof) bevelled all round."""
    c = EDGE_CHAMFER
    if f.spline or c <= 0 or z1 - z0 < 3 * c:
        return _outline_prism(f.outline, z0, z1, f.spline)
    full = _ccw(geom.polygon(f.outline))
    small = _ccw(geom.inset(f.outline, c))
    if len(small) != len(full):
        return _outline_prism(f.outline, z0, z1, f.spline)
    i0 = min(range(len(small)), key=lambda i: (small[i][0] - full[0][0]) ** 2 + (small[i][1] - full[0][1]) ** 2)
    small = small[i0:] + small[:i0]
    if max((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 for a, b in zip(small, full)) > (3 * c) ** 2:
        return _outline_prism(f.outline, z0, z1, f.spline)
    zs = [(z0, small), (z0 + c, full), (z1, full)] if bevel_low else [(z0, full), (z1 - c, full), (z1, small)]
    return sh.loft([{"z": sh.r(z), "points": [[x, y] for x, y in pts], "spline": False} for z, pts in zs], ruled=True)


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
    tub = sh.S(_outer_body(f, z0, z1, half == "bottom"), _outline_prism(inner_outline(f), iz0, iz1, f.spline))
    housings = []
    for p in plan.pockets:
        if p.housing > 0 and half in p.halves:
            x0_, x1_, y0_, y1_ = p.outer()
            hz0, hz1 = z0, z1
            if half == "top" and p.z1 + p.housing < z1 - f.floor - 1.0:  # short part: a lid over it, no solid block to the roof
                hz1 = p.z1 + p.housing
            if half == "bottom" and p.z0 - p.housing > z0 + f.floor + 1.0:
                hz0 = p.z0 - p.housing
            if hz1 - hz0 > 0.5:
                housings.append(sh.boxr(x0_, x1_, y0_, y1_, hz0, hz1))
    body = sh.U(tub, *housings, *plan.adds[half])
    cavities = [pk_mod.cavity(p) for p in plan.pockets]
    body = sh.S(body, *cavities, *plan.cuts[half])
    return sh.S(body, *plan.late_cuts[half])


def _slab(f, z0, z1):
    return _outline_prism(f.outline, z0, z1, f.spline)


def add_tub(plan, material="nylon", color="#23262b"):
    """Open tub + base panel + top sheet: the same walls, housings and cuts as the clamshell, but the floor and the roof
    are separate screwed sheets (Revron). Every pocket is open upward to the top sheet so its part drops in from above;
    the sheets close it. The base panel gives service access to the drive and electronics without touching the weapon."""
    f = plan.frame
    for p in plan.pockets:  # open every pocket up to the top sheet: the part drops in, the sheet holds it down
        p.z1 = max(p.z1, f.zt - f.floor + 0.01)
    full = sh.U(half_shape(plan, "bottom"), half_shape(plan, "top"))
    # the sheets sit inside the side walls (the walls run full height): no sheet edge is left as a sliver beside the
    # wheel slots, and a side hit lands on the tub, not on a sheet edge
    from shapely.geometry import Polygon as _P
    inner = _ccw(_P(f.outline).buffer(-f.wall, join_style=2))
    top_slab = _outline_prism(inner, f.zt - f.floor, f.zt + 40.0, f.spline)
    base_slab = _outline_prism(inner, f.zb - 40.0, f.zb + f.floor, f.spline)
    tub = sh.S(full, top_slab, base_slab)
    lid = {"type": "intersect", "items": [full, top_slab]}
    base = {"type": "intersect", "items": [full, base_slab]}
    parts = [
        {"id": "tub", "kind": "structure", "material": material, "process": "fdm", "shape": tub, "color": color,
         "print_orientation": "+z"},
        {"id": "base_panel", "kind": "structure", "material": material, "process": "fdm", "shape": base, "color": color,
         "print_orientation": "+z"},
        {"id": "lid", "kind": "structure", "material": material, "process": "fdm", "shape": lid, "color": "#2f3238",
         "print_orientation": "-z"},
    ]
    for p in parts:
        p.update(at=[0.0, 0.0, 0.0], rot=[0.0, 0.0, 0.0])
    plan.parts[:0] = parts
    plan.feature("part", I("load_path", "open tub: perimeter wall, motor and wheel housings and every pocket in one "
                           "print, so the drive and weapon loads close through one piece", "walls 1.6 mm; open top and bottom"),
                 target="tub")
    plan.feature("part", I("service", "base panel: screwed under the tub; off in 4 screws for the drive and electronics "
                           "without touching the weapon module (Revron RV26)", f"{f.floor} mm sheet = print minimum skin"),
                 target="base_panel")
    plan.feature("part", I("protection", "top sheet: closes the pockets (holds every part down) and carries the wheel "
                           "guards; screwed on, so the bay opens without disturbing the drive", f"{f.floor} mm sheet"),
                 target="lid")
    plan.feature("wall", I("protection", "perimeter wall: the armour every side hit lands on, and the beam that ties the "
                           "front (weapon) to the rear (drive)", plan.extra.get("wall_basis", f"{f.wall} mm")),
                 target="chassis", half="both")
    plan.feature("bevel", I("protection", "belly and top edges bevelled: removes the elephant's-foot lip and gives a hit "
                            "on the corner a ramp to slide off", f"chamfer {EDGE_CHAMFER} mm (print rule)"),
                 target="chassis", half="both")


def add_shell(plan, material="nylon", color="#23262b"):
    """Turn the plan's chassis features into the two printed halves (first structure part = chassis root)."""
    if plan.is_tub:
        return add_tub(plan, material, color)
    bottom = {"id": "chassis_bottom", "kind": "structure", "material": material, "process": "fdm",
              "shape": half_shape(plan, "bottom"), "color": color, "print_orientation": "+z"}
    top = {"id": "chassis_top", "kind": "structure", "material": material, "process": "fdm",
           "shape": half_shape(plan, "top"), "color": color, "print_orientation": "-z"}
    for p in (top, bottom):
        p.setdefault("at", [0.0, 0.0, 0.0])
        p.setdefault("rot", [0.0, 0.0, 0.0])
    plan.parts[:0] = [bottom, top]
    f = plan.frame
    plan.feature("part", I("load_path", "bottom half: floor, perimeter wall and every pocket; the drive and weapon loads "
                           "close through it", "split at the axle plane so motors and wheels drop in from above"),
                 target="chassis_bottom")
    plan.feature("part", I("protection", "top half: roof and upper wall close the electronics bay against hits from "
                           "above; it lifts off for service", "split at z = 0; printed roof-down (flat face on the bed)"),
                 target="chassis_top")
    plan.feature("wall", I("protection", "perimeter wall: the armour every side hit lands on, and the beam that ties the "
                           "front (weapon) to the rear (drive)", plan.extra.get("wall_basis", f"{f.wall} mm")),
                 target="chassis", half="both")
    plan.feature("floor", I("load_path", "floor and roof skins: shear webs that keep the box square; they carry no "
                            "direct hits", f"{f.floor} mm = 5 layers at 0.2 mm (print minimum skin)"),
                 target="chassis", half="both")
    plan.feature("bevel", I("protection", "belly and roof edges bevelled: removes the elephant's-foot lip on the bed "
                            "face and gives a hit on the corner a ramp to slide off", f"chamfer {EDGE_CHAMFER} mm (print rule)"),
                 target="chassis", half="both")
