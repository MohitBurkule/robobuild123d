"""Low-DOF curve fitting: turn a measured outline into a designer's sketch (a few numbers), never a copy.

WHY: organic parts (wedgelets, armour shells, forks) were modelled as stacks of boxes or dense polylines lifted
from the reference, which gives stair steps and is a copy, not a design. Fitting a cubic B-spline with as FEW control
points as reach the error target (default RMS <= 0.3 mm, at most 8 points) gives numbers to type into `params`
and a smooth surface when lofted (robot.cad.smooth).

  fit_bspline(points, closed=True, max_ctrl=8, rms_target=0.3) -> {"ctrl", "closed", "n_ctrl", "rms", "max_err"}
  bspline_eval(ctrl, closed, n)                                 -> dense points (for tests and error measures)
  segments(points, closed)                                      -> [{"type": "line", "length", "angle_deg"} |
                                                                    {"type": "arc", "radius", "sweep_deg", "center"}]
  fillet_radii(points, closed)                                  -> radii of the arcs between straight runs

Cubic B-splines here are uniform: periodic for closed outlines, clamped (end points interpolated) for open ones.
The same convention is used by robot.cad.smooth.bspline_face, so fitted control points loft exactly.
"""

from __future__ import annotations

import math

import numpy as np

MAX_CTRL = 8


def _basis(t):
    """Uniform cubic B-spline blending weights for local parameter t in [0, 1)."""
    t2, t3 = t * t, t * t * t
    return np.stack([(1 - t) ** 3, 3 * t3 - 6 * t2 + 4, -3 * t3 + 3 * t2 + 3 * t + 1, t3], axis=-1) / 6.0


def _knots_open(n):
    """Clamped uniform knot vector for n control points, degree 3."""
    inner = max(n - 4, 0)
    return np.concatenate([[0] * 4, np.arange(1, inner + 1) / (inner + 1), [1] * 4])


def _bs_open_matrix(u, n):
    """Basis matrix (len(u) x n) of a clamped cubic B-spline (Cox-de Boor)."""
    from scipy.interpolate import BSpline

    k = _knots_open(n)
    u = np.clip(u, 0, 1 - 1e-12)
    return BSpline.design_matrix(u, k, 3).toarray()


def _bs_closed_matrix(u, n):
    """Basis matrix of a periodic uniform cubic B-spline, u in [0, 1)."""
    s = (np.asarray(u) % 1.0) * n
    i = np.floor(s).astype(int)
    w = _basis(s - i)
    B = np.zeros((len(s), n))
    for j in range(4):
        np.add.at(B, (np.arange(len(s)), (i + j - 1) % n), w[:, j])
    return B


def _matrix(u, n, closed):
    return _bs_closed_matrix(u, n) if closed else _bs_open_matrix(u, n)


def bspline_eval(ctrl, closed=True, n=400):
    ctrl = np.asarray(ctrl, float)
    u = np.linspace(0, 1, n, endpoint=not closed)
    return _matrix(u, len(ctrl), closed) @ ctrl


def _chord(P, closed):
    Q = np.vstack([P, P[:1]]) if closed else P
    d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(d)])
    return (s[:-1] if closed else s) / s[-1]


def _resample(P, closed, n=200):
    """Even arc-length resample (so dense reference meshes do not weight flat areas)."""
    Q = np.vstack([P, P[:1]]) if closed else P
    d = np.linalg.norm(np.diff(Q, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(d)])
    t = np.linspace(0, s[-1], n, endpoint=not closed)
    return np.stack([np.interp(t, s, Q[:, k]) for k in range(Q.shape[1])], axis=1)


def _dist_to_curve(P, C):
    from scipy.spatial import cKDTree

    return cKDTree(C).query(P)[0]


