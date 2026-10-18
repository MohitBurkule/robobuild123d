"""Strength under a design impact (the whole robot stopped at `IMPACT_G` g): weapon shaft bending and deflection (beam
formulas), bearing static rating, bending of the uprights that carry the bearings (section modulus from the B-rep cut at
several heights), and pull-out of bolts and heat-set inserts from plastic. Hand calculations with conservative
handbook material values, not FEA; anything without data is listed under NOT CHECKED."""

from __future__ import annotations

import math
from functools import reduce

import numpy as np
import trimesh
from shapely.geometry import LineString, box
from shapely.geometry.polygon import orient
from shapely.ops import polygonize, unary_union

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, note, ok
from . import _physics as ph

G = "strength"
SAFETY = 1.5  # required margin on yield for printed and bolted parts
MAX_SHAFT_DEFLECTION_MM = 0.2
UPRIGHT_WINDOW_MM = 10.0  # half-width of the slice of structure (along the shaft axis) that carries a bearing
THREAD_SHEAR_FACTOR = 0.6  # share of the cylinder at the major diameter that actually shears when a thread strips


def run(ctx):
    out = []
    F = ph.impact_n(ctx)
    ctx.metrics["design_impact_n"] = F
    basis = f"design impact {F:.0f} N ({ph.IMPACT_G:.0f} g on {ph.robot_mass_g(ctx):.0f} g)"
    ws = ph.weapons(ctx)
    if not ws:
        out.append(note("strength.shaft", G, "No spinning weapon shaft", "No spinning weapon, so shaft and bearing loads are not computed."))
    for p, wb, origin, axis in ws:
        out += shaft_and_bearings(ctx, p, wb, origin, axis, F, basis)
    if any(b.kind == "fork" for b in ctx.world.bodies):
        ctx.not_checked.append("Fork bending: forks are not traced to their mount; only weapon uprights are sectioned")
    out += bolt_pullout(ctx, F, basis)
    return out


def shaft_and_bearings(ctx, p, wb, origin, axis, F, basis):
    out = []
    lay = ph.shaft_layout(ctx, wb, origin, axis)
    if lay is None or not lay["sides"]:
        ctx.not_checked.append(f"Shaft strength of `{p.id}`: no supported shaft through the weapon centre")
        out.append(fail("strength.shaft", G, WARNING, "Weapon shaft not analysed",
                        f"`{p.id}`: no shaft body passes through the weapon centre and into a support, so bending was not computed.").on(p.id))
        return out
    sh = lay["shaft"]
    mp = catalog.mech(ph.material_of(ctx, sh))
    if mp is None:
        ctx.not_checked.append(f"Shaft `{sh.id}`: unknown material strength")
        out.append(fail("strength.shaft", G, WARNING, "Shaft material unknown", f"`{sh.id}` has no material with known strength.").on(sh.id))
        return out
    sy, _, E = mp
    d = lay["d"]
    M, R, a, b, simple = ph.reactions(F, lay["sides"])
    I = math.pi * d ** 4 / 64
    sigma = M * (d / 2) / I
    if simple:
        L = a + b
        defl = F * a * a * b * b / (3 * E * 1e3 * I * L)
    else:
        defl = F * a ** 3 / (3 * E * 1e3 * I)
    ctx.metrics[f"shaft_stress_mpa.{sh.id}"] = sigma
    ctx.metrics[f"shaft_deflection_mm.{sh.id}"] = defl
    how = f"between supports {a:.1f} and {b:.1f} mm either side" if simple else f"cantilevered {a:.1f} mm from its only support"
    msg = (f"`{sh.id}` (Ø{d:.1f} mm, {ph.material_of(ctx, sh)}) {how}: {basis} at the weapon gives {sigma:.0f} MPa "
           f"(yield {sy:.0f}) and {defl:.3f} mm deflection.")
    if sigma > sy:
        out.append(fail("strength.shaft", G, BLOCKER, "Weapon shaft bends on a hit", msg).on(sh.id, p.id)
                   .expect(f"<= {sy:.0f} MPa", f"{sigma:.0f} MPa").fix("Use a thicker or hardened shaft, or bring the bearings closer to the weapon."))
    elif sigma > sy / SAFETY or defl > MAX_SHAFT_DEFLECTION_MM:
        out.append(fail("strength.shaft", G, WARNING, "Weapon shaft is marginal", msg + f" Need {SAFETY}x margin and <= {MAX_SHAFT_DEFLECTION_MM} mm.")
                   .on(sh.id, p.id).expect(f"<= {sy / SAFETY:.0f} MPa, <= {MAX_SHAFT_DEFLECTION_MM} mm", f"{sigma:.0f} MPa, {defl:.3f} mm"))
    else:
        out.append(ok("strength.shaft", G, "Weapon shaft is strong enough", msg))

    for s, (t, body) in lay["sides"].items():
        r_n = R.get(s, F)
        if body.kind == "bearing":
            od = 2 * float(ph.perp_radius(body.mesh.vertices, origin, axis).max())
            rt = ph.bearing_rating(d, od)
            if rt is None:
                ctx.not_checked.append(f"Bearing `{body.id}` ({d:.1f}x{od:.1f} mm): not in the rating table")
                out.append(fail("strength.bearing", G, WARNING, "Bearing rating unknown",
                                f"`{body.id}` is {d:.1f}x{od:.1f} mm, which is not in the bearing table; its load {r_n:.0f} N was not judged.").on(body.id))
            else:
                ctx.metrics[f"bearing_load_n.{body.id}"] = r_n
                m2 = f"`{body.id}` ({rt[0]}, static rating {rt[2]} N) takes {r_n:.0f} N of the {basis}."
                if r_n > rt[2]:
                    out.append(fail("strength.bearing", G, WARNING, "Bearing overloaded on a hit", m2 + " The balls dent the races (brinelling).")
                               .on(body.id).expect(f"<= {rt[2]} N", f"{r_n:.0f} N").fix("Use a bigger bearing or share the load over more bearings."))
                else:
                    out.append(ok("strength.bearing", G, "Bearing rating is enough", m2))
            host = _host(ctx, body, origin, axis, t, od)
        else:
            host = body
        out += upright(ctx, host, origin + axis * t, axis, r_n, basis)
    return out


