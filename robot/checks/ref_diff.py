"""Geometric diff of a model part against a reference mesh in a shared frame (measurement only, never copied).

boolean_diff(model, ref)  extra = model - ref, missing = ref - model (manifold booleans; voxel fallback when the
                          reference mesh is not a closed manifold). Each disconnected blob of either set is one feature
                          difference (a missing chamfer, a round bore where the reference has a D, a wall in the wrong
                          place) and is reported with its bbox, centroid, volume and mean thickness. Skins thinner than
                          `min_thick` (tessellation noise on coincident faces) are dropped.
surface_deviation(a, b)   points sampled on each surface, unsigned distance to the other: max / p95 both ways.
render_deviation(...)     heat map PNG (red: model surface outside the reference, blue: reference surface the model
                          does not reach).
"""

from __future__ import annotations

import numpy as np
import trimesh


def _manifold(m):
    from ..geom import to_manifold

    mm = to_manifold(m)
    try:
        import manifold3d as mf

        if mm.status() != mf.Error.NoError or mm.is_empty():
            return None
    except Exception:  # noqa: BLE001
        return None
    return mm


def _blobs_from_mesh(d, min_vol, min_thick):
    out = []
    if d is None or not len(d.faces):
        return out
    for c in d.split(only_watertight=False):
        v = abs(float(c.volume)) if c.is_volume else float(c.convex_hull.volume) * 0.5
        a = float(c.area) or 1.0
        t = 2.0 * v / a
        if v < min_vol or t < min_thick:
            continue
        lo, hi = c.bounds
        P = np.asarray(c.vertices)
        P = P[np.linspace(0, len(P) - 1, min(len(P), 400)).astype(int)] if len(P) else P
        out.append({"volume_mm3": round(v, 2), "thick_mm": round(t, 3), "centroid": np.round(c.centroid, 2).tolist(),
                    "bbox": [np.round(lo, 2).tolist(), np.round(hi, 2).tolist()], "pts": np.round(P, 2).tolist()})
    return sorted(out, key=lambda b: -b["volume_mm3"])


def _voxel_blobs(occ, lo, h, min_vol, min_thick):
    from scipy import ndimage

    lab, n = ndimage.label(occ)
    out = []
    cell = h ** 3
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        v = float(m.sum()) * cell
        if v < min_vol:
            continue
        # thickness: volume / half the exposed face area of the blob
        faces = sum(np.count_nonzero(np.diff(np.pad(m, 1), axis=k)) for k in range(3)) * h * h
        t = 2.0 * v / max(faces, 1e-9)
        if t < min_thick:
            continue
        idx = np.argwhere(m) + [s.start for s in sl]
        pts = lo + (idx + 0.5) * h
        sub = pts[np.linspace(0, len(pts) - 1, min(len(pts), 400)).astype(int)]
        out.append({"volume_mm3": round(v, 2), "thick_mm": round(t, 3), "centroid": np.round(pts.mean(0), 2).tolist(),
                    "bbox": [np.round(pts.min(0) - h / 2, 2).tolist(), np.round(pts.max(0) + h / 2, 2).tolist()],
                    "pts": np.round(sub, 2).tolist()})
    return sorted(out, key=lambda b: -b["volume_mm3"])


def clean(m: trimesh.Trimesh) -> trimesh.Trimesh:
    """Drop the zero-volume sliver shells STEP exporters leave beside a part (open, degenerate bodies), so a reference
    whose real body is closed can be diffed exactly. A mesh with no closed body is returned unchanged."""
    if m.is_watertight:
        return m
    try:
        bodies = m.split(only_watertight=False)
    except Exception:  # noqa: BLE001
        return m
    keep = [b for b in bodies if b.is_watertight and abs(float(b.volume)) > 1e-3]
    if not keep:
        return m
    return keep[0] if len(keep) == 1 else trimesh.util.concatenate(keep)


