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


def section(m, ax, h):
    import trimesh
    from shapely.geometry import LineString, Polygon
    from shapely.ops import linemerge, unary_union

    n = np.zeros(3)
    n[ax] = 1.0
    o = np.zeros(3)
    o[ax] = h
    segs = trimesh.intersections.mesh_plane(m, n, o)
    a, b = [i for i in range(3) if i != ax]
    q = lambda p: (round(float(p[a]), 3), round(float(p[b]), 3))  # noqa: E731
    lines = [LineString([q(s), q(e)]) for s, e in segs if q(s) != q(e)]
    if not lines:
        return None
    mg = linemerge(unary_union(lines))
    rings = [g for g in getattr(mg, "geoms", [mg]) if g.is_ring and len(g.coords) > 3]
    polys = sorted((Polygon(g).buffer(0) for g in rings), key=lambda p: -p.area)
    out = None
    for p in polys:
        if p.area < 1e-4:
            continue
        out = p if out is None else out.symmetric_difference(p)
    return out


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


def compare_sections(model, ref, fracs=(0.25, 0.5, 0.75), hole_tol=0.6, sec_iou_min=0.8, area_tol=0.15, corner_tol=0.6):
    """Feature differences between two meshes in one frame. Returns (diffs, stats): diffs is a list of
    {"kind", "axis", "h", "msg", "severity"} with kinds: section_area, section_iou, hole_missing, hole_extra,
    hole_shape, hole_kind, corner."""
    lo = np.minimum(model.bounds[0], ref.bounds[0])
    hi = np.maximum(model.bounds[1], ref.bounds[1])
    rlo, rhi = ref.bounds
    diffs, stats = [], {"sections": 0, "holes_ref": 0, "holes_model": 0}
    for ax in range(3):
        for f in fracs:
            h = float(rlo[ax] + (rhi[ax] - rlo[ax]) * f)
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
                if s != s2 and "other" not in (s, s2):
                    diffs.append({"kind": "hole_shape", "axis": name, "h": round(h, 2), "severity": "blocker", "at": c,
                                  "msg": f"{name}={h:.2f}: hole at {c} is {s2} (d{d2}) in the model but {s} (d{d}) in the reference"})
                elif abs(d - d2) > max(0.3, 0.1 * d):
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