def _fit_n(P, n, closed, iters=8):
    u = _chord(P, closed)
    if closed:
        # start the parameter at the point of max x so different n give comparable control polygons
        pass
    for _ in range(iters):
        B = _matrix(u, n, closed)
        if not closed:
            # interpolate the end points: solve with the first/last control points fixed
            C = np.zeros((n, P.shape[1]))
            C[0], C[-1] = P[0], P[-1]
            rhs = P - np.outer(B[:, 0], P[0]) - np.outer(B[:, -1], P[-1])
            C[1:-1] = np.linalg.lstsq(B[:, 1:-1], rhs, rcond=None)[0]
        else:
            C = np.linalg.lstsq(B, P, rcond=None)[0]
        # parameter correction: move each u to the closest dense-curve parameter
        uu = np.linspace(0, 1, 2000, endpoint=not closed)
        D = _matrix(uu, n, closed) @ C
        from scipy.spatial import cKDTree

        _, j = cKDTree(D).query(P)
        u_new = uu[j]
        if not closed:
            u_new[0], u_new[-1] = 0.0, 1.0
        u = u_new
    C = _refine(P, u, C, closed)
    dense = bspline_eval(C, closed, 3000)
    e = _dist_to_curve(P, dense)
    return C, float(np.sqrt(np.mean(e ** 2))), float(e.max())


def _refine(P, u, C, closed):
    """Joint least squares over control points and point parameters (fixes the slow convergence of alternating
    projection). End control points stay fixed on open curves."""
    from scipy.optimize import least_squares
    from scipy.sparse import lil_matrix

    n, m, dim = len(C), len(P), P.shape[1]
    free = list(range(n)) if closed else list(range(1, n - 1))
    nc = len(free) * dim
    iu = np.arange(m) if closed else np.arange(1, m - 1)

    def unpack(x):
        CC = C.copy()
        CC[free] = x[:nc].reshape(-1, dim)
        uu = u.copy()
        uu[iu] = x[nc:]
        return CC, uu

    def res(x):
        CC, uu = unpack(x)
        return (_matrix(uu if closed else np.clip(uu, 0, 1), n, closed) @ CC - P).ravel()

    sp = lil_matrix((m * dim, nc + len(iu)), dtype=int)
    sp[:, :nc] = 1
    for k, i in enumerate(iu):
        sp[i * dim:(i + 1) * dim, nc + k] = 1
    x0 = np.concatenate([C[free].ravel(), u[iu]])
    try:
        r = least_squares(res, x0, jac_sparsity=sp, max_nfev=60, x_scale="jac")
        return unpack(r.x)[0]
    except Exception:  # noqa: BLE001 - keep the alternating result
        return C


def fit_bspline(points, closed=True, max_ctrl=MAX_CTRL, rms_target=0.3, min_ctrl=None):
    """Fewest control points (min_ctrl..max_ctrl, capped at MAX_CTRL) reaching rms_target; else the best found."""
    max_ctrl = min(int(max_ctrl), MAX_CTRL)
    P = np.asarray(points, float)
    if closed and np.allclose(P[0], P[-1]):
        P = P[:-1]
    P = _resample(P, closed)
    lo = min_ctrl or (4 if closed else 4)
    best = None
    for n in range(lo, max_ctrl + 1):
        C, rms, mx = _fit_n(P, n, closed)
        cand = {"ctrl": [[round(float(x), 3) for x in c] for c in C], "closed": closed, "n_ctrl": n,
                "rms": round(rms, 4), "max_err": round(mx, 4)}
        if best is None or rms < best["rms"]:
            best = cand
        if rms <= rms_target:
            return cand
    return best


# ---------------------------------------------------------------- straight / arc segments


def _circle(P):
    """Least-squares circle (Kasa): centre, radius, rms residual."""
    A = np.column_stack([2 * P[:, 0], 2 * P[:, 1], np.ones(len(P))])
    b = (P ** 2).sum(1)
    (cx, cy, c), *_ = np.linalg.lstsq(A, b, rcond=None)
    r = math.sqrt(max(c + cx * cx + cy * cy, 0.0))
    res = np.hypot(P[:, 0] - cx, P[:, 1] - cy) - r
    return np.array([cx, cy]), r, float(np.sqrt(np.mean(res ** 2)))


