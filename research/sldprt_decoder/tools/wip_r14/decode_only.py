#!/usr/bin/env python3
"""Round 14 (4): end-to-end "decode only" rebuild check for the revdev parts.

Pipeline per part (no dumps, no API data):
  SLDPRT -> decoded/<part>.json (decoder output) -> item_sketchplane / item_endcond /
  item_fillet / item_pattern regenerated here from the SLDPRT -> build123d replay
  (rebuild/rv01_rebuild.Rebuild, generalised: fallback sketch links, revolves, sketch
  placement from the decoded sketch record) -> voxel IoU against the reference STL
  (research/rvrn_step/parts/, assembly frame) using the decoded rvrn 2.0 placement.
Usage: python3 decode_only.py [part-name-prefix ...]   -> decode_only.json / .txt
"""
import sys, os, json, math, re, glob, time, traceback, contextlib, io
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'tools')); sys.path.insert(0, os.path.join(ROOT, 'rebuild'))
import rv01_rebuild as R
from sldprt import item_sketchplane as ISP, item_endcond as IEC, item_fillet as IFL, item_pattern as IPT
from build123d import Solid, Vector, Location, Axis, Compound, revolve, Plane
STL = os.path.join(ROOT, '..', 'rvrn_step', 'parts')
OUT = os.path.join(HERE, 'decode_only'); os.makedirs(OUT, exist_ok=True)
DEC = os.path.join(ROOT, 'decoded')

def num(s):
    m = re.search(r'-?\d+(\.\d+)?', str(s).replace('<MOD-DIAM>', ''))
    return float(m.group()) if m else None

def regen(part):
    """decoded side files, regenerated from the SLDPRT + decoded json only."""
    sl = os.path.join(ROOT, 'revdev', part + '.SLDPRT'); dj = os.path.join(DEC, part + '.json')
    od = os.path.join(OUT, part); os.makedirs(od, exist_ok=True)
    J = json.load(open(dj)); json.dump(J, open(os.path.join(od, part + '.json'), 'w'))
    try: sp = ISP.decode_part(sl, dj)
    except Exception as ex: sp = {'sketches': [], 'error': repr(ex)}
    json.dump(sp, open(os.path.join(od, part + '.sketchplane.json'), 'w'), indent=1)
    try: ec = IEC.classify(J, sp)
    except Exception as ex: ec = {}
    json.dump(ec, open(os.path.join(od, part + '.endcond.json'), 'w'), indent=1, default=float)
    try: IFL.run(sl, dj, os.path.join(od, part + '.fillets.json'))
    except Exception: json.dump({'features': []}, open(os.path.join(od, part + '.fillets.json'), 'w'))
    try: pt = IPT.run(dj)
    except Exception: pt = {}
    json.dump(pt, open(os.path.join(od, part + '.patterns.json'), 'w'), indent=1, default=float)
    return od

