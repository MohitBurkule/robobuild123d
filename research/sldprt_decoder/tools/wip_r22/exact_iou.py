"""Round 17 non-voxel oracle metrics (resolution-free; replaces the 0.2 mm voxel IoU as the score).

  * exact_iou(A, B):   boolean volume IoU of two closed triangle meshes (mm), computed with
                       manifold3d (exact mesh booleans).  A B-rep body is tessellated finely first
                       (linear deflection 0.002 mm), so the only error is tessellation chord error.
  * surf_dist(A, B):   symmetric point-to-surface distance sampling: area-weighted samples on each
                       mesh, exact closest-point distance to the other mesh (trimesh proximity);
                       returns mean / p95 / max and the F-score at tol (fraction within tol both ways).
  * mesh_of(shape):    B-rep -> welded triangle array (n,3,3) in mm.
Meshes that are not watertight are welded with a tolerance; if still open (XT-face meshes) the
volume IoU is not defined here (None) and callers use surf_dist / the voxel score instead.
The oracle mesh is only scored against; nothing from it enters a model."""
import numpy as np

def mesh_of(shape, tol=0.002, ang=0.1):
    from OCP.BRepMesh import BRepMesh_IncrementalMesh
    from OCP.BRep import BRep_Tool
    from OCP.TopLoc import TopLoc_Location
    from OCP.TopAbs import TopAbs_REVERSED
    w = shape.wrapped if hasattr(shape, 'wrapped') else shape
    BRepMesh_IncrementalMesh(w, tol, False, ang, True)
    out = []
    for f in (shape.faces() if hasattr(shape, 'faces') else []):
        loc = TopLoc_Location(); tr = BRep_Tool.Triangulation_s(f.wrapped, loc)
        if tr is None: continue
        T = loc.Transformation()
        P = np.array([[p.X(), p.Y(), p.Z()] for p in (tr.Node(i).Transformed(T) for i in range(1, tr.NbNodes() + 1))])
        I = np.array([tr.Triangle(i).Get() for i in range(1, tr.NbTriangles() + 1)]) - 1
        if f.wrapped.Orientation() == TopAbs_REVERSED: I = I[:, ::-1]
        out.append(P[I])
    return np.concatenate(out) if out else np.zeros((0, 3, 3))

def _tm(T, weld=1e-4):
    import trimesh
    m = trimesh.Trimesh(vertices=np.asarray(T, float).reshape(-1, 3), faces=np.arange(len(T) * 3).reshape(-1, 3), process=False)
    m.merge_vertices(digits_vertex=int(-np.log10(weld)))
    m.remove_degenerate_faces() if hasattr(m, 'remove_degenerate_faces') else None
    m.update_faces(m.nondegenerate_faces()) if hasattr(m, 'nondegenerate_faces') else None
    m.remove_unreferenced_vertices()
    return m

def _manifold(m):
    import manifold3d as M3
    mm = M3.Manifold(M3.Mesh(vert_properties=np.asarray(m.vertices, np.float32), tri_verts=np.asarray(m.faces, np.uint32)))
    if mm.status() != M3.Error.NoError or mm.is_empty(): return None
    if mm.volume() < 0: return None
    return mm

def as_manifold(T):
    for w in (1e-5, 1e-4, 1e-3):
        m = _tm(T, w)
        mm = _manifold(m)
        if mm is not None and abs(mm.volume() - abs(m.volume)) < 1e-3 * abs(m.volume) + 1e-6: return mm
    return None

def mc_iou(A, B, n=400000, seed=0):
    """fallback: Monte-Carlo volume IoU with exact (ray-parity) point classification."""
    a, b = _tm(A), _tm(B)
    lo = np.minimum(a.bounds[0], b.bounds[0]); hi = np.maximum(a.bounds[1], b.bounds[1])
    P = lo + np.random.default_rng(seed).random((n, 3)) * (hi - lo)
    ia = a.contains(P); ib = b.contains(P)
    u = (ia | ib).sum(); return float((ia & ib).sum() / max(u, 1))

def exact_iou(A, B):
    """volume IoU of meshes A, B (n,3,3 arrays, mm) -> (iou, method)."""
    ma, mb = as_manifold(A), as_manifold(B)
    if ma is not None and mb is not None:
        i = (ma ^ mb).volume(); u = ma.volume() + mb.volume() - i
        return float(i / u) if u > 0 else 0.0, 'manifold'
    return None, 'open mesh'      # ray-parity Monte Carlo on open meshes crashes trimesh/rtree: callers fall back

def surf_dist(A, B, n=20000, tol=0.05, seed=0):
    import trimesh
    a, b = _tm(A), _tm(B)
    pa, _ = trimesh.sample.sample_surface(a, n, seed=seed); pb, _ = trimesh.sample.sample_surface(b, n, seed=seed + 1)
    da = np.abs(trimesh.proximity.closest_point(b, pa)[1]); db = np.abs(trimesh.proximity.closest_point(a, pb)[1])
    d = np.concatenate([da, db])
    prec, rec = float((da <= tol).mean()), float((db <= tol).mean())
    return dict(mean=float(d.mean()), p95=float(np.percentile(d, 95)), max=float(d.max()), tol=tol,
                precision=prec, recall=rec, fscore=2 * prec * rec / max(prec + rec, 1e-12))

def occ_solid_of_mesh(T):
    """r19: closed triangle mesh (mm) -> OCC solid (sewn planar triangles), for B-rep booleans
    against a body whose own tessellation does not close (RV23 / side panel / their mirrors)."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace, BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
    from OCP.gp import gp_Pnt
    from OCP.TopoDS import TopoDS
    from OCP.ShapeFix import ShapeFix_Solid
    m = _tm(T, 1e-5)
    V = np.asarray(m.vertices, float)
    sw = BRepBuilderAPI_Sewing(1e-6)
    for f in m.faces:
        a, b, c = (V[i] for i in f)
        if np.linalg.norm(np.cross(b - a, c - a)) < 1e-12: continue
        pg = BRepBuilderAPI_MakePolygon(gp_Pnt(*a), gp_Pnt(*b), gp_Pnt(*c), True)
        sw.Add(BRepBuilderAPI_MakeFace(pg.Wire(), True).Face())
    sw.Perform()
    sh = TopoDS.Shell(sw.SewedShape()) if hasattr(TopoDS, "Shell") else TopoDS.Shell_s(sw.SewedShape())
    so = BRepBuilderAPI_MakeSolid(sh).Solid()
    fx = ShapeFix_Solid(so); fx.Perform()
    return fx.Solid()

def occ_iou(body, T):
    """r19: volume IoU of a B-rep body and a closed mesh by OCC booleans (exact up to the mesh)."""
    from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
    from OCP.GProp import GProp_GProps
    from OCP.BRepGProp import BRepGProp
    def vol(s):
        g = GProp_GProps(); BRepGProp.VolumeProperties_s(s, g); return abs(g.Mass())
    S = occ_solid_of_mesh(T); w = body.wrapped if hasattr(body, 'wrapped') else body
    i = vol(BRepAlgoAPI_Common(w, S).Shape()); a, b = vol(w), vol(S)
    return i / max(a + b - i, 1e-12)
