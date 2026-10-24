from common import *
pn,sn=sys.argv[1],sys.argv[2]
for n,D,d in parts():
    if n!=pn: continue
    for f,s,e in regions(D,d):
        if f.name!=sn: continue
        print(sorted(f.pts.keys())); print([sg['id'] for sg in f.segs])
        for m in MARK.finditer(d,s,e):
            o=m.start()-8; R=m.end()+47
            print(hex(o),u32(d,o),i32(d,o+4),d[o-6:o].hex(),m.group()[5:13].hex(),d[m.end():m.end()+24].hex(),d[R:R+24].hex())
