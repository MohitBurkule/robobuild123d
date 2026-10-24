#!/usr/bin/env python3
"""Round 15: decode-only feature replay driven by an in-file oracle.

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
    path = os.path.join(ROOT, 'revdev', part + '.SLDPRT')
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
        T = DL.triangles(os.path.join(ROOT, 'revdev', twin + '.SLDPRT'))
        if T is None or len(T) <= 12: continue
        sc, n, d = MD.fit_plane(part, twin)
        if sc < 0.95: continue
        T = MD.reflect(T.reshape(-1, 3), n, d).reshape(-1, 3, 3)
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
    for j, e in enumerate(sk['entities']):   # construction lines (revolve axes)
        if e.get('flag') == 0 and e['type'] == 'line' and e.get('start') and e.get('end'):
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
    def __init__(self, part_name, ref):
        self.pname = part_name
        with contextlib.redirect_stdout(io.StringIO()):
            self.g = DO.GRebuild()
        self.part = to_part(self.g)
        self.ref = ref; self.body = None
        self.bin = np.zeros(int(np.prod(ref.G.n)), bool)
        self.tools = {}; self.choice = {}; self.order = []

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
        if code in (None, 0) and D: c1.append((-D, D))
        if code in (None, 1) or (kind == 'cut' and code is None): c1.append((0, BIG))
        if code == 9: c1.append((-BIG, BIG))
        if code in (None, 2, 3, 4, 5, 7):
            c1 += [(0, s) for s in fw[:12]]
            if code == 5 and D: c1 += [(0, s + k * D) for s in offs for k in (1, -1) if s + k * D > 1e-4]
        if not c1 and D is None: c1 = [(0, s) for s in fw[:12]] + [(0, BIG)]
        c1 = list(dict.fromkeys((round(a, 4), round(b, 4)) for a, b in c1))
        c2 = [None]
        if code2 is not None and code not in (6, 9):
            c2 = [None] + ([(-D2, 0)] if D2 else []) + ([(-BIG, 0)] if code2 in (1, 9) else [])
        return [[iv1] + ([iv2] if iv2 else []) for iv1 in c1 for iv2 in c2]

    def xt_points(self):
        if getattr(self, '_xtp', None) is None:
            import mirror_derived as MD
            from scipy.spatial import cKDTree
            P = MD.xt_vertices(self.pname); self._xtp = cKDTree(P)
            self._xtplanes = [(np.array(x['params']['normal'], float), np.array(x['params']['point']) * MM)
                              for x in self.g.faces if x['surface_type'] == 'plane' and 'normal' in (x.get('params') or {})]
        return self._xtp

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
        return float(np.mean(d < 2e-3))

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
            for n, o in self._xtplanes:
                if abs(abs(n @ Z) - 1) < 1e-6: offs.add(round(float(o @ Z), 4))
            for off in offs:
                tr = tuple(Z * off / MM)
                if nm == 'decoded' and abs(off - float(np.dot(tr0, Z)) * MM) < 1e-6: tr = tr0
                cand.append((rot, tr, f'{nm}@{off:g}' if not (nm == 'decoded' and tr is tr0) else 'decoded'))
        uniq = []
        for c in cand:
            if not any(np.allclose(np.array(c[0]), np.array(u[0])) and np.allclose(c[1], u[1], atol=1e-9) for u in uniq): uniq.append(c)
        sc = [self.reg_score(sk, r, t) for r, t, _ in uniq]
        dec = 0
        order = [dec] + [i for i in sorted(range(len(uniq)), key=lambda i: -sc[i]) if i != dec and sc[i] >= max(0.2, sc[dec] - 1e-9)][:4]
        if len(order) == 1:   # nothing registers (revolve profiles: XT vertices only on the axis): try the plain default planes
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
        s0 = self.score(self.bin)
        best = None; ncand = 0; frames = self.frames(skf)
        for fi, (rot, tr, fname) in enumerate(frames):
            if fi == 1 and best is not None and best[0] > s0 + 1e-6 and best[5] >= 0.9: break
            sk.rot, sk.trans = rot, tr
            cells = FD.sketch_cells(skf)
            if not cells: continue
            origin = np.array(sk.trans) * MM; n0 = np.array(sk.normal, float)
            percell = [None] * len(cells)     # best (gain, n, ivs, idx) per cell over all candidates
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
        sk.rot, sk.trans = rot0, tr0
        if best is None:
            FD.log(F.name, 'FAIL', 'no cells selected', sketch=skf.name, cand=ncand); return
        sc, fname, sel, nb, nc, q, how, fr, ov = best
        sk.rot, sk.trans = fr
        sols = [x for c, n, ivs in sel for lo, hi in ivs for x in self.prism([c], n, lo, hi)]
        T = sols[0] if len(sols) == 1 else sols[0].fuse(*sols[1:]).clean()
        self.commit(F.name, kind, T, None, ov)
        ivs_s = sorted({(round(lo, 3), round(hi, 3), tuple(np.round(n, 3))) for c, n, ivs in sel for lo, hi in ivs})
        self.choice[F.name] = dict(kind=kind, sketch=skf.name, frame=fname, how=how, cells=f'{len(sel)}/{nc}', ivs=[list(x) for x in ivs_s], code=code, D=D)
        FD.log(F.name, 'OK', kind, sketch=skf.name, frame=fname, how=how, code=code, D=D, cells=f'{len(sel)}/{nc}', ivs=str(ivs_s[:4]),
               cand=ncand, iou=round(float(self.score(self.bin)), 4))

    def commit(self, name, kind, T, B=None, out=0.0):
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
        self.body = nbody
        self.bin = B; self.tools[name] = (kind, T); self.order.append(name)

    def try_tool(self, name, kind, T, tag):
        """apply tool T only if the oracle IoU improves."""
        try:
            inT = self.ref.pts_in(T)
        except Exception:
            return False
        nb = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
        s0 = self.score(self.bin); s1 = self.score(nb)
        if s1 > s0 + 1e-5:
            self.commit(name, kind, T, nb); FD.log(name, 'OK', tag, iou=round(s1, 4)); return True
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
                    inT = self.ref.pts_in(T); nb = (self.bin | inT) if kind == 'boss' else (self.bin & ~inT)
                    sc = self.score(nb)
                    if best is None or sc > best[0]: best = (sc, T, nb, len(keep), self.quality(kind, inT), fname, len(cells), (rot, tr))
        if best is None or best[0] <= self.score(self.bin) + 1e-6:
            sk.rot, sk.trans = rot0, tr0
            FD.log(F.name, 'FAIL', f'revolve {skf.name}: no axis/cell gives an IoU gain'); return
        sk.rot, sk.trans = best[7]
        self.commit(F.name, kind, best[1], best[2])
        FD.log(F.name, 'OK', f'revolve {kind} {skf.name} {ang:g} deg', frame=best[5], cells=f'{best[3]}/{best[6]}', prec=round(float(best[4]), 3), iou=round(best[0], 4))

    def blend_feature(self, F, mirror=None):
        # FD.blend_feature reads FACE lines = faces the feature created
        cf = getattr(F, 'created_faces', None) or []
        if not cf:   # no creator attribution decoded (RV22): every XT face whose geometry fits the blend size
            bp = DP.blend_params(F); sz = (bp[1] or 0) if bp else 0
            for x in self.g.faces:
                S = xt_surface(x)
                if F.type == 'Fillet' and ((S.kind == 'cyl' and abs(S.params['r'] - sz) < 1e-6) or
                                           (S.kind == 'torus' and abs(S.params['values'][7] - sz) < 1e-6)): cf.append(S)
                if F.type != 'Fillet' and (S.kind == 'cone' or (S.kind == 'plane' and max(abs(np.array(S.params['n']))) < 0.999)): cf.append(S)
        F.faces, keep = cf, F.faces
        try:
            if F.type == 'Chamfer' and not F.chamfer: F.type = 'Chamfer'
            super().blend_feature(F, mirror)
        finally:
            F.faces = keep

    def mirror_feature(self, F):
        m = self.g.pat.get(F.name) or {}
        planes = []
        if m.get('normal') is not None: planes.append((np.array(m['normal'], float), m['offset_mm']))
        for nn in ((1, 0, 0), (0, 1, 0), (0, 0, 1)):
            if not any(abs(abs(np.dot(p[0], nn)) - 1) < 1e-6 and abs(p[1]) < 1e-6 for p in planes): planes.append((np.array(nn, float), 0.0))
        done = []
        for nrm, off in planes:
            mp = Plane(origin=tuple(nrm * off), z_dir=tuple(nrm))
            for src in list(self.order):
                kind, T = self.tools[src]
                try: M = T.mirror(mp)
                except Exception: continue
                if self.try_tool(f'{F.name}<{src}', kind, M, f'mirror of {src} about n={np.round(nrm, 3).tolist()} d={off:g}'): done.append(src)
            if done: break
        if not done: FD.log(F.name, 'SKIP', 'no mirrored seed improves the oracle IoU')

    def pattern_feature(self, F):
        m = self.g.pat.get(F.name) or {}
        offs = m.get('common_offsets_mm') or []
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
        for k in range(len(prev) - 1):
            profs = prev[k:]
            secs = []
            for sf in profs:
                fr = self.frames(sf)
                sk = sf.sketch; r0, t0 = sk.rot, sk.trans
                sk.rot, sk.trans = max(fr, key=lambda x: float(x[2].split('reg=')[-1]))[:2]
                cells = FD.sketch_cells(sf)
                if cells:
                    U = cells[0].fuse(*cells[1:]) if len(cells) > 1 else cells[0]
                    fc = max(U.faces(), key=lambda x: x.area) if hasattr(U, 'faces') else U
                    secs.append(fc)
                sk.rot, sk.trans = r0, t0
            if len(secs) < 2: continue
            try:
                T = loft([Face(f.outer_wire()) for f in secs])
            except Exception as ex:
                FD.log(F.name, 'FAIL', f'loft: {type(ex).__name__}'); continue
            for kd in (kind,):
                try: inT = self.ref.pts_in(T)
                except Exception: continue
                nb = (self.bin | inT) if kd == 'boss' else (self.bin & ~inT)
                sc = self.score(nb)
                if best is None or sc > best[0]: best = (sc, T, nb, [p.name for p in profs], kd)
        if best is None or best[0] <= self.score(self.bin) + 1e-6:
            FD.log(F.name, 'SKIP', f'loft of {[p.name for p in prev]}: no IoU gain'); return
        for p in best[3]: self.g.used.add(p)
        self.commit(F.name, best[4], best[1], best[2]); FD.log(F.name, 'OK', f'loft {best[4]} of {best[3]}', iou=round(best[0], 4))

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
        best = None; s0 = self.score(self.bin); cands = []
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
                        inT = self.ref.pts_in(T); nb = self.bin & ~inT; sc = self.score(nb)
                    except Exception as ex:
                        nfail = locals().get('nfail', 0) + 1
                        if nfail == 1: FD.log(F.name, 'WARN', f'thread candidate failed: {type(ex).__name__} {str(ex)[:80]}')
                        continue
                    cands.append((sc, tool, nb, dict(r=round(r, 3), L=round(L, 3), hole=hole, phase=float(ph), lefthand=lh, land=land)))
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
        if best is None or best[0] <= s0 + 1e-6: FD.log(F.name, 'SKIP', 'thread: no helix improves the oracle IoU'); return
        self.commit(F.name, 'cut', best[1], best[2]); FD.log(F.name, 'OK', f'thread pitch {pitch:g} h {h:g} {best[3]}', iou=round(best[0], 4))

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
        for f in self.part.features:
            if prog:
                with open(prog, 'w') as fh: fh.write(f.name)
            if f.name in skip:
                FD.log(f.name, 'SKIP', 'OCC crashed (segfault) on this feature in an earlier attempt'); continue
            prev = self.body
            try:
                self._run_one(f)
            except Exception as ex:
                FD.log(f.name, 'ERROR', f'{type(ex).__name__}: {str(ex)[:120]}')
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
    bp = os.path.join(out_dir, 'breps', src + '.brep')
    if not os.path.exists(bp): run_part(src, out_dir)
    if not os.path.exists(bp): return dict(iou=0.0, note=f'source {src} not rebuilt')
    sc, n, d = MD.fit_plane(src, part)
    body = import_brep(bp).mirror(Plane(origin=tuple(n * d), z_dir=tuple(n)))
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Copy   # deep copy: the mirrored shape can carry stale/missing triangulation
    body = type(body)(BRepBuilderAPI_Copy(body.wrapped, True, False).Shape())
    try: export_brep(body, os.path.join(out_dir, 'breps', part + '.brep'))
    except Exception: pass
    T = DL.triangles(os.path.join(ROOT, 'revdev', part + '.SLDPRT'))
    if T is None or len(T) <= 12:   # no display mesh of its own: the source's final-body mesh, reflected
        Ts = DL.triangles(os.path.join(ROOT, 'revdev', src + '.SLDPRT'))
        if Ts is not None and len(Ts) > 12:
            T = Ts - 2 * ((Ts @ n) - d)[..., None] * n
    b = compare(body, part, T if T is not None and len(T) > 12 else None)
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], oracle=None, derived_from=src,
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
        rb = OracleReplay(part, ref); body = body_solid(rb.run())
    if body is None: return dict(iou=0.0, note='no body', oracle=ref.source, log=LOG[:])
    try: export_brep(body, os.path.join(out_dir, 'breps', part + '.brep'))
    except Exception: pass
    b = compare(body, part, ref.T)
    st = {}
    for x in LOG: st[x['status']] = st.get(x['status'], 0) + 1
    return dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], oracle=ref.source,
                oracle_iou=round(float(ref.miou(rb.bin)), 4), volume=round(body.volume, 1), oracle_volume=round(ref.V, 1),
                ops=st, seconds=round(time.time() - t0, 1),
                log=[{k: (v if isinstance(v, (int, float, str, type(None))) else str(v)) for k, v in x.items()} for x in LOG])


def main(sel):
    os.makedirs(os.path.join(HERE, 'breps'), exist_ok=True)
    parts = sorted(os.path.basename(p)[:-7] for p in glob.glob(os.path.join(ROOT, 'revdev', '*.SLDPRT')))
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
