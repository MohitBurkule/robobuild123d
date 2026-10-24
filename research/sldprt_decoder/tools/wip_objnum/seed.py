exec(open('g.py').read())
import bisect
from sldprt import answer_key as AK
DUMPS = '/mnt/project-files/robot-cad/research/sldprt/dumps_v2/'
def objidx(d, log):
    """feature id -> (header, obj index) ; obj index = index of the def/ref tag just before the header CString minus 0x8004 tag"""
    pos = [o for o, c, n, k in log]
    out = {}
    for h in FS.feature_headers(d):
        j = bisect.bisect_left(pos, h.offset) - 1
        # skip the 0x8004-style sub-object tag that directly precedes the name
        while j >= 0 and log[j][3] == 'ref' and isinstance(log[j][2], int) and log[j][0] + 2 == h.offset: j -= 1
        if j < 0: continue
        o, c, n, k = log[j]
        oi = c + 1 if k == 'def' else c
        out.setdefault(h.feature_id, (h, oi, n))
    return out
PT = ('CirPattern', 'LPattern', 'MirrorPattern', 'LocalCirPattern', 'LocalLPattern', 'MirrorSolid', 'SketchPattern', 'TablePattern', 'CurvePattern')
def pattern_cases(nm):
    Dm = AK.parse(open(DUMPS + nm + '.dump.txt', encoding='utf-8', errors='replace').read(), nm) if hasattr(AK, 'parse') else AK.load(DUMPS + nm + '.dump.txt')
    return Dm
import re, os
MOT = re.compile(rb'([\x01-\xff][\x80-\x8f])([\x00-\x01])\x00(..)\1', re.S)
def pat_eval(nm, runf=None, verbose=False):
    d = D[nm]; p = DUMPS + nm + '.dump.txt'
    if not os.path.exists(p): return []
    Dm = AK.parse(p); top = Dm.top(); ids = {x.name: x.id for x in top}
    pats = [f for f in top if f.type in ('MirrorPattern', 'CirPattern', 'LPattern')]
    if not pats: return []
    S = struct.unpack_from('<I', d, 0)[0]
    log = (runf or run)(d, S, len(d)); oi = objidx(d, log)
    res = []
    for f in pats:
        if f.id not in oi: continue
        h = oi[f.id][0]
        refs = [struct.unpack('<H', m.group(3))[0] for m in MOT.finditer(d, h.offset, h.region_end)]
        for pn, pt in f.parents:
            if pt == 'RefPlane' or ids.get(pn) not in oi: continue
            t = oi[ids[pn]][1]
            res.append((f.name, pn, pt, t, refs))
    return res
