import sys, os, struct
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for n in sys.argv[1:]:
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d)
    names={e.cls:e.name for e in ev if e.kind=='def'}; acc={e.offset for e in ev}
    offs=sorted(acc)
    c=Counter()
    import bisect
    for m in ON.REF.finditer(d):
        o=m.start(); v=ON.u16(d,o)
        if o in acc or v==0xffff: continue
        a=v&0x7fff
        S=struct.unpack_from("<I",d,0)[0]
        if a not in names and not 0<a<S: continue
        # next word is an accepted tag start? (strong structural evidence)
        nxt = any(x in acc for x in (o+2,o+4,o+6))
        if not nxt: continue
        why = 'float' if ON.in_float(d,o) else 'stamp' if ON.is_stamp(d,o) else 'rej' if o in ON._numbering7.reject else 'other'
        c[(names.get(a) or "S-%d"%(S-a), why, min(x for x in (o+2,o+4,o+6) if x in acc)-o)]+=1
    print(n, c.most_common(15))
