"""MFC CArchive object / class numbering for the feature stream (round 7).

CArchive keeps one map for classes and objects.  Index 0 is the null object.
    FF FF <schema u16> <len u16> <name>   new class: class gets index n, the object n+1
    0x8000 | c                            new object of the class with index c: object gets n
    u16 r (1 <= r < 0x7FFF)               back-reference to object / class r (no new index)
    7F FF <u32>                           big form of either (index >= 0x7FFF)
The feature stream continues an archive that was started elsewhere: its first
u32 is the running map count, so the first ClassDef gets that index.  Class
indices below it ("external" classes, e.g. 0x8004 = the class of the CString
holder in every feature header) are defined in an earlier stream.

Layouts of most classes are unknown, so tags are found by scanning, with
filters for false positives:
  * a tag must name a known class (or an external one followed by a plausible field);
  * not inside an IEEE double (any covering 8-byte window decodes to 1e-9..1e7);
  * not the low half of a timestamp u32 (high half 0x4000..0x72FF);
and with resynchronisation: if a tag v names no class but a class defined
nearby (|v - c| <= RESYNC_W) whose first object starts with the same bytes as
those following the tag, the class's true index is v; numbering is redone from
that ClassDef.  The count is exact wherever both the start value and every tag
between are right; resyncs repair it at the next class that is reused.
"""
import re
import struct
from bisect import bisect_right
from dataclasses import dataclass

from .mfc import CLASSDEF as CD

REF = re.compile(rb'(?=([\x01-\xff][\x80-\xff]))', re.S)
BIG = re.compile(rb'\xff\x7f(..)([\x00-\x7f]\x80)', re.S)  # 7FFF + u32 0x8000_0000|class
RESYNC_W = 1000
SIG = 4
MIN_DISTINCT = 3
MIN_VOTES = 2


def u16(d, o): return struct.unpack_from('<H', d, o)[0]


def in_float(d, o):
    for w in range(max(0, o - 6), o + 1):
        if w + 8 > len(d):
            break
        x = abs(struct.unpack_from('<d', d, w)[0])
        if 1e-9 < x < 1e7:
            return True
    return False


def is_stamp(d, o):
    return o + 4 <= len(d) and 0x40 <= d[o + 3] <= 0x72


def ext_ok(d, o):
    if o + 4 > len(d):
        return False
    h = d[o + 3]
    if h in (0x00, 0x01, 0xff) or 0x80 <= h <= 0x8f:
        return True
    if d[o + 2:o + 5] == b'\xff\xfe\xff':                        # CString follows (holder objects)
        return True
    return _ext_id(d, o)


def _ext_id(d, o):
    # round 8: 'I 1 | T | u16 id | 00 00' (external id-object class, e.g. S-7): id high byte is free
    return d[o - 4:o] == b'\x01\x00\x00\x00' and d[o + 4:o + 6] == b'\x00\x00'


@dataclass
class Ev:
    offset: int
    end: int
    index: int          # map index: class index for 'def' (object = index + 1), object index for 'new'
    cls: int            # class index
    name: str           # class name ('' for external classes)
    kind: str           # 'def' | 'new'

    @property
    def obj(self):
        return self.index + 1 if self.kind == 'def' else self.index


ZBLOB = re.compile(rb'(?=....\x78[\x01\x5e\x9c\xda])', re.S)


def zblobs(d):
    """Round 8: embedded zlib blobs 'u32 n | n bytes zlib' (n bytes inflate exactly).  Their bytes
    are compressed payload, never tags; 513 blobs / 2.1 MB in 87 of the 131 files."""
    import zlib
    out, last = [], 0
    for m in ZBLOB.finditer(d):
        o = m.start()
        if o < last:
            continue
        n = struct.unpack_from('<I', d, o)[0]
        if not 8 < n <= len(d) - o - 4:
            continue
        try:
            z = zlib.decompressobj()
            z.decompress(d[o + 4:o + 4 + n])
        except zlib.error:
            continue
        if z.eof and not z.unused_data:
            out.append((o, o + 4 + n))
            last = o + 4 + n
    return out


def _events(d):
    ev = []
    bl = zblobs(d)
    bs = [a for a, b in bl]
    for m in CD.finditer(d):
        ln = m.group(2)[0]
        nm = m.group(3)[:ln]
        if len(nm) == ln:
            ev.append((m.start(), 0, ln, nm.decode()))
    for m in REF.finditer(d):
        o = m.start()
        j = bisect_right(bs, o) - 1
        if j >= 0 and o < bl[j][1]:
            continue
        ev.append((o, 1, u16(d, o) & 0x7fff, None))
    ev.sort()
    return ev


