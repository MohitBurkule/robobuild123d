"""Sketch (lines, arcs, relations, named dims) from a planar section of a reference B-rep.

    python -m robot.cad.sketch_extract rvrn_2.0.step <solid index> nx ny nz offset

`extract(solid, origin, normal)` cuts the solid with the plane and returns a Sketch in plane coordinates (u, v): the
exact section curves (lines and circular arcs, as OCC computes them from the B-rep, no point fitting), the relations
between them (tangent, equal, concentric, parallel, perpendicular, horizontal / vertical, symmetric about the
section's own mid lines) and named dims: line lengths, radii / diameters, angles between adjacent lines, distances
between parallel lines, centre-to-centre dx / dy / distance, centre-to-line distances, overall width / height.
`section_planes(solid)` proposes the planes a designer would sketch on: for each direction shared by several planar
faces, one section between each pair of neighbouring face levels. Nothing but the solid is read.
"""
from __future__ import annotations

import itertools
import math
import sys
from dataclasses import dataclass, field

import numpy as np
from OCP.BRepAdaptor import BRepAdaptor_Curve, BRepAdaptor_Surface
from OCP.BRepAlgoAPI import BRepAlgoAPI_Section
from OCP.GeomAbs import GeomAbs_Circle, GeomAbs_Line, GeomAbs_Plane
from OCP.gp import gp_Dir, gp_Pln, gp_Pnt

TOL = 1e-4      # mm: geometric coincidence
ANG = 1e-4      # rad


@dataclass
class Sketch:
    origin: np.ndarray
    normal: np.ndarray
    u: np.ndarray
    v: np.ndarray
    lines: dict = field(default_factory=dict)      # name -> (p0, p1) in (u, v)
    arcs: dict = field(default_factory=dict)       # name -> (centre, r, full)
    relations: list = field(default_factory=list)  # (kind, a, b)
    dims: dict = field(default_factory=dict)       # name -> mm or deg


def frame(normal, u=None):
    n = np.asarray(normal, float) / np.linalg.norm(normal)
    if u is None:
        u = min((np.eye(3)[i] for i in range(3)), key=lambda a: abs(a @ n))
    u = np.asarray(u, float) - n * (np.asarray(u, float) @ n)
    u /= np.linalg.norm(u)
    return n, u, np.cross(n, u)


def section_edges(solid, origin, normal):
    from build123d import Compound
    sec = BRepAlgoAPI_Section(solid.wrapped, gp_Pln(gp_Pnt(*map(float, origin)), gp_Dir(*map(float, normal))))
    sec.Build()
    return Compound(sec.Shape()).edges() if sec.IsDone() else []


def extract(solid, origin, normal, u=None):
    n, u, v = frame(normal, u)
    o = np.asarray(origin, float)
    S = Sketch(o, n, u, v)
    uv = lambda p: np.array([(np.asarray(p) - o) @ u, (np.asarray(p) - o) @ v])
    for e in section_edges(solid, o, n):
        c = BRepAdaptor_Curve(e.wrapped)
        t = c.GetType()
        if t == GeomAbs_Line:
            p0, p1 = uv(tuple(e.position_at(0))), uv(tuple(e.position_at(1)))
            if np.linalg.norm(p1 - p0) > TOL:
                S.lines[f"L{len(S.lines) + 1}"] = (p0, p1)
        elif t == GeomAbs_Circle:
            ci = c.Circle()
            cc = ci.Location()
            full = e.is_closed if hasattr(e, "is_closed") else False
            S.arcs[f"A{len(S.arcs) + 1}"] = (uv((cc.X(), cc.Y(), cc.Z())), ci.Radius(), bool(full))
    _merge_lines(S)
    _relations(S)
    _dims(S)
    return S


def _merge_lines(S):
    """Join collinear line pieces that touch end to end (a face boundary split one sketch line)."""
    L = list(S.lines.values())
    changed = True
    while changed:
        changed = False
        for i, j in itertools.combinations(range(len(L)), 2):
            a, b = L[i], L[j]
            da, db = a[1] - a[0], b[1] - b[0]
            if abs(da[0] * db[1] - da[1] * db[0]) > ANG * np.linalg.norm(da) * np.linalg.norm(db):
                continue
            ends = [(p, q) for p in a for q in b if np.linalg.norm(p - q) < TOL]
            if not ends:
                continue
            pts = [p for p in (*a, *b) if not any(np.linalg.norm(p - x[0]) < TOL for x in ends)]
            if len(pts) == 2:
                L[i] = (pts[0], pts[1]); L.pop(j); changed = True
                break
    S.lines = {f"L{k + 1}": l for k, l in enumerate(L)}


def _dir(l):
    d = l[1] - l[0]
    return d / np.linalg.norm(d)


