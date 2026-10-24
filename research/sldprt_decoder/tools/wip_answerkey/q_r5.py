import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for n,D,d in parts():
    if not n.startswith(sys.argv[1]): continue
    dec=FS.decode(d,set()); S=[f for f in D.top() if f.name==sys.argv[2]][0]
    X=dec.sketches[S.id]; sk=X['sketch']
    ch=X['chains'] or FS.computed_contours(sk)
    print('stored',bool(X['chains']),[(c.serials,c.closed) for c in ch])
    bs=sk.by_serial()
    for x in [3,4,5,6,15]:
        g=bs.get(x); print(x,g.kind if g else None, g and (g.start,g.end,g.centre,g.real), g and FS._seg_polyline(sk,g)[:2])
    for c in X['choosers']:
        for ct in c.contours:
            e,p=FS._loop_geom(sk,ct.serials); print('outer',ct.serials,len(e))
    break
    loops=[sorted(c.serials) for c in FS.computed_contours(sk) if c.closed]
    print('computed loops',loops)
    for c in X['choosers']:
        for ct in c.contours: print('nested',FS.nested_loops(sk,ct.serials,loops))
