import sys, os, json
sys.path.insert(0, '..')
from sldprt import validate as V, objnum as ON, fstream as FS, answer_key as AK
n = sys.argv[1]; R = '../../'
top = AK.parse(R + 'dumps_v2/' + n + '.dump.txt').top()
d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
ev, fix = ON.numbering(d); heads = FS.feature_headers(d); hidx = FS.header_index(d)
fobj = ON.feature_objects(d, heads, ev)
nm = {f.id: f.name for f in top}
for fid, (h, i, c) in sorted(fobj.items(), key=lambda x: x[1][0].offset): print('F', fid, nm.get(fid), h.offset, i, c)
for f in top:
    if f.type in V.PATTERN_TYPES and f.id in hidx:
        refs = ON.seed_list(d, hidx[f.id]); print('PAT', f.name, [s for s in getattr(f,'seeds',[])], refs, ON.resolve_objects(refs, fobj, hidx[f.id].offset))
print('resid', ON.numbering.residuals)
