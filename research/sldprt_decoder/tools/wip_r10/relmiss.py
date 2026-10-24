import sys, os, glob, pickle
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter
from sldprt import validate as V, fstream as FS, answer_key as AK
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'; D='/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
names = sorted(os.path.basename(p)[:-9] for p in glob.glob(D+'*.dump.txt'))
fp=Counter(); fn=Counter(); ex=[]
for k,n in enumerate(names):
    if len(sys.argv)>1 and k%2!=int(sys.argv[1]): continue
    d=V.feature_stream(R+n+'.SLDPRT'); A=AK.parse(D+n+'.dump.txt')
    dec=V.evaluate(d,A,V.Acc())


    top=A.top()
    for f in top:
        if f.type!='ProfileFeature' or f.id not in dec.sketches: continue
        X=dec.sketches[f.id]
        allr=X['relations']
        got=Counter((r.type,tuple(sorted(x[1] for x in r.ents))) for r in FS.api_relations(allr))
        want=Counter((t,tuple(sorted(es))) for t,es in f.rels)
        for kk,v in got.items():
            if v>want.get(kk,0):
                fp[kk[0]]+=v-want.get(kk,0); ex.append(('FP',n,f.name if hasattr(f,'name') else f.id,kk))
        for kk,v in want.items():
            if v>got.get(kk,0):
                fn[kk[0]]+=v-got.get(kk,0)
                hid=[ (r.type,r.api_visible,r.dimension) for r in allr if tuple(sorted(x[1] for x in r.ents))==kk[1]]
                ex.append(('FN',n,f.name if hasattr(f,'name') else f.id,kk,hid))
print('FP',fp.most_common()); print('FN',fn.most_common())
for e in ex[:80]: print(e)
