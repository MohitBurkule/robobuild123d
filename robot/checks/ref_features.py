"""Feature-level comparison of a model part with its reference mesh (both already in one world frame).

sections(m, ax, h)        even-odd cross-section of a mesh by the plane {axis = h} as a shapely geometry.
hole_shape(ring)          'round' | 'D' | 'hex' | 'slot' | 'other' from the hole's radial profile about its centroid.
holes(m, ax, h)           [(centroid (u, v), equivalent diameter, shape)] of the holes in one section.
corners(poly)             sharp outline corners [(x, y, turn deg)]: a filleted corner has none, a chamfer has two
                          ~45 deg ones where the sharp edge has one 90 deg one.
compare_sections(...)     per-part multi-height sections on all three axes: area, section IoU, hole count + shape
                          (centroid-matched), countersink / counterbore profile of every hole along the thin axis,
                          and corner treatment (fillet / chamfer / sharp). Returns a list of feature differences.
"""

from __future__ import annotations

import math

import numpy as np


SNAP_MM = 1e-3   # section segment ends closer than this are one vertex (mesh_plane floats differ in the last bits)


def snap_segments(q, tol=SNAP_MM):
    """(n,2,2) segment ends -> the same array with ends within `tol` merged onto one representative point.
    Rounding to a grid instead (round(, 3)) splits a shared vertex whose coordinate sits at k + 0.5 grid steps
    (1.0005 vs 1.00049999 round apart), so linemerge leaves the ring open and the outline is dropped."""
    from scipy.sparse.csgraph import connected_components
    from scipy.sparse import coo_matrix
    from scipy.spatial import cKDTree

    q = np.asarray(q, float)
    if not len(q):
        return q
    P = q.reshape(-1, 2)
    pairs = cKDTree(P).query_pairs(tol, output_type="ndarray")
    n = len(P)
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(n, n)) if len(pairs) else coo_matrix((n, n))
    _, lab = connected_components(g, directed=False)
    first = np.full(lab.max() + 1, -1)
    for i in range(n - 1, -1, -1):
        first[lab[i]] = i
    S = P[first[lab]].reshape(q.shape)
    return S[np.any(S[:, 0] != S[:, 1], axis=1)]


def section_region(noded, min_area=1e-4):
    """Material region bounded by a noded set of closed section outlines (None if empty).

    Faces come from polygonize, and a face is material when a ray from inside it crosses the outlines an odd number of
    times (even-odd rule). The old path (linemerge -> closed rings -> xor by area) lost outlines that touch at a vertex:
    a deck pocket meeting the tub wall outline at z 17.65 makes degree-4 nodes, linemerge returns the wall and the pocket
    as open lines, both were dropped and none of the pockets inside counted as holes."""
    from shapely.geometry import LineString
    from shapely.ops import polygonize, unary_union

    faces = [f for f in polygonize(noded) if f.area >= min_area]
    if not faces:
        return None
    x0, y0, x1, y1 = noded.bounds
    far = 10.0 * (abs(x1 - x0) + abs(y1 - y0) + 1.0)
    keep = []
    for f in faces:
        p = f.representative_point()
        ray = LineString([(p.x, p.y), (p.x + far, p.y + far * 0.0123456789)])  # odd slope: never along an edge
        hit = ray.intersection(noded)
        n = len(getattr(hit, "geoms", [hit])) if not hit.is_empty else 0
        if n % 2:
            keep.append(f)
    return unary_union(keep).buffer(0) if keep else None


def section(m, ax, h):
    import trimesh
    from shapely.geometry import LineString
    from shapely.ops import unary_union

    n = np.zeros(3)
    n[ax] = 1.0
    o = np.zeros(3)
    o[ax] = h
    segs = trimesh.intersections.mesh_plane(m, n, o)
    a, b = [i for i in range(3) if i != ax]
    lines = [LineString(s) for s in snap_segments(np.asarray(segs, float)[:, :, [a, b]] if len(segs) else [])]
    if not lines:
        return None
    return section_region(unary_union(lines))