RESCUE = True


class _Rescue(frozenset):
    stampok = frozenset()


RESCUE_KNOWN = True
RESCUE_EXT = False
_rcache = {}


def repeats(d):
    """Round 8: offsets of tag candidates 0x8000|v that a filter would reject (inside a double,
    timestamp half, implausible external field) but whose following bytes repeat at another
    occurrence of the same v: (v, next 6 bytes) or (v, bytes 2..8 after the tag, i.e. skipping
    a free first u16 field such as an entity index or id) seen at least twice.  Data words
    rarely repeat with identical 6-byte context; real instances of a class do."""
    k = id(d)
    if k in _rcache and _rcache[k][0] is d:
        return _rcache[k][1]
    from collections import Counter
    c1, c2, pos = Counter(), Counter(), []
    for m in REF.finditer(d):
        o = m.start()
        v = u16(d, o)
        if v == 0xffff or o + 10 > len(d):
            continue
        a, b = d[o + 2:o + 8], d[o + 4:o + 10]
        pos.append((o, v, a, b))
        c1[(v, a)] += 1
        c2[(v, b)] += 1

    def okkey(x):
        return len(set(x)) >= 2 and x.count(0) <= 4
    out = _Rescue(o for o, v, a, b in pos
                  if (c1[(v, a)] >= 2 and okkey(a)) or (c2[(v, b)] >= 2 and okkey(b)))
    # timestamp-like candidates (next byte pair = high half of a stamp) only on the second key
    out.stampok = frozenset(o for o, v, a, b in pos if c2[(v, b)] >= 2 and okkey(b) and c1[(v, a)] < 3)
    if len(_rcache) > 8:
        _rcache.clear()
    _rcache[k] = (d, out)
    return out


def number(d, fix=None, start=None, ev=None, reject=frozenset(), look=False):
    """One numbering pass. fix: {classdef offset: forced class index}."""
    fix = fix or {}
    rescue = repeats(d) if RESCUE else frozenset()
    start = struct.unpack_from('<I', d, 0)[0] if start is None else start
    ev = ev if ev is not None else _events(d)
    cnt, classes, i, out = start, {}, 0, []
    resid = number.residuals = []
    for o, k, a, nm in ev:
        if o < i or (o in reject and not (k and REJ_IDREP and a in classes and classes[a].endswith('IdRep_c')
                                              and _idrep_ok(d, o, classes, cnt))):
            continue
        if k == 0:
            if o in fix:
                resid.append((o, fix[o] - cnt))
                cnt = fix[o]
            elif look:
                cnt = _lookahead(d, o + 6 + a, cnt, classes, start)
            classes[cnt] = nm
            out.append(Ev(o, o + 6 + a, cnt, cnt, nm, 'def'))
            cnt += 2
            i = o + 6 + a
            continue
        after_def = o == i and bool(out)
        if a in classes:
            ok = after_def or not (in_float(d, o) or is_stamp(d, o))
            # round 9: 'T | u16 objref >= 0x4000 | next tag' looks like a stamp half in big parts
            if not ok and not in_float(d, o) and o + 6 <= len(d) and 0x80 <= d[o + 5] <= 0x8f \
                    and u16(d, o + 2) < cnt and (u16(d, o + 4) & 0x7fff) in classes:
                ok = True
        elif 0 < a < start:
            ok = after_def or (ext_ok(d, o) and not in_float(d, o))
        else:
            ok = False
        if not ok and IDREP_RESCUE and 0 < a < start and (_fr_like(d, o + 2, cnt) or _ext_idrep(d, o, cnt)
                                                         or _ext_list(d, o, a, start, classes)):
            ok = True
        if not ok and IDREP_RESCUE and a in classes and not in_float(d, o) and _idrep_ok(d, o, classes, cnt):
            ok = True
        if not ok and STRUCT_RESCUE and _struct_ok(d, o, classes):
            ok = True
        if not ok and o in rescue and (not is_stamp(d, o) or o in rescue.stampok) and ((a in classes and RESCUE_KNOWN) or (0 < a < start and RESCUE_EXT)):
            ok = True
        if ok:
            out.append(Ev(o, o + 2, cnt, a, classes.get(a, ''), 'new'))
            cnt += 1
            i = o + 2
    return out


