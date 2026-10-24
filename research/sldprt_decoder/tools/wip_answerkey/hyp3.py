import sys,collections,json
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import item_relations as IR, sketch as SK
R='/mnt/project-files/robot-cad/research/sldprt/'
for p in sys.argv[1:]:
    d=IR.feature_stream(R+'revdev/'+p+'.SLDPRT'); j=json.load(open(R+'decoded/'+p+'.json'))
    roles=IR.infer_tags(IR.relation_records(d,0,len(d)))
    sk=sorted(j['sketches'],key=lambda s:s['stream_offset'])
    per=collections.Counter()
    for n,s in enumerate(sk):
        a=s['stream_offset']; b=sk[n+1]['stream_offset'] if n+1<len(sk) else len(d)
        pts,segs,_=SK.parse_records(d,a,b)
        sid={(g['kind'],g['rec_id']):g for g in segs}
        c=collections.Counter()
        for r in IR.relation_records(d,a,b):
            E=[IR._ent(roles.get(t),i,pts,sid) if roles.get(t) else None for t,i in r['slots']]
            c[IR.verify(r['type_code'],E)]+=1
        dup=len(segs)-len(sid)
        print(p[:4],s['name'],len(pts),len(segs),'dup',dup,'T',c[True],'F',c[False],'?',c[None])
