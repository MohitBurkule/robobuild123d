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
    DO.OUT = os.path.join(ROOT, 'tools', 'wip_r19', 'decode_only_' + SRC); os.makedirs(DO.OUT, exist_ok=True)
    _src = open(DO.__file__).read()
    exec(compile(_src[_src.index('def regen(part):'):_src.index('class GRebuild')].replace("'revdev'", repr(SRC)), DO.__file__, 'exec'), DO.__dict__)
    import mirror_derived as _MD; _MD.DEC = DO.DEC
BIG = FD.BIG
BSUF = ('' if SRC == 'revdev' else '_' + SRC) + (('_' + os.environ['R18_TAG']) if os.environ.get('R18_TAG') else '')
LOG = FD.LOG


def num(s):
    s = str(s).replace('<MOD-DIAM>', '')
    m = re.search(r'-?\d+(\.\d+)?', s)
    return float(m.group()) if m else None


_CRASHES = 0
def _forked(orig, label):
    """round 18: run an OCC blend in a forked child.  OCC fillets segfault intermittently (RV16
    Fillet1 2 of 3 runs; RV01 Fillet13/16/17), which used to kill the whole part and force a rerun
    without that feature.  The child computes the blend and writes it as BRep; a crash in the child
    is an ordinary exception here.  R18_FORKBLEND=0 calls OCC directly."""
    import functools
    @functools.wraps(orig)
    def run(self, *a, **k):
        if os.environ.get('R18_FORKBLEND', '1') != '1' or not hasattr(os, 'fork'): return orig(self, *a, **k)
        import tempfile, signal as _sg
        from build123d import import_brep
        fd, path = tempfile.mkstemp(suffix='.brep'); os.close(fd)
        pid = os.fork()
        if pid == 0:
            code = 3
            try:
                r = orig(self, *a, **k)
                if r is not None: export_brep(r, path); code = 0
            except BaseException:
                code = 3
            os._exit(code)
        t0 = time.time(); st = None
        while True:
            p_, st = os.waitpid(pid, os.WNOHANG)
            if p_: break
            if time.time() - t0 > float(os.environ.get('R18_FORKTMO', 300)):
                os.kill(pid, _sg.SIGKILL); os.waitpid(pid, 0); os.unlink(path)
                raise RuntimeError(f'{label}: OCC blend timed out (isolated)')
            time.sleep(0.01)
        try:
            if os.WIFSIGNALED(st):
                global _CRASHES
                _CRASHES += 1
                FD.log('occ', 'INFO', f'{label}: OCC crashed (signal {os.WTERMSIG(st)}) in an isolated blend; candidate dropped')
                raise RuntimeError(f'{label}: OCC crashed (isolated)')
            if os.WEXITSTATUS(st) != 0: raise RuntimeError(f'{label} failed')
            r = import_brep(path)
            sl = r.solids()
            return sl[0] if len(sl) == 1 else r
        finally:
            try: os.unlink(path)
            except Exception: pass
    return run


def _install_forked_blends():
    from build123d.topology import Mixin3D
    if not getattr(Mixin3D.fillet, '_r18', False):
        for nm in ('fillet', 'chamfer'):
            f = _forked(getattr(Mixin3D, nm), nm); f._r18 = True; setattr(Mixin3D, nm, f)
_install_forked_blends()


def span_pairs(offs, D, tol=1e-3):
    """round 18: (lo, hi) extents of length D whose both ends lie on the given plane offsets (mm)."""
    so = sorted({round(float(o), 4) for o in offs}); out = []
    for o1 in so:
        for o2 in so:
            if abs(o2 - o1 - D) < tol and (abs(o1) > 1e-4 or abs(o2) > 1e-4) and o2 > 1e-4: out.append((o1, o2))
    return out


def sheet_thickness(d):
    """round 18: decoded sheet-metal thickness (mm): the 'Thickness' dim of a Sheet-Metal feature."""
    T = None
    for f in d.get('features') or []:
        for dn, dv in f.get('dims') or []:
            if f['type'] == 'Sheet-Metal' and dn == 'Thickness' and num(dv): T = num(dv)
    return T


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
    out += close_gaps(out)
    return out, len(dropped)


