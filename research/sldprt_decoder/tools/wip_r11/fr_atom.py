"""moFR_c vs Parasolid ATOM_ID_2001: match (fid,stamp) and compare tail words with atom raw ints."""
import sys, glob, os, struct
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter, defaultdict
from sldprt import validate as V, objnum as ON, classrec as CR, fstream as FS, streams as ST
from sldprt.xt import XT
R='/mnt/project-files/robot-cad/research/sldprt/'
def atoms(path):
    A=[]
    for s in ST.all_streams(open(path,'rb').read()):
        if ST.classify(s)=='parasolid':
            x=XT(s['data'])
            for a in x.attributes:
                if a['name'] in ('ATOM_ID_2001','FACE_ID_2001'):
                    for v in a['values']:
                        if isinstance(v,list) and len(v)>=5: A.append(tuple(v))
    return A
stat=Counter(); ex=[]
for p in sorted(glob.glob(R+'dumps_v2/*.dump.txt'))[:int(sys.argv[1]) if len(sys.argv)>1 else 99]:
    n=os.path.basename(p)[:-9]; path=R+'revdev/'+n+'.SLDPRT'; d=V.feature_stream(path); ev,_=ON.numbering(d)
    fids={h.feature_id for h in FS.feature_headers(d)}
    A=atoms(path); byfs=defaultdict(list)
    for a in A: byfs[(a[1],a[2])].append(a)
    for e,a,b in CR._obj_spans(d,ev):
        if e.name!='moFR_c' or b-a<10: continue
        r,fid,st=struct.unpack_from('<HII',d,a)
        if fid not in fids: continue
        k=(b-a-10)//4; tail=list(struct.unpack_from('<%dI'%k,d,a+10))
        m=byfs.get((fid,st))
        stat['fr']+=1; stat['match' if m else 'nomatch']+=1
        if m:
            seqs={x[4] for x in m}; full=[x[3:] for x in m]
            if tuple(tail) in {tuple(x[3:]) for x in m}: stat['tail==atom[3:]']+=1
            if tuple(tail) in {tuple(x[4:]) for x in m}: stat['tail==atom[4:]']+=1
            if len(ex)<25: ex.append((n[:12],fid,st,tail,m[:3]))
    stat['atoms']+=len(A)
print(stat)
for x in ex: print(x)
