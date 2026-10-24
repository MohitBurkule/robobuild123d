"""Round 15 diagnostic: oracle residual (missing / extra voxel blobs) after the decode-only replay,
with the XT-face creator features near each blob -> where the replay first diverges."""
import sys, os, json, io, contextlib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, '..'))
import decode_replay as D
import numpy as np
from scipy import ndimage
def run(part, upto=None):
    D.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
    ref = D.oracle_for(part); ref.init_points()
    with contextlib.redirect_stdout(io.StringIO()):
        rb = D.OracleReplay(part, ref)
        if upto: rb.part.features = [f for f in rb.part.features if f.id <= upto]
        rb.run()
    J = json.load(open(os.path.join(D.DO.DEC, part + '.json')))
    G = ref.G; n = tuple(G.n)
    for lab, M in (('missing', ref.rin & ~rb.bin), ('extra', rb.bin & ~ref.rin)):
        M = ndimage.binary_opening(M.reshape(n), iterations=1)
        L, k = ndimage.label(M); sz = ndimage.sum(M, L, range(1, k + 1))
        for i in np.argsort(-sz)[:6]:
            if sz[i] * G.dv < 0.5: break
            idx = np.argwhere(L == i + 1); lo = G.lo + idx.min(0) * G.d; hi = G.lo + (idx.max(0) + 1) * G.d
            near = collections.Counter()
            for f in J['faces']:
                V = np.array([e['start_vertex'] for l in f.get('loops', []) for e in l['edges'] if e.get('start_vertex')]) * 1e3
                if len(V) and np.any(np.all((V >= lo - 0.3) & (V <= hi + 0.3), 1)): near[f.get('feature_first_name')] += 1
            print(f'  {lab:7s} {sz[i]*G.dv:8.1f} mm3 box {np.round(lo,2).tolist()} .. {np.round(hi,2).tolist()} creators {dict(near.most_common(6))}')
    print(part, 'oracle iou', round(float(ref.miou(rb.bin)), 4))
    for x in D.LOG: print('   ', x['status'], x['feature'], x['msg'][:40], {k: v for k, v in x.items() if k in ('frame', 'cells', 'ivs', 'prec', 'iou', 'edges')})
if __name__ == '__main__':
    run(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else None)