def hole_shape(ring, densify=False):
    """Classify a hole outline by its radial profile r(theta) about the centroid."""
    from shapely.geometry import Polygon

    p = Polygon(ring)
    c = np.array(p.centroid.coords[0])
    if len(ring.coords) < 7:
        return "other"
    # densify (opt-in): a straight edge (a D flat) is only its two end vertices, and interpolating r(theta) between
    # them draws it as an arc, so a D reads as 'other' depending on tessellation; sampling the outline sees the flat
    pts = np.array((p.exterior.segmentize(max(0.02, p.length / 720)) if densify else p.exterior).coords)[:-1] - c
    if len(pts) < 6:
        return "other"
    mrr = p.minimum_rotated_rectangle
    xs, ys = mrr.exterior.coords.xy
    e = sorted([math.dist((xs[0], ys[0]), (xs[1], ys[1])), math.dist((xs[1], ys[1]), (xs[2], ys[2]))])
    if e[0] > 0 and e[1] / e[0] > 1.6:
        return "slot"
    ang = np.arctan2(pts[:, 1], pts[:, 0])
    r = np.hypot(pts[:, 0], pts[:, 1])
    o = np.argsort(ang)
    grid = np.linspace(-math.pi, math.pi, 360, endpoint=False)
    rr = np.interp(grid, ang[o], r[o], period=2 * math.pi)
    rmax, rmin = rr.max(), rr.min()
    if rmax <= 0:
        return "other"
    if (rmax - rmin) / rmax < 0.05:
        return "round"
    low = rr < rmin + 0.25 * (rmax - rmin)
    runs = int(np.count_nonzero(low & ~np.roll(low, 1))) or (1 if low.all() else 0)
    if 5 <= runs <= 7 and rmin / rmax > 0.8:
        return "hex"
    if runs == 1 and rmin / rmax > 0.55:
        return "D"
    return "other"


def holes(geom, densify=False):
    from shapely.geometry import Polygon

    out = []
    if geom is None or geom.is_empty:
        return out
    for g in getattr(geom, "geoms", [geom]):
        if not hasattr(g, "interiors"):
            continue
        for i in g.interiors:
            hp = Polygon(i)
            if hp.area < 0.5:
                continue
            out.append((tuple(np.round(hp.centroid.coords[0], 2)), round(2 * math.sqrt(hp.area / math.pi), 2), hole_shape(i, densify)))
    return out


def corners(geom, min_turn=35.0, min_edge=0.25):
    """Sharp corners of the outlines (exterior + interiors) of a section: [(x, y, turn deg)]."""
    out = []
    if geom is None or geom.is_empty:
        return out
    for g in getattr(geom, "geoms", [geom]):
        if not hasattr(g, "exterior"):
            continue
        for ring in [g.exterior, *g.interiors]:
            p = np.array(ring.simplify(0.02).coords)[:-1]
            n = len(p)
            if n < 3:
                continue
            for k in range(n):
                a, b, c = p[k - 1], p[k], p[(k + 1) % n]
                u, v = b - a, c - b
                lu, lv = np.linalg.norm(u), np.linalg.norm(v)
                if lu < min_edge or lv < min_edge:
                    continue
                t = math.degrees(math.acos(max(-1.0, min(1.0, float(u @ v / (lu * lv))))))
                if t >= min_turn:
                    out.append((round(float(b[0]), 2), round(float(b[1]), 2), round(t, 1)))
    return out


def _match_holes(ha, hb, tol):
    """Pair holes by centroid; returns (pairs, only_a, only_b)."""
    hb = list(hb)
    pairs, only_a = [], []
    for h in ha:
        j = min(range(len(hb)), key=lambda k: math.dist(h[0], hb[k][0]), default=None)
        if j is not None and math.dist(h[0], hb[j][0]) <= max(tol, 0.3 * h[1]):
            pairs.append((h, hb.pop(j)))
        else:
            only_a.append(h)
    return pairs, only_a, hb


def _thin_axis(m):
    ext = m.bounds[1] - m.bounds[0]
    return int(np.argmin(ext))


