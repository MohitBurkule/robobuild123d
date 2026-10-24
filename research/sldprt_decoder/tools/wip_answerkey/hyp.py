import sys,collections,json,struct
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import item_relations as IR, sketch as SK
R='/mnt/project-files/robot-cad/research/sldprt/'
for p in sys.argv[1:]:
    d=IR.feature_stream(R+'revdev/'+p+'.SLDPRT'); j=json.load(open(R+'decoded/'+p+'.json'))
    roles=IR.infer_tags(IR.relation_records(d,0,len(d)))
    sk=sorted([s for s in j['sketches']],key=lambda s:s['stream_offset'])
    C=collections.Counter()
    for n,s in enumerate(sk):
        a=s['stream_offset']; b=sk[n+1]['stream_offset'] if n+1<len(sk) else len(d)
        pts,segs,_=SK.parse_records(d,a,b)
        for g in segs: g['a']=struct.unpack_from('<i',d,g['pos']-8)[0]
        H={'rec':{g['rec_id']:g for g in segs},'fi':dict(enumerate(segs)),'fi1':{i+1:g for i,g in enumerate(segs)},'a':{g['a']:g for g in segs}}
        for r in IR.relation_records(d,a,b):
            if r['type_code'] in (4,5) and len(r['slots'])==1 and roles.get(r['slots'][0][0])=='line':
                for h,m in H.items():
                    e=IR._ent('line',r['slots'][0][1],pts,m)
                    C[(h,IR.verify(r['type_code'],[e]))]+=1
    print(p,sorted(C.items(),key=str))
