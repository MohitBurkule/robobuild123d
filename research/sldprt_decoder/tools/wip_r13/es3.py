import sys, os, time, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, objnum as ON
for n in sys.argv[1:]:
    d=V.feature_stream('../dumps_ab/'+n+'.SLDPRT'); t=time.time()
    ev,_=ON.numbering(d)
    k=[e.cls for e in ev if e.kind=='def' and e.name=='moEndSpec_c']
    print(n, time.time()-t, k, k and hex(0x8000|k[0]))
    if k:
        tg=struct.pack('<H',0x8000|k[0])
        i=0
        while (i:=d.find(tg,i+1))>0: print('  ',i,d[i:i+30].hex())
