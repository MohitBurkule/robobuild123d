"""r21: OCC blend variants for tangent edge chains that BRepFilletAPI_MakeFillet rejects as one set.
variants(body, edges, size, kind) yields (tag, body) for each variant that OCC builds and that is a
valid solid: chain-ordered edges, the QuasiAngular / Polynomial fillet shapes, loosened SetParams,
and per-edge sequential building (each edge re-found on the previous result by its centre)."""
import os
from build123d import Shape, Compound

def _wrap(s):
    try: return Shape.cast(s)
    except Exception: return Compound(s)

def order_chain(edges):
    """order edges so consecutive ones share an end point (tangent chains); others keep their order."""
    if len(edges) < 3: return list(edges)
    ends = []
    for e in edges:
        try: ends.append((e.position_at(0), e.position_at(1)))
        except Exception: return list(edges)
    left = list(range(len(edges))); out = [left.pop(0)]
    while left:
        a0, a1 = ends[out[-1]]
        j = min(left, key=lambda i: min((ends[i][0] - a1).length, (ends[i][1] - a1).length, (ends[i][0] - a0).length, (ends[i][1] - a0).length))
        out.append(j); left.remove(j)
    return [edges[i] for i in out]

def _fillet(shape, edges, r, fshape=None, params=None):
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeFillet
    from OCP.ChFi3d import ChFi3d_FilletShape
    mk = BRepFilletAPI_MakeFillet(shape.wrapped, getattr(ChFi3d_FilletShape, fshape or 'ChFi3d_Rational'))
    if params: mk.SetParams(*params)
    for e in edges: mk.Add(r, e.wrapped)
    mk.Build()
    if not mk.IsDone(): return None
    return _wrap(mk.Shape())

def _chamfer(shape, edges, d):
    from OCP.BRepFilletAPI import BRepFilletAPI_MakeChamfer
    mk = BRepFilletAPI_MakeChamfer(shape.wrapped)
    for e in edges: mk.Add(d, e.wrapped)
    mk.Build()
    if not mk.IsDone(): return None
    return _wrap(mk.Shape())

def _ok(b, v0):
    try: return b is not None and b.is_valid and b.volume > 0 and (v0 is None or abs(b.volume - v0) < 0.05 * abs(v0) + 1)
    except Exception: return False

def sequential(body, edges, size, kind, v0=None):
    cur = body; n = 0
    cs = [e.center() for e in edges]
    for c in cs:
        try:
            Ec = cur.edges(); e = min(Ec, key=lambda x: (x.center() - c).length)
            if (e.center() - c).length > 2 * size + 1e-3: continue   # a neighbour's blend trims the edge
            nb = _fillet(cur, [e], size) if kind == 'fillet' else _chamfer(cur, [e], size)
            if _ok(nb, v0): cur, n = nb, n + 1
        except Exception: continue
    return cur if n == len(edges) else None

def variants(body, edges, size, kind, v0=None, seq=True):
    seen = []
    def gen():
        if kind == 'fillet':
            oe = order_chain(edges)
            yield 'chain-ordered', lambda: _fillet(body, oe, size)
            yield 'quasi-angular', lambda: _fillet(body, oe, size, 'ChFi3d_QuasiAngular')
            yield 'polynomial', lambda: _fillet(body, oe, size, 'ChFi3d_Polynomial')
            yield 'loose-params', lambda: _fillet(body, oe, size, None, (1e-3, 1e-3, 1e-2, 1e-4))
        else:
            yield 'chain-ordered', lambda: _chamfer(body, order_chain(edges), size)
        if seq and len(edges) > 1: yield 'per-edge', lambda: sequential(body, edges, size, kind, v0)
    for tag, f in gen():
        try: b = f()
        except Exception: b = None
        if _ok(b, v0): yield tag, b

def components(edges, tol=1e-4):
    """index lists of the connected chains (edges sharing an end point) among edges."""
    n = len(edges); par = list(range(n))
    def fnd(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    try: ends = [(e.position_at(0), e.position_at(1)) for e in edges]
    except Exception: return [list(range(n))]
    for a in range(n):
        for b in range(a + 1, n):
            if min((x - y).length for x in ends[a] for y in ends[b]) < tol: par[fnd(a)] = fnd(b)
    out = {}
    for i in range(n): out.setdefault(fnd(i), []).append(i)
    return list(out.values())
