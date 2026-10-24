import sys,collections,json
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import item_relations as IR, sketch as SK
R='/mnt/project-files/robot-cad/research/sldprt/'
for p in sys.argv[1:]:
    d=IR.feature_stream(R+'revdev/'+p+'.SLDPRT'); j=json.load(open(R+'decoded/'+p+'.json'))
    roles=IR.infer_tags(IR.relation_records(d,0,len(d)))
    sk=sorted(j['sketches'],key=lambda s:s['stream_offset'])
    for n,s in enumerate(sk):
        a=s['stream_offset']; b=sk[n+1]['stream_offset'] if n+1<len(sk) else len(d)
        pts,segs,_=SK.parse_records(d,a,b)
        sid={(g['kind'],g['rec_id']):g for g in segs}
        res=[]
        for lo in (0,1):
          for po in (0,1):
            c=collections.Counter()
            for r in IR.relation_records(d,a,b):
                E=[]
                for t,i in r['slots']:
                    ro=roles.get(t)
                    E.append(IR._ent(ro,i+(lo if ro in('line','arc') else po),pts,sid) if ro else None)
                c[IR.verify(r['type_code'],E)]+=1
            res.append('%d%d:%d/%d'%(lo,po,c[True],c[False]))
        print(p[:4],s['name'],' '.join(res))
