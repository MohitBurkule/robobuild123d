#!/usr/bin/env python3
"""Round 15-17: decode-only feature replay driven by an in-file oracle.

Round 17: when the oracle mesh is closed (every Contents/DisplayLists mesh is), every decision is
scored with exact mesh booleans (manifold3d, ExactTrack below) instead of the 0.2 mm voxel grid.

Inputs, all decoded from the SLDPRT (no dumps, no reference STL):
  * feature tree, sketches, sketch planes, end conditions, fillet sizes, mirror/pattern planes,
    XT faces with their creating features   (decoded json + regenerated side files, as round 14)
  * the final-body display mesh in Contents/DisplayLists   (sldprt/displaylist.py, new in round 15)
    or, when a file has none, a mesh tessellated from the decoded XT faces   (xt_mesh.py)

The replay is the dump replay (rebuild_dump/rv01_from_dump.Rebuild) fed by an adapter that turns
the decoded data into its Part/Feature/Sketch objects.  The oracle mesh plays the role the
reference solid plays there: it is only *queried* (voxel membership) to choose sketch cells,
extrude extents, mirror/pattern seeds and blend edges.  No oracle geometry enters the model.

  python3 decode_replay.py [part-prefix ...]      -> decode_replay.json / .txt
"""
import sys, os, json, math, re, glob, time, io, contextlib, traceback
import numpy as np
HERE = os.environ.get('R15_OUT') or os.path.dirname(os.path.abspath(__file__))
TOOLS = os.environ.get('R15_TOOLS') or os.path.abspath(os.path.join(HERE, '..'))
ROOT = os.path.abspath(os.path.join(TOOLS, '..'))
for p in (TOOLS, os.path.join(ROOT, 'rebuild'), os.path.join(ROOT, 'rebuild_dump'), os.path.join(TOOLS, 'wip_r14')):
    if p not in sys.path: sys.path.insert(0, p)
import rv01_from_dump as FD
import dump_parser as DP
import rv01_rebuild as R
import decode_only as DO
from sldprt import displaylist as DL
from build123d import Solid, Compound, Vector, Location, Plane, Axis, Face, extrude, revolve, export_brep

MM = 1000.0
SRC = os.environ.get('R16_SRC', 'revdev')        # 'corpus' for the round-16 generalization check
if SRC != 'revdev':
    DO.DEC = os.path.join(ROOT, 'decoded_' + SRC)
    DO.OUT = os.path.join(ROOT, 'tools', 'wip_r17', 'decode_only_' + SRC); os.makedirs(DO.OUT, exist_ok=True)
    _src = open(DO.__file__).read()
    exec(compile(_src[_src.index('def regen(part):'):_src.index('class GRebuild')].replace("'revdev'", repr(SRC)), DO.__file__, 'exec'), DO.__dict__)
    import mirror_derived as _MD; _MD.DEC = DO.DEC
BIG = FD.BIG
LOG = FD.LOG


def num(s):
    s = str(s).replace('<MOD-DIAM>', '')
    m = re.search(r'-?\d+(\.\d+)?', s)
    return float(m.group()) if m else None


# ----------------------------------------------------------------------------- oracle
class MeshRef(FD.Ref):
    """FD.Ref over a triangle soup (mm).  Membership = z-ray parity on a voxel grid."""
    def __init__(self, T, source):
        self.T = np.asarray(T, float); self.source = source
        self.V = abs(DL.volume(self.T)); self.s = None; self.faces = []; self.kinds = []
        self.M = None
        if os.environ.get('R17_EXACT', '1') == '1' and source != 'xt_faces':
            import exact_iou as XI
            try:
                M = XI.as_manifold(self.T)
                if M is not None and abs(M.volume() - self.V) < 0.01 * self.V + 1e-3: self.M = M
            except Exception: self.M = None
        self.exact = self.M is not None

    def init_points(self, cache=None, max_cells=12e6):
        lo = self.T.reshape(-1, 3).min(0) - 1.0; hi = self.T.reshape(-1, 3).max(0) + 1.0
        dxy, dz = 0.2, 0.1
        while np.prod(np.ceil((hi - lo) / np.array([dxy, dxy, dz]))) > max_cells: dxy *= 1.25; dz *= 1.25
        self.G = FD.Grid(lo, hi, dxy, dz); self.dv = self.G.dv
        self.rin = grid_inside_tris(self.G, self.T)
        self.Vpts = self.rin.sum() * self.dv

    def at(self, P):
        """grid flat indices of points P (outside grid -> -1)."""
        G = self.G; k = np.floor((np.atleast_2d(P) - G.lo) / G.d).astype(int)
        ok = np.all((k >= 0) & (k < G.n), 1)
        idx = np.full(len(k), -1); idx[ok] = np.ravel_multi_index(k[ok].T, G.n); return idx


def grid_inside_tris(G, T):
    """FD.Grid.inside for a raw triangle soup."""
    class _S:
        def tessellate(self, *a):
            V = T.reshape(-1, 3); return [Vector(*v) for v in V], np.arange(len(V)).reshape(-1, 3).tolist()
    return G.inside(_S())


def oracle_for(part):
    path = os.path.join(ROOT, SRC, part + '.SLDPRT')
    T = DL.triangles(path)
    if T is not None and len(T) > 12: return MeshRef(T, 'displaylist')
    # no display mesh: a mirror-derived twin's display mesh, reflected back (RV17 <- RV18)
    import mirror_derived as MD
    for q in sorted(glob.glob(os.path.join(DO.DEC, '*.json'))):
        twin = os.path.basename(q)[:-5]
        if '.' in twin: continue
        try:
            if MD.source_of(twin) != part: continue
        except Exception: continue
        T = DL.triangles(os.path.join(ROOT, SRC, twin + '.SLDPRT'))
        if T is None or len(T) <= 12: continue
        sc, n, d = MD.fit_plane(part, twin)
        if sc < 0.95: continue
        T = MD.reflect(T.reshape(-1, 3), n, d).reshape(-1, 3, 3)[:, ::-1]   # a reflection flips the winding
        return MeshRef(T, f'displaylist of mirror twin {twin} (plane n={n.tolist()} d={d}, fit {sc:.3f})')
    try:
        import xt_mesh
        T = xt_mesh.mesh(os.path.join(DO.DEC, part + '.json'))
        if T is not None and len(T): return MeshRef(T, 'xt_faces')
    except Exception as ex:
        print('xt mesh failed', repr(ex))
    return None


# ----------------------------------------------------------------------------- decoded -> dump objects
def xt_surface(f):
    """decoded XT face -> dump_parser.Surface (metres) with a box from the loop geometry."""
    p = f.get('params') or {}; t = f['surface_type']
    if t == 'plane' and 'normal' in p: S = DP.Surface('plane', dict(n=tuple(p['normal']), o=tuple(p['point'])))
    elif t == 'cylinder' and 'axis' in p: S = DP.Surface('cyl', dict(o=tuple(p['point']), ax=tuple(p['axis']), r=p['radius']))
    elif t == 'cone' and 'axis' in p: S = DP.Surface('cone', dict(values=list(p['point']) + list(p['axis']) + [p['radius'], math.radians(p.get('half_angle_deg', 0))]))
    elif t == 'torus' and 'axis' in p: S = DP.Surface('torus', dict(values=list(p['centre']) + list(p['axis']) + [p['major_radius'], p['minor_radius']]))
    elif t == 'sphere' and 'radius' in p: S = DP.Surface('sphere', dict(values=list(p['centre']) + [p['radius']]))
    else: S = DP.Surface('other', {})
    P = []
    for l in f.get('loops', []):
        for e in l['edges']:
            if e.get('start_vertex'): P.append(e['start_vertex'])
            c = e.get('curve') or {}
            if c.get('type') == 'circle' and len(l['edges']) == 1:   # full circle loop: whole circle
                C = np.array(c['centre']); n = np.array(c['normal'], float); x = np.array(c['x_axis'], float); y = np.cross(n, x)
                for a in np.linspace(0, 2 * math.pi, 13): P.append(list(C + c['radius'] * (math.cos(a) * x + math.sin(a) * y)))
    if P:
        P = np.array(P); S.box = list(P.min(0)) + list(P.max(0))
    S.raw = f'xt{f.get("xt_index")}'
    return S


def seg_list(rb, name):
    """decoded sketch -> dump_parser.Seg list (metres), arcs oriented as the round-14 rebuild does."""
    sk = rb.sk[name]
    ents, _ = R.sketch_entities(sk); R.resolve_arcs(ents)
    try:
        with contextlib.redirect_stdout(io.StringIO()): rb.orient_arcs(name, ents)
    except Exception: pass
    if os.environ.get('R17_ARC_CCW', '1') == '1':
        # round 17: SolidWorks stores sketch arcs counter-clockwise from the decoded start point to
        # the decoded end point (194 / 195 arcs of dumps_v2 agree); the bulge / XT-cylinder
        # heuristics picked the major arc for shallow arcs (FS1 knurl groove: a 10 mm^2 cell
        # instead of 0.1 mm^2)
        for e in ents:
            if e['type'] != 'arc': continue
            c = e['c']; a0 = math.atan2(e['a'][1] - c[1], e['a'][0] - c[0]); a1 = math.atan2(e['b'][1] - c[1], e['b'][0] - c[0])
            e['a0'] = a0; e['sweep'] = (a1 - a0) % (2 * math.pi) or 2 * math.pi
    ents, dropped = R.drop_crossing(ents)
    out = []
    for i, e in enumerate(ents):
        if e['type'] == 'line':
            out.append(DP.Seg(f'{i}', 0, False, p0=(e['a'][0] / MM, e['a'][1] / MM, 0), p1=(e['b'][0] / MM, e['b'][1] / MM, 0)))
        elif e['type'] == 'circle':
            c = e['c']; r = e['r']; p = ((c[0] + r) / MM, c[1] / MM, 0)
            out.append(DP.Seg(f'{i}', 1, False, p0=p, p1=p, c=(c[0] / MM, c[1] / MM, 0), r=r / MM, dir=1))
        else:
            out.append(DP.Seg(f'{i}', 1, False, p0=(e['a'][0] / MM, e['a'][1] / MM, 0), p1=(e['b'][0] / MM, e['b'][1] / MM, 0),
                              c=(e['c'][0] / MM, e['c'][1] / MM, 0), r=e['r'] / MM, dir=1 if e['sweep'] > 0 else -1))
    key = lambda q: (round(q[0], 7), round(q[1], 7))
    vs = {key(p) for e in sk['entities'] if e.get('flag') == 1 for p in (e.get('start'), e.get('end')) if p}
    prof = {tuple(sorted((key(e['start']), key(e['end'])))) for e in sk['entities']
            if e.get('flag') == 1 and e['type'] == 'line' and e.get('start') and e.get('end')}
    seen0 = set()
    for j, e in enumerate(sk['entities']):   # construction lines (revolve axes)
        if e.get('flag') == 0 and e['type'] == 'line' and e.get('start') and e.get('end'):
            k2 = tuple(sorted((key(e['start']), key(e['end']))))
            # round 17: a flag-0 copy of a profile line (RV17/RV23 sketches store each profile line
            # twice) is not a split line; repeated flag-0 copies are dropped
            if k2 in seen0: continue
            seen0.add(k2)
            if k2 in prof and os.environ.get('R17_DUP0', '1') == '1':
                out.append(DP.Seg(f'a{j}', 0, True, p0=tuple(e['start']) + (0,), p1=tuple(e['end']) + (0,))); continue
            # flag-0 line joining two profile vertices: often a mislabelled closing edge (RV19 Sketch1);
            # kept as a split line too: the oracle decides which cells are material
            closing = key(e['start']) in vs and key(e['end']) in vs
            out.append(DP.Seg(f'c{j}', 0, not closing, p0=tuple(e['start']) + (0,), p1=tuple(e['end']) + (0,)))
            if closing: out.append(DP.Seg(f'a{j}', 0, True, p0=tuple(e['start']) + (0,), p1=tuple(e['end']) + (0,)))
    return out, len(dropped)


