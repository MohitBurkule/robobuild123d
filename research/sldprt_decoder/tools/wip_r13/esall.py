import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
sys.argv=[sys.argv[0],'../corpus','../dumps_corpus']
import esdiag2 as E
from sldprt import fstream as FS
a=E.run()
FS.ES_TAG_MAX=1<<16; FS.ES_TAG_MIN=0; FS.ES_TIE_FIRST=False; FS.ES_CD_FIRST=False; FS.ES_DIR0_BOTH=False
b=E.run(); print(sum(v[0] for v in a.values()), sum(v[0] for v in b.values()))
for k in a:
    if a[k][0]!=b[k][0]: print(k,a[k],b[k][2])
