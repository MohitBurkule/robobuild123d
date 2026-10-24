"""Round 15: final-body triangle soup from the decoded XT faces (for files without a display mesh).

Each decoded face becomes an OCC face: its analytic surface (plane / cylinder / cone / sphere /
torus) bounded by wires rebuilt from the loop vertices and edge curves (line, circle, ellipse;
other curve types -> polyline through the known vertices), then ShapeFix_Face + BRepMesh.
Faces whose surface is not decoded (b_surface, swept, offset, blended_edge) or that fail to build
are fan-triangulated from their boundary polygon.  The result is only used as a voxel-parity
oracle, so small cracks between faces are tolerated.
"""
import json, math
import numpy as np
from OCP.gp import gp_Pnt, gp_Dir, gp_Ax2, gp_Ax3, gp_Circ, gp_Elips, gp_Pln, gp_Cylinder, gp_Cone, gp_Sphere, gp_Torus
from OCP.GC import GC_MakeArcOfCircle, GC_MakeArcOfEllipse
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCP.Geom import Geom_Plane, Geom_CylindricalSurface, Geom_ConicalSurface, Geom_SphericalSurface, Geom_ToroidalSurface
from OCP.ShapeFix import ShapeFix_Face

MM = 1000.0
ERR = []
ARC_MID = {}   # edge id -> arc midpoint (m), set by orient_arcs()


def P(v): return gp_Pnt(*(np.array(v, float) * MM))


def _ax2(c, n, x):
    n = np.array(n, float); x = np.array(x, float); x = x - n * (x @ n)
    return gp_Ax2(P(c), gp_Dir(*n), gp_Dir(*(x / np.linalg.norm(x))))


def curve_pts(e, a, b, n=16):
    """sample points (m) from a to b along the decoded curve of edge e."""
    c = e.get('curve') or {}
    t = c.get('type')
    a = np.array(a, float); b = np.array(b, float)
    if t in ('circle', 'ellipse'):
        C = np.array(c['centre']); nn = np.array(c['normal'], float); X = np.array(c['x_axis'], float); Y = np.cross(nn, X)
        R1 = c['radius']; R2 = c.get('minor_radius', R1)
        ang = lambda p: math.atan2(((p - C) @ Y) / R2, ((p - C) @ X) / R1)
        a0 = ang(a); a1 = ang(b)
        sw = (a1 - a0) % (2 * math.pi)
        if np.linalg.norm(a - b) < 1e-9: sw = 2 * math.pi
        if e.get('fin_sense') == '-': sw = sw - 2 * math.pi if sw < 2 * math.pi - 1e-12 else -2 * math.pi
        M = ARC_MID.get(e.get('edge'))
        if M is not None and abs(sw) < 2 * math.pi - 1e-9:
            alt = sw - 2 * math.pi if sw > 0 else sw + 2 * math.pi
            pm = lambda s_: C + R1 * math.cos(a0 + s_ / 2) * X + R2 * math.sin(a0 + s_ / 2) * Y
            if np.linalg.norm(pm(alt) - M) < np.linalg.norm(pm(sw) - M): sw = alt
        return [C + R1 * math.cos(a0 + sw * k / n) * X + R2 * math.sin(a0 + sw * k / n) * Y for k in range(n + 1)]
    return [a, b]


_VX = {}


