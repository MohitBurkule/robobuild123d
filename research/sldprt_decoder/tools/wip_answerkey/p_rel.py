from sk import *
from sldprt import item_relations as IR
pn,sn=sys.argv[1],sys.argv[2]
for n,D,d in parts():
    if n!=pn: continue
    for f,s,e in regions(D,d):
        if f.name!=sn: continue
        for r in f.rels: print('D',r)
        for r in IR.relation_records(d,s,e): print('F',hex(r['pos']),r['type_code'],r['flag'],[(hex(t) if isinstance(t,int) else t,i) for t,i in r['slots']])
