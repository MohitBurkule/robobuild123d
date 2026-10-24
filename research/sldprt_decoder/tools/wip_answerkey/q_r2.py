import sys,os;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from common import *
from sldprt import fstream as FS
for n,D,d in parts():
    if not n.startswith(('RV01','RV04','RV06')): continue
    hidx=FS.header_index(d)
    for f in D.sketches():
        h=hidx[f.id]
        i=d.find(FS.CD_ONE,h.offset,h.region_end)
        while i>=0:
            print(n[:5],f.name,i,d[i-24:i].hex(' '),'|',d[i+20:i+40].hex(' '))
            i=d.find(FS.CD_ONE,i+1,h.region_end)
