"""Round 12: exact pattern seed refs (drift 0) on dumps_v2 + dumps_corpus; argv[1] optional variant module to import first."""
import sys, os, glob, json, importlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sldprt import validate as V, objnum as ON, fstream as FS, answer_key as AK
if len(sys.argv) > 1: importlib.import_module(sys.argv[1])
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
LST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'seedfiles_ab.json')
if os.path.exists(LST): todo = json.load(open(LST))
else:
    todo = []
    for src, dd in (('dumps_ab', 'dumps_ab'),):
        for p in sorted(glob.glob(R + dd + '/*.dump.txt')):
            n = os.path.basename(p)[:-9]
            if any(f.type in V.PATTERN_TYPES for f in AK.parse(p).top()) and os.path.exists(R + src + '/' + n + '.SLDPRT'):
                todo.append((dd, src, n))
    json.dump(todo, open(LST, 'w'))
tot = {}
for dd, src, n in todo:
    top = AK.parse(R + dd + '/' + n + '.dump.txt').top()
    d = V.feature_stream(R + src + '/' + n + '.SLDPRT')
    if d is None: continue
    ev, _ = ON.numbering(d); heads = FS.feature_headers(d); hidx = FS.header_index(d)
    fobj = ON.feature_objects(d, heads, ev)
    dr = []
    for f in top:
        if f.type in V.PATTERN_TYPES and f.id in hidx:
            dr += [x[1] for x in ON.resolve_objects(ON.seed_list(d, hidx[f.id]), fobj, hidx[f.id].offset) if x]
    t = tot.setdefault(dd, [0, 0]); t[0] += sum(x == 0 for x in dr); t[1] += len(dr)
    print(dd, n[:30], 'res', ON.numbering.residual, dr, flush=True)
print('EXACT', tot)