IDREP_RESCUE = True
REJ_IDREP = False  # round 12: tried, corpus seeds 20 -> 18
PBUD_KEEP = False      # round 14: never outlier-reject a struct-valid moPointBackedUpData_c tag.
#   v2 |drift| 52 -> 26, corpus 397 -> 280, vert2_v2ch residual 1663 -> 10, but exact seeds
#   v2 14/22 -> 14/22, corpus 20/76 -> 18/76 (MB hub 0 -> -3, Micron 0 -> -1): off by default.
STRUCT_RESCUE = True   # round 12: fixed-layout classes whose tags the float/stamp/outlier filters reject


def _f64ok(x):
    return x == 0.0 or 1e-9 < abs(x) < 1e4


def _pbud(d, o):
    """moPointBackedUpData_c: 'tag | f64 x | f64 y | u16 0' (2-D sketch point; positive x with a
    0x3f.. high byte puts 0x40-0x72 at tag+3, which the stamp filter took for a timestamp)."""
    if o + 20 > len(d):
        return False
    x, y = struct.unpack_from('<dd', d, o + 2)
    return _f64ok(x) and _f64ok(y) and d[o + 18:o + 20] == b'\0\0'


STRUCTS = {'moPointBackedUpData_c': _pbud}


def _struct_ok(d, o, classes):
    f = STRUCTS.get(classes.get(u16(d, o) & 0x7fff, ''))
    return bool(f) and f(d, o)
STAMP_LO, STAMP_HI = 1_400_000_000, 1_900_000_000


def _fr_like(d, o, cnt):
    """moFR_c body 'u16 docref < count | u32 fid | u32 stamp' (external moFR_c-class objects)."""
    if o + 10 > len(d):
        return False
    r, fid, st = struct.unpack_from('<HII', d, o)
    return 0 < r < cnt and 0 < fid < 1 << 16 and STAMP_LO < st < STAMP_HI


def _ext_idrep(d, o, cnt):
    """external IdRep object: 'tag | u16 | moFR-class tag | moFR body' (seen in prefs as 03 80 00 00 05 80 ...)."""
    if o + 16 > len(d):
        return False
    v = u16(d, o + 4)
    return bool(v & 0x8000) and v != 0xffff and _fr_like(d, o + 6, cnt)


def _ext_list(d, o, a, start, classes):
    """object list S-28/S-29: 'tag | u16 n (1..32) | first item = new-object tag of a known/external class'."""
    if a not in (start - 28, start - 29) or o + 6 > len(d):
        return False
    n, v = u16(d, o + 2), u16(d, o + 4)
    return 1 <= n <= 32 and bool(v & 0x8000) and v != 0xffff and ((v & 0x7fff) in classes or 0 < (v & 0x7fff) < start)


def _idrep_ok(d, o, classes, cnt):
    """Round 11b (struct rule from DumpV3 pref archives): an '*IdRep_c' object is 'tag | u16 (00 00 in prefs)'
    followed by its moFR_c child 'tag | u16 docref | u32 fid | u32 stamp'; a moFR_c tag is
    'tag | u16 docref < count | u32 fid | u32 stamp'.  Such tags are real even when the
    float / stamp filters reject them."""
    nm = classes.get(u16(d, o) & 0x7fff, '')
    if nm == 'moFR_c':
        if o + 12 > len(d):
            return False
        r, fid, st = struct.unpack_from('<HII', d, o + 2)
        return r < cnt and 0 < fid < 1 << 20 and STAMP_LO < st < STAMP_HI
    if nm.endswith('IdRep_c') and o + 6 <= len(d):
        v = u16(d, o + 4)
        return bool(v & 0x8000) and classes.get(v & 0x7fff) == 'moFR_c' and _idrep_ok(d, o + 4, classes, cnt)
    return False


LOOK_W = 400
LOOK_K = 4


def _lookahead(d, e, pred, classes, start):
    """True index of the class whose first object starts at e: the value v of later tags
    0x8000|v that are followed by the same LOOK_K bytes, if they agree and differ from pred."""
    sig = d[e:e + LOOK_K]
    if len(sig) < LOOK_K or len(set(sig)) < MIN_DISTINCT:
        return pred
    from collections import Counter
    c = Counter()
    j = d.find(sig, e + 1)
    while j >= 0:
        v = struct.unpack_from('<H', d, j - 2)[0]
        if v & 0x8000:
            v &= 0x7fff
            if abs(v - pred) <= LOOK_W and v >= start and (v == pred or v not in classes):
                c[v] += 1
        j = d.find(sig, j + 1)
    if not c:
        return pred
    v, n = c.most_common(1)[0]
    if v != pred and n >= MIN_VOTES and n > 2 * c.get(pred, 0):
        return v
    return pred


