"""r21 diagnostic: replay up to the feature before a blend, then for the blend's dumps_v4_edges hint
edges report which OCC variants (chain_blend) build the whole set, per tangent chain and per edge."""
import sys, os, io, contextlib, time
import numpy as np
os.environ.setdefault('R15_OUT', os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('R19_BEAM', '1'); os.environ.setdefault('R16_PASSES', '1')
import decode_replay as D, chain_blend as CB
part, blend = sys.argv[1], sys.argv[2]
D.LOG.clear(); D.R.LOG.clear(); D.R.DEC = D.DO.regen(part); D.R.PART = part
ref = D.oracle_for(part); ref.init_points()
rb = D.OracleReplay(part, ref)
fs = rb.part.features; i = [f.name for f in fs].index(blend); F = fs[i]; rb.part.features = fs[:i]
with contextlib.redirect_stdout(io.StringIO()): rb.run()
H = rb.edge_hints().get(blend); bp = D.DP.blend_params(F); size = bp[1] * D.MM; kind = bp[0]
body = D.FD._one(rb.body); E = body.edges()
sel = []
for h in H:
    k, s_, e_, m_, L, sep = h
    s_, e_, m_ = (np.array(x) * D.MM for x in (s_, e_, m_))
    best = None
    for j, e in enumerate(E):
        try:
            p0, p1 = (np.array(tuple(e.position_at(t))) for t in (0, 1))
            d = min(np.linalg.norm(p0 - s_) + np.linalg.norm(p1 - e_), np.linalg.norm(p1 - s_) + np.linalg.norm(p0 - e_)) / 2
        except Exception: continue
        if best is None or d < best[0]: best = (d, j)
    if best and best[0] < 0.05 + (1.5 * size if k.startswith('derived') else 0): sel.append(best[1])
sel = sorted(set(sel)); es = [E[j] for j in sel]
print(blend, kind, size, 'hints', len(H), 'matched edges', len(es))
v0 = body.volume
def tryop(f):
    t = time.time()
    try: b = f(); ok = CB._ok(b, v0)
    except Exception as ex: ok = repr(ex)[:60]
    return ok, round(time.time() - t, 2)
print('build123d all', tryop(lambda: body.fillet(size, es) if kind == 'fillet' else body.chamfer(size, None, es)))
for tag, b in CB.variants(body, es, size, kind, v0): print('variant OK', tag)
# tangent chains: connected components of the selected edges
import collections
adj = collections.defaultdict(set)
for a in range(len(es)):
    for b_ in range(a + 1, len(es)):
        pa = [es[a].position_at(0), es[a].position_at(1)]; pb = [es[b_].position_at(0), es[b_].position_at(1)]
        if min((x - y).length for x in pa for y in pb) < 1e-4: adj[a].add(b_); adj[b_].add(a)
seen = set(); comps = []
for a in range(len(es)):
    if a in seen: continue
    st = [a]; c = []
    while st:
        x = st.pop()
        if x in seen: continue
        seen.add(x); c.append(x); st += list(adj[x])
    comps.append(c)
print('chains', [len(c) for c in comps])
for c in comps:
    ce = [es[x] for x in c]
    print(' chain', len(c), 'all', tryop(lambda: CB._fillet(body, CB.order_chain(ce), size) if kind == 'fillet' else CB._chamfer(body, ce, size)),
          'single edges ok', sum(1 for e in ce if tryop(lambda: CB._fillet(body, [e], size) if kind == 'fillet' else CB._chamfer(body, [e], size))[0] is True))
