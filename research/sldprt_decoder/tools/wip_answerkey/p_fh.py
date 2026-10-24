from common import *
from sldprt import fstream as FS
import collections
M=re.compile(re.escape(b'\xff\xff\x00\x00\x03'+b'\xff'*8+b'\x00\x00\x80\xbf'))
c=collections.Counter(); c2=collections.Counter(); ex=[]
for n,D,d in parts():
    for h in FS.feature_headers(d):
        m=M.search(d,h.end,min(h.region_end,h.end+400))
        if not m: c['nomark']+=1; continue
        c[m.start()-h.end]+=1
        k=d.find(b'\x8b\x30\x05\x00',m.end(),m.end()+80)
        c2[k-m.end() if k>=0 else None]+=1
        if len(ex)<3: ex.append(d[h.end:m.end()+80].hex(' '))
print(c.most_common(12)); print(c2.most_common(8))
for x in ex: print(x)
