"""r22: does the XT internal oracle agree with the dump audit?  per part: dump matched / dump
patches vs XT-oracle matched / XT patches on breps/<part>.brep (dump used only to check)."""
import sys, os, json, glob
HERE = os.path.dirname(os.path.abspath(__file__)); sys.argv_ = sys.argv; sys.argv = ['x']
import decode_replay as D, decode_only as DO, xt_oracle as XO, face_gate as FG
from build123d import import_brep
bd = sys.argv_[1] if len(sys.argv_) > 1 else os.path.join(HERE, 'breps'); sel = sys.argv_[2:]
out = {}
for b in sorted(glob.glob(os.path.join(bd, '*.brep'))):
    p = os.path.basename(b)[:-5]
    if sel and not any(p.startswith(s) for s in sel): continue
    dp = os.path.join(D.ROOT, 'dumps_v2', p + '.dump.txt')
    try:
        d = json.load(open(os.path.join(DO.DEC, p + '.json'))); X = XO.xt_faces(d); body = import_brep(b)
        r = dict(xt_m=XO.count(X, body), xt_n=XO.n_patches(X), xt_fb=XO.xt_faces.fallback)
        if os.path.exists(dp): g = FG.gate(b, dp); r.update(dump_m=g['matched'], dump_n=g['dump_patches'])
    except Exception as ex: r = dict(error=repr(ex)[:200])
    out[p] = r; print(p, r, flush=True)
json.dump(out, open(os.path.join(HERE, 'agree_' + os.path.basename(os.path.normpath(bd)) + '.json'), 'w'), indent=1)
