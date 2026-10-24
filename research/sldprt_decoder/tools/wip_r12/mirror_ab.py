import sys, os, struct, glob
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS, answer_key as AK
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../')
for p in sys.argv[1:]:
    p, dp = p.split('|') if '|' in p else (p, p[:-7] + '.dump.txt')
    D = AK.parse(dp); top = D.top(); ids = {f.name: f.id for f in top}
    d = V.feature_stream(p)
    if d is None: continue
    hidx = FS.header_index(d)
    for f in top:
        if f.type != 'MirrorPattern' or f.id not in hidx: continue
        h = hidx[f.id]; mp = FS.mirror_plane_ref(d, h, set(ids.values()))
        pl = [(pn, ids.get(pn)) for pn, pt in f.parents if pt == 'RefPlane']
        print(os.path.basename(p), f.name, 'truth', pl, 'got', mp and mp[0], 'rend-off', mp and h.region_end - mp[3])
        for pn, fid in pl:
            q = d.find(struct.pack('<I', fid), h.offset, h.region_end)
            while q >= 0:
                print('    fid@', q - h.offset, h.region_end - q, d[q - 8:q + 12].hex()); q = d.find(struct.pack('<I', fid), q + 1, h.region_end)
