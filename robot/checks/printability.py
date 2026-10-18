"""FDM printability of every printed part: the best of the six axis-aligned print orientations by unsupported overhang
area, bridges that are too long, and holes too small to print true. Works on the part in its own frame."""

from __future__ import annotations

import math

import numpy as np
import trimesh

from .. import catalog
from ..finding import WARNING, fail, ok

G = "printability"
OVERHANG_DEG = 45.0  # faces leaning further than this from vertical need support
BRIDGE_COS = math.cos(math.radians(5.0))  # a face this close to flat-down is a bridge, not an overhang
MAX_BRIDGE_MM = 15.0
MAX_OVERHANG_MM2 = 60.0  # unsupported overhang area tolerated in the best orientation (chamfers, hole tops)
MIN_HOLE_MM = 1.8
BED_TOL_MM = 0.3
UPS = {"+z": (0, 0, 1), "-z": (0, 0, -1), "+x": (1, 0, 0), "-x": (-1, 0, 0), "+y": (0, 1, 0), "-y": (0, -1, 0)}


def fdm(p):
    if p.process is not None:
        return p.process == "fdm"
    m = catalog.material(p.material)
    return bool(m and m.cls in ("printed", "elastomer") and p.material not in ("rubber", "silicone", "lego_tyre", "resin"))


def analyse(mesh: trimesh.Trimesh, up):
    """(unsupported overhang area mm^2, longest bridge span mm, worst point) with `up` as the build direction."""
    up = np.asarray(up, float)
    n = mesh.face_normals
    h = mesh.triangles_center @ up
    base = h.min()
    down = -(n @ up)
    off_bed = mesh.triangles.dot(up).min(axis=1) > base + BED_TOL_MM
    steep = (down > math.cos(math.radians(OVERHANG_DEG))) & off_bed
    flat = steep & (down > BRIDGE_COS)
    area = mesh.area_faces
    over = steep & ~flat
    span, worst_pt = 0.0, None
    over_area = float(area[over].sum())
    if flat.any():
        idx = np.nonzero(flat)[0]
        adj = mesh.face_adjacency
        keep = flat[adj[:, 0]] & flat[adj[:, 1]]
        comps = trimesh.graph.connected_components(adj[keep], nodes=idx, min_len=1)
        for c in comps:
            s, pt = bridge_span(mesh, c, up, h)
            if s > MAX_BRIDGE_MM:
                over_area += float(area[c].sum())
            if s > span:
                span, worst_pt = s, pt
    if worst_pt is None and over.any():
        worst_pt = mesh.triangles_center[over][np.argmax(area[over])]
    return over_area, span, worst_pt


def bridge_span(mesh, comp, up, h):
    """Unsupported span of a flat downward face patch: twice the farthest distance from an anchor, where an anchor is an
    edge of the patch whose neighbouring face drops below it (a wall carrying the bridge). No anchor: its full extent."""
    import shapely
    from shapely.geometry import MultiLineString, Polygon
    from shapely.ops import unary_union

    ax = [k for k in range(3) if abs(up[k]) < 0.5]
    in_c = np.zeros(len(mesh.faces), bool)
    in_c[comp] = True
    adj, edges = mesh.face_adjacency, mesh.face_adjacency_edges
    a_in, b_in = in_c[adj[:, 0]], in_c[adj[:, 1]]
    border = a_in ^ b_in
    inner = np.where(a_in, adj[:, 0], adj[:, 1])[border]
    outer = np.where(a_in, adj[:, 1], adj[:, 0])[border]
    anchored = h[outer] < h[inner] - 1e-6
    V = mesh.vertices[:, ax]
    tri = unary_union([Polygon(t) for t in mesh.triangles[comp][:, :, ax]]).buffer(0)
    pts3 = mesh.triangles[comp].reshape(-1, 3)
    centre = pts3[np.argmin(np.abs(pts3 - pts3.mean(axis=0)).sum(axis=1))]
    if not anchored.any() or tri.is_empty:
        return float(np.ptp(V[mesh.faces[comp].ravel()], axis=0).max()), centre
    lines = MultiLineString([V[e] for e in edges[border][anchored]])
    x0, y0, x1, y1 = tri.bounds
    step = max(min(x1 - x0, y1 - y0) / 40, 0.25)
    gx, gy = np.meshgrid(np.arange(x0, x1 + step, step), np.arange(y0, y1 + step, step))
    P = shapely.points(gx.ravel(), gy.ravel())
    P = P[shapely.contains(tri, P) | shapely.touches(tri, P)]
    if not len(P):
        return 0.0, centre
    d = shapely.distance(lines, P)
    k = int(np.argmax(d))
    pt = centre.copy()
    pt[ax[0]], pt[ax[1]] = shapely.get_x(P[k]), shapely.get_y(P[k])
    return 2.0 * float(d[k]), pt