def hole_profile(m, ax, centre, lo, hi, n=7):
    """Equivalent diameter of the hole at `centre` (in the section plane) at n heights along `ax` between lo and hi."""
    from shapely.geometry import Point

    out = []
    for t in np.linspace(0.04, 0.96, n):
        g = section(m, ax, lo + (hi - lo) * t)
        d = None
        for c, dia, _ in holes(g):
            if math.dist(c, centre) < 1.0:
                d = dia
                break
        if d is None and g is not None and not g.is_empty and not g.contains(Point(centre)):
            d = 0.0   # no material there at all (outside the part at this height)
        out.append(d)
    return out


def hole_kind(profile):
    """'plain' | 'csk' (diameter falls steadily from one face) | 'cbore' (a step) | 'blind' from a hole profile."""
    v = [d for d in profile if d]
    if len(v) < 3:
        return "blind" if len(v) else "none"
    lo = min(v)
    big = [d > lo * 1.2 for d in profile if d]
    if not any(big):
        return "plain"
    seq = [d for d in profile if d]
    steps = [abs(b - a) for a, b in zip(seq, seq[1:])]
    if steps and max(steps) > 0.6 * (max(seq) - lo) and sum(1 for s in steps if s > 0.1 * (max(seq) - lo)) <= 1:
        return "cbore"
    return "csk"


EXACT_HOLE_TOL_MM = 0.15   # hole size tolerance when the reference diameter is exact (SolidWorks dump); mesh facets


PLANE_EPS_MM = 1e-3      # a section within this of a face lying in the plane cuts along the face: ambiguous
PLANE_SHIFT_MM = 0.05    # moved this far off such a face (well under any feature a section compares)


def off_face(h, ax, *meshes):
    """h, or h +- PLANE_SHIFT_MM when a face of any mesh lies in the plane: a section on a face plane returns that face's
    edges or not at random per tessellation, so holes through the face show in one mesh and not the other."""
    def on(x):
        return any(bool(np.any((np.abs(m.face_normals[:, ax]) > 0.999) & (np.abs(m.triangles_center[:, ax] - x) < PLANE_EPS_MM)))
                   for m in meshes)
    for x in (h, h + PLANE_SHIFT_MM, h - PLANE_SHIFT_MM, h + 2 * PLANE_SHIFT_MM, h - 2 * PLANE_SHIFT_MM):
        if not on(x):
            return x
    return h


