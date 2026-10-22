"""Dump-free local surface comparison of a part against its reference mesh (STEP export) in our world frame.

gap_field(src, dst)   src surface sampled at `spacing` (default 0.25 mm, 16 pts/mm2): each sample's distance to dst.
                      A KD-tree of dense dst samples (0.05 mm) gives an upper bound; only samples whose bound exceeds
                      the tolerance get an exact point-to-triangle query, so a 18000 mm2 part takes ~12 s a side.
blobs(...)            samples deviating more than `tol` (0.1 mm), single-linkage clustered at 3 x spacing; each
                      cluster's area is its sample count x the area per sample. Every blob of >= `min_area` (2 mm2)
                      is one local difference: a fillet of the wrong radius, a chamfer on the wrong edges, a pocket
                      0.15 off, a boss outline misread. A global diff at the entry's tol_mm (often 1 mm) or an IoU
                      hides all of these.
mirror_blobs(...)     the part against its own mirror (plane x = 0 by default) where the REFERENCE is itself mirror
                      symmetric there: an asymmetric leftover (one copy edited, the other not) or a mirrored copy
                      that differs from its seed.
"""

from __future__ import annotations

import numpy as np

TOL_MM = 0.1
MIN_AREA_MM2 = 2.0
SPACING_MM = 0.25
DENSE_MM = 0.05


def gap_field(src, dst, tol=TOL_MM, spacing=SPACING_MM, dense=DENSE_MM, seed=1):
    """(P, d, area per sample): src surface samples and their distance to dst (exact where > tol, else a bound <= tol)."""
    import trimesh
    from scipy.spatial import cKDTree

    from .ref_diff import closest_dist_chunked

    n = max(1000, int(src.area / spacing ** 2))
    P = trimesh.sample.sample_surface(src, n, seed=seed)[0]
    S = trimesh.sample.sample_surface(dst, max(1000, int(dst.area / dense ** 2)), seed=seed + 1)[0]
    ub, _ = cKDTree(S).query(P, workers=-1)
    d = ub.copy()
    m = ub > tol
    if m.any():
        d[m] = closest_dist_chunked(dst, P[m], chunk=1000)
    return P, d, float(src.area) / n


def cluster(Q, link):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree

    if not len(Q):
        return 0, np.zeros(0, int)
    pairs = cKDTree(Q).query_pairs(link, output_type="ndarray")
    g = coo_matrix((np.ones(len(pairs)), (pairs[:, 0], pairs[:, 1])) if len(pairs) else ([], ([], [])), shape=(len(Q), len(Q)))
    return connected_components(g, directed=False)


def blobs(P, d, ap, kind, tol=TOL_MM, min_area=MIN_AREA_MM2, spacing=SPACING_MM, mask=None):
    """[{kind, area_mm2, max_mm, centroid, bbox, pts}] for every cluster of samples deviating > tol, >= min_area.
    `kind` is one label or an array of per-sample labels ("extra" / "missing"); a cluster holding both is "moved"
    (a surface standing off the reference: extra on one side, missing on the other: one difference, both areas)."""
    m = d > tol
    if mask is not None:
        m &= mask
    K = np.broadcast_to(np.asarray(kind, dtype=object), (len(P),))[m]
    A = np.broadcast_to(np.asarray(ap, float), (len(P),))[m]
    Q, D = P[m], d[m]
    k, lab = cluster(Q, 3.0 * spacing)
    out = []
    for i in range(k):
        s = lab == i
        area = float(A[s].sum())
        if area < min_area:
            continue
        q = Q[s]
        kinds = set(K[s])
        sub = q[np.linspace(0, len(q) - 1, min(len(q), 300)).astype(int)]
        out.append({"kind": kinds.pop() if len(kinds) == 1 else "moved", "area_mm2": round(area, 2), "max_mm": round(float(D[s].max()), 3),
                    "median_mm": round(float(np.median(D[s])), 3), "centroid": np.round(q.mean(0), 2).tolist(),
                    "bbox": [np.round(q.min(0), 2).tolist(), np.round(q.max(0), 2).tolist()], "pts": sub})
    return sorted(out, key=lambda b: -b["area_mm2"] * b["max_mm"])


def local_blobs(model, ref, tol=TOL_MM, min_area=MIN_AREA_MM2, spacing=SPACING_MM):
    """Both ways, clustered together: 'extra' = our surface off the reference, 'missing' = reference surface we do not
    reach, 'moved' = both at one place."""
    Ps, ds, aps, ks = [], [], [], []
    for kind, a, b in (("extra", model, ref), ("missing", ref, model)):
        P, d, ap = gap_field(a, b, tol, spacing)
        Ps.append(P)
        ds.append(d)
        aps.append(np.full(len(P), ap))
        ks.append(np.full(len(P), kind, dtype=object))
    return blobs(np.vstack(Ps), np.concatenate(ds), np.concatenate(aps), np.concatenate(ks), tol, min_area, spacing)


def mirrored(m, axis=0, c=0.0):
    M = np.eye(4)
    M[axis, axis] = -1.0
    M[axis, 3] = 2.0 * c
    r = m.copy()
    r.apply_transform(M)
    r.invert()
    return r


def mirror_blobs(model, ref, axis=0, c=0.0, tol=TOL_MM, min_area=MIN_AREA_MM2, spacing=SPACING_MM, sym_tol=0.05):
    """Blobs where our part differs from its own mirror at a place where the reference matches its mirror within
    sym_tol (the reference is symmetric there, so ours must be too). None when the reference is not symmetric overall
    (fewer than 90 % of its samples within sym_tol of its mirror)."""
    from scipy.spatial import cKDTree

    Pr, dr, _ = gap_field(ref, mirrored(ref, axis, c), sym_tol, spacing)
    if float((dr <= sym_tol).mean()) < 0.9:
        return None
    sym_pts = Pr[dr <= sym_tol]
    T = cKDTree(sym_pts)
    P, d, ap = gap_field(model, mirrored(model, axis, c), tol, spacing)
    near_sym = T.query(P, workers=-1)[0] <= 2.0 * spacing
    # only where the reference is symmetric AND our surface is on the reference there (a deliberate waived change is
    # reported by local_blobs, not twice)
    return blobs(P, d, ap, "asymmetric", tol, min_area, spacing, mask=near_sym)
