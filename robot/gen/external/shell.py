"""The printed clamshell: outline extruded per half, hollowed to a wall + floor/roof, plus housings, minus cavities.

Order (each a separate step so the generators stay independent):
  outer prism - inner prism  ->  + housings and added solids  ->  - cavities and cuts  ->  - late cuts (bolt bores).
"""

from __future__ import annotations

from ..intent import I, chamfer_for
from ..layout import geom
from . import pockets as pk_mod
from . import sh


INNER_R = 1.05  # inside-corner radius of every half (load corners need >= 1.0)


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
    R = INNER_R
    # the open side of the void runs R + 0.5 past the split so rounding never leaves a lip on the split face
    iz0x, iz1x = (iz0, iz1 + R) if half == "bottom" else (iz0 - R, iz1)
    inner = _outline_prism(inner_outline(f), iz0x, iz1x, f.spline)
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
            # a raised tray / short lid must still reach the shell: a hollow skirt (the housing walls continued) down
            # to the floor or up to the roof, so the half is one solid by construction (integrity.solids)
            if hz0 > z0 + 1e-6:
                housings.append(sh.S(sh.boxr(x0_, x1_, y0_, y1_, z0, hz0 + 0.01), sh.boxr(p.x0, p.x1, p.y0, p.y1, z0 - 1, hz0 + 1)))
            if hz1 < z1 - 1e-6:
                housings.append(sh.S(sh.boxr(x0_, x1_, y0_, y1_, hz1 - 0.01, z1), sh.boxr(p.x0, p.x1, p.y0, p.y1, hz1 - 1, z1 + 1)))
    cavities = [pk_mod.cavity(p) for p in plan.pockets]
    # 1. the shell with its housings and bosses, inside corners where they meet the walls filleted R (round_inside);
    # 2. then the pockets and channels, each box with corner reliefs (dogbones) so the part's inside corner there is
    #    an R arc while the box still fits the component square (rounding a pocket would pinch its corners).
    body = sh.S(sh.U(_outer_body(f, z0, z1, half == "bottom"), *housings, *plan.adds[half]), sh.S(inner, *housings, *plan.adds[half]))
    if R > 0:
        body = {"type": "round_inside", "radius": R, "axis": "z", "shape": body}
    body = sh.S(body, *cavities, *plan.cuts[half])
    return sh.S(body, *plan.late_cuts[half])


