import sys, pickle, struct
sys.path.insert(0, '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/w')
from collections import Counter
from sldprt import fstream as FS, objnum as ON
D = pickle.load(open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/fs.pkl', 'rb'))
def frs(d, ev):
    out = []
    for e in ev:
        if e.name == 'moFR_c':
            o = e.end if e.kind == 'new' else e.end
            if o + 10 <= len(d):
                out.append((e.offset, struct.unpack_from('<H', d, o)[0], struct.unpack_from('<I', d, o + 2)[0]))
    return out
if __name__ == '__main__':
    for nm in sorted(D):
        d = D[nm]; ev, _ = ON.numbering(d); fo = ON.feature_objects(d, FS.feature_headers(d), ev)
        c = Counter()
        for o, r, fid in frs(d, ev):
            if fid in fo: c[r - fo[fid][1]] += 1
            else: c['nofid'] += 1
        print(nm[:22], sum(c.values()), c.most_common(5))
