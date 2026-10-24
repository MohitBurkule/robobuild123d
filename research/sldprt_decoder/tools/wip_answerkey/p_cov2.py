from common import *
from sldprt import fstream as FS
import collections
R20=re.compile(rb'([\x00-\xff][\x80-\xff])\x00\x00([\x00-\xff][\x80-\xff])([\x00-\xff]{2})(.{4})(.{4})(.{4})',re.S)
for n,D,d in parts():
    if n not in sys.argv[1:]: continue
    ids={h.feature_id for h in FS.feature_headers(d)}
    c=0; k=0
    for m in R20.finditer(d):
        if u32(d,m.start(4)) in ids and u32(d,m.start(6))<100000: c+=20; k+=1
    print(n,len(d),'refs',k,c, round(100*c/len(d),1))
    # zero runs >= 16
    z=sum(len(m.group()) for m in re.finditer(rb'\x00{16,}',d)); print(' zero runs>=16:',round(100*z/len(d),1))
    z=sum(len(m.group()) for m in re.finditer(rb'(?:\xff\xff\xff\xff){2,}',d)); print(' ff runs:',round(100*z/len(d),1))