def small_holes(g):
    """Diameters of concave cylindrical faces (holes) in the exact B-rep that span at least half a turn."""
    s = g.solid
    if s is None:
        return None
    import build123d as bd
    from OCP.BRepTools import BRepTools

    out = []
    for f in s.faces():
        if f.geom_type != bd.GeomType.CYLINDER:
            continue
        try:
            u0, u1, _, _ = BRepTools.UVBounds_s(f.wrapped)
            if u1 - u0 < math.pi - 1e-3:
                continue
            p = f.position_at(0.5, 0.5)
            nrm = f.normal_at(p)
            axis = f.axis_of_rotation
            q = p - axis.position
            radial = q - axis.direction * q.dot(axis.direction)
            if radial.dot(nrm) < 0:
                out.append((2 * f.radius, (p.X, p.Y, p.Z)))
        except Exception:  # noqa: BLE001 - an odd face is skipped, the rest are still judged
            continue
    return out


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    n_ok = 0
    for rp in r.parts:
        p = rp.part
        if rp.cat is not None or not fdm(p):
            continue
        b = w.body(p.id)
        mesh = rp.geom.mesh
        res = {k: analyse(mesh, u) for k, u in UPS.items()}
        best = min(res, key=lambda k: (res[k][0], res[k][1]))
        area, span, pt = res[best]
        ctx.metrics[f"print_up.{p.id}"] = best
        ctx.metrics[f"print_overhang_mm2.{p.id}"] = area
        ctx.metrics[f"print_bridge_mm.{p.id}"] = span
        wpt = b.M[:3, :3] @ pt + b.M[:3, 3] if (pt is not None and b is not None) else None
        good = True
        if area > MAX_OVERHANG_MM2:
            good = False
            out.append(fail("printability.overhang", G, WARNING, "Needs support to print",
                            f"`{p.id}`: best print orientation is build-up {best}, which still leaves {area:.0f} mm² of overhang steeper "
                            f"than {OVERHANG_DEG:.0f}° or bridge longer than {MAX_BRIDGE_MM:.0f} mm.").on(p.id).here(wpt)
                       .expect(f"<= {MAX_OVERHANG_MM2:.0f} mm²", f"{area:.0f} mm²")
                       .fix("Chamfer overhangs to 45°, split the part, or accept support material."))
        if span > MAX_BRIDGE_MM:
            good = False
            out.append(fail("printability.bridge", G, WARNING, "Bridge too long",
                            f"`{p.id}` printed build-up {best} has a {span:.1f} mm bridge (limit {MAX_BRIDGE_MM:.0f} mm); it sags.")
                       .on(p.id).here(wpt).expect(f"<= {MAX_BRIDGE_MM:.0f} mm", f"{span:.1f} mm"))
        holes = small_holes(rp.geom)
        if holes is None:
            ctx.not_checked.append(f"Minimum hole size of `{p.id}`: no exact B-rep")
        else:
            tiny = [h for h in holes if h[0] < MIN_HOLE_MM]
            if tiny:
                good = False
                d, at = min(tiny)
                out.append(fail("printability.min_hole", G, WARNING, "Hole too small to print",
                                f"`{p.id}` has {len(tiny)} hole(s) down to Ø{d:.2f} mm; FDM closes holes under {MIN_HOLE_MM} mm.")
                           .on(p.id).here(b.M[:3, :3] @ np.array(at) + b.M[:3, 3] if b is not None else None)
                           .expect(f">= {MIN_HOLE_MM} mm", f"{d:.2f} mm").fix("Print a pilot and drill it, or enlarge the hole."))
        n_ok += good
    if n_ok:
        out.append(ok("printability.ok", G, "Printable without support", f"{n_ok} printed part(s) print support-free in their best orientation."))
    return out
