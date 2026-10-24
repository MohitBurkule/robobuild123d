import sys, os, glob
from collections import Counter
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from sldprt import validate as V, fstream as FS
C = Counter()
for p in sys.argv[2:]:
    d = V.feature_stream(p)
    if d is None: continue
    try: dec = FS.decode(d, set())
    except Exception as ex: print('ERR', p, ex); continue
    for sid, X in dec.sketches.items():
        regs = X['regions']
        for c in X['choosers']:
            for ct in c.contours:
                C[ct.how] += 1
                if ct.rid is None:
                    rs = [r.serials for r in regs if r.edges]
                    cs = set(ct.serials)
                    sub = [r for r in rs if set(r) <= cs]
                    union = set(x for r in sub for x in r) == cs and len(sub) > 1
                    sup = [r for r in rs if cs < set(r)]
                    k = 'union_of_regions' if union else 'subset_of_region' if sup else 'no_regions' if not rs else \
                        'stubs=%d' % sum(not r.edges for r in regs) if not ct.serials else 'empty_contour' if not ct.serials else 'other'
                    if not ct.serials: k = 'empty_contour,stubs=%d' % sum(not r.edges for r in regs)
                    C[k] += 1
                    if int(sys.argv[1]): print(os.path.basename(p)[:25], sid, k, 'ct', ct.serials[:12], 'regs', [r[:8] for r in rs][:6], 'stubs', [r.rid for r in regs if not r.edges])
print(C)
