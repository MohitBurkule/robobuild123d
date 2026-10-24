import sys, glob, os, struct
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter, defaultdict
from sldprt import validate as V, objnum as ON, classrec as CR, fstream as FS
sys.path.insert(0, os.path.dirname(__file__)); from fr_atom import atoms
R='/mnt/project-files/robot-cad/research/sldprt/'
S=Counter(); stamps=Counter()
for p in sorted(glob.glob(R+'dumps_v2/*.dump.txt')):
    n=os.path.basename(p)[:-9]; path=R+'revdev/'+n+'.SLDPRT'; d=V.feature_stream(path); ev,_=ON.numbering(d)
    hs=FS.feature_headers(d); fids={h.feature_id for h in hs}
    A=atoms(path); fs={(a[1],a[2]) for a in A}; full={(a[1],a[2])+tuple(a[4:]) for a in A}
    fstamp=defaultdict(set)
    for a in A: fstamp[a[1]].add(a[2])
    for e,a,b in CR._obj_spans(d,ev):
        if e.name!='moFR_c' or b-a<14: continue
        r,fid,st,s0=struct.unpack_from('<HIII',d,a)
        if fid not in fids: continue
        S['fr']+=1
        S['fs']+= (fid,st) in fs
        S['fid_in_atoms']+= fid in fstamp
        S['stamp_consistent']+= (fid in fstamp and st in fstamp[fid])
        # exact atom identity: tail prefix equals atom seq-tail
        for k in (1,3):
            if b-a>=10+4*k:
                t=struct.unpack_from('<%di'%k,d,a+10)
                if (fid,st)+t in full: S['exact_k%d'%k]+=1
    S['atoms']+=len(A)
print(S)
