"""Round 15: mirror-derived parts (MirrorStock feature, e.g. RV18 = mirror of RV17).

The derived file carries the mirrored final body in its XT partition.  The mirror plane is fitted
decode-only: reflect the source part's XT vertices about candidate planes (normal = a model axis or
a source XT plane normal; offset from the support extremes) and keep the plane whose reflected
vertices land on the derived part's XT vertices.
"""
import os, json, re
import numpy as np
from scipy.spatial import cKDTree
HERE = os.path.dirname(os.path.abspath(__file__))
DEC = os.path.abspath(os.path.join(os.environ.get('R15_TOOLS') or os.path.join(HERE, '..'), '..', 'decoded'))


def xt_vertices(part):
    J = json.load(open(os.path.join(DEC, part + '.json')))
    P = [e['start_vertex'] for f in J['faces'] for l in f.get('loops', []) for e in l['edges'] if e.get('start_vertex')]
    for f in J['faces']:   # circle-only loops have no vertex: use the circle centres
        for l in f.get('loops', []):
            for e in l['edges']:
                c = e.get('curve') or {}
                if c.get('type') == 'circle': P.append(c['centre'])
    return np.unique(np.round(np.array(P) * 1e3, 5), axis=0)


def source_of(part):
    J = json.load(open(os.path.join(DEC, part + '.json')))
    for f in J['features']:
        if f['type'].endswith('_Mirrored'):
            src = f['type'][:-len('_Mirrored')]
            return resolve(part, src)
    return None


def resolve(part, src):
    """round 17: the MirrorStock feature names the source by its bare file name ('tbcpt1'); corpus
    files carry a '<group>_' prefix ('TBC_tbcpt1').  Resolve to an existing decoded part."""
    if os.path.exists(os.path.join(DEC, src + '.json')): return src
    if '_' in part:
        q = part.split('_', 1)[0] + '_' + src
        if os.path.exists(os.path.join(DEC, q + '.json')): return q
    for f in sorted(os.listdir(DEC)):
        if f.endswith('_' + src + '.json'): return f[:-5]
    return src


def reflect(P, n, d):
    return P - 2 * (P @ n - d)[:, None] * n


def fit_plane(src, dst):
    A = xt_vertices(src); B = xt_vertices(dst); tree = cKDTree(B)
    J = json.load(open(os.path.join(DEC, src + '.json')))
    normals = [np.eye(3)[i] for i in range(3)] + [np.array(f['params']['normal'], float) for f in J['faces'] if f['surface_type'] == 'plane']
    best = None
    for n in normals:
        n = n / np.linalg.norm(n)
        ds = {round(float((A @ n).max() + (B @ n).min()) / 2, 4), round(float((A @ n).min() + (B @ n).max()) / 2, 4), 0.0}
        for d in ds:
            dist, _ = tree.query(reflect(A, n, d))
            sc = float(np.mean(dist < 1e-3))
            if best is None or sc > best[0]: best = (sc, n, d)
    return best   # (fraction of reflected source vertices hitting a derived vertex, normal, offset mm)


if __name__ == '__main__':
    import glob, sys
    for p in sorted(glob.glob(os.path.join(DEC, '*.json'))):
        part = os.path.basename(p)[:-5]
        if '.' in part: continue
        try: s = source_of(part)
        except Exception: continue
        if not s: continue
        src = s if os.path.exists(os.path.join(DEC, s + '.json')) else None
        print(part, '<-', s, fit_plane(src, part) if src else 'source not decoded')
