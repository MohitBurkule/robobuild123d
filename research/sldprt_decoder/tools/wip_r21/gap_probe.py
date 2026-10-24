"""r20 diagnostic: endpoint gaps of a sketch's profile segments."""
import sys, os, io, contextlib, numpy as np
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
import decode_replay as D
part, skn = sys.argv[1], sys.argv[2]
D.R.DEC = D.DO.regen(part); D.R.PART = part
with contextlib.redirect_stdout(io.StringIO()): g = D.DO.GRebuild()
segs, nd = D.seg_list(g, skn)
prof = [s for s in segs if not s.construction]
print('segs', len(segs), 'profile', len(prof), 'dropped', nd, 'types', {t: sum(1 for s in prof if s.type == t) for t in (0, 1)})
P = np.array([p[:2] for s in prof for p in (s.p0, s.p1)]) * 1e3
from scipy.spatial import cKDTree
kd = cKDTree(P); d, i = kd.query(P, 2)
print('nearest other endpoint (mm): max', d[:, 1].max().round(5), 'n > 1e-6', (d[:, 1] > 1e-6).sum(), 'n>1e-3', (d[:, 1] > 1e-3).sum())
print(np.sort(d[:, 1])[-12:].round(5))
r = np.linalg.norm(P, axis=1); print('radius range', r.min().round(3), r.max().round(3))
sk = g.sk[skn]; print('raw entity flags', {f: sum(1 for e in sk['entities'] if e.get('flag') == f) for f in (0, 1, None)}, 'types', {t: sum(1 for e in sk['entities'] if e['type'] == t) for t in set(e['type'] for e in sk['entities'])})
ents, _ = D.R.sketch_entities(sk)
print('sketch_entities', len(ents), {t: sum(1 for e in ents if e['type'] == t) for t in ('line','arc','circle')})
E = sk['entities']
import collections
for f in (0, 1):
    A = [e for e in E if e.get('flag') == f and e['type'] == 'arc']
    pts = np.array([p for e in A for p in (e.get('start'), e.get('end')) if p]) * 1e3
    if len(pts): print('flag', f, 'arcs', len(A), 'with ends', len(pts)//2, 'radius of ends', np.linalg.norm(pts,axis=1).min().round(3), np.linalg.norm(pts,axis=1).max().round(3))
print(E[0].keys()); print([ (e['type'], e.get('flag'), e.get('start'), e.get('end'), e.get('r')) for e in E[:6]])
for sg in segs:
    if not sg.construction: print(sg.id, sg.type, np.round(np.array(sg.p0[:2])*1e3,2), np.round(np.array(sg.p1[:2])*1e3,2), None if sg.c is None else (np.round(np.array(sg.c[:2])*1e3,2), round(sg.r*1e3,3)))
