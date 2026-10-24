import sys, pickle, struct, os, re, time
sys.path.insert(0, '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/w')
from sldprt import fstream as FS, objnum as ON, answer_key as AK
D = pickle.load(open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/fs.pkl', 'rb'))
DUMPS = '/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
MOT = re.compile(rb'([\x01-\xff][\x80-\x8f])([\x00-\x01])\x00(..)\1', re.S)
def feat_obj(d, ev):
    return {h.feature_id: (h, ON.object_at(ev, h.offset)) for h in FS.feature_headers(d)[::-1]}
def evalpart(nm, resync=True):
    d = D[nm]
    t = time.time()
    ev, fix = ON.numbering(d) if resync else (ON.number(d), {})
    dt = time.time() - t
    tm = FS.tag_map(d)
    idx = {}
    for e in ev:
        if e.kind == 'def': idx.setdefault(e.name, e.index)
    hand = [(t & 0x7fff) - idx.get(c, -9999) for t, c in list(tm.items())[:2]]
    fo = feat_obj(d, ev)
    pats = []
    p = DUMPS + nm + '.dump.txt'
    if os.path.exists(p):
        top = AK.parse(p).top(); ids = {x.name: x.id for x in top}
        for f in top:
            if f.type in ('MirrorPattern', 'CirPattern', 'LPattern') and f.id in fo:
                h = fo[f.id][0]
                refs = [struct.unpack('<H', m.group(3))[0] for m in MOT.finditer(d, h.offset, h.region_end)]
                par = [fo[ids[pn]][1] for pn, pt in f.parents if pt != 'RefPlane' and ids.get(pn) in fo]
                pats.append((f.name, par, refs[:3]))
    return dict(hand=hand, fixes=len(fix), n=len(ev), dt=round(dt, 2), pats=pats)
if __name__ == '__main__':
    for nm in (sys.argv[1:] or D):
        print(nm[:22], evalpart(nm))