def _relations(S):
    R = S.relations
    for k, l in S.lines.items():
        d = _dir(l)
        if abs(d[1]) < ANG: R.append(("horizontal", k, None))
        if abs(d[0]) < ANG: R.append(("vertical", k, None))
    for (a, la), (b, lb) in itertools.combinations(S.lines.items(), 2):
        c = abs(_dir(la) @ _dir(lb))
        if c > 1 - ANG: R.append(("parallel", a, b))
        elif c < ANG: R.append(("perpendicular", a, b))
        if abs(np.linalg.norm(la[1] - la[0]) - np.linalg.norm(lb[1] - lb[0])) < TOL: R.append(("equal", a, b))
    for (a, x), (b, y) in itertools.combinations(S.arcs.items(), 2):
        if np.linalg.norm(x[0] - y[0]) < TOL: R.append(("concentric", a, b))
        if abs(x[1] - y[1]) < TOL: R.append(("equal", a, b))
    for (a, x), (b, l) in itertools.product(S.arcs.items(), S.lines.items()):
        d = _dir(l)
        dist = abs((x[0] - l[0])[0] * d[1] - (x[0] - l[0])[1] * d[0])
        touches = any(abs(np.linalg.norm(p - x[0]) - x[1]) < TOL for p in l)
        if touches and abs(dist - x[1]) < TOL: R.append(("tangent", a, b))
    # symmetry about the section's own vertical / horizontal mid line
    pts = [p for l in S.lines.values() for p in l] + [a[0] for a in S.arcs.values()]
    if pts:
        P = np.array(pts); mid = (P.min(0) + P.max(0)) / 2
        for ax, name in ((0, "symmetric_v"), (1, "symmetric_h")):
            for (a, x), (b, y) in itertools.combinations(S.arcs.items(), 2):
                m = x[0].copy(); m[ax] = 2 * mid[ax] - m[ax]
                if np.linalg.norm(m - y[0]) < TOL and abs(x[1] - y[1]) < TOL: R.append((name, a, b))
            for (a, la), (b, lb) in itertools.combinations(S.lines.items(), 2):
                ma = [p.copy() for p in la]
                for p in ma: p[ax] = 2 * mid[ax] - p[ax]
                if min(np.linalg.norm(ma[0] - lb[0]) + np.linalg.norm(ma[1] - lb[1]),
                       np.linalg.norm(ma[0] - lb[1]) + np.linalg.norm(ma[1] - lb[0])) < 2 * TOL: R.append((name, a, b))


def _line_x(a, b):
    """Intersection of the infinite lines through segments a and b, or None when parallel."""
    da, db = a[1] - a[0], b[1] - b[0]
    den = da[0] * db[1] - da[1] * db[0]
    if abs(den) < 1e-9:
        return None
    w = b[0] - a[0]
    return a[0] + da * ((w[0] * db[1] - w[1] * db[0]) / den)


def _virtual_sharp(S, k):
    """Line k extended at each end through a tangent blend arc to the next line (the designer's sharp corner)."""
    l = S.lines[k]
    ends = [l[0].copy(), l[1].copy()]
    moved = False
    for i, p in enumerate(l):
        for a, (c, r, _f) in S.arcs.items():
            if abs(np.linalg.norm(p - c) - r) > TOL or ("tangent", a, k) not in S.relations:
                continue
            for k2, l2 in S.lines.items():
                if k2 == k or ("tangent", a, k2) not in S.relations:
                    continue
                x = _line_x(l, l2)
                if x is not None and np.linalg.norm(x - p) < 4 * r:
                    ends[i] = x; moved = True
    return ends if moved else None


