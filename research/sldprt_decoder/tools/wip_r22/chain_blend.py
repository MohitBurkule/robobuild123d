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
        if kind == 'fillet' and os.environ.get('R22_OFFBLEND', '1') == '1':
            # r22: manual blend by offset opening / closing, localised to a tube around the chain
            yield 'offset-open', lambda: offset_blend_sub(body, edges, size, v0)
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

# ---- r22: blend by morphological opening / closing (BRepOffsetAPI), localised to the chain
def _offset(shape, d):
    from OCP.BRepOffsetAPI import BRepOffsetAPI_MakeOffsetShape
    from OCP.BRepOffset import BRepOffset_Skin
    from OCP.GeomAbs import GeomAbs_Arc
    mk = BRepOffsetAPI_MakeOffsetShape()
    mk.PerformByJoin(shape.wrapped, d, 1e-4, BRepOffset_Skin, False, False, GeomAbs_Arc, False)
    if not mk.IsDone(): return None
    S = mk.Shape()
    from OCP.TopAbs import TopAbs_SHELL
    if S.ShapeType() == TopAbs_SHELL:
        from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeSolid
        from OCP.TopoDS import TopoDS
        ms = BRepBuilderAPI_MakeSolid(TopoDS.Shell(S) if hasattr(TopoDS, 'Shell') else TopoDS.Shell_s(S))
        if not ms.IsDone(): return None
        S = ms.Solid()
    return _wrap(S)

BALLS = os.environ.get('R22_OBALLS', '0') == '1'

def tube(edges, r):
    """union of pipes of radius r along the edges plus balls at their ends (the blend's reach)."""
    from build123d import Solid, Wire, Plane, Face, Circle, Vector
    from OCP.BRepOffsetAPI import BRepOffsetAPI_MakePipe
    parts = []
    for e in edges:
        try:
            p0 = e.position_at(0); t0 = e.tangent_at(0)
            prof = Face(Wire.make_circle(r, Plane(origin=p0, z_dir=t0)))
            mk = BRepOffsetAPI_MakePipe(Wire([e]).wrapped, prof.wrapped); mk.Build()
            if mk.IsDone(): parts.append(_wrap(mk.Shape()))
            if BALLS:
                for q in (p0, e.position_at(1)): parts.append(Solid.make_sphere(r).moved(__import__('build123d').Location(q)))
        except Exception: continue
    if not parts: return None
    T = parts[0]
    for p in parts[1:]: T = _one(T.fuse(p))
    return T

def _one(x):
    if x is None: return None
    if isinstance(x, (list, tuple)) or type(x).__name__ == 'ShapeList':
        return Compound(list(x)) if len(x) else None
    return x

def offset_blend(body, edges, r, v0=None):
    """fillet of an edge chain as body - ((body - open_r(body)) & tube) for convex edges, and
    body + ((close_r(body) - body) & tube) for concave ones; the variant that changes the volume
    near the chain is returned (or None)."""
    T = tube(edges, float(os.environ.get('R22_OTUBE', 1.05)) * r)
    if T is None: return None
    out = None
    try:
        a = _offset(body, -r); o = _offset(a, r) if a is not None else None
        if o is not None:
            rem = _one(_one(body.cut(o)).intersect(T))
            if rem is not None and rem.volume > 1e-9: out = _one(body.cut(rem))
    except Exception: out = None
    if out is None:
        try:
            a = _offset(body, r); c = _offset(a, -r) if a is not None else None
            if c is not None:
                add = _one(_one(c.cut(body)).intersect(T))
                if add is not None and add.volume > 1e-9: out = _one(body.fuse(add))
        except Exception: out = None
    return out if _ok(out, v0) else None


def offset_blend_sub(body, edges, r, v0=None, tmo=None):
    """offset_blend in a child process with a hard timeout (BRepOffsetAPI can run for ever on a large
    body: RV01 Fillet10 hung past the part timeout).  Edges travel as their centres."""
    import tempfile, subprocess, sys, json
    from build123d import export_brep, import_brep
    tmo = tmo or float(os.environ.get('R22_OFFTMO', 60))
    d = tempfile.mkdtemp(prefix='r22off_'); bi, bo = os.path.join(d, 'in.brep'), os.path.join(d, 'out.brep')
    export_brep(body, bi)
    cs = [tuple(e.center()) for e in edges]
    code = ("import sys, json; sys.path.insert(0, %r); import chain_blend as CB\n"
            "from build123d import import_brep, export_brep\n"
            "b = import_brep(%r); cs = json.loads(%r)\n"
            "E = [min(b.edges(), key=lambda x: (x.center() - __import__('build123d').Vector(*c)).length) for c in cs]\n"
            "nb = CB.offset_blend(b, E, %r, %r)\n"
            "if nb is not None: export_brep(nb, %r)\n") % (os.path.dirname(os.path.abspath(__file__)), bi, json.dumps(cs), r, v0, bo)
    try: subprocess.run([sys.executable, '-c', code], timeout=tmo, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.TimeoutExpired: return None
    if not os.path.exists(bo): return None
    try: nb = import_brep(bo)
    except Exception: return None
    return nb if _ok(nb, v0) else None
