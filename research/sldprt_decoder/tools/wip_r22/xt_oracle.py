"""Round 22 internal face oracle: the decoded final-body XT faces built as OCC faces (analytic
surface + loop wires, xt_mesh), then recorded with face_audit.faces_from_shape, so area and bbox
come from the same code path as the rebuilt body.  audit(xt, body) 'matched' then uses the same
standard (same surface, bbox within 0.05 mm, area within 1 %) as the dump audit.  Decode-only."""
import numpy as np, os
ALLMINOR = os.environ.get('R22_ALLMINOR', '1') == '1'
MINOR = os.environ.get('R22_MINOR', '1') == '1'
import xt_mesh as XM

def _edge(e, a, b):
    """XM.occ_edge, falling back to a parameter-trimmed edge when a decoded vertex is not on the
    curve within the vertex tolerance (BRep_API: command not done)."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
    c = e.get('curve') or {}
    if c.get('type') == 'circle' and np.linalg.norm(np.array(a) - np.array(b)) > 1e-10:
        # r22: the arc through the sampled midpoint (curve_pts honours the decoded arc midpoint,
        # occ_edge does not: quarter-round faces came out as three-quarter rounds)
        from OCP.GC import GC_MakeArcOfCircle
        Q = XM.curve_pts(e, a, b, 2)
        if (e.get('edge') not in XM.ARC_MID or ALLMINOR) and MINOR:
            # no decoded arc sense: the minor arc (fillet / round ends are quarter arcs)
            C = np.array(c['centre']); M = np.array(Q[1]); H = (np.array(a) + np.array(b)) / 2
            M2 = C - (M - C)
            if np.linalg.norm(M2 - H) < np.linalg.norm(M - H): Q = [Q[0], M2, Q[2]]
        try:
            arc = GC_MakeArcOfCircle(XM.P(Q[0]), XM.P(Q[1]), XM.P(Q[2])).Value()
            try: return BRepBuilderAPI_MakeEdge(arc, XM.VX(a), XM.VX(b)).Edge(), True
            except Exception: return BRepBuilderAPI_MakeEdge(arc).Edge(), False
        except Exception: pass
    try: return XM.occ_edge(e, a, b), True
    except Exception: pass
    from OCP.gp import gp_Circ
    from OCP.ElCLib import ElCLib
    import math
    c = e.get('curve') or {}
    if c.get('type') != 'circle': return BRepBuilderAPI_MakeEdge(XM.P(a), XM.P(b)).Edge(), False
    nn = np.array(c['normal'], float) * (1 if e.get('fin_sense') != '-' else -1)
    g = gp_Circ(XM._ax2(c['centre'], nn, c['x_axis']), c['radius'] * XM.MM)
    u0 = ElCLib.Parameter_s(g, XM.P(a)); u1 = ElCLib.Parameter_s(g, XM.P(b))
    if np.linalg.norm(np.array(a) - np.array(b)) < 1e-10: u1 = u0 + 2 * math.pi
    elif u1 <= u0: u1 += 2 * math.pi
    return BRepBuilderAPI_MakeEdge(g, u0, u1).Edge(), False

OWNER = {}

def _plane_cut(f, e):
    """r22: an undecoded closed trimmed curve on a cylinder / cone (a hole's far end): its point on
    the plane face that shares the edge, where the axis meets that plane (x_axis side)."""
    p = f.get('params') or {}
    for g in OWNER.get(e.get('edge'), []):
        if g is f or g['surface_type'] != 'plane': continue
        n = np.array(g['params']['normal'], float); P0 = np.array(g['params']['point'], float)
        C = np.array(p['point'], float); ax = np.array(p['axis'], float); X = np.array(p['x_axis'], float)
        if abs(ax @ n) < 0.999: continue
        t = ((P0 - C) @ n) / (ax @ n); Q = C + t * ax
        if f['surface_type'] == 'cylinder': return list(Q + p['radius'] * X)
    return None

def _uv_band(f, S):
    """r22: a face bounded only by closed circles on a periodic surface (torus / cylinder / cone /
    sphere band): MakeFace with closed wires gives the whole surface; build it from its UV range
    instead (u full turn, v from the circles; on a torus the minor v arc)."""
    import math
    from OCP.GeomAPI import GeomAPI_ProjectPointOnSurf
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeFace
    loops = f.get('loops', [])
    if not loops or f['surface_type'] == 'plane': return None
    vs = []
    for l in loops:
        le = XM.loop_ends(l)
        if len(le) != 1: return None
        e, a, b = le[0]
        if a is None and (e.get('curve') or {}).get('type') == 'trimmed_curve' and f['surface_type'] in ('cylinder', 'cone'):
            a = b = _plane_cut(f, e)
        if (e.get('curve') or {}).get('type') not in ('circle', 'trimmed_curve') or a is None or np.linalg.norm(np.array(a) - np.array(b)) > 1e-10: return None
        pr = GeomAPI_ProjectPointOnSurf(XM.P(a), S)
        if pr.NbPoints() < 1: return None
        u, v = pr.LowerDistanceParameters(); vs.append(v)
    u0, u1, v0, v1 = S.Bounds()
    if len(vs) == 1:
        if f['surface_type'] in ('cone', 'cylinder'): return None
        vs.append(v1 if f['surface_type'] == 'sphere' else vs[0])
    va, vb = min(vs), max(vs)
    if f['surface_type'] == 'torus' and vb - va > math.pi: va, vb = vb, va + 2 * math.pi
    m = BRepBuilderAPI_MakeFace(S, 0.0, 2 * math.pi, va, vb, 1e-6)
    return m.Face() if m.IsDone() else None

def occ_face(f):
    """one decoded XT face -> OCC TopoDS_Face (or None)."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
    from OCP.ShapeFix import ShapeFix_Face
    S = XM.surface(f)
    if S is None: return None
    occ_face.loop_areas = None
    try:
        B = _uv_band(f, S)
        if B is not None: return B
    except Exception: pass
    def ext(l):
        Q = np.array([p for e, a, b in XM.loop_ends(l) if a is not None and b is not None for p in XM.curve_pts(e, a, b, 8)])
        return float(np.linalg.norm(np.ptp(Q, 0))) if len(Q) else 0.0
    wires = []
    from OCP.ShapeFix import ShapeFix_Wire
    from OCP.ShapeExtend import ShapeExtend_WireData
    for l in sorted(f.get('loops', []), key=lambda l: -ext(l)):
        Es, shared = [], True
        for e, a, b in XM.loop_ends(l):
            if a is None or b is None: return None
            E, ok = _edge(e, a, b); shared &= ok
            if E is not None: Es.append(E)
        if not Es: return None
        if shared:
            W = BRepBuilderAPI_MakeWire()
            for E in Es: W.Add(E)
            if W.IsDone(): wires.append(W.Wire()); continue
        wd = ShapeExtend_WireData()
        for E in Es: wd.Add(E)
        fw = ShapeFix_Wire(); fw.Load(wd); fw.SetPrecision(2e-3); fw.FixConnected(); fw.FixClosed()
        wires.append(fw.Wire())
    if not wires: return None
    occ_face.loop_areas = None
    if len(wires) > 1 and f['surface_type'] == 'plane':
        # r22: decoded loop orientation is not reliable for OCC: a plane's area is the outer loop's
        # area minus its holes, each taken from a one-loop face
        from OCP.GProp import GProp_GProps
        from OCP.BRepGProp import BRepGProp
        A = []
        for w in wires:
            m1 = BRepBuilderAPI_MakeFace(S, w, True)
            if not m1.IsDone(): return None
            g = GProp_GProps(); BRepGProp.SurfaceProperties_s(m1.Face(), g); A.append(abs(g.Mass()))
        k = int(np.argmax(A)); occ_face.loop_areas = (A[k] - (sum(A) - A[k])) / 1e0
        wires = [wires[k]] + wires[:k] + wires[k + 1:]
    mf = BRepBuilderAPI_MakeFace(S, wires[0], True)
    for w in wires[1:]: mf.Add(w)
    if not mf.IsDone(): return None
    sf = ShapeFix_Face(mf.Face()); sf.FixOrientationMode = 1; sf.Perform(); sf.FixOrientation(); return sf.Face()

def xt_faces(d):
    """face_audit Face records of the decoded XT faces of decoded dict d (analytic faces only;
    faces that fail to build fall back to the loop-curve box with area 0, which can only reach
    'area', never 'matched')."""
    import face_audit as FA
    from build123d import Shape, Compound
    XM.orient_arcs(d)
    OWNER.clear()
    for g in d['faces']:
        for l in g.get('loops', []):
            for e in l['edges']: OWNER.setdefault(e.get('edge'), []).append(g)
    out, n_fb = [], 0
    for f in d['faces']:
        if f['surface_type'] not in ('plane', 'cylinder', 'cone', 'sphere', 'torus'): continue
        G = None
        try: G = occ_face(f); la = occ_face.loop_areas
        except Exception: G = None
        rec = []
        if G is not None:
            try:
                rec = FA.faces_from_shape(Compound([Shape.cast(G)]))
                for r_ in rec: r_.area = abs(r_.area) if la is None else la   # reversed loop orientation gives a signed (negative) area
                if rec and not (rec[0].area > 1e-9): rec = []
            except Exception: rec = []
        if rec: out += rec
        else: n_fb += 1
    xt_faces.fallback = n_fb
    return out

def count(xt, body):
    """strict matched XT patches of body (same rule as the dump audit 'matched')."""
    import face_audit as FA
    if not xt or body is None: return 0
    try: r = FA.audit(xt, FA.faces_from_shape(body))
    except Exception: return 0
    return r['counts'].get('matched', 0)

def n_patches(xt):
    import face_audit as FA
    return len(FA.make_patches(xt)) if xt else 0
