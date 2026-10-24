import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for n,D,d in parts():
    if not n.startswith(sys.argv[1]): continue
    hidx=FS.header_index(d)
    S=[f for f in D.top() if f.name==sys.argv[2]][0]
    print('users',[f.name for f in D.top() if any(p==S.name for p,_ in f.parents)])
    cnt=collections.Counter() if False else {}
    for h in FS.feature_headers(d):
        k=sum(1 for m in FS.EREF.finditer(d,h.offset,h.region_end) if u32(d,m.start(1))==S.id)
        if k: print(h.name,h.feature_id,h.offset,h.region_end,k, d.count(FS.CC_NAME,h.offset,h.region_end))
    break
