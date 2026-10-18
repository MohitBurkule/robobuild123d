"""Material placement: printed parts should carry material only where loads need it, in every axis.

Each printed, non-exempt part is voxelised in its own frame and an inscribed-ball depth field (Euclidean distance to the
surface) is computed. From it:

  * `material.boss_excess`   around every fastener that engages the part, the annulus just outside the needed boss
                              (heat-set insert: boss OD 2x insert OD; tapped plastic: 3d; clearance: d/2 + wall) should be
                              wall or air, not solid. Flags a pod that is full thickness at a screw spot.
  * `material.solid_core`    fraction of the part deeper than 2x design wall (local thickness > 4 walls): a chunky part.
  * `material.thick_wall`    99th-percentile local thickness away from fasteners vs the design wall (uniformity).
  * `material.load_free`     thick material (deeper than one wall) farther than R_LOAD from every load anchor (fastener
                              axis, insert, contact with another part such as an axle, bearing, motor or armour) - pocketable.
  * `material.saving`        grams saveable per part (shell to one design wall each side, ribs back at RIB_KEEP) and total.

Exempt (thickness intentional): kinds armor / weapon / wedge / wedgelet / skirt, elastomer parts (tyres), or a part with
`"solid_reason": "..."`. A part may set `"design_wall_mm"` to override WALL_MM.
"""

from __future__ import annotations

import numpy as np
from scipy import ndimage

from .. import catalog, geom
from ..finding import WARNING, fail, note, ok
from .printability import fdm

G = "material"
WALL_MM = 2.0  # design wall of a printed structural part (>= 2x profile min wall, 4-5 perimeters)
EXEMPT_KINDS = {"armor", "weapon", "wedge", "wedgelet", "skirt", "tyre"}
BOSS_RING = 2.0  # walls of annulus checked outside the needed boss radius
BOSS_DEEP = 1.0  # annulus material deeper than this many walls (local thickness > 2 walls) is excess
BOSS_MAX_FRAC = 0.35  # excess fraction of the annulus allowed
CORE_DEEP = 2.0  # "deep" = more than 2 walls from any surface
CORE_MAX_FRAC = 0.10  # fraction of part volume allowed that deep
THICK_MAX = 3.0  # p99 local thickness away from fasteners, in design walls
R_LOAD = 10.0  # mm: thick material farther than this from every load anchor is load-path-free
LOAD_FREE_MAX_G = 0.3
RIB_KEEP = 0.25  # share of removed core assumed kept back as ribs
SAVING_NOTE_G = 0.2
CONTACT_MM = 0.4
COLLAR_FILL = 0.6  # ring slice this full counts as solid collar
COLLAR_MAX_WALLS = 3.0  # solid collar longer than this many design walls along the screw is a chunky block
MAX_CELLS = 1_500_000


def exempt(p) -> str | None:
    x = getattr(p, "_extra", {}) or {}
    if x.get("solid_reason"):
        return f"solid_reason: {x['solid_reason']}"
    if p.kind in EXEMPT_KINDS:
        return f"kind {p.kind}"
    m = catalog.material(p.material)
    if m is not None and m.cls == "elastomer":
        return "elastomer"
    return None


def depth_field(mesh, h):
    """Occupancy grid of `mesh` and the inscribed depth (mm, distance from each solid cell centre to the surface)."""
    lo, hi = mesh.bounds
    lo, hi = lo - h, hi + h
    vol = float(np.prod(hi - lo))
    h = max(h, (vol / MAX_CELLS) ** (1 / 3))
    occ, lo, h = geom.voxelize(mesh, h, lo, hi, max_cells=MAX_CELLS)
    depth = ndimage.distance_transform_edt(occ) * h - 0.5 * h
    return occ, lo, h, np.where(occ, np.maximum(depth, 0.0), 0.0)


def cell_centres(occ, lo, h):
    idx = np.argwhere(occ)
    return idx, lo + (idx + 0.5) * h


def to_local(M, P):
    Mi = np.linalg.inv(M)
    return np.asarray(P, float) @ Mi[:3, :3].T + Mi[:3, 3]