def close_gaps(segs, gmax=None, nmax=8):
    """r20: a profile whose chains stay open (Toolbox small mod gear Sketch1: converted gear arcs with
    undecoded end points, 4 dangling ends 0.25-9.3 mm apart) yields no cells.  Dangling profile end
    points (used once) are paired nearest-first and joined by straight closing lines, up to R20_GAP mm
    (default 10).  Closed sketches have no dangling ends and are unchanged."""
    if os.environ.get('R20_CLOSEGAPS', '1') != '1': return []
    gmax = float(os.environ.get('R20_GAP', 10.0)) if gmax is None else gmax
    key = lambda q: (round(q[0] * MM, 4), round(q[1] * MM, 4))
    deg = {}; pos = {}
    for sg in segs:
        if sg.construction or (sg.type == 1 and sg.p0 == sg.p1): continue
        for q in (sg.p0, sg.p1):
            k = key(q); deg[k] = deg.get(k, 0) + 1; pos[k] = q
    dang = [k for k, n in deg.items() if n % 2 == 1]
    if not dang or len(dang) > nmax: return []
    # only a profile with no closed loop at all is closed up (RV12 Sketch1 has closed loops plus stray
    # open curves: closing those changed its cells, 0.875 -> 0.865)
    par = {}
    def fnd(x):
        while par.get(x, x) != x: x = par[x]
        return x
    for sg in segs:
        if sg.construction: continue
        if sg.type == 1 and sg.p0 == sg.p1: return []          # a full circle is a closed loop
        a, b = fnd(key(sg.p0)), fnd(key(sg.p1))
        if a == b: return []                                     # this edge closes a cycle
        par[a] = b
    pairs = sorted((math.dist(a, b), a, b) for i, a in enumerate(dang) for b in dang[i + 1:])
    used = set(); out = []
    for d, a, b in pairs:
        if a in used or b in used or d > gmax or d < 1e-9: continue
        used |= {a, b}; pa, pb = pos[a], pos[b]
        out.append(DP.Seg(f'g{len(out)}', 0, False, p0=(pa[0], pa[1], 0), p1=(pb[0], pb[1], 0)))
    # ends too far apart for a closing line: a minor arc about a centre of the sketch's own arcs from which
    # both ends are equidistant (small mod gear: the undecoded R35.35 arc concentric with the R44.65 one)
    C = {(round(sg.c[0] * MM, 4), round(sg.c[1] * MM, 4)) for sg in segs if sg.type == 1 and sg.c is not None}
    for d, a, b in pairs:
        if a in used or b in used or d <= gmax: continue
        best = None
        for c in C:
            ra, rb = math.dist(a, c), math.dist(b, c)
            if abs(ra - rb) < 1e-3 and ra > d / 2 and (best is None or abs(ra - rb) < best[0]): best = (abs(ra - rb), c, ra)
        if best is None: continue
        c = best[1]; a0 = math.atan2(a[1] - c[1], a[0] - c[0]); a1 = math.atan2(b[1] - c[1], b[0] - c[0])
        if (a1 - a0) % (2 * math.pi) > math.pi: a, b = b, a      # counter-clockwise minor arc a -> b
        used |= {a, b}; pa, pb = pos[a], pos[b]
        out.append(DP.Seg(f'g{len(out)}', 1, False, p0=(pa[0], pa[1], 0), p1=(pb[0], pb[1], 0), c=(c[0] / MM, c[1] / MM, 0), r=best[2] / MM, dir=1))
    return out


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
        self._pdead = time.time() + float(os.environ.get('R18_PBUDGET', 1e9)) * 0.8
        self._pckpt = time.time() + float(os.environ.get('R18_PBUDGET', 1e9)) * 0.25
        self.ftime = {}; self._deadline = float('inf'); self._budget_hit = False; self._mfc = {}
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
            self._fsdec = dec
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

    @staticmethod
    def repair_mf(shape):
        """r18: ShapeFix + sewing, then a trimesh hole fill, before giving up on a closed manifold."""
        import exact_iou as XI
        try:
            from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
            from build123d import Shape as _S
            sw = BRepBuilderAPI_Sewing(1e-4); sw.Add(shape.wrapped); sw.Perform()
            T = XI.mesh_of(_S.cast(sw.SewedShape()), 0.01)
            M = XI.as_manifold(T) if len(T) else None
            if M is not None: return M
            m = XI._tm(XI.mesh_of(shape, 0.01), 1e-3); m.fill_holes(); m.fix_normals()
            if m.is_watertight: return XI._manifold(m)
            # r19: a multi-solid body whose solids touch along an edge (RV24 / side panel: 3 edges shared by
            # 4 triangles) is not watertight; per solid, a manifold within 1 % of the mesh volume is accepted
            ms = []
            for so in (shape.solids() if hasattr(shape, 'solids') else [shape]):
                Ts = XI.mesh_of(so, 0.01)
                if not len(Ts): continue
                Mi = XI.as_manifold(Ts)
                if Mi is None:
                    t = XI._tm(Ts, 1e-4); Mi = XI._manifold(t)
                    if Mi is None or abs(Mi.volume() - abs(t.volume)) > 1e-2 * abs(t.volume) + 1e-6: return None
                ms.append(Mi)
            if ms:
                import manifold3d as M3
                return ms[0] if len(ms) == 1 else M3.Manifold.batch_boolean(ms, M3.OpType.Add)
        except Exception:
            return None
        return None

    def mfc(self, shape):
        """round 18 coarse check: candidate tools are scored on a coarser tessellation (R18_CTOL mm,
        default 0.005; the committed boolean is still checked at 0.002).  Prism tessellation at 0.002 mm
        dominated the exact track on large parts (corpus timeouts)."""
        return self.mf(shape, float(os.environ.get('R18_CTOL', 0.005)))

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

    def checkpoint(self, force=False):
        """r18: once past the part budget, the body so far is saved (at most once a minute) to
        R18_PARTIAL, so a part the run_all timeout kills still yields a body and a score."""
        p = os.environ.get('R18_PARTIAL')
        if not p or self.body is None: return
        if not force and (time.time() < self._pckpt or time.time() - getattr(self, '_ckt', 0) < 60): return
        if force and getattr(self, '_ckbody', None) is self.body: return
        self._ckbody = self.body
        self._ckt = time.time()
        try:
            export_brep(body_solid(self.body), p + '.brep')
            json.dump(dict(log=[{k: (v if isinstance(v, (int, float, str, type(None))) else str(v)) for k, v in x.items()} for x in LOG],
                           oracle_iou_exact_track=round(float(self.escore()), 4) if self.exact else None, ftime=self.ftime), open(p + '.json', 'w'))
        except Exception:
            pass

    def over(self):
        """round 18: per-feature time budget (R18_FBUDGET s): searches stop once a candidate exists."""
        if time.time() > self._deadline: self._budget_hit = True; return True
        return False

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
            P = self.mfc(T)
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
        if M is None and self.body is not None and self.MB is not None and os.environ.get('R18_KEEPEXACT', '1') == '1':
            # r18: a blend (no tool manifold) left a body whose tessellation does not close: keep the
            # previous manifold (the blend changes the volume by a sliver) instead of dropping to the
            # voxel track for the rest of the part (RV17 lost the exact track at Fillet1)
            M = self.repair_mf(self.body)
            if M is None:
                self._approx = getattr(self, '_approx', 0) + 1
                FD.log('exact-track', 'INFO', 'body tessellation not closed after a blend: previous exact manifold kept')
                return
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
        if D and os.environ.get('R18_SPAN', '1') == '1':
            # r18: a blind extent whose two ends both land on final XT planes parallel to the sketch
            # (start offset from the sketch plane: RV21 Cut-Extrude2 runs 7.25 -> -3.75 from a sketch at 4.75)
            self.xt_points()
            xo = [float((p - origin) @ n) for nn, p in self._xtplanes if abs(abs(nn @ n) - 1) < 1e-6]
            c1 += span_pairs(list(offs) + xo, D)
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

    def fmargin(self, fname, best_fname):
        """round 18: score margin an alternative frame must beat the incumbent by.  A record-backed
        decoded frame is right (plane audit), so an alternative that ties it within tessellation noise
        must not replace it (RV21 Revolve1: top-revy won by noise and moved the revolve seam, 66 -> 53 %
        faces matched).  self._cur_doubt is set per sketch by extrude/revolve."""
        if os.environ.get('R18_FMARGIN', '1') != '1': return 1e-9
        if fname == best_fname or str(fname).startswith('decoded') and not str(fname).startswith('decoded@'): return 1e-9
        return 2e-4 if getattr(self, '_cur_doubt', True) else 2e-3

    def frame_doubt(self, skf):
        """round 18: True when the sketch plane was not read from a plane record (item_sketchplane
        'identity_default': no record found, the Front plane is assumed).  The plane audit against the
        dumps (plane_audit.py) shows every plane_rec / refplane_rec frame right (67/67 on RV01, RV17,
        RV21, RV23, Top Panel) and 41 of 58 identity_default frames wrong (34 offset, 7 normal), so for
        these the alternatives are always searched instead of stopping at a good decoded frame."""
        if os.environ.get('R18_DOUBT', '1') != '1': return False
        sp = self.g.sp.get(skf.name) or {}
        return sp.get('record_class') in (None, 'identity_default', 'sketch_record')

    def frames(self, skf):
        """sketch frame candidates.  Sketch-plane decoding is wrong or incomplete for some sketches
        (RV19 Sketch1: decoded Right Plane; RV23: plane offsets 3 / 7.5 / 17 mm not decoded; sketches
        on back faces with a reversed frame).  Candidates: the decoded frame; the three default
        planes and their reversed versions, each at every offset where a final XT plane parallel to
        it lies.  They are ranked by reg_score (sketch points on XT vertices); the decoded frame
        is always tried first, then the best-registered alternatives."""
        if getattr(skf, '_frames', None) is not None: return skf._frames
        if os.environ.get('R18_DIAG_TRUEFRAME'):   # DIAGNOSTIC ONLY (upper bound): the dump's frame; never used in results
            T_ = DP.parse_dump(os.path.join(ROOT, 'dumps_v2', self.pname + '.dump.txt')); t_ = T_.by_name.get(skf.name)
            if t_ is not None and t_.sketch is not None:
                skf._frames = [(t_.sketch.rot, t_.sketch.trans, 'TRUE(diag)')]; return skf._frames
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
        if self.frame_doubt(skf):   # r18: no plane record: every well-registered alternative, not only those beating the Front-plane guess
            order = [dec] + [i for i in sorted(range(len(uniq)), key=lambda i: -sc[i]) if i != dec and sc[i] >= 0.2][:6]
        else:
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

    # ---- r19 decoded region selection (fstream moContourChooser_c; no chooser = every region)
    def region_segs(self, skf):
        """the replay sketch segments that bound the decoded selected regions: every profile segment
        when the sketch has no contour chooser (validated 291/291 face-evidenced segments), the chooser's
        contours (+ nested loops) otherwise, matched to the replay segments by end points.  None when
        the sketch is not decoded or a selected segment cannot be matched."""
        if os.environ.get('R19_REGION', '1') != '1': return None
        dec = getattr(self, '_fsdec', None)
        fid = next((f['id'] for f in self.g.d['features'] if f['name'] == skf.name), None)
        X = dec.sketches.get(fid) if dec is not None and fid is not None else None
        if X is None: return None
        from sldprt import fstream as FS
        try: sel, has = FS.selected_serials(X['choosers'], X['regions'], X['sketch'], X['chains'] or None)
        except Exception: return None
        prof = skf.sketch.profile_segs()
        if not has: return ('all', prof)
        fsk = X['sketch']; P = {p.pid: p.xy for p in fsk.points if p.xy is not None}
        key = lambda q: (round(q[0] * 1e5), round(q[1] * 1e5))
        out = []
        for sg in fsk.lines + fsk.arcs:
            if sg.serial not in sel or not sg.real: continue
            a, b = P.get(sg.start), P.get(sg.end)
            if a is None or b is None: return None
            ka, kb = key(a), key(b)
            m = [x for x in prof if x.type == (0 if sg.kind == 'line' else 1) and {key(x.p0), key(x.p1)} == {ka, kb}]
            if not m: return None
            out += m
        return ('chooser', list({id(x): x for x in out}.values())) if out else None

    @staticmethod
    def parity_inside(segs, pt):
        """even-odd test of a sketch-local point (mm) against segments (metres): ray to +x."""
        x0, y0 = pt[0], pt[1] + 1.234567e-5; n = 0
        for sg in segs:
            e = FD.seg_edge(sg)
            if e is None: continue
            k = 2 if sg.type == 0 else 48
            Q = [tuple(e.position_at(t / k))[:2] for t in range(k + 1)]
            for (xa, ya), (xb, yb) in zip(Q, Q[1:]):
                if (ya > y0) != (yb > y0):
                    xi = xa + (y0 - ya) * (xb - xa) / (yb - ya)
                    if xi > x0: n += 1
        return n % 2 == 1

    def region_mask(self, skf, cells):
        rs = getattr(skf, '_r19_rs', 0)
        if rs == 0: rs = skf._r19_rs = self.region_segs(skf)
        if rs is None: return None, None
        sk = skf.sketch; X = np.array(sk.rot[0], float); Y = np.array(sk.rot[1], float); t = np.array(sk.trans) * MM
        out = []
        for c in cells:
            try:
                V, Tr = c.tessellate(0.01)
                V = np.array([tuple(v) for v in V]); Tr = np.array(Tr)
                ar = np.linalg.norm(np.cross(V[Tr[:, 1]] - V[Tr[:, 0]], V[Tr[:, 2]] - V[Tr[:, 0]]), axis=1)
                p = V[Tr[int(np.argmax(ar))]].mean(0)
                out.append(self.parity_inside(rs[1], ((p - t) @ X, (p - t) @ Y)))
            except Exception:
                return None, None
        return out, rs[0]

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
        s0 = self.cur_score(); self._ecands = []; self._rbest = None; self._regm = None
        best = None; ncand = 0; frames = self.frames(skf); self._cur_doubt = self.frame_doubt(skf)
        for fi, (rot, tr, fname) in enumerate(frames):
            if fi == 1 and best is not None and best[0] > s0 + 1e-6 and best[5] >= 0.9 and not self.frame_doubt(skf): break
            if fi >= 1 and best is not None and self.over(): break
            sk.rot, sk.trans = rot, tr
            cells = FD.sketch_cells(skf)
            if not cells: continue
            origin = np.array(sk.trans) * MM; n0 = np.array(sk.normal, float)
            percell = [None] * len(cells)     # best (gain, n, ivs, idx) per cell over all candidates
            spec = [None] * len(cells)        # look-ahead: smallest prism per cell that lies outside the final body
            self._regm, self._regmode = self.region_mask(skf, cells) if self.exact else (None, None)
            if self._regm is not None and not any(self._regm): self._regm = None
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
                    if best is None or sc > best[0] + self.fmargin(fname, best[1]):
                        best = (sc, fname, [(cells[ci], n, ivs) for ci in keep], nb, len(cells), self.quality(kind, nb if kind == 'boss' else ~nb & self.bin), 'uniform', (rot, tr), sum(OV))
            # mixed candidate: every cell with a positive net gain, each with its own direction / extent
            mix = [(cells[ci], p[1], p[2], p[3], p[4]) for ci, p in enumerate(percell) if p is not None and p[0] > 0]
            if mix:
                nb = self.bin.copy(); I = np.concatenate([m[3] for m in mix]); nb[I] = kind == 'boss'
                ov = sum(m[4] for m in mix); sc = self.score(nb, ov)
                if best is None or sc > best[0] + self.fmargin(fname, best[1]):
                    best = (sc, fname, [(m[0], m[1], m[2]) for m in mix], nb, len(cells), self.quality(kind, nb if kind == 'boss' else ~nb & self.bin), 'per-cell', (rot, tr), ov)
            if not self.exact and kind == 'cut' and fi == 0 and any(x is not None for x in spec):
                m = np.zeros_like(self.bin); m[np.concatenate([x for x in spec if x is not None])] = True
                self.cutvox.setdefault(F.name + '#spec', m)
        sk.rot, sk.trans = rot0, tr0
        rb_ = self._rbest
        if rb_ is not None and os.environ.get('R19_REGIONSTRICT', '1') == '1' and \
                ((os.environ.get('R19_REGIONTIE', '1') == '1' and rb_[0] >= best[0] - float(os.environ.get('R19_RTOL', 0.002))) if best is not None else rb_[0] >= s0 - float(os.environ.get('R19_RFAIL', 0.002))):
            # r19: the decoded regions replace the oracle's cell choice (the extent is still searched);
            # a region candidate far below the best (wrong frame / mis-decoded chooser) does not
            best = rb_
        self._last_alts = (F.name, skf, kind, code, D, ncand, self.rank_alts(best) if getattr(self, '_beam_on', False) else [])
        if best is None:
            txt = self.sketch_text(skf.name)
            if txt:
                FD.log(F.name, 'SKIP', f'sketch text {txt[0]!r} (font {txt[1]!r}, height {txt[2]:g} mm): glyph outlines are not stored in the file', sketch=skf.name); return
            FD.log(F.name, 'FAIL', 'no cells selected', sketch=skf.name, cand=ncand); return
        fm = None
        if os.environ.get('R18_DBG') == F.name:
            for c in sorted(self._ecands, key=lambda c: -c[0])[:25]:
                print('ECAND', round(c[0], 5), c[1], c[6], len(c[2]), sorted({(round(lo, 2), round(hi, 2)) for cc, n, ivs in c[2] for lo, hi in ivs}), file=sys.stderr, flush=True)
        if self.exact and os.environ.get('R17_FACES', '1') == '1':
            best, fm = self.face_rerank(kind, best)
        if getattr(self, '_beam_on', False) and self._last_alts[6]:
            self._last_alts[6][0] = best    # rank 0 = the greedy choice (after the face re-rank)
        self.commit_extrude(F, skf, kind, code, D, ncand, best, fm)

    def rank_alts(self, best, K=None):
        """r19 beam: the greedy choice plus the K-1 best distinct other extrude candidates of this
        feature (different cell subset, direction or extent) and the best every-cell candidate."""
        K = int(os.environ.get('R19_K', 3)) if K is None else K
        sig = lambda c: (c[1], tuple(sorted((id(cc), tuple(np.round(n, 4)), tuple(map(tuple, np.round(ivs, 4)))) for cc, n, ivs in c[2])))
        out, seen = [best], {sig(best)} if best is not None else set()
        C = sorted(self._ecands, key=lambda c: -c[0])
        for c in C:
            if len(out) >= K: break
            if sig(c) not in seen: seen.add(sig(c)); out.append(c)
        for h in ('all', 'region'):   # the best every-cell and decoded-region candidates are always offered
            a = next((c for c in C if str(c[6]).startswith(h)), None)
            if a is not None and sig(a) not in seen: seen.add(sig(a)); out.append(a)
        return out

    def commit_extrude(self, F, skf, kind, code, D, ncand, best, fm=None):
        sk = skf.sketch; rot0, tr0 = sk.rot, sk.trans
        sc, fname, sel, nb, nc, q, how, fr, ov = best
        sk.rot, sk.trans = fr
        sols = [x for c, n, ivs in sel for lo, hi in ivs for x in self.prism([c], n, lo, hi)]
        T = sols[0] if len(sols) == 1 else sols[0].fuse(*sols[1:]).clean()
        if self.commit(F.name, kind, T, None, ov) is False:
            sk.rot, sk.trans = rot0, tr0
            FD.log(F.name, 'FAIL', 'B-rep boolean failed', sketch=skf.name); return
        self._skframe = {**getattr(self, '_skframe', {}), skf.name: fr}
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
                if best is not None and self.over(): break
                ncand += 1
                keep, U, VV = [], [], []
                for ci, c in enumerate(cells):
                    key = (id(c), tuple(np.round(n, 6)), tuple((round(lo, 5), round(hi, 5)) for lo, hi in ivs))
                    if key in self._mfc: P = self._mfc[key][1]
                    else:
                        try:
                            T = FD.solid_of([x for lo, hi in ivs for x in self.prism([c], n, lo, hi)])
                            P = self.mfc(T)
                        except Exception: P = None
                        self._mfc[key] = (c, P)   # holds c: its id stays unique while cached
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
                if self._regm is not None:   # r19: the decoded region selection
                    RK = [(ci, self._mfc.get((id(c), tuple(np.round(n, 6)), tuple((round(lo, 5), round(hi, 5)) for lo, hi in ivs)), (None, None))[1]) for ci, c in enumerate(cells) if self._regm[ci]]
                    RK = [(ci, P) for ci, P in RK if P is not None]
                    if RK and len(RK) == sum(self._regm):
                        UR = RK[0][1] if len(RK) == 1 else M3.Manifold.batch_boolean([P for _, P in RK], M3.OpType.Add)
                        cr = (self.etool_score(kind, UR), fname, [(cells[ci], n, ivs) for ci, _ in RK], None, len(cells), 1.0, 'region-' + self._regmode, (rot, tr), 0.0)
                        self._ecands.append(cr)
                        if self._rbest is None or cr[0] > self._rbest[0] + self.fmargin(fname, self._rbest[1]): self._rbest = cr
                if getattr(self, '_beam_on', False):   # r19: every cell (SolidWorks' default region), offered to the beam only
                    AL = [(ci, self._mfc.get((id(c), tuple(np.round(n, 6)), tuple((round(lo, 5), round(hi, 5)) for lo, hi in ivs)), (None, None))[1]) for ci, c in enumerate(cells)]
                    AL = [(ci, P) for ci, P in AL if P is not None and P.volume() > eps]
                    if AL and len(AL) != len(keep):
                        UA = AL[0][1] if len(AL) == 1 else M3.Manifold.batch_boolean([P for _, P in AL], M3.OpType.Add)
                        self._ecands.append((self.etool_score(kind, UA), fname, [(cells[ci], n, ivs) for ci, _ in AL], None, len(cells), None, 'all', (rot, tr), 0.0))
                if not keep: continue
                UU = U[0] if len(U) == 1 else M3.Manifold.batch_boolean(U, M3.OpType.Add)
                sc = self.etool_score(kind, UU)
                self._ecands.append((sc, fname, [(cells[ci], n, ivs) for ci in keep], None, len(cells), None, 'uniform', (rot, tr), 0.0))
                if best is None or sc > best[0] + self.fmargin(fname, best[1]):
                    q = self.ecell(kind, UU); q = (q[1] / max(q[0], 1e-12)) if kind == 'boss' else (1 - q[1] / max(q[0], 1e-12))
                    best = (sc, fname, [(cells[ci], n, ivs) for ci in keep], None, len(cells), q, 'uniform', (rot, tr), 0.0)
        mix = [(cells[ci], p[1], p[2], p[3]) for ci, p in enumerate(percell) if p is not None and p[0] > 0]
        if mix:
            UU = mix[0][3] if len(mix) == 1 else M3.Manifold.batch_boolean([m[3] for m in mix], M3.OpType.Add)
            sc = self.etool_score(kind, UU)
            self._ecands.append((sc, fname, [(m[0], m[1], m[2]) for m in mix], None, len(cells), None, 'per-cell', (rot, tr), 0.0))
            if best is None or sc > best[0] + self.fmargin(fname, best[1]):
                q = self.ecell(kind, UU); q = (q[1] / max(q[0], 1e-12)) if kind == 'boss' else (1 - q[1] / max(q[0], 1e-12))
                best = (sc, fname, [(m[0], m[1], m[2]) for m in mix], None, len(cells), q, 'per-cell', (rot, tr), 0.0)
        return best, ncand

    def face_rerank(self, kind, best, tol=None, k=6):
        tol = float(os.environ.get('R18_FTOL', 6e-3)) if tol is None else tol
        """round 17: among extrude candidates whose exact oracle IoU is within tol of the best, keep
        the one whose body reproduces the most decoded XT face patches (face gate as the primary
        criterion; volume IoU cannot tell a 0.05 mm extent error or a wrong cap plane)."""
        if self.over(): return best, None
        C = sorted(self._ecands, key=lambda c: -c[0])
        if str(best[6]).startswith('region'): C = [c for c in C if str(c[6]).startswith('region')]   # r19: stay on the decoded regions
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
        # r18: a candidate up to R18_FTOL below the best IoU wins on faces only with a clear face gain
        # (>= 2 more XT patches); within 2e-3 one more patch is enough (round 17 rule)
        res = [r for r in res if r[2] is best or r[0] > m0 + (0 if r[1] >= best[0] - 2e-3 else 1)]
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
        if getattr(self, '_in_thread', False) or self.over(): B = B0   # r18: voxelising a helical body took > 4 min (10mm standoff); the exact track does not need it
        else:
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
        best = None; self._cur_doubt = self.frame_doubt(skf)
        for fi, (rot, tr, fname) in enumerate(self.frames(skf)):
            if fi == 1 and best is not None and best[4] >= 0.9 and not self.frame_doubt(skf): break
            if fi >= 1 and best is not None and self.over(): break
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
                        except Exception as ex:
                            if os.environ.get('R20_DBG'): print('REVEXC', fname, repr(ex)[:100], file=sys.stderr)
                            continue
                        if P is None or P.volume < 1e-6: continue
                        if self.exact:
                            M = self.mfc(P)
                            if M is None: continue
                            v, vin = self.ecell(kind, M)
                            if os.environ.get('R20_DBG'): print('REVCELL', fname, a.p0, a.p1, sgn, round(v, 3), round(vin, 3), round(P.volume, 9), file=sys.stderr)
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
                    if best is None or sc > best[0] + self.fmargin(fname, best[5]): best = (sc, T, nb, len(keep), q, fname, len(cells), (rot, tr))
        if (best is None or best[0] <= self.cur_score() + 1e-6) and self.exact and os.environ.get('R20_RVFACE', '1') == '1':
            if self.revolve_axis_fallback(F, skf, kind, ang, rot0, tr0): return
        if best is None or best[0] <= self.cur_score() + 1e-6:
            sk.rot, sk.trans = rot0, tr0
            FD.log(F.name, 'FAIL', f'revolve {skf.name}: no axis/cell gives an IoU gain'); return
        sk.rot, sk.trans = best[7]
        if self.commit(F.name, kind, best[1], best[2]) is False:
            sk.rot, sk.trans = rot0, tr0; FD.log(F.name, 'FAIL', 'revolve: B-rep boolean failed'); return
        FD.log(F.name, 'OK', f'revolve {kind} {skf.name} {ang:g} deg', frame=best[5], cells=f'{best[3]}/{best[6]}', prec=round(float(best[4]), 3), iou=round(best[0], 4))

    @staticmethod
    def revolve_axes(sk):
        """r20: the revolve axis is the sketch's own construction line: a flag-0 line that is not a
        flag-0 copy of a profile line (seg_list names those 'a..'; real construction lines 'c..')."""
        own = [s for s in sk.segs if s.construction and s.type == 0 and str(getattr(s, 'id', getattr(s, 'name', ''))).startswith('c')]
        return own or [s for s in sk.segs if s.construction and s.type == 0]

    def revolve_axis_fallback(self, F, skf, kind, ang, rot0, tr0, collect=False):
        """r20: revolve the whole decoded profile (every cell) by the decoded angle about the sketch's
        construction line, both senses, in every candidate frame.  A revolve of a heavily carved body
        (RV17 Revolve4-7: later cuts remove most of the swept volume) gains no oracle IoU, so the choice
        is gated by the decoded XT face patches it reproduces (decode-only face gate): committed when
        the face count rises and the exact oracle IoU drops by at most R20_RVTOL."""
        sk = skf.sketch; tol = float(os.environ.get('R20_RVTOL', 0.01))
        s0 = self.cur_score(); f0 = 0 if collect else self.face_matches(self.body); cand = None; allc = []
        for fi, (rot, tr, fname) in enumerate(self.frames(skf)[:8]):
            if self.over(): break
            sk.rot, sk.trans = rot, tr
            try: cells = FD.sketch_cells(skf)
            except Exception: continue
            if not cells: continue
            for a in self.revolve_axes(sk)[:3]:
                p0 = np.array(sk.to_model(a.p0)) * MM; p1 = np.array(sk.to_model(a.p1)) * MM
                if np.linalg.norm(p1 - p0) < 1e-6: continue
                ax = Axis(tuple(p0), tuple(p1 - p0))
                for sgn in ((1,) if ang >= 359.99 else (1, -1)):
                    ps = []
                    for c in cells:
                        try:
                            P = revolve(c, ax, sgn * ang)
                            if P is not None and P.volume > 1e-6: ps.append(P)
                        except Exception: pass
                    if not ps: continue
                    try:
                        T = ps[0] if len(ps) == 1 else ps[0].fuse(*ps[1:]).clean()
                        M = self.mf(T)
                        if M is None: continue
                        sc = self.etool_score(kind, M)
                        if collect:
                            if sc >= s0 - float(os.environ.get('R20_RVBTOL', 0.06)): allc.append((sc, T, fname, (rot, tr), len(ps)))
                            continue
                        if sc < s0 - tol: continue
                        nb = FD.bop(self.body, T, 'fuse' if kind == 'boss' else 'cut')
                        fm = self.face_matches(nb)
                    except Exception: continue
                    if os.environ.get('R20_DBG'): print('RVFB', fname, sgn, round(sc, 4), fm, f0, file=sys.stderr)
                    k = (fm, sc)
                    if fm > f0 and (cand is None or k > cand[0]): cand = (k, T, fname, (rot, tr), len(ps))
        if collect:
            sk.rot, sk.trans = rot0, tr0; return sorted(allc, key=lambda x: -x[0])
        if cand is None:
            sk.rot, sk.trans = rot0, tr0; return False
        sk.rot, sk.trans = cand[3]
        if self.commit(F.name, kind, cand[1]) is False:
            sk.rot, sk.trans = rot0, tr0; return False
        self._skframe = {**getattr(self, '_skframe', {}), skf.name: cand[3]}
        FD.log(F.name, 'OK', f'revolve {kind} {skf.name} {ang:g} deg about its construction line (face gate {f0} -> {cand[0][0]})',
               frame=cand[2], cells=cand[4], iou=round(float(self.cur_score()), 4))
        return True

    def revolve_alt(self, F, alt):
        """r20 beam: commit one collected revolve candidate (sc, T, fname, frame, ncells)."""
        skf = self.sketch_feat(F); kind = 'cut' if 'cut' in F.name.lower() or 'Cut' in F.type else 'boss'
        sk = skf.sketch; rot0, tr0 = sk.rot, sk.trans; sk.rot, sk.trans = alt[3]
        if self.commit(F.name, kind, alt[1]) is False:
            sk.rot, sk.trans = rot0, tr0; return False
        self._skframe = {**getattr(self, '_skframe', {}), skf.name: alt[3]}
        for x in LOG[::-1]:
            if x['feature'] == F.name: LOG.remove(x); break
        FD.log(F.name, 'OK', f'revolve {kind} {skf.name} about its construction line (beam alt)', frame=alt[2], cells=alt[4], iou=round(float(self.cur_score()), 4))
        return True

    def edge_hints(self):
        """round 18: dumps_v4_edges blend hints (the user's SolidWorks edge dump, rebuild_dump/sw_gen/model.
        parse_edges): per blend feature the edges SW blended (exact BLEND_EDGE items, or sharp edges
        derived from the blend face rails).  Used only to choose which body edges a decoded blend size
        is applied to; no other geometry is taken from them.  R18_EDGEHINTS=0 turns them off."""
        if getattr(self, '_hints', None) is None:
            self._hints = {}
            if os.environ.get('R18_EDGEHINTS', '1') == '1':
                try:
                    sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
                    from sw_gen import model as SWM
                    p = os.path.join(ROOT, 'dumps_v4_edges', self.pname + '.edges.txt')
                    if os.path.exists(p): self._hints = SWM.parse_edges(p)
                except Exception:
                    self._hints = {}
        return self._hints

    def hint_blend(self, F):
        """apply F's decoded blend size on the body edges named by the dumps_v4_edges hints; kept when
        OCC succeeds and the oracle score does not drop by more than 2e-4.  Returns True if applied."""
        H = self.edge_hints().get(F.name)
        bp = DP.blend_params(F)
        if not H or not bp or not bp[1] or self.body is None: return False
        kind, size = bp[0], bp[1] * MM
        lim = 2.5 * bp[1] + 1e-6
        H = [h for h in H if not h[0].startswith('derived') or h[5] <= lim]
        if not H: return False
        body = FD._one(self.body); E = body.edges()
        def d_of(e, h):
            k, s_, e_, m_, L, sep = h
            s_, e_, m_ = (np.array(x) * MM for x in (s_, e_, m_))
            try:
                if np.linalg.norm(s_ - e_) < 1e-6:     # closed: centre (s and m are opposite points) and length
                    bb = e.bounding_box(); c = (np.array(tuple(bb.min)) + np.array(tuple(bb.max))) / 2
                    return float(np.linalg.norm(c - (s_ + m_) / 2)) + (abs(e.length - L * MM) if L else 0.0)
                p0, p1, pm = (np.array(tuple(e.position_at(t))) for t in (0, 1, 0.5))
                return min(np.linalg.norm(p0 - s_) + np.linalg.norm(p1 - e_), np.linalg.norm(p1 - s_) + np.linalg.norm(p0 - e_)) / 2 + \
                       (np.linalg.norm(pm - m_) if not k.startswith('derived') else 0.0)
            except Exception:
                return 1e9
        sel = []
        for h in H:
            tol = 0.05 if not h[0].startswith('derived') else 1.5 * size + 0.05
            ds = [(d_of(e, h), i) for i, e in enumerate(E)]
            dm, i = min(ds) if ds else (1e9, -1)
            if dm <= tol and i not in sel: sel.append(i)
        if not sel: return False
        op = (lambda b, es: b.fillet(size, es)) if kind == 'fillet' else (lambda b, es: b.chamfer(size, None, es))
        v0 = FD.vol(self.body); s0 = self.cur_score()
        split = os.environ.get('R20_HSPLIT', '1') == '1'
        cands = [sel] + ([] if split else ([[i] for i in sel] if len(sel) > 1 else []))
        cur, done = body, 0
        fgate = [None]
        def try_grp(grp):
            nonlocal cur, done, s0
            try:
                Ec = cur.edges()
                es = [min(Ec, key=lambda x: (x.center() - E[i].center()).length) for i in grp]
                if any((a_.center() - E[i].center()).length > 1e-3 for a_, i in zip(es, grp)): return False
                nb = op(cur, es)
                if nb is None or not nb.is_valid or abs(FD.vol(nb) - v0) > 0.05 * v0 + 1: return False
                sc = self.ebody_score(nb) if self.exact else float(self.ref.miou(self.ref.G.inside(nb)))
                if sc is None: return False
                if sc < s0 - 2e-4:
                    # r20: a hinted blend that costs a little IoU is still kept when it reproduces more
                    # decoded XT face patches (the oracle mesh is a tessellation: blends move it by < 1e-3)
                    if not split or sc < s0 - float(os.environ.get('R20_HFTOL', 1.5e-3)): return False
                    if fgate[0] is None: fgate[0] = self.face_matches(cur)
                    fm = self.face_matches(nb)
                    if fm <= fgate[0]: return False
                    fgate[0] = fm
                else: fgate[0] = None
                cur, done, s0 = nb, done + len(grp), sc
                return True
            except Exception:
                return False
        def rec(grp, depth=0):
            # r20: a set OCC cannot blend together is halved (tangent chains stay together more often
            # than with the r18 one-edge-at-a-time fallback), down to single edges
            if self.over() or not grp: return
            if try_grp(grp) or len(grp) == 1: return
            h = len(grp) // 2; rec(grp[:h], depth + 1); rec(grp[h:], depth + 1)
        if split: rec(list(sel))
        else:
            for grp in cands:
                if self.over(): break
                if try_grp(grp) and grp is sel: break
        if not done: return False
        self.body = cur; self.bin = self.ref.G.inside(cur)
        if self.exact: self.resync()
        FD.log(F.name, 'OK' if done >= len(H) else 'PART', f'{kind} {size:g} on dumps_v4_edges hint edges', edges=f'{done}/{len(H)}', iou=round(float(self.cur_score()), 4))
        self._hint_rem = max(0, len(H) - done)
        return 'full' if done >= len(H) else 'part'

    def blend_feature(self, F, mirror=None):
        """r19 forked-blend guard: when an isolated OCC blend crashed during this feature, the partial
        blend (the edges that did not crash) is kept only if it does not lose decoded XT face patches.
        Round 17 skipped such a feature whole (the crash killed the process); R18 kept whatever the
        remaining candidates did, which cost RV23 / side panel ~3 points of faces matched."""
        c0, body0, bin0, MB0, n0 = _CRASHES, self.body, self.bin, (self.MB, self.VB, self.I), len(LOG)
        r = self._blend_feature0(F, mirror)
        if _CRASHES > c0 and self.body is not body0 and body0 is not None and os.environ.get('R19_CRASHGUARD', '1') == '1':
            m1, m0 = self.face_matches(self.body), self.face_matches(body0)
            if m1 < m0 or (m1 == m0 and os.environ.get('R19_CRASHSTRICT', '1') == '1'):
                self.body, self.bin = body0, bin0; self.MB, self.VB, self.I = MB0
                FD.log(F.name, 'INFO', f'forked blend crashed: partial blend dropped (XT faces {m0} -> {m1})')
        return r

    def _blend_feature0(self, F, mirror=None):
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
        hb = None
        if mirror is None:
            try:
                hb = self.hint_blend(F)
                if hb == 'full' or (hb == 'part' and os.environ.get('R18_HINTCONT', '1') != '1'): F.faces = keep; return
                # partial: the replay's own edge search continues on the hinted body (RV22 Fillet1: hints
                # gave 3/5, the face-fit search alone 5/5); kept only if it does not lose decoded XT face
                # patches (RV01 / RV23 lost 15 / 4 % of faces matched when it always continued)
            except Exception as ex:
                FD.log(F.name, 'WARN', f'hint blend failed: {type(ex).__name__}')
        hstate = (self.body, self.bin, len(LOG)) if hb == 'part' else None
        try:
            if F.type == 'Chamfer' and not F.chamfer: F.type = 'Chamfer'
            with self.exact_blend_scoring():
                n0 = len(LOG); super().blend_feature(F, mirror)
                self.small_blend(F, mirror, LOG[n0:])
        finally:
            F.faces = keep
            if hstate is not None and self.body is not hstate[0] and os.environ.get('R18_HINTGUARD', '1') == '1':
                # the continuation may only add the edges the hints name but did not place (RV22: 3/5 by
                # hints + 2 by face fit); adding more blends edges SW did not (RV01: 28.8 -> 13.8 % faces)
                added = 0
                for x in LOG[hstate[2]:]:
                    m_ = re.match(r'(\d+)/', str(x.get('edges') or ''))
                    if x.get('feature') == F.name and m_: added += int(m_.group(1))
                rem = getattr(self, '_hint_rem', 0)
                if added > rem:
                    self.body, self.bin = hstate[0], hstate[1]; del LOG[hstate[2]:]
                    FD.log(F.name, 'INFO', f'face-fit continuation dropped: it added {added} edges, the hints leave {rem}')
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
                if me.over(): return -1.0     # r18: time budget spent: further blend candidates are rejected
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
                    if cands and self.over(): break
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
            for c in sorted(cands, key=lambda c: -c[0]):
                if len(sc2) >= 4 and self.over(): break
                try: sup = self.surf_support('cut', c[1](), n=160)
                except Exception: sup = None
                sc2.append((c[0] + (0.0 if sup is None else sup), c[0], c[1], c[2], dict(c[3], support=sup), sup))
            self._thread_sup = sorted([round(sup, 3) for k, v, t, nb, i, sup in sc2 if sup is not None], reverse=True)[:6]
            cands = [(k, t, nb, dict(i, voxel=v)) for k, v, t, nb, i, sup in sc2 if v >= s0 - 1e-3 and (v > s0 + 1e-6 or (sup or 0) >= 0.8)]
            s0 = -1.0
        cands.sort(key=lambda c: -c[0])
        best = None; ok = None; s00 = s0
        for sc, tool, nb, info in cands[:6]:
            if sc <= s00 + 1e-6: break
            for shrink in (1.0, 0.95, 0.85):   # OCC cuts of near-touching helix turns fail silently: verify on the B-rep
                try:
                    T = tool(shrink); c = self.body.cut(T); dv = FD.vol(self.body) - FD.vol(c)
                    if dv > 0.5 * T.volume * 0.5:
                        best = (sc, T, None, dict(info, shrink=shrink))
                        # r18: commit inside the loop; a candidate whose exact-checked commit fails gives way to the next
                        self._in_thread = self.exact
                        try: ok = self.commit(F.name, 'cut', T, None if s0 < 0 else nb)
                        finally: self._in_thread = False
                        if ok is not False: break
                except Exception:
                    pass
            if best and ok is not False and ok is not None: break
        if best is None: FD.log(F.name, 'SKIP', f'thread: no helix improves the oracle IoU (best surface support {getattr(self, "_thread_sup", None)}, {len(cands)} candidates)'); return
        if ok is False or ok is None: FD.log(F.name, 'FAIL', 'thread: B-rep boolean failed'); return
        FD.log(F.name, 'OK', f'thread pitch {pitch:g} h {h:g} {best[3]}', iou=round(best[0], 4))

    def base_flange(self, F):
        """round 18 sheet metal: a Base-Flange is its sketch extruded by the sheet thickness (decoded
        'Thickness' dim of the Sheet-Metal feature); the extent search picks the side.  Edge flanges and
        bends are not rebuilt."""
        T = sheet_thickness(self.g.d)
        if T is None: FD.log(F.name, 'SKIP', 'base flange: no decoded sheet thickness'); return
        e = self.g.ec.setdefault(F.name, {}); e.setdefault('D_mm', [T]); e.setdefault('end_code_dir1', None)
        if not e.get('sketch'):   # flat-pattern helper sketches (Bend-Lines, Bounding-Box) come later in id order: skip them
            c = [f for f in self.g.d['features'] if f['type'] == 'Sketch' and f['id'] < F.id and not re.match(r'Bend-Lines|Bounding-Box', f['name'])
                 and f['name'] not in self.g.used and self.part.by_name.get(f['name']) is not None and getattr(self.part.by_name[f['name']].sketch, 'segs', None)]
            if c: e['sketch'] = max(c, key=lambda f: f['id'])['name']
        self.extrude_feature(F)

    def edge_flange(self, F):
        """r19 sheet metal: an Edge-Flange is rebuilt as bend + flat flange on a thin side face of the
        sheet: the side face (one side = the decoded thickness T) revolved by the decoded angle (D4)
        about an axis along its long edge at bend radius R (Sheet-Metal 'R..' dim) from the inner
        surface, then extruded by the decoded length (D7, also L-R-T for outer-virtual-sharp lengths).
        The edge is not decoded: every thin side face, both bend sides and both rotation senses are
        scored against the oracle; the best is kept while it improves the score (an Edge-Flange can
        hold several edges, at most 4 here)."""
        T = sheet_thickness(self.g.d)
        dd = {}
        for f in self.g.d['features']:
            if f['name'] == F.name: dd = {dn: dv for dn, dv in f.get('dims') or []}
        L = num(dd.get('D7')) if dd.get('D7') else None
        ang = num(dd.get('D4')) if dd.get('D4') else 90.0
        R = next((num(dv) for f in self.g.d['features'] if f['type'] == 'Sheet-Metal' for dn, dv in f.get('dims') or [] if str(dv).startswith('R') and num(dv)), None)
        if T is None or L is None: FD.log(F.name, 'SKIP', 'edge flange: no decoded thickness / length'); return
        if R is None: R = T
        from OCP.BRepAdaptor import BRepAdaptor_Surface
        from OCP.GeomAbs import GeomAbs_Plane
        from build123d import Axis as _Ax
        done = 0; allc = []
        for rnd in range(4):
            best = None; s0 = self.cur_score()
            for fc in self.body.faces():
                if self.over() and best is not None: break
                ad = BRepAdaptor_Surface(fc.wrapped)
                if ad.GetType() != GeomAbs_Plane or len(fc.edges()) < 4: continue
                E = [e for e in fc.edges() if e.geom_type in ('LINE', 'Line') or getattr(e.geom_type, 'name', '') == 'LINE']
                short = [e for e in E if abs(e.length - T) < 1e-3]; long_ = [e for e in E if e.length > T + 1e-3]
                if len(short) < 2 or not long_: continue
                c = np.array(tuple(fc.center())); sN = np.array(tuple(fc.normal_at(fc.center())))
                lg = max(long_, key=lambda e: e.length)
                u = np.array(tuple(lg.end_point() - lg.start_point())); u /= np.linalg.norm(u)
                v = np.cross(sN, u); v /= max(np.linalg.norm(v), 1e-12)
                ext = [float(np.dot(np.array(tuple(p_)) - c, v)) for e in E for p_ in (e.start_point(), e.end_point())]
                if abs(max(ext) - min(ext) - T) > 1e-3: continue   # the face is one sheet thickness wide
                c = c + v * (max(ext) + min(ext)) / 2
                for vs in (1, -1):
                    ax_o = c + vs * v * (T / 2 + R)
                    for sg in (1, -1):
                        A = _Ax(tuple(ax_o), tuple(u))
                        for Ln in sorted({L, max(L - R - T, 0.1), max(L - T, 0.1), max(L - R, 0.1)}):   # r20: + L-R (inner virtual sharp)
                            try:
                                bend = revolve(fc, A, sg * ang)
                                end = fc.rotate(A, sg * ang)
                                en = np.array(tuple(end.normal_at(end.center())))
                                if en @ (np.array(tuple(end.center())) - np.array(tuple(bend.center()))) < 0: en = -en
                                fl = extrude(end, Ln, dir=tuple(en))
                                tool = bend.fuse(fl).clean()
                                sc, _ = self.tool_score('boss', tool)
                            except Exception:
                                continue
                            if os.environ.get('R20_DBG'): print('EFL', round(sc, 5), round(s0, 5), round(fc.area, 3), vs, sg, Ln, file=sys.stderr)
                            if best is None or sc > best[0]: best = (sc, tool, f'side {round(fc.area, 2)} mm2, bend {"+" if vs > 0 else "-"}{"cw" if sg > 0 else "ccw"}, L={Ln:g}')
                            allc.append((sc, tool, fc, u, lg, Ln, vs, sg))
            if (best is None or best[0] <= s0 + 1e-5) and os.environ.get('R20_EFTRIM', '1') == '1' and allc:
                # r20: a flange along part of its edge (TBC_Top Edge-Flange1: y 2..10 of a 20 mm side):
                # the best whole-edge tools of the two best side faces are cut to a slab [a, b] along the
                # edge, a and b on a tenth-of-the-edge grid
                tb = self._ef_trim(allc, s0)
                if tb is not None and (best is None or tb[0] > best[0]): best = tb
            allc = []
            if best is None or best[0] <= s0 + 1e-5: break
            if self.commit(F.name, 'boss', best[1]) is False: break
            done += 1; FD.log(F.name, 'OK', f'edge flange {done}: {best[2]}, angle {ang:g}, R {R:g}, T {T:g}', iou=round(float(self.cur_score()), 4))
        if not done: FD.log(F.name, 'FAIL', 'edge flange: no side face / bend gives an IoU gain')
        self._flanged = bool(done)   # the EdgeBend sub-features that follow belong to this flange

    def _ef_trim(self, allc, s0, n=10):
        from build123d import Box, Pos
        seen = []; best = None
        for sc, tool, fc, u, lg, Ln, vs, sg in sorted(allc, key=lambda x: -x[0]):
            if any(fc is f_ for f_ in seen): continue
            if len(seen) >= int(os.environ.get("R20_EFTF", 4)): break
            seen.append(fc)
            p0 = np.array(tuple(lg.start_point())); Lg = lg.length
            bb = tool.bounding_box(); big = 4 * max(bb.size.X, bb.size.Y, bb.size.Z) + 10
            for i in range(n):
                for j in range(i + 1, n + 1):
                    if i == 0 and j == n: continue
                    if self.over(): return best
                    a, b = Lg * i / n, Lg * j / n
                    try:
                        # slab of thickness b-a along u, centred at p0 + u (a+b)/2
                        from build123d import Plane as _Pl
                        pl = _Pl(origin=tuple(p0 + u * (a + b) / 2), z_dir=tuple(u))
                        slab = pl * Box(big, big, b - a)
                        t2 = tool.intersect(slab)
                        if isinstance(t2, (list, tuple)) or type(t2).__name__ == 'ShapeList':
                            t2 = Compound(list(t2)) if len(t2) else None
                        if t2 is None or t2.volume < 1e-6: continue
                        sc2, _ = self.tool_score('boss', t2)
                    except Exception as ex:
                        if os.environ.get('R20_DBG'): print('EFTRIM', repr(ex)[:200], file=sys.stderr)
                        continue
                    if os.environ.get('R20_DBG'): print('EFT', round(sc2, 5), round(s0, 5), a, b, file=sys.stderr)
                    if best is None or sc2 > best[0]:
                        best = (sc2, t2, f'side {round(fc.area, 2)} mm2 trimmed to {a:.2f}..{b:.2f} of {Lg:.2f} mm, bend {"+" if vs > 0 else "-"}{"cw" if sg > 0 else "ccw"}, L={Ln:g}')
        return best if best is not None and best[0] > s0 + 1e-5 else None

    def gear_dims(self):
        dd = {}
        for f in self.g.d['features']:
            for dn, dv in f.get('dims') or []: dd.setdefault(f['name'], {})[dn] = num(dv)
        return dd

    def gear_feature(self, F):
        """r19 Toolbox spur gear: the sketches of a Toolbox gear hold no decoded geometry, but its
        keyword dims define it (BasProSke Diameter / Thickness, TooCutSke Base / Root / Pitch dia,
        TeethCuts Num_teeth, HoldingSke Backlash, BorSke Diameter).  The gear is rebuilt as a standard
        involute profile extruded by the thickness; the axis, the start offset and the tooth phase are
        chosen against the oracle; the bore is cut if it improves the score."""
        dd = self.gear_dims(); bp, tc, tp = dd.get('BasProSke', {}), dd.get('TooCutSke', {}), dd.get('TeethCuts', {})
        hs = dd.get('HoldingSke', {})
        z = int(round(tp.get('Num_teeth') or hs.get('Num_teeth') or 0)); ra = (bp.get('Diameter') or 0) / 2; th = bp.get('Thickness') or hs.get('Thickness')
        rb = (tc.get('Base_dia') or 0) / 2; rr = (tc.get('Root_dia') or 0) / 2; rp = (tc.get('Pitch_dia') or 0) / 2
        if not (z >= 3 and ra > 0 and th and rp > 0):
            FD.log(F.name, 'SKIP', 'gear: Toolbox dims incomplete'); return False
        if rb <= 0: rb = rp * math.cos(math.radians(20))
        if rr <= 0: rr = rp - 1.25 * (2 * rp / z)
        bl = hs.get('Backlash') or 0.0
        inv = lambda a: math.tan(a) - a
        ap = math.acos(min(1.0, rb / rp)); psi = math.pi / (2 * z) - bl / (2 * rp)
        def half(r):
            if r <= rb: return psi + inv(ap)
            return psi + inv(ap) - inv(math.acos(rb / r))
        rs = [max(rr, rb) + (ra - max(rr, rb)) * k / 12 for k in range(13)]
        pts = []
        for k in range(z):
            c = 2 * math.pi * k / z
            fl = [(r, half(r)) for r in rs if half(r) > 0]
            if not fl: continue
            if rr < rb: pts.append((rr * math.cos(c - fl[0][1]), rr * math.sin(c - fl[0][1])))
            pts += [(r * math.cos(c - h), r * math.sin(c - h)) for r, h in fl]
            pts += [(r * math.cos(c + h), r * math.sin(c + h)) for r, h in fl[::-1]]
            if rr < rb: pts.append((rr * math.cos(c + fl[0][1]), rr * math.sin(c + fl[0][1])))
        from build123d import Polyline, make_face, Rot, Pos, Cylinder
        try:
            prof = make_face(Polyline(*pts, close=True))
            G0 = extrude(prof, th)
        except Exception as ex:
            FD.log(F.name, 'FAIL', f'gear profile: {type(ex).__name__}'); return False
        best = None
        for axn, rot in (('z', Rot(0, 0, 0)), ('x', Rot(0, 90, 0)), ('y', Rot(-90, 0, 0))):
            for off in (0.0, -th, -th / 2):
                for ph in range(4):
                    G = rot * Pos(0, 0, off) * Rot(0, 0, ph * 90.0 / z) * G0
                    try: sc, _ = self.tool_score('boss', G)
                    except Exception: continue
                    if best is None or sc > best[0]: best = (sc, G, f'axis {axn}, offset {off:g}, phase {ph}/4 pitch', rot, off)
        if best is None or self.commit(F.name, 'boss', best[1]) is False:
            FD.log(F.name, 'FAIL', 'gear: no placement'); return False
        msg = f'Toolbox gear z={z}, OD {2 * ra:g}, root {2 * rr:g}, base {2 * rb:g}, pitch {2 * rp:g}, width {th:g}: {best[2]}'
        FD.log(F.name, 'OK', 'gear blank (' + msg + ')', iou=round(float(self.cur_score()), 4))
        for nm in ('ToothCut', 'TeethCuts'):
            if nm in dd or any(f['name'] == nm for f in self.g.d['features']): FD.log(nm, 'OK', 'teeth built with the Toolbox gear profile')
        self._gear = (best[3], best[4], th)
        bd = (dd.get('BorSke') or {}).get('Diameter')
        if bd:
            rot, off = best[3], best[4]
            Cb = rot * Pos(0, 0, off + th / 2) * Cylinder(bd / 2, th + 2)
            self._gear_bore = self.try_tool('Bore', 'cut', Cb, f'gear bore dia {bd:g}')
        return True

    def _run_one(self, f):
        if f.name in ('Base-Revolve',) and self.body is None and 'TooCutSke' in self.gear_dims() and self.sketch_feat(f) is None:
            self._gear_mode = self.gear_feature(f); return
        if getattr(self, '_gear_mode', False) and f.name in ('ToothCut', 'TeethCuts', 'Bore'): return
        if f.type == 'Edge-Flange' and self.body is not None: return self.edge_flange(f)
        if f.type == 'EdgeBend':   # the bend sub-feature of an Edge-Flange: built with it
            if getattr(self, '_flanged', None): FD.log(f.name, 'OK', 'bend built with its edge flange')
            else: FD.log(f.name, 'SKIP', 'edge flange not rebuilt')
            return
        t = f.type; nm = f.name
        if t in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion', 'Cut', 'Boss', 'ICE', 'Extrude'): self.extrude_feature(f)
        elif t in ('Revolve', 'Cut-Revolve', 'RevCut'): self.revolve_feature(f)
        elif t in ('Base-Flange', 'SMBaseFlange'): self.base_flange(f)
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
        if getattr(self, '_beam_on', False) and self.exact: return self._run_beam(feats, prog, skip, rin0)
        for k, f in enumerate(feats): self._step(k, f, prog, skip, rin0)
        return self.body

    # ---- r19 beam search over the extrude region / extent choices
    def clone(self):
        import copy
        c = copy.copy(self)
        c.bin = self.bin.copy(); c.tools = dict(self.tools); c.choice = dict(self.choice); c.order = list(self.order)
        c.cutvox = dict(self.cutvox); c.cutman = dict(self.cutman); c.ftime = dict(self.ftime); c._mfc = {}
        c._skframe = dict(getattr(self, '_skframe', {})); c._log = list(getattr(self, '_log', []))
        return c

    def _sketches(self):
        return [f.sketch for f in self.part.features if getattr(f, 'sketch', None) is not None]

    def _enter(self):
        """make the shared globals (LOG, sketch frames) this state's."""
        LOG[:] = self._log
        for f in self.part.features:
            sk = getattr(f, 'sketch', None)
            if sk is None: continue
            if not hasattr(sk, '_r19_frame0'): sk._r19_frame0 = (sk.rot, sk.trans)
            sk.rot, sk.trans = self._skframe.get(f.name, sk._r19_frame0)
            if hasattr(f, '_frames'): del f._frames   # frames depend on this state's body planes

    def _leave(self):
        self._log = list(LOG)

    def beam_key(self, final=False):
        """pruning / final score: exact oracle IoU plus R19_FW x the fraction of decoded XT face
        patches the body reproduces (decode-only face gate)."""
        if self.body is None: return -1.0
        if getattr(self, '_bk', None) and self._bk[0] is self.body and self._bk[1] == final: return self._bk[2]
        nx = max(1, len(self.xt_fa()))
        if final:
            i = (self.MB ^ self.ref.M).volume() if self.MB is not None else 0.0
            io = i / max(self.VB + self.ref.M.volume() - i, 1e-12)
        else:
            # pruning: material outside the final body costs R19_EXW (< 1) of the material found: a later
            # cut can still remove it, while missing material can only come from a later boss
            io = (self.I - float(os.environ.get('R19_EXW', 0.5)) * max(self.VB - self.I, 0.0)) / max(self.VT, 1e-12)
        k = float(io) + float(os.environ.get('R19_FW', 0.05)) * self.face_matches(self.body) / nx
        self._bk = (self.body, final, k); return k

    def _run_beam(self, feats, prog, skip, rin0):
        B = int(os.environ.get('R19_BEAM', 3))
        self._log = list(LOG); self._skframe = {}
        states = [self]
        for k, f in enumerate(feats):
            if time.time() > self._pdead and len(states) > 1:   # out of time: the best state continues greedily
                states = [max(states, key=lambda s: s.beam_key())]
                FD.log('beam', 'INFO', f'part budget: beam collapsed at {f.name}')
            ext = f.type in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion', 'Cut', 'Boss', 'ICE', 'Extrude') and len(states) * 0 == 0
            rev = f.type in ('Revolve', 'Cut-Revolve', 'RevCut') and os.environ.get('R20_BEAMREV', '1') == '1'
            if getattr(self, '_beam_upto', None) is not None and k > self._beam_upto: ext = rev = False   # r20: no branching past greedy's last failure
            kids = []
            for s in states:
                c0 = s.clone(); c0._enter(); c0._last_alts = None
                c0._step(k, f, prog, skip, rin0); c0._leave(); kids.append(c0)
                if rev and B > 1 and self.exact:
                    try:
                        c1 = s.clone(); c1._enter()
                        MT = s._sufm[k + 1] if s._sufm[k + 1] is not None else s.ref.M
                        if MT is not c1.MT: c1.set_target(MT)
                        skf = c1.sketch_feat(f); kd = 'cut' if 'cut' in f.name.lower() or 'Cut' in f.type else 'boss'
                        ang = next((math.degrees(v) for kk, v in f.dims.items() if kk.startswith('D1@') and v < 7), 360.0) or 360.0
                        alts = c1.revolve_axis_fallback(f, skf, kd, ang, skf.sketch.rot, skf.sketch.trans, collect=True) if skf is not None else []
                        c1._leave()
                    except Exception: alts = []
                    for alt in alts[:int(os.environ.get('R20_RK', 2))]:
                        c = s.clone(); c._enter()
                        if self.exact:
                            MT = s._sufm[k + 1] if s._sufm[k + 1] is not None else s.ref.M
                            if MT is not c.MT: c.set_target(MT)
                        try: c.revolve_alt(f, alt)
                        except Exception as ex: FD.log(f.name, 'ERROR', f'beam revolve alt: {type(ex).__name__}')
                        c._leave()
                        if c.body is not s.body: kids.append(c)
                la = c0._last_alts
                if not ext or B <= 1 or not la or la[0] != f.name: continue
                for alt in la[6][1:]:
                    if alt is None: continue
                    c = s.clone(); c._enter()
                    if self.exact:
                        MT = s._sufm[k + 1] if s._sufm[k + 1] is not None else s.ref.M
                        if MT is not c.MT: c.set_target(MT)
                    try: c.commit_extrude(f, la[1], la[2], la[3], la[4], la[5], alt, 'beam alt')
                    except Exception as ex: FD.log(f.name, 'ERROR', f'beam alt: {type(ex).__name__}')
                    c._leave()
                    if c.body is not s.body: kids.append(c)
            if len(kids) > 1:
                u = {}
                for c in kids:
                    key = (round(c.VB, 4), round(c.I, 4))
                    if key not in u or c.beam_key() > u[key].beam_key(): u[key] = c
                states = sorted(u.values(), key=lambda c: -c.beam_key())[:B]
            else: states = kids
        best = max(states, key=lambda s: s.beam_key(final=True))
        best._enter()
        if best is not self: self.__dict__.update(best.__dict__)
        FD.log('beam', 'INFO', f'beam {B}: final key {best.beam_key(final=True):.4f}')
        return self.body

    def _step(self, k, f, prog, skip, rin0):
        if True:
            self.ref.rin = rin0 if self._suf[k + 1] is None else (rin0 | self._suf[k + 1])
            if self.exact:
                MT = self._sufm[k + 1] if self._sufm[k + 1] is not None else self.ref.M
                if MT is not self.MT: self.set_target(MT)
            if prog:
                with open(prog, 'w') as fh: fh.write(f.name)
            if f.name in skip:
                FD.log(f.name, 'SKIP', 'OCC crashed (segfault) on this feature in an earlier attempt'); return
            prev = self.body
            # r19: before a pattern / mirror / blend / thread (single OCC calls that can outlast every budget:
            # bbb ant servo CirPattern1 hung from 60 s to the 600 s kill, before the first timed checkpoint)
            self.checkpoint(force=any(k_ in f.type for k_ in ('Pattern', 'Mirror', 'Fillet', 'Chamfer', 'Thread')))
            self.checkpoint()   # before the feature too: one OCC call can outlast every budget (helix sweeps)
            self._mfc = {}
            # r18 hard per-feature cap: SIGALRM raises in the Python layer once the feature has run 3x its
            # budget (a single OCC call still finishes first); the feature is logged ERROR and skipped
            import signal
            def _alarm(*a, me=self):
                me._deadline = 0.0          # every search stops at its next budget check
                try: signal.alarm(5)        # and keep raising: loops that swallow exceptions still end
                except Exception: pass
                raise TimeoutError('feature time cap')
            cap = int(3 * float(os.environ.get('R18_FBUDGET', 240)))
            try: signal.signal(signal.SIGALRM, _alarm); signal.alarm(cap)
            except Exception: pass
            t_f = time.time(); self._deadline = t_f + float(os.environ.get('R18_FBUDGET', 240)); self._budget_hit = False
            # r18 part budget: past R18_PBUDGET s every feature keeps only its first workable candidate
            self._deadline = min(self._deadline, max(t_f + 5.0, self._pdead))
            try:
                self._run_one(f)
            except Exception as ex:
                FD.log(f.name, 'ERROR', f'{type(ex).__name__}: {str(ex)[:120]}')
                if self.exact and self.body is not prev: self.resync()
            try: signal.alarm(0)
            except Exception: pass
            self.ftime[f.name] = round(time.time() - t_f, 1)
            self.checkpoint()
            if self._budget_hit: FD.log(f.name, 'INFO', f'per-feature time budget hit ({self.ftime[f.name]} s): search cut short')
            if self.body is not None and self.body is not prev and not self.body.is_valid:
                from OCP.ShapeFix import ShapeFix_Shape
                sf = ShapeFix_Shape(self.body.wrapped); sf.Perform()
                fx = Compound(sf.Shape())
                if fx.is_valid: self.body = fx


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
    bp = os.path.join(out_dir, 'breps' + BSUF, src + '.brep')
    if not os.path.exists(os.path.join(ROOT, SRC, src + '.SLDPRT')) or not os.path.exists(os.path.join(DO.DEC, src + '.json')):
        return dict(iou=None, note=f'mirror source {src} not in {SRC}/')
    if not os.path.exists(bp):
        r = run_part(src, out_dir)
        if SRC != 'revdev':
            try: json.dump(r, open(os.path.join(out_dir, 'results' + BSUF, src + '.json'), 'w'), indent=1, default=float)
            except Exception: pass
    if not os.path.exists(bp): return dict(iou=0.0, note=f'source {src} not rebuilt')
    sc, n, d = MD.fit_plane(src, part)
    body = import_brep(bp).mirror(Plane(origin=tuple(n * d), z_dir=tuple(n)))
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy   # deep copy: the mirrored shape can carry stale/missing triangulation
    body = type(body)(BRepBuilderAPI_Copy(body.wrapped, True, False).Shape())
    os.makedirs(os.path.join(out_dir, 'breps' + BSUF), exist_ok=True)
    try: export_brep(body, os.path.join(out_dir, 'breps' + BSUF, part + '.brep'))
    except Exception: pass
    T = DL.triangles(os.path.join(ROOT, SRC, part + '.SLDPRT')); own_T = T is not None and len(T) > 12
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
        if oe[0] is None:   # r18: mirrored body whose fine tessellation does not close (RV24): sewn / repaired manifold
            try:
                ma, mb = OracleReplay.repair_mf(body), XI.as_manifold(T)
                if ma is not None and mb is not None:
                    i = (ma ^ mb).volume(); oe = (i / (ma.volume() + mb.volume() - i), 'manifold (repaired)')
            except Exception: pass
        if oe[0] is None:   # r19: the source body's mesh, reflected (the reflection is exact; RV24's mirrored B-rep never meshes closed)
            try:
                # r19: the source body's manifold, reflected (exact); the reflected B-rep can fail to mesh closed
                sb = import_brep(bp); ms = OracleReplay.mf(sb) or OracleReplay.repair_mf(sb); mb = XI.as_manifold(T)
                if ms is not None and mb is not None:
                    t_ = tuple(map(float, n * d)); ma = ms.translate(tuple(-x for x in t_)).mirror(tuple(map(float, n))).translate(t_)
                    i = (ma ^ mb).volume(); oe = (i / (ma.volume() + mb.volume() - i), 'manifold (reflected source manifold)')
            except Exception: pass
    if oe[0] is None and own_T is False:
        # r19: the oracle is the source's mesh reflected and the body the source's body reflected: the IoU
        # is the source's (exact reflection), as scored in the source's own result
        try:
            rs = json.load(open(os.path.join(out_dir, 'results' + BSUF, src + '.json')))
            if rs.get('oracle_iou') is not None: oe = (rs['oracle_iou'], 'source oracle IoU (exact reflection; ' + str(rs.get('oracle_iou_method')) + ')')
        except Exception: pass
    mname = next((f['name'] for f in json.load(open(os.path.join(DO.DEC, part + '.json')))['features'] if f['type'].endswith('_Mirrored')), 'MirrorStock')
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], oracle=None, derived_from=src,
                oracle_iou=round(float(oe[0]), 4) if oe[0] is not None else None, oracle_iou_method=oe[1],
                log=[dict(feature=mname, status='OK', msg=f'mirror of the {src} rebuild')],
                mirror=dict(normal=n.tolist(), offset_mm=d, vertex_fit=round(sc, 4)), volume=round(body.volume, 1),
                seconds=round(time.time() - t0, 1))