def _sig(d, e):
    return d[e:e + SIG]


def outliers(d, out):
    """tags whose following u16 is unlike every other instance of the class (likely data, not a tag)"""
    from collections import Counter, defaultdict
    prof = defaultdict(Counter)
    first = {}
    for e in out:
        nx = d[e.end:e.end + 2]
        if e.kind == 'def':
            first[e.cls] = nx
        prof[e.cls][nx] += 1
    bad = set()
    rescue = repeats(d) if RESCUE else _Rescue()
    keep = {e.offset for e in out if PBUD_KEEP and e.kind == 'new' and e.name == 'moPointBackedUpData_c' and _pbud(d, e.offset)}
    for e in out:
        if e.kind != 'new' or e.offset in rescue or e.offset in keep or _ext_id(d, e.offset):
            continue
        nx = d[e.end:e.end + 2]
        if len(nx) < 2 or nx == first.get(e.cls) or prof[e.cls][nx] > 1:
            continue
        if nx[1] in (0x00, 0x01, 0xff) or 0x80 <= nx[1] <= 0x8f:
            continue
        bad.add(e.offset)
    return bad


def numbering(d, max_fix=400, prune=True, look=False, dp=True, dp_iters=4):
    """Numbering with resynchronisation, then (round 8) the global class-index assignment
    (assign_classes) repeated until stable.  Returns (events, fixes).  After the call,
    numbering.residual = total |forced - counted| over the fixed ClassDefs (objects the counter
    could not account for; 0 = self-consistent)."""
    out, fix = _numbering7(d, max_fix, prune, look)
    if dp:
        S = struct.unpack_from('<I', d, 0)[0]
        ev = _events(d)
        for _ in range(dp_iters):
            f2 = assign_classes(d, out)
            cur = {e.offset: e.index for e in out if e.kind == 'def'}
            f2 = {o: v for o, v in f2.items() if cur.get(o) != v}
            if not f2:
                break
            fix = {**fix, **f2}
            out = number(d, fix, S, ev, _numbering7.reject)
    numbering.residual = sum(abs(r) for _, r in number.residuals)
    numbering.residuals = list(number.residuals)
    return out, fix


def _numbering7(d, max_fix=400, prune=True, look=False):
    """Round-7 numbering with resynchronisation. Returns (events, fixes)."""
    start = struct.unpack_from('<I', d, 0)[0]
    ev = _events(d)
    fix = {}
    reject = frozenset()
    if prune:
        for _ in range(3):
            r2 = reject | outliers(d, number(d, fix, start, ev, reject, look))
            if r2 == reject:
                break
            reject = frozenset(r2)
    for _ in range(max_fix):
        out = number(d, fix, start, ev, reject, look)
        defs = [e for e in out if e.kind == 'def']
        by_idx = {e.index: e for e in defs}
        sigs = {e.index: _sig(d, e.end) for e in defs}
        accepted = {e.offset for e in out}
        doffs = [e.offset for e in defs]
        bysig = {}
        for c, sg in sigs.items():
            bysig.setdefault(sg, []).append(c)
        ch = None
        votes = {}
        for o, k, a, _ in ev:
            if k != 1 or o in accepted or a < start or a in by_idx:
                continue
            if in_float(d, o) or is_stamp(d, o):
                continue
            nxt = d[o + 2:o + 2 + SIG]
            if len(set(nxt)) < MIN_DISTINCT:
                continue
            # a class defined before o, near index a, whose first object starts with the same bytes
            cands = [c for c in bysig.get(nxt, ()) if abs(c - a) <= RESYNC_W and by_idx[c].offset < o]
            if len(cands) == 1 and by_idx[cands[0]].offset not in fix:
                key = (by_idx[cands[0]].offset, a)
                votes.setdefault(key, []).append(o)
                if len(votes[key]) >= MIN_VOTES:
                    ch = key
                    break
        if ch is None:
            _numbering7.reject = reject
            return out, fix
        fix[ch[0]] = ch[1]
    _numbering7.reject = reject
    return number(d, fix, start, ev, reject, look), fix


