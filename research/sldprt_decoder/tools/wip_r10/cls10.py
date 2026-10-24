"""Unexplained bytes per class with all round-10 decoders (revdev dump parts), same spans as validate."""
import sys, os, glob, json
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter
from sldprt import validate as V, fstream as FS, objnum as ON, classrec as CR, answer_key as AK
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'; D='/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
tot=Counter(); une=Counter(); cnt=Counter(); gl=[0,0]
for p in sorted(glob.glob(D+'*.dump.txt')):
    n=os.path.basename(p)[:-9]
    d=V.feature_stream(R+n+'.SLDPRT')
    A=AK.parse(p)
    top=A.top(); dec=FS.decode(d,{f.id for f in top if f.extrude})
    ev,_=ON.numbering(d); hs=FS.feature_headers(d)
    recs=CR.decode(d,ev,{h.feature_id for h in hs})
    sp=dec.spans+CR.spans(recs)+[(e.offset,e.end) for e in ev]
    tm=V._templates(); sp+=CR.spans(CR.decode_templates(d,ev,tm))
    sp+=CR.spans(CR.decode_templates2(d,ev,V._templates2()))
    sp+=[(a,b) for a,b,_ in CR.ps_blobs(d)]
    gl[0]+=len(d)*FS.coverage(d,sp)/100; gl[1]+=len(d)
    objs=ON.objects(d,ev,hs)
    for k,(t,u,c) in ON.class_bytes(d,objs,sp).items():
        tot[k]+=t; une[k]+=u; cnt[k]+=c
print('byte-weighted coverage', round(100*gl[0]/gl[1],2), 'unexplained', gl[1]-gl[0])
out=[(k,une[k],tot[k],cnt[k]) for k,_ in une.most_common(30)]
for x in out: print(x)
json.dump(out,open('/mnt/project-files/robot-cad/research/sldprt/tools/wip_r10/cls10.json','w'),indent=1)
