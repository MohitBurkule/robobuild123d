import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, answer_key as AK
for n in sys.argv[1:]:
    src='../dumps_ab/'+n+'.SLDPRT'; d=V.feature_stream(src); D=AK.parse('../dumps_ab/'+n+'.dump.txt')
    ex={f.id:f for f in D.top() if f.extrude}
    feats=[(h.offset,h.region_end) for h in FS.feature_headers(d)] if hasattr(FS.feature_headers(d)[0],'region_end') else None
    hs=FS.feature_headers(d)
    print(n, 'tag', hex(FS.endspec_tag(d,[(h.offset,h.region_end) for h in hs])))
    for h in hs:
        if h.feature_id in ex:
            print(' feat',h.feature_id,h.offset,h.region_end, 'cd', d.find(FS.CD_ES,h.offset,h.region_end))
            for m in FS.ES_MARK.finditer(d,h.offset,h.region_end):
                print('  mark',m.start(), d[m.start()-46:m.start()+30].hex())
