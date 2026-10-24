import sys, os, glob, struct
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, objnum as ON, fstream as FS, answer_key as AK, item_structs as IS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
MODE = sys.argv[1]
if MODE == 'new':
    old = ON.ext_ok
    def ext_ok(d, o):
        if old(d, o): return True
        e = min(len(d), o + 2 + 400)
        return bool(IS.hist_display(d, o + 2, e, ()) or IS.named_item(d, o + 2, e, ()))
    ON.ext_ok = ext_ok
for n in sys.argv[2:]:
    p = R + 'dumps_v2/' + n + '.dump.txt'; D = AK.parse(p); top = D.top()
    d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT'); ev, _ = ON.numbering(d); heads = FS.feature_headers(d); hidx = FS.header_index(d)
    fobj = ON.feature_objects(d, heads, ev)
    out = []
    for f in top:
        if f.type in V.PATTERN_TYPES and f.id in hidx:
            out += [x[1] for x in ON.resolve_objects(ON.seed_list(d, hidx[f.id]), fobj, hidx[f.id].offset) if x]
    print(MODE, n, 'residual', ON.numbering.residual, 'drifts', out)
