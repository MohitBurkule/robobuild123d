import sys, os, glob, struct
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, classrec as CR
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
def cstr(b, i):
    if b[i:i+3] != b'\xff\xfe\xff': return None
    n = b[i+3]; 
    if n == 0xff: n = struct.unpack_from('<H', b, i+4)[0]; return i+6+2*n
    return i+4+2*n
tails = Counter(); shown=0
for p in sorted(glob.glob(R + 'dumps_v2/*.dump.txt')):
    n = os.path.basename(p)[:-9]; d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev,_=ON.numbering(d); S=struct.unpack_from('<I',d,0)[0]
    for e,a,b in CR._obj_spans(d,ev):
        if e.name or e.kind!='new': continue
        j = cstr(d, a)
        if j is None: continue
        t = d[j:b]
        if t[8:9]==b'\x40':
            tails[len(t)]+=1
            if shown<int(sys.argv[1]): shown+=1; print(n[:12],'S-%d'%(S-e.cls), len(t), t.hex(' ',4))
print(tails.most_common(10))
