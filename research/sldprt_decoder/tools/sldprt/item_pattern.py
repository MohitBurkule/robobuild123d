"""Mirror / pattern recovery from decoded B-rep (geometric, works off <part>.json).

Mirror: faces stamped with the Mirror feature id are paired with congruent faces
(same surface type, radius, edge count) elsewhere; each pair votes for the bisecting
plane (n, d).  The winning plane is the mirror plane; it is named against the
default planes (Front z=0, Top y=0, Right x=0) or a coincident planar face.  Seed
features = creator ids on the partner faces.
Patterns: instance faces vs. seed faces -> centroid set; linear = cluster of
translation vectors, circular = circle fit through centroids (axis = plane normal).
"""
import json, math, sys, collections
import numpy as np

DEFAULT = {'Front Plane': (np.array([0, 0, 1.]), 0.0), 'Top Plane': (np.array([0, 1., 0]), 0.0),
           'Right Plane': (np.array([1., 0, 0]), 0.0)}

def face_pts(f):
    return np.array([e['start_vertex'] for l in f.get('loops', []) for e in l['edges'] if e.get('start_vertex')])

def sig(f):
    p = f.get('params') or {}
    return (f['surface_type'], round(p.get('radius', 0) * 1e5), sum(len(l['edges']) for l in f.get('loops', [])))

def _canon(n, d):
    i = int(np.argmax(np.abs(n)))
    if n[i] < 0: n, d = -n, -d
    return n, d

def mirror_plane(faces, fid):
    mine = [f for f in faces if fid in f['feature_ids_by_time']]
    others = [f for f in faces if fid not in f['feature_ids_by_time']]
    votes = collections.Counter(); seeds = collections.defaultdict(collections.Counter)
    cache = {}
    for f in faces:
        P = face_pts(f)
        cache[id(f)] = P.mean(0) if len(P) else None
    for a in mine:
        ca = cache[id(a)]
        if ca is None: continue
        for b in others:
            cb = cache[id(b)]
            if cb is None or sig(a) != sig(b): continue
            v = cb - ca; L = np.linalg.norm(v)
            if L < 1e-6: continue
            n, d = _canon(v / L, float(np.dot(v / L, (ca + cb) / 2)))
            k = (tuple(np.round(n, 3)), round(d * 1e4))
            votes[k] += 1; seeds[k][b['feature_first_name']] += 1
    if not votes: return None
    k, c = votes.most_common(1)[0]
    n = np.array(k[0]); d = k[1] / 1e4
    # verify: reflect every vertex of mine and check it lands on a vertex of others
    allv = np.vstack([face_pts(f) for f in others if len(face_pts(f))])
    hit = tot = 0
    for a in mine:
        for p in face_pts(a):
            r = p - 2 * (np.dot(n, p) - d) * n; tot += 1
            hit += np.min(np.linalg.norm(allv - r, axis=1)) < 1e-5
    name = None
    for nm, (dn, dd) in DEFAULT.items():
        if abs(abs(np.dot(dn, n)) - 1) < 1e-6 and abs(d - dd) < 1e-6: name = nm
    if not name:
        for f in faces:
            if f['surface_type'] == 'plane':
                P = face_pts(f)
                if len(P) and np.all(np.abs(P @ n - d) < 1e-6): name = f'face plane (feature {f["feature_first_name"]})'; break
    return {'normal': list(n), 'offset_mm': d * 1e3, 'ref': name or 'reference plane/face not coincident with defaults',
            'votes': c, 'n_mirror_faces': len(mine), 'vertex_reflection_hits': f'{hit}/{tot}',
            'seed_features': dict(seeds[k].most_common()),
            'confidence': 'high' if tot and hit / tot > .9 else 'medium' if c >= 3 else 'low'}

def pattern(faces, fid, feat):
    mine = [f for f in faces if fid in f['feature_ids_by_time']]
    dims = {k: v for k, v in feat['dims']}
    out = {'dims': dims, 'n_instance_faces': len(mine)}
    groups = collections.defaultdict(list)
    for f in faces:
        P = face_pts(f)
        if len(P): groups[sig(f)].append((fid in f['feature_ids_by_time'], P.mean(0), f['feature_first_name']))
    best = None
    for s, g in groups.items():
        if any(m for m, _, _ in g) and (best is None or len(g) > len(best[1])) and len(g) >= 2: best = (s, g)
    if not best: out['note'] = 'no instance faces with ATOM_ID of pattern'; return out
    s, g = best
    C = np.array([c for _, c, _ in g])
    out['seed_features'] = dict(collections.Counter(nm for m, _, nm in g if not m))
    out['instances_found'] = len(g)
    if 'Cir' in feat['type'] and len(C) >= 3:
        c0 = C.mean(0); U, S, Vt = np.linalg.svd(C - c0); ax = Vt[2]
        # circle centre in plane
        e1, e2 = Vt[0], Vt[1]; Q = np.c_[(C - c0) @ e1, (C - c0) @ e2]
        A = np.c_[2 * Q, np.ones(len(Q))]; sol = np.linalg.lstsq(A, (Q ** 2).sum(1), rcond=None)[0]
        ctr = c0 + sol[0] * e1 + sol[1] * e2; R = math.sqrt(sol[2] + sol[0] ** 2 + sol[1] ** 2)
        ang = sorted(math.degrees(math.atan2(*(((c - ctr) @ e2), ((c - ctr) @ e1)))) % 360 for c in C)
        steps = np.diff(ang + [ang[0] + 360])
        out.update(kind='circular', axis_dir=list(np.round(ax, 6)), axis_point_mm=list(np.round(ctr * 1e3, 4)),
                   radius_mm=R * 1e3, angular_steps_deg=list(np.round(steps, 3)), face_signature=str(s))
    else:
        d = C[:, None] - C[None]; v = [tuple(np.round(x * 1e3, 3)) for x in d.reshape(-1, 3) if np.linalg.norm(x) > 1e-6]
        out.update(kind='linear', common_offsets_mm=[list(k) for k, _ in collections.Counter(v).most_common(4)], face_signature=str(s))
    return out

def run(path):
    d = json.load(open(path)); faces = d['faces']; res = {}
    for f in d['features']:
        if f['type'] == 'Mirror': res[f['name']] = mirror_plane(faces, f['id'])
        elif 'Pattern' in f['type']: res[f['name']] = pattern(faces, f['id'], f)
    return res

if __name__ == '__main__':
    for p in sys.argv[1:]:
        r = run(p); o = p[:-5] + '.patterns.json'
        json.dump(r, open(o, 'w'), indent=1, default=float); print(o, json.dumps(r, default=float)[:3000])
