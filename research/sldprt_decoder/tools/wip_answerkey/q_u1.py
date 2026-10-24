import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for k,(n,D,d) in enumerate(parts()):
    ids={x.name:x.id for x in D.top()}
    hidx=FS.header_index(d)
    for f in D.top():
        x=f.extrude
        if not x or not ({int(x['end1']),int(x['end2'])}&{3,4,5,7}): continue
        h=hidx[f.id]
        refs=FS.referenced_feature_ids(d,h.offset,h.region_end,set(ids.values()))
        print('tv'[k%2],n[:12],f.name,f.id,int(x['end1']),int(x['end2']),'par',[(p,t,ids.get(p)) for p,t in f.parents],'refs',dict(refs))
