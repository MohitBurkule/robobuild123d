import sys, pickle, json
sys.path.insert(0, '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/w')
from sldprt import fstream as FS, objnum as ON
D = pickle.load(open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/fs.pkl', 'rb'))
tot = {}; parts = {}; allb = une = struct_b = 0
for nm, d in D.items():
    ev, _ = ON.numbering(d)
    hs = FS.feature_headers(d)
    objs = ON.objects(d, ev)
    try:
        spans = FS.decode(d).spans
    except Exception as ex:
        print("decode failed", nm, ex); spans = []
    cb = ON.class_bytes(d, objs, spans)
    allb += len(d)
    first = ev[0].offset if ev else len(d)
    struct_b += sum(o.end - o.start for o in objs if not o.name.startswith('ext['))
    for k, (t, u, n) in cb.items():
        x = tot.setdefault(k, [0, 0, 0]); x[0] += t; x[1] += u; x[2] += n
        parts.setdefault(k, set()).add(nm)
    une += sum(u for t, u, n in cb.values())
print('bytes', allb, 'unexplained', une, 'struct(named class)', struct_b, round(100 * struct_b / allb, 2))
rows = sorted(tot.items(), key=lambda x: -x[1][1])
for k, (t, u, n) in rows[:60]:
    print(f'{k}|{u}|{100*u/une:.1f}|{t}|{n}|{len(parts[k])}')
json.dump({k: v + [len(parts[k])] for k, v in tot.items()}, open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/cls7.json', 'w'))