def _host(ctx, bearing, origin, axis, t, od):
    """The structure body that holds a bearing: most points of a ring just outside the bearing inside it."""
    c = origin + axis * t
    u = np.cross(axis, [0, 0, 1.0])
    if np.linalg.norm(u) < 1e-6:
        u = np.cross(axis, [1.0, 0, 0])
    u /= np.linalg.norm(u)
    v = np.cross(axis, u)
    ring = np.array([c + (od / 2 + 0.8) * (math.cos(k) * u + math.sin(k) * v) for k in np.linspace(0, 2 * math.pi, 16, endpoint=False)])
    best = None
    for b in ctx.world.bodies:
        if b.fastener or b.kind not in ph.SUPPORT:
            continue
        n = int(b.inside(ring).sum())
        if n and (best is None or n > best[0]):
            best = (n, b)
    return best[1] if best else None


def _section(mesh, z):
    segs = trimesh.intersections.mesh_plane(mesh, [0, 0, 1.0], [0, 0, z])
    if len(segs) == 0:
        return None
    lines = [LineString(s[:, :2]) for s in segs]
    polys = list(polygonize(unary_union(lines)))
    if not polys:
        return None
    return reduce(lambda a, b: a.symmetric_difference(b), polys)


def _ring_moment(coords, vc):
    """Signed second moment about the line v = vc of a ring given as (u, v) coordinates (Green's theorem)."""
    c = np.asarray(coords)
    u, v = c[:, 0], c[:, 1] - vc
    u2, v2 = np.roll(u, -1), np.roll(v, -1)
    cr = u * v2 - u2 * v
    return float(np.sum(cr * (v * v + v * v2 + v2 * v2)) / 12.0)


def section_modulus(poly):
    """(I about the centroidal axis parallel to u, distance to the extreme fibre, area) of a shapely (Multi)Polygon in (u, v)."""
    geoms = getattr(poly, "geoms", [poly])
    A = sum(g.area for g in geoms)
    if A <= 1e-9:
        return 0.0, 0.0, 0.0
    vc = poly.centroid.y
    I = 0.0
    for g in geoms:
        g = orient(g, 1.0)
        I += _ring_moment(g.exterior.coords, vc)
        for h in g.interiors:
            I += _ring_moment(h.coords, vc)
    lo, hi = poly.bounds[1], poly.bounds[3]
    return abs(I), max(hi - vc, vc - lo), A