def fastener_axes(ctx):
    """[(fastener, at, unit dir, d, length, r_need_by_part fn)] in world, with the insert OD where there is one."""
    r, w = ctx.r, ctx.world
    out = []
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            continue
        d, ln = dl
        dr = np.asarray(f.dir, float)
        dr = dr / np.linalg.norm(dr)
        at = np.asarray(f.at, float)
        ins = w.body(f.threads_into) if f.threads_into else None
        ins_od, ins_part = None, None
        if ins is not None and ins.kind == "insert":
            V = ins.mesh.vertices - at
            rad = V - np.outer(V @ dr, dr)
            ins_od = 2 * float(np.linalg.norm(rad, axis=1).max())
            ins_part = ins
        out.append((f, at, dr, d, ln, ins_od, ins_part))
    return out


def boss_radius(f, pid, d, ins_od, ins_inside, wall):
    if ins_od is not None and ins_inside:
        return ins_od  # boss OD 2x insert OD -> radius = OD
    if f.threads_into == pid:
        return 1.5 * d  # tapped plastic: 3d boss
    return d / 2 + 0.1 + wall  # clearance hole plus one wall


def analyse_part(ctx, rp, body, axes, wall, h0):
    p = rp.part
    occ, lo, h, depth = depth_field(rp.geom.mesh, h0)
    idx, C = cell_centres(occ, lo, h)
    D = depth[occ]
    cell = h ** 3
    vol = len(D) * cell
    res = {"h": h, "vol": vol, "bosses": [], "occ": occ}
    if not len(D):
        return res
    M = body.M
    near_boss = np.zeros(len(D), bool)
    boss_core = np.zeros(len(D), bool)
    anchor = np.zeros(occ.shape, bool)
    lo_g, n = lo, np.array(occ.shape)

    def mark(P):
        k = np.floor((P - lo_g) / h).astype(int)
        m = np.all((k >= 0) & (k < n), axis=1)
        anchor[tuple(k[m].T)] = True

    for f, at, dr, d, ln, ins_od, ins_body in axes:
        a = to_local(M, at[None])[0]
        u = M[:3, :3].T @ dr
        V = C - a
        t = V @ u
        rho = np.linalg.norm(V - np.outer(t, u), axis=1)
        ins_inside = False
        if ins_body is not None:
            ic = to_local(M, ins_body.center[None])[0]
            k = np.floor((ic - lo) / h).astype(int)
            # insert sits in this part if the cells around its hole are solid
            ring = (rho < ins_od / 2 + 2 * h) & (rho > ins_od / 2 - h) & (np.abs(V @ u - (ic - a) @ u) < 1.0)
            ins_inside = bool(ring.sum() >= 4) and bool(np.all((k >= 0) & (k < n)))
        rn = boss_radius(f, p.id, d, ins_od, ins_inside, wall)
        span = (t > -1.0) & (t < ln + 1.0)
        zone = span & (rho < rn + BOSS_RING * wall)
        if not (zone & (rho < rn + wall)).any():
            continue  # the fastener does not engage this part
        near_boss |= zone
        boss_core |= span & (rho < rn + wall)
        axis_pts = a + np.outer(np.linspace(-1.0, ln + 1.0, max(int(ln / h) + 3, 3)), u)
        mark(axis_pts)
        ann = span & (rho > rn) & (rho < rn + BOSS_RING * wall)
        n_ann_ideal = _annulus_cells(rn, rn + BOSS_RING * wall, ann, t, h)
        excess = ann & (D > BOSS_DEEP * wall)
        frac = excess.sum() / max(n_ann_ideal, 1)
        collar = solid_collar_len(t[ann], rn, rn + BOSS_RING * wall, h)
        res["bosses"].append({"fastener": f.id, "r_need": rn, "frac": float(frac), "collar": collar, "excess_mm3": float(excess.sum() * cell),
                              "where": at})
    # contact anchors: surface points of other bodies touching this part (axle, bearing, motor, armour, mating part)
    lo_w, hi_w = body.aabb
    grow = int(np.ceil(CONTACT_MM / h)) + 1
    near = ndimage.binary_dilation(occ, iterations=grow) & ~ndimage.binary_erosion(occ, iterations=1)
    for ob in ctx.world.bodies:
        if ob is body or ob.is_wire:
            continue
        olo, ohi = ob.aabb
        if np.any(olo > hi_w + CONTACT_MM) or np.any(ohi < lo_w - CONTACT_MM):
            continue
        P, _ = ob.surface(max(h, 0.8))
        P = P[np.all((P >= lo_w - CONTACT_MM) & (P <= hi_w + CONTACT_MM), axis=1)]
        if not len(P):
            continue
        k = np.floor((to_local(M, P) - lo) / h).astype(int)
        m = np.all((k >= 0) & (k < n), axis=1)
        k = k[m]
        hit = near[tuple(k.T)]
        anchor[tuple(k[hit].T)] = True
    if anchor.any():
        adist = ndimage.distance_transform_edt(~anchor) * h
        A = adist[occ]
    else:
        A = np.full(len(D), np.inf)
    res["deep_frac"] = float((D > CORE_DEEP * wall).sum() / len(D))
    away = ~near_boss
    res["thick_p99"] = float(2 * np.percentile(D[away], 99)) if away.any() else 0.0
    res["load_free_mm3"] = float(((D > wall) & (A > R_LOAD)).sum() * cell)
    res["save_mm3"] = float(((D > wall) & ~boss_core).sum() * cell * (1 - RIB_KEEP))
    res["anchored"] = bool(anchor.any())
    return res


