"""Round 13: decode rebuild_dump/sw_runs/RV01_rebuilt_run5.SLDPRT and compare extrusions
with the macro log (rebuild_dump/sw_run5_log.txt)."""
import sys, os, re
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../rebuild_dump/')
d = V.feature_stream(R + 'sw_runs/RV01_rebuilt_run5.SLDPRT')
want = {}
for l in open(R + 'sw_run5_log.txt'):
    m = re.search(r'OK\s+((?:Boss|Cut)-Extrude\d+) (\w+) d1=([\d.]+) d2=([\d.]+) rev=(\w+)', l)
    if m: want[m.group(1)] = (m.group(2), float(m.group(3)), float(m.group(4)), m.group(5) == 'True')
hs = FS.feature_headers(d); ids = {h.feature_id for h in hs if h.name in want}
dec = FS.decode(d, ids); ok = n = 0
names = [h.name for h in hs]
for h in hs:
    if h.name not in want or h.feature_id not in dec.endspecs: continue
    es = dec.endspecs[h.feature_id]; w = want[h.name]; n += 1
    kind = ('both_thru' if es.both else 'thru') if es.end1 == 1 else 'two' if es.both else 'one'
    good = kind == w[0] and (w[0] in ('both_thru', 'thru') or abs((es.depth1 or 0) - w[1]) < 1e-9) and (not es.both or w[0]=='both_thru' or abs((es.depth2 or 0) - w[2]) < 1e-9)
    good = good and bool(es.reverse) == w[3]
    ok += good
    print(('OK ' if good else 'BAD'), h.name, w, '->', kind, es.end1, es.end2, es.reverse, es.depth1, es.depth2)
print('extrusions', ok, '/', n, 'of', len(want), 'in log; headers found', sum(x in names for x in want))