def VX(p):
    """shared vertex per decoded point (MakeWire needs coincident vertices; float noise > 1e-7 mm)."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
    k = tuple(np.round(np.array(p, float) * 1e7).astype(int))
    if k not in _VX:
        from OCP.BRep import BRep_Builder
        v = BRepBuilderAPI_MakeVertex(P(p)).Vertex(); BRep_Builder().UpdateVertex(v, 2e-3); _VX[k] = v
    return _VX[k]


def occ_edge(e, a, b):
    c = e.get('curve') or {}; t = c.get('type')
    closed = np.linalg.norm(np.array(a) - np.array(b)) < 1e-10
    if closed and t not in ('circle', 'ellipse'): return None
    if t == 'circle':
        nn = np.array(c['normal'], float) * (1 if e.get('fin_sense') != '-' else -1)
        g = gp_Circ(_ax2(c['centre'], nn, c['x_axis']), c['radius'] * MM)
    elif t == 'ellipse':
        R1, R2 = c['radius'], c['minor_radius']
        nn = np.array(c['normal'], float) * (1 if e.get('fin_sense') != '-' else -1)
        if R2 > R1: g = gp_Elips(_ax2(c['centre'], nn, np.cross(nn, np.array(c['x_axis'], float))), R2 * MM, R1 * MM)
        else: g = gp_Elips(_ax2(c['centre'], nn, c['x_axis']), R1 * MM, R2 * MM)
    else:
        return BRepBuilderAPI_MakeEdge(VX(a), VX(b)).Edge()
    if closed: return BRepBuilderAPI_MakeEdge(g, VX(a), VX(a)).Edge()
    return BRepBuilderAPI_MakeEdge(g, VX(a), VX(b)).Edge()


def loop_ends(l):
    """(edge, fin start, fin end) per fin.  Observed: the decoded start_vertex of fin i is the END
    of fin i (= start of fin i+1); fin '+' runs along the curve sense (CCW about a circle normal),
    fin '-' against it."""
    es = l['edges']; n = len(es)
    if n == 1 and es[0].get('start_vertex') is None:
        c = es[0].get('curve') or {}
        if c.get('type') in ('circle', 'ellipse'):
            v = list(np.array(c['centre']) + c['radius'] * np.array(c['x_axis'], float)); return [(es[0], v, v)]
    return [(e, es[i - 1].get('start_vertex'), e.get('start_vertex')) for i, e in enumerate(es)]


def surface(f):
    p = f.get('params') or {}; t = f['surface_type']
    try:
        if t == 'plane': return Geom_Plane(gp_Pln(P(p['point']), gp_Dir(*p['normal'])))
        if t == 'cylinder': return Geom_CylindricalSurface(gp_Cylinder(gp_Ax3(_ax2(p['point'], p['axis'], p['x_axis'])), p['radius'] * MM))
        if t == 'cone': return Geom_ConicalSurface(gp_Cone(gp_Ax3(_ax2(p['point'], p['axis'], p['x_axis'])), math.radians(p['half_angle_deg']), p['radius'] * MM))
        if t == 'sphere': return Geom_SphericalSurface(gp_Sphere(gp_Ax3(_ax2(p['centre'], p['axis'], p['x_axis'])), p['radius'] * MM))
        if t == 'torus': return Geom_ToroidalSurface(gp_Torus(gp_Ax3(_ax2(p['centre'], p['axis'], p['x_axis'])), p['major_radius'] * MM, p['minor_radius'] * MM))
    except Exception:
        return None
    return None


def tris_of_face(F):
    from build123d import Face
    V, T = Face(F).tessellate(0.02, 0.2)
    V = np.array([tuple(v) for v in V])
    return [V[list(t)] for t in T]


def fan(f):
    out = []
    for l in f.get('loops', []):
        pts = []
        for e, a, b in loop_ends(l):
            if a is None or b is None: continue
            pts += curve_pts(e, a, b, 8)[:-1]
        if len(pts) < 3: continue
        Q = np.array(pts) * MM; c = Q.mean(0)
        for i in range(len(Q)): out.append(np.array([c, Q[i], Q[(i + 1) % len(Q)]]))
    return out


def face_tris(f):
    try:
        T = uv_mesh(f)
        if T: return T, 'uv'
    except Exception as ex:
        ERR.append((f['surface_type'], 'uv ' + repr(ex)[:60]))
    S = surface(f)
    if S is not None:
        try:
            wires = []
            def ext(l):
                Q = np.array([p for e, a, b in loop_ends(l) if a is not None and b is not None for p in curve_pts(e, a, b, 8)])
                return float(np.linalg.norm(np.ptp(Q, 0))) if len(Q) else 0.0
            for l in sorted(f.get('loops', []), key=lambda l: -ext(l)):   # outer loop first
                W = BRepBuilderAPI_MakeWire()
                for e, a, b in loop_ends(l):
                    if a is None or b is None: raise ValueError('vertex')
                    E = occ_edge(e, a, b)
                    if E is not None: W.Add(E)
                if W.IsDone(): wires.append(W.Wire())
            if wires:
                mf = BRepBuilderAPI_MakeFace(S, wires[0], True)
                for w in wires[1:]: mf.Add(w)
                if mf.IsDone():
                    from OCP.ShapeFix import ShapeFix_Shape
                    from build123d import Shape
                    sf = ShapeFix_Face(mf.Face()); sf.Perform()
                    for G in (sf.Face(), None):
                        try:
                            if G is None:
                                ss = ShapeFix_Shape(mf.Face()); ss.Perform(); G = ss.Shape()
                            V, TT = Shape.cast(G).tessellate(0.02, 0.2)
                            if TT:
                                V = np.array([tuple(v) for v in V]); return [V[list(t)] for t in TT], 'occ'
                        except Exception as ex:
                            ERR.append((f['surface_type'], repr(ex)[:60]))
                else: ERR.append((f['surface_type'], str(mf.Error())))
        except Exception as ex:
            ERR.append((f['surface_type'], repr(ex)[:80]))
    return fan(f), 'fan'


def _net(f):
    return (1 if f.get('face_sense', '+') == '+' else -1) * (1 if f.get('surface_sense', '+') == '+' else -1)


def orient_arcs(J):
    """Arc sense is not decoded per edge (the fin sense alone is wrong for some edges, RV15).
    On a planar face, a circular edge shared with a cylinder/cone face is convex when the
    cylinder's net sense is '+' (material inside); Parasolid fins keep the face on their left
    seen from the outward normal, so the fin runs CCW about the plane's outward normal around a
    convex arc and CW around a concave one.  The chosen midpoint is used for both fins."""
    ARC_MID.clear()
    owner = {}
    for f in J['faces']:
        for l in f.get('loops', []):
            for e in l['edges']: owner.setdefault(e['edge'], []).append(f)
    for f in J['faces']:
        if f['surface_type'] != 'plane': continue
        N = np.array(f['params']['normal'], float) * _net(f)
        for l in f.get('loops', []):
            for e, a, b in loop_ends(l):
                c = e.get('curve') or {}
                if c.get('type') != 'circle' or a is None or b is None or np.linalg.norm(np.array(a) - np.array(b)) < 1e-9: continue
                oth = [g for g in owner.get(e['edge'], []) if g is not f and g['surface_type'] in ('cylinder', 'cone')]
                if not oth: continue
                convex = _net(oth[0]) > 0
                C = np.array(c['centre']); X = np.array(a) - C; X /= np.linalg.norm(X); Y = np.cross(N, X)
                ang = math.atan2((np.array(b) - C) @ Y, (np.array(b) - C) @ X) % (2 * math.pi)
                sw = ang if convex else ang - 2 * math.pi       # CCW about N when convex
                r = c['radius']
                ARC_MID[e['edge']] = C + r * (math.cos(sw / 2) * X + math.sin(sw / 2) * Y)


def mesh(decoded_json, stats=None):
    _VX.clear()
    J = json.load(open(decoded_json)) if isinstance(decoded_json, str) else decoded_json
    orient_arcs(J)
    out = []
    for f in J['faces']:
        T, how = face_tris(f)
        if stats is not None: stats[how] = stats.get(how, 0) + 1
        out += T
    return np.array(out) if out else None


# ----------------------------------------------------------------------------- UV mesher (round 15)
import shapely
from shapely.geometry import Polygon, box as sbox
from shapely.ops import unary_union

TWO_PI = 2 * math.pi


def _frame(p, ax_key):
    a = np.array(p[ax_key], float); a /= np.linalg.norm(a)
    X = np.array(p['x_axis'], float); X = X - a * (X @ a); X /= np.linalg.norm(X)
    return a, X, np.cross(a, X)


def param(f, pts):
    """(to_uv(P[N,3]) -> [N,2], from_uv([N,2]) -> [N,3], periodic_u, periodic_v, u-scale) in mm."""
    p = f.get('params') or {}; t = f['surface_type']
    if t == 'plane':
        o = np.array(p['point']) * MM; n = np.array(p['normal'], float); X = np.array(p['x_axis'], float); Y = np.cross(n, X)
        return (lambda P: np.c_[(P - o) @ X, (P - o) @ Y]), (lambda U: o + np.outer(U[:, 0], X) + np.outer(U[:, 1], Y)), False, False
    if t in ('cylinder', 'cone'):
        a, X, Y = _frame(p, 'axis'); o = np.array(p['point']) * MM
        def to(P):
            w = P - o; return np.c_[np.arctan2(w @ Y, w @ X), w @ a]
        if t == 'cylinder':
            r = p['radius'] * MM; k0, k1 = r, 0.0
        else:   # radius linear in v, fitted on the boundary points (sign convention of the half angle not needed)
            w = pts - o; h = w @ a; rho = np.linalg.norm(w - np.outer(h, a), axis=1)
            k1 = math.tan(math.radians(p['half_angle_deg'])) * (1 if np.corrcoef(h, rho)[0, 1] >= 0 else -1) if np.ptp(h) > 1e-9 else 0.0
            k0 = float(np.mean(rho - k1 * h))
        fr = lambda U: o + np.outer(U[:, 1], a) + (k0 + k1 * U[:, 1])[:, None] * (np.outer(np.cos(U[:, 0]), X) + np.outer(np.sin(U[:, 0]), Y))
        return to, fr, True, False
    if t == 'sphere':
        a, X, Y = _frame(p, 'axis'); c = np.array(p['centre']) * MM; r = p['radius'] * MM
        to = lambda P: np.c_[np.arctan2((P - c) @ Y, (P - c) @ X), np.arcsin(np.clip(((P - c) @ a) / r, -1, 1))]
        fr = lambda U: c + r * (np.cos(U[:, 1])[:, None] * (np.outer(np.cos(U[:, 0]), X) + np.outer(np.sin(U[:, 0]), Y)) + np.outer(np.sin(U[:, 1]), a))
        return to, fr, True, False
    if t == 'torus':
        a, X, Y = _frame(p, 'axis'); c = np.array(p['centre']) * MM; R = p['major_radius'] * MM; r = p['minor_radius'] * MM
        def to(P):
            w = P - c; h = w @ a; rho = np.linalg.norm(w - np.outer(h, a), axis=1)
            return np.c_[np.arctan2(w @ Y, w @ X), np.arctan2(h, rho - R)]
        fr = lambda U: c + (R + r * np.cos(U[:, 1]))[:, None] * (np.outer(np.cos(U[:, 0]), X) + np.outer(np.sin(U[:, 0]), Y)) + np.outer(r * np.sin(U[:, 1]), a)
        return to, fr, True, True
    return None


def uv_mesh(f, du=0.2):
    loops = []
    for l in f.get('loops', []):
        Q = []
        for e, a, b in loop_ends(l):
            if a is None or b is None: return None
            Q += [np.array(q) * MM for q in curve_pts(e, a, b, 24)[:-1]]
        if len(Q) < 2: return None
        loops.append(np.array(Q))
    if not loops: return None
    pr = param(f, np.concatenate(loops))
    if pr is None: return None
    to, fr, pu, pv = pr
    closed, wind = [], []
    for Q in loops:
        U = to(np.vstack([Q, Q[:1]]))
        if pu: U[:, 0] = np.unwrap(U[:, 0])
        if pv: U[:, 1] = np.unwrap(U[:, 1])
        nw = int(round((U[-1, 0] - U[0, 0]) / TWO_PI)) if pu else 0
        if pv and int(round((U[-1, 1] - U[0, 1]) / TWO_PI)) != 0: return None
        U = U[:-1]
        if nw == 0: closed.append(U)
        else: wind.append((U, nw))
    U0 = min([U[:, 0].min() for U in closed] + [U[:, 0].min() for U, _ in wind]) if pu else 0
    def norm_u(U):
        if not pu: return U
        U = U.copy(); m = U[:, 0].mean(); U[:, 0] -= TWO_PI * math.floor((m - U0) / TWO_PI); return U
    geoms = [Polygon(norm_u(U)).buffer(0) for U in closed if len(U) >= 3]
    vall = np.concatenate([U[:, 1] for U in closed] + [U[:, 1] for U, _ in wind])
    if wind:
        if len(wind) % 2: return None   # single winding loop (cap to a pole): not handled
        bands = []
        ext = []
        for U, nw in wind:
            if nw < 0: U = U[::-1]
            U = U.copy(); U[:, 0] -= TWO_PI * math.floor((U[0, 0] - U0) / TWO_PI)
            E = np.concatenate([U + [k * TWO_PI, 0] for k in (-1, 0, 1, 2)])
            ext.append(E)
        ext.sort(key=lambda E: E[:, 1].mean())
        for i in range(0, len(ext), 2):
            A, B = ext[i], ext[i + 1]
            bands.append(Polygon(np.concatenate([A, B[::-1]])).buffer(0))
        clip = sbox(U0, vall.min() - 1, U0 + TWO_PI, vall.max() + 1)
        geoms = [unary_union(bands).intersection(clip)] + geoms
    reg = geoms[0]
    for g in geoms[1:]: reg = reg.symmetric_difference(g)
    if reg.is_empty: return None
    if pu or pv:   # strips so flat triangles follow the curvature
        lo, hi = np.array(reg.bounds[:2]), np.array(reg.bounds[2:])
        us = np.arange(lo[0], hi[0] + du, du) if pu else [lo[0] - 1, hi[0] + 1]
        vs = np.arange(lo[1], hi[1] + du, du) if pv else [lo[1] - 1, hi[1] + 1]
        pieces = [reg.intersection(sbox(us[i], vs[j], us[i + 1], vs[j + 1])) for i in range(len(us) - 1) for j in range(len(vs) - 1)]
    else:
        pieces = [reg]
    out = []
    for pc in pieces:
        if pc.is_empty or pc.area <= 0: continue
        tri = shapely.constrained_delaunay_triangles(pc)
        for t in getattr(tri, 'geoms', [tri]):
            if t.is_empty: continue
            C = np.array(t.exterior.coords)[:3]
            out.append(fr(C))
    return out or None

