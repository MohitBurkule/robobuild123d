import sys, glob, os, struct
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter
from sldprt import validate as V, objnum as ON, classrec as CR, fstream as FS
R='/mnt/project-files/robot-cad/research/sldprt/'
mod=Counter(); w=Counter(); nxt=Counter()
for p in sorted(glob.glob(R+'dumps_v2/*.dump.txt')):
    n=os.path.basename(p)[:-9]; d=V.feature_stream(R+'revdev/'+n+'.SLDPRT'); ev,_=ON.numbering(d)
    fids={h.feature_id for h in FS.feature_headers(d)}
    for i,(e,a,b) in enumerate(CR._obj_spans(d,ev)):
        if e.name!='moFR_c' or b-a<10: continue
        r,fid=struct.unpack_from('<HI',d,a)
        if fid not in fids: continue
        L=b-a; mod[(L-10)%4]+=1
        if (L-10)%4==0:
            for j in range(a+10,b,4): w[(j-a, struct.unpack_from('<i',d,j)[0] if struct.unpack_from('<i',d,j)[0]<64 else 'big')]+=1
        else:
            nxt[(L, ev[i+1].name if i+1<len(ev) else None)]+=1
print(mod); print(sorted(w.items(),key=str)[:90]); print(nxt.most_common(10))