# ------------------------------------------------------------------ round 8: global class-index assignment
DP_W = 32          # bytes of the first object compared with instance bytes
DP_MINSIM = 0.35   # trigram Jaccard for an instance to count as evidence
DP_LAM = 0.15      # penalty per sqrt(jump size)
DP_BEAM = 60
DP_UBK = 8          # jump bound: tag-like words since the DP_UBK-th previous def


def _tag_candidates(d, S):
    occ = {}
    bl = zblobs(d)
    bs = [a for a, b in bl]
    for m in REF.finditer(d):
        o = m.start()
        j = bisect_right(bs, o) - 1
        if j >= 0 and o < bl[j][1]:
            continue
        v = u16(d, o) & 0x7fff
        if v < S or v == 0x7fff or in_float(d, o) or is_stamp(d, o):
            continue
        occ.setdefault(v, []).append(o)
    return occ


def assign_classes(d, base):
    """{ClassDef offset: class index} chosen jointly for all ClassDefs.

    Each ClassDef k gets index t_k.  By default t_k - t_{k-1} is the number of objects our
    counter saw between the two definitions; t_k may instead jump to a tag value v whose later
    occurrences 0x8000|v are followed by bytes resembling the def's first object (trigram
    similarity of DP_W bytes).  A beam search maximises total evidence minus a jump penalty,
    with t increasing by >= 2 per def and at most the number of tag-like words in between.
    This fixes classes whose first object has no distinctive 4-byte signature (zero-led
    objects such as moDisplayDistanceDim_c), where the round-7 resync could not vote."""
    from bisect import bisect_left
    S = struct.unpack_from('<I', d, 0)[0]
    defs = [e for e in base if e.kind == 'def']
    if not defs:
        return {}
    occ = _tag_candidates(d, S)
    allpos = sorted(p for ps in occ.values() for p in ps)
    by2 = {}
    for v, ps in occ.items():
        if len(ps) >= 2:
            for p in ps:
                by2.setdefault(d[p + 2:p + 4], []).append((p, v))
    gcache = {}

    def g(p):
        x = gcache.get(p)
        if x is None:
            b = d[p:p + DP_W]
            x = gcache[p] = {b[i:i + 3] for i in range(len(b) - 2)}
        return x
    cand = []
    for e in defs:
        ge = g(e.end)
        per = {}
        for p, v in by2.get(d[e.end:e.end + 2], ()):
            if p > e.end:
                l = per.setdefault(v, [])
                if len(l) < 8:
                    l.append(p)
        cs = []
        for v, ps in per.items():
            ss = []
            for p in ps:
                gp = g(p + 2)
                u = len(ge | gp)
                ss.append(len(ge & gp) / u if u else 0)
            good = sum(1 for x in ss if x >= DP_MINSIM)
            if good:
                cs.append((v, min(good, 4) * max(ss)))
        cs.sort(key=lambda x: -x[1])
        cand.append(dict(cs[:40]))
    assign_classes.cand = cand
    assign_classes.defs = defs
    states = {defs[0].index: (0.0, ())}
    for k, e in enumerate(defs):
        dc = e.index - defs[k - 1].index if k else 0
        ub = bisect_left(allpos, e.offset) - bisect_left(allpos, defs[max(0, k - DP_UBK)].offset) if k else 0
        new = {}
        for lv, (sc, path) in states.items():
            pred = lv + dc
            t = (sc + cand[k].get(pred, 0), path)
            if pred not in new or new[pred][0] < t[0]:
                new[pred] = t
            for v, s_ in cand[k].items():
                if v == pred or v < lv + 2 or (k and v > lv + 2 + ub + dc):
                    continue
                t = (sc + s_ - DP_LAM * abs(v - pred) ** 0.5 - 1.0, path + ((k, v),))
                if v not in new or new[v][0] < t[0]:
                    new[v] = t
        states = dict(sorted(new.items(), key=lambda x: -x[1][0])[:DP_BEAM])
    sc, path = max(states.values())
    return {defs[k].offset: v for k, v in path}


def object_at(events, offset):
    """object index of the record that starts at/just before offset (feature header CString)."""
    offs = [e.offset for e in events]
    j = bisect_right(offs, offset) - 1
    while j >= 0 and events[j].kind == 'new' and events[j].end == offset and not events[j].name:
        j -= 1          # the external 0x8004-type holder object directly before the CString
    return events[j].obj if j >= 0 else None