def upright(ctx, host, c, axis, load, basis):
    """Bending of the structure that carries one bearing, cut horizontally at several heights below it; the load acts
    horizontally (a front hit) at the bearing height."""
    out = []
    if host is None:
        ctx.not_checked.append("Upright bending: no structure body found around a weapon support")
        return out
    if abs(axis[2]) > 0.7:
        ctx.not_checked.append(f"Upright bending of `{host.id}`: vertical weapon axis (horizontal spinner) not modelled")
        return out
    mp = catalog.mech(ph.material_of(ctx, host))
    if mp is None:
        ctx.not_checked.append(f"Upright bending of `{host.id}`: unknown material strength")
        out.append(fail("strength.upright", G, WARNING, "Upright material unknown", f"`{host.id}` has no material with known strength.").on(host.id))
        return out
    sy = mp[0] * (catalog.PRINTED_Z_FACTOR if ph.printed(ctx, host) else 1.0)
    ua = np.array([axis[0], axis[1], 0.0])
    ua /= np.linalg.norm(ua)
    va = np.array([-ua[1], ua[0], 0.0])
    z0, z1 = float(host.aabb[0][2]) + 0.3, float(c[2]) - 2.0
    if z1 <= z0:
        return out
    worst = None
    for z in np.linspace(z0, z1, 8):
        sec = _section(host.mesh, z)
        if sec is None or sec.is_empty:
            continue
        # Rotate to (u along the shaft, v front-back) and keep the slice of wall that carries this bearing.
        from shapely import affinity

        M = [ua[0], ua[1], va[0], va[1], 0, 0]
        rs = affinity.affine_transform(sec, M)
        uc = float(c[:2] @ ua[:2])
        win = rs.intersection(box(uc - UPRIGHT_WINDOW_MM, -1e4, uc + UPRIGHT_WINDOW_MM, 1e4))
        if win.is_empty or win.area < 1e-3:
            continue  # this cut misses the wall (a pocket or a failed slice); the other heights still judge it
        I, cfib, A = section_modulus(win)
        sigma = load * (float(c[2]) - z) * cfib / max(I, 1e-9)
        if worst is None or sigma > worst[0]:
            worst = (sigma, z, I / max(cfib, 1e-9), A)
    if worst is None:
        ctx.not_checked.append(f"Upright bending of `{host.id}`: no cross-section found below the bearing")
        return out
    sigma, z, Z, A = worst
    floor = ph.floor_z(ctx)
    ctx.metrics[f"upright_stress_mpa.{host.id}"] = sigma
    msg = (f"`{host.id}` carries {load:.0f} N of the {basis} at {c[2] - floor:.1f} mm; the weakest cut, {z - floor:.1f} mm up, has "
           f"{A:.0f} mm² and section modulus {Z:.0f} mm³: {sigma:.0f} MPa against {sy:.0f} MPa"
           f"{' (across layers)' if ph.printed(ctx, host) else ''}.")
    if sigma > sy / SAFETY:
        out.append(fail("strength.upright", G, WARNING, "Weapon upright may snap", msg).on(host.id).here([c[0], c[1], z])
                   .expect(f"<= {sy / SAFETY:.0f} MPa", f"{sigma:.0f} MPa")
                   .fix("Thicken the upright front-to-back, add a gusset, or print it so the layers run up the upright."))
    else:
        out.append(ok("strength.upright", G, "Weapon upright is strong enough", msg))
    return out