def beam_upto(feats, log, score=1.0):
    """r20 beam pruning: index of the last solid feature greedy logged FAIL (or a low-gain PART
    revolve/extrude); the beam branches only up to there.  None (no beam) when greedy failed nothing.
    R20_BEAMALL=1 restores the r19 behaviour (branch everywhere, every part under 0.995)."""
    if os.environ.get('R20_BEAMALL') == '1': return len(feats)
    bad = {x['feature'] for x in log if x.get('status') == 'FAIL'}
    idx = [i for i, f in enumerate(feats) if f.name in bad]
    if idx: return max(idx)
    # nothing failed but the greedy body is far off (RV11 0.929: the r19 beam gained 0.027): branch everywhere
    return len(feats) if score < float(os.environ.get('R20_BEAMLOW', 0.95)) else None

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
            if time.time() - t0 > float(os.environ.get('R18_PBUDGET', 1e9)): passes.append('part budget: no further pass'); break
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
        beam = None
        if os.environ.get('R19_BEAM', '3') not in ('0', '1') and rb.exact and sco(rb) < 0.995 and beam_upto(rb.part.features, log, sco(rb)) is not None \
                and time.time() - t0 < float(os.environ.get('R19_BEAMSTART', 0.5)) * float(os.environ.get('R18_PBUDGET', 1e9)):
            # r19: beam search over the extrude choices, scored by the final oracle + decode-only face gate;
            # kept only if its final key beats the greedy result's
            # the greedy result is the checkpoint while the beam runs (a run_all kill scores it, not a beam state)
            try: LOG[:] = log; rb._pckpt = 0; rb._ckt = 0; rb.checkpoint(force=True)
            except Exception: pass
            LOG.clear(); R.LOG.clear()
            try:
                rb3 = OracleReplay(part, ref, rb.lookahead, rb.lookahead_m); rb3._beam_on = True
                rb3._beam_upto = beam_upto(rb.part.features, log, sco(rb))
                rb3.checkpoint = lambda *a, **k: None
                rb3._pdead = min(rb3._pdead, t0 + 0.9 * float(os.environ.get('R18_PBUDGET', 1e9)))   # the look-ahead the kept pass used
                b3 = body_solid(rb3.run())
                k0 = rb.beam_key(final=True) if rb.body is not None else -1; k3 = rb3.beam_key(final=True) if b3 is not None else -1
                beam = dict(greedy_key=round(k0, 4), beam_key=round(k3, 4), beam_oracle=round(sco(rb3), 4), kept=bool(k3 > k0 + 1e-4))
                if k3 > k0 + 1e-4: rb, body, log = rb3, b3, LOG[:]
            except Exception as ex:
                beam = dict(error=repr(ex)[:200], tb=traceback.format_exc()[-800:])
            LOG[:] = log
    if body is None: return dict(iou=0.0, note='no body', oracle=ref.source, log=LOG[:])
    os.makedirs(os.path.join(out_dir, 'breps' + BSUF), exist_ok=True)
    try: export_brep(body, os.path.join(out_dir, 'breps' + BSUF, part + '.brep'))
    except Exception: pass
    b = compare(body, part, ref.T) if SRC == 'revdev' else None
    st = {}
    for x in LOG: st[x['status']] = st.get(x['status'], 0) + 1
    import exact_iou as XI
    try:
        BT = XI.mesh_of(body); oe = XI.exact_iou(BT, ref.T); sd = XI.surf_dist(BT, ref.T, n=int(os.environ.get('R18_SDN', 8000)))
    except Exception as ex:
        oe, sd = (None, repr(ex)[:80]), {}
    if oe[0] is None:   # r19: per-solid repaired manifold (multi-solid bodies touching along an edge)
        try:
            ma, mb = OracleReplay.repair_mf(body), XI.as_manifold(ref.T)
            if ma is not None and mb is not None:
                i = (ma ^ mb).volume(); oe = (i / (ma.volume() + mb.volume() - i), 'manifold (repaired)')
        except Exception: pass
    if oe[0] is None and rb.exact and getattr(rb, 'MB', None) is not None and os.environ.get('R20_TRACKMF', '1') == '1':
        # r20: the body's own tessellation does not close (RV23: 130 open / 93 non-manifold mesh edges on
        # faces left by fuzzy booleans) but the exact track followed it with manifold booleans of the same
        # tools: that manifold is scored when its volume agrees with the B-rep volume within 0.5 %
        try:
            mv = rb.MB.volume()
            if abs(mv - body.volume) <= 5e-3 * abs(body.volume):
                i = (rb.MB ^ XI.as_manifold(ref.T)).volume(); oe = (i / (mv + ref.M.volume() - i), 'exact-track manifold (B-rep mesh open)')
        except Exception: pass
    vox = round(float(ref.miou(ref.G.inside(body) if rb.exact else rb.bin)), 4)
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], iou_method=b and b[3], oracle=ref.source,
                oracle_iou=round(float(oe[0]), 4) if oe[0] is not None else vox, oracle_iou_method=oe[1] if oe[0] is not None else 'voxel (open oracle mesh)',
                oracle_iou_vox=vox,
                oracle_surf=dict((k, round(v, 4)) for k, v in sd.items()), exact_track=rb.exact,
                volume=round(body.volume, 1), oracle_volume=round(ref.V, 1),
                ops=st, seconds=round(time.time() - t0, 1), passes=passes, beam=beam, feature_seconds=getattr(rb, 'ftime', {}),
                log=[{k: (v if isinstance(v, (int, float, str, type(None))) else str(v)) for k, v in x.items()} for x in LOG])