# ------------------------------------------------------------------ feature objects and object refs
NON_SEED = ('Folder', 'moRefPlane_c', 'moProfileFeature_c', 'moOriginProfileFeature_c', 'moDetailCabinet_c',
            'moNotesAreaFtrFolder_c', 'moCommentsFolder_c', 'moFavoriteFolder_c', 'moHistoryFolder_c')


def feature_objects(d, headers, events):
    """feature id -> (header, object index, class name) for the first header of each feature."""
    offs = [e.offset for e in events]
    out = {}
    for h in headers:
        if h.feature_id in out:
            continue
        j = bisect_right(offs, h.offset) - 1
        while j >= 0 and events[j].kind == 'new' and events[j].end == h.offset and not events[j].name:
            j -= 1
        if j >= 0:
            out[h.feature_id] = (h, events[j].obj, events[j].name)
    return out


LIST_KS = (28, 29, 27)


def list_class_tags(d):
    """the stream's object-list class: external class S-28 or S-29 (moFeatureList-like, 'T u16 n, n items')."""
    S = struct.unpack_from('<I', d, 0)[0]
    # round 12: S-27 in small A/B mirror parts (Mirror-only files define one class fewer before the list)
    return [struct.pack("<H", 0x8000 | (S - k)) for k in LIST_KS]


def seed_list(d, h):
    """object back-references of the first object list in a pattern / mirror region (the seed features)."""
    best = None
    for t in list_class_tags(d):
        j = d.find(t, h.offset, h.region_end)
        while j >= 0:
            n = u16(d, j + 2)
            if 1 <= n <= 32 and j + 4 + 2 * n <= len(d):
                refs = list(struct.unpack_from('<%dH' % n, d, j + 4))
                if all(0 < r < 0x7fff for r in refs):
                    if best is None or j < best[0]:
                        best = (j, refs)
                    break
            j = d.find(t, j + 1, h.region_end)
    return best[1] if best else []


def resolve_objects(refs, fobj, before):
    """map object indices to the feature whose object index is nearest (numbering drifts by a few
    objects in large parts; feature objects are tens to hundreds of indices apart)."""
    cand = [(i, fid) for fid, (h, i, cls) in fobj.items()
            if h.offset < before and i is not None and not any(x in cls for x in NON_SEED)]
    out = []
    for r in refs:
        if not cand:
            out.append(None)
            continue
        i, fid = min(cand, key=lambda x: abs(x[0] - r))
        out.append((fid, r - i))
    return out


# ------------------------------------------------------------------ object tree
@dataclass
class Obj:
    index: int
    cls: int
    name: str           # class name, 'ext#<n>' for classes defined in an earlier stream
    start: int          # tag offset
    end: int            # next tag (objects are serialised depth-first, so a parent's own
                        # fields are the bytes up to its first child tag)
    parent: int = None  # index of the enclosing object (feature header object for top level)


def objects(d, events, headers=None):
    """Every numbered object with its class and byte span [start, next tag).  Objects are
    nested under the feature whose header precedes them (feature tree level)."""
    out = []
    hoffs = sorted(h.offset for h in (headers or []))
    S = struct.unpack_from('<I', d, 0)[0]
    for k, e in enumerate(events):
        end = events[k + 1].offset if k + 1 < len(events) else len(d)
        out.append(Obj(e.obj, e.cls, e.name or 'ext[S-%d]' % (S - e.cls), e.offset, end))
    if hoffs:
        owner, hi = None, 0
        for o in out:
            # the object whose span contains a feature header CString is that feature's object
            while hi < len(hoffs) and hoffs[hi] < o.start:
                hi += 1
            o.parent = owner
            if hi < len(hoffs) and o.start <= hoffs[hi] < o.end + 2:
                owner = o.index
                o.parent = None
    return out


def class_bytes(d, objs, explained=()):
    """per class: (total bytes, unexplained bytes) given explained spans [(a, b)]."""
    return _class_bytes(d, objs, explained)


def _class_bytes(d, objs, explained):
    mask = bytearray(len(d))
    for a, b in explained:
        a, b = max(0, a), min(len(d), b)
        if b > a:
            mask[a:b] = b'\x01' * (b - a)
    out = {}
    for o in objs:
        tot = o.end - o.start
        une = tot - mask[o.start:o.end].count(1)
        t = out.setdefault(o.name, [0, 0, 0])
        t[0] += tot
        t[1] += une
        t[2] += 1
    return out