def bolt_pullout(ctx, F, basis):
    out = []
    w, spec = ctx.world, ctx.r.spec
    groups = {}
    for f in spec.fasteners:
        if f.threads_into:
            groups.setdefault(tuple(sorted(f.through or [])), []).append(f)
    bad, judged = 0, 0
    for key, fs in groups.items():
        load = F / len(fs)
        for f in fs:
            dl = catalog.parse_designation(f.designation)
            tgt = w.body(f.threads_into)
            if not dl or tgt is None:
                ctx.not_checked.append(f"Pull-out of `{f.id}`: unknown designation or threaded part")
                continue
            dmaj = dl[0]
            ax = np.asarray(f.dir, float) / max(np.linalg.norm(f.dir), 1e-9)
            at = np.asarray(f.at, float)
            mat_t = ph.material_of(ctx, tgt)
            tm = catalog.material(mat_t)
            if tgt.kind in ("insert",) or (tm is not None and tm.cls == "metal") or (ph.part(ctx, tgt) and ph.part(ctx, tgt).catalog):
                if tgt.kind != "insert":
                    continue  # a metal nut or a catalog part's own thread: the thread is not the weak link
                # A heat-set insert: it pulls out of the plastic around it; shear over its outer cylinder.
                rr = ph.perp_radius(tgt.mesh.vertices, at, ax)
                od, ln = 2 * float(rr.max()), float(np.ptp((tgt.mesh.vertices - at) @ ax))
                host = _around(w, tgt, ax, od / 2 + 0.4)
                if host is None:
                    ctx.not_checked.append(f"Pull-out of `{f.id}`: no plastic around insert `{tgt.id}`")
                    continue
                area, what, holder = math.pi * od * ln, f"insert `{tgt.id}` (Ø{od:.1f} x {ln:.1f} mm)", host
            else:
                ts = np.arange(0.0, dl[1], 0.2)
                eng = float(tgt.inside(at + np.outer(ts, ax)).sum()) * 0.2
                area, what, holder = math.pi * dmaj * eng * THREAD_SHEAR_FACTOR, f"{eng:.1f} mm of thread in `{tgt.id}`", tgt
            mp = catalog.mech(ph.material_of(ctx, holder))
            if mp is None:
                ctx.not_checked.append(f"Pull-out of `{f.id}`: unknown strength of `{holder.id}`")
                continue
            tau = mp[1] * (catalog.PRINTED_Z_FACTOR if ph.printed(ctx, holder) else 1.0)
            cap = area * tau
            judged += 1
            ctx.metrics[f"bolt_pullout_margin.{f.id}"] = cap / max(load, 1e-9)
            if cap < load * SAFETY:
                bad += 1
                out.append(fail("strength.bolt_pullout", G, WARNING, "Bolt can pull out of the plastic",
                                f"`{f.id}` ({f.designation}) holds by {what} in {ph.material_of(ctx, holder)}: {area:.0f} mm² x {tau:.0f} MPa = "
                                f"{cap:.0f} N, against {load:.0f} N ({basis} over {len(fs)} bolts) with {SAFETY}x margin.")
                           .on(f.id, holder.id).here(at).expect(f">= {load * SAFETY:.0f} N", f"{cap:.0f} N")
                           .fix("Use a longer insert or bolt, more bolts, or a through-bolt with a nut."))
    if judged and not bad:
        out.append(ok("strength.bolt_pullout", G, "Bolts hold in the plastic",
                      f"{judged} threaded joints each hold their share of the {basis} with {SAFETY}x margin."))
    return out


def _perp(ax):
    u = np.cross(ax, [0, 0, 1.0])
    if np.linalg.norm(u) < 1e-6:
        u = np.cross(ax, [1.0, 0, 0])
    return u / np.linalg.norm(u)


def _around(w, tgt, ax, rad):
    """The body holding most of a ring of points just outside a cylindrical part (an insert's plastic)."""
    u = _perp(ax)
    v = np.cross(ax, u)
    ts = np.linspace(-0.3, 0.3, 3)[:, None] * float(np.ptp((tgt.mesh.vertices - tgt.center) @ ax)) * ax
    ring = np.array([tgt.center + t + rad * (math.cos(k) * u + math.sin(k) * v)
                     for k in np.linspace(0, 2 * math.pi, 12, endpoint=False) for t in ts])
    best = None
    for b in w.bodies:
        if b is tgt or b.fastener or b.kind == "insert" or b.is_wire:
            continue
        n = int(b.inside(ring).sum())
        if n and (best is None or n > best[0]):
            best = (n, b)
    return best[1] if best else None
