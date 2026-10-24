import sys,os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
src,du=sys.argv[1],sys.argv[2]; sys.argv=[sys.argv[0],src,du]
import esdiag2 as E
from collections import Counter
c=Counter()
for k,(ok,w,g) in E.run().items():
    if g: c[(w[2], g[3], g[1]!=0)]+=1
    else: c['none']+=1
print(src, sorted(c.items(),key=str))
