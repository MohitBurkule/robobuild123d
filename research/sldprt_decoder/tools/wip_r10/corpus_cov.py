"""Coverage over corpus/ parts (no dumps): same decoders as validate, templates trained on revdev train half."""
import sys, glob, os, json
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, fstream as FS, objnum as ON, classrec as CR
R='/mnt/project-files/robot-cad/research/sldprt/corpus/'
use2 = len(sys.argv) < 2
res={}
for p in sorted(glob.glob(R+'*.SLDPRT')+glob.glob(R+'*.sldprt')):
    try:
        d=V.feature_stream(p)
        if not d: continue
        dec=FS.decode(d,None); ev,_=ON.numbering(d); hs=FS.feature_headers(d)
        sp=dec.spans+CR.spans(CR.decode(d,ev,{h.feature_id for h in hs}))+[(e.offset,e.end) for e in ev]
        sp+=CR.spans(CR.decode_templates(d,ev,V._templates()))
        if use2: sp+=CR.spans(CR.decode_templates2(d,ev,V._templates2()))
        sp+=[(a,b) for a,b,_ in CR.ps_blobs(d)]
        res[os.path.basename(p)]=(len(d),FS.coverage(d,sp))
    except Exception as ex:
        print('ERR',p,ex)
print(len(res),'mean',round(sum(c for _,c in res.values())/len(res),2),'byte-weighted',round(sum(n*c for n,c in res.values())/sum(n for n,_ in res.values()),2))
