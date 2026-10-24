import sys, os, glob
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from collections import Counter
from sldprt import validate as V, fstream as FS, answer_key as AK
R='/mnt/project-files/robot-cad/research/sldprt/revdev/'; D='/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
names = sorted(os.path.basename(p)[:-9] for p in glob.glob(D+'*.dump.txt'))
for k,n in enumerate(names):
    acc=V.Acc(); d=V.feature_stream(R+n+'.SLDPRT'); A=AK.parse(D+n+'.dump.txt'); V.evaluate(d,A,acc)
    t=acc.table() if hasattr(acc,'table') else {}
    p=t.get('Relation.type+entities (precision)',{}); r=t.get('Relation.type+entities (recall)',{})
    print(k%2, n[:30], p.get('ok'),p.get('n'), r.get('ok'), r.get('n'))
