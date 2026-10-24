"""Round 11b: per pattern feature, seed object refs vs nearest feature object (drift), for dumps_v2 + dumps_corpus."""
import sys, os, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, fstream as FS, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for src, dd in (('revdev', 'dumps_v2'), ('corpus', 'dumps_corpus')):
    for p in sorted(glob.glob(R + dd + '/*.dump.txt')):
        n = os.path.basename(p)[:-9]
        D = AK.parse(p); top = D.top()
        pats = [f for f in top if f.type in V.PATTERN_TYPES]
        if not pats: continue
        fp = R + src + '/' + n + '.SLDPRT'
        d = V.feature_stream(fp) if os.path.exists(fp) else None
        if d is None: continue
        ev, _ = ON.numbering(d); heads = FS.feature_headers(d); hidx = FS.header_index(d)
        fobj = ON.feature_objects(d, heads, ev); ids = {x.name: x.id for x in top}
        idobj = {fid: i for fid, (h, i, c) in fobj.items()}
        for f in pats:
            h = hidx.get(f.id)
            if h is None: continue
            refs = ON.seed_list(d, h)
            par = [(pn, ids.get(pn), idobj.get(ids.get(pn))) for pn, pt in f.parents if pt != 'RefPlane']
            res = ON.resolve_objects(refs, fobj, h.offset)
            print(dd[6:] or 'v2', n[:28], f.type, f.name, 'refs', refs, 'resolved', res, 'parents(name,fid,obj)', par, 'self_obj', idobj.get(f.id), 'res', ON.numbering.residual, flush=True)