def to_part(rb):
    """rb: a decode_only.GRebuild (decoded json + side files loaded).  Returns dump_parser.Part."""
    d = rb.d; feats = sorted(d['features'], key=lambda f: f['id'])
    faces_of = {}
    for f in rb.faces:
        for fid in set(f.get('feature_ids_by_time') or []): faces_of.setdefault(fid, []).append(f)
    created = {}
    for f in rb.faces:
        if f.get('feature_first') is not None: created.setdefault(f['feature_first'], []).append(f)
    out, by = [], {}
    for k, f in enumerate(feats):
        F = DP.Feature(k, f['name'], f['type'], f['id'], False, 0)
        F.decoded = f
        for dn, dv in f.get('dims', []):
            v = num(dv)
            if v is None: continue
            F.dims[f'{dn}@{f["name"]}@part'] = math.radians(v) if '°' in str(dv) else v / MM
        t = f['type']
        if t in ('Sketch', 'ProfileFeature', '3DSketch') and f['name'] in rb.sk and f['name'] in rb.sp:
            sp = rb.sp[f['name']]
            X = np.array(sp['x_axis'], float); Y = np.array(sp['y_axis'], float); Z = np.cross(X, Y)
            F.type = 'ProfileFeature'
            F.sketch = DP.Sketch([list(X), list(Y), list(Z)], tuple(sp['origin_m']), 1.0)
            try: F.sketch.segs, F.n_dropped = seg_list(rb, f['name'])
            except Exception as ex: F.sketch.segs = []; F.err = repr(ex)
        F.faces = [xt_surface(x) for x in faces_of.get(f['id'], [])]
        F.created_faces = [xt_surface(x) for x in created.get(f['id'], [])]
        out.append(F); by.setdefault(F.name, F)
    return DP.Part(d.get('file', ''), out, by)