def boolean_diff(model: trimesh.Trimesh, ref: trimesh.Trimesh, min_vol=2.0, min_thick=0.12, voxel_h=0.15):
    """Return {"extra_mm3", "missing_mm3", "extra": [blobs], "missing": [blobs], "method"}."""
    from ..geom import from_manifold

    ref = clean(ref)

    a, b = _manifold(model), _manifold(ref) if ref.is_watertight else None
    if a is not None and b is not None:
        ex, mi = from_manifold(a - b), from_manifold(b - a)
        return {"method": "brep-mesh boolean", "extra_mm3": round(abs(float(ex.volume)) if len(ex.faces) else 0.0, 2),
                "missing_mm3": round(abs(float(mi.volume)) if len(mi.faces) else 0.0, 2),
                "extra": _blobs_from_mesh(ex, min_vol, min_thick), "missing": _blobs_from_mesh(mi, min_vol, min_thick)}
    from ..geom import voxelize

    lo = np.minimum(model.bounds[0], ref.bounds[0]) - 2 * voxel_h
    hi = np.maximum(model.bounds[1], ref.bounds[1]) + 2 * voxel_h
    A, lo_, h = voxelize(model, voxel_h, lo, hi)
    B, _, _ = voxelize(ref, voxel_h, lo, hi)
    ex, mi = A & ~B, B & ~A
    bad = [n for n, ok_ in (("model", a is not None), ("reference", b is not None)) if not ok_]
    return {"method": f"voxel {voxel_h} mm ({' and '.join(bad)} not a closed manifold)", "extra_mm3": round(float(ex.sum()) * h ** 3, 2),
            "missing_mm3": round(float(mi.sum()) * h ** 3, 2),
            "extra": _voxel_blobs(ex, lo_, h, min_vol, min_thick), "missing": _voxel_blobs(mi, lo_, h, min_vol, min_thick)}


def closest_dist_chunked(mesh, pts, chunk=256):
    """Exact unsigned distance from each point to `mesh`, queried in chunks: trimesh's closest_point builds candidate
    triangle arrays for every query point at once, which on a thin, finely filleted panel ran to ~8 GB for 8000 points."""
    pts = np.asarray(pts, float)
    d = np.empty(len(pts))
    for i in range(0, len(pts), chunk):
        d[i:i + chunk] = trimesh.proximity.closest_point(mesh, pts[i:i + chunk])[1]
    return d


def surface_deviation(model: trimesh.Trimesh, ref: trimesh.Trimesh, n=20000, seed=3):
    """Unsigned surface-to-surface distances both ways: {"model_to_ref": {max, p95}, "ref_to_model": {max, p95}}."""
    rng = np.random.default_rng(seed)
    out = {}
    for name, a, b in (("model_to_ref", model, ref), ("ref_to_model", ref, model)):
        pts, _ = trimesh.sample.sample_surface(a, n, seed=int(rng.integers(1 << 30)))
        d = closest_dist_chunked(b, pts)
        out[name] = {"max": round(float(d.max()), 3), "p95": round(float(np.percentile(d, 95)), 3)}
        out[f"_{name}_pts"] = (pts, d)
    return out


def deviation_clusters(dev, tol=0.5, link=1.5, min_pts=1):
    """Sample points whose surface deviation exceeds `tol`, grouped into clusters (single linkage at `link` mm).

    Returns [{"kind": "extra" | "missing", "centroid": [x, y, z], "max_mm": d, "n": count}]: "extra" for model surface
    farther than `tol` from the reference, "missing" for reference surface our model does not reach; "pts": the
    cluster's sample points (a waiver must hold all of them)."""
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree

    out = []
    for kind, key in (("extra", "_model_to_ref_pts"), ("missing", "_ref_to_model_pts")):
        pts, d = dev[key]
        m = d > tol
        if not m.any():
            continue
        P, D = pts[m], d[m]
        pairs = cKDTree(P).query_pairs(link, output_type="ndarray")
        import scipy.sparse as sp

        g = sp.coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])), shape=(len(P), len(P))) if len(pairs) else sp.coo_matrix((len(P), len(P)))
        n, lab = connected_components(g, directed=False)
        for i in range(n):
            k = lab == i
            if k.sum() < min_pts:
                continue
            out.append({"kind": kind, "centroid": np.round(P[k].mean(0), 2).tolist(), "max_mm": round(float(D[k].max()), 3), "n": int(k.sum()),
                        "pts": P[k]})
    return sorted(out, key=lambda c: -c["max_mm"])


def render_deviation(dev, path, title="", vmax=1.0):
    """Two-view heat map of the sampled deviations (red: model outside the reference, blue: reference not reached)."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 3, figsize=(18, 6))
    pm, dm = dev["_model_to_ref_pts"]
    pr, dr = dev["_ref_to_model_pts"]
    for A, (i, j), lab in zip(axs, ((0, 1), (1, 2), (0, 2)), ("top (X, Y)", "side (Y, Z)", "front (X, Z)")):
        A.scatter(pr[:, i], pr[:, j], c=np.clip(dr / vmax, 0, 1), cmap="Blues", s=1, vmin=0, vmax=1)
        sc = A.scatter(pm[:, i], pm[:, j], c=np.clip(dm / vmax, 0, 1), cmap="Reds", s=1, vmin=0, vmax=1, alpha=0.8)
        A.set_aspect("equal")
        A.set_title(f"{title} {lab}")
    fig.colorbar(sc, ax=axs, shrink=0.7, label=f"deviation / {vmax} mm (red extra, blue missing)")
    fig.savefig(path, dpi=70)
    plt.close(fig)
