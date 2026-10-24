from common import *
import collections
st=collections.Counter()
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        recs=[]
        for m in MARK.finditer(d,s,e):
            o=m.start()-8; R=m.end()+47
            recs.append((o,u32(d,o),i32(d,o+4),u16(d,R),R))
        pid={k[1]:v for k,v in f.pts.items()}
        filepts={r[2]:r for r in recs if r[3]==0x1e}
        for (a,b),xyz in f.pts.items():
            r=filepts.get(b)
            if r is None: st['pt_missing']+=1; continue
            x,y=f64(d,r[4]+2),f64(d,r[4]+10)
            if abs(x-xyz[0])<1e-9 and abs(y-xyz[1])<1e-9: st['pt_ok']+=1
            else: st['pt_xy_bad']+=1
        st['extra_file_pts']+=len(set(filepts)-set(pid))
print(st)