class GRebuild(R.Rebuild):
    def __init__(s):
        super().__init__()
        s.used = set(e.get('sketch') for e in s.ec.values() if e.get('sketch'))
        for sk in s.d['sketches']:
            if sk['name'] not in s.sp:
                T = (sk.get('placement') or {}).get('transform_rows_x_y_z_t') or [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]
                s.sp[sk['name']] = dict(sketch=sk['name'], origin_m=T[9:12], x_axis=T[0:3], y_axis=T[3:6], normal=T[6:9],
                                        record_class='sketch_record')
        s.fid = {f['name']: f for f in s.d['features']}; s.generic = set()

    def link(s, F):
        """fallback sketch link: nearest earlier unconsumed sketch with entities."""
        fid = s.fid[F]['id']
        c = [f for f in s.d['features'] if f['type'] in ('Sketch', 'ProfileFeature') and f['id'] < fid and f['name'] in s.sk
             and f['name'] not in s.used and s.sk[f['name']].get('entities')]
        if not c: return None
        n = max(c, key=lambda f: f['id'])['name']; s.used.add(n); return n

    def tool(s, F, kind):
        e = s.ec.get(F) or {}
        if e.get('sketch') and e['sketch'] in s.sp and (e.get('D_mm') or e.get('extent_abs_mm') or e.get('end_code_dir1') in (1, 9)):
            try:
                T = super().tool(F, kind)
                if T is not None: return T
            except Exception as ex:
                R.log(F, 'FIX', f'generic rule after {type(ex).__name__}')
        name = e.get('sketch') or s.link(F)
        if not name: R.log(F, 'SKIP', 'no sketch'); return None
        prof, info = s.profile(name)
        if not prof: R.log(F, 'SKIP', f'{name}: no closed region'); return None
        O, X, Y, Z = R.sketch_frame(s.sp[name])
        D = (e.get('D_mm') or [None])[0] or next((num(v) for _, v in s.fid[F].get('dims', []) if num(v)), None)
        code = e.get('end_code_dir1')
        if code in (1, 9) or not D: lo, hi = (-R.BIG, R.BIG) if kind == 'cut' else (0, 0)
        elif code == 6: lo, hi = -D / 2, D / 2
        else: lo, hi = (0, D) if kind == 'boss' else (-D, D)  # cut direction unknown: both sides
        if hi - lo < 1e-6: R.log(F, 'SKIP', 'no depth'); return None
        V = Vector(*Z); sol = [Solid.extrude(f.moved(Location(tuple(Z * lo))), V * (hi - lo)) for f in prof]
        s.generic.add(F)
        R.log(F, 'OK', f'generic {kind} {name} [{lo},{hi}] code={code}', sketch=name)
        return sol[0] if len(sol) == 1 else sol[0].fuse(*sol[1:])

    def revolve_tool(s, F):
        name = s.link(F)
        if not name: R.log(F, 'SKIP', 'no sketch'); return None
        sk = s.sk[name]
        ax = [e for e in sk['entities'] if e.get('flag') == 0 and e['type'] == 'line' and e.get('start') and e.get('end')]
        # axis: a flag-0 line with every flag-1 vertex on one side of it (round 14)
        V2 = np.array([p for e in sk['entities'] if e.get('flag') == 1 for p in (e.get('start'), e.get('end')) if p]) * 1e3
        if not len(V2) or not ax: R.log(F, 'SKIP', f'{name}: no profile / axis'); return None
        def side_ok(a):
            p0 = np.array(a['start']) * 1e3; p1 = np.array(a['end']) * 1e3; t = p1 - p0
            if np.linalg.norm(t) < 1e-9: return None
            c = (V2 - p0) @ np.array([-t[1], t[0]]) / np.linalg.norm(t)
            return None if (c.min() < -1e-4 and c.max() > 1e-4) else -abs(c).mean()
        ok = [(side_ok(a), a) for a in ax]; ok = [x for x in ok if x[0] is not None]
        if not ok: R.log(F, 'SKIP', f'{name}: no centreline with the profile on one side'); return None
        a = ok[0][1]; p0 = np.array(a['start']) * 1e3; p1 = np.array(a['end']) * 1e3
        # profile: flag-1 entities + flag-0 lines whose both ends are flag-1 vertices (closing edges
        # the construction flag mislabels, e.g. RV19 Sketch1 x=3.5)
        key = lambda q: (round(q[0], 7), round(q[1], 7))
        vs = {key(p) for e in sk['entities'] if e.get('flag') == 1 for p in (e.get('start'), e.get('end')) if p}
        sk2 = dict(sk, entities=[dict(e, flag=1) if (e.get('flag') == 0 and e['type'] == 'line' and e is not a and e.get('start') and e.get('end')
                                                       and key(e['start']) in vs and key(e['end']) in vs) else e for e in sk['entities']])
        def prof(sk_):
            ents, _ = R.sketch_entities(sk_); R.resolve_arcs(ents); ents, _ = R.drop_crossing(ents)
            sel = R.regions(ents); return ents, sel, sum(c.area for c in sel)
        e1, s1, a1 = prof(sk); e2, s2, a2 = prof(sk2)
        ents, sel = (e1, s1) if a1 >= 0.25 * a2 and s1 else (e2, s2)
        if sel is s2 and a2 > a1: R.log(F, 'FIX', f'{name}: closing flag-0 lines used ({a1:.2f} -> {a2:.2f} mm2)')
        f2 = R.exact_faces(ents, sel)
        if not f2: R.log(F, 'SKIP', f'{name}: no region'); return None
        O, X, Y, Z = R.sketch_frame(s.sp[name])
        ang = next((num(v) for _, v in s.fid[F].get('dims', []) if '°' in str(v)), 360.0) or 360.0
        out = []
        for f in f2:
            try: out.append(revolve(f, Axis((p0[0], p0[1], 0), (p1[0] - p0[0], p1[1] - p0[1], 0)), ang))
            except Exception: pass
        if not out: R.log(F, 'FAIL', 'revolve'); return None
        T = out[0] if len(out) == 1 else out[0].fuse(*out[1:])
        pl = Plane(origin=tuple(O), x_dir=tuple(X), z_dir=tuple(Z))
        R.log(F, 'OK', f'revolve {name} {ang} deg', sketch=name)
        return T.moved(pl.location)

    def apply(s, F, kind, T):
        # decode-only guard: a cut that removes most of the body is a wrong region / extent guess
        if T is not None and kind == 'cut' and s.body is not None and F in s.generic:
            v0 = s.body.volume
            try:
                v1 = R._largest(s.body.cut(T).clean()).volume
                if v1 < 0.4 * v0:
                    R.log(F, 'FIX', f'cut rejected: would remove {100 * (1 - v1 / v0):.0f}% of the body'); return
            except Exception: pass
        super().apply(F, kind, T)

    def run(s):
        for f in sorted(s.d['features'], key=lambda f: f['id']):
            F, t = f['name'], f['type']
            try:
                if t in ('Boss-Extrude', 'Cut-Extrude', 'Extrusion'):
                    kind = 'cut' if F.startswith('Cut') else 'boss'
                    s.apply(F, kind, s.tool(F, kind))
                elif t in ('Revolve', 'Cut-Revolve'):
                    s.apply(F, 'cut' if t.startswith('Cut') else 'boss', s.revolve_tool(F))
                elif t in ('Fillet', 'Chamfer') and s.body is not None:
                    s.blend(F)
                elif t == 'Mirror' and s.body is not None:
                    s.mirror_feat(F)
            except Exception as ex:
                R.log(F, 'ERROR', f'{type(ex).__name__}: {ex}')
        return s.body