def _rounded_cut(c, R):
    """Every box of a cut with all its edges filleted R: the part's inside corners round the pocket / channel are R
    arcs by construction. A square component in a pocket with gap g keeps g*sqrt2 - R*(sqrt2 - 1) clear at its edges
    (0.4 gap, R 1.05: 0.13 mm), so nothing pinches."""
    if R <= 0:
        return c
    boxes = c["items"] if c.get("type") == "union" else [c]
    out = []
    for b in boxes:
        if b.get("type") == "place" and b["shape"].get("type") == "box" and not any(b["rot"]):
            r = min(R, min(b["shape"]["size"]) / 2 - 0.05)
            if r >= 0.3:
                b = {"type": "place", "shape": sh.fillet(b["shape"], r), "at": b["at"], "rot": b["rot"]}
        out.append(b)
    return sh.U(*out)


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
                           "print, so the drive and weapon loads close through one piece", "walls 1.6 mm; open top and bottom", threats=["vspin_front", "vspin_side", "vspin_rear", "wall_slam"]),
                 target="tub")
    plan.feature("part", I("service", "base panel: screwed under the tub; off in 4 screws for the drive and electronics "
                           "without touching the weapon module (Revron RV26)", f"{f.floor} mm sheet = print minimum skin", threats=["lifter_flipper", "hazard_snag"]),
                 target="base_panel")
    plan.feature("part", I("protection", "top sheet: closes the pockets (holds every part down) and carries the wheel "
                           "guards; screwed on, so the bay opens without disturbing the drive", f"{f.floor} mm sheet", threats=["crusher_hammer", "debris", "flip_landing"]),
                 target="lid")
    plan.feature("wall", I("protection", "perimeter wall: the armour every side hit lands on, and the beam that ties the "
                           "front (weapon) to the rear (drive)", plan.extra.get("wall_basis", f"{f.wall} mm"), threats=["vspin_side", "vspin_front", "vspin_rear", "wall_slam", "hspin_floor", "grabber"]),
                 target="chassis", half="both")
    plan.feature("bevel", I("protection", "belly and top edges bevelled: removes the elephant's-foot lip and gives a hit "
                            "on the corner a ramp to slide off", f"chamfer {EDGE_CHAMFER} mm (print rule)", threats=["wall_slam", "vspin_front", "grabber"]),
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
                           "close through it", "split at the axle plane so motors and wheels drop in from above", threats=["vspin_front", "vspin_side", "vspin_rear", "wall_slam", "lifter_flipper"]),
                 target="chassis_bottom")
    plan.feature("part", I("protection", "top half: roof and upper wall close the electronics bay against hits from "
                           "above; it lifts off for service", "split at z = 0; printed roof-down (flat face on the bed)", threats=["crusher_hammer", "debris", "flip_landing", "inverted"]),
                 target="chassis_top")
    plan.feature("wall", I("protection", "perimeter wall: the armour every side hit lands on, and the beam that ties the "
                           "front (weapon) to the rear (drive)", plan.extra.get("wall_basis", f"{f.wall} mm"), threats=["vspin_side", "vspin_front", "vspin_rear", "wall_slam", "hspin_floor", "grabber"]),
                 target="chassis", half="both")
    plan.feature("floor", I("load_path", "floor and roof skins: shear webs that keep the box square; they carry no "
                            "direct hits", f"{f.floor} mm = 5 layers at 0.2 mm (print minimum skin)", threats=["crusher_hammer", "flip_landing", "wall_slam"]),
                 target="chassis", half="both")
    plan.feature("bevel", I("protection", "belly and roof edges bevelled: removes the elephant's-foot lip on the bed "
                            "face and gives a hit on the corner a ramp to slide off", f"chamfer {EDGE_CHAMFER} mm (print rule)", threats=["wall_slam", "vspin_front", "grabber"]),
                 target="chassis", half="both")


SKIRT_OUT = 3.0  # skirt lip protrudes this far beyond the wall
SKIRT_LIP = 0.5  # lip height above the floor: level with a well-set opponent fork (0.3-0.5 mm)
SKIRT_EDGE = 1.0  # vertical lip face: >= 0.9 mm print wall at the tip (R026 asks <= 0.6 mm on the front lip only)
SKIRT_BAND = 1.2  # the skirt's solid band inboard of the outline (a thin band leaves a sliver at the belly bevel)


def _aligned(f, d):
    """Outline offset by d (mitred), with the same vertex count and start as the outline (for a ruled loft)."""
    full = _ccw(geom.polygon(f.outline))
    off = _ccw(geom.inset(f.outline, -d) if d > 0 else geom.inset(f.outline, -d))
    if len(off) != len(full):
        return None, None
    i0 = min(range(len(off)), key=lambda i: (off[i][0] - full[0][0]) ** 2 + (off[i][1] - full[0][1]) ** 2)
    return full, off[i0:] + off[:i0]