def compare_sections(model, ref, fracs=(0.25, 0.5, 0.75), hole_tol=0.6, sec_iou_min=0.8, area_tol=0.15, corner_tol=0.6, exact_d=None):
    """Feature differences between two meshes in one frame. `exact_d`: the reference's exact hole diameters (SolidWorks
    dump): a reference hole's mesh-estimated diameter is snapped to the nearest one (within 0.3 mm / 10 %) and the size
    is then compared at EXACT_HOLE_TOL_MM. Returns (diffs, stats): diffs is a list of
    {"kind", "axis", "h", "msg", "severity"} with kinds: section_area, section_iou, hole_missing, hole_extra,
    hole_shape, hole_kind, corner."""
    lo = np.minimum(model.bounds[0], ref.bounds[0])
    hi = np.maximum(model.bounds[1], ref.bounds[1])
    rlo, rhi = ref.bounds
    diffs, stats = [], {"sections": 0, "holes_ref": 0, "holes_model": 0}
    for ax in range(3):
        for f in fracs:
            h = off_face(float(rlo[ax] + (rhi[ax] - rlo[ax]) * f), ax, model, ref)
            gr, gm = section(ref, ax, h), section(model, ax, h)
            stats["sections"] += 1
            ar = gr.area if gr is not None else 0.0
            am = gm.area if gm is not None else 0.0
            name = "XYZ"[ax]
            if ar > 0 and abs(am / ar - 1) > area_tol:
                diffs.append({"kind": "section_area", "axis": name, "h": round(h, 2), "severity": "warning",
                              "msg": f"{name}={h:.2f}: section area {am:.1f} vs {ar:.1f} mm2 ({am / ar - 1:+.0%})"})
            if ar > 0 and gm is not None:
                u = gr.union(gm).area
                iou = gr.intersection(gm).area / u if u else 1.0
                if iou < sec_iou_min:
                    diffs.append({"kind": "section_iou", "axis": name, "h": round(h, 2), "severity": "warning",
                                  "msg": f"{name}={h:.2f}: section IoU {iou:.2f} < {sec_iou_min}"})
            hr, hm = holes(gr), holes(gm)
            stats["holes_ref"] += len(hr)
            stats["holes_model"] += len(hm)
            pairs, miss, extra = _match_holes(hr, hm, hole_tol)
            for c, d, s in miss:
                diffs.append({"kind": "hole_missing", "axis": name, "h": round(h, 2), "severity": "blocker", "at": c,
                              "msg": f"{name}={h:.2f}: reference hole {s} d{d} at {c} has no counterpart"})
            for c, d, s in extra:
                diffs.append({"kind": "hole_extra", "axis": name, "h": round(h, 2), "severity": "blocker", "at": c,
                              "msg": f"{name}={h:.2f}: model hole {s} d{d} at {c} is not in the reference"})
            for (c, d, s), (c2, d2, s2) in pairs:
                dx = None
                if exact_d:
                    q = min(exact_d, key=lambda v: abs(v - d))
                    dx = q if abs(q - d) <= max(0.3, 0.1 * q) else None
                if s != s2 and "other" not in (s, s2):
                    diffs.append({"kind": "hole_shape", "axis": name, "h": round(h, 2), "severity": "blocker", "at": c,
                                  "msg": f"{name}={h:.2f}: hole at {c} is {s2} (d{d2}) in the model but {s} (d{d}) in the reference"})
                elif dx is not None and abs(dx - d2) > EXACT_HOLE_TOL_MM:
                    diffs.append({"kind": "hole_size", "axis": name, "h": round(h, 2), "severity": "warning", "at": c,
                                  "msg": f"{name}={h:.2f}: hole at {c} d{d2} vs reference d{dx:g} (exact, SolidWorks dump)"})
                elif dx is None and abs(d - d2) > max(0.3, 0.1 * d):
                    diffs.append({"kind": "hole_size", "axis": name, "h": round(h, 2), "severity": "warning", "at": c,
                                  "msg": f"{name}={h:.2f}: hole at {c} d{d2} vs reference d{d}"})
            if f == 0.5 and gr is not None and gm is not None:
                cr, cm = corners(gr), corners(gm)
                for x, y, t in cr:
                    near = [q for q in cm if math.dist((x, y), q[:2]) <= corner_tol]
                    if not near:
                        d = gm.boundary.distance(__import__("shapely.geometry", fromlist=["Point"]).Point(x, y))
                        if d < 1.5:
                            diffs.append({"kind": "corner", "axis": name, "h": round(h, 2), "severity": "warning", "at": (x, y),
                                          "msg": f"{name}={h:.2f}: reference has a sharp {t:.0f} deg corner at ({x}, {y}); the model rounds or chamfers it"})
                for x, y, t in cm:
                    near = [q for q in cr if math.dist((x, y), q[:2]) <= corner_tol]
                    if not near:
                        d = gr.boundary.distance(__import__("shapely.geometry", fromlist=["Point"]).Point(x, y))
                        if d < 1.5:
                            diffs.append({"kind": "corner", "axis": name, "h": round(h, 2), "severity": "warning", "at": (x, y),
                                          "msg": f"{name}={h:.2f}: model has a sharp {t:.0f} deg corner at ({x}, {y}) where the reference is filleted / chamfered"})
    # countersinks / counterbores along the thin axis
    ax = _thin_axis(ref)
    h = float((rlo[ax] + rhi[ax]) / 2)
    for c, d, s in holes(section(ref, ax, h)):
        pr = hole_profile(ref, ax, c, rlo[ax], rhi[ax])
        pm = hole_profile(model, ax, c, rlo[ax], rhi[ax])
        kr, km = hole_kind(pr), hole_kind(pm)
        if kr != km and km != "none":
            diffs.append({"kind": "hole_kind", "axis": "XYZ"[ax], "h": round(h, 2), "severity": "blocker", "at": c,
                          "msg": f"hole at {c} along {'XYZ'[ax]}: reference {kr} {pr}, model {km} {pm}"})
    return diffs, stats
