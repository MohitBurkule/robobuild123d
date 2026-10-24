from common import *
MK=re.compile(re.escape(b'\xff\xff\x00\x00\x03\xff\xff\xff\xff' + b'\x00' * 6 + b'\x80\xbf'))
CD=b'\xff\xff\x01\x00\x0b\x00moEndSpec_c'
for n,D,d in parts():
    for f,s,e in regions(D,d):
        if not f.extrude: continue
        x=f.extrude
        cds=[m.start()+len(CD)-2 for m in re.finditer(re.escape(CD),d[s:e])]
        anc=[s+c for c in cds]
        for m in MK.finditer(d,s,e):
            for k in (44,46):
                t=m.start()-k
                if u16(d,t)&0x8000 and d[t+2:t+4]==b'\x00\x00': anc.append(t)
        anc=sorted(set(anc))
        print(n[:8],f.name[:14],'e1=%d e2=%d both=%d rev=%d d1=%g d2=%g'%(x['end1'],x['end2'],x['both'],x['reverse'],x['d1'],x['d2']),[ (hex(a),d[a:a+24].hex()) for a in anc][:3])