# ----------------------------------------------------------------------------- replay
class OracleReplay(FD.Rebuild):
    def __init__(self, part_name, ref, lookahead=None, lookahead_m=None):
        self.pname = part_name
        self.lookahead = lookahead or {}     # cut feature name -> voxel mask it removes (from an earlier pass)
        self.cutvox = {}                      # this pass: cut name -> voxels removed / speculative removal
        with contextlib.redirect_stdout(io.StringIO()):
            self.g = DO.GRebuild()
        self.part = to_part(self.g)
        self.fs_endspecs()
        self.ref = ref; self.body = None
        self.bin = np.zeros(int(np.prod(ref.G.n)), bool)
        self.tools = {}; self.choice = {}; self.order = []
        # round 17 exact track (mesh booleans against the closed oracle mesh)
        self.exact = bool(getattr(ref, 'exact', False))
        self.lookahead_m = lookahead_m or {}  # cut name -> manifold of material it removes (earlier pass)
        self.cutman = {}                      # this pass: cut name -> manifold removed / speculative
        self.MB = None; self.MT = ref.M if self.exact else None; self.VB = 0.0; self.I = 0.0
        self.VT = self.MT.volume() if self.exact else 0.0

    def fs_endspecs(self):
        """round 17: the round-13 EndSpec reader (fstream.parse_endspec: end codes, both, reverse,
        D1/D2 by DimValue name; 100 % on A/B and on RV01/RV12/RV17/RV23) replaces the older
        mo_classes end specs the decoded json carries (RV23: end1 None on 14 of 31 extrusions)."""
        self.es = {}
        if os.environ.get('R17_FSES', '1') != '1': return
        try:
            from sldprt import validate as V, fstream as FS
            d = V.feature_stream(os.path.join(ROOT, SRC, self.pname + '.SLDPRT'))
            ids = {f['id']: f['name'] for f in self.g.d['features'] if 'Extrude' in f['name'] or f['type'] in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion')}
            dec = FS.decode(d, set(ids))
        except Exception:
            return
        for fid, es in dec.endspecs.items():
            n = ids.get(fid)
            if n is None: continue
            self.es[n] = es
            e = self.g.ec.setdefault(n, {})
            e['end_code_dir1'] = es.end1
            e['end_code_dir2'] = es.end2 if es.both else None
            e['both'] = bool(es.both); e['reverse'] = bool(es.reverse)
            D = [x * MM for x in (es.depth1, es.depth2) if x]
            if es.depth1: e['D_mm'] = [es.depth1 * MM] + ([es.depth2 * MM] if es.depth2 else [])
            elif es.depth2 and not es.both: e['D_mm'] = [es.depth2 * MM]
            e['fs_endspec'] = True

    # ---- round 17 exact track
    @staticmethod
    def mf(shape, tol=0.002):
        """closed manifold of a B-rep (finer tessellations first; a tessellation can leave cracks
        between faces, a coarser or a ShapeFix'ed one often closes)."""
        import exact_iou as XI
        for t in (tol, 0.01, 0.05):
            try:
                T = XI.mesh_of(shape, t)
                M = XI.as_manifold(T) if len(T) else None
                if M is not None: return M
            except Exception:
                pass
        try:
            from OCP.ShapeFix import ShapeFix_Shape
            from build123d import Shape as _S
            sf = ShapeFix_Shape(shape.wrapped); sf.Perform(); fx = _S.cast(sf.Shape())
            T = XI.mesh_of(fx, 0.01)
            return XI.as_manifold(T) if len(T) else None
        except Exception:
            return None

    def obox(self):
        import manifold3d as M3
        if getattr(self, '_obox', None) is None:
            lo = self.ref.T.reshape(-1, 3).min(0) - 1.0; hi = self.ref.T.reshape(-1, 3).max(0) + 1.0
            self._obox = M3.Manifold.cube(tuple(map(float, hi - lo))).translate(tuple(map(float, lo)))
        return self._obox

    def set_target(self, MT):
        self.MT = MT; self.VT = MT.volume(); self.I = (self.MB ^ MT).volume() if self.MB is not None else 0.0

    def escore(self, I=None, VB=None):
        I = self.I if I is None else I; VB = self.VB if VB is None else VB
        return I / max(VB + self.VT - I, 1e-12)

    def ecell(self, kind, P):
        """exact (volume changed, of it inside the target) of applying tool manifold P."""
        if kind == 'boss':
            D = P if self.MB is None else P - self.MB
        else:
            if self.MB is None: return 0.0, 0.0
            D = P ^ self.MB
        v = D.volume()
        return v, ((D ^ self.MT).volume() if v > 0 else 0.0)

    def etool_score(self, kind, P):
        v, vin = self.ecell(kind, P)
        return self.escore(self.I + vin, self.VB + v) if kind == 'boss' else self.escore(self.I - vin, self.VB - v)

    def ebody_score(self, body):
        M = self.mf(body)
        if M is None: return None
        i = (M ^ self.MT).volume(); return i / max(M.volume() + self.VT - i, 1e-12)

    def cur_score(self):
        return self.escore() if self.exact else self.score(self.bin)

    def surf_support(self, kind, T, n=240, tol=0.03):
        """round 17 point-to-surface oracle (for parts whose oracle mesh is not closed: xt_faces):
        sample points on the tool surface that become faces of the new body (inside the current
        body for a cut, outside it for a boss) and return the fraction lying within tol mm of the
        oracle surface mesh.  Resolution-free: a 0.2 mm knurl groove or thread flank registers."""
        import trimesh
        from OCP.BRepClass3d import BRepClass3d_SolidClassifier
        from OCP.gp import gp_Pnt
        from OCP.TopAbs import TopAbs_IN, TopAbs_OUT
        import exact_iou as XI
        if getattr(self, '_otm', None) is None: self._otm = XI._tm(self.ref.T)
        try: Tm = XI._tm(XI.mesh_of(T, 0.005))
        except Exception: return None
        if not len(Tm.faces) or self.body is None and kind == 'cut': return None
        P, _ = trimesh.sample.sample_surface(Tm, n * 3, seed=3)
        keep = []
        for p in P:
            if self.body is None: keep.append(p); continue
            st = BRepClass3d_SolidClassifier(self.body.wrapped, gp_Pnt(*map(float, p)), 1e-6).State()
            if (kind == 'cut' and st == TopAbs_IN) or (kind == 'boss' and st == TopAbs_OUT): keep.append(p)
            if len(keep) >= n: break
        if len(keep) < 8: return None
        d = np.abs(trimesh.proximity.closest_point(self._otm, np.array(keep))[1])
        return float((d <= tol).mean())

    def tool_score(self, kind, T):
        """oracle score after applying tool solid T (exact when possible, else voxel)."""
        if self.exact:
            P = self.mf(T)
            if P is not None: return self.etool_score(kind, P), None
        inT = self.ref.pts_in(T); nb = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
        return self.score(nb), nb

    def resync(self, kind=None, P=None):
        """exact track follows the B-rep body; if the body does not mesh to a closed manifold the
        manifold result of the same boolean is used."""
        if not self.exact: return
        M = self.mf(self.body) if self.body is not None else None
        if M is None and P is not None:
            M = (P if self.MB is None else self.MB + P) if kind == 'boss' else (self.MB - P if self.MB is not None else None)
        if M is None and self.body is not None:
            # the body cannot be scored exactly any more: the rest of this part runs on the voxel track
            self.exact = False; self.ref.rin = self.ref.rin
            FD.log('exact-track', 'WARN', 'body does not mesh to a closed manifold: voxel oracle from here on')
            return
        self.MB = M
        self.VB = M.volume() if M is not None else 0.0
        self.I = (M ^ self.MT).volume() if M is not None else 0.0

    # ---- helpers
    def score(self, B, extra=0.0):
        """oracle IoU; material outside the oracle grid (beyond the final-body box + 1 mm) is
        counted as extra (otherwise a through-all boss would be free)."""
        Rf = self.ref; i = (B & Rf.rin).sum(); u = (B | Rf.rin).sum()
        return i / max(u + getattr(self, 'out_acc', 0.0) + extra, 1)

    def out_vox(self, c, n, ivs):
        """voxel-equivalent volume of a cell prism outside the oracle grid (along n)."""
        G = self.ref.G; hi_ = G.lo + G.n * G.d
        P = np.array([[x, y, z] for x in (G.lo[0], hi_[0]) for y in (G.lo[1], hi_[1]) for z in (G.lo[2], hi_[2])])
        p = np.array(tuple(c.center())); t = (P - p) @ np.array(n); gmin, gmax = t.min(), t.max()
        L = sum(max(0.0, hi - max(lo, gmax)) + max(0.0, min(hi, gmin) - lo) for lo, hi in ivs)
        return c.area * L / G.dv

    def sketch_feat(self, F):
        g = self.g; f = F.decoded
        e = g.ec.get(F.name) or {}
        name = e.get('sketch') if e.get('sketch') in self.part.by_name else None
        if name is None:
            with contextlib.redirect_stdout(io.StringIO()): name = g.link(F.name)
        elif name not in g.used: g.used.add(name)
        sf = self.part.by_name.get(name) if name else None
        return sf if sf is not None and sf.sketch is not None and sf.sketch.segs else None

    def columns(self, cell, n, ivs, solid_cls, body_cls, kind):
        """grid version of FD.columns: fraction of sample columns through the cell holding oracle
        material that the body does not have yet."""
        V, T = cell.tessellate(0.05)
        V = np.array([tuple(v) for v in V]); T = np.array(T)
        if not len(T): return 0.0
        ar = 0.5 * np.linalg.norm(np.cross(V[T[:, 1]] - V[T[:, 0]], V[T[:, 2]] - V[T[:, 0]]), axis=1)
        if ar.sum() <= 0: return 0.0
        rng = np.random.default_rng(1)
        idx = rng.choice(len(T), min(16, 3 * len(T)), p=ar / ar.sum())
        u = rng.random(len(idx)); w = rng.random(len(idx)); mk = u + w > 1; u[mk] = 1 - u[mk]; w[mk] = 1 - w[mk]
        P = V[T[idx, 0]] + u[:, None] * (V[T[idx, 1]] - V[T[idx, 0]]) + w[:, None] * (V[T[idx, 2]] - V[T[idx, 0]])
        good = 0
        for p in P:
            hit = False
            for lo, hi in ivs:
                lo2, hi2 = max(lo, -60), min(hi, 60)
                zs = np.arange(lo2 + 0.05, hi2, 0.1)
                if not len(zs): continue
                k = self.ref.at(p + np.outer(zs, n)); k = k[k >= 0]
                if len(k) and np.any(self.ref.rin[k] & ~self.bin[k]): hit = True; break
            good += hit
        return good / len(P)

    def select_cells(self, cells, n, ivs, kind, name, faces=()):
        keep, info = [], []
        Rf = self.ref
        for c in cells:
            P = FD.solid_of([s for lo, hi in ivs for s in self.prism([c], n, lo, hi)])
            try: inP = Rf.pts_in(P)
            except Exception: info.append('x'); continue
            if kind == 'boss':
                new = inP & ~self.bin
                if new.sum() < 3: info.append('0'); continue
                vf = (new & Rf.rin).sum() / new.sum()
                fr = self.columns(c, np.array(n), ivs, None, None, kind) if vf <= 0.5 else 1.0
                ok = vf > 0.5 or (fr > 0.75 and vf > 0.2)
                info.append(f'{vf:.2f}/{fr:.2f}')
            else:
                rem = inP & self.bin
                if rem.sum() < 3: info.append('0'); continue
                fr = 1 - (rem & Rf.rin).sum() / rem.sum()
                ok = fr > 0.5; info.append(f'{fr:.2f}')
            if ok: keep.append(c)
        return keep, info

    def intervals(self, F, kind, origin, n, D, code, code2, D2):
        """candidate (lo, hi) lists along n for one direction sign."""
        caps = []
        for S in F.faces:
            if S.kind == 'plane' and abs(abs(np.dot(S.params['n'], n)) - 1) < 1e-6:
                caps.append(float(np.dot(np.array(S.params['o']) * MM - origin, n)))
            if S.kind != 'plane' and S.box is not None:
                b = np.array(S.box[:6]) * MM
                pr = [float(np.dot(np.array([b[i], b[1 + j], b[2 + k]]) - origin, n)) for i in (0, 3) for j in (0, 3) for k in (0, 3)]
                caps += [max(pr), min(pr)]
        offs = self.plane_offsets(origin, n)
        fw = sorted({round(c, 4) for c in caps + offs if c > 1e-4})
        c1 = []
        if D: c1.append((0, D))
        if D:   # sketch plane offset not decoded reliably: blind D anchored on the feature's own cap planes
            for c in sorted({round(c, 4) for c in caps}):
                if abs(c) > 1e-4: c1 += [(c - D, c), (c, c + D)]
        if code in (None, 0, 6) and D: c1.append((-D / 2, D / 2))
        if code in (None, 0) and D and self.two_dir(F) is not False: c1.append((-D, D))
        if code in (None, 1) or (kind == 'cut' and code is None): c1.append((0, BIG))
        if code == 9: c1.append((-BIG, BIG))
        if code in (None, 2, 3, 4, 5, 7) or (code == 1 and kind != 'cut'):   # r17: a through-all boss is bounded by the body; offer the up-to caps too (Top Panel Boss-Extrude2)
            c1 += [(0, s) for s in fw[:12]]
            if code == 5 and D: c1 += [(0, s + k * D) for s in offs for k in (1, -1) if s + k * D > 1e-4]
        if not c1 and D is None: c1 = [(0, s) for s in fw[:12]] + [(0, BIG)]
        c1 = list(dict.fromkeys((round(a, 4), round(b, 4)) for a, b in c1))
        c2 = [None]
        if code2 is not None and code not in (6, 9):
            c2 = [None] + ([(-D2, 0)] if D2 else []) + ([(-BIG, 0)] if code2 in (1, 9) else [])
        return [[iv1] + ([iv2] if iv2 else []) for iv1 in c1 for iv2 in c2]

    def sketch_text(self, name):
        """round 17: a sketch text entity (SEG type 4): moDimText_c CString text, then
        utCharFormat_c CString font name and f64 height (Top Panel Sketch6: 'S V R N ', Gill Sans
        Ultra Bold, 6 mm).  Returns (text, font, height_mm) or None."""
        sk = self.g.sk.get(name) or {}
        if not any(e.get('type', '').startswith('unknown_kind') for e in sk.get('entities', [])): return None
        try:
            from sldprt import validate as V
            if getattr(self, '_fsd', None) is None: self._fsd = V.feature_stream(os.path.join(ROOT, SRC, self.pname + '.SLDPRT'))
            d = self._fsd; o = sk.get('stream_offset') or 0
            i = d.find(b'moDimText_c', o, o + 20000)
            if i < 0: return None
            import struct
            def cstr(j):
                k = d.find(b'\xff\xfe\xff', j, j + 64)
                if k < 0: return None, j
                n = d[k + 3]; return d[k + 4:k + 4 + 2 * n].decode('utf-16-le', 'replace'), k + 4 + 2 * n
            t, j = cstr(i)
            jf = d.find(b'CharFormat_c', j, j + 400)
            f, j2 = cstr(jf) if jf >= 0 else (None, j)
            h = struct.unpack_from('<d', d, j2)[0] * MM if j2 + 8 <= len(d) else 0.0
            return (t, f, h) if t else None
        except Exception:
            return None

    # ---- round 17 face oracle: decoded XT faces (final body, from this file) vs body faces
    def xt_fa(self):
        """the decoded final-body XT faces as face_audit records (mm), boxes from the loop curves."""
        if getattr(self, '_xtfa', None) is not None: return self._xtfa
        import face_audit as FA, xt_mesh as XM
        XM.orient_arcs(self.g.d)
        out = []
        for f in self.g.faces:
            S = xt_surface(f)
            if S.kind not in ('plane', 'cyl', 'cone', 'torus', 'sphere'): continue
            P = []
            for l in f.get('loops', []):
                for e, a, b in XM.loop_ends(l):
                    if a is None or b is None: continue
                    P += XM.curve_pts(e, a, b, 24)
            if not P: continue
            P = np.array(P) * MM; S.box = list(P.min(0) / MM) + list(P.max(0) / MM); S.area = 0.0
            try: out.append(FA._dump_face(S, 'xt'))
            except Exception: continue
        self._xtfa = out
        return out

    def face_matches(self, body):
        """number of decoded XT face patches the body reproduces exactly (same surface, bbox within
        0.05 mm): the strict face gate, decode-only (dumps are never read here)."""
        import face_audit as FA
        X = self.xt_fa()
        if not X or body is None: return 0
        try: r = FA.audit(X, FA.faces_from_shape(body))
        except Exception: return 0
        c = r['counts']; return c.get('matched', 0) + c.get('area', 0)

    def two_dir(self, F):
        """decoded 'two directions' flag of an extrusion (round 13 EndSpec S+4 rule), None if unknown."""
        if F.name in getattr(self, 'es', {}): return bool(self.es[F.name].both)
        fp = (self.g.d.get('feature_params') or {}).get(str(F.id)) or {}
        es = (self.g.d.get('end_specs') or {}).get(F.name) or []
        if 'two_directions' in fp: return bool(fp['two_directions'])
        if es: return any(x.get('dir2') for x in es)
        return None

    def xt_points(self):
        if getattr(self, '_xtp', None) is None:
            import mirror_derived as MD
            from scipy.spatial import cKDTree
            P = MD.xt_vertices(self.pname); self._xtp = cKDTree(P)
            self._xtplanes = [(np.array(x['params']['normal'], float), np.array(x['params']['point']) * MM)
                              for x in self.g.faces if x['surface_type'] == 'plane' and 'normal' in (x.get('params') or {})]
        return self._xtp

    def body_planes(self):
        """round 17: planar faces of the body built so far (a sketch is usually drawn on a face of an
        earlier feature that later cuts remove from the final body: RV17 Sketch2 on z=17)."""
        if self.body is None or os.environ.get('R17_BODYPLANES', '1') != '1': return []
        key = id(self.body)
        if getattr(self, '_bp_key', None) == key: return self._bp
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Plane
        out, V = [], []
        for fc in self.body.faces():
            ad = BRepAdaptor_Surface(fc.wrapped)
            if ad.GetType() != GeomAbs_Plane: continue
            ax = ad.Plane().Axis(); d_ = ax.Direction(); p = ax.Location()
            out.append((np.array([d_.X(), d_.Y(), d_.Z()]), np.array([p.X(), p.Y(), p.Z()])))
        try: V = [tuple(v) for v in self.body.vertices()]
        except Exception: V = []
        from scipy.spatial import cKDTree
        self._bp_key, self._bp = key, out
        self._bvt = cKDTree(np.array(V)) if len(V) else None
        return out

    def reg_score(self, sk, rot, tr):
        """fraction of sketch points (segment ends, arc centres) that land on a final XT vertex or
        circle centre when the sketch is placed with (rot, tr): a decode-only check of the frame."""
        tree = self.xt_points()
        pts = []
        for sg in sk.segs:
            if sg.construction: continue
            if sg.type == 1 and sg.c is not None: pts.append(sg.c)
            if sg.p0 is not None and not (sg.type == 1 and sg.is_circle): pts += [sg.p0, sg.p1]
        if not pts: return 0.0
        Rm = np.array(rot, float); Q = (np.array(tr) + np.array(pts)[:, :2] @ Rm[:2]) * MM
        d, _ = tree.query(Q)
        hit = d < 2e-3
        self.body_planes()
        if getattr(self, '_bvt', None) is not None and self.body is not None:
            d2, _ = self._bvt.query(Q); hit |= d2 < 2e-3
        return float(np.mean(hit))

    def frames(self, skf):
        """sketch frame candidates.  Sketch-plane decoding is wrong or incomplete for some sketches
        (RV19 Sketch1: decoded Right Plane; RV23: plane offsets 3 / 7.5 / 17 mm not decoded; sketches
        on back faces with a reversed frame).  Candidates: the decoded frame; the three default
        planes and their reversed versions, each at every offset where a final XT plane parallel to
        it lies.  They are ranked by reg_score (sketch points on XT vertices); the decoded frame
        is always tried first, then the best-registered alternatives."""
        if getattr(skf, '_frames', None) is not None: return skf._frames
        sk = skf.sketch; self.xt_points()
        rot0, tr0 = sk.rot, sk.trans
        base = [(sk.rot, 'decoded')]
        for nm, X, Y in (('front', (1, 0, 0), (0, 1, 0)), ('top', (1, 0, 0), (0, 0, -1)), ('right', (0, 0, -1), (0, 1, 0))):
            for sx, sy, tag in ((1, 1, ''), (-1, 1, '-revx'), (1, -1, '-revy'), (-1, -1, '-rot180')):
                X2 = np.array(X) * sx; Y2 = np.array(Y) * sy; Z2 = np.cross(X2, Y2)
                base.append(([list(X2), list(Y2), list(Z2)], nm + tag))
        cand = [(rot0, tr0, 'decoded')]
        for rot, nm in base:
            Z = np.array(rot[2], float)
            offs = {0.0, round(float(np.dot(tr0, Z)) * MM, 4)}
            for n, o in self._xtplanes + self.body_planes():
                if abs(abs(n @ Z) - 1) < 1e-6: offs.add(round(float(o @ Z), 4))
            for off in offs:
                tr = tuple(Z * off / MM)
                if nm == 'decoded' and abs(off - float(np.dot(tr0, Z)) * MM) < 1e-6: tr = tr0
                cand.append((rot, tr, f'{nm}@{off:g}' if not (nm == 'decoded' and tr is tr0) else 'decoded'))
        # round 17: a decoded reference plane created just before the sketch (FS1 Plane2 -> Sketch7)
        # is a frame candidate, at its decoded offset and at +-its offset dimension
        pref = []
        fid = next((f['id'] for f in self.g.d['features'] if f['name'] == skf.name), None)
        rps = {r['name']: r for r in self.g.d.get('ref_planes') or []}
        prevf = [f for f in self.g.d['features'] if fid is not None and f['id'] < fid and f['type'] not in ('Sketch',)]
        if prevf and prevf[-1]['name'] in rps and fid - prevf[-1]['id'] <= 2:
            rp = rps[prevf[-1]['name']]; T_ = rp.get('transform_rows_x_y_n_t') or []
            if len(T_) == 12:
                X_, Y_, N_ = np.array(T_[0:3], float), np.array(T_[3:6], float), np.array(T_[6:9], float)
                offs = {float(N_ @ np.array(T_[9:12])) * MM}
                for dn, dv in rp.get('dims') or []:
                    v = num(dv)
                    if v is not None: offs |= {v, -v}
                for sx, sy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                    X2 = X_ * sx; Y2 = Y_ * sy; Z2 = np.cross(X2, Y2)
                    for off in sorted(offs):
                        c = ([list(X2), list(Y2), list(Z2)], tuple(Z2 * (off * (1 if Z2 @ N_ > 0 else -1)) / MM), f'{rp["name"]}{"" if sx > 0 else "-x"}{"" if sy > 0 else "-y"}@{off:g}')
                        cand.append(c); pref.append(c[2])
        uniq = []
        for c in cand:
            if not any(np.allclose(np.array(c[0]), np.array(u[0])) and np.allclose(c[1], u[1], atol=1e-9) for u in uniq): uniq.append(c)
        sc = [self.reg_score(sk, r, t) for r, t, _ in uniq]
        dec = 0
        order = [dec] + [i for i in sorted(range(len(uniq)), key=lambda i: -sc[i]) if i != dec and sc[i] >= max(0.2, sc[dec] - 1e-9)][:4]
        rp_i = [i for i, u in enumerate(uniq) if u[2] in pref and i not in order]
        rp_i.sort(key=lambda i: -sc[i])
        order = order[:1] + rp_i[:4] + order[1:]
        if len(order) == 1 + len(rp_i[:4]):   # nothing registers (revolve profiles: XT vertices only on the axis): try the plain default planes
            order += [i for i, u in enumerate(uniq) if i != dec and u[2].endswith('@0') and '-' not in u[2]]
        skf._frames = [uniq[i][:2] + (f'{uniq[i][2]} reg={sc[i]:.2f}',) for i in order]
        return skf._frames

    def quality(self, kind, inT):
        if kind == 'boss':
            new = inT & ~self.bin; return (new & self.ref.rin).sum() / max(1, new.sum())
        rem = inT & self.bin; return (rem & ~self.ref.rin).sum() / max(1, rem.sum())

    def cell_gain(self, kind, idx):
        """net oracle gain (voxels) of adding / removing the voxels idx."""
        rin = self.ref.rin[idx]; bin_ = self.bin[idx]
        if kind == 'boss': return int((rin & ~bin_).sum()) - int((~rin & ~bin_).sum())
        return int((bin_ & ~rin).sum()) - int((bin_ & rin).sum())

    def extrude_feature(self, F):
        skf = self.sketch_feat(F)
        if skf is None: FD.log(F.name, 'SKIP', 'no sketch'); return
        kind = 'cut' if 'cut' in F.name.lower() or 'Cut' in F.type else 'boss'
        e = self.g.ec.get(F.name) or {}
        D = (e.get('D_mm') or [None])[0] or next((v * MM for k, v in F.dims.items() if k.startswith('D1@')), None)
        D2 = (e.get('D_mm') or [None, None])[1] if len(e.get('D_mm') or []) > 1 else None
        code = e.get('end_code_dir1'); code2 = e.get('end_code_dir2')
        if code not in (0, 1, 2, 3, 4, 5, 6, 7, 9): code = None      # undecoded / unknown end-spec codes
        if code2 not in (0, 1, 2, 3, 4, 5, 6, 7, 9): code2 = None
        sk = skf.sketch; rot0, tr0 = sk.rot, sk.trans
        s0 = self.cur_score(); self._ecands = []
        best = None; ncand = 0; frames = self.frames(skf)
        for fi, (rot, tr, fname) in enumerate(frames):
            if fi == 1 and best is not None and best[0] > s0 + 1e-6 and best[5] >= 0.9: break
            sk.rot, sk.trans = rot, tr
            cells = FD.sketch_cells(skf)
            if not cells: continue
            origin = np.array(sk.trans) * MM; n0 = np.array(sk.normal, float)
            percell = [None] * len(cells)     # best (gain, n, ivs, idx) per cell over all candidates
            spec = [None] * len(cells)        # look-ahead: smallest prism per cell that lies outside the final body
            if self.exact:
                best, ncand = self._extrude_exact(F, kind, cells, n0, origin, D, code, code2, D2, fname, rot, tr, best, ncand, spec)
                if kind == 'cut' and fi == 0 and any(x is not None for x in spec):
                    import manifold3d as M3
                    # clipped to the oracle box + 1 mm (a through-all prism is 600 mm long; the voxel
                    # version was clipped by its grid)
                    self.cutman.setdefault(F.name + '#spec', M3.Manifold.batch_boolean([x for x in spec if x is not None], M3.OpType.Add) ^ self.obox())
                continue
            for sg in ((1,) if code in (6, 9) else (1, -1)):
                n = n0 * sg
                for ivs in self.intervals(F, kind, origin, n, D, code, code2, D2):
                    ncand += 1
                    keep, U, OV = [], [], []
                    for ci, c in enumerate(cells):
                        try: idx = np.flatnonzero(self.ref.pts_in(FD.solid_of([x for lo, hi in ivs for x in self.prism([c], n, lo, hi)])))
                        except Exception: continue
                        ov = self.out_vox(c, n, ivs) if kind == 'boss' else 0.0
                        g = self.cell_gain(kind, idx) - ov
                        if percell[ci] is None or g > percell[ci][0]: percell[ci] = (g, n, ivs, idx, ov)
                        if kind == 'cut' and len(idx) >= 3 and self.ref.rin[idx].mean() < 0.1 and (spec[ci] is None or len(idx) < len(spec[ci])):
                            spec[ci] = idx
                        rin = self.ref.rin[idx]; bin_ = self.bin[idx]
                        if kind == 'boss':
                            new = ~bin_
                            ok = new.sum() >= 3 and (rin & new).sum() / new.sum() > 0.5
                            # material removed later (cuts) is not in the final-body oracle: accept a cell
                            # when most sample columns through it still hold oracle material (as FD does)
                            if not ok and new.sum() >= 3 and (rin & new).any():
                                ok = self.columns(c, np.array(n), ivs, None, None, kind) > 0.75
                        else:
                            ok = bin_.sum() >= 3 and (bin_ & ~rin).sum() / bin_.sum() > 0.5
                        if ok: keep.append(ci); U.append(idx); OV.append(ov)
                    if not keep: continue
                    nb = self.bin.copy(); I = np.concatenate(U); nb[I] = kind == 'boss'
                    sc = self.score(nb, sum(OV))
                    if best is None or sc > best[0] + 1e-9:
                        best = (sc, fname, [(cells[ci], n, ivs) for ci in keep], nb, len(cells), self.quality(kind, nb if kind == 'boss' else ~nb & self.bin), 'uniform', (rot, tr), sum(OV))
            # mixed candidate: every cell with a positive net gain, each with its own direction / extent
            mix = [(cells[ci], p[1], p[2], p[3], p[4]) for ci, p in enumerate(percell) if p is not None and p[0] > 0]
            if mix:
                nb = self.bin.copy(); I = np.concatenate([m[3] for m in mix]); nb[I] = kind == 'boss'
                ov = sum(m[4] for m in mix); sc = self.score(nb, ov)
                if best is None or sc > best[0] + 1e-9:
                    best = (sc, fname, [(m[0], m[1], m[2]) for m in mix], nb, len(cells), self.quality(kind, nb if kind == 'boss' else ~nb & self.bin), 'per-cell', (rot, tr), ov)
            if not self.exact and kind == 'cut' and fi == 0 and any(x is not None for x in spec):
                m = np.zeros_like(self.bin); m[np.concatenate([x for x in spec if x is not None])] = True
                self.cutvox.setdefault(F.name + '#spec', m)
        sk.rot, sk.trans = rot0, tr0
        if best is None:
            txt = self.sketch_text(skf.name)
            if txt:
                FD.log(F.name, 'SKIP', f'sketch text {txt[0]!r} (font {txt[1]!r}, height {txt[2]:g} mm): glyph outlines are not stored in the file', sketch=skf.name); return
            FD.log(F.name, 'FAIL', 'no cells selected', sketch=skf.name, cand=ncand); return
        fm = None
        if self.exact and os.environ.get('R17_FACES', '1') == '1':
            best, fm = self.face_rerank(kind, best)
        sc, fname, sel, nb, nc, q, how, fr, ov = best
        sk.rot, sk.trans = fr
        sols = [x for c, n, ivs in sel for lo, hi in ivs for x in self.prism([c], n, lo, hi)]
        T = sols[0] if len(sols) == 1 else sols[0].fuse(*sols[1:]).clean()
        if self.commit(F.name, kind, T, None, ov) is False:
            sk.rot, sk.trans = rot0, tr0
            FD.log(F.name, 'FAIL', 'B-rep boolean failed', sketch=skf.name); return
        ivs_s = sorted({(round(lo, 3), round(hi, 3), tuple(np.round(n, 3))) for c, n, ivs in sel for lo, hi in ivs})
        self.choice[F.name] = dict(kind=kind, sketch=skf.name, frame=fname, how=how, cells=f'{len(sel)}/{nc}', ivs=[list(x) for x in ivs_s], code=code, D=D)
        FD.log(F.name, 'OK', kind, sketch=skf.name, frame=fname, how=how, code=code, D=D, cells=f'{len(sel)}/{nc}', ivs=str(ivs_s[:4]),
               cand=ncand, iou=round(float(self.cur_score()), 4), faces=fm)

    def _extrude_exact(self, F, kind, cells, n0, origin, D, code, code2, D2, fname, rot, tr, best, ncand, spec):
        """round 17: the extrude candidate search of extrude_feature scored with exact mesh booleans."""
        import manifold3d as M3
        percell = [None] * len(cells)
        eps = 1e-4
        for sg in ((1,) if code in (6, 9) else (1, -1)):
            n = n0 * sg
            for ivs in self.intervals(F, kind, origin, n, D, code, code2, D2):
                ncand += 1
                keep, U, VV = [], [], []
                for ci, c in enumerate(cells):
                    try:
                        T = FD.solid_of([x for lo, hi in ivs for x in self.prism([c], n, lo, hi)])
                        P = self.mf(T)
                    except Exception: P = None
                    if P is None: continue
                    v, vin = self.ecell(kind, P)
                    g = (2 * vin - v) if kind == 'boss' else (v - 2 * vin)
                    if percell[ci] is None or g > percell[ci][0]: percell[ci] = (g, n, ivs, P, v, vin)
                    if kind == 'cut' and P.volume() > eps:
                        fin = (P ^ self.ref.M).volume() / P.volume()
                        if fin < 0.1 and (spec[ci] is None or P.volume() < spec[ci].volume()): spec[ci] = P
                    if kind == 'boss':
                        ok = v > eps and vin / v > 0.5
                        if not ok and v > eps and vin > 0:
                            ok = self.columns(c, np.array(n), ivs, None, None, kind) > 0.75
                    else:
                        ok = v > eps and (v - vin) / v > 0.5
                    if ok: keep.append(ci); U.append(P)
                if not keep: continue
                UU = U[0] if len(U) == 1 else M3.Manifold.batch_boolean(U, M3.OpType.Add)
                sc = self.etool_score(kind, UU)
                self._ecands.append((sc, fname, [(cells[ci], n, ivs) for ci in keep], None, len(cells), None, 'uniform', (rot, tr), 0.0))
                if best is None or sc > best[0] + 1e-9:
                    q = self.ecell(kind, UU); q = (q[1] / max(q[0], 1e-12)) if kind == 'boss' else (1 - q[1] / max(q[0], 1e-12))
                    best = (sc, fname, [(cells[ci], n, ivs) for ci in keep], None, len(cells), q, 'uniform', (rot, tr), 0.0)
        mix = [(cells[ci], p[1], p[2], p[3]) for ci, p in enumerate(percell) if p is not None and p[0] > 0]
        if mix:
            UU = mix[0][3] if len(mix) == 1 else M3.Manifold.batch_boolean([m[3] for m in mix], M3.OpType.Add)
            sc = self.etool_score(kind, UU)
            self._ecands.append((sc, fname, [(m[0], m[1], m[2]) for m in mix], None, len(cells), None, 'per-cell', (rot, tr), 0.0))
            if best is None or sc > best[0] + 1e-9:
                q = self.ecell(kind, UU); q = (q[1] / max(q[0], 1e-12)) if kind == 'boss' else (1 - q[1] / max(q[0], 1e-12))
                best = (sc, fname, [(m[0], m[1], m[2]) for m in mix], None, len(cells), q, 'per-cell', (rot, tr), 0.0)
        return best, ncand

    def face_rerank(self, kind, best, tol=2e-3, k=5):
        """round 17: among extrude candidates whose exact oracle IoU is within tol of the best, keep
        the one whose body reproduces the most decoded XT face patches (face gate as the primary
        criterion; volume IoU cannot tell a 0.05 mm extent error or a wrong cap plane)."""
        C = sorted(self._ecands, key=lambda c: -c[0])
        C = [best] + [c for c in C if c[0] >= best[0] - tol and not (abs(c[0] - best[0]) < 1e-12 and c[1] == best[1] and c[6] == best[6])][:k - 1]
        if len(C) < 2: return best, None
        res = []
        for c in C:
            sc, fname, sel, nb, nc, q, how, fr, ov = c
            sk = None
            try:
                sols = [x for cc, n, ivs in sel for lo, hi in ivs for x in self.prism([cc], n, lo, hi)]
                T = sols[0] if len(sols) == 1 else sols[0].fuse(*sols[1:]).clean()
                B = FD.bop(self.body, T, 'fuse' if kind == 'boss' else 'cut')
                m = self.face_matches(B)
            except Exception:
                m = -1
            res.append((m, sc, c))
        m0 = res[0][0]
        m, sc, c = max(res, key=lambda r: (r[0], r[1]))
        if c is not best and m > m0:
            return (c[0], c[1], c[2], None, c[4], best[5], c[6] + '+faces', c[7], 0.0), f'{m} (best-IoU candidate {m0})'
        return best, m0

    def commit(self, name, kind, T, B=None, out=0.0):
        if self.exact: return self.commit_exact(name, kind, T)
        v0 = FD.vol(self.body)
        self.out_acc = getattr(self, 'out_acc', 0.0) + (out if kind == 'boss' else 0.0)
        nbody = FD.bop(self.body, T, 'fuse' if kind == 'boss' else 'cut')
        if B is None:
            inT = self.ref.pts_in(T); B = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
        # the voxel track must follow the B-rep: a boolean that silently fails (helical sweeps,
        # tangent tools) leaves the body unchanged while the tool voxels say otherwise
        dv_vox = (int(B.sum()) - int(self.bin.sum()) + (out if kind == 'boss' else 0.0)) * self.ref.dv
        dv_rep = FD.vol(nbody) - v0
        if nbody is None or abs(dv_rep - dv_vox) > 0.25 * abs(dv_vox) + 0.5:
            try: B = self.ref.G.inside(nbody) if nbody is not None else B
            except Exception: pass
            FD.log(name, 'WARN', f'B-rep volume change {dv_rep:.2f} vs tool voxels {dv_vox:.2f}: voxel track re-read from the body')
        if kind == 'cut': self.cutvox[name] = self.bin & ~B
        self.body = nbody
        self.bin = B; self.tools[name] = (kind, T); self.order.append(name)
        return True

    @staticmethod
    def fuzzy_bop(a, b, op, fz, glue=False, fix=False):
        from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Cut
        if fix:
            from OCP.ShapeFix import ShapeFix_Shape
            from build123d import Shape as _S
            sf = ShapeFix_Shape(a.wrapped); sf.Perform(); a = _S.cast(sf.Shape())
            sf = ShapeFix_Shape(b.wrapped); sf.Perform(); b = _S.cast(sf.Shape())
        k = (BRepAlgoAPI_Fuse if op == 'fuse' else BRepAlgoAPI_Cut)()
        k.SetFuzzyValue(fz); k.SetNonDestructive(True)
        if glue:
            from OCP.BOPAlgo import BOPAlgo_GlueShift
            k.SetGlue(BOPAlgo_GlueShift)
        r = a._bool_op((a,), (b,), k)
        if op == 'fuse':
            try: r = r.clean()
            except Exception: pass
        return r

    def commit_exact(self, name, kind, T):
        """round 17: the B-rep boolean is checked against the exact (manifold) prediction of the same
        boolean; a silently failing OCC boolean is retried fuzzy, else the feature is not applied."""
        P = self.mf(T)
        if P is None:
            dv_pred = None
        else:
            v, vin = self.ecell(kind, P); dv_pred = v if kind == 'boss' else -v
            atol = 0.02 + 0.002 * P.surface_area()
        v0 = FD.vol(self.body); op = 'fuse' if kind == 'boss' else 'cut'
        tries = [lambda: FD.bop(self.body, T, op)]
        if self.body is not None:
            tries += [lambda fz=fz: self.fuzzy_bop(self.body, T, op, fz) for fz in (1e-5, 1e-4, 1e-3)]
            tries += [lambda: self.fuzzy_bop(self.body, T, op, 1e-5, glue=True), lambda: self.fuzzy_bop(self.body, T, op, 1e-5, fix=True)]
            # the tool nudged by 1e-4 mm along each axis: coplanar / tangent coincidences that OCC
            # mis-classifies (RV12 Boss-Extrude11: the fuse returns body + tool unmerged)
            tries += [lambda v=v: FD.bop(self.body, T.moved(Location(v)), op) for v in ((1e-4, 0, 0), (0, 1e-4, 0), (0, 0, 1e-4), (0, 0, -1e-4))]
        nbody = None; seen = []
        for t_ in tries:
            try: nb = t_()
            except Exception: nb = None
            if nb is None: continue
            dv = FD.vol(nb) - v0; seen.append(round(dv, 3))
            if dv_pred is None or abs(dv - dv_pred) <= 0.02 * abs(dv_pred) + atol:
                nbody = nb; break
            nbody = nbody or False
        if not nbody:
            FD.log(name, 'WARN', f'B-rep {op} disagrees with the exact prediction (dv {dv_pred:.3f}, B-rep {seen}, body solids {len(self.body.solids()) if self.body is not None else 0}): not applied'); return False
        if kind == 'cut':
            if P is not None and self.MB is not None: self.cutman[name] = P ^ self.MB
        B0 = self.bin
        try: B = self.ref.G.inside(nbody)
        except Exception: B = B0
        if kind == 'cut': self.cutvox[name] = B0 & ~B
        self.body = nbody; self.bin = B; self.tools[name] = (kind, T); self.order.append(name)
        self.resync(kind, P)
        return True

    def try_tool(self, name, kind, T, tag):
        """apply tool T only if the oracle IoU improves."""
        try:
            s1, nb = self.tool_score(kind, T)
        except Exception:
            return False
        s0 = self.cur_score()
        sup = None
        if not self.exact and not s1 > s0 + 1e-5 and s1 >= s0 - 1e-3 and os.environ.get('R17_SURF', '1') == '1':
            try: sup = self.surf_support(kind, T)
            except Exception: sup = None
        if s1 > s0 + 1e-5 or (sup is not None and sup >= 0.8):
            if self.commit(name, kind, T, nb) is False: return False
            FD.log(name, 'OK', tag, iou=round(float(self.cur_score()), 4)); return True
        return False

    def revolve_feature(self, F):
        skf = self.sketch_feat(F)
        if skf is None: FD.log(F.name, 'SKIP', 'no sketch'); return
        kind = 'cut' if 'cut' in F.name.lower() or 'Cut' in F.type else 'boss'
        sk = skf.sketch; rot0, tr0 = sk.rot, sk.trans
        ang = next((math.degrees(v) for k, v in F.dims.items() if k.startswith('D1@') and v < 7), 360.0)
        if ang < 1e-3: ang = 360.0
        best = None
        for fi, (rot, tr, fname) in enumerate(self.frames(skf)):
            if fi == 1 and best is not None and best[4] >= 0.9: break
            sk.rot, sk.trans = rot, tr
            cells = FD.sketch_cells(skf)
            axes = [s for s in sk.segs if s.construction] + [s for s in sk.segs if not s.construction and s.type == 0]
            for a in axes[:12]:
                p0 = np.array(sk.to_model(a.p0)) * MM; p1 = np.array(sk.to_model(a.p1)) * MM
                if np.linalg.norm(p1 - p0) < 1e-6: continue
                ax = Axis(tuple(p0), tuple(p1 - p0))
                for sgn in ((1,) if ang >= 359.99 else (1, -1)):
                    keep = []
                    for c in cells:
                        try: P = revolve(c, ax, sgn * ang)
                        except Exception: continue
                        if P is None or P.volume < 1e-6: continue
                        if self.exact:
                            M = self.mf(P)
                            if M is None: continue
                            v, vin = self.ecell(kind, M)
                            if v > 1e-4 and ((vin / v > 0.5) if kind == 'boss' else ((v - vin) / v > 0.5)): keep.append(P)
                            continue
                        try: inP = self.ref.pts_in(P)
                        except Exception: continue
                        if kind == 'boss':
                            new = inP & ~self.bin
                            if new.sum() >= 3 and (new & self.ref.rin).sum() / new.sum() > 0.5: keep.append(P)
                        else:
                            rem = inP & self.bin
                            if rem.sum() >= 3 and 1 - (rem & self.ref.rin).sum() / rem.sum() > 0.5: keep.append(P)
                    if not keep: continue
                    T = keep[0] if len(keep) == 1 else keep[0].fuse(*keep[1:]).clean()
                    if self.exact:
                        M = self.mf(T)
                        if M is None: continue
                        sc = self.etool_score(kind, M); v, vin = self.ecell(kind, M); nb = None
                        q = vin / max(v, 1e-12) if kind == 'boss' else 1 - vin / max(v, 1e-12)
                    else:
                        inT = self.ref.pts_in(T); nb = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
                        sc = self.score(nb); q = self.quality(kind, inT)
                    if os.environ.get("R17_DBG"): print("REVCAND", round(sc,5), round(float(q),4), fname, len(keep), len(cells), len(T.faces()) if hasattr(T,"faces") else None, file=sys.stderr, flush=True)
                    if best is None or sc > best[0]: best = (sc, T, nb, len(keep), q, fname, len(cells), (rot, tr))
        if best is None or best[0] <= self.cur_score() + 1e-6:
            sk.rot, sk.trans = rot0, tr0
            FD.log(F.name, 'FAIL', f'revolve {skf.name}: no axis/cell gives an IoU gain'); return
        sk.rot, sk.trans = best[7]
        if self.commit(F.name, kind, best[1], best[2]) is False:
            sk.rot, sk.trans = rot0, tr0; FD.log(F.name, 'FAIL', 'revolve: B-rep boolean failed'); return
        FD.log(F.name, 'OK', f'revolve {kind} {skf.name} {ang:g} deg', frame=best[5], cells=f'{best[3]}/{best[6]}', prec=round(float(best[4]), 3), iou=round(best[0], 4))

    def blend_feature(self, F, mirror=None):
        # FD.blend_feature reads FACE lines = faces the feature created
        cf = list(getattr(F, 'created_faces', None) or [])
        self._ftype = {f['id']: f['type'] for f in self.g.d['features']}
        # round 17: creator attribution is partial (fork 5 Fillet1: 1 of its 3 faces attributed), so
        # the faces whose geometry fits the blend size are always added (FD.blend_edges still requires
        # each edge to sit on such a face, and every edge is kept only if the oracle score improves)
        if not cf or os.environ.get('R17_BLENDFIT', '1') == '1':   # no creator attribution decoded (RV22): every XT face whose geometry fits the blend size
            have = {S.raw for S in cf}; attributed = bool(cf)   # r17 fix: decided before the loop appends
            bp = DP.blend_params(F); sz = (bp[1] or 0) if bp else 0
            for x in self.g.faces:
                S = xt_surface(x)
                if S.raw in have: continue
                ff = x.get('feature_first')
                if attributed and ff is not None and ff != F.id and self._ftype.get(ff) in ('Fillet', 'Chamfer'): continue   # another blend's face
                if attributed and F.type != 'Fillet': continue
                if F.type == 'Fillet' and ((S.kind == 'cyl' and abs(S.params['r'] - sz) < 1e-6) or
                                           (S.kind == 'torus' and abs(S.params['values'][7] - sz) < 1e-6)): cf.append(S)
                if F.type != 'Fillet' and (S.kind == 'cone' or (S.kind == 'plane' and max(abs(np.array(S.params['n']))) < 0.999)): cf.append(S)
        F.faces, keep = cf, F.faces
        body0 = self.body
        try:
            if F.type == 'Chamfer' and not F.chamfer: F.type = 'Chamfer'
            with self.exact_blend_scoring():
                n0 = len(LOG); super().blend_feature(F, mirror)
                self.small_blend(F, mirror, LOG[n0:])
        finally:
            F.faces = keep
            if self.exact and self.body is not body0:
                self.bin = self.ref.G.inside(self.body); self.resync()

    @contextlib.contextmanager
    def exact_blend_scoring(self):
        """round 17: FD.blend_feature scores a candidate body B as ref.miou(ref.G.inside(B)).  In exact
        mode ref.G.inside returns a token for B and ref.miou scores it with mesh booleans."""
        if not self.exact or os.environ.get('R17_EBLEND', '1') != '1':
            yield; return
        Rf = self.ref; G0 = Rf.G; me = self
        class _Tok:
            def __init__(s, B): s.B = B
        class _G:
            d = G0.d; dv = G0.dv; n = G0.n; lo = G0.lo
            def inside(s, B, *a, **k): return _Tok(B)
        def miou(x):
            if isinstance(x, _Tok):
                v = me.ebody_score(x.B)
                return v if v is not None else -1.0
            if x is me.bin:   # same tessellation path as the candidates (cached MB can differ by more than a small blend's gain: FS4 Chamfer1)
                if me.body is not None and id(me.body) != getattr(me, '_eb_key', None):
                    me._eb_key, me._eb_val = id(me.body), me.ebody_score(me.body)
                v = getattr(me, '_eb_val', None) if me.body is not None else None
                return v if v is not None else me.escore()
            return float((x & Rf.rin).sum() / max((x | Rf.rin).sum(), 1))
        bin0 = self.bin
        Rf.G = _G(); Rf.miou = miou
        try:
            yield
        finally:
            Rf.G = G0; del Rf.miou
            if not isinstance(self.bin, np.ndarray): self.bin = bin0

    def small_blend(self, F, mirror, new):
        """round 16: blends below the oracle voxel size cannot raise the voxel IoU, so the greedy
        IoU test rejects them (RV12 0.1/0.2 mm fillets).  Edges come from the decoded created faces;
        apply them in bulk (then one by one) when OCC succeeds and the IoU does not drop."""
        bp = DP.blend_params(F)
        if not bp or not bp[1] or self.body is None or mirror is not None: return
        kind, size = bp[0], bp[1] * MM
        if not self.exact and size > 2 * float(max(self.ref.G.d)): return
        st = [x for x in new if x.get('feature') == F.name]
        if not st or st[-1]['status'] == 'OK' or not str(st[-1].get('edges', '0/')).startswith('0/'): return
        try:
            self._ef = []; sel = self.blend_edges(F, kind, size, F.faces)
        except Exception: return
        if not sel: return
        op = (lambda b, es: FD._one(b).fillet(size, es)) if kind == 'fillet' else (lambda b, es: FD._one(b).chamfer(size, None, es))
        s0 = self.ref.miou(self.bin); v0 = FD.vol(self.body); cur, done = self.body, 0
        cand = [sel] + [[E] for E in sel]
        for es in cand:
            try:
                es2 = [min(cur.edges(), key=lambda x: (x.center() - E.center()).length) for E in es]
                if any((a.center() - E.center()).length > 1e-4 for a, E in zip(es2, es)): continue
                nb = op(cur, es2)
                if nb is None or not nb.is_valid or abs(FD.vol(nb) - v0) > 0.02 * v0 + 1: continue
                B = self.ref.G.inside(nb)
                if self.ref.miou(B) >= s0 - 2e-4:
                    cur, done = nb, done + len(es); self.bin = B
                    if self.exact: self.body = nb; self.resync(); s0 = self.escore()
                    if es is sel: break
            except Exception:
                continue
        if done:
            self.body = cur
            FD.log(F.name, 'OK' if done >= len(sel) else 'PART', f'{kind} {size:g} sub-voxel (applied, IoU-neutral)', edges=f'{min(done, len(sel))}/{len(sel)}',
                   iou=round(float(self.cur_score()), 4))

    def mirror_feature(self, F):
        """round 17: every candidate plane (decoded + 3 default planes) is scored by a dry run (sum of
        the gains of each earlier tool mirrored alone); the best plane is applied.  Seeds named by the
        decoder come first; blend seeds (fillets / chamfers) are re-applied mirrored with
        FD.blend_feature(seed, mirror=plane) on the edges of the mirrored faces."""
        m = self.g.pat.get(F.name) or {}
        planes = []
        if m.get('normal') is not None: planes.append((np.array(m['normal'], float), m['offset_mm']))
        for nn in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if not any(abs(abs(np.dot(p[0], nn)) - 1) < 1e-6 and abs(p[1]) < 1e-6 for p in planes): planes.append((np.array(nn, float), 0.0))
        # round 17: decoded reference planes (FS1 Mirror1 about Plane2, 1.5 mm off the Right plane)
        for rp in self.g.d.get('ref_planes') or []:
            T_ = rp.get('transform_rows_x_y_n_t') or []
            if len(T_) != 12: continue
            nn = np.array(T_[6:9], float)
            if np.linalg.norm(nn) < 0.5: continue
            nn /= np.linalg.norm(nn); offs = {round(float(nn @ np.array(T_[9:12])) * MM, 4)}
            for dn, dv in rp.get('dims') or []:
                v = num(dv)
                if v is not None: offs |= {v, -v}
            for o in offs:
                if not any(abs(abs(np.dot(p[0], nn)) - 1) < 1e-6 and abs(p[1] * np.sign(np.dot(p[0], nn)) - o) < 1e-6 for p in planes):
                    planes.append((nn, o))
        seeds = [x for x in (m.get('seed_features') or {}) if m.get('confidence') != 'low']
        order = [x for x in self.order if x in seeds] + [x for x in self.order if x not in seeds]
        s0 = self.cur_score(); best = None
        for pi, (nrm, off) in enumerate(planes):
            mp = Plane(origin=tuple(nrm * off), z_dir=tuple(nrm)); g = 0.0; cnt = 0
            for src in order:
                kind, T = self.tools[src]
                if kind == 'blend': continue
                try: sc, _ = self.tool_score(kind, T.mirror(mp))
                except Exception: continue
                if sc > s0 + 1e-5: g += sc - s0; cnt += 1
            if best is None or g > best[0] + 1e-9: best = (g, pi, mp, nrm, off, cnt)
        done = []
        if best is not None and best[0] > 0:
            g, pi, mp, nrm, off, cnt = best
            for src in order:
                kind, T = self.tools[src]
                if kind == 'blend': continue
                try: M = T.mirror(mp)
                except Exception: continue
                if self.try_tool(f'{F.name}<{src}', kind, M, f'mirror of {src} about n={np.round(nrm, 3).tolist()} d={off:g} (plane {pi}, dry-run gain {g:.4f})'): done.append(src)
        # mirrored blends
        nrm, off = (best[3], best[4]) if best is not None and best[0] > 0 else planes[0]
        mp = (np.asarray(nrm, float), np.asarray(nrm, float) * off / MM)     # FD.mirror_surface form (metres)
        for src in [x for x in seeds if x in self.part.by_name and self.part.by_name[x].type in ('Fillet', 'Chamfer')]:
            try:
                n0 = len(LOG); self.blend_feature(self.part.by_name[src], mirror=mp)
                if any(x.get('status') in ('OK', 'PART') for x in LOG[n0:]):
                    done.append(src); FD.log(f'{F.name}<{src}', 'OK', f'mirrored blend {src}', iou=round(float(self.cur_score()), 4))
            except Exception as ex:
                FD.log(F.name, 'WARN', f'mirrored blend {src}: {type(ex).__name__}')
        if not done: FD.log(F.name, 'SKIP', 'no mirrored seed improves the oracle IoU')

    def cir_pattern(self, F):
        """round 17: circular pattern from its decoded dims (D1 count, D3 total angle); the axis
        (global axes, cylinder axes of the body) and the seed are chosen by a dry run."""
        fd = {k.split('@')[0]: v for k, v in F.dims.items()}
        N = int(round(fd.get('D1') * MM)) if fd.get('D1') else 0
        tot = math.degrees(fd.get('D3', 2 * math.pi)) if fd.get('D3', 7) < 7 else 360.0
        if N < 2: FD.log(F.name, 'SKIP', 'circular pattern: count not decoded'); return
        step = tot / N if abs(tot - 360) < 1e-6 else tot / (N - 1)
        axes = [((0, 0, 0), a) for a in ((1, 0, 0), (0, 1, 0), (0, 0, 1))]
        try:
            from OCP.BRepAdaptor import BRepAdaptor_Surface
            from OCP.GeomAbs import GeomAbs_Cylinder
            for fc in self.body.faces():
                ad = BRepAdaptor_Surface(fc.wrapped)
                if ad.GetType() != GeomAbs_Cylinder: continue
                ax = ad.Cylinder().Axis(); o = ax.Location(); d_ = ax.Direction()
                c = ((o.X(), o.Y(), o.Z()), (d_.X(), d_.Y(), d_.Z()))
                if not any(np.allclose(np.cross(c[1], a[1]), 0, atol=1e-6) and np.linalg.norm(np.cross(np.subtract(c[0], a[0]), a[1])) < 1e-6 for a in axes): axes.append(c)
        except Exception: pass
        s0 = self.cur_score(); best = None
        for src in [x for x in reversed(self.order) if self.tools[x][0] != 'blend'][:3]:
            kind, T = self.tools[src]
            for o, a in axes[:8]:
                for sg in (1, -1):
                    try:
                        cps = [T.rotate(Axis(o, a), sg * step * k) for k in range(1, N)]
                        U = cps[0].fuse(*cps[1:]) if len(cps) > 1 else cps[0]
                        sc, _ = self.tool_score(kind, U)
                        sup = self.surf_support(kind, cps[0]) if not self.exact else None
                    except Exception: continue
                    key = sc + (0.0 if sup is None else 0.01 * sup)
                    if best is None or key > best[0]: best = (key, sc, sup, src, kind, U, o, a, sg)
                    if abs(step * N - 360) < 1e-6: break
        if best is None: FD.log(F.name, 'SKIP', 'circular pattern: no candidate'); return
        key, sc, sup, src, kind, U, o, a, sg = best
        ok = sc > s0 + 1e-5 or (not self.exact and sup is not None and sup >= 0.8 and sc >= s0 - 1e-3)
        if ok and self.commit(f'{F.name}<{src}', kind, U) is not False:
            FD.log(f'{F.name}<{src}', 'OK', f'circular pattern of {src}: {N} x {step:g} deg about {np.round(a, 3).tolist()} @ {np.round(o, 3).tolist()}', iou=round(float(self.cur_score()), 4), support=sup)
        else:
            FD.log(F.name, 'SKIP', f'circular pattern: best candidate {src} axis {np.round(a, 3).tolist()} gives {sc:.4f} vs {s0:.4f} (support {sup})')

    def pattern_feature(self, F):
        m = self.g.pat.get(F.name) or {}
        offs = m.get('common_offsets_mm') or []
        if not offs and F.type in ('CirPattern', 'CircularPattern'): return self.cir_pattern(F)
        done = 0
        for src in list(self.order):
            kind, T = self.tools[src]
            for o in offs:
                try: M = T.moved(Location(tuple(o)))
                except Exception: continue
                done += self.try_tool(f'{F.name}<{src}', kind, M, f'pattern of {src} by {np.round(o, 3).tolist()}')
        if not done: FD.log(F.name, 'SKIP', f'pattern: {len(offs)} offsets, nothing improves the oracle IoU')

    def loft_feature(self, F):
        """Loft: the closed outlines of the unconsumed sketches just before the feature (profile
        order = feature order), lofted; applied as boss or cut only if the oracle IoU improves."""
        from build123d import loft, Wire
        prev = [f for f in self.part.features if f.id < F.id and f.sketch is not None and f.sketch.segs and f.name not in self.g.used]
        prev = prev[-4:]
        kind = 'cut' if 'cut' in F.name.lower() else 'boss'
        best = None
        import itertools
        def section(sf, fr):
            sk = sf.sketch; r0, t0 = sk.rot, sk.trans
            sk.rot, sk.trans = fr[:2]
            try:
                cells = FD.sketch_cells(sf)
                if not cells: return None
                U = cells[0].fuse(*cells[1:]) if len(cells) > 1 else cells[0]
                return max(U.faces(), key=lambda x: x.area) if hasattr(U, 'faces') else U
            except Exception: return None
            finally: sk.rot, sk.trans = r0, t0
        for k in range(len(prev) - 1):
            profs = prev[k:]
            # round 17: every frame combination of a two-profile loft is tried (FS1 Sketch7 lies on
            # Plane2, not on its decoded frame); longer lofts use each profile's best-registered frame
            if len(profs) == 2:
                opts = [[(fr, section(sf, fr)) for fr in self.frames(sf)[:6]] for sf in profs]
            else:
                opts = [[(max(self.frames(sf), key=lambda x: float(x[2].split('reg=')[-1])),) * 1] for sf in profs]
                opts = [[(o[0], section(sf, o[0]))] for sf, o in zip(profs, opts)]
            for combo in itertools.product(*opts):
                secs = [c[1] for c in combo if c[1] is not None]
                if len(secs) < len(profs): continue
                if len(secs) == 2 and abs((secs[0].center() - secs[1].center()).length) < 1e-6: continue
                try:
                    T = loft([Face(f.outer_wire()) for f in secs])
                    if T is None or T.volume < 1e-9: continue
                except Exception as ex:
                    continue
                kd = kind
                try: sc, nb = self.tool_score(kd, T)
                except Exception: continue
                sup = None
                if not self.exact and os.environ.get('R17_SURF', '1') == '1':
                    try: sup = self.surf_support(kd, T, n=160)
                    except Exception: sup = None
                key = sc + (0.0 if sup is None else 0.05 * sup)
                if best is None or key > best[5]: best = (sc, T, nb, [p.name for p in profs], kd, key, sup, [c[0][2] for c in combo])
        sup = best[6] if best is not None else None
        if best is not None and best[0] < self.cur_score() - 1e-3: sup = None
        if best is None or (best[0] <= self.cur_score() + 1e-6 and not (sup is not None and sup >= 0.8)):
            FD.log(F.name, 'SKIP', f'loft of {[p.name for p in prev]}: no IoU gain (surface support {sup})'); return
        for p in best[3]: self.g.used.add(p)
        if self.commit(F.name, best[4], best[1], best[2]) is False: FD.log(F.name, 'FAIL', 'loft: B-rep boolean failed'); return
        FD.log(F.name, 'OK', f'loft {best[4]} of {best[3]}', frames=str(best[7]), support=sup, iou=round(float(self.cur_score()), 4))

    def thread_feature(self, F):
        """Thread feature: V-profile (Thread Profile sketch: Pitch, Profile_Height, Profile_Angle)
        swept along a helix on a body cylinder of the thread diameter, cut into the material
        (external thread on a rod, internal thread in a hole).  The cylinder, the thread length
        (whole face or a decoded length dim) and the profile side are chosen by the oracle."""
        from build123d import Helix, sweep, Wire
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Cylinder
        prof = next((f for f in reversed(self.part.features) if f.id < F.id and 'Thread Profile' in f.name), None)
        pd = {k.split('@')[0]: v for k, v in (prof.dims.items() if prof else [])}
        fd = {k.split('@')[0]: v for k, v in F.dims.items()}
        pitch = pd.get('Pitch') or fd.get('D7')
        h = pd.get('Profile_Height') or (pitch * 0.54 if pitch else None)
        diam = fd.get('D6')
        if not pitch or not h or not diam: FD.log(F.name, 'SKIP', 'thread: pitch/height/diameter not decoded'); return
        pitch *= MM; h *= MM; r0 = diam * MM / 2
        ang = math.radians(math.degrees(pd.get('Profile_Angle', math.radians(60))) / 2) if pd.get('Profile_Angle', 1) < 7 else math.radians(30)
        hw = min(h * math.tan(ang), 0.49 * pitch)
        lens = sorted({v * MM for k, v in fd.items() if k in ('D2', 'D4') and v * MM > pitch})
        land_ = (pd.get('Profile_Land') or 0) * MM
        best = None; s0 = self.cur_score(); cands = []
        for fc in self.body.faces():
            ad = BRepAdaptor_Surface(fc.wrapped)
            if ad.GetType() != GeomAbs_Cylinder: continue
            cy = ad.Cylinder(); r = cy.Radius()
            if abs(r - r0) > 0.15 * r0: continue
            ax = cy.Axis(); o = np.array([ax.Location().X(), ax.Location().Y(), ax.Location().Z()]); a = np.array([ax.Direction().X(), ax.Direction().Y(), ax.Direction().Z()])
            V = np.array([tuple(v) for v in fc.vertices()]) if fc.vertices() else np.array([tuple(fc.center())])
            bb = fc.bounding_box(); C = np.array([[bb.min.X, bb.min.Y, bb.min.Z], [bb.max.X, bb.max.Y, bb.max.Z]])
            t = sorted(((C - o) @ a).tolist()); t0, t1 = t[0], t[-1]
            if t1 - t0 < pitch: continue
            x = np.cross(a, [1, 0, 0] if abs(a[0]) < 0.9 else [0, 1, 0]); x /= np.linalg.norm(x)
            q = o + a * (t0 + t1) / 2 + x * (r + 0.05 * h)
            from OCP.BRepClass3d import BRepClass3d_SolidClassifier
            from OCP.gp import gp_Pnt
            from OCP.TopAbs import TopAbs_IN
            hole = BRepClass3d_SolidClassifier(self.body.wrapped, gp_Pnt(*q), 1e-6).State() == TopAbs_IN
            for L in [t1 - t0] + [l for l in lens if l < t1 - t0]:
                for start, ph, lh, land in [(s_, ph, lh, land) for s_ in ((t0,) if L >= t1 - t0 - 1e-6 else (t0, t1 - L)) for ph in np.arange(8) / 8 for lh in (False, True) for land in (0.0, land_)]:
                    try:   # phase and hand are not decoded: tried against the oracle
                        st = start + ph * pitch; LL = L - ph * pitch
                        pl = Plane(origin=tuple(o + a * st), x_dir=tuple(x), z_dir=tuple(a))
                        H = Helix(pitch=pitch, height=LL, radius=r, center=pl.origin, direction=pl.z_dir, lefthand=lh)
                        p0 = np.array(tuple(H.position_at(0))); rd = p0 - (o + a * st); rd -= a * (rd @ a); rd /= np.linalg.norm(rd)
                        sgn = 1 if hole else -1
                        def tool(shrink=1.0, land=land, H=H, p0=p0, rd=rd, sgn=sgn):
                            w2 = min(hw + land / 2, 0.45 * pitch) * shrink; pts = [p0 - a * w2 - sgn * rd * 0.02, p0 + sgn * rd * h - a * land / 2 * shrink]
                            if land > 0: pts.append(p0 + sgn * rd * h + a * land / 2 * shrink)
                            pts.append(p0 + a * w2 - sgn * rd * 0.02)
                            return sweep(Face(Wire.make_polygon([Vector(*p) for p in pts], close=True)), path=H, is_frenet=True)
                        T = tool()
                        sc, nb = self.tool_score('cut', T)
                    except Exception as ex:
                        nfail = locals().get('nfail', 0) + 1
                        if nfail == 1: FD.log(F.name, 'WARN', f'thread candidate failed: {type(ex).__name__} {str(ex)[:80]}')
                        continue
                    cands.append((sc, tool, nb, dict(r=round(r, 3), L=round(L, 3), hole=hole, phase=float(ph), lefthand=lh, land=land)))
        if not self.exact and os.environ.get('R17_SURF', '1') == '1':
            # round 17: thread flanks are sub-voxel; rank by point-to-surface support on the oracle
            sc2 = []
            for c in cands:
                try: sup = self.surf_support('cut', c[1](), n=160)
                except Exception: sup = None
                sc2.append((c[0] + (0.0 if sup is None else sup), c[0], c[1], c[2], dict(c[3], support=sup), sup))
            self._thread_sup = sorted([round(sup, 3) for k, v, t, nb, i, sup in sc2 if sup is not None], reverse=True)[:6]
            cands = [(k, t, nb, dict(i, voxel=v)) for k, v, t, nb, i, sup in sc2 if v >= s0 - 1e-3 and (v > s0 + 1e-6 or (sup or 0) >= 0.8)]
            s0 = -1.0
        cands.sort(key=lambda c: -c[0])
        best = None
        for sc, tool, nb, info in cands[:6]:
            if sc <= s0 + 1e-6: break
            for shrink in (1.0, 0.95, 0.85):   # OCC cuts of near-touching helix turns fail silently: verify on the B-rep
                try:
                    T = tool(shrink); c = self.body.cut(T); dv = FD.vol(self.body) - FD.vol(c)
                    if dv > 0.5 * T.volume * 0.5: best = (sc, T, None, dict(info, shrink=shrink)); break
                except Exception:
                    pass
            if best: break
        if best is None or best[0] <= s0 + 1e-6: FD.log(F.name, 'SKIP', f'thread: no helix improves the oracle IoU (best surface support {getattr(self, "_thread_sup", None)}, {len(cands)} candidates)'); return
        if s0 < 0: best = (best[0], best[1], None, best[3])
        if self.commit(F.name, 'cut', best[1], best[2]) is False: FD.log(F.name, 'FAIL', 'thread: B-rep boolean failed'); return
        FD.log(F.name, 'OK', f'thread pitch {pitch:g} h {h:g} {best[3]}', iou=round(best[0], 4))

    def _run_one(self, f):
        t = f.type; nm = f.name
        if t in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion', 'Cut', 'Boss', 'ICE', 'Extrude'): self.extrude_feature(f)
        elif t in ('Revolve', 'Cut-Revolve', 'RevCut'): self.revolve_feature(f)
        elif t in ('Loft', 'Cut-Loft'): self.loft_feature(f)
        elif t == 'Thread' and self.body is not None: self.thread_feature(f)
        elif t in ('Fillet', 'Chamfer') and self.body is not None: self.blend_feature(f)
        elif t in ('Mirror', 'MirrorPattern') and self.body is not None: self.mirror_feature(f)
        elif t in ('LPattern', 'CirPattern', 'LinearPattern', 'CircularPattern') and self.body is not None: self.pattern_feature(f)
        elif t in ('ProfileFeature', 'Plane', 'RefPlane', 'Sketch', 'OriginProfileFeature') or 'Folder' in t: return
        else: FD.log(nm, 'SKIP', f'unsupported type {t}')

    def run(self):
        prog = os.environ.get('R15_PROGRESS'); skip = set(x for x in os.environ.get('R15_SKIP', '').split('|') if x)
        rin0 = self.ref.rin; feats = list(self.part.features)
        # look-ahead target: voxels a later cut removes are don't-care -> treated as body material
        suf = [None] * (len(feats) + 1); acc = None
        for k in range(len(feats) - 1, -1, -1):
            suf[k + 1] = acc
            for key in (feats[k].name, feats[k].name + '#spec'):
                m = self.lookahead.get(key)
                if m is not None: acc = m.copy() if acc is None else (acc | m)
        self._suf = suf
        # exact track: same suffix unions over the removal manifolds of the earlier pass
        sufm = [None] * (len(feats) + 1); acc = None
        if self.exact and self.lookahead_m:
            for k in range(len(feats) - 1, -1, -1):
                sufm[k + 1] = acc
                for key in (feats[k].name, feats[k].name + '#spec'):
                    m = self.lookahead_m.get(key)
                    if m is not None: acc = m if acc is None else (acc + m)
        self._sufm = [None if x is None else (self.ref.M + x) for x in sufm]
        try:
            return self._run_feats(feats, prog, skip, rin0)
        finally:
            self.ref.rin = rin0
            if self.exact: self.set_target(self.ref.M)

    def _run_feats(self, feats, prog, skip, rin0):
        for k, f in enumerate(feats):
            self.ref.rin = rin0 if self._suf[k + 1] is None else (rin0 | self._suf[k + 1])
            if self.exact:
                MT = self._sufm[k + 1] if self._sufm[k + 1] is not None else self.ref.M
                if MT is not self.MT: self.set_target(MT)
            if prog:
                with open(prog, 'w') as fh: fh.write(f.name)
            if f.name in skip:
                FD.log(f.name, 'SKIP', 'OCC crashed (segfault) on this feature in an earlier attempt'); continue
            prev = self.body
            try:
                self._run_one(f)
            except Exception as ex:
                FD.log(f.name, 'ERROR', f'{type(ex).__name__}: {str(ex)[:120]}')
                if self.exact and self.body is not prev: self.resync()
            if self.body is not None and self.body is not prev and not self.body.is_valid:
                from OCP.ShapeFix import ShapeFix_Shape
                sf = ShapeFix_Shape(self.body.wrapped); sf.Perform()
                fx = Compound(sf.Shape())
                if fx.is_valid: self.body = fx
        return self.body


_tri_of0 = DO.tri_of
def _tri_of(shape, tol=0.05):
    """DO.tri_of, falling back to face-by-face tessellation (skipping faces OCC cannot mesh;
    mirrored side panels have one)."""
    try: return _tri_of0(shape, tol)
    except Exception: pass
    out = []
    for f in shape.faces():
        try:
            V, T = f.tessellate(tol, 0.2)
            if len(T): out.append(np.array([tuple(v) for v in V])[np.array(T)])
        except Exception: continue
    return np.concatenate(out) if out else np.zeros((0, 3, 3))
DO.tri_of = _tri_of

_iou_vox = DO.iou
def _iou_exact(A, B, pitch=0.25):
    """round 17: reference-STL IoU by exact mesh booleans (manifold3d); voxel only if a mesh is open."""
    import exact_iou as XI
    if os.environ.get('R17_EXACT', '1') == '1':
        try:
            v, how = XI.exact_iou(A, B)
            if how == 'manifold': return v, 'exact'
        except Exception: pass
    v, p = _iou_vox(A, B, pitch); return v, f'voxel {p:g}'
DO.iou = _iou_exact
def _tri_fine(shape, tol=0.02):
    import exact_iou as XI
    try:
        T = XI.mesh_of(shape)
        if len(T): return T
    except Exception: pass
    return _tri_of(shape, tol)
if os.environ.get('R17_EXACT', '1') == '1': DO.tri_of = _tri_fine


def compare(body, part, oracle_T=None):
    """decode_only.compare, except that when no assembly placement is decoded the registration
    (24 axis rotations + bbox centring) is fitted on the oracle mesh and then applied to the body,
    so a stray tool cannot drag the registration (RV23).  The oracle is decoded from the SLDPRT."""
    tris = DO.tri_of(body)
    if DO.placements(part) or oracle_T is None:
        b = DO.compare(body, part)
        if b is None or b[2] != 'registered(no decoded placement)' or oracle_T is None: return b
    import itertools
    tok = part.split()[0]
    refs = sorted(glob.glob(os.path.join(DO.STL, re.sub(r'[^A-Za-z0-9]', '_', tok) + '_*.stl'))) if tok[:2] in ('RV', 'FS') else \
        sorted(glob.glob(os.path.join(DO.STL, re.sub(r'[^A-Za-z0-9]', '_', part) + '_[0-9].stl')))
    rots = [np.array(P) * np.array(sg)[:, None] for P in itertools.permutations(np.eye(3)) for sg in itertools.product((1, -1), repeat=3)]
    rots = [Q for Q in rots if np.linalg.det(Q) > 0]
    best = None
    for r in refs:
        B = DO.read_stl(r); bl, bh = B.reshape(-1, 3).min(0), B.reshape(-1, 3).max(0)
        E = []
        for k, Q in enumerate(rots):
            A = oracle_T @ Q; al, ah = A.reshape(-1, 3).min(0), A.reshape(-1, 3).max(0)
            E.append((float(np.abs((ah - al) - (bh - bl)).sum()), k))
        E.sort()
        for e_, k in E[:4]:
            Q = rots[k]; A = oracle_T @ Q; al, ah = A.reshape(-1, 3).min(0), A.reshape(-1, 3).max(0)
            t = ((bl + bh) - (al + ah)) / 2
            vo, _ = DO.iou(A + t, B)
            if best is None or vo > best[0]: best = (vo, r, Q, t)
    if best is None: return None
    vo, r, Q, t = best
    v, p = DO.iou(tris @ Q + t, DO.read_stl(r))
    return (v, os.path.basename(r), f'registered on the oracle mesh (oracle IoU {vo:.4f})', p)


def body_solid(b):
    if b is None: return None
    sl = b.solids()
    return sl[0] if len(sl) == 1 else Compound(sl)


def run_derived(part, src, out_dir=HERE):
    """MirrorStock part: the source part's decode-only rebuild, reflected about the fitted plane."""
    import mirror_derived as MD
    from build123d import import_brep
    t0 = time.time()
    bp = os.path.join(out_dir, 'breps' + ('' if SRC == 'revdev' else '_' + SRC), src + '.brep')
    if not os.path.exists(os.path.join(ROOT, SRC, src + '.SLDPRT')) or not os.path.exists(os.path.join(DO.DEC, src + '.json')):
        return dict(iou=None, note=f'mirror source {src} not in {SRC}/')
    if not os.path.exists(bp):
        r = run_part(src, out_dir)
        if SRC != 'revdev':
            try: json.dump(r, open(os.path.join(out_dir, 'results_' + SRC, src + '.json'), 'w'), indent=1, default=float)
            except Exception: pass
    if not os.path.exists(bp): return dict(iou=0.0, note=f'source {src} not rebuilt')
    sc, n, d = MD.fit_plane(src, part)
    body = import_brep(bp).mirror(Plane(origin=tuple(n * d), z_dir=tuple(n)))
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy   # deep copy: the mirrored shape can carry stale/missing triangulation
    body = type(body)(BRepBuilderAPI_Copy(body.wrapped, True, False).Shape())
    try: export_brep(body, os.path.join(out_dir, 'breps' + ('' if SRC == 'revdev' else '_' + SRC), part + '.brep'))
    except Exception: pass
    T = DL.triangles(os.path.join(ROOT, SRC, part + '.SLDPRT'))
    if T is None or len(T) <= 12:   # no display mesh of its own: the source's final-body mesh, reflected
        Ts = DL.triangles(os.path.join(ROOT, SRC, src + '.SLDPRT'))
        if Ts is not None and len(Ts) > 12:
            T = (Ts - 2 * ((Ts @ n) - d)[..., None] * n)[:, ::-1]
    has_T = T is not None and len(T) > 12
    b = compare(body, part, T if has_T else None) if SRC == 'revdev' else None
    oe = (None, None)
    if has_T:
        import exact_iou as XI
        try: oe = XI.exact_iou(XI.mesh_of(body), T)
        except Exception: pass
    mname = next((f['name'] for f in json.load(open(os.path.join(DO.DEC, part + '.json')))['features'] if f['type'].endswith('_Mirrored')), 'MirrorStock')
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], oracle=None, derived_from=src,
                oracle_iou=round(float(oe[0]), 4) if oe[0] is not None else None, oracle_iou_method=oe[1],
                log=[dict(feature=mname, status='OK', msg=f'mirror of the {src} rebuild')],
                mirror=dict(normal=n.tolist(), offset_mm=d, vertex_fit=round(sc, 4)), volume=round(body.volume, 1),
                seconds=round(time.time() - t0, 1))


