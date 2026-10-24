import sys, pickle, struct, re
sys.path.insert(0, '/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/w')
from sldprt import fstream as FS
D = pickle.load(open('/tmp/claude-0/-home-user/7caa9358-7cca-5066-8e9e-a8377adac1a2/scratchpad/fs.pkl', 'rb'))
REF = re.compile(rb'(?=([\x01-\xff][\x80-\x8f]))', re.S)
from sldprt.mfc import CLASSDEF as CD
FLT = {0x3f, 0xbf, 0x40, 0xc0, 0x3e, 0xbe}
def in_float(d, o):
    for w in range(max(0, o - 6), o + 1):
        if w + 8 > len(d): break
        x = abs(struct.unpack_from('<d', d, w)[0])
        if 1e-9 < x < 1e7: return True
    return False
EXT = {4, 5, 6, 43, 44, 45, 46, 47}
def ext_ok(d, o):
    if o + 4 > len(d): return False
    h = d[o + 3]
    return h in (0x00, 0x01, 0xff) or 0x80 <= h <= 0x8f
def run(d, start, lim, fix=None):
    fix = fix or {}
    d = d[:lim]
    ev = [(m.start(), 'def', m.group(2)[0], m.group(3)[:m.group(2)[0]].decode()) for m in CD.finditer(d) if len(m.group(3)) >= m.group(2)[0]]
    ev += [(m.start(), 'ref', struct.unpack_from('<H', d, m.start())[0] & 0x7fff, None) for m in REF.finditer(d)]
    ev.sort()
    cnt = start; classes = {}; i = 0; log = []
    for o, k, a, nm in ev:
        if o < i: continue
        if k == 'def':
            cnt = fix.get(o, cnt)
            classes[cnt] = nm; log.append((o, cnt, nm, 'def')); cnt += 2; i = o + 6 + a
        elif (a in classes or (0 < a < start and (o == i or ext_ok(d, o)))) and (o == i or not in_float(d, o)):
            log.append((o, cnt, classes.get(a, a), 'ref')); cnt += 1; i = o + 2
    return log
def calib(n, S=None):
    d = D[n]; tm = FS.tag_map(d)
    if not tm: return None
    lim = max(m.start() for m in FS.CLASSDEF.finditer(d) if m.group(2)[:m.group(1)[0]].decode() in tm.values()) + 40
    log = run(d, S if S is not None else struct.unpack_from('<I', d, 0)[0], lim)
    idx = {nm: c for (_, c, nm, k) in log if k == 'def'}
    return [(t & 0x7fff) - idx.get(c, 0) for t, c in tm.items()]
