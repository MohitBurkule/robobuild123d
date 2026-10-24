import sys; sys.path.insert(0, "/mnt/project-files/robot-cad/research/sldprt/tools/wip_r8/")
from common import *
D = load()
for nm in sys.argv[1:]:
    d = D[('revdev', nm)]
    ev0 = ON.number(d)
    ev, fix = ON.numbering(d)
    defs0 = {e.offset: e.index for e in ev0 if e.kind == 'def'}
    defs = [(e.offset, e.index, e.name) for e in ev if e.kind == 'def']
    print(nm, len(d), 'defs', len(defs), 'fixes', len(fix), 'last def', defs[-1][0])
    prev = None
    for o, i, n in defs:
        # implied drift: forced minus what plain counting from previous def would give
        if o in fix: print('  fix', o, n, 'idx', i)
