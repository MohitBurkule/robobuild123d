from sk import *
SLOT=re.compile(rb'([\x00-\xff][\x80-\xfe])([\x00-\xff]{2})\xff\xff\xff\xff',re.S)
CD=re.compile(rb'\xff\xff\x01\x00([\x05-\x40])\x00([A-Za-z_][A-Za-z0-9_]+)')
for n,D,d in parts():
    if n not in ('FS8','RV17 Wedgelet LH','RV01 Chassis','RV09 Prop spacer'): continue
    cds=[(m.start(),m.group(2)[:m.group(1)[0]].decode()) for m in CD.finditer(d)]
    hc=[(p,c) for p,c in cds if 'Handle' in c]
    tags=collections.Counter(); first={}
    for m in SLOT.finditer(d):
        t=u16(d,m.start())
        tags[t]+=1; first.setdefault(t,m.start())
    print(n, len(cds)); print('  ',hc)
    print('  ',sorted((hex(t),hex(first[t]),c) for t,c in tags.items() if c>3)[:40])
