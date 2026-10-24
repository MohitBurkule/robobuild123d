import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, objnum as ON
for n in sys.argv[1:]:
    d=V.feature_stream('../dumps_ab/'+n+'.SLDPRT'); hs=FS.feature_headers(d)
    ev,_=ON.numbering(d); k=[e.cls for e in ev if e.kind=='def' and e.name=='moEndSpec_c'][0]
    acc=[e for e in ev if e.kind=='new' and e.cls==k]
    for e in acc: print(n[:30], 'ES obj at', e.offset, d[e.offset:e.offset+28].hex())
    h=[h for h in hs if h.name.startswith('Cut-Extrude1')]
    if h:
        h=h[0]
        for m in re.finditer(rb'[\x00-\xff][\x80-\xfe]\x00\x00[\x00\x01]\x00\x00\x00\x00\x00\x00\x00', d[h.offset:h.region_end]):
            a=h.offset+m.start(); print('   cand',a,d[a:a+28].hex())
