import sys, glob, os
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter
from sldprt import validate as V, objnum as ON, classrec as CR
R='/mnt/project-files/robot-cad/research/sldprt/'
cls=sys.argv[1]; L=Counter(); sigs=Counter(); ex={}
for p in sorted(glob.glob(R+'dumps_v2/*.dump.txt'))[:int(sys.argv[2])]:
    n=os.path.basename(p)[:-9]; d=V.feature_stream(R+'revdev/'+n+'.SLDPRT'); ev,_=ON.numbering(d)
    for k,e,a,b in CR._bodies(d,ev):
        if k==cls:
            s,_=CR._sig(d[a:b]); sigs[s]+=1; ex.setdefault(s,(n,a,d[a:b]))
print(len(sigs), sum(sigs.values()))
for s,c in sigs.most_common(8):
    n,a,b=ex[s]; print(c, s[:10], n, hex(a)); print('   ', b[:160].hex(' ',4))
