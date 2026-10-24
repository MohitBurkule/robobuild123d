import sys,collections,json
sys.path.insert(0,'/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import item_relations as IR, sketch as SK
R='/mnt/project-files/robot-cad/research/sldprt/'
for p in sys.argv[1:]:
    d=IR.feature_stream(R+'revdev/'+p+'.SLDPRT'); j=json.load(open(R+'decoded/'+p+'.json'))
    roles=IR.infer_tags(IR.relation_records(d,0,len(d)))
    sk=sorted(j['sketches'],key=lambda s:s['stream_offset'])
    G=[];RL=[]
    for n,s in enumerate(sk):
        a=s['stream_offset']; b=sk[n+1]['stream_offset'] if n+1<len(sk) else len(d)
        pts,segs,_=SK.parse_records(d,a,b)
        G.append((pts,{(g['kind'],g['rec_id']):g for g in segs}))
        RL.append(IR.relation_records(d,a,b))
    for sh in (-1,0,1):
      for off in (0,-1,1):
        c=collections.Counter()
        for n in range(len(sk)):
            m=n+sh
            if not 0<=m<len(sk): continue
            pts,sid=G[m]
            for r in RL[n]:
                E=[IR._ent(roles.get(t),i+(off if roles.get(t)=='line' else 0),pts,sid) if roles.get(t) else None for t,i in r['slots']]
                c[IR.verify(r['type_code'],E)]+=1
        print(p[:4],'shift',sh,'lineoff',off,c[True],c[False],c[None])
