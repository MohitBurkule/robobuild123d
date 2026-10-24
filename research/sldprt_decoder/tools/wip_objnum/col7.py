import sys, pickle, json
sys.path.insert(0, '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/w')
from sldprt import objnum as ON, colstats as CS
D = pickle.load(open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/fs.pkl', 'rb'))
names = sorted(D)
train = [(n, D[n], ON.numbering(D[n])[0]) for k, n in enumerate(names) if k % 2 == 0]
G = CS.gather(train, 48)
res = {}
for c, bodies in sorted(G.items(), key=lambda x: -len(x[1])):
    if len(bodies) < 8: continue
    res[c] = {'n': len(bodies), 'fields': CS.fields(bodies, 48)}
json.dump(res, open(sys.argv[1], 'w'), indent=0)
for c in list(res)[:40]:
    print(c, res[c]['n'], ' '.join(f'{o}:{t}{("="+v) if v else ""}' for o, l, t, v in res[c]['fields'][:10]))