def solid_collar_len(t, r0, r1, h):
    """Length (mm) along the screw axis over which the ring r0..r1 around it is mostly solid (fill > COLLAR_FILL)."""
    if not len(t):
        return 0.0
    per_slice = np.pi * (r1 * r1 - r0 * r0) / (h * h)
    k = np.floor((t - t.min()) / h).astype(int)
    fill = np.bincount(k) / per_slice
    return float((fill > COLLAR_FILL).sum() * h)


def _annulus_cells(r0, r1, ann, t, h):
    """Cells an annulus r0..r1 over the axial span the fastener actually occupies in this part would hold."""
    if not ann.any():
        return 1
    L = float(np.ptp(t[ann])) + h
    return np.pi * (r1 * r1 - r0 * r0) * L / h ** 3


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    axes = fastener_axes(ctx)
    h0 = 0.6 if ctx.opts.fast else 0.4
    total_g, n_good, n_judged, exempt_ids = 0.0, 0, 0, []
    for rp in r.parts:
        p = rp.part
        if rp.cat is not None or not fdm(p):
            continue
        why = exempt(p)
        if why:
            exempt_ids.append(f"{p.id} ({why})")
            continue
        b = w.body(p.id)
        dens = catalog.density(p.material)
        if b is None or dens is None:
            ctx.not_checked.append(f"Material placement of `{p.id}`: no body or no density")
            continue
        wall = float((getattr(p, "_extra", {}) or {}).get("design_wall_mm") or WALL_MM)
        try:
            res = analyse_part(ctx, rp, b, axes, wall, h0)
        except Exception as e:  # noqa: BLE001 - one bad part is not-checked, the rest still judged
            ctx.not_checked.append(f"Material placement of `{p.id}`: {type(e).__name__}")
            continue
        if not res["vol"]:
            ctx.not_checked.append(f"Material placement of `{p.id}`: voxel grid empty (open mesh?)")
            continue
        n_judged += 1
        frac_fill = p.solid_fraction if p.solid_fraction is not None else 0.85
        gpm = 1e-3 * dens * frac_fill
        good = True
        boss_g = 0.0
        for bs in res["bosses"]:
            cmax = COLLAR_MAX_WALLS * wall
            if bs["frac"] > BOSS_MAX_FRAC or bs["collar"] > cmax:
                good = False
                r0, r1 = bs["r_need"], bs["r_need"] + BOSS_RING * wall
                xs_g = max(bs["collar"] - cmax, 0) * np.pi * (r1 * r1 - r0 * r0) * COLLAR_FILL * gpm
                boss_g += max(xs_g, bs["excess_mm3"] * gpm)
                out.append(fail("material.boss_excess", G, WARNING, "Chunky boss",
                                f"`{p.id}` at `{bs['fastener']}`: the ring {r0:.1f}-{r1:.1f} mm from the screw axis is solid "
                                f"for {bs['collar']:.1f} mm along the screw (limit {cmax:.1f} mm) and {bs['frac'] * 100:.0f}% "
                                f"of it is thicker than {2 * BOSS_DEEP * wall:.1f} mm (limit {BOSS_MAX_FRAC * 100:.0f}%); "
                                f"about {max(xs_g, bs['excess_mm3'] * gpm):.2f} g beyond the boss the screw needs "
                                f"(radius {r0:.1f} mm).")
                           .on(p.id).here(bs["where"])
                           .expect(f"collar <= {cmax:.1f} mm, deep <= {BOSS_MAX_FRAC * 100:.0f}%",
                                   f"{bs['collar']:.1f} mm, {bs['frac'] * 100:.0f}%")
                           .fix("Model a round boss of the needed OD tied in by thin ribs and pocket the rest of the block."))
        ctx.metrics[f"material.deep_frac.{p.id}"] = round(res["deep_frac"], 3)
        ctx.metrics[f"material.thick_p99_mm.{p.id}"] = round(res["thick_p99"], 2)
        if res["deep_frac"] > CORE_MAX_FRAC:
            good = False
            out.append(fail("material.solid_core", G, WARNING, "Mostly solid part",
                            f"`{p.id}`: {res['deep_frac'] * 100:.0f}% of its volume lies more than {CORE_DEEP * wall:.1f} mm "
                            f"from any surface (local thickness > {2 * CORE_DEEP * wall:.0f} mm).")
                       .on(p.id).expect(f"<= {CORE_MAX_FRAC * 100:.0f}%", f"{res['deep_frac'] * 100:.0f}%")
                       .fix("Shell the part to the design wall and add ribs along the load paths; or set `solid_reason`."))
        if res["thick_p99"] > THICK_MAX * wall:
            good = False
            out.append(fail("material.thick_wall", G, WARNING, "Wall much thicker than design wall",
                            f"`{p.id}`: away from fasteners the walls reach {res['thick_p99']:.1f} mm (p99) against a "
                            f"{wall:.1f} mm design wall.").on(p.id)
                       .expect(f"<= {THICK_MAX * wall:.1f} mm", f"{res['thick_p99']:.1f} mm")
                       .fix("Thin non-load walls to the design wall; thicken only along load paths."))
        lf_g = res["load_free_mm3"] * gpm
        ctx.metrics[f"material.load_free_g.{p.id}"] = round(lf_g, 2)
        if not res["anchored"]:
            ctx.not_checked.append(f"Load paths of `{p.id}`: no fastener or contact touches it")
        elif lf_g > LOAD_FREE_MAX_G:
            good = False
            out.append(fail("material.load_free", G, WARNING, "Thick material off any load path",
                            f"`{p.id}`: {lf_g:.2f} g of material thicker than {2 * wall:.0f} mm sits more than {R_LOAD:.0f} mm "
                            f"from every fastener, insert and contact face.").on(p.id)
                       .expect(f"<= {LOAD_FREE_MAX_G} g", f"{lf_g:.2f} g").fix("Pocket it (keep a design-wall skin)."))
        sv = max(res["save_mm3"] * gpm, boss_g)
        ctx.metrics[f"material.saveable_g.{p.id}"] = round(sv, 2)
        total_g += sv
        if sv > SAVING_NOTE_G:
            out.append(note("material.saving", G, "Mass that could be pocketed",
                            f"`{p.id}`: about {sv:.2f} g saveable by shelling to {wall:.1f} mm walls outside the bosses "
                            f"({RIB_KEEP * 100:.0f}% kept as ribs).").on(p.id))
        n_good += good
    ctx.metrics["material.saveable_g"] = round(total_g, 2)
    if exempt_ids:
        out.append(note("material.exempt", G, "Intentionally solid parts",
                        "Not judged for excess material: " + ", ".join(exempt_ids) + "."))
    if n_good:
        out.append(ok("material.ok", G, "Material follows the loads",
                      f"{n_good} of {n_judged} printed part(s) carry no chunky boss, solid core or load-free bulk."))
    return out
