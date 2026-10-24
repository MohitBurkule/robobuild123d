import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS, validate as V
import collections
st=collections.Counter()
for n,D,d in parts():
    dec=FS.decode(d,set()); byname={f.name:f for f in D.top()}
    for f in D.top():
        if f.type not in V.EXTRUDE_TYPES: continue
        skn=[p for p,t in f.parents if t=='ProfileFeature']
        S=byname.get(skn[0]) if skn else None
        if S is None or S.id not in dec.sketches or not S.sketch_to_model: continue
        X=dec.sketches[S.id]; sk=X['sketch']
        sel,has=FS.selected_serials(X['choosers'],X['regions'],sk,X['chains'] or None)
        if not has: continue
        ser={}
        for s_ in sk.lines: ser[(0,)+s_.api_id]=s_.serial
        for s_ in sk.arcs: ser[(1,)+s_.api_id]=s_.serial
        ev={ser[(g['type'],)+g['id']] for g in S.segs if (g['type'],)+g['id'] in ser and not g['constr'] and V.seg_has_face(g,S.sketch_to_model,f.faces)}
        miss=ev-sel-{0}
        unm=[ct for c in X['choosers'] for ct in c.contours if ct.rid is None]
        if miss or unm:
            print(n[:14],f.name,'S',S.name,'nch',len(X['choosers']),[ (c.offset,c.n_selected,len(c.contours)) for c in X['choosers']],'miss',sorted(miss))
            print('   regs',[(r.rid,r.serials) for r in X['regions']][:8])
            print('   unm',[ct.serials for ct in unm][:4])
