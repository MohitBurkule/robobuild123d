import sys, os, re, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import streams as ST, validate as V
from sldprt.mfc import CLASSDEF as CD
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
raw=open(R+'revdev/'+sys.argv[1]+'.SLDPRT','rb').read()
fs=V.feature_stream(R+'revdev/'+sys.argv[1]+'.SLDPRT')
for s in ST.all_streams(raw):
    d=s['data']; 
    if d is None: continue
    m=list(CD.finditer(d))
    if m: print(s.get('name'), len(d), len(m), 'first u32', struct.unpack_from('<I',d,0)[0] if len(d)>4 else None, [x.group(3)[:x.group(2)[0]] for x in m[:6]], d is fs)