def run_part(part, out_dir=HERE, verbose=False):
    import mirror_derived as MD
    src = MD.source_of(part)
    if src: return run_derived(part, src, out_dir)
    t0 = time.time(); LOG.clear(); R.LOG.clear()
    R.DEC = DO.regen(part); R.PART = part
    ref = oracle_for(part)
    if ref is None: return dict(iou=None, note='no oracle (no display mesh, no XT mesh)')
    ref.init_points()
    ctx = contextlib.nullcontext() if verbose else contextlib.redirect_stdout(io.StringIO())
    with ctx:
        rb = OracleReplay(part, ref); body = body_solid(rb.run()); log = LOG[:]
        sco = lambda r: float(r.escore()) if r.exact else float(ref.miou(r.bin))
        npass = int(os.environ.get('R16_PASSES', 3)); passes = [round(sco(rb), 4)]
        la, lam = {}, {}
        if not any(x['status'] == 'FAIL' for x in LOG): npass = 1     # nothing failed: no look-ahead pass
        for it in range(1, npass):
            if not any(k.endswith('#spec') for k in rb.cutvox) and it > 1 and set(rb.cutvox) <= set(la): break
            la = {**la, **rb.cutvox}; lam = {**lam, **rb.cutman}
            LOG.clear(); R.LOG.clear()
            try:
                rb2 = OracleReplay(part, ref, la, lam); b2 = body_solid(rb2.run())
            except Exception as ex:
                passes.append(repr(ex)[:80]); break
            s2 = sco(rb2) if b2 is not None else 0.0; passes.append(round(s2, 4))
            if b2 is not None and s2 > sco(rb) + 1e-4: rb, body, log = rb2, b2, LOG[:]
            else: break
        LOG[:] = log
    if body is None: return dict(iou=0.0, note='no body', oracle=ref.source, log=LOG[:])
    try: export_brep(body, os.path.join(out_dir, 'breps' + ('' if SRC == 'revdev' else '_' + SRC), part + '.brep'))
    except Exception: pass
    b = compare(body, part, ref.T) if SRC == 'revdev' else None
    st = {}
    for x in LOG: st[x['status']] = st.get(x['status'], 0) + 1
    import exact_iou as XI
    try:
        BT = XI.mesh_of(body); oe = XI.exact_iou(BT, ref.T); sd = XI.surf_dist(BT, ref.T)
    except Exception as ex:
        oe, sd = (None, repr(ex)[:80]), {}
    vox = round(float(ref.miou(ref.G.inside(body) if rb.exact else rb.bin)), 4)
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], iou_method=b and b[3], oracle=ref.source,
                oracle_iou=round(float(oe[0]), 4) if oe[0] is not None else vox, oracle_iou_method=oe[1] if oe[0] is not None else 'voxel (open oracle mesh)',
                oracle_iou_vox=vox,
                oracle_surf=dict((k, round(v, 4)) for k, v in sd.items()), exact_track=rb.exact,
                volume=round(body.volume, 1), oracle_volume=round(ref.V, 1),
                ops=st, seconds=round(time.time() - t0, 1), passes=passes,
                log=[{k: (v if isinstance(v, (int, float, str, type(None))) else str(v)) for k, v in x.items()} for x in LOG])


def main(sel):
    os.makedirs(os.path.join(HERE, 'breps' + ('' if SRC == 'revdev' else '_' + SRC)), exist_ok=True)
    parts = sorted(os.path.basename(p)[:-7] for p in glob.glob(os.path.join(ROOT, SRC, '*.SLDPRT')))
    parts = [p for p in parts if not sel or any(p.startswith(x) for x in sel)]
    rp = os.path.join(HERE, 'decode_replay.json')
    res = json.load(open(rp)) if os.path.exists(rp) else {}
    for part in parts:
        try: res[part] = run_part(part, verbose='-v' in sys.argv)
        except Exception as ex:
            res[part] = dict(iou=0.0, note=repr(ex)[:300], tb=traceback.format_exc()[-1500:])
        r = res[part]; print(part, r.get('iou'), r.get('ref'), r.get('oracle'), r.get('oracle_iou'), r.get('ops'), r.get('seconds'), r.get('note', ''), flush=True)
        json.dump(res, open(rp, 'w'), indent=1, default=float)


if __name__ == '__main__':
    main([a for a in sys.argv[1:] if not a.startswith('-')])
