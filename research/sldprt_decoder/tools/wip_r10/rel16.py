import sys
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, fstream as FS, answer_key as AK
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'; D='/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
n,sk=sys.argv[1],sys.argv[2]
d=V.feature_stream(R+n+'.SLDPRT'); A=AK.parse(D+n+'.dump.txt'); dec=V.evaluate(d,A,V.Acc())
f=[f for f in A.top() if f.name==sk][0]; X=dec.sketches[f.id]
print(f.rels)
rs=X['relations']; s=min(r.offset for r in rs); e=max(r.end for r in rs)
for m in FS.REL_HDR.finditer(d,s-2000,e+2000):
    sl,j=FS.read_slots(d,m.end())
    print(hex(m.start()), m.group(1)[0], len(sl), d[m.start():m.start()+60].hex())