def add_skirts(plan, floor_z: float):
    """Side and rear skirt (hypothesis `skirts`): a ramped lip all round below the belly, SKIRT_LIP off the floor and
    SKIRT_OUT proud of the wall, rising at about 40 deg into the belly bevel, so a wedge, fork or lifter arriving from the
    side or rear meets a lip at the floor (not the 4 mm door under the belly) and a rising tooth glances up a ramp.
    Wheels keep their doors (the tyre is what an opponent meets there)."""
    h = plan.hyp
    mode = getattr(h, "skirts", "none")
    if mode == "none" or plan.is_tub:
        return
    f = plan.frame
    full, out = _aligned(f, SKIRT_OUT)
    if full is None:
        return
    z_lip = floor_z + SKIRT_LIP
    sk = sh.loft([{"z": sh.r(z_lip), "points": [list(p) for p in out], "spline": False},
                  {"z": sh.r(z_lip + SKIRT_EDGE), "points": [list(p) for p in out], "spline": False},
                  {"z": sh.r(f.zb + EDGE_CHAMFER + 0.2), "points": [list(p) for p in full], "spline": False}], ruled=True)
    inner = _ccw(geom.inset(f.outline, SKIRT_BAND))
    ys = [p[1] for p in f.outline]
    y0, y1 = min(ys), max(ys)
    # stop short of the front parts (wedge web, side-mounted forks/wedgelets) so the skirt never overlaps them
    fronts = [p for p in plan.parts if p.get("kind") in ("wedge", "skirt") and not any(p.get("at") or [])]
    # (a horizontal bar sweeps just above the front corners: nothing may stand ahead of it there)
    under_front = fronts and h.weapon != "hspin_bar"
    wy = [p["at"][1] for p in plan.parts if p.get("kind") == "wheel"]
    # rear: the skirt wraps the rear corners and ends in the rear wheels' doors (a free end would be a bite step)
    y_rear = (min(wy) + plan.extra.get("wheel_r", 15.0) + 2.0) if wy else y0 + 12.0
    # rear mode still wraps both rear quarters: the skirt runs forward to mid-length, so the side belly edge a tooth
    # sees from a rear-quarter bearing (the 45 deg sector reaches the hull's mid-length) is skirted too
    # under a horizontal bar the skirt still reaches the wedge root (y1 + 1), clear of the bar's sweep ahead of it
    if fronts and not under_front:
        fronts = [p for p in plan.parts if p.get("kind") in ("wedge", "skirt") and not any(p.get("at") or [])]
    y_hi = (y1 + 5.0 if under_front else (y1 + 1.0 if fronts else y1 - 0.5)) if mode == "sides_rear" else max(y0 + 12.0, y_rear, (y0 + y1) / 2 + 4.0 if h.weapon != "hspin_bar" else y_rear)
    keep = sh.boxr(-200, 200, y0 - 10, y_hi, z_lip - 1, f.zb + 5)
    if mode == "rear" and fronts and h.weapon != "hspin_bar":  # and the front quarters beside the ramp root, so its corners have no bare belly edge
        keep = sh.U(keep, sh.boxr(-200, 200, y1 - 12.0, y1 + 1.0, z_lip - 1, f.zb + 5))
    cuts = [_outline_prism(inner, z_lip - 1, f.zb, False)]
    cuts += [p["shape"] for p in fronts]
    cuts += plan.extra.get("skirt_clear", [])  # side-mounted forks / wedgelets: the skirt passes under them  # run under the front ramp's side ends, clear of the ramp itself
    for p in plan.parts:  # the tyre is the edge where a wheel reaches the outline: leave its door
        if p.get("kind") == "wheel":
            x, y = p["at"][0], p["at"][1]
            r = plan.extra.get("wheel_r", 15.0)
            cuts.append(sh.boxr(*sorted((x - (8 if x > 0 else -8), x + (40 if x > 0 else -40))), y - r - 2.0, y + r + 2.0,
                                z_lip - 1, f.zb + EDGE_CHAMFER + 0.5))  # the whole skirt height: no skin over the door
    plan.add("bottom", sh.S({"type": "intersect", "items": [sk, keep]}, *cuts),
             intent=I("ground_game", "side and rear skirt: a wedge, fork, lifter or flipper arriving from the side or rear "
                      "meets a lip at the floor instead of the door under the belly; its ramp face throws a rising tooth "
                      "up and off instead of catching it square",
                      f"lip {SKIRT_LIP} mm off the floor (opponent forks 0.3-0.5 mm), {SKIRT_OUT} mm proud, ramp to the "
                      f"belly bevel; {mode}",
                      threats=["lift_and_throw", "under_side", "under_rear", "lifter_flipper", "vspin_side", "vspin_rear",
                               "hazard_snag"]))