def score_partial(part, pjson, out_dir=HERE):
    """r18: result for a part the run_all timeout killed, from its last checkpoint (R18_PARTIAL)."""
    from build123d import import_brep
    import exact_iou as XI, shutil
    P = json.load(open(pjson)); bp = pjson[:-5] + '.brep'
    body = import_brep(bp); ref = oracle_for(part)
    try: oe = XI.exact_iou(XI.mesh_of(body), ref.T) if ref is not None else (None, None)
    except Exception: oe = (None, None)
    if oe[0] is None and ref is not None:
        try: ref.init_points(); oe = (float(ref.miou(ref.G.inside(body))), 'voxel (open oracle mesh)')
        except Exception: pass
    os.makedirs(os.path.join(out_dir, 'breps' + BSUF), exist_ok=True)
    shutil.copy(bp, os.path.join(out_dir, 'breps' + BSUF, part + '.brep'))
    st = {}
    for x in P['log']: st[x['status']] = st.get(x['status'], 0) + 1
    return dict(iou=None, oracle=ref.source if ref is not None else None, oracle_iou=round(float(oe[0]), 4) if oe[0] is not None else P.get('oracle_iou_exact_track'),
                oracle_iou_method=oe[1], ops=st, log=P['log'], feature_seconds=P.get('ftime'), note='timeout: last checkpoint body (partial)')


def main(sel):
    os.makedirs(os.path.join(HERE, 'breps' + BSUF), exist_ok=True)
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
