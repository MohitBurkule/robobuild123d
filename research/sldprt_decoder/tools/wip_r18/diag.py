"""Round 15 diagnostic: run decode-only rebuild for a part, compare to final XT faces (bbox) and ref STL."""
import sys, os, json, io, contextlib, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r14'))
import decode_only as D
R = D.R
def xt_box(part):
    J = json.load(open(os.path.join(D.DEC, part + '.json')))
    P = np.array([e['start_vertex'] for f in J['faces'] for l in f.get('loops', []) for e in l['edges'] if e.get('start_vertex')]) * 1e3
    return P.min(0), P.max(0)
def stl_vol(T):
    return float(np.einsum('ij,ij->i', T[:, 0], np.cross(T[:, 1], T[:, 2])).sum() / 6)
if __name__ == '__main__':
    for part in sys.argv[1:]:
        R.LOG.clear(); R.DEC = D.regen(part); R.PART = part
        with contextlib.redirect_stdout(io.StringIO()):
            rb = D.GRebuild(); body = rb.run()
        lo, hi = xt_box(part)
        print('==', part, 'XT box', np.round(lo, 2), np.round(hi, 2), 'size', np.round(hi - lo, 2))
        if body is not None:
            bb = body.bounding_box(); print('   ours', np.round(tuple(bb.min), 2), np.round(tuple(bb.max), 2), 'vol', round(body.volume, 1))
            from build123d import export_brep; export_brep(body, os.path.join(HERE, part + '.brep'))
        tok = part.split()[0]
        import glob, re
        for r in sorted(glob.glob(os.path.join(D.STL, re.sub(r'[^A-Za-z0-9]', '_', tok if tok[:2] in ('RV','FS') else part) + '_*.stl'))):
            B = D.read_stl(r); print('   ref', os.path.basename(r), 'size', np.round(np.ptp(B.reshape(-1,3),0), 2), 'vol', round(abs(stl_vol(B)), 1))
        for x in R.LOG: print('   ', x['status'], x['feature'], x['msg'][:120])