def _dims(S):
    D = S.dims
    for k, l in S.lines.items():
        D[f"{k}.len"] = float(np.linalg.norm(l[1] - l[0]))
        sharp = _virtual_sharp(S, k)
        if sharp is not None:
            D[f"{k}.len_sharp"] = float(np.linalg.norm(sharp[1] - sharp[0]))
    groups = []        # collinear pieces of one sketch line split by other features: their overall span
    for k, l in S.lines.items():
        d = _dir(l)
        g = next((g for g in groups if abs(abs(d @ g[1]) - 1) < ANG and abs((g[2] - l[0])[0] * g[1][1] - (g[2] - l[0])[1] * g[1][0]) < TOL), None)
        if g is None:
            groups.append([[k], d, l[0]])
        else:
            g[0].append(k)
    for i, (ks, d, o) in enumerate(groups):
        if len(ks) > 1:
            ends = [_virtual_sharp(S, k) or S.lines[k] for k in ks]
            t = [float((p - o) @ d) for e in ends for p in e]
            D[f"S{i + 1}({'+'.join(ks)}).span"] = max(t) - min(t)
    for k, (c, r, full) in S.arcs.items():
        D[f"{k}.R"] = float(r)
        D[f"{k}.D"] = float(2 * r)
    for (a, la), (b, lb) in itertools.combinations(S.lines.items(), 2):
        touch = any(np.linalg.norm(p - q) < TOL for p in la for q in lb)
        da, db = _dir(la), _dir(lb)
        if touch:
            D[f"{a}_{b}.ang"] = math.degrees(math.acos(min(1.0, abs(float(da @ db)))))
        elif abs(da @ db) > 1 - ANG:
            w = lb[0] - la[0]
            D[f"{a}_{b}.dist"] = float(abs(w[0] * da[1] - w[1] * da[0]))
    for (a, x), (b, y) in itertools.combinations(S.arcs.items(), 2):
        d = y[0] - x[0]
        if np.linalg.norm(d) < TOL:
            continue
        D[f"{a}_{b}.dx"], D[f"{a}_{b}.dy"], D[f"{a}_{b}.dist"] = float(abs(d[0])), float(abs(d[1])), float(np.linalg.norm(d))
    for (a, x), (b, l) in itertools.product(S.arcs.items(), S.lines.items()):
        d = _dir(l); w = x[0] - l[0]
        D[f"{a}_{b}.dist"] = float(abs(w[0] * d[1] - w[1] * d[0]))
    pts = [p for l in S.lines.values() for p in l] + [c + s * r for c, r, _ in S.arcs.values() for s in (np.array([1, 0]), np.array([0, 1]), -np.array([1, 0]), -np.array([0, 1]))]
    if pts:
        P = np.array(pts)
        D["W"], D["H"] = float(np.ptp(P[:, 0])), float(np.ptp(P[:, 1]))
        # datums a designer dimensions from: the section's outer edges and its mid lines (the part's symmetry planes)
        lo, hi = P.min(0), P.max(0)
        ref = {"left": (0, lo[0]), "right": (0, hi[0]), "bottom": (1, lo[1]), "top": (1, hi[1]),
               "midv": (0, (lo[0] + hi[0]) / 2), "midh": (1, (lo[1] + hi[1]) / 2)}
        feats = {k: c for k, (c, _r, _f) in S.arcs.items()}
        for k, l in S.lines.items():
            d = _dir(l)
            if abs(d[1]) < ANG or abs(d[0]) < ANG:
                feats[k] = (l[0] + l[1]) / 2
        for k, c in feats.items():
            for name, (ax, val) in ref.items():
                if k.startswith("L") and abs(_dir(S.lines[k])[ax]) > 1 - ANG:
                    continue          # a line along this axis has no offset from a datum across it
                D[f"{k}.{name}"] = float(abs(c[ax] - val))


def section_planes(solid, min_faces=3, max_levels=12, skin=0.0):
    """[(origin, normal)]: (with skin, also +-skin about each face level and) mid-levels between the planar-face levels of each well-populated face direction."""
    dirs = []
    for f in solid.faces():
        ad = BRepAdaptor_Surface(f.wrapped)
        if ad.GetType() != GeomAbs_Plane:
            continue
        pl = ad.Plane(); d = pl.Axis().Direction(); p = pl.Location()
        n = np.array([d.X(), d.Y(), d.Z()]); n = n if max(n, key=abs) > 0 else -n
        dirs.append((n, float(np.array([p.X(), p.Y(), p.Z()]) @ n), f.area))
    groups = []
    for n, s, a in dirs:
        g = next((g for g in groups if abs(g[0] @ n) > 1 - 1e-6), None)
        if g is None:
            groups.append([n, [], 0.0]); g = groups[-1]
        g[1].append(s); g[2] += a
    out = []
    for n, levels, _a in sorted(groups, key=lambda g: -g[2]):
        lv = sorted(set(round(x, 4) for x in levels))
        if len(levels) < min_faces or len(lv) < 2:
            continue
        mids = [(a + b) / 2 for a, b in zip(lv, lv[1:])]
        if skin:   # also just inside each face level: a sketch usually sits on a face, its feature may be thin
            mids = sorted(set(mids) | {x + d for x in lv for d in (-skin, skin)})
        step = max(1, len(mids) // max_levels)
        out += [(n * m, n) for m in mids[::step]]
    return out


if __name__ == "__main__":
    from .blend_finder import load_step_solid
    s = load_step_solid(sys.argv[1], sys.argv[2])
    n = np.array(list(map(float, sys.argv[3:6])))
    sk = extract(s, n / np.linalg.norm(n) * float(sys.argv[6]), n)
    print(len(sk.lines), "lines", len(sk.arcs), "arcs")
    print(sorted(set(r[0] for r in sk.relations)))
    for k, v in list(sk.dims.items())[:60]:
        print(f"  {k} = {v:.4f}")
