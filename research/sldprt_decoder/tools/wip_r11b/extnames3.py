import sys, os, re, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import streams as ST, validate as V, objnum as ON
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
p=R+'revdev/'+sys.argv[1]+'.SLDPRT'; raw=open(p,'rb').read()
fs=V.feature_stream(p); S=struct.unpack_from('<I',fs,0)[0]; print('S',S)
for s in ST.all_streams(raw):
    d=s['data']
    if not d or b'\xff\xff\x01\x00' not in d[:400] or d[:8]==fs[:8]: continue
    out=ON.number(d, start=0)
    if not out: continue
    inc=sum(2 if e.kind=='def' else 1 for e in out)
    print({k:v for k,v in s.items() if k!='data'} if isinstance(s,dict) else '', 'u32_0',struct.unpack_from('<I',d,0)[0],'inc',inc,[e.name for e in out if e.kind=='def'][:4])
