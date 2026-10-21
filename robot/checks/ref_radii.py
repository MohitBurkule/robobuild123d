"""Dump-free blend radius parity: per-edge fillet / chamfer size of a part against its reference mesh (STEP export).

Edges are sampled on BOTH meshes (an edge only the reference has, or only ours has, is still compared). At each sample
the section normal is the crease direction (cross product of the two face normals, which for a tessellated fillet is
its axis), and sharp_corner.local_radius measures the blend in that section on each mesh (0 = sharp corner; the
estimate is exact to ~1e-6 mm on a tessellated arc). A pair differing by more than RES_MM (0.1) is one difference;
differences are clustered (LINK_MM) into one finding per blended edge run: "R1.5 vs reference R1", "sharp vs R1".
Chamfers show as a 45 deg (or other) single-vertex turn pair; `chamfer_corners` counts, per section height, how many
corners of a run carry a bevel on each mesh.
"""

from __future__ import annotations

import numpy as np

RES_MM = 0.1
GRID_MM = 0.75
LINK_MM = 2.0
MIN_TURN_DEG = 20.0
TURN_MATCH_DEG = 15.0
SNAP_MM = 0.6


def edge_samples(m, grid=GRID_MM, min_deg=0.5):
    """[(point, crease axis)] one per grid cell, on edges whose crease runs along the edge (a fillet facet's long
    edge, a sharp corner): triangle diagonals across a flat or a fillet are skipped."""
    from .sharp_corner import _unit

    ang = np.degrees(m.face_adjacency_angles)
    k = ang > min_deg
    if not k.any():
        return []
    E = m.face_adjacency_edges[k]
    F = m.face_adjacency[k]
    N = m.face_normals
    out, seen = [], set()
    for (i, j), (fa, fb) in zip(E, F):
        pa, pb = m.vertices[i], m.vertices[j]
        e = pb - pa
        L = float(np.linalg.norm(e))
        if L < 1e-6:
            continue
        ax = np.cross(N[fa], N[fb])
        if np.linalg.norm(ax) < 1e-6 or abs(float(_unit(ax) @ (e / L))) < 0.9:
            continue
        for s in (np.linspace(0, 1, int(L / grid) + 2)[1:-1] if L > grid else (0.5,)):
            p = pa + s * e
            key = tuple(np.floor(p / grid).astype(int))
            if key not in seen:
                seen.add(key)
                out.append((p, _unit(ax)))
    return out


def _r(m, boxes, p, t):
    """(r, turn) of the blend at p in the section normal to t: 2 mm window first (a 1 mm chamfer's two bevel vertices
    both in view), then 3, then 1. One submesh (the 3 mm box round p) serves all three windows."""
    from .sharp_corner import local_radius

    W = 3.0
    idx = np.nonzero(np.all(boxes[0] <= p + W, axis=1) & np.all(boxes[1] >= p - W, axis=1))[0]
    if not len(idx):
        return None
    sub = m.submesh([idx], append=True)
    for w in (2.0, 3.0, 1.0):
        x = local_radius(sub, p, t, w)
        if x is not None and abs(x[1]) >= MIN_TURN_DEG:
            return x
    return None


def _near(m, dense=0.05):
    """Nearest-surface lookup by a KD-tree of dense surface samples (~dense mm off at worst): far faster than exact
    closest-point queries, and local_radius only needs a point within ~0.5 mm of the surface."""
    import trimesh
    from scipy.spatial import cKDTree

    S = trimesh.sample.sample_surface(m, max(2000, int(m.area / dense ** 2)), seed=5)[0]
    return S, cKDTree(S)


def blend_map(m, grid=GRID_MM, boxes=None):
    """[(point, axis, r, turn)] of one mesh's own edges (no reference): the blend radius (0 = sharp) at each sample."""
    from .sharp_corner import tri_boxes

    bm = boxes if boxes is not None else tri_boxes(m)
    out = []
    for p, t in edge_samples(m, grid):
        x = _r(m, bm, p, t)
        if x is not None:
            out.append((np.asarray(p, float), t, float(x[0]), float(abs(x[1]))))
    return out


def radius_pairs(model, ref, grid=GRID_MM):
    """[(point, axis, r_ours, r_ref, turn)] at edge samples of both meshes where both have a corner turning alike."""
    from .sharp_corner import tri_boxes

    bm, br = tri_boxes(model), tri_boxes(ref)
    (SA, TA), (SB, TB) = _near(model), _near(ref)
    S, seen = [], set()
    for p, t in edge_samples(model, grid) + edge_samples(ref, grid):   # one sample per grid cell and crease direction
        key = tuple(np.floor(p / grid).astype(int)) + tuple(np.round(np.abs(t), 1))
        if key not in seen:
            seen.add(key)
            S.append((p, t))
    if not S:
        return []
    P = np.array([p for p, _ in S])
    da, ia = TA.query(P, workers=-1)
    db, ib = TB.query(P, workers=-1)
    out = []
    for k, (p, t) in enumerate(S):
        if da[k] > SNAP_MM or db[k] > SNAP_MM:
            continue
        a = _r(model, bm, SA[ia[k]], t)
        b = _r(ref, br, SB[ib[k]], t)
        if a is None or b is None or abs(abs(a[1]) - abs(b[1])) > TURN_MATCH_DEG:
            continue
        out.append((np.asarray(p, float), t, float(a[0]), float(b[0]), float(abs(b[1]))))
    return out


def radius_diffs(pairs, res=RES_MM, link=LINK_MM):
    """Clusters of pairs differing by > res: [{at, n, r_ours, r_ref, turn, pts}] (median radii per cluster)."""
    from .ref_local import cluster

    bad = [x for x in pairs if abs(x[2] - x[3]) > res]
    if not bad:
        return []
    P = np.array([x[0] for x in bad])
    k, lab = cluster(P, link)
    out = []
    for i in range(k):
        g = [bad[j] for j in np.nonzero(lab == i)[0]]
        out.append({"at": np.round(np.mean([x[0] for x in g], axis=0), 2).tolist(), "n": len(g),
                    "r_ours": round(float(np.median([x[2] for x in g])), 2), "r_ref": round(float(np.median([x[3] for x in g])), 2),
                    "turn": round(float(np.median([x[4] for x in g])), 1), "pts": np.array([x[0] for x in g])})
    return sorted(out, key=lambda c: -abs(c["r_ours"] - c["r_ref"]) * c["n"])
