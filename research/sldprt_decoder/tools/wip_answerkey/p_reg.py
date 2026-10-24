from sk import *
from sldprt import item_relations as IR
want=sys.argv[1:] 
for n,D,d in parts():
    if want and n not in want: continue
    tm=tag_map(d)
    R=[m.start() for m in re.finditer(rb'moSketchRegion_c',d)]
    rt=None
    for f,s,e in regions(D,d):
        if f.type!='ProfileFeature': continue
        P,L,C,O=parse(d,s,e)
        print('==',n,f.name,'contours:',[(c[0],[x for x in c[1]]) for c in f.contours])
        print('   lines',[(r['idx'],r['id'],r.get('flag')) for r in L],'arcs',[(r['idx'],r['id'],r.get('flag')) for r in C])
        for m in re.finditer(rb'moSketchRegion_c',d[s:e]):
            j=s+m.end()
            print('   REG',hex(j),d[j:j+4].hex(), [ (tm.get(t,hex(t)) if isinstance(t,int) else t,i) for t,i in IR.read_slots(d,j+4,200)[0]])