# --------------------------------------------------------------- reference + voxel IoU
def read_stl(p):
    b = open(p, 'rb').read(); n = int.from_bytes(b[80:84], 'little')
    a = np.frombuffer(b, dtype=np.dtype([('n', '<3f4'), ('v', '<9f4'), ('x', '<u2')]), count=n, offset=84)
    return a['v'].reshape(-1, 3, 3).astype(float)

def tri_of(shape, tol=0.02):
    V, T = shape.tessellate(tol, 0.2); V = np.array([tuple(v) for v in V]); return V[np.array(T)]

def vox(tris, lo, pitch, shape):
    """z-ray parity voxelisation of a closed triangle soup."""
    nx, ny, nz = shape; hits = [[[] for _ in range(ny)] for _ in range(nx)]
    for t in tris:
        x0, y0 = t[:, 0].min(), t[:, 1].min(); x1, y1 = t[:, 0].max(), t[:, 1].max()
        i0 = max(0, int(math.ceil((x0 - lo[0]) / pitch - 0.5))); i1 = min(nx - 1, int(math.floor((x1 - lo[0]) / pitch - 0.5)))
        j0 = max(0, int(math.ceil((y0 - lo[1]) / pitch - 0.5))); j1 = min(ny - 1, int(math.floor((y1 - lo[1]) / pitch - 0.5)))
        if i1 < i0 or j1 < j0: continue
        (ax, ay, az), (bx, by, bz), (cx, cy, cz) = t
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if abs(den) < 1e-14: continue
        X, Y = np.meshgrid(lo[0] + (np.arange(i0, i1 + 1) + 0.5) * pitch, lo[1] + (np.arange(j0, j1 + 1) + 0.5) * pitch, indexing='ij')
        l1 = ((by - cy) * (X - cx) + (cx - bx) * (Y - cy)) / den; l2 = ((cy - ay) * (X - cx) + (ax - cx) * (Y - cy)) / den; l3 = 1 - l1 - l2
        m = (l1 >= 0) & (l2 >= 0) & (l3 >= 0)
        Zs = l1 * az + l2 * bz + l3 * cz
        for (ii, jj) in zip(*np.nonzero(m)): hits[i0 + ii][j0 + jj].append(Zs[ii, jj])
    G = np.zeros(shape, bool); zc = lo[2] + (np.arange(nz) + 0.5) * pitch
    for i in range(nx):
        for j in range(ny):
            h = hits[i][j]
            if len(h) < 2: continue
            h = np.sort(np.array(h)); k = np.concatenate([[True], np.diff(h) > 1e-9]); h = h[k]
            G[i, j] = (np.searchsorted(h, zc) % 2) == 1
    return G

def iou(A, B, pitch=0.25):
    lo = np.minimum(A.reshape(-1, 3).min(0), B.reshape(-1, 3).min(0)) - pitch
    hi = np.maximum(A.reshape(-1, 3).max(0), B.reshape(-1, 3).max(0)) + pitch
    pitch = max(pitch, float(np.prod(hi - lo) / 4e6) ** (1 / 3))
    shape = tuple(int(math.ceil(x)) for x in (hi - lo) / pitch)
    a = vox(A, lo, pitch, shape); b = vox(B, lo, pitch, shape)
    u = (a | b).sum(); return float((a & b).sum() / u) if u else 0.0, pitch

