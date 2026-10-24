import sys, os, re, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import streams as ST, validate as V, objnum as ON
from sldprt.mfc import CLASSDEF as CD
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
raw=open(R+'revdev/'+sys.argv[1]+'.SLDPRT','rb').read()
fs=V.feature_stream(R+'revdev/'+sys.argv[1]+'.SLDPRT'); S=struct.unpack_from('<I',fs,0)[0]
for s in ST.all_streams(raw):
    d=s['data']
    if d and b'moPart_c' in d[:200]:
        for st in (1,):
            out=ON.number(d, start=st)
            cnt = out[-1].index + (2 if out[-1].kind=='def' else 1)
            print('start',st,'end count',cnt,'feature S',S)
            for e in out:
                if e.kind=='def': print('  cls',e.index,'S-%d'%(S-e.index),e.name)
