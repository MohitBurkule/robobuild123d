import sys
sys.path.insert(0, '/mnt/project-files/robot-cad/research/sldprt/tools/')
from sldprt import validate as V, fstream as FS, answer_key as AK
R = '/mnt/project-files/robot-cad/research/sldprt/'
n = sys.argv[1] if len(sys.argv) > 1 else 'RV26 Base Panel'
skname = sys.argv[2] if len(sys.argv) > 2 else 'Sketch1'
d = V.feature_stream(R + 'revdev/' + n + '.SLDPRT')
A = AK.parse(R + 'dumps_v2/' + n + '.dump.txt')
dec = FS.decode(d)
S = [f for f in A.top() if f.name == skname][0]
X = dec.sketches[S.id]; sk = X['sketch']
P = lambda i: sk.points[i].xy if i is not None and i < len(sk.points) else None
for g in sk.lines + sk.arcs:
    print(g.serial, g.kind, g.real, P(g.start), P(g.end), P(getattr(g, 'centre', None)) if g.kind == 'arc' else '')
for c in X['choosers']:
    for ct in c.contours: print('contour', ct.serials, ct.rid, ct.how)
for r in X['regions']: print('region', r.rid, r.serials)
faces = FS.planar_faces(sk)
print('faces', [(round(a * 1e6, 3), fs) for a, fs, _ in faces])
C = [ct.serials for c in X['choosers'] for ct in c.contours]
print('expand', sorted(FS.face_expand(sk, C)))
for a, fs, probes in faces:
    if a > 0 and 14 in fs:
        ce, _ = FS._loop_geom(sk, C[1])
        print([(sr, FS._inside(pt, ce)) for sr, pt in probes if sr in C[1]])
f = [f for f in A.top() if f.type in V.EXTRUDE_TYPES and any(p == skname for p, t in f.parents)][0]
ser = {}
for s_ in sk.lines: ser[(0,) + s_.api_id] = s_.serial
for s_ in sk.arcs: ser[(1,) + s_.api_id] = s_.serial
ev = sorted(ser.get((sg['type'],) + sg['id']) for sg in S.segs if not sg['constr'] and V.seg_has_face(sg, S.sketch_to_model, f.faces) and ser.get((sg['type'],) + sg['id']) is not None)
print('evidence', ev)
