import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
from sldprt import streams as ST, container as CT
from sldprt.mfc import CLASSDEF as CD
R = '/mnt/project-files/robot-cad/research/sldprt/'
for nm in sys.argv[1:]:
    raw = open(R + 'revdev/' + nm + '.SLDPRT', 'rb').read()
    try:
        names = CT.parse(raw)
    except Exception as e:
        names = None
    for s in ST.all_streams(raw):
        d = s['data']
        cds = [m.group(3)[:m.group(2)[0]] for m in CD.finditer(d[:200000])]
        print(s['offset'], len(d), ST.classify(s), hex(struct.unpack_from('<I', d, 0)[0]), d[:12].hex(), len(cds), cds[:3])
    fd = load()[('revdev', nm)]
    ev, _ = ON.numbering(fd)
    print('final count', ev[-1].obj, hex(ev[-1].obj))