def _line_res(P):
    c = P.mean(0)
    _, s, vt = np.linalg.svd(P - c)
    return vt[0], float(s[1] / math.sqrt(len(P))) if len(s) > 1 else 0.0


def _curvature(Q, w, closed):
    """Signed curvature at each point from the circle through Q[i-w], Q[i], Q[i+w]."""
    n = len(Q)
    idx = np.arange(n)
    if closed:
        A, C = Q[(idx - w) % n], Q[(idx + w) % n]
    else:
        A, C = Q[np.clip(idx - w, 0, n - 1)], Q[np.clip(idx + w, 0, n - 1)]
    B = Q
    ab, bc, ca = np.linalg.norm(B - A, axis=1), np.linalg.norm(C - B, axis=1), np.linalg.norm(A - C, axis=1)
    cr = (B - A)[:, 0] * (C - A)[:, 1] - (B - A)[:, 1] * (C - A)[:, 0]
    den = ab * bc * ca
    k = np.where(den > 1e-12, 2 * cr / np.maximum(den, 1e-12), 0.0)
    return k


def segments(points, closed=True, step=0.2, straight_k=0.02, max_radius=200.0):
    """Split an outline into straight lines and circular arcs.

    Points are resampled every `step` mm; a point is "straight" where the local curvature (circle through its
    neighbours 2 steps away) is below `straight_k` (1/mm, i.e. radius > 50 mm). Runs of curved points become arcs
    (least-squares circle), runs of straight points become lines."""
    P = np.asarray(points, float)
    if closed and np.allclose(P[0], P[-1]):
        P = P[:-1]
    per = np.sum(np.linalg.norm(np.diff(np.vstack([P, P[:1]]) if closed else P, axis=0), axis=1))
    Q = _resample(P, closed, max(int(per / step), 24))
    k = _curvature(Q, 2, closed)
    curved = np.abs(k) > straight_k
    if closed and curved.any() and not curved.all():
        r = int(np.argmax(~curved & np.roll(curved, 1)))  # start at a curved->straight transition
        Q, k, curved = np.roll(Q, -r, 0), np.roll(k, -r), np.roll(curved, -r)
    runs, i, n = [], 0, len(Q)
    while i < n:
        j = i
        while j + 1 < n and curved[j + 1] == curved[i]:
            j += 1
        runs.append((i, j, bool(curved[i])))
        i = j + 1
    out = []
    for i, j, cv in runs:
        S = Q[i:j + 2] if j + 1 < n else (np.vstack([Q[i:], Q[:1]]) if closed else Q[i:])
        if len(S) < 2:
            continue
        L = float(np.sum(np.linalg.norm(np.diff(S, axis=0), axis=1)))
        if cv and len(S) >= 4:
            c, r, _ = _circle(S)
            if r <= max_radius:
                out.append({"type": "arc", "radius": round(r, 3), "sweep_deg": round(math.degrees(L / r), 2),
                            "center": [round(float(c[0]), 3), round(float(c[1]), 3)]})
                continue
        v = S[-1] - S[0]
        out.append({"type": "line", "length": round(L, 3), "angle_deg": round(math.degrees(math.atan2(v[1], v[0])), 2)})
    return _merge(out)


def _merge(segs):
    """Join consecutive lines with the same direction (greedy growth can split them on noise)."""
    out = []
    for s in segs:
        if out and s["type"] == "line" == out[-1]["type"] and abs(s["angle_deg"] - out[-1]["angle_deg"]) < 1.0:
            out[-1]["length"] = round(out[-1]["length"] + s["length"], 3)
            continue
        out.append(s)
    return out


def fillet_radii(points, closed=True, min_sweep=20.0):
    """Radii of arcs that sit between two straight runs (fillets), from `segments`."""
    seg = segments(points, closed)
    out = []
    for k, s in enumerate(seg):
        if s["type"] != "arc" or s["sweep_deg"] < min_sweep:
            continue
        a, b = seg[k - 1], seg[(k + 1) % len(seg)]
        if a["type"] == "line" and b["type"] == "line":
            out.append(s["radius"])
    return out
