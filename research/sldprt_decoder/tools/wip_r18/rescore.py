"""Round 17: re-score a breps directory with the non-voxel metrics (exact mesh-boolean IoU against
the reference STL, registered as decode_replay.compare does; exact IoU and point-to-surface F-score
against the decoded oracle mesh).  Used to put the round-16 breps on the same metric.
    python3 rescore.py <breps_dir> <out.json>"""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import decode_replay as D, exact_iou as XI
import mirror_derived as MD
from build123d import import_brep

def score(part, bd):
    b = import_brep(os.path.join(bd, part + '.brep'))
    src = MD.source_of(part)
    T = None
    if src:
        Ts = D.DL.triangles(os.path.join(D.ROOT, D.SRC, part + '.SLDPRT'))
        if Ts is None or len(Ts) <= 12:
            sc, n, d = MD.fit_plane(src, part); Ts = D.DL.triangles(os.path.join(D.ROOT, D.SRC, src + '.SLDPRT'))
            T = None if Ts is None or len(Ts) <= 12 else (Ts - 2 * ((Ts @ n) - d)[..., None] * n)[:, ::-1]
        else: T = Ts
        src_ = 'derived'
    else:
        D.R.DEC = D.DO.regen(part); D.R.PART = part
        ref = D.oracle_for(part); T = ref.T if ref is not None else None; src_ = ref.source if ref else None
    c = D.compare(b, part, T)
    out = dict(iou=c and round(c[0], 4), ref=c and c[1], method=c and c[3], oracle=src_)
    if T is not None:
        BT = XI.mesh_of(b); e = XI.exact_iou(BT, T); out['oracle_iou'] = e[0] and round(e[0], 4)
        out['oracle_fscore'] = round(XI.surf_dist(BT, T)['fscore'], 4)
    return out

if __name__ == '__main__':
    bd, outp = sys.argv[1], sys.argv[2]; res = {}
    for f in sorted(glob.glob(os.path.join(bd, '*.brep'))):
        p = os.path.basename(f)[:-5]
        try: res[p] = score(p, bd)
        except Exception as ex: res[p] = dict(error=repr(ex)[:200])
        print(p, res[p], flush=True)
        json.dump(res, open(outp, 'w'), indent=1)
