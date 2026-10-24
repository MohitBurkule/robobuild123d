import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for n,D,d in parts():
    ex={f.id:f for f in D.top() if f.extrude}
    dec=FS.decode(d,set(ex))
    for fid,f in ex.items():
        x=f.extrude
        if x['both'] and x['d2']:
            es=dec.endspecs.get(fid); print(n[:12],f.name,x,'dims',f.dims,'got',es and (es.depth1,es.depth2,es.end1,es.end2),'dec dims',dec.dims.get(fid))
