import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
want=sys.argv[1]; skn=sys.argv[2]; a0=int(sys.argv[3]); a1=int(sys.argv[4])
for n,D,d in parts():
    if not n.startswith(want): continue
    S=[f for f in D.top() if f.name==skn][0]
    for m in FS.EDGE_SIG.finditer(d,a0,a1):
        q=m.start()
        refs=[(u32(d,x.start(1)),u32(d,x.start(3))) for x in FS.EREF.finditer(d,q,q+400)][:4]
        print(q, d[q-8:q].hex(' '), d[q+12:q+14].hex(), refs)
    print('sketch id',S.id)
