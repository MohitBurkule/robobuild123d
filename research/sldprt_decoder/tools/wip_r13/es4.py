import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS
for n in sys.argv[1:]:
    d=V.feature_stream('../dumps_ab/'+n+'.SLDPRT'); c=d.find(FS.CD_ES)+len(FS.CD_ES)-2
    print(n[:34].ljust(34), d[c:c+48].hex())
