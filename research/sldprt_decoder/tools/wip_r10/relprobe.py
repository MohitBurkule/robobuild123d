import sys
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, fstream as FS, answer_key as AK
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'; D='/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
n,sk=sys.argv[1],sys.argv[2]
d=V.feature_stream(R+n+'.SLDPRT'); A=AK.parse(D+n+'.dump.txt'); dec=V.evaluate(d,A,V.Acc())
f=[f for f in A.top() if f.name==sk][0]; X=dec.sketches[f.id]
want={(t,tuple(sorted(es))) for t,es in f.rels}
for r in X['relations']:
    if not r.dimension and len(sys.argv)<4: continue
    k=(r.type,tuple(sorted(x[1] for x in r.ents)))
    print('OK ' if k in want else '-- ', r.type,'dim' if r.dimension else 'geo','f',r.flag,'a',r.aux,k[1], hex(r.offset), d[r.offset:r.end][:72].hex())
print('lines',len(X['sketch'].lines),'arcs',len(X['sketch'].arcs),'pts',len(X['sketch'].points))
for r in X['relations'][:12]: print(r.type, r.slots, r.ents)