def placements(part):
    m = json.load(open(os.path.join(DEC, 'rvrn 2.0.mates.json')))
    code = part.split()[0] + ' ' if part.split()[0][:2] in ('RV', 'FS') else part.rsplit(' ', 0)[0]
    return [c for c in m['components'] if c['instance'].startswith(code) or c['instance'].rsplit('-', 1)[0] == part]

def compare(body, part):
    tris = tri_of(body)
    best = None
    tok = part.split()[0]
    refs = sorted(glob.glob(os.path.join(STL, re.sub(r'[^A-Za-z0-9]', '_', tok) + '_*.stl'))) if tok[:2] in ('RV', 'FS') else \
        sorted(glob.glob(os.path.join(STL, re.sub(r'[^A-Za-z0-9]', '_', part) + '_[0-9].stl')))
    for c in placements(part):
        if len(c.get('rotation_rows') or []) != 9 or len(c.get('translation_m') or []) != 3: continue
        Rr = np.array(c['rotation_rows'], float).reshape(3, 3); t = np.array(c['translation_m']) * 1e3
        A = tris @ Rr + t  # p_asm = t + x r0 + y r1 + z r2
        ca = A.reshape(-1, 3).mean(0)
        for r in refs:
            B = read_stl(r)
            if np.linalg.norm(B.reshape(-1, 3).mean(0) - ca) > 30: continue
            v, p = iou(A, B)
            if best is None or v > best[0]: best = (v, os.path.basename(r), c['instance'], p)
    if best is None:
        # no decoded placement for this instance: register over the 24 axis rotations, bbox centres aligned
        import itertools
        rots = [np.array(P) * np.array(sg)[:, None] for P in itertools.permutations(np.eye(3)) for sg in itertools.product((1, -1), repeat=3)]
        rots = [Q for Q in rots if np.linalg.det(Q) > 0]
        for r in refs:
            B = read_stl(r); bl, bh = B.reshape(-1, 3).min(0), B.reshape(-1, 3).max(0)
            def err(Q):
                A = tris @ Q; al, ah = A.reshape(-1, 3).min(0), A.reshape(-1, 3).max(0)
                return float(np.abs((ah - al) - (bh - bl)).sum())
            E = sorted((err(Q), k) for k, Q in enumerate(rots))
            for e_, k in E:
                if e_ > E[0][0] + 1.0 and k not in [x[1] for x in E[:4]]: continue
                Q = rots[k]
                A = tris @ Q; al, ah = A.reshape(-1, 3).min(0), A.reshape(-1, 3).max(0)
                A = A + ((bl + bh) - (al + ah)) / 2
                v, p = iou(A, B)
                if best is None or v > best[0]: best = (v, os.path.basename(r), 'registered(no decoded placement)', p)
    return best

def main(sel):
    parts = sorted(os.path.basename(p)[:-7] for p in glob.glob(os.path.join(ROOT, 'revdev', '*.SLDPRT')))
    parts = [p for p in parts if not sel or any(p.startswith(x) for x in sel)]
    res = {}
    rp = os.path.join(HERE, 'decode_only.json')
    if os.path.exists(rp) and sel: res = json.load(open(rp))
    for part in parts:
        t0 = time.time(); R.LOG.clear()
        try:
            R.DEC = regen(part); R.PART = part
            with contextlib.redirect_stdout(io.StringIO()):
                rb = GRebuild(); body = rb.run()
            if body is None: res[part] = dict(iou=0.0, note='no body', log=R.LOG[:]); print(part, 'no body', flush=True); continue
            b = compare(body, part)
            st = {}
            for x in R.LOG: st[x['status']] = st.get(x['status'], 0) + 1
            res[part] = dict(iou=round(b[0], 4) if b else None, ref=b and b[1], instance=b and b[2], pitch_mm=b and round(b[3], 3),
                             volume=round(body.volume, 1), ops=st, seconds=round(time.time() - t0, 1),
                             log=[{k: v for k, v in x.items() if k in ('feature', 'status', 'msg')} for x in R.LOG])
            print(part, res[part]['iou'], res[part]['ref'], st, flush=True)
        except Exception as ex:
            res[part] = dict(iou=0.0, note=repr(ex)[:300]); print(part, 'ERR', repr(ex)[:200], flush=True)
        json.dump(res, open(rp, 'w'), indent=1, default=float)
    v = [r['iou'] or 0 for r in res.values() if r.get('ref') or r.get('note')]
    print('MEAN IoU', round(sum(v) / len(v), 4), 'parts', len(v))

if __name__ == '__main__':
    main(sys.argv[1:])
